"""9차 후보 2판(11-14 밤): '앞으로의 Weave'를 두 장으로. 1판(next_new.py: 카드 셋이 한 줄의 실에 꿰임)을 보고 받은 검토대로 다시 그림.
  '다른 기기에 집중하는 것 같고 미래, 모든 것을 잇겠다는 포부가 잘 안 느껴짐. 27년 이후가 쭉쭉 드러나게. 선 하나에 그림만 있어 시각화가 부족.
   그림(S펜)과 알레르기(냉장고) 둘만 위아래로(하나는 기술, 하나는 기기 간 연결).'
  이어서: '왼쪽에는 2026년부터만 남기고, 연표의 양식(위는 기술, 아래는 인프라. 해, 그 아래 이름, 그 아래 한 줄)에 맞춰 2027- / 그려서 찾는 기억 / 집에서 건네는 기억.
   전체를 감싸는 흰 상자는 쓰지 말고(떠 있는 조각에는 써도 됨), 사진 시나리오에는 갤러리와 캘린더처럼 기록 두세 개가 이어지게.'

(가) 35쪽에서 넘기면(Morph) 연표가 2026년 마디와 Weave만 남기고 왼쪽으로 옮겨 간다. Weave에서 두 줄이 다시 갈라져 오른쪽 끝까지 뻗는다.
     클릭마다 한 줄씩, 35쪽의 마디와 같은 양식으로 마디가 뜨고 그 오른쪽에 장면이 떠 있는 조각으로 놓인다:
     위(기술) 2027- 그려서 찾는 기억: S펜 메모 → Weave → 갤러리 사진과 그 사진에 이어진 캘린더, 카카오톡 기록
     아래(갤럭시) 2027- 집에서 건네는 기억: 휴대폰 → SmartThings → 냉장고 → Bixby의 말과 그 말이 나온 기록
(나) 한 번 더 넘기면 모두 왼쪽으로 물러나고, 두 줄이 서로 엮이며 오른쪽으로 뻗는다. 위에는 기록(앱), 아래에는 기기가 실에 꿰이고 아래에 해의 눈금.

좌표는 1280×720 px. 그림은 assets/next/ (tools/next_assets.py).
"""
from pathlib import Path

import build as HW
from ui import (BODY, ICON, INK, INK2, LINE, MUTE, PURPLE, PURPLE2, SUB, SHADOW_CARD,
                C, P, R, T, Xf, crop_fit, line, tw)

import next_new as NX
import slides_new as N

Slide = HW.Slide
HERE = Path(__file__).resolve().parent
AS = NX.AS
GRAD = NX.GRAD

# ------------------------------------------------------------------ 자리
PAN = 880                                   # 연표가 왼쪽으로 옮겨 가는 만큼(px): 2026년 마디가 x 102에 남음. Weave 마디는 x 1140 → 260
KEEP = 982                                  # 35쪽에서 이 자리(2026년 마디)부터 오른쪽만 남고 그 왼쪽 마디는 옮겨 가며 사라짐
WX, YC, YU, YL = N.TL_WX - PAN, N.TL_YC, N.TL_YU, N.TL_YL
FX0, FXS, FX1 = WX + 30, WX + 106, 1266     # 미래의 줄: Weave에서 갈라지기 시작, 곧게 뻗기 시작, 오른쪽 끝(화살촉)
NDX = 440                                   # 2027- 마디의 x(위 줄, 아래 줄 같은 자리)
ZX = 534                                    # 장면 조각이 놓이기 시작하는 x(마디 글의 오른쪽)
GONE = 1320                                 # (나)로 넘어갈 때 (가)의 모든 것이 더 옮겨 가는 만큼
TITLE_A = [('2027년부터, ', INK), ('더 넓게 읽고 더 멀리 잇습니다', PURPLE)]
TITLE_B = [('기록에서 기기까지, ', INK), ('모든 것을 잇는 Weave', PURPLE)]
YEAR = '2027-'

OPEN = '그리고 Weave의 연표는 2027년에도 이어집니다.'
SAY_PEN = ('기술은 글을 넘어 그림까지 읽습니다. '
           'S펜으로 서툴게 그리고 몇 글자만 적어도, 갤러리와 캘린더에 흩어진 그날의 기록을 이어 찾아 줍니다.')
SAY_HOME = ('갤럭시는 휴대폰을 넘어 집 안의 기기까지 닿습니다. '
            'SmartThings로 연결된 냉장고가, 잊고 있던 친구의 알레르기를 Bixby의 목소리로 먼저 알려 줍니다.')
CLOSE = '기록에서 기기까지, 흩어진 모든 것을 Weave로 잇겠습니다.'
NOTE_A = '%s (클릭) %s (클릭) %s' % (OPEN, SAY_PEN, SAY_HOME)
SUPS = '¹²³⁴⁵⁶⁷⁸'
SHADOW_FLOAT = (20, 6, '6B4EFF', 13)        # 떠 있는 조각의 그림자


# ------------------------------------------------------------------ 지난 연표(35쪽의 부품. 키가 같아 Morph로 이어짐)
def tl_past(s, dx, gone=False):
    """35쪽 연표를 dx만큼 옮겨 그린다. KEEP보다 왼쪽 마디와 줄 이름은 투명하게(옮겨 가며 사라짐), 남는 마디의 근거 글은 각주 번호 없이.
    gone이면 Weave까지 모두 투명하게((나) 장: 화면 밖으로 물러남)."""
    xf = Xf(0, 0, dx, 0, 1.0)
    s.add('tl/lu', [C('tl/lu', [(N.TL_X0, YU)] * 2 + [(N.TL_X1, YU)] * 2, stops=N.TL_STOPS, w=3)], xf=xf)
    s.add('tl/ll', [C('tl/ll', [(N.TL_X0, YL)] * 2 + [(N.TL_X1, YL)] * 2, stops=N.TL_STOPS, w=3)], xf=xf)
    ex = N.TL_WX - 30
    s.add('tl/ju', [C('tl/ju', [(N.TL_X1, YU), (N.TL_X1 + 44, YU), (ex - 44, YC), (ex, YC)], w=3, color=PURPLE)], xf=xf)
    s.add('tl/jl', [C('tl/jl', [(N.TL_X1, YL), (N.TL_X1 + 44, YL), (ex - 44, YC), (ex, YC)], w=3, color=PURPLE)], xf=xf)
    s.add('tl/now', N.tl_label('tl/now', YU, 'WHY NOW', '지금이라서'), xf=xf, alpha=0)
    s.add('tl/sam', N.tl_label('tl/sam', YL, 'WHY SAMSUNG', '갤럭시라서'), xf=xf, alpha=0)
    for up, rows, y in ((True, N.TL_UP, YU), (False, N.TL_DN, YL)):
        for x, year, word, ref, icon in rows:
            k = 'tl/%s%d' % ('u' if up else 'd', x)
            a = 0 if (gone or x < KEEP) else 100
            s.add(k, N.tl_node(k, x, y, up, year, word, ref.rstrip(SUPS), icon), xf=xf, alpha=a)
    wx = N.TL_WX
    a = 0 if gone else 100
    s.add('tl/wglow', [R('tl/wglow', wx - 56, YC - 56, 112, 112, prst='ellipse', fill=None, line=None,
                         grad=dict(stops=[(0, '8B6BFF', 46), (60, 'B9A6FF', 16), (100, 'F2EDFF', 0)], path='circle'))], xf=xf, alpha=a)
    s.add('tl/w', [R('tl/w/c', wx - 30, YC - 30, 60, 60, prst='ellipse', line='FFFFFF', line_w=2.5, shadow=(18, 6, '6B4EFF', 30),
                     grad=dict(stops=[(0, '8D6BFF', None), (100, '5A3FE0', None)], ang=55)),
                   P('tl/w/sp', ICON['spool_w'], wx - 17, YC - 17, 34, 34),
                   T('tl/w/n', wx - 70, YC + 38, 140, 28, 'Weave', size=17, color=PURPLE, weight='b', align='c', anchor='ctr')], xf=xf, alpha=a)


# ------------------------------------------------------------------ (가)의 부품
def lane(key, y):
    """Weave에서 갈라져 오른쪽 끝까지 뻗는 줄. 아래에 옅은 빛을 받침."""
    pts = [(FX0, YC), (FX0 + 44, YC), (FXS - 44, y), (FXS, y), (FXS + 220, y), (FX1 - 220, y), (FX1, y)]
    return [C(key + '/glow', pts, w=11, color='B9A6FF', alpha=30),
            C(key + '/line', pts, w=3.4, stops=[(0, '6B4EFF', None), (100, 'A48BFF', None)], tail='triangle')]


def comet(key, y):
    """줄을 따라 달려 나가는 작은 빛(잠깐만 보임). 놓인 자리는 곧은 구간의 시작."""
    return [R(key, FXS - 5.5, y - 5.5, 11, 11, prst='ellipse', fill='FFFFFF', line=PURPLE, line_w=2.6, glow=(9, PURPLE2, 70))]


def run(s, key, t, dur=900, first=False):
    """빛이 줄의 끝까지 달려 나가고 사라진다. 빛은 화면 밖에 두었다가(temp) 처음 달릴 때 제자리로 옮긴다(정적 보기에는 안 보임)."""
    s.on(key, 'jump' if first else 'fade_in', t, 110)
    s.on(key, 'move', t, dur, dx=FX1 - FXS - 34, dy=0, accel=15000, decel=85000)
    s.on(key, 'fade_out', t + dur - 160, 200)


def fnode(key, x, y, up, year, word, ref, icon):
    """35쪽의 마디(slides_new.tl_node)와 같은 양식: 점, 해, 이름, 한 줄, 아이콘. 위 줄은 글이 줄 위에, 아래 줄은 줄 아래에."""
    ys = (y - 96, y - 68, y - 44, y - 138) if up else (y + 22, y + 50, y + 74, y + 104)
    return [R(key + '/dot', x - 8, y - 8, 16, 16, prst='ellipse', fill='FFFFFF', line=PURPLE, line_w=3),
            T(key + '/y', x - 60, ys[0], 120, 26, year, size=15, color=PURPLE, weight='b', align='c', anchor='ctr'),
            T(key + '/w', x - 100, ys[1], 200, 24, word, size=14.5, color=INK, weight='b', align='c', anchor='ctr'),
            T(key + '/r', x - 100, ys[2], 200, 20, ref, size=10.5, color=MUTE, align='c', anchor='ctr'),
            P(key + '/ic', str(icon), x - 17, ys[3], 34, 34)]


def tile(key, cx, cy, icon=None, z=28):
    """실 가운데의 작은 네모: Weave(보라 바탕에 흰 실타래) 또는 앱 아이콘."""
    if icon:
        return [R(key + '/w', cx - z / 2 - 3, cy - z / 2 - 3, z + 6, z + 6, prst='ellipse', fill='FFFFFF', line=None),
                P(key + '/i', str(icon), cx - z / 2, cy - z / 2, z, z)]
    return [R(key + '/t', cx - z / 2, cy - z / 2, z, z, prst='roundRect', radius=z * 0.3, line='FFFFFF', line_w=2, grad=GRAD, shadow=(10, 3, '6B4EFF', 30)),
            P(key + '/s', ICON['spool_w'], cx - z * 0.31, cy - z * 0.31, z * 0.62, z * 0.62)]


def chip_w(tag, text, pt=10.5):
    return 37 + tw(tag, 10.5, 'b') + 16 + 7 + tw(text, pt) + 13


def chip(key, kind, tag, text, x, y, pt=10.5):
    """기록 조각(인트로 11~13쪽과 같은 알약: 앱 아이콘, 보라 꼬리표, 한 줄). 여기서는 흰 바탕을 불투명하게."""
    out = N.rc_card(key, kind, tag, text, pt, chip_w(tag, text, pt), x, y)
    out[0] = R(key + '/bg', x, y, chip_w(tag, text, pt), 34, prst='roundRect', fill='FFFFFF', line='E4DDF7', line_w=1.0, shadow=(14, 4, '6B5CB0', 12))
    return out


def fridge(key, cx, top, h):
    """Bespoke AI 패밀리허브: 문 넷, 오른쪽 위 문에 화면."""
    k = h / 204
    w = 122 * k
    x = cx - w / 2
    split = top + h * 0.6
    sw, sh = 40 * k, 74 * k
    sx, sy = cx + 12.5 * k, top + 19 * k
    return [NX.floor(key + '/fl', cx, top + h + 3, w * 1.4),
            R(key + '/body', x, top, w, h, prst='roundRect', radius=9 * k, fill=None, grad=NX.METAL, line=NX.EDGE, line_w=1.3, shadow=(16, 6, '5B3FE6', 13)),
            line(key + '/sv', (cx, top + 3), (cx, top + h - 3), color=NX.EDGE, w=1.3),
            line(key + '/sh', (x + 3, split), (x + w - 3, split), color=NX.EDGE, w=1.3),
            R(key + '/h1', cx - 7 * k, top + h * 0.30, 2.4, 30 * k, prst='roundRect', fill='A9AEC6', line=None),
            R(key + '/h2', cx + 4.4 * k, top + h * 0.30, 2.4, 30 * k, prst='roundRect', fill='A9AEC6', line=None),
            R(key + '/h3', cx - 34 * k, split + 9 * k, 25 * k, 2.4, prst='roundRect', fill='A9AEC6', line=None),
            R(key + '/h4', cx + 9 * k, split + 9 * k, 25 * k, 2.4, prst='roundRect', fill='A9AEC6', line=None),
            R(key + '/scr', sx, sy, sw, sh, prst='roundRect', radius=4.5 * k, fill=None, grad=NX.DARK, line=None),
            R(key + '/s1', sx + 6 * k, sy + 9 * k, sw - 12 * k, 3.2 * k, prst='roundRect', fill='FFFFFF', alpha=88, line=None),
            R(key + '/s2', sx + 6 * k, sy + 17 * k, (sw - 12 * k) * 0.6, 3.2 * k, prst='roundRect', fill='FFFFFF', alpha=50, line=None),
            R(key + '/s3', sx + 6 * k, sy + sh - 21 * k, sw - 12 * k, 13 * k, prst='roundRect', radius=4 * k, fill=PURPLE2, line=None)]


def mini_phone(key, x, y, w=46, h=88):
    """기록이 들어 있는 휴대폰(작게): 흰 화면 가운데에 Weave."""
    cx = x + w / 2
    return [R(key + '/frame', x, y, w, h, prst='roundRect', radius=11, line='FFFFFF', line_w=1.0, shadow=(12, 4, '5B3FE6', 18),
              grad=dict(stops=[(0, 'D5D8EC', None), (100, 'B7BBD8', None)], ang=60)),
            R(key + '/screen', x + 3, y + 3, w - 6, h - 6, prst='roundRect', radius=8.5, fill='FFFFFF', line=None),
            R(key + '/cam', cx - 2, y + 7.5, 4, 4, prst='ellipse', fill='23212B', line=None),
            R(key + '/wv', cx - 12, y + h / 2 - 12, 24, 24, prst='ellipse', line=None, grad=GRAD),
            P(key + '/sp', ICON['spool_w'], cx - 7, y + h / 2 - 7, 14, 14)]


def bubble(key, x, y, w, icon, l1, l2):
    """떠 있는 말 조각: 아이콘과 두 줄."""
    h, isz = 74, 30
    tx = x + 15 + isz + 12
    return [R(key + '/bg', x, y, w, h, prst='roundRect', radius=20, fill='FFFFFF', line='E4DDF7', line_w=1.0, shadow=SHADOW_FLOAT),
            P(key + '/i', str(icon), x + 15, y + (h - isz) / 2, isz, isz),
            T(key + '/1', tx, y + 12, w - (tx - x) - 10, 26, l1, size=14, color=INK, weight='b', anchor='ctr'),
            T(key + '/2', tx, y + 38, w - (tx - x) - 10, 23, l2, size=12.5, color=BODY, anchor='ctr')]


PEN = dict(note='note-light.png', photo='photo-light.jpg', date='2025년 10월 4일', at=(0.80, 0.90, 60),
           links=[('cal', '10월 4일', '강릉 여행'), ('talk', '엄마', '바다 또 가자')])
HOME = dict(l1='지은님은 새우를 못 드세요', l2='오늘 저녁 메뉴에서 뺄까요?', src=('talk', '지은', '나 갑각류 알레르기 있어'))
PEN_SUB, HOME_SUB = 'S펜 · 멀티모달 임베딩', 'SmartThings · Bixby'


def parts_a(s, dx=0, alpha=100, pen=PEN, home=HOME):
    """(가)의 모든 부품을 넣는다. dx, alpha: (나) 장에서는 화면 밖으로 옮겨 투명하게. 돌려줌: 효과를 걸 값."""
    from PIL import Image
    xf = Xf(0, 0, dx, 0, 1.0)
    add = lambda key, prims, **kw: s.add(key, prims, xf=xf, alpha=alpha, **kw)
    K = {}
    add('n2/lu', lane('n2/lu', YU))
    add('n2/ll', lane('n2/ll', YL))
    # ---- 위(기술): 2027- 그려서 찾는 기억. 장면은 줄 위쪽에 왼쪽에서 오른쪽으로: 메모 → Weave → 사진과 이어진 기록
    add('n2/u/node', fnode('n2/u/node', NDX, YU, True, YEAR, '그려서 찾는 기억', PEN_SUB, AS / 'ic-pen-line.png'))
    cy = 206                                                # 위 장면의 가운데 높이
    cw = max(chip_w(tag, text) for _, tag, text in pen['links'])
    cx0 = 1240 - cw                                         # 이어진 기록 조각들의 왼쪽(오른쪽 끝을 1240에 맞춤)
    pw, ph = 200, 124                                       # 사진
    fx0 = cx0 - 14 - (pw + 16)                              # 사진 조각의 왼쪽
    nb = (ZX, cy - 86, fx0 - 44 - ZX, 172)                  # 메모 조각
    add('n2/u/nbg', [R('n2/u/nbg', *nb, prst='roundRect', radius=18, fill='FFFFFF', line='E4DDF7', line_w=1.0, shadow=SHADOW_FLOAT)])
    nw, nh = Image.open(AS / pen['note']).size
    k = min((nb[2] - 14) / nw, (nb[3] - 16) / nh)
    dw, dh = nw * k, nh * k
    nx, ny = nb[0] + (nb[2] - dw) / 2, nb[1] + (nb[3] - dh) / 2
    add('n2/u/note', [P('n2/u/note', str(AS / pen['note']), nx, ny, dw, dh)])
    fx, fy, ang = pen['at']
    px_, py_ = nx + dw * fx, ny + dh * fy
    K['pen_from'] = (nx + 12 - px_, ny + dh * 0.42 - py_)             # 그리기 시작하는 곳(그림의 왼쪽)에서 놓인 자리까지
    add('n2/u/pen', NX.s_pen('n2/u/pen', px_, py_), rot=ang, **({} if dx else dict(start=K['pen_from'])))
    tx0, tx1 = nb[0] + nb[2] + 6, fx0 - 6
    add('n2/u/th', [line('n2/u/th', (tx0, cy), (tx1, cy), color=PURPLE2, w=2.6)])
    add('n2/u/tile', tile('n2/u/tile', (tx0 + tx1) / 2, cy))
    fy0 = cy - (ph + 16 + 24) / 2
    add('n2/u/photo', [R('n2/u/pbg', fx0, fy0, pw + 16, ph + 16 + 24, prst='roundRect', radius=16, fill='FFFFFF', line=PURPLE2, line_w=2.0, shadow=SHADOW_FLOAT),
                       P('n2/u/pic', str(AS / pen['photo']), fx0 + 8, fy0 + 8, pw, ph, radius=10, crop=crop_fit(str(AS / pen['photo']), pw, ph, (0.5, 0.5))),
                       P('n2/u/pi', ICON['gallery'], fx0 + 10, fy0 + ph + 13, 17, 17),
                       T('n2/u/pt', fx0 + 33, fy0 + ph + 11, pw - 30, 21, pen['date'], size=10.5, color=INK2, weight='m', anchor='ctr')])
    K['links'] = []
    for i, (kind, tag, text) in enumerate(pen['links']):               # 사진에 이어진 기록(캘린더, 카카오톡)
        ky = cy - 42 + i * 50
        key = 'n2/u/l%d' % i
        add(key + '/th', [C(key + '/th', [(fx0 + pw + 16, cy), (fx0 + pw + 26, cy), (cx0 - 12, ky + 17), (cx0, ky + 17)], color=PURPLE2, w=2.2)])
        add(key, chip(key, kind, tag, text, cx0, ky))
        K['links'].append(key)
    # ---- 아래(갤럭시): 2027- 집에서 건네는 기억. 휴대폰 → SmartThings → 냉장고 → Bixby의 말, 그 아래에 그 말이 나온 기록
    add('n2/l/node', fnode('n2/l/node', NDX, YL, False, YEAR, '집에서 건네는 기억', HOME_SUB, AS / 'ic-house.png'))
    cy = 566
    x = ZX + 26
    add('n2/l/phone', mini_phone('n2/l/phone', x, cy - 44))
    add('n2/l/th', [line('n2/l/th', (x + 46 + 6, cy), (x + 46 + 64, cy), color=PURPLE2, w=2.6, dash='dash')])
    add('n2/l/tile', tile('n2/l/tile', x + 46 + 35, cy, NX.STHINGS, z=28))
    fcx = x + 46 + 70 + 50
    add('n2/l/fridge', fridge('n2/l/fridge', fcx, cy - 84, 166))
    add('n2/l/voice', NX.voice('n2/l/voice', fcx + 60, cy - 84 + 166 * 0.27, n=5, h=20))
    bx = fcx + 108
    add('n2/l/say', bubble('n2/l/say', bx, cy - 56, 344, NX.BIXBY, home['l1'], home['l2']))
    kind, tag, text = home['src']
    add('n2/l/src/th', [line('n2/l/src/th', (bx + 34, cy + 18), (bx + 34, cy + 34), color=PURPLE2, w=2.2)])
    add('n2/l/src', chip('n2/l/src', kind, tag, text, bx + 14, cy + 34))
    return K


def s_next2a(key='n2a'):
    """35쪽 다음 장. 연표가 2026년 마디와 Weave만 남기고 옮겨 가고, 두 줄이 다시 뻗는다 → (클릭) 그려서 찾는 기억 → (클릭) 집에서 건네는 기억."""
    s = Slide(key, trans=('morph', 1100), bar=False, notes=NOTE_A)
    tl_past(s, -PAN)
    s.add('n2/title', [N.title('n2/title', TITLE_A)])
    K = parts_a(s)
    s.add('n2/cu', comet('n2/cu', YU), temp=True)
    s.add('n2/cl', comet('n2/cl', YL), temp=True)
    # 장이 열리면(연표가 다 옮겨 간 뒤): 두 줄이 오른쪽 끝까지 뻗고 빛이 달려 나감
    s.on('n2/title', 'fade_in', 0, 400)
    s.on(['n2/lu', 'n2/ll'], 'wipe_in', 80, 900, dir='left')
    run(s, 'n2/cu', 260, first=True)
    run(s, 'n2/cl', 260, first=True)
    s.click()      # 1: 위 줄(기술) — 마디 → 메모가 그려지고 → Weave가 읽어 → 사진, 이어진 기록 둘
    s.on('n2/u/node', 'rise', 0, 420, dy=-12)
    run(s, 'n2/cu', 60, 800)
    s.on('n2/u/nbg', 'rise', 160, 400, dy=10)
    s.on('n2/u/pen', 'fade_in', 420, 200)
    s.on('n2/u/pen', 'goto', 420)
    s.on('n2/u/note', 'wipe_in', 560, 1100, dir='left')
    s.on('n2/u/pen', 'fly', 560, 1100, dx=K['pen_from'][0], dy=K['pen_from'][1], bend=0, show=False, fade=False)
    s.on('n2/u/th', 'wipe_in', 1720, 260, dir='left')
    s.on('n2/u/tile', 'zoom_in', 1760, 300, **{'from': 0.5})
    s.on('n2/u/photo', 'zoom_in', 2020, 440, **{'from': 0.92})
    for i, key_ in enumerate(K['links']):
        s.on(key_ + '/th', 'wipe_in', 2420 + i * 200, 240, dir='left')
        s.on(key_, 'rise', 2520 + i * 200, 380, dy=8)
    s.click()      # 2: 아래 줄(갤럭시) — 마디 → 휴대폰의 기록이 SmartThings를 따라 냉장고로 → Bixby가 먼저 말함, 그 말이 나온 기록
    s.on('n2/l/node', 'rise', 0, 420, dy=12)
    run(s, 'n2/cl', 60, 800)
    s.on('n2/l/phone', 'fade_in', 200, 320)
    s.on('n2/l/th', 'wipe_in', 480, 320, dir='left')
    s.on('n2/l/tile', 'zoom_in', 560, 300, **{'from': 0.5})
    s.on('n2/l/fridge', 'fade_in', 780, 400)
    s.on('n2/l/voice', 'fade_in', 1200, 260)
    s.on('n2/l/say', 'rise', 1300, 460, dy=10)
    s.on('n2/l/src/th', 'wipe_in', 1820, 200, dir='down')
    s.on('n2/l/src', 'rise', 1900, 380, dy=8)
    return s


# ------------------------------------------------------------------ (나): 두 줄이 엮이며 뻗는 끝 장
BX, BP, BN = 172, 150, 7                    # 첫 마루의 x, 마루 사이, 마루의 수
REC = ['talk', 'gallery', 'note', 'cal', 'mail', 'map', 'wallet']                                     # 위 줄: 기록(앱)
DEV = ['smartphone', 'watch', 'laptop', 'tv', 'refrigerator', 'washing-machine', 'car']                # 아래 줄: 기기(선 그림 assets/next/ic-*.png)
RY, DY, NR = 232, 540, 31                   # 기록 마디의 가운데 y, 기기 마디의 가운데 y, 마디 반지름
YEARS = [(0, '2027'), (2, '2028'), (4, '2029'), (6, '2030')]        # 해의 눈금: (몇째 엇갈림, 해). 마디 바로 아래가 아니라 엇갈리는 자리에 둠(해마다의 계획처럼 읽히지 않게)
RULE_Y = 628


def braid(top_first):
    """왼쪽 끝에서 들어와 마루마다 위아래를 바꾸며 오른쪽 밖까지 가는 실 한 가닥의 점들."""
    y0, y1 = (YU, YL) if top_first else (YL, YU)
    pts = [(-16, y0), (40, y0), (BX - 60, y0), (BX, y0)]
    xa, ya = BX, y0
    for _ in range(BN):
        xb, yb = xa + BP, (y1 if ya == y0 else y0)
        pts += [(xa + BP * 0.364, ya), (xb - BP * 0.364, yb), (xb, yb)]
        xa, ya = xb, yb
    return pts + [(xa + 30, ya), (xa + 60, ya), (xa + 90, ya)]


def bead(key, cx, cy, icon, z):
    return [R(key + '/c', cx - NR, cy - NR, 2 * NR, 2 * NR, prst='ellipse', fill='FFFFFF', line='E4DDF7', line_w=1.2, shadow=(14, 4, '6B4EFF', 14)),
            P(key + '/i', icon, cx - z / 2, cy - z / 2, z, z)]


def s_next2b(key='n2b'):
    """(가)의 모든 것이 왼쪽으로 물러나고, 두 줄이 서로 엮이며 뻗는다. 마루마다 위에는 기록, 아래에는 기기가 꿰인다."""
    s = Slide(key, trans=('morph', 1300), bar=False, notes=CLOSE)
    tl_past(s, -(PAN + GONE), gone=True)
    parts_a(s, dx=-GONE, alpha=0)
    s.add('n2b/title', [N.title('n2b/title', TITLE_B)])
    for name, top in (('a', True), ('b', False)):
        pts = braid(top)
        s.add('n2b/th' + name, [C('n2b/th%s/glow' % name, pts, w=11, color='B9A6FF', alpha=26),
                                C('n2b/th%s/line' % name, pts, w=3.4, stops=[(0, '6B4EFF', None), (100, 'A48BFF', None)])])
    xs = [BX + BP * k for k in range(BN)]
    for k, x in enumerate(xs):
        s.add('n2b/r%d' % k, [line('n2b/r%d/stem' % k, (x, YU - 4), (x, RY + NR), color=PURPLE2, w=2.2)] +
              bead('n2b/r%d' % k, x, RY, ICON[REC[k]], 36))
        s.add('n2b/d%d' % k, [line('n2b/d%d/stem' % k, (x, YL + 4), (x, DY - NR), color=PURPLE2, w=2.2)] +
              bead('n2b/d%d' % k, x, DY, str(AS / ('ic-%s.png' % DEV[k])), 34))
        cx = x + BP / 2                                 # 두 가닥이 엇갈리는 곳: 작은 Weave
        s.add('n2b/x%d' % k, [R('n2b/x%d/c' % k, cx - 11, YC - 11, 22, 22, prst='ellipse', line='FFFFFF', line_w=2, grad=GRAD, shadow=(8, 2, '6B4EFF', 30)),
                              P('n2b/x%d/s' % k, ICON['spool_w'], cx - 6.5, YC - 6.5, 13, 13)])
    s.add('n2b/lab', [T('n2b/lab/r', 36, RY - 13, 100, 26, '기록', size=15, color=SUB, weight='b', align='c', anchor='ctr'),
                      T('n2b/lab/d', 36, DY - 13, 100, 26, '기기', size=15, color=SUB, weight='b', align='c', anchor='ctr')])
    s.add('n2b/rule', [C('n2b/rule', [(xs[0] - 40, RULE_Y)] * 2 + [(1236, RULE_Y)] * 2, color='C9BFEA', w=1.8, tail='triangle')])
    for k, year in YEARS:
        x = xs[k] + BP / 2
        s.add('n2b/y%d' % k, [R('n2b/y%d/t' % k, x - 0.9, RULE_Y - 6, 1.8, 12, fill='B0A4DC', line=None),
                              T('n2b/y%d/l' % k, x - 40, RULE_Y + 8, 80, 22, year, size=13, color=PURPLE if k == 0 else SUB, weight='b', align='c', anchor='ctr')])
    # 장이 열리면: 실 두 가닥이 왼쪽에서 오른쪽으로 엮여 나가고, 지나가는 자리마다 기록과 기기가 꿰임
    t0, dur = 200, 1700
    at = lambda x: t0 + dur * (x + 16) / (xs[-1] + BP + 90 + 16)
    s.on('n2b/title', 'fade_in', 0, 400)
    s.on('n2b/lab', 'fade_in', 150, 400)
    s.on(['n2b/tha', 'n2b/thb'], 'wipe_in', t0, dur, dir='left')
    s.on('n2b/rule', 'wipe_in', t0, dur, dir='left')
    for k, x in enumerate(xs):
        s.on(['n2b/r%d' % k, 'n2b/d%d' % k], 'zoom_in', at(x) - 40, 340, **{'from': 0.6})
        s.on('n2b/x%d' % k, 'zoom_in', at(x + BP / 2) - 30, 260, **{'from': 0.5})
    for k, _ in YEARS:
        s.on('n2b/y%d' % k, 'fade_in', at(xs[k] + BP / 2) + 60, 300)
    return s


def specs(deck=False):
    """영상: 35쪽의 마지막 구간부터. 덱: 35쪽(지금 덱의 장 그대로) 다음에."""
    return [N.s_tl() if deck else NX.s_tl_end(), s_next2a(), s_next2b()]


CANDIDATES = [('미래2', specs, '두 줄이 다시 뻗음, 끝에는 엮임', NX.FUT)]
