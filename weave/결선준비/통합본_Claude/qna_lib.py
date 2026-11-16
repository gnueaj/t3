"""Appendix(발표 뒤 질의응답용, 11-15)의 공통 틀과 부품.

장마다 같은 틀이다: 왼쪽 위에 코드(A-2)와 묶음 이름, 오른쪽 위에 쪽 번호와 '목차' 단추, 가운데 위에 제목과 한 줄 결론, 가운데에 그림이나 표 하나, 아래에 각주.
쪽 번호는 PowerPoint의 슬라이드 번호 필드라서 어느 덱에 붙여도 맞는다. 목차의 항목과 '목차' 단추는 누르면 그 장으로 간다(finish).
장마다 물음과 답(Page.q, Page.a, Page.more)을 함께 적어 두고, 노트와 `Appendix_QnA_대본.md`가 같은 글을 쓴다(qna_doc.py).
"""
import copy
import itertools
from pathlib import Path

from lxml import etree

import build as HW
from appendix import foot, head
from ui import (BODY, INK, LAV, LAV2, LINE2, MUTE, PURPLE, PURPLE2, RING, SUB, SHADOW_CARD, SHADOW_SOFT, C, Painter, R, T, chip, numdot, tw)

HERE = Path(__file__).resolve().parent
Slide = HW.Slide
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'

# 묶음 이름과 목차의 칸.
# 13차(11-17, 사용자의 지시): 상품화의 메모리와 속도 세 장은 D로 옮기고, 계획과 가전 두 장은 '데이터와 사업'과 합쳐 B 하나로(새 이름 '상품화와 사업성').
#   시나리오 더 보기(11차의 E)는 C로 바꿔 B 옆에 두고, 동작 방식(11차의 C)은 그 뒤에 이어 같은 글자 C를 씀(목차의 칸은 둘: 11차에 B가 두 칸이던 것과 같은 꼴).
#   모델과 학습(D)은 옮겨 온 세 장을 더해 두 칸으로 나눔. 처음에는 D-4에서 나눴고(모델과 성능 / 학습과 근거 연구),
#   같은 날 사용자의 말('D-7까지를 한 컬럼에')로 D-7에서 나눔: 앞 칸은 모델과 성능 네 장에 Query Rewriter 세 장(종류, 작은 모델, 튜닝),
#   뒤 칸은 Reasoning Embedding 두 장(정의와 유형, 튜닝)과 Multi-hop Retrieval 연구, 한국어 데이터와 평가. 장의 차례와 코드는 그대로.
#   코드는 묶음 글자마다 이어짐: C-1~C-3 시나리오, C-4~C-9 동작 방식, D-1~D-7 모델과 성능, Query Rewriter, D-8~D-11 Reasoning Embedding과 데이터.
SECTIONS = {'A': '기존 기술과의 차이', 'B': '상품화와 사업성', 'C1': '시나리오 더 보기', 'C2': '동작 방식',
            'D1': '모델과 성능, Query Rewriter', 'D2': 'Reasoning Embedding과 데이터', 'R': '출처'}
SPLIT = {'C': 3, 'D': 7}                # C-1 ~ C-3은 C1(시나리오), C-4부터 C2(동작 방식). D-1 ~ D-7은 D1, D-8부터 D2
ORDER = 'ABCDR'                         # 묶음의 차례(장의 차례는 qna.pages가 코드로 정렬)


def group_of(code):
    """장의 코드(C-7) → 묶음(C2)."""
    g = code[0]
    if g not in SPLIT:
        return g
    return g + ('1' if int(code.split('-')[1]) <= SPLIT[g] else '2')


RED_BG, RED_INK = 'FDF0F0', 'B4232B'
GRAY_BG = 'F7F5FC'
X0, W0 = 70, 1140                      # 본문이 놓이는 왼쪽 끝과 폭(다른 Appendix 장과 같음)


class Page:
    """Appendix 한 장. make()가 장(Slide)을 돌려준다. foreign = (덱 파일, 쪽, 손보는 함수)이면 그 덱의 장을 그대로 옮겨 온다.
    q = 임원이 물을 말, a = 답(실제로 말할 문장), more = [(이어서 물을 말, 답)], basis = 근거 목록(대본 md에만)."""

    def __init__(self, code, toc, make=None, q='', a='', more=(), basis=(), foreign=None, clicks=0, plain=False):
        self.code, self.toc, self.make, self.q, self.a = code, toc, make, q, a
        self.more, self.basis, self.foreign, self.clicks, self.plain = list(more), list(basis), foreign, clicks, plain

    @property
    def sec(self):
        return SECTIONS[group_of(self.code)]

    def notes(self):
        if self.plain:
            return self.a
        out = ['Q. ' + self.q, 'A. ' + self.a]
        for q, a in self.more:
            out.append('더 물으면: %s → %s' % (q, a))
        return '\n'.join(out)


# ------------------------------------------------------------------ 글
def wrapl(text, pt, w, weight='r'):
    """글을 폭 w(px)에 맞춰 낱말 단위로 줄을 나눈다. 돌려줌: 줄 목록."""
    out = []
    for para in text.split('\n'):
        line = ''
        for word in para.split(' '):
            cand = (line + ' ' + word) if line else word
            if line and tw(cand, pt, weight) > w:
                out.append(line)
                line = word
            else:
                line = cand
        out.append(line)
    return out


def lh_of(pt, k=1.4):
    return pt * 4 / 3 * k


def para(name, x, y, w, text, pt=12, color=BODY, weight='r', align='l', k=1.4, anchor='t', h=None):
    """여러 줄 글(폭에 맞춰 줄을 나눔). text = 문자열이나 줄 목록(줄 = 문자열이나 [(글, 꾸밈)]). 돌려줌: (원시, 높이)."""
    lines = wrapl(text, pt, w, weight) if isinstance(text, str) else list(text)
    lh = lh_of(pt, k)
    hh = lh * len(lines) + 4
    return T(name, x, y, w, h or hh, lines, size=pt, color=color, weight=weight, align=align, lnspc=lh * 0.75, anchor=anchor), hh


def bullets(key, x, y, w, items, pt=12, color=BODY, k=1.4, gap=0):
    """• 항목 목록. 항목은 폭에 맞춰 줄을 나누고 둘째 줄부터는 글머리만큼 들여 쓴다. 돌려줌: (원시 목록, 높이)."""
    ind = tw('• ', pt)
    lh = lh_of(pt, k)
    out, yy = [], y
    for i, it in enumerate(items):
        lines = wrapl(it, pt, w - ind) if isinstance(it, str) else list(it)
        out.append(T('%s/b%d' % (key, i), x, yy, ind + 4, lh, '•', size=pt, color=color))
        out.append(T('%s/t%d' % (key, i), x + ind, yy, w - ind, lh * len(lines) + 4, lines, size=pt, color=color, lnspc=lh * 0.75))
        yy += lh * len(lines) + gap
    return out, yy - y


def note_box(key, x, y, w, lines, fill=LAV, ink=PURPLE, pt=12, weight='b', align='l'):
    """옅은 바탕의 강조 상자. 돌려줌: (원시 목록, 높이)."""
    lh = lh_of(pt)
    h = lh * len(lines) + 22
    return [R(key + '/bg', x, y, w, h, prst='roundRect', radius=12, fill=fill, line=None),
            T(key + '/t', x + 14, y + 11, w - 28, h - 22, [[(ln, dict(color=ink))] if isinstance(ln, str) else ln for ln in lines], size=pt,
              weight=weight, lnspc=lh * 0.75, align=align)], h


def box(key, x, y, w, h, on=False, fill='FFFFFF', radius=20, shadow=True, line=None, line_w=None):
    """흰 카드."""
    return R(key, x, y, w, h, prst='roundRect', radius=radius, fill=fill, line=line or (RING if on else LINE2),
             line_w=line_w or (1.8 if on else 1.2), shadow=SHADOW_CARD if shadow else None)


def titled(key, x, y, w, h, title, n=None, on=False, pt=14.5):
    """제목이 달린 흰 카드(번호 동그라미는 선택). 돌려줌: 원시 목록."""
    out = [box(key + '/bg', x, y, w, h, on=on)]
    tx = x + 22
    if n is not None:
        out += numdot(key + '/n', x + 34, y + 32, n, r=12, pt=10)
        tx = x + 54
    out.append(T(key + '/t', tx, y + 19, w - (tx - x) - 16, 26, title, size=pt, color=PURPLE, weight='b', anchor='ctr'))
    return out


def arrow(key, a, b, color=PURPLE2, w=1.8, dash=None, tail='triangle'):
    return C(key, [a, a, b, b], color=color, w=w, dash=dash, tail=tail)


def step(key, x, y, w, h, title, sub=None, style='base', pt=12, sub_pt=10):
    """흐름 그림의 한 칸: 이름(+ 아래 작은 글). style: base(옅은 회색), on(보라 테), fill(보라 바탕), ghost(점선)."""
    fill, ln, lw, ink, sink, dash = {'base': (GRAY_BG, None, 1.0, INK, SUB, None), 'on': (LAV, RING, 1.6, PURPLE, SUB, None),
                                     'fill': (PURPLE, None, 1.0, 'FFFFFF', 'E4DDFF', None), 'white': ('FFFFFF', LINE2, 1.2, INK, SUB, None),
                                     'ghost': ('FFFFFF', 'B9B2C9', 1.2, SUB, MUTE, 'dash')}[style]
    out = [R(key + '/bg', x, y, w, h, prst='roundRect', radius=14, fill=fill, line=ln, line_w=lw, dash=dash)]
    tl = title if isinstance(title, list) else [title]
    sl = [] if sub is None else (sub if isinstance(sub, list) else [sub])
    lh, slh = lh_of(pt, 1.32), lh_of(sub_pt, 1.32)
    th = lh * len(tl) + (slh * len(sl) + 2 if sl else 0)
    ty = y + (h - th) / 2
    out.append(T(key + '/t', x + 6, ty, w - 12, lh * len(tl) + 2, tl, size=pt, color=ink, weight='b', align='c', lnspc=lh * 0.75))
    if sl:
        out.append(T(key + '/s', x + 6, ty + lh * len(tl) + 2, w - 12, slh * len(sl) + 2, sl, size=sub_pt, color=sink, align='c', lnspc=slh * 0.75))
    return out


def tag(key, x, y, text, style='soft', pt=9.5, h=20, align='l'):
    """작은 알약 꼬리표. 돌려줌: (원시 목록, 폭)."""
    return chip(key, x, y, text, style, pt=pt, h=h, padx=9, align=align)

# ------------------------------------------------------------------ 빽빽한 표 (11-15 밤: 보충 자료는 내용을 많이, 정확히 → 장의 몸통을 표로)
def grid(s, key, x, y, w, cols, header, rows, pt=10.5, head_pt=10.5, padx=11, pady=7, hi=(), bold0=True, head_h=30, k=1.4, head_fill=LAV, vline=True):
    """줄 높이가 글에 맞는 표. cols = 칸의 상대 폭, header = 머리글(없으면 None),
    rows의 칸 = 문자열 | 줄 목록 | (문자열이나 줄 목록, {'color':…, 'weight':…}). hi = 옅게 칠할 줄 번호. 돌려줌: 높이."""
    tot = float(sum(cols))
    cw = [w * c / tot for c in cols]
    lh = lh_of(pt, k)

    def parse(t, j):
        opt = {}
        if isinstance(t, tuple):
            t, opt = t
        wt = opt.get('weight', 'b' if (bold0 and j == 0) else 'r')
        lines = []
        for part in (t if isinstance(t, list) else [t]):
            lines += rwrap(part, pt, cw[j] - 2 * padx, wt) if '**' in part else wrapl(part, pt, cw[j] - 2 * padx, wt)
        return lines, wt, opt.get('color', INK if (bold0 and j == 0) else BODY)
    parsed = [[parse(t, j) for j, t in enumerate(r)] for r in rows]
    heights = [max(len(c[0]) for c in r) * lh + 2 * pady for r in parsed]
    hh = head_h if header else 0
    h = hh + sum(heights)
    out = [R(key + '/bg', x, y, w, h, prst='roundRect', radius=12, fill='FFFFFF', line=LINE2, line_w=1.0)]
    if header:
        out += [R(key + '/hd', x + 1, y + 1, w - 2, hh - 1, prst='roundRect', radius=11, fill=head_fill, line=None),
                R(key + '/hd2', x + 1, y + hh - 12, w - 2, 12, fill=head_fill, line=None)]
        cx = x
        for j, t in enumerate(header):
            out.append(T('%s/h%d' % (key, j), cx + padx, y, cw[j] - 2 * padx, hh, t, size=head_pt, color=PURPLE, weight='b', anchor='ctr'))
            cx += cw[j]
    yy = y + hh
    for i, r in enumerate(parsed):
        if i in hi:
            if i == len(parsed) - 1:                     # 마지막 줄은 아래 모서리가 둥글어서 둥근 도형 + 윗부분 네모
                out += [R('%s/hi%d' % (key, i), x + 1, yy, w - 2, heights[i] - 1, prst='roundRect', radius=11, fill=LAV2, line=None),
                        R('%s/hi%db' % (key, i), x + 1, yy, w - 2, heights[i] - 14, fill=LAV2, line=None)]
            else:
                out.append(R('%s/hi%d' % (key, i), x + 1, yy, w - 2, heights[i], fill=LAV2, line=None))
        if i or header:
            out.append(R('%s/sp%d' % (key, i), x + 1, yy, w - 2, 1, fill='E6E0F5', line=None))
        cx = x
        for j, (lines, wt, col) in enumerate(r):
            out.append(T('%s/c%d_%d' % (key, i, j), cx + padx, yy + pady, cw[j] - 2 * padx, lh * len(lines) + 4, lines, size=pt, color=col, weight=wt,
                         lnspc=lh * 0.75))
            cx += cw[j]
        yy += heights[i]
    cx = x
    for j in range(len(cols) - 1):
        cx += cw[j]
        if vline:
            out.append(R('%s/v%d' % (key, j), cx, y + (hh if header else 6), 1, h - (hh if header else 12), fill='EEE9F8', line=None))
    s.add(key, out)
    return h


def label(s, key, x, y, text, pt=12.5, color=PURPLE):
    """표나 그림 위에 붙는 작은 이름."""
    s.add(key, [T(key, x, y, 900, 22, text, size=pt, color=color, weight='b', anchor='ctr')])
    return 26


def note(s, key, x, y, w, text, pt=10.5, color=SUB):
    """표 아래에 붙는 설명 글(폭에 맞춰 줄을 나눔). 돌려줌: 높이."""
    pr, h = para(key, x, y, w, text, pt=pt, color=color)
    s.add(key, [pr])
    return h


# ------------------------------------------------------------------ 3판 (11-16 새벽): 질문과 답 줄, 작은 그림, 막대, 파이프라인
# 1판은 문장 제목 + 부제 + 카드 셋(발표 장표 같고 내용이 얕음), 2판은 표 일색(눈에 안 들어옴)이라 둘 다 퇴짜.
# 3판의 장은 세 꼴 가운데 하나다: ① 질문과 답 줄(팀원의 Finder 장과 같은 짜임: Q, A 두세 줄, 오른쪽에 작은 그림)
# ② 파이프라인 그림 + 짧은 설명 ③ 꼭 필요한 표나 막대 하나 + 요점. 본문 글자는 12pt 이상, 표는 한 장에 하나.
BAR_SOFT, BAR_GRAY = 'CDBFFF', 'D8D3E3'
BLUE = '3E7BFA'


def rwrap(text, pt, w, weight='r', emph=None, color=None):
    """**강조** 표시가 든 글을 폭 w(px)에 맞춰 줄로 나눈다. 돌려줌: 줄 목록(줄 = [(글, 꾸밈)])."""
    emph = emph or dict(color=PURPLE, weight='b')
    base = {} if color is None else dict(color=color)
    lines = []
    for par in text.split('\n'):
        chars, on, i = [], False, 0
        while i < len(par):
            if par.startswith('**', i):
                on = not on
                i += 2
                continue
            chars.append((par[i], on))
            i += 1
        words, cur = [], []
        for ch, f in chars:
            if ch == ' ':
                words.append(cur)
                cur = []
            else:
                cur.append((ch, f))
        words.append(cur)

        def width(word):
            tot = 0
            for f, grp in itertools.groupby(word, key=lambda t: t[1]):
                tot += tw(''.join(c for c, _ in grp), pt, emph.get('weight', weight) if f else weight)
            return tot
        sp = tw('가 가', pt, weight) - tw('가가', pt, weight)
        line, lw = [], 0
        for wd in words:
            ww = width(wd)
            if line and lw + sp + ww > w:
                lines.append(line)
                line, lw = [wd], ww
            else:
                lw += (sp if line else 0) + ww
                line.append(wd)
        lines.append(line)
    out = []
    for line in lines:
        flat = []
        for k, wd in enumerate(line):
            if k:
                flat.append((' ', bool(flat) and bool(wd) and flat[-1][1] and wd[0][1]))
            flat += wd
        runs = [(''.join(c for c, _ in grp), dict(emph) if f else dict(base)) for f, grp in itertools.groupby(flat, key=lambda t: t[1])]
        out.append(runs or [('', {})])
    return out


def rich(s, key, x, y, w, text, pt=13, color=BODY, weight='r', k=1.5, align='l'):
    """**강조**가 든 문단. 돌려줌: 높이."""
    lines = rwrap(text, pt, w, weight)
    lh = lh_of(pt, k)
    s.add(key, [T(key, x, y, w, lh * len(lines) + 4, lines, size=pt, color=color, weight=weight, lnspc=lh * 0.75, align=align)])
    return lh * len(lines)


def points(s, key, x, y, w, items, pt=12.5, gap=7, color=BODY, k=1.45, dot=PURPLE):
    """요점 목록. 항목 = '**굵게** 보통' 꼴의 글. 돌려줌: 높이."""
    lh = lh_of(pt, k)
    out, yy = [], y
    for i, it in enumerate(items):
        lines = rwrap(it, pt, w - 16)
        out.append(R('%s/d%d' % (key, i), x, yy + lh / 2 - 2.5, 5, 5, prst='ellipse', fill=dot, line=None))
        out.append(T('%s/t%d' % (key, i), x + 16, yy, w - 16, lh * len(lines) + 4, lines, size=pt, color=color, lnspc=lh * 0.75))
        yy += lh * len(lines) + gap
    s.add(key, out)
    return yy - y - gap


def ring_gauge(key, cx, cy, ro, pct, color=PURPLE, track='E4DDF7', k=0.098):
    """고리 그래프(본 발표 7쪽, 33쪽과 같은 모양): 바탕 고리 + 12시에서 시계 방향으로 pct%만큼의 호. ro = 바깥 반지름, k = 굵기 ÷ 바깥지름. 돌려줌: 원시 목록."""
    adj = round(k * 100000)
    end = (16200000 + round(pct / 100 * 21600000)) % 21600000
    b = (cx - ro, cy - ro, 2 * ro, 2 * ro)
    return [R(key + '/track', *b, prst='donut', fill=track, line=None, adj=dict(adj=adj)),
            R(key + '/arc', *b, prst='blockArc', fill=color, line=None, adj=dict(adj1=16200000, adj2=end, adj3=adj))]


def panel(key, x, y, w, h, fill=GRAY_BG, radius=14):
    """그림이 들어가는 옅은 바탕."""
    return R(key, x, y, w, h, prst='roundRect', radius=radius, fill=fill, line=None)


def qrow(s, key, y, h, q, a, n=None, vis=None, vw=420, q_pt=15, a_pt=13, ref=None):
    """질문과 답 한 줄(흰 카드). 왼쪽에 Q와 A, 오른쪽에 작은 그림(vis(x, y, w, h) → 원시 목록). a = '**강조**'가 든 글이나 글 목록(문단마다 줄을 바꿈)."""
    x, w = X0, W0
    lab = 'Q.' if n is None else 'Q%d.' % n
    tx = x + 76
    aw = w - 76 - 24 - ((vw + 16) if vis else 0)
    out = [box(key + '/bg', x, y, w, h, radius=18),
           T(key + '/ql', x + 26, y + 16, 50, 26, lab, size=q_pt + 1, color=PURPLE, weight='b', anchor='ctr'),
           T(key + '/q', tx, y + 16, aw, 26, q, size=q_pt, color=INK, weight='b', anchor='ctr'),
           T(key + '/al', x + 26, y + 52, 50, 24, 'A.', size=a_pt + 1, color=PURPLE, weight='b', anchor='ctr')]
    lh = lh_of(a_pt, 1.5)
    yy = y + 52 + (24 - lh) / 2 + 1
    for i, par in enumerate(a if isinstance(a, list) else [a]):
        lines = rwrap(par, a_pt, aw)
        out.append(T('%s/a%d' % (key, i), tx, yy, aw, lh * len(lines) + 4, lines, size=a_pt, color=BODY, lnspc=lh * 0.75))
        yy += lh * len(lines) + 3
    if ref:
        out.append(T(key + '/ref', tx, yy + 2, aw, 18, ref, size=10, color=MUTE))
        yy += 20
    assert yy <= y + h - 8, '%s: 답이 카드를 넘침 (%d > %d)' % (key, yy, y + h - 8)
    if vis:
        px, py, pw, ph = x + w - 16 - vw, y + 14, vw, h - 28
        out.append(panel(key + '/pn', px, py, pw, ph))
        out += vis(px, py, pw, ph)
    s.add(key, out)


def hbars(key, x, y, w, items, vmax=None, pt=11, bar_h=14, gap=9, label_w=None, val_w=None, unit=''):
    """가로 막대. items = [(이름, 값, 값 글 또는 None, 강조 여부)]. 돌려줌: (원시 목록, 높이)."""
    vmax = vmax or max(v for _, v, _, _ in items)
    label_w = label_w or max(tw(n, pt, 'b' if hi else 'r') for n, _, _, hi in items) + 10
    vals = [(vt if vt is not None else ('%g%s' % (v, unit))) for _, v, vt, _ in items]
    val_w = val_w or max(tw(t, pt, 'b') for t in vals) + 8
    bw = w - label_w - val_w
    row = max(bar_h, lh_of(pt, 1.2))
    out, yy = [], y
    for i, ((name, v, _, hi), vt) in enumerate(zip(items, vals)):
        ln = max(3, bw * v / vmax)
        out += [T('%s/n%d' % (key, i), x, yy, label_w - 8, row, name, size=pt, color=INK if hi else SUB, weight='b' if hi else 'r', anchor='ctr', align='r'),
                R('%s/b%d' % (key, i), x + label_w, yy + (row - bar_h) / 2, ln, bar_h, prst='roundRect', radius=4, fill=PURPLE if hi else BAR_SOFT, line=None),
                T('%s/v%d' % (key, i), x + label_w + ln + 6, yy, val_w + 40, row, vt, size=pt, color=PURPLE if hi else SUB, weight='b', anchor='ctr')]
        yy += row + gap
    return out, yy - y - gap


def vis_bars(title, items, vmax=None, note=None, pt=11, unit=''):
    """qrow의 그림: 작은 제목 + 가로 막대 + 아래 한 줄."""
    def draw(x, y, w, h):
        gap = 9 if len(items) <= 2 else 5
        _, bh = hbars('vb', x + 18, 0, w - 36, items, vmax=vmax, pt=pt, unit=unit, gap=gap)
        tot = 20 + 6 + bh + (20 if note else 0)
        top = y + (h - tot) / 2
        bars, _ = hbars('vb/%s' % title[:6], x + 18, top + 26, w - 36, items, vmax=vmax, pt=pt, unit=unit, gap=gap)
        out = [T('vb/t', x + 18, top, w - 36, 20, title, size=10.5, color=INK, weight='b', anchor='ctr')] + bars
        if note:
            out.append(T('vb/n', x + 18, top + 26 + bh + 3, w - 36, 18, note, size=9.5, color=MUTE, anchor='ctr'))
        return out
    return draw


def vis_nums(items, pt=22):
    """qrow의 그림: 큰 숫자와 설명을 나란히. items = [(숫자, 설명 줄 목록)]."""
    def draw(x, y, w, h):
        n = len(items)
        cw = (w - 24) / n
        out = []
        for i, (num, cap) in enumerate(items):
            cx = x + 12 + i * cw
            cap = cap if isinstance(cap, list) else [cap]
            th = pt * 4 / 3 * 1.25 + 6 + lh_of(10.5, 1.4) * len(cap)
            top = y + (h - th) / 2
            if i:
                out.append(R('vn/l%d' % i, cx, y + 18, 1, h - 36, fill='E3DDF2', line=None))
            out += [T('vn/n%d' % i, cx, top, cw, pt * 4 / 3 * 1.25, num, size=pt, color=PURPLE, weight='b', align='c', anchor='ctr'),
                    T('vn/c%d' % i, cx + 6, top + pt * 4 / 3 * 1.25 + 6, cw - 12, lh_of(10.5, 1.4) * len(cap) + 4, cap, size=10.5, color=SUB, align='c',
                      lnspc=lh_of(10.5, 1.4) * 0.75)]
        return out
    return draw


def vis_steps(steps, note=None, pt=11, on=()):
    """qrow의 그림: 작은 흐름(상자 → 상자). steps = [이름 또는 (이름, 작은 글)]. on = 강조할 칸 번호."""
    def draw(x, y, w, h):
        n = len(steps)
        gap = 22
        bw = (w - 32 - gap * (n - 1)) / n
        bh = 54
        top = y + (h - bh - (24 if note else 0)) / 2
        out = []
        for i, st in enumerate(steps):
            name, sub = (st, None) if isinstance(st, str) else st
            bx = x + 16 + i * (bw + gap)
            out += step('vs/%d' % i, bx, top, bw, bh, name, sub, style='on' if i in on else 'white', pt=pt, sub_pt=9.5)
            if i < n - 1:
                out.append(arrow('vs/a%d' % i, (bx + bw + 3, top + bh / 2), (bx + bw + gap - 3, top + bh / 2), color='B9B2C9', w=1.4))
        if note:
            out.append(T('vs/n', x + 16, top + bh + 8, w - 32, 18, note, size=10, color=PURPLE, weight='b', align='c', anchor='ctr'))
        return out
    return draw


def vis_text(lines, pt=11.5):
    """qrow의 그림: 가운데 놓인 글 몇 줄(줄 = 글이나 [(글, 꾸밈)])."""
    def draw(x, y, w, h):
        lh = lh_of(pt, 1.55)
        th = lh * len(lines)
        return [T('vt/t', x + 18, y + (h - th) / 2, w - 36, th + 4, lines, size=pt, color=BODY, lnspc=lh * 0.75)]
    return draw


def vis_xo(bad, good, pt=11):
    """qrow의 그림: 하지 않는 것(✕)과 하는 것(✓) 두 줄. bad, good = 줄 목록."""
    def draw(x, y, w, h):
        lh = lh_of(pt, 1.5)
        hb, hg = lh * len(bad) + 16, lh * len(good) + 16
        top = y + (h - hb - hg - 8) / 2
        out = []
        for k, (lines, hh, mark, col, fill, yy) in enumerate(((bad, hb, '✕', 'C8323A', 'FFFFFF', top), (good, hg, '✓', PURPLE, 'FFFFFF', top + hb + 8))):
            out += [R('vx/%d' % k, x + 16, yy, w - 32, hh, prst='roundRect', radius=10, fill=fill, line='F2B8BA' if k == 0 else 'CFC3FF', line_w=1.0),
                    T('vx/%dm' % k, x + 26, yy, 22, hh, mark, size=pt + 2, color=col, weight='b', anchor='ctr'),
                    T('vx/%dt' % k, x + 50, yy + 8, w - 32 - 44, lh * len(lines) + 4, lines, size=pt, color=INK if k else BODY, weight='b' if k else 'r', lnspc=lh * 0.75)]
        return out
    return draw


def vis_rows(rows, pt=11, kw=64):
    """qrow의 그림: 이름과 설명을 한 줄씩(사이에 가는 줄). rows = [(이름, 글)]."""
    def draw(x, y, w, h):
        rh = 34
        top = y + (h - rh * len(rows)) / 2
        out = []
        for i, (a, b) in enumerate(rows):
            yy = top + i * rh
            if i:
                out.append(R('vr/l%d' % i, x + 18, yy, w - 36, 1, fill='E3DDF2', line=None))
            out += [T('vr/a%d' % i, x + 18, yy, kw, rh, a, size=pt, color=PURPLE, weight='b', anchor='ctr'),
                    T('vr/b%d' % i, x + 18 + kw, yy, w - 36 - kw, rh, b, size=pt, color=INK, weight='m', anchor='ctr')]
        return out
    return draw


TEAL = '14A3A8'
KIND = {'gen': (PURPLE, 'sLLM 생성'), 'emb': (BLUE, '임베딩 검색'), 'off': ('B9B2C9', 'Rule 기반'), 'cls': (TEAL, '임베딩 + 분류기'),
        'n': ('A996FF', ''), 'kw': ('B9B2C9', ''), 'sem': ('F26B3A', ''), 'rsn': (PURPLE, '')}      # n = 색 뜻이 없는 단계, kw/sem/rsn = 검색의 세 단계(주황은 일반 임베딩)
# cls(13차): 임베딩 벡터 위에 얹는 작은 분류기(먼저 건네는 기억의 챙길 일 분류기와 Gate 모델, C-7)


def legend(s, y, x=X0 + W0, kinds=('off', 'emb', 'gen')):
    """파이프라인의 색 설명(오른쪽 끝에 맞춤)."""
    out = []
    for k in kinds:
        col, lab = KIND[k]
        w = 18 + 6 + tw(lab, 10) + 16
        x -= w
        out += [R('pl/lg/%s' % k, x, y + 7, 18, 4, fill=col, line=None), T('pl/lg/%st' % k, x + 24, y, w - 24, 18, lab, size=10, color=SUB, anchor='ctr')]
    s.add('pl/lg', out)


def col_layout(n, x, w, gap, weights=None):
    """칸 n개의 (왼쪽 끝, 폭) 목록. weights = 칸의 상대 폭."""
    ws = list(weights or [1] * n)
    unit = (w - gap * (n - 1)) / float(sum(ws))
    out, cx = [], x
    for wi in ws:
        out.append((cx, unit * wi))
        cx += unit * wi + gap
    return out


def pipeline(s, key, y, h, steps, x=X0, w=W0, gap=16, name_pt=13, desc_pt=11, arrows=True, weights=None):
    """단계 카드를 한 줄로. steps = [(종류, 꼬리표, 이름, 설명, 아래 글)]. 카드 윗선의 색이 그 단계에서 도는 모델(KIND).
    h가 None이면 글에 맞춘 높이. weights = 칸의 상대 폭. 돌려줌: 카드의 높이."""
    n = len(steps)
    cols_ = col_layout(n, x, w, gap, weights)
    lhn, lhd = lh_of(name_pt, 1.3), lh_of(desc_pt, 1.45)
    cells = []
    for (kind, tagt, name, desc, foot_), (cx, cw) in zip(steps, cols_):
        nl = wrapl(name, name_pt, cw - 28, 'b') if isinstance(name, str) else name
        dl = rwrap(desc, desc_pt, cw - 28) if isinstance(desc, str) else desc
        cells.append((nl, dl))
    need = max(34 + lhn * len(nl) + 6 + lhd * len(dl) + (32 if st[4] else 10) for (nl, dl), st in zip(cells, steps))
    h = max(h or 0, need)
    for i, ((kind, tagt, name, desc, foot_), (nl, dl), (cx, cw)) in enumerate(zip(steps, cells, cols_)):
        col = KIND[kind][0]
        ny = y + 34
        dy = ny + lhn * len(nl) + 6
        out = [box('%s/%d/bg' % (key, i), cx, y, cw, h, radius=14, shadow=False),
               R('%s/%d/top' % (key, i), cx + 14, y, cw - 28, 4, fill=col, line=None),
               T('%s/%d/tag' % (key, i), cx + 14, y + 12, cw - 28, 18, tagt, size=10, color={'off': MUTE, 'kw': MUTE, 'n': PURPLE}.get(kind, col), weight='b'),
               T('%s/%d/n' % (key, i), cx + 14, ny, cw - 28, lhn * len(nl) + 4, nl, size=name_pt, color=INK, weight='b', lnspc=lhn * 0.75),
               T('%s/%d/d' % (key, i), cx + 14, dy, cw - 28, lhd * len(dl) + 4, dl, size=desc_pt, color=BODY, lnspc=lhd * 0.75)]
        if foot_:
            out.append(T('%s/%d/t' % (key, i), cx + 14, y + h - 28, cw - 28, 18, foot_, size=10.5, color={'off': MUTE, 'kw': MUTE, 'n': SUB}.get(kind, col),
                         weight='r' if kind == 'n' else 'b'))
        if arrows and i < n - 1:
            out.append(arrow('%s/%d/a' % (key, i), (cx + cw + 2, y + h / 2), (cx + cw + gap - 2, y + h / 2), color='A79FBD', w=1.6))
        s.add('%s/%d' % (key, i), out)
    return h


def timebar(s, key, x, y, w, segs, total, h=22, pt=10.5, title='걸리는 시간', pins=(), span=None, title_w=None, total_w=None):
    """시간 띠. segs = [(이름, 초(폭의 기준), 글, 종류)]. 폭이 좁은 칸의 글은 위에 선으로 이어 적는다.
    pins = [(몇째 칸 뒤, 글)]: 그 칸이 끝나는 자리에 아래로 표시를 단다. 돌려줌: 높이."""
    tot = span or sum(v for _, v, _, _ in segs)
    lw = title_w or (tw(title, pt, 'b') + 14)
    tw_tot = total_w or (tw(total, 12.5, 'b') + 12)
    bx, bw = x + lw, w - lw - tw_tot - 10
    out = [T(key + '/t', x, y + 20, lw, h, title, size=pt, color=INK, weight='b', anchor='ctr')]
    cx, ends = bx, []
    for i, (name, v, txt, kind) in enumerate(segs):
        sw = max(4, bw * v / tot)
        col = KIND[kind][0]
        out.append(R('%s/s%d' % (key, i), cx, y + 20, sw - 2, h, prst='roundRect', radius=5, fill=col, line=None))
        lab = ('%s %s' % (name, txt)).strip() if name else ''
        if not lab:
            pass
        elif tw(lab, pt, 'b') + 12 <= sw:
            out.append(T('%s/l%d' % (key, i), cx, y + 20, sw - 2, h, lab, size=pt, color='FFFFFF', weight='b', align='c', anchor='ctr'))
        else:
            out += [R('%s/tk%d' % (key, i), cx + sw / 2 - 1, y + 8, 1, 12, fill=col, line=None),
                    T('%s/l%d' % (key, i), cx + sw / 2 - 150, y - 10, 300, 18, lab, size=pt, color=col, weight='b', align='c', anchor='ctr')]
        cx += sw
        ends.append(cx)
    out.append(T(key + '/tot', (cx + 8) if span else (bx + bw + 10), y + 20, tw_tot + 60, h, total, size=12.5, color=PURPLE, weight='b', anchor='ctr'))
    for k, (after, lab) in enumerate(pins):
        px = ends[after] - 1
        out += [R('%s/p%d' % (key, k), px - 0.5, y + 20 + h, 1.5, 10, fill=INK, line=None),
                T('%s/pt%d' % (key, k), px - 200, y + 20 + h + 10, 400, 18, lab, size=pt, color=INK, weight='b', align='c', anchor='ctr')]
    s.add(key, out)
    return 20 + h + (30 if pins else 0)


def notes3(s, key, y, items, x=X0, w=W0, pt=12, gap=28, title_pt=13):
    """그림 아래에 놓는 짧은 설명 칸들(상자 없이 윗줄만). items = [(이름, '**강조**'가 든 글)]. 돌려줌: 높이."""
    n = len(items)
    cw = (w - gap * (n - 1)) / n
    hh = 0
    for i, (a, b) in enumerate(items):
        cx = x + i * (cw + gap)
        lines = rwrap(b, pt, cw)
        lh = lh_of(pt, 1.5)
        s.add('%s/%d' % (key, i), [R('%s/%d/ln' % (key, i), cx, y, cw, 2, fill='D9CFFF', line=None),
                                    T('%s/%d/a' % (key, i), cx, y + 10, cw, 22, a, size=title_pt, color=PURPLE, weight='b', anchor='ctr'),
                                    T('%s/%d/b' % (key, i), cx, y + 36, cw, lh * len(lines) + 4, lines, size=pt, color=BODY, lnspc=lh * 0.75)])
        hh = max(hh, 36 + lh * len(lines))
    return hh


def tbl(s, key, x, y, w, cols, header, rows, pt=12, hi=(), pady=9, head_h=34, bold0=True):
    """꼭 필요할 때만 쓰는 표(글자 12pt, 세로줄 없음). grid와 같은 인자."""
    return grid(s, key, x, y, w, cols, header, rows, pt=pt, head_pt=pt - 0.5, padx=14, pady=pady, hi=hi, bold0=bold0, head_h=head_h, k=1.45, vline=False)


def mini_rec(key, x, y, w, icon, title, meta=None, body=(), img=None, img_h=58, focus=(0.5, 0.5), on=False, bubble=False, pt=10.5):
    """작은 기록 카드: 앱 아이콘 + 굵은 이름 + 회색 '앱 · 날짜' + (본문 한두 줄 | 사진). 돌려줌: (원시 목록, 높이)."""
    from ui import ICON, P, crop_fit, GRAY_FILL
    pad, isz = 11, 24
    tx = x + pad + isz + 8
    body = [body] if isinstance(body, str) else list(body)
    lines = []
    for b in body:
        lines += wrapl(b, pt, w - 2 * pad - (16 if bubble else 0))
    lh = lh_of(pt, 1.4)
    h = pad + isz + pad
    by = y + pad + isz + 8
    if lines:
        h = (by - y) + lh * len(lines) + (10 if bubble else 0) + pad - 2
    if img:
        h = (by - y) + img_h + pad
    out = [R(key + '/bg', x, y, w, h, prst='roundRect', radius=14, fill='FFFFFF', line=RING if on else 'E0D9F2', line_w=1.6 if on else 1.0, shadow=SHADOW_SOFT),
           P(key + '/ic', ICON.get(icon, icon), x + pad, y + pad, isz, isz)]
    if meta:
        out += [T(key + '/n', tx, y + pad - 3, w - (tx - x) - pad, 17, title, size=11, color=INK, weight='b'),
                T(key + '/m', tx, y + pad + 12, w - (tx - x) - pad, 15, meta, size=9, color=MUTE)]
    else:
        out.append(T(key + '/n', tx, y + pad, w - (tx - x) - pad, isz, title, size=11, color=INK, weight='b', anchor='ctr'))
    if lines:
        if bubble:
            out.append(R(key + '/bb', x + pad, by, w - 2 * pad, lh * len(lines) + 10, prst='roundRect', radius=10, fill=GRAY_FILL, line=None))
        out.append(T(key + '/b', x + pad + (8 if bubble else 0), by + (5 if bubble else 0), w - 2 * pad - (16 if bubble else 0), lh * len(lines) + 4, lines,
                     size=pt, color=BODY, lnspc=lh * 0.75))
    if img:
        out.append(P(key + '/img', img, x + pad, by, w - 2 * pad, img_h, radius=9, crop=crop_fit(img, w - 2 * pad, img_h, focus)))
    return out, h


def mini_out(key, x, y, w, head, lines, pt=11, icon=None):
    """Weave가 건네는 것(보라 테 카드): 작은 머리글 + 굵은 글. 돌려줌: (원시 목록, 높이)."""
    from ui import ICON, P
    pad = 11
    ll = []
    for b in ([lines] if isinstance(lines, str) else lines):
        ll += wrapl(b, pt, w - 2 * pad, 'b')
    lh = lh_of(pt, 1.4)
    h = pad + 18 + 6 + lh * len(ll) + pad - 2
    out = [R(key + '/bg', x, y, w, h, prst='roundRect', radius=14, fill=LAV2, line=RING, line_w=1.6),
           P(key + '/ic', ICON['spool'], x + pad, y + pad, 16, 16),
           T(key + '/h', x + pad + 21, y + pad - 1, w - 2 * pad - 21, 18, head, size=9.5, color=PURPLE, weight='b', anchor='ctr'),
           T(key + '/t', x + pad, y + pad + 24, w - 2 * pad, lh * len(ll) + 4, ll, size=pt, color=INK, weight='b', lnspc=lh * 0.75)]
    return out, h


def mini_q(key, x, y, w, lines, pt=10.5, head=None, fill=GRAY_BG, ink=INK):
    """질의나 조건을 적는 작은 칸(옅은 바탕). lines = 글 목록(줄마다 따로 줄을 나눔). 돌려줌: (원시 목록, 높이)."""
    pad = 10
    ll = []
    for b in ([lines] if isinstance(lines, str) else lines):
        ll += wrapl(b, pt, w - 2 * pad, 'm')
    lh = lh_of(pt, 1.45)
    hh = 17 if head else 0
    h = pad + hh + lh * len(ll) + pad - 2
    out = [R(key + '/bg', x, y, w, h, prst='roundRect', radius=12, fill=fill, line=None)]
    if head:
        out.append(T(key + '/h', x + pad, y + pad - 2, w - 2 * pad, 16, head, size=9, color=MUTE, weight='b'))
    out.append(T(key + '/t', x + pad, y + pad + hh, w - 2 * pad, lh * len(ll) + 4, ll, size=pt, color=ink, weight='m', lnspc=lh * 0.75))
    return out, h


def data_row(s, key, y, cells, x=X0, w=W0, gap=16, weights=None):
    """파이프라인 카드 아래에 그 단계의 실제 기록을 칸마다 놓는다. cells = [(종류, 인자 dict) | 그 목록 | None]. 종류: rec, out, q. 돌려줌: 가장 큰 높이."""
    cols_ = col_layout(len(cells), x, w, gap, weights)
    hh = 0
    for i, c in enumerate(cells):
        if not c:
            continue
        cx, cw = cols_[i]
        out = [R('%s/%d/ln' % (key, i), cx + cw / 2 - 0.5, y, 1, 12, fill='C9C0E6', line=None)]
        yy = y + 12
        for j, (kind, kw) in enumerate(c if isinstance(c, list) else [c]):
            fn = {'rec': mini_rec, 'out': mini_out, 'q': mini_q}[kind]
            pr, h = fn('%s/%d_%d' % (key, i, j), cx, yy, cw, **kw)
            out += pr
            yy += h + 8
        s.add('%s/%d' % (key, i), out)
        hh = max(hh, yy - 8 - y)
    return hh


# ------------------------------------------------------------------ 틀
def frame(s, code):
    """코드와 묶음 이름(왼쪽 위), 쪽 번호와 '목차' 단추(오른쪽 위). 본문의 왼쪽 끝(70)과 오른쪽 끝(1210)에 맞춘다.
    쪽 번호는 finish()가 슬라이드 번호 필드로 바꾼다."""
    c, w = chip('qna/code', X0, 28, code, 'fill', pt=10.5, h=24, padx=10)
    s.add('qna/code', c + [T('qna/sec', X0 + w + 8, 28, 300, 24, SECTIONS[group_of(code)], size=10.5, color=MUTE, anchor='ctr')])
    b, bw = chip('qna/toc', X0 + W0, 28, '목차', 'outline', pt=10, h=24, padx=12, align='r')
    s.add('qna/toc', b)
    s.add('qna/pg', [T('qna/pg', X0 + W0 - bw - 10 - 60, 28, 60, 24, '0', size=11, color=MUTE, weight='b', align='r', anchor='ctr')])
    return s


def page_slide(key, code, title_runs, sub=None, size=22):
    """틀과 제목이 놓인 빈 장. 제목은 주제를 적은 구절이나 질문 그대로이고 부제는 두지 않는다(sub는 옮겨 온 장을 위해 남김)."""
    s = Slide(key, trans=('fade', 400), bar=False, notes='')
    head(s, title_runs, sub, y=50, size=size)
    return frame(s, code)


def footnote(s, lines, y):
    """각주. lines = 문자열 목록(한 줄에 하나). 본문의 왼쪽 끝에 맞춘다."""
    text = lines if isinstance(lines, list) else [lines]
    s.add('apx/foot', [T('apx/foot', X0, y, W0, 13 * len(text) + 6, text, size=8.5, color='8E88A0', lnspc=13 * 0.75)])


def closing(key, y, text, pt=14):
    """장을 맺는 한 줄(가운데, 굵게). 보라 띠 대신 쓴다."""
    return [T(key, X0, y, W0, 30, text, size=pt, color=INK, weight='b', align='c', anchor='ctr')]


def cols(key, x, y, w, h, items, title_pt=12.5, pt=11.5, on=None):
    """흰 카드 하나를 세로 줄로 나눈 칸들. items = [(이름, 글)] (글은 문자열이나 줄 목록). on = 강조할 칸 번호. 돌려줌: 원시 목록."""
    n = len(items)
    cw = w / n
    out = [box(key + '/bg', x, y, w, h)]
    for i, (a, b) in enumerate(items):
        cx = x + i * cw
        if i:
            out.append(R('%s/ln%d' % (key, i), cx, y + 16, 1, h - 32, fill='E6E0F5', line=None))
        out.append(T('%s/a%d' % (key, i), cx + 22, y + 16, cw - 44, 24, a, size=title_pt, color=PURPLE if (on is None or on == i) else INK, weight='b'))
        lines = wrapl(b, pt, cw - 44) if isinstance(b, str) else list(b)
        out.append(T('%s/b%d' % (key, i), cx + 22, y + 44, cw - 44, lh_of(pt) * len(lines) + 4, lines, size=pt, color=BODY, lnspc=lh_of(pt) * 0.75))
    return out


# ------------------------------------------------------------------ 옮겨 온 장에 덧그리기, 필드와 이동
def live_tree(slide):
    return slide._element.find('{%s}cSld' % P_NS).find('{%s}spTree' % P_NS)


def overlay(slide):
    """다른 덱에서 옮겨 온 장에 원시 도형을 그려 넣는 붓(make.painter와 같음)."""
    pa = Painter(slide)
    pa.tree = live_tree(slide)
    ids = [int(e.get('id')) for e in pa.tree.iter() if e.tag.endswith('}cNvPr') and (e.get('id') or '').isdigit()]
    pa.ids = itertools.count(max(ids) + 1)
    return pa


def draw_on(slide, s):
    """빈 Slide(틀만 든 것)의 부품을 옮겨 온 장 위에 그린다."""
    pa = overlay(slide)
    for key, prims, alpha, xf, group, temp, start in s.items:
        pa.put(key, prims, alpha=alpha, group=group)


def named(slide, name):
    return [e for e in live_tree(slide).iter() if e.tag.endswith('}cNvPr') and e.get('name') == name]


def retext(slide, old, new):
    """장 안의 글 조각(a:t)에서 old를 new로 바꾼다. 돌려줌: 바꾼 곳 수."""
    n = 0
    for t in live_tree(slide).iter('{%s}t' % A_NS):
        if t.text and old in t.text:
            t.text = t.text.replace(old, new)
            n += 1
    return n


def _field(slide):
    """'!!qna/pg' 글 상자의 글을 슬라이드 번호 필드로 바꾼다."""
    for nv in named(slide, '!!qna/pg'):
        sp = nv.getparent().getparent()
        for r in sp.iter('{%s}r' % A_NS):
            fld = etree.SubElement(r.getparent(), '{%s}fld' % A_NS)
            fld.set('id', '{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}')
            fld.set('type', 'slidenum')
            for ch in list(r):
                fld.append(ch)
            r.getparent().replace(r, fld)
            for t in fld.iter('{%s}t' % A_NS):
                t.text = '‹#›'


def _link(slide, name, target):
    """이름이 name인 도형(묶음이면 그 안의 도형 모두)을 누르면 target 장으로 가게 한다."""
    rid = slide.part.relate_to(target.part, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide')
    n = 0
    for nv in named(slide, name):
        root = nv.getparent().getparent()
        for e in root.iter():
            if not e.tag.endswith('}cNvPr'):
                continue
            if e.getparent().tag.endswith('}nvGrpSpPr'):
                continue
            for old in e.findall('{%s}hlinkClick' % A_NS):
                e.remove(old)
            h = etree.SubElement(e, '{%s}hlinkClick' % A_NS)
            h.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', rid)
            h.set('action', 'ppaction://hlinksldjump')
            e.insert(0, h)
            n += 1
    return n


def finish(slides, toc):
    """slides = {코드: 장}, toc = 목차 장. 쪽 번호 필드를 넣고, '목차' 단추와 목차의 항목에 이동을 건다."""
    for code, sl in slides.items():
        _field(sl)
        _link(sl, '!!qna/toc', toc)
        _link(toc, '!!toc/' + code, sl)
    _field(toc)
