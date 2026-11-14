#!/usr/bin/env python3
"""떠 있는 흰 조각(카드, 말풍선)의 안쪽 여백을 장의 그림에서 잰다.

  python tools/pad_audit.py 35                          → 35쪽의 조각마다 (왼, 위, 오른, 아래) 여백을 적고 out/pad_audit/s35.png에 그려 봄
  python tools/pad_audit.py 30 31 35                    → 여러 쪽
  python tools/pad_audit.py --png out/next_try/png_미래 2   → 다른 폴더의 그림(sNN.png)

그림은 make.py --png로 찍은 out/png/sNN.png(1600×900)를 읽는다. 여백의 단위는 장의 px(1280×720).
흰 조각 = 순백 픽셀이 이어진 덩어리 가운데 네 변 안쪽이 흰 것. 잉크 = 그 덩어리에 둘러싸인 흰색 아닌 픽셀(글, 아이콘, 회색 말풍선).
회색 말풍선(F3F1F7)은 한 번 더 잰다: 말풍선 안의 글까지의 여백.
옅게 깔린 조각, 사진으로 꽉 찬 조각, 알약처럼 둥근 조각은 못 찾을 수 있다(그런 것은 그림을 잘라 눈으로 봄).

11월 14일: 35쪽의 기록 카드가 빽빽하다는 검토를 받고 30쪽의 기록 카드와 견주려고 만듦
(30쪽은 글이 테두리에서 14~16px, 35쪽은 7~10px이었고 12~14px로 고침).
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / 'out' / 'pad_audit'
BUBBLE = (243, 241, 247)            # 회색 말풍선의 색(ui.GRAY_FILL)


def ring_ok(comp, m=3, keep=0.7, need=0.9):
    """덩어리의 네 변에서 m px 안쪽 줄이 (모서리를 뺀 가운데 keep만큼) 거의 다 덩어리에 들면 네모난 조각으로 봄."""
    h, w = comp.shape
    a, b = int(w * (1 - keep) / 2), int(w * (1 + keep) / 2)
    c, d = int(h * (1 - keep) / 2), int(h * (1 + keep) / 2)
    edges = [comp[m, a:b], comp[h - 1 - m, a:b], comp[c:d, m], comp[c:d, w - 1 - m]]
    return all(e.mean() >= need for e in edges)


def find(mask, im, k, kind, min_w, min_h, ink_fn=None):
    """mask의 덩어리 가운데 조각을 찾아 [{kind, x, y, w, h, L, T, R, B}] (장의 px)."""
    H, W = mask.shape
    lab, _ = ndi.label(mask)
    out = []
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        w, h = x1 - x0, y1 - y0
        if w < min_w * k or h < min_h * k or w * h > 0.45 * W * H:
            continue
        comp = lab[sl] == i
        if not ring_ok(comp):
            continue
        ink = ndi.binary_fill_holes(comp) & ~comp
        if ink_fn is not None:
            ink &= ink_fn(im[sl])
        if ink.sum() < 12:
            continue
        ys, xs = np.where(ink)
        out.append(dict(kind=kind, x=round(x0 / k, 1), y=round(y0 / k, 1), w=round(w / k, 1), h=round(h / k, 1),
                        L=round(xs.min() / k, 1), T=round(ys.min() / k, 1), R=round((w - 1 - xs.max()) / k, 1), B=round((h - 1 - ys.max()) / k, 1)))
    return out


def audit(png):
    im = np.asarray(Image.open(png).convert('RGB')).astype(np.int16)
    k = im.shape[1] / 1280
    res = find(im.min(axis=2) >= 251, im, k, '카드', 44, 22)
    grey = np.abs(im - np.array(BUBBLE)).max(axis=2) <= 3
    res += find(grey, im, k, '말풍선', 30, 14, ink_fn=lambda a: a.max(axis=2) < 200)
    return sorted(res, key=lambda b: (b['y'], b['x'])), k


def draw(png, res, k, dst):
    """잰 것을 그림 위에: 조각의 테두리(카드는 빨강, 말풍선은 파랑), 잉크의 테두리(초록), 여백 네 값."""
    im = Image.open(png).convert('RGB')
    d = ImageDraw.Draw(im)
    for b in res:
        x, y, w, h = b['x'] * k, b['y'] * k, b['w'] * k, b['h'] * k
        col = (230, 40, 60) if b['kind'] == '카드' else (20, 120, 220)
        d.rectangle((x, y, x + w, y + h), outline=col, width=2)
        d.rectangle((x + b['L'] * k, y + b['T'] * k, x + w - b['R'] * k, y + h - b['B'] * k), outline=(0, 170, 90), width=1)
        t = '%g %g %g %g' % (b['L'], b['T'], b['R'], b['B'])
        d.rectangle((x, y - 12, x + d.textlength(t) + 4, y), fill=col)
        d.text((x + 2, y - 12), t, fill='white')
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pages', type=int, nargs='+')
    ap.add_argument('--png', default=str(HERE / 'out' / 'png'), help='sNN.png이 있는 폴더')
    a = ap.parse_args()
    for n in a.pages:
        png = Path(a.png) / ('s%02d.png' % n)
        res, k = audit(png)
        print('%d쪽: 조각 %d' % (n, len(res)))
        for b in res:
            print('   %-3s (%6.1f, %5.1f) %5.1f×%5.1f   왼 %4.1f  위 %4.1f  오른 %5.1f  아래 %4.1f' %
                  (b['kind'], b['x'], b['y'], b['w'], b['h'], b['L'], b['T'], b['R'], b['B']))
        draw(png, res, k, OUT / ('s%02d.png' % n))
    print('→', OUT)


if __name__ == '__main__':
    main()
