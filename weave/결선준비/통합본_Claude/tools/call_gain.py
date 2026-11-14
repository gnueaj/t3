#!/usr/bin/env python3
"""2쪽 통화 음성의 목소리를 키운다 → assets/intro/call-hook.mp3

  python tools/call_gain.py <원본 wav> [--gain 6] [--from 1.3]

원본(Carbon이 다듬은 최종후보 B의 wav)은 통화 연결음이 크고(-13.9 LUFS) 그 뒤의 목소리가 작다(-21.9 LUFS. 낭독은 -16 LUFS).
연결음까지 함께 키우면 연결음만 더 커지므로, 연결음이 끝난 뒤(--from 초)부터만 --gain dB를 올린다(연결음과 목소리 사이의 빈 곳 0.2초에 걸쳐 서서히).
목소리의 높은 봉우리는 넘치지 않게 눌러 준다(ffmpeg alimiter, -1 dBFS). 길이와 말하는 때는 그대로라 make.py의 CALL_LEN, CALL_LINES는 바꾸지 않는다.

11월 15일: '첫 통화 부분 볼륨만 살짝 높여서 … 지금은 잘 안 들리네'라는 검토를 받고 만듦.
"""
import argparse
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
DST = HERE / 'assets' / 'intro' / 'call-hook.mp3'
TMP = HERE / 'out' / '_call_gain.wav'
FFMPEG = str(Path.home() / '.cache' / 'weave-tools' / 'bin' / 'ffmpeg')
RAMP = 0.2                          # 키우기 시작해서 다 키울 때까지(초)
LIMIT = 0.89                        # 봉우리의 위 끝(-1 dBFS)


def lufs(path, ss=None, t=None):
    """integrated loudness(LUFS). ss, t를 주면 그 구간만."""
    cmd = [FFMPEG, '-hide_banner'] + (['-ss', str(ss)] if ss is not None else []) + (['-t', str(t)] if t else []) + ['-i', str(path), '-af', 'ebur128', '-f', 'null', '-']
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', err)[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('--gain', type=float, default=6.0, help='목소리를 키우는 만큼(dB)')
    ap.add_argument('--from', dest='start', type=float, default=1.3, help='이때(초)부터 키움: 통화 연결음이 끝난 뒤')
    a = ap.parse_args()
    with wave.open(a.src, 'rb') as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2, '모노 16비트 wav'
        sr, n = w.getframerate(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768
    t = np.arange(n) / sr
    g = 10 ** (a.gain / 20)
    env = 1 + (g - 1) * np.clip((t - a.start) / RAMP, 0, 1)
    y = x * env                                         # 봉우리는 1을 넘을 수 있음 → 32비트 실수 wav로 넘겨 ffmpeg가 누르게 함
    TMP.parent.mkdir(parents=True, exist_ok=True)
    raw = TMP.with_suffix('.f32')
    y.astype('<f4').tofile(raw)
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', str(raw),
                    '-af', 'alimiter=limit=%.2f:attack=5:release=60:level=false:latency=true' % LIMIT, '-c:a', 'pcm_s16le', str(TMP)], check=True)
    raw.unlink()
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-i', str(TMP), '-ac', '1', '-ar', '44100', '-c:a', 'libmp3lame', '-q:a', '2', str(DST)], check=True)
    with wave.open(str(TMP), 'rb') as w:
        z = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    k = min(len(z), n)
    voice = slice(int((a.start + RAMP) * sr), k)
    print('길이 %.3f초 → %.3f초, 봉우리 %.2f → %.2f' % (n / sr, len(z) / sr, np.abs(x).max(), np.abs(z).max()))
    print('목소리(%.1f초부터): %.1f → %.1f LUFS, 연결음: %.1f → %.1f LUFS' % (
        a.start + RAMP, lufs(a.src, a.start + RAMP), lufs(TMP, a.start + RAMP), lufs(a.src, 0, a.start), lufs(TMP, 0, a.start)))
    print('눌린 정도: 목소리의 크기가 gain보다 %.1f dB 덜 커짐' % (a.gain - 20 * np.log10(np.sqrt((z[voice] ** 2).mean()) / np.sqrt((x[voice] ** 2).mean()))))
    print('→', DST, '%.0f KB' % (DST.stat().st_size / 1e3))


if __name__ == '__main__':
    main()
