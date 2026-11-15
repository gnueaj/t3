#!/usr/bin/env python3
"""Appendix(질의응답용)만 담은 덱 → Weave_Appendix_Claude.pptx. 팀원 덱에 붙이기 쉽게 따로 낸다(통합본에는 make.py가 같은 장을 넣는다).

  python qna_make.py            덱만
  python qna_make.py --png      + out/qna_png/s01.png… 와 out/qna_sheet_*.jpg(네 장씩 모은 확인용 그림)
  python qna_make.py --only B   B 묶음만(확인용. 목차의 쪽 번호는 이 덱 기준)
"""
import argparse
import copy
import sys
from pathlib import Path

from pptx import Presentation

import make as M                       # 통합본의 바탕 덱, 장 지우기와 차례 바꾸기
import qna as Q

HW, OUT = M.HW, M.OUT
DST = Path(__file__).resolve().parent / 'Weave_Appendix_Claude.pptx'


def build(dst, only=None):
    prs = Presentation(str(M.BASE))
    old = list(prs.slides)
    layout = old[5].slide_layout
    note_tpl = [copy.deepcopy(sh._element) for sh in old[5].notes_slide.placeholders]
    report = []

    def draw(specs):
        slides, rep, _ = HW.add_slides(prs, layout, note_tpl, specs)
        report.extend(rep)
        return slides
    if only:
        allp = Q.pages
        Q.pages = lambda: [p for p in allp() if p.code[0] in only]
    order = Q.assemble(prs, layout, note_tpl, draw, 1)
    M.drop_slides(prs, old)
    M.reorder(prs, order)
    M.samsung_fonts.remap_prs(prs)
    prs.save(str(dst))
    for key, nclick, nnote, _ in report:
        if nclick != nnote:
            print('   ! %s: 클릭 %d ≠ 노트 (클릭) %d' % (key, nclick, nnote))
    return order


def sheets(pngs, per=4, cols=2, w=800):
    from PIL import Image
    out = []
    for k in range(0, len(pngs), per):
        ims = [Image.open(p).convert('RGB') for p in pngs[k:k + per]]
        h = round(w * ims[0].height / ims[0].width)
        rows = (len(ims) + cols - 1) // cols
        sh = Image.new('RGB', (w * cols, h * rows), 'white')
        for i, im in enumerate(ims):
            sh.paste(im.resize((w, h), Image.LANCZOS), ((i % cols) * w, (i // cols) * h))
        p = OUT / ('qna_sheet_%02d.jpg' % (k // per + 1))
        sh.save(p, quality=88)
        out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--png', action='store_true')
    ap.add_argument('--only', default=None)
    a = ap.parse_args()
    dst = DST if not a.only else OUT / ('qna_only_%s.pptx' % a.only)
    order = build(dst, a.only)
    print('→', dst.name, '%.1f MB' % (dst.stat().st_size / 1e6), len(order), '장')
    if a.png:
        pngs = M.render_c.png(dst, OUT / 'qna_png', 1600, 900)
        print('png', len(pngs), [p.name for p in sheets(pngs)])


if __name__ == '__main__':
    sys.exit(main())
