"""Appendix에 새로 넣는 장. 11-14: '왜 온디바이스여야 하나요?'(s_ondevice) — 사생활 보호 Q&A(apx_q_data) 바로 뒤.

이 파일은 팀원 저장소(ysy19/superrookie_t3, 통합본_Claude/apx_new.py)의 것을 11-15에 그대로 가져왔다(아이콘 assets/apx/도 함께).
가져온 뒤 바꾼 곳은 하나다: ①의 붉은 상자 '개인 기록을 다루는 기능에는 유출 위험이 큽니다'를
'유출 위험이 크고, 질문마다 기록을 올리고 / 기다려야 해서 통신이 끊기면 쓸 수 없습니다'로(API 호출의 비효율을 보탬, 두 줄이 되어 위 글을 8px 올림).
틀(코드, 쪽 번호, 목차 단추)은 qna_b.py가 씌운다.
11-16 11차(팀 검토): ①의 글이 짧은 줄로 끊겨 오른쪽이 비어 보임 → 글자를 12 → 13pt로 키워 칸을 채우고 가운뎃점을 풀어 씀.
  ②의 상자 셋(PDE, KEEP, Knox Vault)이 색이 제각각 → 같은 모양으로(옅은 보라 바탕, 가는 테, 보라 아이콘). 방패 아이콘은 보라로 칠한 ic-shield-p.png.
  ②와 ③의 자리를 바꿈: ① 밖으로 보내면 → ② 사용자도 기기 안 처리를 원함(설문) → ③ 갤럭시는 기기 안에서 지킴 → 아래 결론. 번호와 각주 번호, 말할 글의 차례도 함께.

흐름은 왼쪽에서 오른쪽으로 ① 밖으로 보내면 생기는 문제 → ② 사용자도 기기 안 처리를 원함(설문) → ③ 갤럭시가 기기 안에서 지키는 구조 → 아래 결론 한 줄.
(11차에 ②와 ③의 자리를 바꿈. 아래 글의 근거에 적힌 ②, ③은 바꾸기 전의 번호)
글의 근거
- ②: 삼성 공식 문구만 씀(09_HowItWorks/리서치/삼성_현재기술_조사.md §1-1). PDE는 개인 데이터를 기기 안에서 분석하는 엔진이고,
  보호는 KEEP(앱별 암호화 저장 공간)과 Knox Vault(변조 방지 하드웨어 보안 환경)가 맡음. PDE 자체를 '보안 계층'이라 부르지 않는다.
  외부 앱용 PDE·KEEP API는 공개된 적이 없으므로 Weave는 '이 구조 위에서 동작하도록 설계'로만 씀.
- ③: 12_설문 13번 문항, 응답자 210명 전원 기준. 휴대폰 안에서만 처리된다면 쓰겠다 169명(80.5%), 밖(서버)으로 나가도 쓰겠다 26명(12.4%),
  어느 쪽이든 쓰지 않겠다 15명(7.1%). 다른 설문 장(93.8% = 197/210)과 같은 분모.
아이콘은 tools/ondevice_assets.py가 assets/apx/에 만든다(ic-pde.png만 assets/outro의 것).
"""
from pathlib import Path

import build as HW
from appendix import head
from ui import (BODY, INK, LAV, LAV2, LINE2, MUTE, PURPLE, SUB, SHADOW_CARD, P, R, T, line, numdot)

import slides_new as N

HERE = Path(__file__).resolve().parent
AP, OUTRO = HERE / 'assets' / 'apx', HERE / 'assets' / 'outro'
Slide = HW.Slide

DEEP = '4A33C9'                      # Knox Vault 층(가장 안쪽, 하드웨어)
MID = 'E3DBFF'                       # KEEP 층
RED_BG, RED_INK = 'FDF0F0', 'B4232B'

NOTES = {'ondevice': ('온디바이스여야 하는 이유는 두 가지입니다. 휴대폰 속 기록에는 나만 아는 정보와 대화 상대의 정보까지 섞여 있어서, '
                      '외부 LLM 서버로 보내는 순간 어디에 남고 어떻게 쓰이는지 사용자가 통제할 수 없습니다. '
                      '사용자도 같은 답을 했습니다. 저희 설문에서 80.5%가 내 기록이 휴대폰 안에서만 처리된다면 쓰겠다고 답했고, '
                      '서버로 나가도 쓰겠다는 답은 12.4%에 그쳤습니다. '
                      '갤럭시는 개인 데이터를 기기 안에서 처리하는 PDE와, 이를 암호화해 지키는 KEEP과 Knox Vault를 갖추고 있고, '
                      'Weave도 이 구조 위에서 기록을 밖으로 내보내지 않고 동작합니다.')}

SURVEY = [(80.5, '휴대폰 안에서만 처리된다면 쓰겠다'), (12.4, '휴대폰 밖(서버)으로 나가도 쓰겠다'), (7.1, '어느 쪽이든 쓰지 않겠다')]
SRC = ["¹ 스마트폰 내 개인 기록 탐색 및 재검색 행태에 관한 자체 설문조사, 13번 문항 (응답자 210명, '26.11)",
       '² Samsung Newsroom, "Samsung Introduces Future-Ready Mobile Security for Personalized AI Experiences" (2025. 07): '
       '"These insights stay entirely on-device, protected by KEEP and further secured by Knox Vault"']

Y0, CH, CW, GAP, X0 = 138, 386, 368, 18, 70          # 카드: 위, 높이, 폭, 사이, 첫 칸 왼쪽(사생활 보호 Q&A 장과 같은 칸)
LH = 12 * 1.33 * 1.4                                   # 12pt 본문 한 줄


def card(key, i, title, bold=False):
    """흰 카드 + 번호 + 제목. 돌려줌: (원시 목록, 카드 왼쪽 x)."""
    x = X0 + i * (CW + GAP)
    out = [R(key + '/bg', x, Y0, CW, CH, prst='roundRect', radius=20, fill='FFFFFF', line=PURPLE if bold else LINE2,
             line_w=1.8 if bold else 1.2, shadow=SHADOW_CARD)]
    out += numdot(key + '/n', x + 34, Y0 + 32, i + 1, r=12, pt=10)
    out.append(T(key + '/t', x + 54, Y0 + 19, CW - 70, 26, title, size=14.5, color=PURPLE, weight='b', anchor='ctr'))
    return out, x


def bullets(key, x, y, w, items, pt=12, color=BODY):
    """• 항목(각 항목은 줄 목록). 둘째 줄부터는 글머리 폭만큼 들여씀."""
    paras = []
    for it in items:
        for j, ln in enumerate(it):
            paras.append(('• ' if j == 0 else '   ') + ln)
    lh = pt * 1.33 * 1.4
    return T(key, x, y, w, lh * len(paras) + 6, paras, size=pt, color=color, lnspc=lh * 0.75)


def note_box(key, x, y, w, lines, fill, ink, pt=12):
    h = pt * 1.33 * 1.4 * len(lines) + 22
    return [R(key + '/bg', x, y, w, h, prst='roundRect', radius=12, fill=fill, line=None),
            T(key + '/t', x + 14, y + 11, w - 28, h - 22, [[(ln, dict(color=ink))] for ln in lines], size=pt, weight='b',
              lnspc=pt * 1.33 * 1.4 * 0.75)]


# ------------------------------------------------------------------ ① 밖으로 보내면
def col_out(s):
    key = 'od/c1'
    out, x = card(key, 0, '외부 LLM API로 보낸다면')
    cy = Y0 + 98
    ax, bx = x + 82, x + CW - 82                       # 휴대폰, 서버 아이콘의 가운데
    out += [P(key + '/ph', AP / 'ic-phone.png', ax - 26, cy - 26, 52, 52),
            P(key + '/cl', AP / 'ic-cloud.png', bx - 30, cy - 30, 60, 60),
            T(key + '/phl', ax - 60, cy + 32, 120, 20, '내 휴대폰 속 기록', size=10.5, color=SUB, align='c'),
            T(key + '/cll', bx - 60, cy + 32, 120, 20, '외부 LLM 서버', size=10.5, color=SUB, align='c'),
            line(key + '/ar', (ax + 38, cy), (bx - 42, cy), w=2, color='C9C2DA', dash='dash', tail='triangle')]
    lw = 64
    out += [R(key + '/lk/bg', (ax + bx) / 2 - lw / 2, cy - 30, lw, 22, prst='roundRect', fill='FFFFFF', line='F2B8BA', line_w=1.0),
            T(key + '/lk/t', (ax + bx) / 2 - lw / 2, cy - 30, lw, 22, '원문 전송', size=9.5, color=RED_INK, weight='b', align='c', anchor='ctr')]
    by = Y0 + 152
    out.append(bullets(key + '/b', x + 24, by, CW - 40,
                       [['대화, 사진, 메모의 원문이', '기기 밖으로 나갑니다'],
                        ['서버에 얼마나 남고 어디에 쓰이는지', '사용자가 확인하고 통제할 수 없습니다'],
                        ['대화 상대의 개인정보까지', '그 사람의 동의 없이 함께 나갑니다']], pt=13))
    out += note_box(key + '/nb', x + 16, Y0 + CH - 16 - (12 * 1.33 * 1.4 * 2 + 22), CW - 32,
                    ['유출 위험이 크고, 질문마다 기록을 올리고', '기다려야 해서 통신이 끊기면 쓸 수 없습니다'],
                    RED_BG, RED_INK)
    s.add(key, out)


# ------------------------------------------------------------------ ② 갤럭시는 기기 안에서
def col_in(s):
    key = 'od/c2'
    out, x = card(key, 2, '갤럭시는 기기 안에서 지킵니다')
    layers = [('Personal Data Engine (PDE)', '개인 데이터를 기기 안에서 분석', LAV2, LINE2, INK, SUB, OUTRO / 'ic-pde.png'),
              ('KEEP', '앱마다 분리된 암호화 저장 공간', LAV2, LINE2, INK, SUB, AP / 'ic-lock.png'),
              ('Knox Vault', '변조 방지 하드웨어 보안 환경', LAV2, LINE2, INK, SUB, AP / 'ic-shield-p.png')]
    ly, lh, lg = Y0 + 64, 58, 8
    lx, lw = x + 18, CW - 36
    for j, (name, desc, fill, edge, ink, sub, ic) in enumerate(layers):
        y = ly + j * (lh + lg)
        out += [R(key + '/l%d/bg' % j, lx, y, lw, lh, prst='roundRect', radius=14, fill=fill, line=edge, line_w=1.0),
                P(key + '/l%d/ic' % j, ic, lx + 14, y + lh / 2 - 15, 30, 30),
                T(key + '/l%d/a' % j, lx + 56, y + 9, lw - 66, 22, name, size=13, color=ink, weight='b'),
                T(key + '/l%d/b' % j, lx + 56, y + 31, lw - 66, 20, desc, size=11, color=sub)]
    by = ly + 3 * lh + 2 * lg + 12
    out.append(T(key + '/b', x + 24, by, CW - 48, 20, '개인 데이터는 기기 안에 머물며 암호화해 보호²', size=11, color=SUB, align='c'))
    out += note_box(key + '/nb', x + 16, Y0 + CH - 16 - (12 * 1.33 * 1.4 * 2 + 22), CW - 32,
                    ['Weave도 이 구조 위에서 동작해', '기록을 기기 밖으로 내보내지 않습니다'], LAV, PURPLE)
    s.add(key, out)


# ------------------------------------------------------------------ ③ 사용자도 원함
def col_user(s):
    key = 'od/c3'
    out, x = card(key, 1, '사용자도 기기 안 처리를 원합니다¹', bold=True)
    out.append(T(key + '/q', x + 24, Y0 + 52, CW - 48, 20, 'Q. AI가 내 메모, 사진, 대화를 살펴 찾아 준다면?', size=11, color=SUB))
    cx, cy, ro = x + 92, Y0 + 152, 64
    track, arc = N.ring(key + '/r', cx, cy, ro, SURVEY[0][0], color=PURPLE)
    out += track + arc
    out.append(T(key + '/pct', cx - ro, cy - 18, 2 * ro, 36, '80.5%', size=23, color=PURPLE, weight='b', align='c', anchor='ctr'))
    tx = cx + ro + 22
    out.append(T(key + '/qt', tx, cy - 40, x + CW - 20 - tx, 80, [[('"내 기록이', dict(color=INK))], [('휴대폰 안에서만', dict(color=PURPLE))],
                                                                    [('처리된다면 쓰겠다"', dict(color=INK))]],
                 size=13.5, weight='b', anchor='ctr', lnspc=13.5 * 1.33 * 1.35 * 0.75))
    ry = Y0 + 236
    for j, (pct, label) in enumerate(SURVEY[1:]):
        y = ry + j * 26
        out += [R(key + '/k%d' % j, x + 26, y + 5, 10, 10, prst='ellipse', fill='B9B2C9' if j == 0 else 'E4DDF7', line=None),
                T(key + '/kl%d' % j, x + 44, y, 230, 20, label, size=11.5, color=BODY),
                T(key + '/kv%d' % j, x + CW - 24 - 70, y, 70, 20, '%.1f%%' % pct, size=11.5, color=INK, weight='b', align='r')]
    out += note_box(key + '/nb', x + 16, Y0 + CH - 16 - (12 * 1.33 * 1.4 * 2 + 22), CW - 32,
                    ['서버로 보내는 방식을 받아들인 응답은', '10명 중 1명 남짓(12.4%)입니다'], LAV, PURPLE)
    s.add(key, out)


def s_ondevice():
    s = Slide('apx_ondevice', trans=('fade', 400), bar=False, notes=NOTES['ondevice'])
    head(s, [('Q. ', PURPLE), ('왜 Weave는 온디바이스여야 하나요?', INK)],
         '휴대폰 속 기록은 밖으로 나가는 순간 통제할 수 없고, 사용자도 기기 안에서 처리될 때 쓰겠다고 답했습니다')
    col_out(s)
    col_user(s)
    col_in(s)
    y, h = Y0 + CH + 18, 54
    s.add('od/end', [R('od/end/bg', X0, y, 3 * CW + 2 * GAP, h, prst='roundRect', radius=27, fill=PURPLE, line=None, shadow=SHADOW_CARD),
                     T('od/end/t', X0, y, 3 * CW + 2 * GAP, h,
                       [[('그래서 Weave는 기록의 색인부터 검색, 답변까지 ', dict(color='FFFFFF')),
                         ('모두 기기 안에서 처리합니다', dict(color='FFFFFF', weight='b'))]],
                       size=15.5, align='c', anchor='ctr')])
    s.add('od/src', [T('od/src', 50, y + h + 14, 1180, 30, SRC, size=8.5, color=MUTE, lnspc=12)])
    return s
