#!/usr/bin/env python3
"""2쪽 통화 음성의 목소리와 연결음을 키우고 받는 소리를 넣는다 → assets/intro/call-hook.mp3

  python tools/call_gain.py <원본 wav> [--gain 6] [--ring 5.5] [--from 1.3] [--click 1.666 --click-gap 0.63]

원본(Carbon이 다듬은 최종후보 B의 wav)은 통화 연결음이 크고(-13.9 LUFS) 그 뒤의 목소리가 작다(-21.9 LUFS. 낭독은 -16 LUFS).
연결음까지 함께 키우면 연결음만 더 커지므로, 연결음이 끝난 뒤(--from 초)부터만 --gain dB를 올린다(연결음과 목소리 사이의 빈 곳 0.2초에 걸쳐 서서히).
목소리의 높은 봉우리는 넘치지 않게 눌러 준다(ffmpeg alimiter, -1 dBFS). 길이와 말하는 때는 그대로라 make.py의 CALL_LEN, CALL_LINES는 바꾸지 않는다.

11월 15일: '첫 통화 부분 볼륨만 살짝 높여서 … 지금은 잘 안 들리네'라는 검토를 받고 만듦.
그 뒤 '벨소리 살짝만 더 크게, 뚜루루 소리 약간 작은 듯': 목소리를 키우고 나니 연결음이 견주어 작게 들려서 연결음도 따로 키울 수 있게 함(--ring dB).
그 뒤 '벨소리 약간만 더 키워 주고, 받을 때 딸깍(받는 소리)이 명확히 있고 딜레이 0.2초 정도 주고 말하는 게 자연스러울 것 같아':
원본의 받는 소리는 1.24초에 0.01초 동안 나는 작은 '틱' 하나(봉우리 0.2)였고 첫마디 '네'(1.666초)는 그 0.43초 뒤였다.
--click <첫마디가 시작하는 때>를 주면 그 '틱'을 지우고 '딸깍'(짧은 부딪힘 둘, pickup_click)을 넣는다.
연결음은 봉우리가 넘치지 않는 데까지(--ring 5.5, 봉우리 0.88).
처음에는 '딜레이 0.2초'를 딸깍에서 첫마디까지 0.2초로 읽어 그렇게 만들었는데(길이는 그대로), '0.2초 더 주라는 거였는데? 그럼 총 0.7초 정도 되겠지':
있던 틈(0.43초)에 0.2초를 더하라는 뜻이었다. 딸깍은 연결음 0.23초 뒤에 두고, 딸깍이 끝나고 첫마디까지를 --click-gap 0.63으로
(딸깍의 첫 소리부터는 0.74초). 모자라는 만큼(0.43초)은 딸깍과 첫마디 사이의 조용한 바닥을 이어 붙여 늘린다.
그래서 길이가 14.02초 → 14.45초가 되고 말하는 때가 모두 0.43초 늦어진다 → make.py의 CALL_LEN, CALL_LINES도 그만큼 옮긴다.
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
RING_END = 1.13                     # 연결음이 끝난 때(초). 여기서 딸깍 앞까지는 조용히 비움(원본의 옛 '틱'과 숨소리가 있던 자리)
CLICK_AFTER = 0.231                 # 연결음이 끝나고 딸깍까지(초)
CLICK_GAP = 0.085                   # 딸과 깍 사이(초)
CLICK_PEAK = 0.85                   # 딸깍의 봉우리(깍). 딸은 그 0.75배


def lufs(path, ss=None, t=None):
    """integrated loudness(LUFS). ss, t를 주면 그 구간만."""
    cmd = [FFMPEG, '-hide_banner'] + (['-ss', str(ss)] if ss is not None else []) + (['-t', str(t)] if t else []) + ['-i', str(path), '-af', 'ebur128', '-f', 'null', '-']
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', err)[-1])


def band_noise(rng, n, lo, hi, sr):
    """lo~hi Hz 띠 안의 잡음(가장자리는 부드럽게), 봉우리 1"""
    F = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / sr)
    w = (hi - lo) * 0.18
    m = np.clip((f - (lo - w)) / w, 0, 1) * np.clip(((hi + w) - f) / w, 0, 1)
    y = np.fft.irfft(F * np.sin(m * np.pi / 2) ** 2, n)
    return y / np.abs(y).max()


def hit(rng, sr, band, tau, length=0.06):
    """한 번 부딪히는 소리: 띠 안의 잡음 한 줌이 tau(초)로 사그라듦. 울림(sin)을 섞으면 나무토막 소리처럼 들려서 잡음만 씀
    (기기 안의 AST·CLAP 판정: 울림을 섞은 안은 'wood block'·'Plop', 잡음만 쓴 안은 'a click'·'Tick')."""
    n = int(length * sr)
    t = np.arange(n) / sr
    return band_noise(rng, n, band[0], band[1], sr) * np.exp(-t / tau) * (1 - np.exp(-t / 0.00012))


def pickup_click(sr, peak=CLICK_PEAK, seed=7):
    """받는 소리 '딸깍': 밝고 짧은 '딸'(바로 뒤에 작게 한 번 더 튐) → 0.085초 → 조금 낮고 센 '깍'. 전화선의 띠(300~4200 Hz)를 거침.
    돌려줌: (소리, 들리는 길이(초): 봉우리의 3%보다 큰 마지막 때까지)"""
    from scipy.signal import butter, sosfilt
    rng = np.random.default_rng(seed)
    y = np.zeros(int((CLICK_GAP + 0.08) * sr))

    def put(at, amp, h):
        i = int(at * sr)
        y[i:i + len(h)] += amp * h[:len(y) - i] / np.abs(h).max()
    put(0.0, 0.75, hit(rng, sr, (1800, 4200), 0.0026))
    put(0.0065, 0.36, hit(rng, sr, (1800, 4200), 0.0021))
    put(CLICK_GAP, 1.0, hit(rng, sr, (950, 3600), 0.0048))
    y = sosfilt(butter(2, [300, 4200], btype='band', fs=sr, output='sos'), y)
    y *= peak / np.abs(y).max()
    return y, (np.nonzero(np.abs(y) > 0.03 * peak)[0][-1] + 1) / sr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('--gain', type=float, default=6.0, help='목소리를 키우는 만큼(dB)')
    ap.add_argument('--ring', type=float, default=0.0, help='통화 연결음(--from 앞)을 키우는 만큼(dB)')
    ap.add_argument('--from', dest='start', type=float, default=1.3, help='이때(초)부터 목소리: 통화 연결음이 끝난 뒤')
    ap.add_argument('--click', type=float, default=0.0, help="받는 소리 '딸깍'을 넣음: 첫마디가 시작하는 때(초). 0이면 넣지 않음")
    ap.add_argument('--click-gap', type=float, default=0.63, help='딸깍이 끝나고 첫마디까지(초). 원본에 그만한 틈이 없으면 첫마디와 그 뒤를 늦춤')
    a = ap.parse_args()
    with wave.open(a.src, 'rb') as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2, '모노 16비트 wav'
        sr, n = w.getframerate(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768
    t = np.arange(n) / sr
    g, gr = 10 ** (a.gain / 20), 10 ** (a.ring / 20)
    env = gr + (g - gr) * np.clip((t - a.start) / RAMP, 0, 1)      # 연결음은 gr배, 그 뒤 0.2초에 걸쳐 g배로
    y = x * env                                         # 봉우리는 1을 넘을 수 있음 → 32비트 실수 wav로 넘겨 ffmpeg가 누르게 함
    TMP.parent.mkdir(parents=True, exist_ok=True)
    raw = TMP.with_suffix('.f32')
    y.astype('<f4').tofile(raw)
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', str(raw),
                    '-af', 'alimiter=limit=%.2f:attack=5:release=60:level=false:latency=true' % LIMIT, '-c:a', 'pcm_s16le', str(TMP)], check=True)
    raw.unlink()
    with wave.open(str(TMP), 'rb') as w:
        z = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    if a.click:
        c, heard = pickup_click(sr)
        t0 = RING_END + CLICK_AFTER                         # 딸이 시작하는 때
        late = t0 + heard + a.click_gap - a.click           # 첫마디를 늦춰야 하는 만큼(초)
        if late < 0:                                        # 틈이 남으면 딸깍을 첫마디 쪽으로 옮김
            t0, late = t0 - late, 0.0
        fade = 0.005                                        # 연결음 뒤부터 딸깍 앞까지는 비움(옛 '틱'과 숨소리)
        z *= 1 - np.clip((t[:len(z)] - RING_END) / fade, 0, 1) * np.clip((t0 - t[:len(z)]) / fade, 0, 1)
        i0 = int(round(t0 * sr))
        z[i0:i0 + len(c)] += c
        if late > 0:                                        # 딸깍과 첫마디 사이의 조용한 바닥을 뒤집어 잇고 다시 바로 이어(이음매가 매끄러움) 늘림
            s1 = int((a.click - 0.02) * sr)
            room = s1 - int((t0 + heard + 0.03) * sr)
            pairs = int(np.ceil(late * sr / (2 * room)))
            ln = int(round(late * sr / (2 * pairs)))
            seg = z[s1 - ln:s1]
            assert np.abs(seg).max() < 0.02, '늘릴 자리에 소리가 있음'
            z = np.concatenate([z[:s1]] + [seg[::-1], seg] * pairs + [z[s1:]])
            late = 2 * pairs * ln / sr
        assert np.abs(z).max() <= LIMIT + 0.01, '딸깍을 더하니 봉우리가 넘침'
        with wave.open(str(TMP), 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes((np.clip(z, -1, 1) * 32767).astype('<i2').tobytes())
        e = (c ** 2).sum()
        print("딸깍: 딸 %.3f초, 깍 %.3f초, 끝 %.3f초 → 첫마디 %.3f초까지 %.2f초(첫마디와 그 뒤를 %.3f초 늦춤). 봉우리 %.2f, 0.1초에 고르게 편 크기 %.1f dBFS" % (
            t0, t0 + CLICK_GAP, t0 + heard, a.click + late, a.click + late - t0 - heard, late, np.abs(c).max(), 10 * np.log10(e / (0.1 * sr))))
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-i', str(TMP), '-ac', '1', '-ar', '44100', '-c:a', 'libmp3lame', '-q:a', '2', str(DST)], check=True)
    sh = len(z) - n                                     # 첫마디와 그 뒤가 늦어진 만큼(표본)
    v0 = int((a.start + RAMP) * sr)
    print('길이 %.3f초 → %.3f초, 봉우리 %.2f → %.2f' % (n / sr, len(z) / sr, np.abs(x).max(), np.abs(z).max()))
    print('목소리(%.1f초부터): %.1f → %.1f LUFS, 연결음: %.1f → %.1f LUFS' % (
        a.start + RAMP, lufs(a.src, a.start + RAMP), lufs(TMP, a.start + RAMP + sh / sr), lufs(a.src, 0, a.start), lufs(TMP, 0, a.start)))
    print('눌린 정도: 목소리의 크기가 gain보다 %.1f dB 덜 커짐' % (a.gain - 20 * np.log10(np.sqrt((z[v0 + sh:] ** 2).mean()) / np.sqrt((x[v0:] ** 2).mean()))))
    print('→', DST, '%.0f KB' % (DST.stat().st_size / 1e3))


if __name__ == '__main__':
    main()
