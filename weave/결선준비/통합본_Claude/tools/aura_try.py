#!/usr/bin/env python3
"""3~5쪽 인물 뒤의 옅은 보라 그라데이션(make.patch_aura)을 세기만 달리해 나란히 본다. 덱은 바꾸지 않는다.

  python -I tools/aura_try.py     → 인물그라데이션_후보/한눈에.jpg (지금, 조금 더, 그보다 조금 더)

세기 = tools/intro_assets.py의 AURA_MAX(몸 안쪽의 가장 진한 곳. 윤곽 바로 밖은 그 절반쯤). 지금 덱은 0.26.
"""
import copy
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / 'tools'))
import make as MK  # noqa: E402
import intro_assets as IA  # noqa: E402
from pptx import Presentation  # noqa: E402

WORK = MK.OUT / 'aura_try'
DST = HERE / '인물그라데이션_후보'
LEVELS = [('지금', 0.26), ('조금 더', 0.42), ('그보다 조금 더', 0.60)]
KEYS = ('in03', 'in04', 'in05')


def build(level):
    d = WORK / ('a%02d' % round(level * 100))
    d.mkdir(parents=True, exist_ok=True)
    for f in (HERE / 'assets' / 'intro').glob('floats*.png'):
        shutil.copyfile(f, d / f.name)
    IA.DST, IA.AURA_MAX = d, level
    IA.auras()
    MK.INTRO_AS = d
    prs = Presentation(str(MK.BASE))
    old = list(prs.slides)
    note_tpl = [copy.deepcopy(sh._element) for sh in old[5].notes_slide.placeholders]
    intro = MK.copy_intro(prs, note_tpl)
    keep = [intro[k] for k in KEYS]
    MK.drop_slides(prs, old + [s for k, s in intro.items() if k not in KEYS])
    MK.reorder(prs, keep)
    MK.samsung_fonts.remap_prs(prs)
    dst = d / 'aura.pptx'
    prs.save(str(dst))
    return MK.render_c.png(dst, d / 'png', 1600, 900)


def main():
    from PIL import Image, ImageDraw, ImageFont
    import talk as TK
    WORK.mkdir(parents=True, exist_ok=True)
    cols = [(name, level, build(level)) for name, level in LEVELS]
    font = ImageFont.truetype(str(TK.FONT), 30)
    w, h, pad, head = 1000, 562, 14, 60
    im = Image.new('RGB', (pad + len(cols) * (w + pad), head + 2 * (h + pad)), '#FFFFFF')
    d = ImageDraw.Draw(im)
    for j, (name, level, pngs) in enumerate(cols):
        x = pad + j * (w + pad)
        d.text((x + w / 2, head / 2), '%s (세기 %.2f)' % (name, level), font=font, fill='#1C1A24', anchor='mm')
        full = Image.open(pngs[2]).convert('RGB')                      # 5쪽: 세 인물이 다 있음
        im.paste(full.resize((w, h), Image.LANCZOS), (x, head))
        z = full.crop((300, 338, 1300, 900))                            # 인물 둘레를 크게
        im.paste(z.resize((w, round(z.height * w / z.width)), Image.LANCZOS).crop((0, 0, w, h)), (x, head + h + pad))
    DST.mkdir(exist_ok=True)
    im.save(DST / '한눈에.jpg', quality=92)
    print('→', DST / '한눈에.jpg', im.size)


if __name__ == '__main__':
    main()
