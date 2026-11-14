"""9차 후보(11-14): 34쪽 비즈니스 임팩트 장을 다시 그린 세 가지. 덱에는 아직 넣지 않았고 tools/next_try.py로 후보 덱, 그림, 낭독 영상을 만든다.

- 임팩트가 '다음 세대가 고를 이유': 한국갤럽 조사(13~18세: 지금 갤럭시 61% → 다음에 사고 싶은 휴대폰 갤럭시 47%)와
  우리 설문의 아이폰 사용자 62명(61명이 같은 불편, 60명이 기록을 찾아 주는 AI를 쓰겠다고 답함). 고리 그래프 없이 띠와 점으로.
- 임팩트나 '8억 대': Galaxy AI가 들어가는 기기(2025년 말 4억 대 → 2026년 말 8억 대). 작은 휴대폰 80개(하나 = 1,000만 대)에 Weave가 번짐.
- 임팩트다 '옮길 수 없는 실': 지금 장의 말(쓸수록 쌓여 떠나기 어려움)을 숫자 없이 그림으로. 기록은 다른 휴대폰으로 옮겨도 이어 둔 실은 옮겨지지 않는다.

숫자의 출처는 장마다 각주에. 좌표는 1280×720 px.
"""
import math
from pathlib import Path

import build as HW
from ui import BODY, ICON, INK, INK2, LINE, MUTE, PURPLE, PURPLE2, SUB, SHADOW_CARD, C, P, R, T, line, star4_icon, tw

import slides_new as N

Slide = HW.Slide
HERE = Path(__file__).resolve().parent
OUTRO = HERE / 'assets' / 'outro'
NAVY = N.NAVY
GRAY = 'A9A3BA'
SOFT = 'E4DDF7'
GRAD = dict(stops=[(0, '8D6BFF', None), (100, '5A3FE0', None)], ang=55)

NOTES = {
    'biza': ('갤럽 조사에서 10대의 61%는 갤럭시를 쓰고 있지만, 다음에 사고 싶은 휴대폰으로 갤럭시를 고른 10대는 47%였습니다. '
             '(클릭) 그런데 저희 설문에서 아이폰을 쓰는 응답자 62명 중 61명도 같은 불편을 겪고 있었고, '
             '(클릭) 60명은 기록을 찾아 주는 AI가 있다면 쓰겠다고 답했습니다. Weave는 다음 세대가 갤럭시를 고를 이유가 됩니다.'),
    'bizb': ('Galaxy AI가 들어간 기기는 지난해 말 4억 대에서, 올해 말 8억 대로 늘어납니다. '
             '(클릭) Weave는 새 부품이 필요 없는 소프트웨어입니다. 업데이트 한 번으로, 8억 대의 갤럭시가 내 기록을 아는 휴대폰이 될 수 있습니다.'),
    'bizc': ('Weave가 이어 둔 기억은 쓸수록 촘촘해집니다. '
             '(클릭) 사진과 메모는 다른 휴대폰으로 옮길 수 있습니다. '
             '(클릭) 하지만 그 사이를 이어 둔 실은 옮길 수 없습니다. 쓸수록 갤럭시를 떠나기 어려워지는 이유입니다.'),
}
SRC_A = ("* ¹ 한국갤럽, 「스마트폰 관련 조사 2012-2026」 (2026. 07), 13~18세 200명   "
         "² 스마트폰 내 개인 기록 탐색 및 재검색 행태에 관한 자체 설문조사 (응답자 210명, '26.11) 중 아이폰 사용자 62명")
SRC_B = '* ¹ 삼성전자 발표: Reuters 인터뷰 (2026. 01), Galaxy Unpacked (2026. 02, 2026. 07)'


# ------------------------------------------------------------------ 임팩트가: 다음 세대가 고를 이유
A_DY = 48                                   # 내용 묶음을 아래로 내린 만큼(제목과 각주 사이의 가운데에 오게)
A_BAR = (92, 470, 52)                       # 띠의 왼쪽 x, 폭, 높이
A_IPHONE = '8E88A0'
A_ROWS = [('지금 쓰는 휴대폰', 206, [('갤럭시', 61, PURPLE), ('아이폰', 39, A_IPHONE)]),
          ('다음에 사고 싶은 휴대폰', 316, [('갤럭시', 47, PURPLE), ('아이폰', 51, A_IPHONE), ('', 2, SOFT)])]      # 나머지 2% = 아직 모르겠다
A_GRID = (676, 184, 24, 34, 16)             # 점 묶음의 왼쪽 x, 위 y, 점 지름, 간격, 한 줄의 점 수
A_N = 62


def a_bar(key, y, segs):
    """가로 띠 하나: 몫만큼 나눈 조각(사이에 3px 틈)과 조각 안의 이름, 숫자."""
    x0, w, h = A_BAR
    gap = 3
    room = w - gap * (len(segs) - 1)
    out, x = [], x0
    for i, (name, pct, col) in enumerate(segs):
        sw = room * pct / 100
        out.append(R('%s/s%d' % (key, i), x, y, sw, h, prst='roundRect', radius=min(10, sw / 2), fill=col, line=None))
        if name:
            lab = [[(name + ' ', dict(size=13.5)), ('%d%%' % pct, dict(size=18))]]
            out.append(T('%s/t%d' % (key, i), x, y, sw, h, lab, size=13.5, color='FFFFFF', weight='b', align='c', anchor='ctr'))
        x += sw + gap
    return out


def a_dots(key, n_on, color, d_pad=0.0):
    """점 62개 가운데 앞의 n_on개. 한 줄에 16개씩."""
    x0, y0, d, gap, cols = A_GRID
    out = []
    for i in range(n_on):
        r_, c_ = divmod(i, cols)
        out.append(R('%s/%d' % (key, i), x0 + c_ * gap - d_pad, y0 + A_DY + r_ * gap - d_pad, d + 2 * d_pad, d + 2 * d_pad, prst='ellipse', fill=color, line=None))
    return out


def a_stat(key, y, num, color, text):
    nw = tw(num, 30, 'b')
    x = A_GRID[0]
    return [T(key + '/n', x - 2, y, nw + 10, 44, num, size=30, color=color, weight='b', anchor='ctr', spc=-0.5),
            T(key + '/t', x + nw + 16, y + 2, 420, 44, text, size=16, color=INK2, weight='b', anchor='ctr')]


def s_biza(key='biza'):
    """10대의 선택(띠 둘) → (클릭) 아이폰 사용자 62명 중 61명이 같은 불편 → (클릭) 60명이 쓰겠다."""
    s = Slide(key, trans=('fade', 500), bar=False, notes=NOTES[key])
    s.add('ba/title', [N.title('ba/title', [('다음 세대가 ', INK), ('갤럭시를 고를 이유', PURPLE)])])
    x0, w, h = A_BAR
    dy = A_DY
    s.add('ba/lh', [T('ba/lh', x0, 140 + dy, 470, 26, '13~18세의 휴대폰¹', size=14, color=SUB, weight='b', anchor='ctr')])
    rows = []
    for i, (lab, y, segs) in enumerate(A_ROWS):
        k = 'ba/r%d' % i
        s.add(k + '/lab', [T(k + '/lab', x0, y + dy - 28, 300, 24, lab, size=13, color=INK2, weight='b', anchor='ctr')])
        s.add(k + '/bar', a_bar(k + '/bar', y + dy, segs))
        rows.append(k)
    # 61 → 47: 두 띠의 갤럭시 조각 끝을 잇는 옅은 점선
    xa, xb = x0 + (w - 3) * 0.61, x0 + (w - 6) * 0.47
    ya, yb = A_ROWS[0][1] + dy + h + 4, A_ROWS[1][1] + dy - 4
    s.add('ba/drop', [C('ba/drop', [(xa, ya), (xa, ya + 20), (xb, yb - 20), (xb, yb)], color=PURPLE2, w=2.2, dash='dash')])
    s.add('ba/cap', [T('ba/cap', x0, 396 + dy, 470, 40, [[('스스로 고를 때, 갤럭시는 ', dict(color=INK)), ('61%에서 47%로', dict(color=PURPLE))]],
                       size=18, weight='b', anchor='ctr')])
    s.add('ba/rule', [R('ba/rule', 620, 144 + dy, 1, 296, fill='D9CEFA', line=None)])
    s.add('ba/rh', [T('ba/rh', A_GRID[0] - 2, 140 + dy, 520, 26, '아이폰을 쓰는 설문 응답자 62명²', size=14, color=SUB, weight='b', anchor='ctr')])
    s.add('ba/d0', a_dots('ba/d0', A_N, SOFT))
    s.add('ba/d1', a_dots('ba/d1', 61, NAVY))
    s.add('ba/d2', a_dots('ba/d2', 60, PURPLE, 0.6))
    gy = A_GRID[1] + dy + 4 * A_GRID[3]
    s.add('ba/s1', a_stat('ba/s1', gy + 12, '61명', NAVY, '같은 불편을 겪었어요'))
    s.add('ba/s2', a_stat('ba/s2', gy + 66, '60명', PURPLE, '기록을 찾아 주는 AI가 있다면 쓰겠어요'))
    s.add('ba/src', [T('ba/src', 60, 652, 1160, 36, SRC_A, size=9, color=MUTE, wrap=True, lnspc=13)])
    # 장이 열리면: 띠 둘이 차례로
    s.on('ba/lh', 'fade_in', 150, 350)
    s.on(rows[0] + '/lab', 'fade_in', 250, 300)
    s.on(rows[0] + '/bar', 'wipe_in', 300, 650, dir='left')
    s.on(rows[1] + '/lab', 'fade_in', 1050, 300)
    s.on(rows[1] + '/bar', 'wipe_in', 1100, 650, dir='left')
    s.on('ba/drop', 'fade_in', 1750, 350)
    s.on('ba/cap', 'rise', 1900, 480, dy=10)
    s.click()      # 1: 아이폰 사용자 62명, 그 가운데 61명
    s.on(['ba/rule', 'ba/rh'], 'fade_in', 0, 300)
    s.on('ba/d0', 'fade_in', 80, 320)
    s.on('ba/d1', 'wipe_in', 420, 800, dir='left')
    s.on('ba/s1', 'rise', 900, 460, dy=10)
    s.click()      # 2: 60명
    s.on('ba/d2', 'wipe_in', 0, 800, dir='left')
    s.on('ba/s2', 'rise', 420, 460, dy=10)
    return s


# ------------------------------------------------------------------ 임팩트나: 8억 대
B_GRID = (574, 190, 26, 44, 39, 60, 16, 5)      # 왼쪽 x, 위 y, 휴대폰 폭, 높이, 가로 간격, 세로 간격, 한 줄의 수, 줄 수


def b_phones(key, idx, fill, line_c, spool=False):
    x0, y0, pw, ph, gx, gy, cols, _ = B_GRID
    out = []
    for i in idx:
        r_, c_ = divmod(i, cols)
        x, y = x0 + c_ * gx, y0 + r_ * gy
        if spool:
            out.append(R('%s/p%d' % (key, i), x, y, pw, ph, prst='roundRect', radius=6, fill=None, grad=GRAD, line=None))
            out.append(P('%s/s%d' % (key, i), ICON['spool_w'], x + (pw - 14) / 2, y + (ph - 14) / 2, 14, 14))
        else:
            out.append(R('%s/p%d' % (key, i), x, y, pw, ph, prst='roundRect', radius=6, fill=fill, line=line_c, line_w=1.2))
    return out


def b_num(key, y, num, unit, color, pt, label):
    nw = tw(num, pt, 'b') + tw(unit, pt * 0.5, 'b') + 4
    return [T(key + '/n', 96, y, nw + 12, pt * 1.5, [[(num, dict(size=pt)), (unit, dict(size=pt * 0.5))]], size=pt, color=color, weight='b', anchor='ctr', spc=-1),
            T(key + '/l', 98, y + pt * 1.5 - 2, 420, 26, label, size=14.5, color=INK2 if color == PURPLE else SUB, anchor='ctr')]


def s_bizb(key='bizb'):
    """작은 휴대폰 80개(하나 = 1,000만 대): 4억 대 → 8억 대 → (클릭) 모두 Weave의 보라로."""
    s = Slide(key, trans=('fade', 500), bar=False, notes=NOTES[key])
    s.add('bb/title', [N.title('bb/title', [('업데이트 한 번으로, ', INK), ('8억 대의 갤럭시에', PURPLE)])])
    cols, nrow = B_GRID[6], B_GRID[7]
    half = [i for i in range(cols * nrow) if i % cols < cols // 2]
    rest = [i for i in range(cols * nrow) if i % cols >= cols // 2]
    s.add('bb/base', b_phones('bb/base', range(cols * nrow), 'F7F4FF', 'E4DDF7'))
    s.add('bb/h1', b_phones('bb/h1', half, 'D9CEFA', 'C3B4F5'))
    s.add('bb/h2', b_phones('bb/h2', rest, 'D9CEFA', 'C3B4F5'))
    s.add('bb/on', b_phones('bb/on', range(cols * nrow), None, None, spool=True))
    s.add('bb/n4', b_num('bb/n4', 196, '4', '억 대', GRAY, 40, '2025년 말'))
    s.add('bb/n8', b_num('bb/n8', 300, '8', '억 대', PURPLE, 76, '2026년 말, Galaxy AI가 들어가는 기기¹'))
    gx0, gy0 = B_GRID[0], B_GRID[1] + nrow * B_GRID[5] - 8
    s.add('bb/leg', [R('bb/leg/p', gx0, gy0 + 5, 13, 21, prst='roundRect', radius=3.5, fill='D9CEFA', line='C3B4F5', line_w=1.0),
                     T('bb/leg/t', gx0 + 20, gy0 + 4, 200, 22, '= 1,000만 대', size=11.5, color=MUTE, anchor='ctr')])
    s.add('bb/cap', [T('bb/cap', 96, 470, 440, 64, [[('새 부품 없이, ', dict(color=INK))], [('그 위에 더하는 소프트웨어', dict(color=PURPLE))]],
                       size=20, weight='b', lnspc=23)])
    s.add('bb/src', [N.foot('bb/src', SRC_B, pt=9)])
    s.on('bb/base', 'fade_in', 150, 350)
    s.on('bb/n4', 'rise', 300, 420, dy=10)
    s.on('bb/h1', 'wipe_in', 420, 600, dir='left')
    s.on('bb/h2', 'wipe_in', 1500, 600, dir='left')
    s.on('bb/n8', 'rise', 1600, 480, dy=12)
    s.on('bb/leg', 'fade_in', 2100, 350)
    s.click()      # 1: Weave가 번짐
    s.on('bb/on', 'wipe_in', 0, 1000, dir='left')
    s.on('bb/cap', 'rise', 450, 480, dy=10)
    return s


# ------------------------------------------------------------------ 임팩트다: 옮길 수 없는 실
C_PH = (200, 344)                            # 휴대폰 크기
C_Y = 156                                    # 휴대폰의 위
C_LX, C_RX = 390, 890                        # 왼쪽(갤럭시), 오른쪽(다른 휴대폰)의 가운데
C_RECS = [    # (아이콘, 휴대폰 가운데에서 (dx, dy), 처음부터 보이는가)
    ('talk', (-62, -98), 1), ('gallery', (62, -98), 1), ('note', (-66, 92), 1), ('cal', (64, 96), 1),
    ('mail', (0, -130), 0), ('map', (-72, -8), 0), ('wallet', (72, -8), 0), ('phone', (0, 130), 0),
    (str(OUTRO / 'app-messages.png'), (-34, -52), 0), (str(OUTRO / 'app-reminder.png'), (36, -48), 0),
    (str(OUTRO / 'app-recorder.png'), (-40, 50), 0), (str(OUTRO / 'app-contacts.png'), (40, 46), 0),
]
C_LINKS = [(0, 4), (1, 4), (0, 5), (1, 6), (2, 5), (3, 6), (2, 7), (3, 7), (8, 0), (9, 1), (10, 2), (11, 3), (8, 5), (9, 6)]      # 기록끼리 잇는 실(번호 쌍)


def c_phone(key, cx, gray=False):
    w, h = C_PH
    x, y = cx - w / 2, C_Y
    g = 'A9A6BA'
    ny = y + h - 22
    frame = dict(stops=[(0, 'E3E3EA', None), (100, 'CBCBD6', None)], ang=60) if gray else dict(stops=[(0, 'D5D8EC', None), (100, 'B7BBD8', None)], ang=60)
    return [R(key + '/frame', x, y, w, h, prst='roundRect', radius=34, line='FFFFFF', line_w=1.2, shadow=(30, 12, '5B3FE6', 9 if gray else 20), grad=frame),
            R(key + '/screen', x + 6, y + 6, w - 12, h - 12, prst='roundRect', radius=28, fill='FFFFFF', line=None),
            R(key + '/cam', cx - 4, y + 16, 8, 8, prst='ellipse', fill='23212B', line=None),
            R(key + '/n1a', cx - 46, ny, 1.5, 9, fill=g, line=None), R(key + '/n1b', cx - 42.5, ny, 1.5, 9, fill=g, line=None),
            R(key + '/n1c', cx - 39, ny, 1.5, 9, fill=g, line=None),
            R(key + '/n2', cx - 5, ny - 0.5, 10, 10, prst='roundRect', radius=3, fill=None, line=g, line_w=1.5),
            C(key + '/n3a', [(cx + 44, ny)] * 2 + [(cx + 39.5, ny + 4.5)] * 2, color=g, w=1.5),
            C(key + '/n3b', [(cx + 39.5, ny + 4.5)] * 2 + [(cx + 44, ny + 9)] * 2, color=g, w=1.5)]


def s_bizc(key='bizc'):
    """갤럭시 안에서 기록이 실로 이어짐 → (클릭) 더 촘촘해지고, 다른 휴대폰이 뜸 → (클릭) 기록은 옮겨 가지만 실은 옮겨지지 않음."""
    s = Slide(key, trans=('fade', 500), bar=False, notes=NOTES[key])
    s.add('bc/title', [N.title('bc/title', [('쓸수록 쌓여, ', INK), ('갤럭시를 떠나기 어려워집니다', PURPLE)])])
    cyc = C_Y + C_PH[1] / 2 - 4                 # 휴대폰 안 Weave 동그라미의 가운데
    isz = 30
    s.add('bc/glow', [R('bc/glow', C_LX - 210, cyc - 210, 420, 420, prst='ellipse', fill=None, line=None,
                        grad=dict(stops=[(0, '8B6BFF', 26), (50, 'B9A6FF', 11), (100, 'F2EDFF', 0)], path='circle'))])
    s.add('bc/pl', c_phone('bc/pl', C_LX))
    s.add('bc/pr', c_phone('bc/pr', C_RX, gray=True))
    first = [i for i, r in enumerate(C_RECS) if r[2]]
    later = [i for i, r in enumerate(C_RECS) if not r[2]]
    pos = [(C_LX + dx, cyc + dy) for _, (dx, dy), _ in C_RECS]

    def spoke(i):
        x, y = pos[i]
        return C('bc/sp%d' % i, [(C_LX, cyc)] * 2 + [(x, y)] * 2, w=2.0, color=PURPLE2, alpha=80)

    def chord(n, a, b):
        return C('bc/ch%d' % n, [pos[a]] * 2 + [pos[b]] * 2, w=1.5, color='B9A6FF', alpha=90)
    s.add('bc/th1', [spoke(i) for i in first])
    s.add('bc/th2', [spoke(i) for i in later] + [chord(n, a, b) for n, (a, b) in enumerate(C_LINKS)])
    icon = lambda k, i, cx, a=100: P('%s%d' % (k, i), ICON.get(C_RECS[i][0], C_RECS[i][0]), cx + C_RECS[i][1][0] - isz / 2, cyc + C_RECS[i][1][1] - isz / 2,
                                     isz, isz, alpha=a, shadow=(8, 2, '6B4EFF', 14) if a == 100 else None)
    s.add('bc/ic1', [icon('bc/ic', i, C_LX) for i in first])
    s.add('bc/ic2', [icon('bc/ic', i, C_LX) for i in later])
    r = 26
    s.add('bc/wv', [R('bc/wv/c', C_LX - r, cyc - r, 2 * r, 2 * r, prst='ellipse', line='FFFFFF', line_w=2.2, shadow=(16, 5, '6B4EFF', 34), grad=GRAD),
                    P('bc/wv/sp', ICON['spool_w'], C_LX - 15, cyc - 15, 30, 30)])
    s.add('bc/gic', [icon('bc/gic', i, C_RX, 46) for i in range(len(C_RECS))])
    s.add('bc/hole', [R('bc/hole', C_RX - r, cyc - r, 2 * r, 2 * r, prst='ellipse', fill=None, line='C9C6D6', line_w=1.6, dash='dash')])
    ly = C_Y + C_PH[1] + 14
    s.add('bc/ll', [T('bc/ll', C_LX - 120, ly, 240, 28, '갤럭시', size=17, color=PURPLE, weight='b', align='c', anchor='ctr')])
    s.add('bc/rl', [T('bc/rl', C_RX - 120, ly, 240, 28, '다른 휴대폰', size=17, color=SUB, weight='b', align='c', anchor='ctr')])
    ax0, ax1 = C_LX + C_PH[0] / 2 + 34, C_RX - C_PH[0] / 2 - 34
    s.add('bc/arr', [C('bc/arr', [(ax0, cyc)] * 2 + [(ax1, cyc)] * 2, color='B9B2C9', w=2.2, tail='triangle'),
                     T('bc/arr/t', (ax0 + ax1) / 2 - 80, cyc - 34, 160, 24, '옮기면', size=14, color=SUB, weight='b', align='c', anchor='ctr')])
    s.add('bc/cap', [T('bc/cap', 140, 578, 1000, 40, [[('기록은 옮겨도, ', dict(color=INK)), ('이어 둔 실은 옮겨지지 않습니다', dict(color=PURPLE))]],
                       size=22, weight='b', align='c', anchor='ctr', spc=-0.3)])
    # 장이 열리면: 갤럭시와 기록 넷, 실 넷
    s.on(['bc/glow', 'bc/pl', 'bc/ll'], 'rise', 150, 520, dy=14)
    s.on('bc/wv', 'zoom_in', 520, 380, **{'from': 0.6})
    s.on('bc/ic1', 'fade_in', 700, 380)
    s.on('bc/th1', 'fade_in', 950, 420)
    s.on('bc/ic2', 'fade_in', 1650, 420)
    s.on('bc/th2', 'fade_in', 1950, 520)
    s.click()      # 1: 다른 휴대폰, 기록은 옮겨 감
    s.on(['bc/pr', 'bc/rl'], 'rise', 0, 480, dy=14)
    s.on('bc/arr', 'wipe_in', 250, 420, dir='left')
    s.on('bc/gic', 'fade_in', 620, 480)
    s.click()      # 2: 실은 옮겨지지 않음
    s.on('bc/hole', 'fade_in', 0, 380)
    s.on('bc/wv', 'pulse', 80, 190, scale=1.1)
    s.on('bc/cap', 'rise', 280, 520, dy=10)
    return s


BIZ = HERE / '비즈니스임팩트_후보'


def _one(fn):
    return lambda deck=False: [fn()]


CANDIDATES = [('임팩트가', _one(s_biza), '다음 세대가 고를 이유', BIZ),
              ('임팩트나', _one(s_bizb), '8억 대', BIZ),
              ('임팩트다', _one(s_bizc), '옮길 수 없는 실', BIZ)]
