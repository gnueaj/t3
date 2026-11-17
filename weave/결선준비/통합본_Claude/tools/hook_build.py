#!/usr/bin/env python3
"""2쪽 음성(혼잣말)을 ElevenLabs에서 받은 목소리 파일 하나로 만든다 → assets/intro/call-hook.mp3

  python -I tools/hook_build.py <받은 mp3나 wav> [--tempo 1.15]            통화음 없이(덱에 넣는 파일)
  python -I tools/hook_build.py <받은 mp3나 wav> --call --out <mp3>       통화음을 그대로 둔 판(연결음, 딸깍, 전화 음질, 끊는 소리)을 따로

14차 뒤(11월 17일 밤): 사용자가 새 목소리를 주며 '이거를 먼저 넣고(통화음 같은 것은 유지) … (ppt도 교체)', 곧이어
'아 통화가 아니니까 통화 아이콘 같은 건 빼서 장표 구성해야 했다. 텍스트는 알맞게 나오도록'.
받은 목소리(9.4초, Chaerin, Eleven v4): "그 자료... 어디에 있지?" → "메신저에도 없고" → "메일함에도 없는데?" → "다시 전화해 봐야 하나?"
통화가 아니라 혼자 찾는 말이어서 덱에 넣는 파일에는 통화 연결음, 받는 소리, 전화 음질, 끊는 소리를 넣지 않는다.
12차의 손질 가운데 통화와 상관없는 것은 그대로 한다(call_build.py와 같은 값):
  1) 앞뒤의 빈 곳을 잘라 내고 목소리를 --tempo배 빠르게(높낮이는 그대로, 말 사이의 쉼도 함께)
  2) 크기: 목소리가 -17.8 LUFS가 되게 키우고 봉우리는 -1dBFS에서 누름(낭독은 -16 LUFS)
  3) 앞에 0.10초, 뒤에 0.35초의 빈 곳
끝나면 구절이 시작하고 끝나는 때를 찍는다 → make.py의 CALL_LEN, CALL_LINES에 옮겨 적음.
만든 파일은 받아쓰기로 돌려 끝말까지 나오는지 확인한다(12차에 끝말을 숨소리로 보고 잘라 낸 적이 있음).
"""
import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / 'tools'))
import call_build as B  # noqa: E402  (읽기, 빠르기, 누르기, 크기 재기, 통화음)
import call_gain as G  # noqa: E402

SR = B.SR
LEAD, TAIL = 0.10, 0.35                   # 목소리 앞뒤의 빈 곳(초)
SOUND = 0.004                             # 이보다 크면 소리가 있는 곳(받은 파일의 처음과 끝을 찾을 때)


def phrases(x, thr=0.012, join=0.30, minlen=0.10):
    """소리가 이어지는 구간들 [(시작, 끝)](초). join초보다 짧은 틈은 한 구간으로 본다."""
    ev = B.env10(x) > thr
    out, i, n = [], 0, len(ev)
    while i < n:
        if ev[i]:
            j = i
            while j < n and ev[j]:
                j += 1
            if out and i / SR - out[-1][1] < join:
                out[-1] = (out[-1][0], j / SR)
            else:
                out.append((i / SR, j / SR))
            i = j
        else:
            i += 1
    return [(a, b) for a, b in out if b - a >= minlen]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('--tempo', type=float, default=1.15)
    ap.add_argument('--call', action='store_true', help='통화음을 그대로 둔 판(연결음 → 딸깍 → 전화 음질의 목소리 → 끊는 소리)')
    ap.add_argument('--out', default='', help='만든 파일을 둘 곳(없으면 assets/intro/call-hook.mp3)')
    a = ap.parse_args()
    dst = Path(a.out) if a.out else B.DST
    raw = B.load(a.src)
    on = np.nonzero(np.abs(raw) > SOUND)[0]
    i0 = max(on[0] - int(0.05 * SR), 0)
    i1 = min(on[-1] + int(0.10 * SR), len(raw))
    x = raw[i0:i1].copy()
    f = int(0.05 * SR)
    x[-f:] *= np.linspace(1, 0, f)
    v = B.tempo(x, a.tempo)
    y = B.phone_fx(v) if a.call else v
    g = 10 ** ((B.VOICE_LUFS - B.lufs_of(y)) / 20)
    for _ in range(4):                                      # 누르고 나면 조금 작아지므로 몇 번 맞춤
        z = B.limit(y * g)
        g *= 10 ** ((B.VOICE_LUFS - B.lufs_of(z)) / 20)
    z = B.limit(y * g)
    if a.call:
        click, heard = G.pickup_click(SR)
        t_click = B.RING_AT + 1.0 + 0.01 + G.CLICK_AFTER
        t_voice = t_click + heard + B.CLICK_GAP - 0.05 / a.tempo
        t_beep = t_voice + len(z) / SR + B.END_GAP
        n = int((t_beep + B.BEEP_LEN + B.TAIL) * SR)
        out = np.zeros(n)
        r = B.ringback()
        out[int(B.RING_AT * SR):int(B.RING_AT * SR) + len(r)] += r
        out[int(round(t_click * SR)):int(round(t_click * SR)) + len(click)] += click
        j = int(round(t_voice * SR))
        out[j:j + len(z)] += z[:n - j]
        b = B.hangup()
        out[int(t_beep * SR):int(t_beep * SR) + len(b)] += b
        bed = B.biquad(B.biquad(np.random.default_rng(101).normal(0, 1, n), 140.0, 0.707, 'hp'), 2400.0, 0.707, 'lp')
        bed *= 10 ** (B.BED_DB / 20) / np.sqrt((bed ** 2).mean())
        t = np.arange(n) / SR
        bed *= np.clip((t - (t_click + heard)) / 0.05, 0, 1) * np.clip((n / SR - t) / 0.25, 0, 1)
        out += bed
    else:
        t_voice = LEAD
        out = np.concatenate([np.zeros(int(LEAD * SR)), z, np.zeros(int(TAIL * SR))])
    assert np.abs(out).max() <= G.LIMIT + 0.02, '봉우리가 넘침 %.3f' % np.abs(out).max()
    tmp = B.TMP.with_name('_hook_build.wav')
    tmp.parent.mkdir(parents=True, exist_ok=True)
    B.save(tmp, out)
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([B.FFMPEG, '-y', '-loglevel', 'error', '-i', str(tmp), '-ac', '1', '-ar', '44100', '-c:a', 'libmp3lame', '-q:a', '2', str(dst)], check=True)
    print('받은 파일 %.2f초 → 쓰는 구간 %.2f~%.2f초 → %.2f배 빠르게 %.2f초 → 만든 파일 %.2f초%s' % (
        len(raw) / SR, i0 / SR, i1 / SR, a.tempo, len(v) / SR, len(out) / SR, ' (통화음을 둔 판)' if a.call else ''))
    print('크기: 목소리 %.1f LUFS (키운 만큼 %.1f dB), 봉우리 %.2f' % (G.lufs(tmp, t_voice), 20 * np.log10(g), np.abs(out).max()))
    print('받은 파일의 구절: ' + ', '.join('%.2f~%.2f' % p for p in phrases(raw)))
    print('만든 파일의 구절: ' + ', '.join('%.2f~%.2f' % (t_voice + p0, t_voice + p1) for p0, p1 in phrases(z)))
    print('→', dst, '%.0f KB' % (dst.stat().st_size / 1e3))


if __name__ == '__main__':
    sys.exit(main())
