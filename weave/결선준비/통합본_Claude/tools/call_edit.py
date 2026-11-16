#!/usr/bin/env python3
"""2쪽 통화 음성에서 말을 덜어 내고 조금 빠르게 한다 → out/_call_edit.wav (그 뒤 call_gain.py가 크기와 받는 소리를 손봄)

  python tools/call_edit.py <원본 wav> [--tempo 1.15]
  python tools/call_gain.py out/_call_edit.wav --gain 6 --ring 5.5 --click 1.65 --click-gap 0.63

11월 16일: '두 번째 장 음성에서도 소속 빼 줘. "안녕하세요 양서윤 프로입니다."로. 아.. 네.. 음.. 만 말하고 속도 1.1~1.2배 정도로 빠르고 자연스럽게,
편집 힘들면 음성 수정 예정'이라는 검토를 받고 만듦. 원본은 Carbon이 다듬은 최종후보 B(wav, 44.1kHz 모노).
녹음에 없는 말('안녕하세요')은 만들 수 없어서, 있는 말을 덜어 내는 데까지만 한다:
  "네, 삼성리서치 양서윤 프로입니다."  →  "네, 양서윤 프로입니다."     ('삼성리서치' 2.16~2.94초를 덜어 냄. 두 낱말 사이의 조용한 틈은 2.82~2.91초인데,
                                                                    그 바로 뒤 2.91~2.94초에 '치'에서 '양'으로 넘어가는 여린 소리가 남아 2.86초나 2.90초에서 이으면
                                                                    받아쓰기가 '네, 지의 양서윤'으로 들었다. 2.93~2.96초에서 이으면 '네, 양서윤 프로입니다.')
  "어... 네.. 그거요...?"              →  "어... 네.."                   ('그거요...?' 8.10~8.84초를 덜어 냄. 앞뒤가 모두 조용한 자리)
  "아... 잠깐만요, 찾아보고 다시 알려 드릴게요."는 그대로.
그다음 목소리 구간(첫마디 바로 앞 1.60초부터 끊는 소리 앞 13.40초까지, 말 사이의 쉼도 함께)을 --tempo배 빠르게 한다(높낮이는 그대로: ffmpeg atempo).
통화 연결음과 받는 소리, 끊는 소리는 그대로 둔다. 자르는 때는 기기 안의 받아쓰기(낱말마다의 때)와 10ms마다 잰 소리 크기로 잡았다.
"""
import argparse
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
DST = HERE / 'out' / '_call_edit.wav'
FFMPEG = str(Path.home() / '.cache' / 'weave-tools' / 'bin' / 'ffmpeg')
CUTS = [(2.16, 2.94, 0.010), (8.10, 8.84, 0.006)]      # 덜어 내는 구간(원본의 초)과 그 뒤 소리를 키우는 길이(초): '삼성리서치', '그거요...?'
VOICE = (1.60, 13.40)                     # 빠르게 하는 구간(원본의 초): 첫마디 '네' 바로 앞 ~ 끊는 소리 앞의 조용한 자리
FADE = 0.006                              # 이음매 앞에서 소리를 줄이는 길이(초). 자르는 자리는 모두 조용한 곳이라 짧게


def tempo(x, sr, k):
    """x를 k배 빠르게(높낮이는 그대로)."""
    out = subprocess.run([FFMPEG, '-loglevel', 'error', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', 'pipe:0',
                          '-af', 'atempo=%.4f' % k, '-f', 'f32le', '-ar', str(sr), '-ac', '1', 'pipe:1'],
                         input=x.astype('<f4').tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype='<f4').astype(np.float64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('--tempo', type=float, default=1.15)
    a = ap.parse_args()
    with wave.open(a.src, 'rb') as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2, '모노 16비트 wav'
        sr, n = w.getframerate(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768
    nf = int(FADE * sr)
    ramp = np.linspace(1, 0, nf)
    parts, at, v0, v1, fin = [], 0.0, VOICE[0], VOICE[1], 0
    for c0, c1, up in CUTS:
        seg = x[int(at * sr):int(c0 * sr)].copy()
        seg[-nf:] *= ramp                               # 덜어 내는 자리 앞은 줄이고
        if fin:
            seg[:fin] *= np.linspace(0, 1, fin)         # 앞에서 덜어 낸 자리 뒤는 키움
        parts.append(seg)
        at, fin = c1, int(up * sr)
        v1 -= c1 - c0                                   # 덜어 낸 만큼 목소리 구간의 끝이 앞당겨짐
    tail = x[int(at * sr):].copy()
    tail[:fin] *= np.linspace(0, 1, fin)
    parts.append(tail)
    y = np.concatenate(parts)
    i0, i1 = int(v0 * sr), int(v1 * sr)
    assert np.abs(y[i0 - nf:i0 + nf]).max() < 0.01 and np.abs(y[i1 - nf:i1 + nf]).max() < 0.01, '빠르게 하는 구간의 끝이 조용한 자리가 아님'
    fast = tempo(y[i0:i1], sr, a.tempo)
    z = np.concatenate([y[:i0], fast, y[i1:]])
    DST.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(DST), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(z, -1, 1) * 32767).astype('<i2').tobytes())
    print('길이 %.3f초 → 덜어 낸 뒤 %.3f초 → %.2f배 빠르게 %.3f초' % (n / sr, len(y) / sr, a.tempo, len(z) / sr))
    print('목소리 구간 %.2f~%.2f초(%.2f초) → %.2f초. 첫마디는 %.3f초쯤' % (v0, v1, v1 - v0, len(fast) / sr, v0 + (1.65 - v0) / a.tempo))
    print('→', DST)


if __name__ == '__main__':
    sys.exit(main())
