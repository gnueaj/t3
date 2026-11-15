"""Appendix E 묶음: 시나리오 더 보기 (11-15).

UX마다 한 장, 한 장에 장면 둘. 장면은 왼쪽부터 [사용자의 말이나 계기] → [단서가 된 기록] → [Weave가 건네는 것] 순서로 놓인다.
화면의 장면마다 붙는 한 줄 설명은 짧게 줄였고, Carbon이 쓴 설명 문장은 대본(Page.a)에 그대로 있다.
씨앗은 사용자가 준 여섯 장면이고, 글은 Carbon(Gemini)이 다듬었다(11-15). 고른 안과 바꾼 곳은 `Appendix_QnA_대본.md`의 근거에 적었다.
기록 카드는 35쪽(미래의 Weave)과 같은 짜임이다: 앱 아이콘, 굵은 이름, 작은 회색 줄 '앱 이름 · 날짜', 본문(카카오톡과 메시지는 회색 말풍선). 갤러리는 사진을 묘사한 이름만.
가전이 나오는 장면 셋에는 '미래' 꼬리표를 달았다.
"""
from pathlib import Path

from ui import (BODY, GRAY_FILL, ICON, INK, LAV2, LINE, LINE2, MUTE, PURPLE, PURPLE2, RING, SUB, SHADOW_SOFT, P, R, T, chip)

from qna_lib import (GRAY_BG, Page, arrow, box, lh_of, page_slide, para, wrapl)

HERE = Path(__file__).resolve().parent
NX, OU = HERE / 'assets' / 'next', HERE / 'assets' / 'outro'
IC = {'cal': ICON['cal'], 'note': ICON['note'], 'talk': ICON['talk'], 'gallery': ICON['gallery'], 'msg': OU / 'app-messages.png',
      'fridge': NX / 'ic-refrigerator.png', 'washer': NX / 'ic-washing-machine.png', 'school': OU / 'ic-rag.png', 'bixby': NX / 'app-bixby.png',
      'weave': ICON['spool']}
PAD, ISZ, LH = 14, 30, 18.5


def rec(key, x, y, w, icon, name, meta=None, lines=(), bubble=False):
    """기록 카드 하나. 돌려줌: (원시 목록, 높이)."""
    body = []
    for ln in lines:
        body += wrapl(ln, 11, w - 2 * PAD - (24 if bubble else 0))
    if not meta and not body:                     # 갤러리: 사진을 묘사한 이름만
        h = PAD * 2 + ISZ
        return [R(key + '/bg', x, y, w, h, prst='roundRect', radius=16, fill='FFFFFF', line=LINE, line_w=1.0, shadow=SHADOW_SOFT),
                P(key + '/ic', IC[icon], x + PAD, y + PAD, ISZ, ISZ),
                T(key + '/n', x + PAD + ISZ + 10, y, w - PAD * 2 - ISZ - 10, h, name, size=12, color=INK, weight='b', anchor='ctr')], h
    by = y + PAD + ISZ + 10
    bh = LH * len(body) + (14 if bubble else 0)
    h = (by - y) + bh + PAD if body else PAD * 2 + ISZ
    out = [R(key + '/bg', x, y, w, h, prst='roundRect', radius=16, fill='FFFFFF', line=LINE, line_w=1.0, shadow=SHADOW_SOFT),
           P(key + '/ic', IC[icon], x + PAD, y + PAD, ISZ, ISZ),
           T(key + '/n', x + PAD + ISZ + 10, y + PAD - 3, w - PAD * 2 - ISZ - 10, 20, name, size=12.5, color=INK, weight='b'),
           T(key + '/m', x + PAD + ISZ + 10, y + PAD + 16, w - PAD * 2 - ISZ - 10, 16, meta or '', size=9.5, color=MUTE)]
    if body:
        if bubble:
            out.append(R(key + '/bb', x + PAD, by, w - 2 * PAD, bh, prst='roundRect', radius=12, fill=GRAY_FILL, line=None))
        out.append(T(key + '/b', x + PAD + (12 if bubble else 0), by + (7 if bubble else 0), w - 2 * PAD - (24 if bubble else 0), LH * len(body) + 4, body,
                     size=11, color=BODY, lnspc=LH * 0.75))
    return out, h


def scenario(s, key, y, h, tag, title, say_label, say, desc, columns, res_icon, res_head, res_lines, res_note=None):
    """장면 하나. columns = [[기록, …], …] (기록 = rec()의 인자 dict). 가로로 말 → 기록 → 결과."""
    x0, lw, rw_, gap = 94, 236, 262, 34
    out = [box(key + '/bg', 70, y, 1140, h)]
    c, cw = chip(key + '/tag', x0, y + 20, tag, 'fill' if tag == '미래' else 'soft', pt=9.5, h=20, padx=9)
    out += c
    out.append(T(key + '/t', x0 + cw + 8, y + 16, lw - cw - 8, 28, title, size=13.5, color=INK, weight='b', anchor='ctr'))
    out.append(T(key + '/sl', x0, y + 54, lw, 16, say_label, size=9.5, color=MUTE, weight='b'))
    sl = wrapl(say, 12, lw - 28, 'm')
    sh = lh_of(12) * len(sl) + 18
    out += [R(key + '/sb', x0, y + 74, lw, sh, prst='roundRect', radius=12, fill=GRAY_BG, line=None),
            T(key + '/st', x0 + 14, y + 74 + 9, lw - 28, sh - 18, sl, size=12, color=INK, weight='m', lnspc=lh_of(12) * 0.75)]
    out.append(para(key + '/d', x0, y + 74 + sh + 12, lw, desc, pt=10.5, color=SUB)[0])
    s.add(key, out)
    cx = x0 + lw + gap
    top = y + 20
    s.add(key + '/a1', [arrow(key + '/a1', (cx - gap + 8, y + h / 2), (cx - 8, y + h / 2), color='B9B2C9', w=1.8)])
    for ci, col in enumerate(columns):
        yy = top
        for ri, r in enumerate(col):
            pr, ph = rec('%s/r%d_%d' % (key, ci, ri), cx, yy, rw_, **r)
            s.add('%s/r%d_%d' % (key, ci, ri), pr)
            yy += ph + 10
        cx += rw_ + 12
    cx += gap - 12
    s.add(key + '/a2', [arrow(key + '/a2', (cx - gap + 8, y + h / 2), (cx - 8, y + h / 2), w=2.0)])
    rw = 70 + 1140 - 24 - cx
    rl = []
    for ln in res_lines:
        rl += wrapl(ln, 12.5, rw - 36, 'b')
    rh = 58 + lh_of(12.5) * len(rl) + (30 if res_note else 12)
    out = [box(key + '/o/bg', cx, top, rw, rh, on=True),
           P(key + '/o/ic', IC[res_icon], cx + 18, top + 16, 24, 24),
           T(key + '/o/h', cx + 50, top + 16, rw - 68, 24, res_head, size=11, color=PURPLE, weight='b', anchor='ctr'),
           T(key + '/o/t', cx + 18, top + 52, rw - 36, lh_of(12.5) * len(rl) + 4, rl, size=12.5, color=INK, weight='b', lnspc=lh_of(12.5) * 0.75)]
    if res_note:
        out.append(T(key + '/o/n', cx + 18, top + rh - 30, rw - 36, 18, res_note, size=9.5, color=SUB))
    s.add(key + '/o', out)


def page(key, code, title_runs, scenes):
    s = page_slide(key, code, title_runs)
    y, h = 104, 222
    for i, sc in enumerate(scenes):
        scenario(s, 'qe/%d' % i, y + i * (h + 18), h, **sc)
    return s


# ------------------------------------------------------------------ 장면 (글은 Carbon의 안. 바꾼 곳은 대본 md에)
E1 = [dict(tag='기본', title='취업 준비 때의 일기', say_label='검색창에 입력', say='취업 준비 때 우울할 때마다 썼던 일기',
           desc='캘린더로 시기를 알고, 마음이 드러난 일기를 찾습니다',
           columns=[[dict(icon='cal', name='상반기 공채 서류 마감', meta='캘린더 · 2024년 3월 18일 (월)')],
                    [dict(icon='note', name='집에 오는 길', meta='삼성노트 · 2024년 3월 29일 (금)', lines=['불합격 문자 보고 한참 그냥 걸었다.', '나만 제자리인 것 같아 마음이 무겁다.'])]],
           res_icon='weave', res_head='Weave가 건네는 것', res_lines=['2024년 봄 취업 준비 시기에 작성한 일기 2건을 찾았어요.'],
           res_note='‘우울’이라는 낱말이 없어도 찾습니다'),
      dict(tag='미래', title='엄마의 갈비찜 양념', say_label='요리하다가 말로', say='빅스비, 엄마가 알려준 갈비찜 양념 비율 알려줘',
           desc='레시피 메모와 냉장고 속 재료를 함께 봅니다',
           columns=[[dict(icon='note', name='엄마표 갈비찜 레시피', meta='삼성노트 · 2026년 2월 15일 (일)', lines=['간장 6, 설탕 2, 다진 마늘 2, 참기름 1', '사과 1개랑 배 2개는 꼭 갈아 넣기!'])],
                    [dict(icon='fridge', name='보관 중인 과일', meta='냉장고 · 오늘', lines=['사과 3개', '배 없음'])]],
           res_icon='bixby', res_head='Bixby가 하는 말', res_lines=['간장 6, 설탕 2, 마늘 2, 참기름 1 비율이에요.', '레시피대로 만들려면 배 2개가 더 필요해요.'])]
E2 = [dict(tag='기본', title='눈 내리던 팔공산 사진', say_label='카카오톡 입력 칸에', say='눈 오던 날 팔공산에서 신나게 논 사진',
           desc='카카오톡에서 날짜를 찾고, 눈과 웃는 모습이 담긴 사진을 고릅니다',
           columns=[[dict(icon='talk', name='동현', meta='카카오톡 · 2025년 1월 11일 (토)', lines=['케이블카 타기 전에 팔공산 입구 도착!', '눈 엄청 오는데 패딩 단단히 입고 와'], bubble=True)],
                    [dict(icon='gallery', name='눈길에서 환하게 웃는 모습'), dict(icon='gallery', name='정상 표지석 앞 브이'), dict(icon='gallery', name='눈사람 들고 장난치는 모습')]],
           res_icon='weave', res_head='Weave가 건네는 것', res_lines=['2025년 1월 11일 사진 3장을 대화창에 첨부했어요.'], res_note='찾은 사진 파일을 바로 첨부합니다'),
      dict(tag='기본', title='작년 건강검진 소견', say_label='메일 쓰는 화면에', say='작년에 다른 병원에서 받은 건강검진 소견서',
           desc='안내 문자의 날짜로, 그날 찍은 문서 사진을 찾습니다',
           columns=[[dict(icon='msg', name='한빛건강검진센터', meta='메시지 · 2025년 10월 24일 (금)', lines=['검진 결과지 수령 및 전문의 상담 안내드립니다.', '신분증 지참 후 내원 바랍니다.'], bubble=True)],
                    [dict(icon='gallery', name='책상 위에 놓인 검진 결과지')]],
           res_icon='weave', res_head='Weave가 건네는 것', res_lines=['작년 10월 검진 소견서 사진을 메일에 첨부했어요.'], res_note='병원 이름이 기억나지 않아도 찾습니다')]
E3 = [dict(tag='미래', title='남편 생일 미역국', say_label='계기', say='남편 생일 하루 전, 일요일 저녁',
           desc='생일 일정과 남편의 말, 냉장고 속 재료를 잇습니다',
           columns=[[dict(icon='cal', name='남편 생일', meta='캘린더 · 내일, 11월 16일 (월)'), dict(icon='fridge', name='보관 중인 식재료', meta='냉장고 · 오늘', lines=['건미역 있음, 국간장 있음', '국거리 소고기 없음'])],
                    [dict(icon='talk', name='남편', meta='카카오톡 · 10월 18일 (일)', lines=['나 이번 생일엔 다른 거 말고', '자기가 끓여준 소고기 미역국 먹고 싶어'], bubble=True)]],
           res_icon='fridge', res_head='냉장고가 먼저 건네는 말', res_lines=['내일은 남편분 생일이에요.', '미역국에 넣을 국거리 소고기를 준비해 볼까요?']),
      dict(tag='미래', title='알림장의 체육복', say_label='계기', say='수요일 저녁, 빨래 돌리기 전',
           desc='알림장의 준비물 안내를 전날 저녁에 챙깁니다',
           columns=[[dict(icon='school', name='2학년 3반 주간 안내', meta='알림장 · 11월 16일 (월)', lines=['목요일 3교시는 강당 체육 활동입니다.', '아이들 동복 체육복 꼭 챙겨 입혀 보내주세요.'])]],
           res_icon='washer', res_head='세탁기가 먼저 건네는 말', res_lines=['내일 학교 체육 수업에 체육복이 필요해요.', '오늘 저녁 세탁할 때 체육복도 함께 돌릴까요?'], res_note='알림장은 서드파티 앱의 알림으로 읽습니다')]


def s_e1():
    return page('qe_ux1', 'E-1', [('UX1 기록 통합 검색: 시나리오 더 보기', INK)], E1)


def s_e2():
    return page('qe_ux2', 'E-2', [('UX2 단서로 찾는 기억: 시나리오 더 보기', INK)], E2)


def s_e3():
    return page('qe_ux3', 'E-3', [('UX3 먼저 건네는 기억: 시나리오 더 보기', INK)], E3)


CARBON = '장면의 글은 Carbon(Gemini)이 사용자의 씨앗을 다듬은 것(11-15).'
PAGES = [
    Page('E-1', 'UX1 시나리오 더 보기', s_e1,
         q='기록 통합 검색은 다른 어떤 상황에서 쓰나요?',
         a='두 가지를 준비했습니다. 첫째는 취업 준비 때 우울할 때마다 썼던 일기를 찾는 장면입니다. 캘린더의 공채 일정과 삼성노트의 일기를 함께 읽어, '
           '취업 준비 시절 마음이 힘들 때 남긴 글만 모아 보여 줍니다. 일기에는 우울이라는 낱말이 없고 ‘마음이 무겁다’고만 적혀 있어도 찾습니다. '
           '둘째는 요리하다가 손을 쓸 수 없을 때입니다. 엄마가 알려 준 갈비찜 양념 비율을 Bixby에게 물으면, 삼성노트에 적어 둔 레시피와 냉장고 속 식재료를 함께 확인해 '
           '양념 비율은 물론 부족한 배까지 음성으로 알려 줍니다.',
         more=[('일기처럼 민감한 기록도 다 읽나요?', '어느 앱을 색인할지는 사용자가 정합니다. 읽은 것은 기기 밖으로 나가지 않습니다.'),
               ('냉장고의 재료는 어떻게 아나요?', '2026년형 패밀리허브의 AI 비전이 알아보는 재료를 SmartThings로 받는 것을 전제로 한 미래 장면입니다.')],
         basis=[CARBON + ' 일기 장면은 1안에서 캘린더와 일기 하나를 썼고, 입력하는 말은 사용자의 씨앗에 가깝게 ‘취업 준비 때 우울할 때마다 썼던 일기’로 함(Carbon의 안은 ‘취준할 때 우울해서 썼던 일기들’). 캘린더 카드의 본문 ‘오후 5시 최종 제출 잊지 말기’와 둘째 일기 ‘새벽 단상’은 자리가 없어 뺌.',
                '갈비찜 장면은 1안 그대로. 설 연휴(2026년 2월 16~18일) 전날인 2월 15일의 메모.',
                '날짜와 요일: 2024-03-18 월, 2024-03-29 금, 2026-02-15 일.']),
    Page('E-2', 'UX2 시나리오 더 보기', s_e2,
         q='단서로 찾는 기억은 글자만 찾아 주나요? 사진이나 파일도 되나요?',
         a='사진과 파일도 됩니다. 첫째 장면은 카카오톡 대화 중에 ‘눈 오던 날 팔공산에서 신나게 논 사진’이라고 입력하고 실타래 버튼을 누른 경우입니다. '
           '친구와 나눈 카카오톡으로 팔공산에 간 날짜를 찾고, 갤러리에서 눈 배경과 밝은 표정의 사진을 골라 대화창에 바로 첨부합니다. '
           '둘째는 의사 선생님께 메일을 쓰면서 작년에 다른 병원에서 받은 건강검진 소견서를 찾는 장면입니다. '
           '검진센터 안내 문자의 날짜와 갤러리의 문서 사진을 엮어, 폴더를 뒤지지 않아도 소견서를 메일에 곧바로 넣어 줍니다.',
         more=[('사진의 표정이나 배경은 어떻게 아나요?', '색인할 때 사진을 벡터로 바꿔 둡니다. EmbeddingGemma 2는 글과 사진을 같은 공간에 놓기 때문에 ‘눈’, ‘웃는 모습’ 같은 말로 사진을 찾습니다.'),
               ('엉뚱한 사진을 보내면요?', '바로 보내지 않고 입력 칸에 첨부만 합니다. 보내기는 사용자가 누릅니다.')],
         basis=[CARBON + ' 팔공산 장면은 입력하는 말과 결과는 1안, 카카오톡은 2안(이름 동현. 1안의 민수는 UX1의 민수님과 겹침). 갤러리 이름은 카드 폭에 맞춰 줄임(‘눈 내리는 산길에서 환하게 웃는 모습’ → ‘눈길에서 환하게 웃는 모습’, ‘눈 쌓인 정상 표지석 앞 브이 포즈’ → ‘정상 표지석 앞 브이’).',
                '건강검진 장면은 2안(안내 문자와 문서 사진). 1안의 파일 이름 ‘종합검진_소견서_스캔본.pdf’는 낱말이 겹쳐 한 번의 검색으로 찾아지므로 쓰지 않음. 입력하는 말은 ‘병원서’를 ‘병원에서’로. 갤러리 이름은 ‘책상 위에 놓인 검진 결과지’로 지음.',
                '날짜와 요일: 2025-01-11 토, 2025-10-24 금. 병원 이름은 지어낸 이름.']),
    Page('E-3', 'UX3 시나리오 더 보기', s_e3,
         q='먼저 건네는 기억은 공항 말고 어떤 상황이 있나요?',
         a='집 안 기기와 이어지는 두 장면입니다. 첫째는 남편의 생일 전날입니다. 캘린더의 생일 일정과 지난달 남편의 카카오톡, 그리고 냉장고 재료 상태를 이어, '
           '생일 전날 부족한 미역국 재료를 냉장고가 먼저 챙겨 줍니다. 둘째는 아이의 알림장입니다. '
           '학교 알림장 앱의 준비물 안내를 읽고, 체육 수업 전날 저녁 세탁기가 체육복 세탁을 먼저 챙겨 줍니다. '
           '두 장면 모두 기억을 찾는 일은 휴대폰이 하고, 가전은 그 답을 건네는 자리입니다.',
         more=[('냉장고가 재료를 정확히 알아야 하지 않나요?', '재료를 모를 때는 생일과 부탁만 알려 줍니다. 재료는 냉장고가 알아보는 범위에서만 더합니다.'),
               ('가족이 함께 보는 화면에 개인 대화가 뜨면 곤란하지 않나요?', '가전에는 찾아낸 답만 건네고 대화 원문은 건네지 않습니다. 누구에게 보여 줄지는 Voice ID로 본인이 확인됐을 때로 한정합니다.'),
               ('알림장 같은 서드파티 앱은 어떻게 읽나요?', '카카오톡과 같습니다. 사용자가 허용한 알림으로 읽습니다.')],
         basis=[CARBON + ' 미역국 장면은 1안. 카카오톡 끝의 ‘(웃는 얼굴)’은 그림이 없어 뺌. 체육복 장면은 1안에서 알림장 카드만 쓰고 세탁기 기록 카드(‘주간 의류 세탁 후 4일 경과’)는 뺌.',
                '날짜와 요일: 2026-10-18 일, 2026-11-16 월(체육 수업은 11-19 목, 계기는 11-18 수).',
                '가전 장면은 35쪽(미래의 Weave)의 SmartThings 연동을 전제로 함.']),
]
