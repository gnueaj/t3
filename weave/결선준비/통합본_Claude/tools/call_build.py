#!/usr/bin/env python3
"""2쪽 통화 음성을 ElevenLabs에서 받은 목소리 파일 하나로 처음부터 만든다 → assets/intro/call-hook.mp3

  python tools/call_build.py <받은 mp3나 wav> --end 9.90 [--tempo 1.15] [--pause 1.56]

12차(11월 16일 밤): 사용자가 새 목소리를 주며 '첨부한 파일로 바꾸고 1.15배속 하기(기존 효과도 해야 함. "프로입니다." 이후 딜레이라든지는 넣어야 하고)'.
받은 목소리(10.5초): "네, 양서윤 프로입니다." → "아, 그거요?" → 한숨 → 작게 "어디 적어놨더라" → "음, 잠깐만요. 찾아보고 다시 알려 드릴게요."
그 전(11차)의 파일은 Carbon이 다듬은 최종후보 B(연결음, 전화 음질, 첫 정적 1.85초, 끊는 소리)에 call_edit.py(말을 덜어 내고 1.15배)와
call_gain.py(크기, 받는 소리 '딸깍', 첫마디까지 0.63초)를 거친 것이었다. 새 목소리에는 그 손질이 하나도 없으므로 여기서 같은 값으로 한 번에 한다:
  1) 앞의 빈 곳과 끝의 숨소리를 잘라 내고(--end: 마지막 말이 끝나는 때), 목소리를 --tempo배 빠르게(높낮이는 그대로, 말 사이의 쉼도 함께)
  2) "프로입니다." 뒤의 쉼(상대의 말을 듣는 틈)을 --pause초로. 11차 파일에서 잰 값이 1.56초(Carbon의 1.85초를 1.15배 빠르게 한 길이)
  3) 전화 음질: 285~3550Hz 띠만 남기고 1.15kHz를 조금 올리고 여리게 누름(Carbon의 classic_phone_fx와 같은 값)
  4) 크기: 목소리 전체가 11차 파일과 같은 -17.8 LUFS가 되게 키우고 봉우리는 -1dBFS에서 누름(낭독은 -16 LUFS)
  5) 통화 연결음(440+480Hz, 1초, 봉우리 0.885) → 0.23초 → 받는 소리 '딸깍' → 0.63초 → 목소리 → 0.315초 → 끊는 소리(480Hz 0.22초) → 0.22초
작게 말한 "어디 적어놨더라"는 받은 파일의 크기 차이를 그대로 둔다(누르는 과정에서 차이가 줄면 그만큼 다시 낮춤).
끝나면 낱말이 시작하는 때를 찍는다 → make.py의 CALL_LEN, CALL_PICK, CALL_HANG, CALL_LINES에 옮겨 적음.
"""
import argparse
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from scipy.signal import lfilter

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / 'tools'))
import call_gain as G  # noqa: E402  (받는 소리 '딸깍', 크기 재기)

DST = HERE / 'assets' / 'intro' / 'call-hook.mp3'
TMP = HERE / 'out' / '_call_build.wav'
FFMPEG = G.FFMPEG
SR = 44100
RING_AT, RING_PEAK = 0.12, 0.885          # 연결음이 시작하는 때(초)와 봉우리(11차 파일에서 잰 값)
CLICK_GAP = 0.63                          # 딸깍이 끝나고 첫마디까지(초)
END_GAP = 0.315                           # 마지막 말이 끝나고 끊는 소리까지(초)
BEEP_PEAK, BEEP_LEN, TAIL = 0.347, 0.22, 0.22      # 끊는 소리의 봉우리와 길이, 그 뒤의 빈 곳(초)
VOICE_LUFS = -17.8                        # 목소리의 크기(11차 파일)
BED_DB = -56.0                            # 딸깍 뒤부터 깔리는 전화선의 바닥 소리(11차 파일에서 잰 값, dBFS)
QUIET = 0.006                             # 이보다 작으면 조용한 곳(10ms마다의 크기)


def load(path):
    out = subprocess.run([FFMPEG, '-loglevel', 'error', '-i', str(path), '-f', 'f32le', '-ar', str(SR), '-ac', '1', 'pipe:1'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype='<f4').astype(np.float64)


def tempo(x, k):
    out = subprocess.run([FFMPEG, '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', 'pipe:0',
                          '-af', 'atempo=%.4f' % k, '-f', 'f32le', '-ar', str(SR), '-ac', '1', 'pipe:1'],
                         input=x.astype('<f4').tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype='<f4').astype(np.float64)


def limit(x):
    """봉우리를 -1dBFS에서 누름(call_gain.py와 같은 값)."""
    out = subprocess.run([FFMPEG, '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', 'pipe:0',
                          '-af', 'alimiter=limit=%.2f:attack=5:release=60:level=false:latency=true' % G.LIMIT,
                          '-f', 'f32le', '-ar', str(SR), '-ac', '1', 'pipe:1'],
                         input=x.astype('<f4').tobytes(), capture_output=True, check=True).stdout
    y = np.frombuffer(out, dtype='<f4').astype(np.float64)
    return np.concatenate([y, np.zeros(max(len(x) - len(y), 0))])[:len(x)]


def biquad(x, f0, q, mode):
    """2차 필터(Carbon의 build_phone_hook.biquad_filter와 같은 식)."""
    w0 = 2 * np.pi * f0 / SR
    al, c = np.sin(w0) / (2 * q), np.cos(w0)
    b = {'lp': [(1 - c) / 2, 1 - c, (1 - c) / 2], 'hp': [(1 + c) / 2, -(1 + c), (1 + c) / 2], 'bp': [al, 0.0, -al]}[mode]
    a = [1 + al, -2 * c, 1 - al]
    return lfilter(np.array(b) / a[0], np.array(a) / a[0], x)


def phone_fx(x, hp=(285.0, 0.82), lp=(3550.0, 0.85), mid=(1150.0, 1.45), drive=1.55):
    """전화 음질: 띠 제한 + 수화기의 울림(1.15kHz) + 여린 눌림."""
    y = biquad(biquad(x, hp[0], hp[1], 'hp'), lp[0], lp[1], 'lp')
    y = y + 0.32 * biquad(y, mid[0], mid[1], 'bp')
    return np.tanh(y * drive) / np.tanh(drive)


def ringback():
    """통화 연결음 한 번(440 + 480Hz, 1초). Carbon의 korean_ringback과 같은 식, 봉우리는 RING_PEAK."""
    t = np.arange(SR) / SR
    env = np.ones(SR)
    f = int(0.018 * SR)
    env[:f], env[-f:] = np.linspace(0, 1, f), np.linspace(1, 0, f)
    y = phone_fx((0.5 * np.sin(2 * np.pi * 440 * t) + 0.5 * np.sin(2 * np.pi * 480 * t)) * env * 0.22, hp=(280.0, 0.8), mid=(1150.0, 1.4))
    return y * RING_PEAK / np.abs(y).max()


def hangup():
    n = int(BEEP_LEN * SR)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * 480 * t) * np.exp(-t * 4.5)
    f = int(0.012 * SR)
    y[:f] *= np.linspace(0, 1, f)
    y[-f:] *= np.linspace(1, 0, f)
    return y * BEEP_PEAK / np.abs(y).max()


def env10(x):
    n = int(0.01 * SR)
    return np.sqrt(np.convolve(x ** 2, np.ones(n) / n, mode='same'))


def quiet_runs(x, thr=QUIET, minlen=0.12):
    q = env10(x) < thr
    out, i = [], 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]:
                j += 1
            if j - i >= minlen * SR:
                out.append((i, j))
            i = j
        else:
            i += 1
    return out


def lufs_of(x):
    f = TMP.with_name('_call_lufs.wav')
    save(f, x)
    v = G.lufs(f)
    f.unlink()
    return v


def save(path, x):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())


def db(x):
    return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('--tempo', type=float, default=1.15)
    ap.add_argument('--pause', type=float, default=1.56, help='"프로입니다." 뒤의 쉼(초, 빠르게 한 뒤의 길이)')
    ap.add_argument('--end', type=float, default=0.0, help='받은 파일에서 마지막 말이 끝나는 때(초). 그 뒤의 숨소리는 잘라 냄. 0이면 끝까지')
    ap.add_argument('--soft', default='', help='작게 말한 구간(받은 파일의 초, "4.20:6.15"): 크기 차이를 받은 파일과 같게 지킴')
    ap.add_argument('--soft-db', type=float, default=0.0, help='작게 말한 구간을 더 낮추는 만큼(dB)')
    a = ap.parse_args()
    raw = load(a.src)
    on = np.nonzero(np.abs(raw) > 0.004)[0]
    i0 = max(on[0] - int(0.05 * SR), 0)                     # 첫 소리 0.05초 앞부터
    i1 = int(a.end * SR) + int(0.06 * SR) if a.end else min(on[-1] + int(0.08 * SR), len(raw))
    x = raw[i0:i1].copy()
    f = int(0.05 * SR)
    x[-f:] *= np.linspace(1, 0, f)                          # 끝은 조용히 닫음
    lead = (on[0] - i0) / SR / a.tempo                      # 빠르게 한 뒤 첫 소리까지(초)
    v = tempo(x, a.tempo)
    # "프로입니다." 뒤의 쉼: 앞쪽 절반에서 가장 긴 조용한 곳을 --pause초로(양 끝 0.03초는 원래 소리를 두고 그 사이를 같은 크기의 바닥 소리로 채움)
    runs = [r for r in quiet_runs(v) if r[0] > 0.3 * SR and r[1] < 0.5 * len(v)]
    p0, p1 = max(runs, key=lambda r: r[1] - r[0])
    e = int(0.03 * SR)
    fd = int(0.015 * SR)
    left, right = v[:p0 + e].copy(), v[p1 - e:].copy()
    left[-fd:] *= np.linspace(1, 0, fd)
    right[:fd] *= np.linspace(0, 1, fd)
    floor = float(np.std(v[p0 + e:p1 - e]))
    gap = np.random.default_rng(77).normal(0, max(floor * 0.8, 1e-5), int(a.pause * SR) - 2 * e)
    old_pause = (p1 - p0) / SR
    v = np.concatenate([left, gap, right])
    shift = len(gap) / SR - (old_pause - 2 * e / SR)        # 쉼 뒤의 말이 늦어진 만큼(초)

    def at(t_raw):
        """받은 파일의 때 → 빠르게 하고 쉼을 늘린 목소리 안의 때(초)"""
        t = (t_raw * SR - i0) / SR / a.tempo
        return t + (shift if t * SR > p0 + e else 0)
    y = phone_fx(v)
    g = 10 ** ((VOICE_LUFS - lufs_of(y)) / 20)
    for _ in range(4):                                      # 누르고 나면 조금 작아지므로 몇 번 맞춤
        z = limit(y * g)
        g *= 10 ** ((VOICE_LUFS - lufs_of(z)) / 20)
    z = limit(y * g)
    soft = None
    if a.soft:
        s0, s1 = (float(t) for t in a.soft.split(':'))
        j0, j1 = int(at(s0) * SR), int(at(s1) * SR)
        r0, r1 = int(s0 * SR), int(s1 * SR)
        loud_raw = np.concatenate([raw[i0:r0], raw[r1:i1]])
        loud_out = np.concatenate([z[:j0], z[j1:]])

        def top(s):                                         # 말하는 곳만(조용한 곳은 빼고) 잰 크기
            ev = env10(s)
            return 20 * np.log10(np.sqrt((s[ev > QUIET] ** 2).mean()) + 1e-9)
        want = top(raw[r0:r1]) - top(loud_raw)              # 받은 파일에서 작게 말한 곳이 나머지보다 작은 만큼(dB, 음수)
        got = top(z[j0:j1]) - top(loud_out)
        fix = min(want - got, 0.0) - a.soft_db              # 누르면서 줄어든 차이를 되돌리고, 더 낮추라는 만큼 더
        ramp = int(0.04 * SR)
        k = np.ones(len(z))
        k[j0:j1] = 10 ** (fix / 20)
        k[j0 - ramp:j0] = np.linspace(1, 10 ** (fix / 20), ramp)
        k[j1:j1 + ramp] = np.linspace(10 ** (fix / 20), 1, ramp)
        z = z * k
        soft = (want, got, fix, top(z[j0:j1]) - top(loud_out))
    # 조립
    click, heard = G.pickup_click(SR)
    t_click = RING_AT + 1.0 + 0.01 + G.CLICK_AFTER          # 연결음이 끝나고(1.13초) 0.231초 뒤
    t_voice = t_click + heard + CLICK_GAP - lead            # 목소리 토막을 놓는 때: 첫 소리가 딸깍 0.63초 뒤
    t_last = t_voice + at(a.end if a.end else (on[-1] / SR))                  # 마지막 말이 끝나는 때
    t_beep = t_last + END_GAP
    n = int((t_beep + BEEP_LEN + TAIL) * SR)
    out = np.zeros(n)
    r = ringback()
    out[int(RING_AT * SR):int(RING_AT * SR) + len(r)] += r
    out[int(round(t_click * SR)):int(round(t_click * SR)) + len(click)] += click
    j = int(round(t_voice * SR))
    out[j:j + len(z)] += z[:n - j]
    b = hangup()
    out[int(t_beep * SR):int(t_beep * SR) + len(b)] += b
    bed = biquad(biquad(np.random.default_rng(101).normal(0, 1, n), 140.0, 0.707, 'hp'), 2400.0, 0.707, 'lp')
    bed *= 10 ** (BED_DB / 20) / np.sqrt((bed ** 2).mean())
    t = np.arange(n) / SR
    bed *= np.clip((t - (t_click + heard)) / 0.05, 0, 1) * np.clip((n / SR - t) / 0.25, 0, 1)      # 딸깍 뒤부터, 끝은 서서히
    out += bed
    assert np.abs(out).max() <= G.LIMIT + 0.02, '봉우리가 넘침 %.3f' % np.abs(out).max()
    TMP.parent.mkdir(parents=True, exist_ok=True)
    save(TMP, out)
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-i', str(TMP), '-ac', '1', '-ar', '44100', '-c:a', 'libmp3lame', '-q:a', '2', str(DST)], check=True)
    print('받은 파일 %.2f초 → 쓰는 구간 %.2f~%.2f초 → %.2f배 빠르게 %.2f초 → 쉼 %.2f초 → %.2f초 (쉼 뒤는 %.2f초 늦어짐)' % (
        len(raw) / SR, i0 / SR, i1 / SR, a.tempo, len(x) / SR / a.tempo, old_pause, a.pause, shift))
    print('크기: 목소리 %.1f LUFS (키운 만큼 %.1f dB), 연결음 %.1f LUFS, 봉우리 %.2f' % (
        G.lufs(TMP, t_voice), 20 * np.log10(g), G.lufs(TMP, 0, t_click - 0.05), np.abs(out).max()))
    if soft:
        print('작게 말한 곳: 받은 파일에서 나머지보다 %.1f dB, 손질 뒤 %.1f dB → %.1f dB 더 낮춰 %.1f dB' % soft)
    print('연결음 %.2f~%.2f초, 딸깍 %.3f~%.3f초(깍 %.3f초), 첫마디 %.3f초, 쉼 %.2f~%.2f초, 마지막 말의 끝 %.2f초, 끊는 소리 %.2f~%.2f초, 길이 %.2f초' % (
        RING_AT, RING_AT + 1.0, t_click, t_click + heard, t_click + G.CLICK_GAP, t_voice + lead,
        t_voice + (p0 + e) / SR, t_voice + (p0 + e) / SR + len(gap) / SR, t_last, t_beep, t_beep + BEEP_LEN, n / SR))
    print('받은 파일의 때 → 만든 파일의 때: ' + ', '.join('%.2f → %.2f' % (tr, t_voice + at(tr)) for tr in (0.05, 2.45, 3.10, 4.27, 4.88, 6.55, 7.19, 8.35, 9.07, 9.88)))
    print('→', DST, '%.0f KB' % (DST.stat().st_size / 1e3))


if __name__ == '__main__':
    sys.exit(main())
