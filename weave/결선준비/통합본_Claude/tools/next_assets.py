#!/usr/bin/env python3
"""'앞으로의 Weave' 장(next_new.py)에 쓰는 그림을 만든다 → assets/next/

  python -I tools/next_assets.py --src <받아 둔 원본 폴더>

원본(저장소에는 넣지 않음)
- note_<이름>.png   서툰 손그림과 손글씨(흰 바탕, 검정 펜). codex 이미지 생성으로 만든 것 → 흰 바탕을 투명으로, 잉크는 한 가지 검정으로, 그림과 글씨의 테두리에 맞춰 잘라 냄
- photo_<이름>.png  그 손그림으로 찾는 사진(codex 이미지 생성) → 카드의 사진 칸 비율로 잘라 jpg로
- bixby_512.png (Galaxy Store의 Bixby 앱 아이콘), smartthings_512.png (Google Play의 SmartThings 앱 아이콘) → 128px. SmartThings는 네모 그림이라 모서리를 둥글림
- lucide/<이름>.svg   Lucide(ISC)의 기기 선 그림 → assets/src/icons_next.html에 옮겨 적고 assets/next/ic-<이름>.png로 찍음
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent.parent
DST = HERE / 'assets' / 'next'
INK = (28, 26, 36)                  # 손그림과 손글씨의 색(덱의 글자색)
THICK = 5                           # 손그림 선을 굵히는 정도(원본 px, 홀수)
CARD_AR = 248 / 124                 # 카드 속 사진 칸의 가로 ÷ 세로
PHOTO_AR = {'family': 16 / 9}        # 사진마다 자를 비율이 다르면 여기에(없으면 카드 속 사진 칸 248 : 112)
PHOTO_FOCUS = {'light': (0.5, 0.50), 'wind': (0.5, 0.42), 'tree': (0.5, 0.72), 'rock': (0.5, 0.52), 'family': (0.5, 0.56)}      # 잘라 낼 때 남길 가운데(가로, 세로 비율)


def note(src, dst, pad=18):
    """흰 바탕의 검정 펜 그림 → 투명 바탕. 진한 정도를 투명도로 쓰고 색은 INK 한 가지로. 잉크가 있는 곳의 테두리 + pad만 남긴다."""
    im = Image.open(src).convert('L').filter(ImageFilter.MinFilter(THICK))      # 선을 조금 굵게(카드 안에서 작게 줄여도 읽히게)
    g = np.asarray(im, dtype=np.float32)
    a = np.clip((235 - g) / (235 - 70), 0, 1)          # 235보다 밝으면 종이, 70보다 어두우면 잉크
    ys, xs = np.where(a > 0.25)
    x0, x1, y0, y1 = max(xs.min() - pad, 0), min(xs.max() + pad, g.shape[1] - 1), max(ys.min() - pad, 0), min(ys.max() + pad, g.shape[0] - 1)
    a = a[y0:y1 + 1, x0:x1 + 1]
    px = np.zeros(a.shape + (4,), dtype=np.uint8)
    px[..., :3] = INK
    px[..., 3] = np.round(a * 255)
    Image.fromarray(px).save(dst, optimize=True)
    print('→', dst.name, px.shape[1], px.shape[0])
    return px.shape[1], px.shape[0]


def photo(src, dst, focus, ar=CARD_AR, w=1260):
    im = Image.open(src).convert('RGB')
    W, H = im.size
    ch = W / ar
    top = min(max(focus[1] * H - ch / 2, 0), H - ch)
    im = im.crop((0, round(top), W, round(top + ch))).resize((w, round(w / ar)), Image.LANCZOS)
    im.save(dst, quality=90)
    print('→', dst.name, im.size)


def icon(src, dst, size=128, round_k=None):
    im = Image.open(src).convert('RGBA').resize((size * 4, size * 4), Image.LANCZOS)
    if round_k:
        m = Image.new('L', im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=round(im.width * round_k), fill=255)
        im.putalpha(m)
    im.resize((size, size), Image.LANCZOS).save(dst, optimize=True)
    print('→', dst.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    a = ap.parse_args()
    src = Path(a.src)
    DST.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.glob('note_*.png')):
        note(f, DST / (f.stem.replace('_', '-') + '.png'))
    for f in sorted(src.glob('photo_*.png')):
        name = f.stem.split('_', 1)[1]
        photo(f, DST / ('photo-%s.jpg' % name), PHOTO_FOCUS.get(name, (0.5, 0.5)), PHOTO_AR.get(name, CARD_AR))
    if (src / 'bixby_512.png').exists():
        icon(src / 'bixby_512.png', DST / 'app-bixby.png')
    if (src / 'smartthings_512.png').exists():
        icon(src / 'smartthings_512.png', DST / 'app-smartthings.png', round_k=0.26)
    if (src / 'lucide').is_dir():
        icons(src)



# ------------------------------------------------------------------ 선 그림: 2027- 마디의 펜과 집, 끝 장 아래 줄의 기기
LUCIDE = ['smartphone', 'tv', 'refrigerator', 'washing-machine', 'watch', 'laptop', 'car', 'pen-line', 'house']      # lucide-static 0.460.0 (ISC)
ICON_HTML = '''<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<!-- '앞으로의 Weave' 끝 장의 기기 아이콘. Lucide(ISC, lucide.dev)의 선 그림을 연표 아이콘(ic-*.png)과 같은 규격(24칸 격자, 굵기 2)으로, 색은 보라(6B4EFF).
     찍기: python -I tools/next_assets.py --src <원본 폴더> (원본 폴더의 lucide/*.svg를 읽어 이 파일을 다시 씀) → assets/next/ic-*.png (256×256) -->
<style>
  * { margin: 0; padding: 0; }
  body { background: transparent; }
  .shot { width: 256px; height: 256px; }
  svg { width: 256px; height: 256px; fill: none; stroke: #6B4EFF; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
</style>
<body>
%s
</body>
</html>
'''


def icons(src):
    """원본 폴더의 lucide/<이름>.svg에서 도형만 읽어 assets/src/icons_next.html을 쓰고 PNG로 찍는다."""
    import re
    import subprocess
    rows = []
    for name in LUCIDE:
        svg = (src / 'lucide' / (name + '.svg')).read_text(encoding='utf-8')
        body = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.S).group(1)
        shapes = ' '.join(m.group(0) for m in re.finditer(r'<(?:path|rect|circle|line|polyline|ellipse|polygon)\b[^>]*/>', body))
        assert shapes and '<script' not in svg.lower(), name
        rows.append('<div class="shot" data-name="ic-%s"><svg viewBox="0 0 24 24">%s</svg></div>' % (name, shapes))
    html = HERE / 'assets' / 'src' / 'icons_next.html'
    html.write_text(ICON_HTML % '\n'.join(rows), encoding='utf-8')
    subprocess.run(['node', str(HERE / 'tools' / 'shot.cjs'), str(html), str(DST)], check=True)

if __name__ == '__main__':
    main()
