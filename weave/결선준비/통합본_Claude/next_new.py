"""9차 후보(11-14): 연표(35쪽) 다음의 '앞으로의 Weave' 장. 덱에는 아직 넣지 않았고 tools/next_try.py로 후보 덱, 그림, 낭독 영상을 만든다.

짜임
- 35쪽에서 넘기면(Morph) 연표 전체가 왼쪽으로 옮겨 가고(옛 마디는 옮겨 가며 사라짐) Weave 마디만 왼쪽에 남는다.
- Weave에서 실이 오른쪽으로 이어지고, 클릭할 때마다 같은 크기의 카드가 하나씩 실에 꿰인다. 카드 위에 이름(굵게)과 한 줄(옅게).
- 카드 = 위쪽에 장면 그림, 아래쪽에 Weave가 건네는 것(찾은 사진, 또는 두 줄의 말과 그 말이 나온 기록 한 줄).
  어느 자리에 어느 카드를 넣어도 틀이 같아 그대로 맞는다(두 장만 넣으면 카드가 넓어짐).

자리와 후보 (CARDS)
- 자리 1 '그려서 찾는 기억'(S펜 + 멀티모달 임베딩): 서툰 풍경 그림과 어설픈 손글씨 단서 → 그날의 사진
- 자리 2 '집에서 건네는 기억'(SmartThings + Bixby, 먼저 건네는 기억의 다음): 잊고 있던 것을 가전이 먼저 말해 줌
- 자리 3 상상: TV, 안경, 차

좌표는 1280×720 px. 말할 글은 next_note()((클릭) = 그 자리에서 클릭).
그림: assets/next/ (tools/next_assets.py). 손그림과 사진은 codex 이미지 생성, 앱 아이콘은 Galaxy Store와 Google Play의 것.
"""
import math
from pathlib import Path

from lxml import etree

import build as HW
from hiw_lib import q
from ui import (BODY, ICON, INK, INK2, LAV2, LINE, MUTE, PURPLE, PURPLE2, SUB, SHADOW_CARD,
                C, P, R, T, Xf, crop_fit, line, spark_icon, star4_icon, tw)

import slides_new as N

Slide = HW.Slide
HERE = Path(__file__).resolve().parent
AS = HERE / 'assets' / 'next'

# ------------------------------------------------------------------ 자리
PAN = 926                                   # 연표가 왼쪽으로 옮겨 가는 만큼(px). Weave 마디가 x 1140 → 214
WX, YC = N.TL_WX - PAN, N.TL_YC             # 옮겨 간 뒤 Weave 마디의 가운데
X0, X1 = 334, 1218                          # 카드가 놓이는 가로 범위
GAP = 22                                    # 카드 사이
CY, CH = 206, 392                           # 카드의 위, 높이(실은 카드의 한가운데쯤을 지남)
NAME_Y = 144                                # 카드 위 이름(18pt)의 위. 그 아래 한 줄(12.5pt)
CW0 = 280                                   # 카드 속 그림을 그릴 때의 기준 폭(세 장일 때의 카드 폭)
REPLY_Y = CH - 136                          # 건네는 말 칸의 위(카드 위에서부터). 그 위 14 ~ 248px이 장면 그림의 자리
GRAD = dict(stops=[(0, '8D6BFF', None), (100, '5A3FE0', None)], ang=55)
TITLE = [('휴대폰을 넘어, ', INK), ('갤럭시의 모든 기기로', PURPLE)]


# ------------------------------------------------------------------ 연표(35쪽)의 부품: 키와 모양은 slides_new.s_tl과 같다(Morph로 이어짐)
def tl_parts(s, dx=0, ghost=False, title=True):
    """연표를 dx만큼 옮겨 그린다. ghost면 마디와 이름표는 투명하게(옮겨 가며 사라짐), 각주는 넣지 않는다. 돌려줌: (위 마디 키, 아래 마디 키)."""
    xf = Xf(0, 0, dx, 0, 1.0)
    a = 0 if ghost else 100
    if title:
        s.add('tl/title', [N.title('tl/title', [('갤럭시라서', PURPLE), (', 그리고 ', INK), ('지금이라서', PURPLE), (' 되는 Weave', INK)])])
    s.add('tl/lu', [C('tl/lu', [(N.TL_X0, N.TL_YU)] * 2 + [(N.TL_X1, N.TL_YU)] * 2, stops=N.TL_STOPS, w=3)], xf=xf)
    s.add('tl/ll', [C('tl/ll', [(N.TL_X0, N.TL_YL)] * 2 + [(N.TL_X1, N.TL_YL)] * 2, stops=N.TL_STOPS, w=3)], xf=xf)
    ex = N.TL_WX - 30
    s.add('tl/ju', [C('tl/ju', [(N.TL_X1, N.TL_YU), (N.TL_X1 + 44, N.TL_YU), (ex - 44, N.TL_YC), (ex, N.TL_YC)], w=3, color=PURPLE)], xf=xf)
    s.add('tl/jl', [C('tl/jl', [(N.TL_X1, N.TL_YL), (N.TL_X1 + 44, N.TL_YL), (ex - 44, N.TL_YC), (ex, N.TL_YC)], w=3, color=PURPLE)], xf=xf)
    s.add('tl/now', N.tl_label('tl/now', N.TL_YU, 'WHY NOW', '지금이라서'), xf=xf, alpha=a)
    s.add('tl/sam', N.tl_label('tl/sam', N.TL_YL, 'WHY SAMSUNG', '갤럭시라서'), xf=xf, alpha=a)
    ups, dns = [], []
    for x, year, word, ref, icon in N.TL_UP:
        k = 'tl/u%d' % x
        s.add(k, N.tl_node(k, x, N.TL_YU, True, year, word, ref, icon), xf=xf, alpha=a)
        ups.append(k)
    for x, year, word, ref, icon in N.TL_DN:
        k = 'tl/d%d' % x
        s.add(k, N.tl_node(k, x, N.TL_YL, False, year, word, ref, icon), xf=xf, alpha=a)
        dns.append(k)
    wx = N.TL_WX
    s.add('tl/wglow', [R('tl/wglow', wx - 56, N.TL_YC - 56, 112, 112, prst='ellipse', fill=None, line=None,
                         grad=dict(stops=[(0, '8B6BFF', 46), (60, 'B9A6FF', 16), (100, 'F2EDFF', 0)], path='circle'))], xf=xf)
    s.add('tl/w', [R('tl/w/c', wx - 30, N.TL_YC - 30, 60, 60, prst='ellipse', line='FFFFFF', line_w=2.5, shadow=(18, 6, '6B4EFF', 30),
                     grad=dict(stops=[(0, '8D6BFF', None), (100, '5A3FE0', None)], ang=55)),
                   P('tl/w/sp', ICON['spool_w'], wx - 17, N.TL_YC - 17, 34, 34),
                   T('tl/w/n', wx - 70, N.TL_YC + 38, 140, 28, 'Weave', size=17, color=PURPLE, weight='b', align='c', anchor='ctr')], xf=xf)
    if not ghost:
        s.add('tl/src', [T('tl/src', 60, 648, 1160, 44, N.TL_SRC, size=9, color=MUTE, wrap=True, lnspc=13)])
    return ups, dns


TL_END_NOTE = '기술과 인프라가 모두 준비된 지금이, Weave가 필요한 때입니다.'      # 35쪽의 마지막 구간(후보 영상은 여기서 시작)


def s_tl_end(key='tl_end'):
    """후보 영상의 첫 장: 35쪽에서 두 줄의 마디가 이미 다 뜬 모습. 장이 열리면 두 줄이 Weave에서 만난다(덱에서는 35쪽의 셋째 클릭)."""
    s = Slide(key, trans=('fade', 320), bar=False, notes=TL_END_NOTE)
    tl_parts(s)
    s.on(['tl/ju', 'tl/jl'], 'wipe_in', 250, 520)
    s.on('tl/wglow', 'fade_in', 670, 500)
    s.on('tl/w', 'zoom_in', 730, 420, **{'from': 0.6})
    s.on('tl/w', 'pulse', 1190, 180, scale=1.08)
    return s


# ------------------------------------------------------------------ 작은 그림 조각
def arc(key, cx, cy, r, a0, a1, **o):
    """원의 한 토막(도, 시계 방향이 +, 0 = 오른쪽)을 3차 곡선 하나로."""
    t0, t1 = math.radians(a0), math.radians(a1)
    k = 4 / 3 * math.tan((t1 - t0) / 4) * r
    p0 = (cx + r * math.cos(t0), cy + r * math.sin(t0))
    p3 = (cx + r * math.cos(t1), cy + r * math.sin(t1))
    c1 = (p0[0] - k * math.sin(t0), p0[1] + k * math.cos(t0))
    c2 = (p3[0] + k * math.sin(t1), p3[1] - k * math.cos(t1))
    return C(key, [p0, c1, c2, p3], **o)


def poly(key, pts, **o):
    """꼭짓점을 곧은 선으로 이은 닫힌 도형(px)."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    bx, by, bw, bh = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    cg = etree.Element(q('a:custGeom'))
    for t in ('a:avLst', 'a:gdLst', 'a:ahLst', 'a:cxnLst'):
        etree.SubElement(cg, q(t))
    etree.SubElement(cg, q('a:rect'), l='l', t='t', r='r', b='b')
    path = etree.SubElement(etree.SubElement(cg, q('a:pathLst')), q('a:path'), w=str(round(bw * 100)), h=str(round(bh * 100)))
    for i, (x, y) in enumerate(pts):
        e = etree.SubElement(path, q('a:moveTo' if i == 0 else 'a:lnTo'))
        etree.SubElement(e, q('a:pt'), x=str(round((x - bx) * 100)), y=str(round((y - by) * 100)))
    etree.SubElement(path, q('a:close'))
    return R(key, bx, by, bw, bh, custom_path=cg, **o)


def glow(key, cx, cy, r, a=26):
    return R(key, cx - r, cy - r, 2 * r, 2 * r, prst='ellipse', fill=None, line=None,
             grad=dict(stops=[(0, 'B9A6FF', a), (55, 'D9CEFA', a * 0.42), (100, 'F2EDFF', 0)], path='circle'))


def floor(key, cx, y, w, a=10):
    return R(key, cx - w / 2, y - 5, w, 10, prst='ellipse', fill='4B3BB0', alpha=a, line=None)


METAL = dict(stops=[(0, 'F8F9FC', None), (100, 'E1E4EF', None)], ang=90)      # 가전의 몸(밝은 금속)
EDGE = 'C3C7D9'
DARK = dict(stops=[(0, '3B3470', None), (100, '1C1930', None)], ang=60)        # 화면(짙은 보라)


def voice(key, x, cy, color=PURPLE2, n=5, h=18):
    """말하는 중임을 알리는 작은 막대들."""
    hs = [0.45, 1.0, 0.62, 0.32, 0.8][:n]
    return [R('%s/v%d' % (key, i), x + i * 5.4, cy - h * k / 2, 2.8, h * k, prst='roundRect', fill=color, line=None) for i, k in enumerate(hs)]


# ------------------------------------------------------------------ 카드의 틀
def card_box(n, i):
    """n장 가운데 i째 카드의 (x, 폭)."""
    w = (X1 - X0 - GAP * (n - 1)) / n
    return X0 + i * (w + GAP), w


def card_frame(key, x, w):
    return [R(key + '/bg', x, CY, w, CH, prst='roundRect', radius=24, fill='FFFFFF', line=LINE, line_w=1.0, shadow=SHADOW_CARD)]


def card_head(key, x, w, name, sub):
    """카드 위의 이름과 한 줄. sub = [(아이콘 파일 또는 None, 글)] — 아이콘이 있으면 글 앞에 작게, 아이콘이 하나도 없으면 가운뎃점으로 이은 한 줄."""
    cx = x + w / 2
    out = [T(key + '/name', x - 20, NAME_Y, w + 40, 28, name, size=18, color=INK, weight='b', align='c', anchor='ctr', spc=-0.3)]
    pt, isz, g1, g2 = 12.5, 16, 5, 14
    if not any(ic for ic, _ in sub):
        return out + [T(key + '/st', x - 20, NAME_Y + 31, w + 40, 22, ' · '.join(t for _, t in sub), size=pt, color=SUB, weight='m', align='c', anchor='ctr')]
    widths = [(isz + g1 if ic else 0) + tw(t, pt, 'm') for ic, t in sub]
    px = cx - (sum(widths) + g2 * (len(sub) - 1)) / 2
    for j, ((ic, t), wd) in enumerate(zip(sub, widths)):
        if ic:
            out.append(P('%s/si%d' % (key, j), str(ic), px, NAME_Y + 34, isz, isz))
        tx = px + (isz + g1 if ic else 0)
        out.append(T('%s/st%d' % (key, j), tx, NAME_Y + 31, tw(t, pt, 'm') + 8, 22, t, size=pt, color=SUB, weight='m', anchor='ctr'))
        px += wd + g2
    return out


def reply(key, x, w, icon, l1, l2, src=None):
    """카드 아래쪽: Weave(또는 Bixby)가 건네는 두 줄 + 그 말이 나온 기록 한 줄. icon = 'spool' 또는 그림 파일. src = (앱 아이콘 키, 이름, 글)."""
    y = CY + REPLY_Y
    px, pw, ph = x + 14, w - 28, 70
    isz = 26
    out = [R(key + '/rp', px, y, pw, ph, prst='roundRect', radius=17, fill=LAV2, line='E9E2FB', line_w=1.0)]
    ix, iy = px + 12, y + (ph - isz) / 2
    if icon == 'spool':
        out += [R(key + '/ri', ix, iy, isz, isz, prst='roundRect', radius=8, line=None, grad=GRAD),
                P(key + '/rs', ICON['spool_w'], ix + 5, iy + 5, isz - 10, isz - 10)]
    else:
        out.append(P(key + '/ri', str(icon), ix, iy, isz, isz))
    tx = ix + isz + 9
    room = px + pw - 14 - tx
    p1 = next((p for p in (12.5, 12, 11.5) if tw(l1, p, 'b') <= room), None)
    p2 = next((p for p in (11.5, 11, 10.5) if tw(l2, p) <= room), None)
    assert p1 and p2, (key, l1, round(tw(l1, 11.5, 'b')), l2, round(tw(l2, 10.5)), round(room))
    out += [T(key + '/r1', tx, y + 12, room + 6, 24, l1, size=p1, color=INK, weight='b', anchor='ctr'),
            T(key + '/r2', tx, y + 35, room + 6, 22, l2, size=p2, color=BODY, anchor='ctr')]
    if src:                             # 덱의 '연결된 기억' 줄처럼: 앱 아이콘, 굵은 이름, 옅은 글
        app, name, rest = src
        sy = y + ph + 14
        assert tw(name, 10, 'b') + tw(' ' + rest, 10) <= pw - 30, (key, name, rest)
        out += [P(key + '/sa', ICON.get(app, app), px + 5, sy, 17, 17),
                T(key + '/sx', px + 28, sy - 2, pw - 30, 21, [[(name, dict(color=INK2, weight='b')), (' ' + rest, dict(color=SUB))]], size=10, anchor='ctr')]
    return out


# ------------------------------------------------------------------ 자리 2의 장면: 가전 (ox = 280px 그림 칸의 왼쪽, oy = 카드의 위)
def sc_fridge(key, ox, oy):
    """Bespoke AI 패밀리허브: 문 넷, 오른쪽 위 문에 화면."""
    cx, top, w, h = ox + 134, oy + 30, 122, 204
    x = cx - w / 2
    split = top + h * 0.6
    out = [glow(key + '/gl', cx + 6, top + h * 0.5, 138), floor(key + '/fl', cx, top + h + 3, 164),
           R(key + '/body', x, top, w, h, prst='roundRect', radius=9, fill=None, grad=METAL, line=EDGE, line_w=1.3, shadow=(16, 6, '5B3FE6', 13)),
           line(key + '/sv', (cx, top + 3), (cx, top + h - 3), color=EDGE, w=1.3),
           line(key + '/sh', (x + 3, split), (x + w - 3, split), color=EDGE, w=1.3),
           R(key + '/h1', cx - 7, top + h * 0.30, 2.6, 30, prst='roundRect', fill='A9AEC6', line=None),
           R(key + '/h2', cx + 4.4, top + h * 0.30, 2.6, 30, prst='roundRect', fill='A9AEC6', line=None),
           R(key + '/h3', cx - 34, split + 9, 25, 2.6, prst='roundRect', fill='A9AEC6', line=None),
           R(key + '/h4', cx + 9, split + 9, 25, 2.6, prst='roundRect', fill='A9AEC6', line=None)]
    sw, sh = 40, 74
    sx, sy = cx + 12.5, top + 19
    out += [R(key + '/scr', sx, sy, sw, sh, prst='roundRect', radius=4.5, fill=None, grad=DARK, line=None),
            R(key + '/s1', sx + 6, sy + 9, sw - 12, 3.4, prst='roundRect', fill='FFFFFF', alpha=88, line=None),
            R(key + '/s2', sx + 6, sy + 17, (sw - 12) * 0.6, 3.4, prst='roundRect', fill='FFFFFF', alpha=50, line=None),
            R(key + '/s3', sx + 6, sy + sh - 21, sw - 12, 13, prst='roundRect', radius=4, fill=PURPLE2, line=None)]
    out += voice(key + '/vo', x + w + 15, sy + sh / 2)
    return out


def sc_washer(key, ox, oy):
    """Bespoke AI 콤보(세탁건조기): 위에 화면이 있는 띠, 가운데 둥근 문. 문 안에 니트 한 벌."""
    cx, top, w, h = ox + 134, oy + 36, 146, 196
    x = cx - w / 2
    dy = top + 38 + (h - 38) / 2 - 2            # 문의 가운데
    out = [glow(key + '/gl', cx + 6, top + h * 0.5, 138), floor(key + '/fl', cx, top + h + 3, 180),
           R(key + '/body', x, top, w, h, prst='roundRect', radius=11, fill=None, grad=METAL, line=EDGE, line_w=1.3, shadow=(16, 6, '5B3FE6', 13)),
           line(key + '/bar', (x + 3, top + 34), (x + w - 3, top + 34), color=EDGE, w=1.3),
           R(key + '/scr', cx - 25, top + 9, 50, 17, prst='roundRect', radius=4.5, fill=None, grad=DARK, line=None),
           R(key + '/s1', cx - 17, top + 16, 20, 3.2, prst='roundRect', fill='FFFFFF', alpha=85, line=None),
           R(key + '/dot', x + w - 23, top + 12, 11, 11, prst='ellipse', fill='FFFFFF', line=EDGE, line_w=1.3),
           R(key + '/ring', cx - 56, dy - 56, 112, 112, prst='ellipse', fill=None, grad=dict(stops=[(0, 'FFFFFF', None), (100, 'D5D9E8', None)], ang=60), line=EDGE, line_w=1.3),
           R(key + '/glass', cx - 44, dy - 44, 88, 88, prst='ellipse', fill=None, grad=dict(stops=[(0, '4A4388', None), (100, '1E1B36', None)], ang=55), line='8E8AB0', line_w=1.3)]
    k = 1.25                                    # 니트: 목, 어깨, 소매, 몸통
    knit = [(-6, -14), (-11, -15), (-23, -3), (-17, 4), (-12, -1), (-12, 16), (12, 16), (12, -1), (17, 4), (23, -3), (11, -15), (6, -14), (0, -10)]
    out += [poly(key + '/knit', [(cx + px * k, dy + 1 + py * k) for px, py in knit], fill='C9BBFF', line=None),
            arc(key + '/hl', cx, dy, 35, 198, 262, color='FFFFFF', w=3.4, alpha=50)]
    out += voice(key + '/vo', x + w + 14, top + 17)
    return out


def sc_robot(key, ox, oy):
    """Bespoke AI 스팀(로봇청소기)을 위에서 본 모습. 지나온 길에 옅은 줄과 반짝임."""
    cx, cy, r = ox + 160, oy + 130, 60
    out = [glow(key + '/gl', cx - 10, cy, 138), floor(key + '/fl', cx, cy + r + 7, 136, 9),
           C(key + '/path', [(ox + 22, oy + 196), (ox + 62, oy + 228), (ox + 92, oy + 174), (cx - r - 7, cy + 20)], color=PURPLE2, w=2.8, alpha=70, dash='dash'),
           R(key + '/body', cx - r, cy - r, 2 * r, 2 * r, prst='ellipse', fill=None, grad=dict(stops=[(0, 'FFFFFF', None), (100, 'E4E7F1', None)], ang=70), line=EDGE, line_w=1.4,
             shadow=(16, 6, '5B3FE6', 14)),
           R(key + '/lid', cx - r + 10, cy - r + 10, 2 * r - 20, 2 * r - 20, prst='ellipse', fill=None, line='D5D8E6', line_w=1.3),
           R(key + '/tur', cx - 16, cy - 33, 32, 32, prst='ellipse', fill=None, grad=dict(stops=[(0, 'F4F5FA', None), (100, 'CDD1E2', None)], ang=60), line='B3B8CE', line_w=1.3),
           R(key + '/eye', cx - 6, cy - 23, 12, 12, prst='ellipse', fill='2B2640', line=None),
           arc(key + '/bump', cx, cy, r - 5, 205, 335, color='AEB3CB', w=3.6),
           R(key + '/led', cx - 10, cy + 24, 20, 4.4, prst='roundRect', fill=PURPLE2, line=None)]
    for i, (dx, dy, sr) in enumerate([(-106, 30, 8), (-76, 78, 5.5), (-128, 72, 5)]):
        out += star4_icon('%s/sk%d' % (key, i), cx + dx, cy + dy, r=sr, color=PURPLE2)
    out += voice(key + '/vo', cx + r - 2, cy - r + 2)
    return out


# ------------------------------------------------------------------ 자리 3의 장면: TV, 안경, 차
def sc_tv(key, ox, oy, photo=None, say=None):
    """Samsung TV: 화면에 찾은 사진. say = 가족이 건넨 한마디(TV 아래의 말풍선)."""
    w, h = 230, 129
    x, y = ox + 140 - w / 2, oy + 36
    out = [glow(key + '/gl', ox + 140, y + h * 0.5, 140), floor(key + '/fl', ox + 140, y + h + 17, 160),
           R(key + '/neck', ox + 140 - 3, y + h, 6, 10, fill='3A3650', line=None),
           R(key + '/foot', ox + 140 - 40, y + h + 9, 80, 4.5, prst='roundRect', fill='3A3650', line=None),
           R(key + '/bezel', x - 3, y - 3, w + 6, h + 6, prst='roundRect', radius=6, fill='17151F', line=None, shadow=(18, 7, '2B1F7A', 22))]
    if photo:
        out.append(P(key + '/pic', str(photo), x, y, w, h, radius=3, crop=crop_fit(str(photo), w, h, (0.5, 0.5))))
    else:
        out.append(R(key + '/scr', x, y, w, h, prst='roundRect', radius=3, fill=None, grad=DARK, line=None))
    if say:
        pt = 11
        bw = tw(say, pt, 'm') + 50
        bx, by = ox + 140 - bw / 2, y + h + 27
        out += [R(key + '/bb', bx, by, bw, 30, prst='roundRect', fill='F3F1F7', line=None)]
        out += voice(key + '/vo', bx + 13, by + 15, color='8E88A0', n=4, h=14)
        out.append(T(key + '/bt', bx + 40, by, bw - 44, 30, say, size=pt, color=BODY, weight='m', anchor='ctr'))
    return out


def sc_glasses(key, ox, oy):
    """안경 너머로 보이는 서가. 한 권에만 Weave의 고리."""
    lw, lh, gap = 106, 86, 22
    y = oy + 86
    xl = ox + 140 - gap / 2 - lw
    xr = ox + 140 + gap / 2
    frame = '2B2640'
    out = [glow(key + '/gl', ox + 140, y + lh / 2, 140)]
    spines = [('D8D2EE', 16, 54), ('C9D6F2', 13, 62), ('EBD9E6', 18, 50), ('D2E3E0', 14, 58), ('E6DCC9', 17, 54), ('D8D2EE', 13, 64), ('C9D6F2', 16, 52)]
    for side, lx in (('l', xl), ('r', xr)):
        out.append(R('%s/%s/glass' % (key, side), lx, y, lw, lh, prst='roundRect', radius=26, fill='FFFFFF', alpha=92, line=None))
        bx, base = lx + 13, y + lh - 15
        for j, (col, bw_, bh_) in enumerate(spines[:5] if side == 'l' else spines[2:]):
            if side == 'r' and j == 2:              # 이 책: 앞표지가 보이게, 보라 고리
                out += [R('%s/r/ring' % key, bx - 4, base - 64, 42, 68, prst='roundRect', radius=7, fill='F1ECFF', line=PURPLE2, line_w=2.0),
                        R('%s/r/book' % key, bx + 1, base - 59, 32, 57, prst='roundRect', radius=3, fill=None, grad=GRAD, line=None),
                        R('%s/r/bt1' % key, bx + 7, base - 49, 19, 3.2, prst='roundRect', fill='FFFFFF', alpha=90, line=None),
                        R('%s/r/bt2' % key, bx + 7, base - 42, 13, 3.2, prst='roundRect', fill='FFFFFF', alpha=60, line=None)]
                bx += 46
                continue
            if bx + bw_ > lx + lw - 11:
                break
            out.append(R('%s/%s/b%d' % (key, side, j), bx, base - bh_, bw_, bh_, prst='roundRect', radius=2, fill=col, line=None))
            bx += bw_ + 3
        out.append(line('%s/%s/shelf' % (key, side), (lx + 9, base + 1.5), (lx + lw - 9, base + 1.5), color='B9B2C9', w=2.2))
        out.append(R('%s/%s/rim' % (key, side), lx, y, lw, lh, prst='roundRect', radius=26, fill=None, line=frame, line_w=5))
    out += [C(key + '/bridge', [(xl + lw - 2, y + 28), (xl + lw + 6, y + 16), (xr - 6, y + 16), (xr + 2, y + 28)], color=frame, w=5),
            line(key + '/tl', (xl + 4, y + 26), (xl - 11, y + 18), color=frame, w=5),
            line(key + '/tr', (xr + lw - 4, y + 26), (xr + lw + 11, y + 18), color=frame, w=5)]
    return out


def sc_car(key, ox, oy):
    """차량 화면: 지도 위에 가는 길과 도착할 곳. 아래에 운전대의 윗부분."""
    w, h = 240, 106
    x, y = ox + 140 - w / 2, oy + 40
    out = [glow(key + '/gl', ox + 140, y + h * 0.6, 140),
           R(key + '/dash', x - 14, y + h - 10, w + 28, 34, prst='roundRect', radius=17, fill='E9E5F6', line=None),
           R(key + '/bezel', x - 3, y - 3, w + 6, h + 6, prst='roundRect', radius=15, fill='17151F', line=None, shadow=(18, 7, '2B1F7A', 20)),
           R(key + '/map', x, y, w, h, prst='roundRect', radius=12, fill='262338', line=None)]
    road = '48436A'
    out += [line(key + '/r1', (x + 14, y + 32), (x + w - 14, y + 24), color=road, w=5),
            line(key + '/r2', (x + 32, y + h - 12), (x + 100, y + 10), color=road, w=5),
            line(key + '/r3', (x + 124, y + h - 8), (x + w - 20, y + 68), color=road, w=5),
            C(key + '/route', [(x + 36, y + h - 18), (x + 74, y + 44), (x + 124, y + 86), (x + w - 46, y + 40)], w=4.4, stops=[(0, 'B597FF', None), (100, '7C5CFF', None)]),
            R(key + '/me', x + 29, y + h - 25, 13, 13, prst='ellipse', fill='FFFFFF', line=PURPLE2, line_w=3),
            R(key + '/pin', x + w - 56, y + 22, 20, 20, prst='ellipse', fill=None, grad=GRAD, line='FFFFFF', line_w=2),
            R(key + '/pind', x + w - 49.5, y + 28.5, 7, 7, prst='ellipse', fill='FFFFFF', line=None)]
    wy = y + h + 128
    out += [arc(key + '/wheel', ox + 140, wy, 96, 222, 318, color='3A3650', w=11),
            arc(key + '/wheel2', ox + 140, wy, 96, 224, 316, color='625D82', w=3.2)]
    return out


# ------------------------------------------------------------------ 자리 1의 카드: 서툰 손그림과 손글씨 → 찾은 사진
NOTE_BOX = (248, 196)                       # 손그림과 손글씨가 들어가는 칸
PHOTO_BOX = (248, 124)                      # 찾은 사진이 들어가는 칸


def s_pen(key, x, y, k=1.0):
    """S펜 한 자루(몸통, 옆 단추, 펜촉)를 곧게 세워 그린다. (x, y) = 펜의 가운데. 기울기는 장에 넣을 때(rot)."""
    w, h = 7.5 * k, 84 * k
    bx, by = x - w / 2, y - h / 2 - 5 * k
    return [R(key + '/body', bx, by, w, h, prst='roundRect', radius=3.6 * k, fill=None, grad=dict(stops=[(0, '4A4563', None), (100, '2B2640', None)], ang=0), line=None,
              shadow=(8, 3, '2B1F7A', 22)),
            R(key + '/btn', bx + w - 2.4 * k, by + h * 0.50, 1.7 * k, 13 * k, prst='roundRect', fill='8E88A0', line=None),
            R(key + '/nib', x - 2.8 * k, by + h - 0.5, 5.6 * k, 10 * k, prst='flowChartMerge', fill='6A6474', line=None)]


def pen_card(s, key, x, w, note, photo, meta, pen=(0.80, 0.86, 58)):
    """손그림과 손글씨(note) → Weave가 찾은 사진(photo)과 한 줄(meta = (앱 아이콘 키, 글)).
    pen = S펜의 가운데(그림 폭과 높이에 대한 비율)와 기울기(도). 돌려줌: 뜨는 차례대로의 키."""
    from PIL import Image
    ox = x + (w - CW0) / 2
    nw, nh = Image.open(AS / note).size
    k = min(NOTE_BOX[0] / nw, NOTE_BOX[1] / nh)
    dw, dh = nw * k, nh * k
    nx, ny = ox + 16 + (NOTE_BOX[0] - dw) / 2, CY + 14 + (NOTE_BOX[1] - dh) / 2
    s.add(key + '/note', [P(key + '/note', str(AS / note), nx, ny, dw, dh)])
    fx, fy, ang = pen
    s.add(key + '/pen', s_pen(key + '/pen', nx + dw * fx, ny + dh * fy), rot=ang)
    px, py = ox + 16, CY + 14 + NOTE_BOX[1] + 8
    pw, ph = PHOTO_BOX
    s.add(key + '/photo', [R(key + '/pglow', px - 3, py - 3, pw + 6, ph + 6, prst='roundRect', radius=15, fill='FFFFFF', line=PURPLE2, line_w=2.2, shadow=(14, 4, '6B4EFF', 22)),
                           P(key + '/pic', str(AS / photo), px, py, pw, ph, radius=12, crop=crop_fit(str(AS / photo), pw, ph, (0.5, 0.5)))])
    app, text = meta
    my = py + ph + 11
    s.add(key + '/meta', spark_icon(key + '/msp', px + 2, my + 1, size=17) + [
        P(key + '/mi', ICON.get(app, app), px + 25, my + 1, 17, 17),
        T(key + '/mt', px + 48, my - 1, pw - 50, 21, text, size=10.5, color=INK2, weight='m', anchor='ctr')])
    return [key + '/note', key + '/pen', key + '/photo', key + '/meta']


def scene_card(s, key, x, w, scene, rep):
    """장면 그림 + 건네는 말. scene = (그리는 함수, {더 넘길 값}), rep = (아이콘, 첫 줄, 둘째 줄, (기록 앱, 이름, 글))."""
    ox = x + (w - CW0) / 2
    fn, kw = scene
    s.add(key + '/scene', fn(key + '/scene', ox, CY, **kw))
    icon, l1, l2, src = rep
    s.add(key + '/reply', reply(key, x, w, icon, l1, l2, src))
    return [key + '/scene', key + '/reply']


BIXBY, STHINGS = AS / 'app-bixby.png', AS / 'app-smartthings.png'
PEN_SAY = 'S펜으로 서툴게 그리고 몇 글자만 적어도, 그림과 글씨를 함께 읽어 그날의 사진을 찾아 줍니다.'
PEN_SUB = [(None, 'S펜'), (None, '멀티모달 임베딩')]
HOME_SUB = [(STHINGS, 'SmartThings'), (BIXBY, 'Bixby')]
# 자리마다의 후보: 코드 → 이름, 한 줄, 종류, 내용, 말할 문장
CARDS = {
    # ---- 자리 1: 그려서 찾는 기억 (손글씨: '바다에 빨간 거 있었는데 / 엄마랑 노을 본 날', '바다에 바람개비..? / 노을 예뻤던 데', '언덕에 나무 하나 달랑 / 해 질 때였는데')
    '1가': dict(name='그려서 찾는 기억', sub=PEN_SUB, kind='pen', note='note-light.png', photo='photo-light.jpg',
               meta=('gallery', '2025년 10월 4일 · 엄마와 강릉'), pen=(0.80, 0.90, 60), say=PEN_SAY),
    '1나': dict(name='그려서 찾는 기억', sub=PEN_SUB, kind='pen', note='note-wind.png', photo='photo-wind.jpg',
               meta=('gallery', '2024년 10월 5일 · 제주'), pen=(0.78, 0.90, 60), say=PEN_SAY),
    '1다': dict(name='그려서 찾는 기억', sub=PEN_SUB, kind='pen', note='note-tree.png', photo='photo-tree.jpg',
               meta=('gallery', '2025년 11월 2일 · 서울'), pen=(0.86, 0.90, 62), say=PEN_SAY),
    # ---- 자리 2: 집에서 건네는 기억 (SmartThings로 이어진 가전, Bixby의 목소리). 먼저 건네는 기억(UX 3)의 다음
    '2가': dict(name='집에서 건네는 기억', sub=HOME_SUB, kind='scene', scene=(sc_fridge, {}),
               rep=(BIXBY, '지은님은 새우를 못 드세요', '오늘 저녁 메뉴에서 뺄까요?', ('talk', '지은', '‘나 갑각류 알레르기 있어’ 9월 12일')),
               say='집에서는 SmartThings로 이어진 냉장고가, 잊고 있던 친구의 알레르기를 Bixby의 목소리로 먼저 알려 줍니다.'),
    '2나': dict(name='집에서 건네는 기억', sub=HOME_SUB, kind='scene', scene=(sc_washer, {}),
               rep=(BIXBY, '이 니트는 건조하면 줄어요', '울 코스로 바꿀까요?', ('gallery', '캡처', '‘울 혼방, 건조기 사용 주의’ 10월 20일')),
               say='집에서는 SmartThings로 이어진 세탁건조기가, 캡처해 두고 잊은 세탁 주의 사항을 Bixby의 목소리로 먼저 알려 줍니다.'),
    '2다': dict(name='집에서 건네는 기억', sub=HOME_SUB, kind='scene', scene=(sc_robot, {}),
               rep=(BIXBY, '부모님이 3시에 오세요', '미리 청소를 시작할까요?', ('talk', '엄마', '‘토요일 3시쯤 갈게’ 11월 11일')),
               say='집에서는 SmartThings로 이어진 로봇청소기가, 잊고 있던 부모님의 방문을 Bixby의 목소리로 먼저 알려 줍니다.'),
    # ---- 자리 3: 상상
    '3가': dict(name='거실에서 함께 보는 기억', sub=[(None, 'Samsung TV')], kind='scene',
               scene=(sc_tv, dict(photo=AS / 'photo-family.jpg', say='비 오던 날 갔던 온천 어디였지?')),
               rep=(BIXBY, '2023년 가을, 유후인이에요', '그날의 사진을 보여 드릴게요', ('talk', '엄마', '‘비 와서 온천만 했네’')),
               say='거실에서는 가족의 어렴풋한 한마디만으로, TV가 그날의 사진을 큰 화면에 펼쳐 줍니다.'),
    '3나': dict(name='보는 순간 떠오르는 기억', sub=[(None, 'AI 글라스')], kind='scene', scene=(sc_glasses, {}),
               rep=('spool', '작년 여름에 읽은 책이에요', '민수님께 선물도 했어요', ('note', '독서 메모', '‘완독’ 2025년 8월')),
               say='언젠가는 안경 너머로 바라보는 것만으로, 그 물건에 얽힌 지난 기록이 떠오를 것입니다.'),
    '3다': dict(name='가는 길을 이어 주는 기억', sub=[(None, '차량 화면')], kind='scene', scene=(sc_car, {}),
               rep=('spool', '양평 두물머리로 안내할까요?', '주중에 이야기한 곳이에요', ('talk', '아내', '‘이번 주말엔 여기 가 보자’')),
               say='차에 오르면, 주중에 대화방에서 이야기한 곳으로 가는 길을 먼저 이어 줍니다.'),
}
OPEN = '그리고 Weave는 휴대폰에서 멈추지 않습니다.'
CLOSE = '휴대폰에서 시작한 Weave를, 갤럭시의 모든 기기로 넓혀 가겠습니다.'


def next_note(picks):
    return OPEN + ''.join(' (클릭) ' + CARDS[c]['say'] for c in picks) + ' ' + CLOSE


def s_next(picks=('1가', '2가', '3가'), key='nx'):
    """35쪽 다음 장. 넘기면 연표가 왼쪽으로 옮겨 가고 실이 오른쪽으로 이어진다 → (클릭마다) 카드 하나."""
    s = Slide(key, trans=('morph', 1100), bar=False, notes=next_note(picks))
    tl_parts(s, dx=-PAN, ghost=True, title=False)
    s.add('nx/title', [N.title('nx/title', TITLE)])
    n = len(picks)
    boxes = [card_box(n, i) for i in range(n)]
    # 실: Weave에서 오른쪽 끝까지. 카드 뒤로 지나가 카드 사이에서만 보인다
    s.add('nx/th', [C('nx/th', [(WX + 30, YC)] * 2 + [(X1 + 14, YC)] * 2, w=3, color=PURPLE)])
    s.add('nx/end', star4_icon('nx/end', X1 + 28, YC, r=9, color=PURPLE))
    groups = []
    for i, (code, (x, w)) in enumerate(zip(picks, boxes)):
        c = CARDS[code]
        k = 'nx/c%d' % (i + 1)
        s.add(k + '/head', card_head(k, x, w, c['name'], c['sub']))
        s.add(k + '/bg', card_frame(k, x, w))
        if c['kind'] == 'pen':
            parts = pen_card(s, k, x, w, c['note'], c['photo'], c['meta'], c['pen'])
        else:
            parts = scene_card(s, k, x, w, c['scene'], c['rep'])
        groups.append((k, c['kind'], parts))
    # 장이 열리면(연표가 다 옮겨 간 뒤): 실이 오른쪽으로 뻗음
    s.on('nx/title', 'fade_in', 0, 400)
    s.on('nx/th', 'wipe_in', 100, 700, dir='left')
    s.on('nx/end', 'zoom_in', 760, 300, **{'from': 0.4})
    for k, kind, parts in groups:
        s.click()
        s.on([k + '/bg', k + '/head'], 'rise', 0, 420, dy=12)
        if kind == 'pen':
            note, pen, photo, meta = parts
            s.on(pen, 'fade_in', 200, 280)
            s.on(note, 'wipe_in', 300, 1000, dir='left')
            s.on(photo, 'rise', 1400, 460, dy=10)
            s.on(meta, 'fade_in', 1650, 360)
        else:
            scene, rep = parts
            s.on(scene, 'fade_in', 220, 420)
            s.on(rep, 'rise', 620, 460, dy=10)
    return s


# ------------------------------------------------------------------ 후보 묶음 (tools/next_try.py)
FUT = HERE / '미래장표_후보'
SETS = [    # (코드, 자리마다 고른 카드, 한 줄 이름)
    ('미래A', ('1가', '2가', '3가'), 'S펜, 냉장고, TV'),
    ('미래B', ('1나', '2나', '3나'), 'S펜, 세탁건조기, AI 글라스'),
    ('미래C', ('1다', '2다', '3다'), 'S펜, 로봇청소기, 차량'),
    ('미래D', ('1가', '2가'), '두 장만: S펜, 냉장고'),
]


def _set(picks, key):
    def fn(deck=False):
        """영상: 35쪽의 마지막 구간부터. 덱: 35쪽(지금 덱의 장 그대로) 다음에."""
        return [N.s_tl() if deck else s_tl_end(), s_next(picks, key)]
    return fn


CANDIDATES = [(code, _set(picks, 'nx' + code[-1].lower()), label, FUT) for code, picks, label in SETS]
DECKS = [('미래', '미래장표_후보', '미래장표_후보.pptx'), ('임팩트', '비즈니스임팩트_후보', '비즈니스임팩트_후보.pptx')]
