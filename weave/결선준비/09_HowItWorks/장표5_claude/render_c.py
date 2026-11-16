#!/usr/bin/env python3
"""PowerPoint(Windows, COM)로 확인용 렌더. 열린 PowerPoint 창과 다른 프레젠테이션은 건드리지 않음
(사본을 창 없이 열고 그 사본만 닫으며, PowerPoint가 원래 켜져 있었으면 끄지 않음). 다른 작업과 겹치지 않게 flock으로 줄 세움.

  python render_c.py png <pptx> <outdir> [W H]
  python render_c.py video <pptx> <mp4> <장별 초,...>     클릭 효과까지 저절로 나오는 사본(build.py --auto)을 녹화
"""
import fcntl
import shutil
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WINTMP = Path('/mnt/c/Temp/weave-ppt')
POWERSHELL = '/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe'
PS_EXPORT = ROOT / '07_소스' / 'slides' / 'tools' / 'ppt_export.ps1'
LOCK = '/tmp/weave-ppt.lock'
FFMPEG = str(Path.home() / '.cache' / 'weave-tools' / 'bin' / 'ffmpeg')

VIDEO_PS1 = r'''param([string]$Pptx, [string]$Mp4, [string]$Secs, [int]$H = 1080)
$ErrorActionPreference = "Stop"
$running = @(Get-Process POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open($Pptx, 0, 0, 0)
try {
  $t = $Secs.Split(',')
  $i = 0
  foreach ($s in $pres.Slides) { $s.SlideShowTransition.AdvanceOnTime = -1; $s.SlideShowTransition.AdvanceTime = [double]$t[[Math]::Min($i, $t.Count - 1)]; $i++ }
  $pres.CreateVideo($Mp4, $true, 3, $H, 30, 92)
  $w = 0
  while ($pres.CreateVideoStatus -eq 1 -or $pres.CreateVideoStatus -eq 2) { Start-Sleep -Seconds 2; $w += 2; if ($w -gt 3000) { break } }
  "status " + $pres.CreateVideoStatus
} finally {
  $pres.Saved = -1
  $pres.Close()
  if (-not $running) { $app.Quit() }
}
'''


@contextmanager
def ppt_lock():
    with open(LOCK, 'w') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def winpath(p):
    return subprocess.run(['wslpath', '-w', str(p)], capture_output=True, text=True, check=True).stdout.strip()


def ps(script, *args, timeout=3600):
    err = ''
    for i in range(20):
        try:
            r = subprocess.run([POWERSHELL, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', winpath(script), *args],
                               cwd=WINTMP, capture_output=True, timeout=timeout)
            log = (r.stdout + r.stderr).decode('utf-8', 'replace')
            if r.returncode != 0 and 'powershell.exe: Invalid argument' in log:      # 같은 실패가 종료 코드로 돌아올 때도 있음
                raise OSError(log.strip())
            return r.returncode, log
        except OSError as e:          # WSL 연동이 가끔 'Invalid argument'로 실패함 → 점점 길게 기다렸다 다시
            err = str(e)
            time.sleep(min(30, 2 * (i + 1)))
    return 1, err


def png(src, outdir, W=1920, H=1080):
    WINTMP.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PS_EXPORT, WINTMP / 'ppt_export.ps1')
    tag = 'claude-png-%d' % int(time.time() * 1000)
    tmp = WINTMP / (tag + '.pptx')
    od = WINTMP / tag
    shutil.copyfile(src, tmp)
    try:
        with ppt_lock():
            code, log = ps(WINTMP / 'ppt_export.ps1', '-Pptx', winpath(tmp), '-OutDir', winpath(od), '-W', str(W), '-H', str(H))
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
    assert code == 0, log
    outdir = Path(outdir)
    shutil.rmtree(outdir, ignore_errors=True)
    outdir.mkdir(parents=True)
    for p in sorted(od.glob('s*.png')):
        shutil.copyfile(p, outdir / p.name)
    shutil.rmtree(od, ignore_errors=True)
    return sorted(outdir.glob('s*.png'))


def video(src, mp4, secs):
    WINTMP.mkdir(parents=True, exist_ok=True)
    (WINTMP / 'claude_video.ps1').write_text('﻿' + VIDEO_PS1, encoding='utf-8')
    tag = 'claude-video-%d' % int(time.time() * 1000)
    tmp = WINTMP / (tag + '.pptx')
    out = WINTMP / (tag + '.mp4')
    shutil.copyfile(src, tmp)
    with ppt_lock():
        code, log = ps(WINTMP / 'claude_video.ps1', '-Pptx', winpath(tmp), '-Mp4', winpath(out), '-Secs',
                       ','.join('%.2f' % s for s in secs))
    assert code == 0 and out.exists(), log
    shutil.copyfile(out, mp4)
    out.unlink()
    tmp.unlink()
    fixed = repair(mp4)
    return log.strip()[-40:] + (' (깨진 장면 %d개를 앞 장면으로 바꿈: %s)' % (len(fixed), fixed) if fixed else '')


def bad_frames(mp4, w=64, h=36):
    """PowerPoint가 내보낸 영상에 가끔 한 장씩 끼는 깨진 장면(화면 전체의 색이 자홍, 주황 따위로 뒤집힌 한 장)의 번호들(0부터, 풀린 차례 그대로).
    글자와 도형의 밝기는 멀쩡하고 색 정보만 틀어져 있어서, 작게 줄여 장면마다 평균 색의 색차(U, V)를 본다:
    앞의 멀쩡한 장면에서 색차가 크게 튀었다가 세 장 안에 제자리로 돌아오면 그 사이가 깨진 장면이다(장이 바뀌는 것은 돌아오지 않으므로 걸리지 않음).
    11-16: 2쪽만 담은 17초 영상에 자홍 한 장(14.9초), 11차 낭독 영상에 자홍 두 장(37.8초, 44.7초), 12차 녹화에 주황 한 장(36.9초)과 자홍 한 장(110.5초).
    풀 때 오류는 없다."""
    import numpy as np
    out = subprocess.run([FFMPEG, '-loglevel', 'quiet', '-i', str(mp4), '-vf', 'scale=%d:%d' % (w, h), '-fps_mode', 'passthrough',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
    m = np.frombuffer(out, dtype=np.uint8).reshape(-1, w * h, 3).astype(float).mean(1)
    u = -0.169 * m[:, 0] - 0.331 * m[:, 1] + 0.5 * m[:, 2]
    v = 0.5 * m[:, 0] - 0.419 * m[:, 1] - 0.081 * m[:, 2]

    def far(a, b):
        return abs(u[a] - u[b]) + abs(v[a] - v[b])
    bad, good, i, n = [], 0, 1, len(m)
    while i < n:
        if far(i, good) > 40:
            back = next((k for k in range(i + 1, min(i + 4, n)) if far(k, good) < 8), None)
            if back is not None:
                bad += list(range(i, back))
                i = back
                continue
        good = i
        i += 1
    return bad


def repair(mp4):
    """깨진 장면(bad_frames)을 바로 앞 장면으로 바꿔 그 파일을 고쳐 쓴다(소리와 장면의 때는 그대로). 돌려줌: 바꾼 장면의 번호들."""
    bad = bad_frames(mp4)
    if not bad:
        return []
    mp4 = Path(mp4)
    chain, cur = '', '[0:v]'
    for k, i in enumerate(bad):          # 앞에서부터 하나씩: 깨진 장면이 이어져 있어도 바로 앞(이미 고친) 장면으로 바뀜
        chain += '%ssplit[a%d][b%d];[a%d][b%d]freezeframes=first=%d:last=%d:replace=%d[v%d];' % (cur, k, k, k, k, i, i, max(i - 1, 0), k)
        cur = '[v%d]' % k
    tmp = mp4.with_name(mp4.stem + '_repair.mp4')
    subprocess.run([FFMPEG, '-y', '-loglevel', 'quiet', '-i', str(mp4), '-filter_complex', chain.rstrip(';'), '-map', cur, '-map', '0:a?',
                    '-c:a', 'copy', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12', '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough', str(tmp)],
                   check=True, stderr=subprocess.DEVNULL)
    left = bad_frames(tmp)
    assert not left, '고친 뒤에도 깨진 장면이 남음 %s' % left
    tmp.replace(mp4)
    return bad


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'png':
        print(png(sys.argv[2], sys.argv[3], *(int(v) for v in sys.argv[4:6])))
    elif cmd == 'video':
        print(video(sys.argv[2], sys.argv[3], [float(v) for v in sys.argv[4].split(',')]))
    elif cmd == 'repair':             # python render_c.py repair <mp4>: 이미 찍어 둔 영상의 깨진 장면을 고침
        print('깨진 장면', repair(sys.argv[2]))
