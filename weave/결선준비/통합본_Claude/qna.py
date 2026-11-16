"""Appendix(발표 뒤 질의응답용, 11-15)의 차례와 조립.

차례: 목차 → A 기존 기술과의 차이 → B 상품화 → C 동작 방식 → D 모델과 학습 → E 시나리오 더 보기 → 출처.
임원이 물을 가능성이 높은 순서다. 장마다 코드(A-2)와 쪽 번호가 있고, 목차의 항목을 누르면 그 장으로 간다.
make.py(통합본)와 qna_make.py(Appendix만 담은 덱)가 assemble()을 함께 쓴다.
"""
import copy
import importlib
import io

from pptx import Presentation

import build as HW
from appendix import head
from ui import INK, LINE2, MUTE, PURPLE, SUB, R, T

import foreign as F
from qna_lib import SECTIONS, Slide, box, draw_on, finish, group_of

MODULES = ['qna_a', 'qna_b', 'qna_c', 'qna_d', 'qna_e', 'qna_r']


def pages():
    out = []
    for name in MODULES:
        try:
            m = importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name != name:
                raise
            continue
        out += m.PAGES
    codes = [p.code for p in out]
    assert len(codes) == len(set(codes)), codes
    return out


def numbers(first, pgs=None):
    """{코드: 쪽}. 목차가 first쪽이고 그 뒤로 차례대로."""
    return {p.code: first + 1 + i for i, p in enumerate(pgs or pages())}


# ------------------------------------------------------------------ 목차
TOC_W, TOC_GAP, ROW_H, HEAD_H = 368, 18, 25, 44
# 묶음이 놓이는 자리(두 줄). 11차(11-16): B를 둘로 나누고, 시나리오 더 보기와 출처는 한 칸에 위아래로('E 시나리오 더 보기 / 출처 한 컬럼에')
TOC_GRID = [['A', 'B1', 'B2'], ['C', 'D', ('E', 'R')]]


def s_toc(first, pgs=None):
    pgs = pgs or pages()
    num = numbers(first, pgs)
    s = Slide('qna_toc', trans=('fade', 500), bar=False,
              notes='여기부터는 질의응답 때 띄우는 Appendix입니다. 본 발표에서는 넘기지 않습니다. '
                    '질문이 나오면 목차의 쪽 번호를 오퍼레이터에게 말합니다(발표 중에는 쪽 번호를 누르고 Enter를 치면 그 장이 열립니다).')
    head(s, [('Appendix', PURPLE), (' 목차', INK)], None, y=50, size=22)
    s.add('qna/pg', [T('qna/pg', 1150, 28, 60, 24, '0', size=11, color=MUTE, weight='b', align='r', anchor='ctr')])
    by = {}
    for p in pgs:
        by.setdefault(group_of(p.code), []).append(p)
    y = 100
    for row in TOC_GRID:
        hmax = 0
        cells = [(ci, sec, 0) for ci, cell in enumerate(row) for sec in ([cell] if isinstance(cell, str) else [])]
        for ci, cell in enumerate(row):                    # 한 칸에 위아래로 놓는 묶음들
            if not isinstance(cell, str):
                dy = 0
                for sec in cell:
                    cells.append((ci, sec, dy))
                    dy += HEAD_H + ROW_H * len(by.get(sec, [])) + 12 + 14
        for ci, sec, dy in cells:
            items = by.get(sec, [])
            if not items:
                continue
            x = 70 + ci * (TOC_W + TOC_GAP)
            h = HEAD_H + ROW_H * len(items) + 12
            hmax = max(hmax, dy + h)
            lab = SECTIONS[sec] if sec == 'R' else '%s  %s' % (sec[0], SECTIONS[sec])
            rng = '%d~%d쪽' % (num[items[0].code], num[items[-1].code]) if len(items) > 1 else '%d쪽' % num[items[0].code]
            cy = y + dy
            s.add('toc/card/' + sec, [box('toc/card/%s/bg' % sec, x, cy, TOC_W, h),
                                      T('toc/card/%s/t' % sec, x + 20, cy + 9, 250, 28, lab, size=13.5, color=PURPLE, weight='b', anchor='ctr'),
                                      T('toc/card/%s/r' % sec, x + TOC_W - 120, cy + 9, 100, 28, rng, size=10.5, color=MUTE, align='r', anchor='ctr'),
                                      R('toc/card/%s/ln' % sec, x + 16, cy + HEAD_H - 4, TOC_W - 32, 1, fill='EEE9F8', line=None)])
            for i, p in enumerate(items):
                ry = cy + HEAD_H + i * ROW_H
                code = '' if sec == 'R' else p.code
                s.add('toc/' + p.code, [R('toc/%s/bg' % p.code, x + 8, ry, TOC_W - 16, ROW_H, prst='roundRect', radius=8, fill='FFFFFF', line=None),
                                        T('toc/%s/c' % p.code, x + 20, ry, 40, ROW_H, code, size=11, color=PURPLE, weight='b', anchor='ctr'),
                                        T('toc/%s/t' % p.code, x + (20 if sec == 'R' else 60), ry, TOC_W - 120, ROW_H, p.toc, size=11.5, color=INK, anchor='ctr'),
                                        T('toc/%s/p' % p.code, x + TOC_W - 60, ry, 40, ROW_H, str(num[p.code]), size=12.5, color=PURPLE, weight='b', align='r',
                                          anchor='ctr')])
        y += hmax + 14
    return s


# ------------------------------------------------------------------ 조립
def copy_foreign(prs, src, layout, note_tpl):
    """다른 덱의 장을 prs 끝에 옮긴다(foreign.copy_slide와 같고, 같은 이름의 틀이 없으면 layout을 씀)."""
    try:
        lay = F.same_layout(prs, src.slide_layout)
    except (KeyError, IndexError, ValueError):
        lay = layout
    new = prs.slides.add_slide(lay)
    rid = {}
    for k, rel in src.part.rels.items():
        if not rel.is_external and rel.reltype.endswith('/image'):
            rid[k] = new.part.get_or_add_image_part(io.BytesIO(rel.target_part.blob))[1]
    el = copy.deepcopy(src._element)
    for e in el.iter():
        for k, v in list(e.attrib.items()):
            if k.startswith(F.RNS):
                assert v in rid, '옮기지 못하는 관계 %s=%s' % (k, v)
                e.set(k, rid[v])
    dst = new._element
    for ch in list(dst):
        dst.remove(ch)
    for ch in list(el):
        dst.append(ch)
    for k, v in el.attrib.items():
        dst.set(k, v)
    return new


def assemble(prs, layout, note_tpl, draw, first):
    """목차와 모든 장을 prs에 그려 넣는다. draw(specs) → 장 목록. 돌려줌: 차례대로의 장 목록(목차가 맨 앞)."""
    pgs = pages()
    toc = draw([s_toc(first, pgs)])[0]
    slides = {}
    for pg in pgs:
        if pg.foreign:
            path, idx, patch = pg.foreign
            src = list(Presentation(str(path)).slides)[idx - 1]
            sl = copy_foreign(prs, src, layout, note_tpl)
            draw_on(sl, patch(sl))
            F.set_notes(sl, pg.notes(), note_tpl)
        else:
            s = pg.make()
            s.notes = pg.notes()
            assert s.clicks() == pg.clicks, '%s: 클릭 %d ≠ %d' % (pg.code, s.clicks(), pg.clicks)
            sl = draw([s])[0]
        slides[pg.code] = sl
    finish(slides, toc)
    return [toc] + [slides[p.code] for p in pgs]
