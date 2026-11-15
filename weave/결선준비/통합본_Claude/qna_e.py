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
      'fridge': NX / 'ic-refrigerator.png', 'washer': NX / 'ic-washing-machine.png', 'car': NX / 'ic-car.png', 'wallet': ICON['wallet'], 'school': OU / 'ic-rag.png', 'bixby': NX / 'app-bixby.png',
      'weave': ICON['spool']}
PAD, ISZ, LH = 11, 26, 17
# 칸의 자리: 모든 장, 모든 줄이 같다(11-16: 줄마다 카드의 높이와 자리가 달라 정렬이 안 맞는다는 검토 → 세로는 줄의 가운데, 가로는 고정된 칸)
X_SAY, W_SAY = 92, 222
X_REC, W_REC, G_REC = 348, 240, 12
X_OUT, W_OUT = 886, 302
ROW_Y, ROW_H, ROW_GAP = 100, 184, 10


def rec_lines(w, lines, bubble):
    body = []
    for ln in lines:
        body += wrapl(ln, 10.5, w - 2 * PAD - (18 if bubble else 0))
    return body


def rec_h(w, icon, name, meta=None, lines=(), bubble=False):
    body = rec_lines(w, lines, bubble)
    if not meta and not body:
        return PAD * 2 + ISZ - 4
    if not body:
        return PAD * 2 + ISZ + 2
    return PAD + ISZ + 7 + LH * len(body) + (12 if bubble else 0) + PAD - 2


def rec(key, x, y, w, icon, name, meta=None, lines=(), bubble=False):
    """기록 카드 하나: 앱 아이콘, 굵은 이름, 회색 '앱 이름 · 날짜', 본문(대화는 회색 말풍선). 갤러리는 사진을 묘사한 이름만. 돌려줌: 원시 목록."""
    body = rec_lines(w, lines, bubble)
    h = rec_h(w, icon, name, meta, lines, bubble)
    out = [R(key + '/bg', x, y, w, h, prst='roundRect', radius=14, fill='FFFFFF', line=LINE, line_w=1.0, shadow=SHADOW_SOFT)]
    tx = x + PAD + ISZ + 9
    if not meta and not body:
        return out + [P(key + '/ic', IC[icon], x + PAD, y + (h - ISZ) / 2, ISZ, ISZ),
                      T(key + '/n', tx, y, w - (tx - x) - PAD, h, name, size=11.5, color=INK, weight='b', anchor='ctr')]
    out += [P(key + '/ic', IC[icon], x + PAD, y + PAD, ISZ, ISZ),
            T(key + '/n', tx, y + PAD - 3, w - (tx - x) - PAD, 18, name, size=11.5, color=INK, weight='b'),
            T(key + '/m', tx, y + PAD + 13, w - (tx - x) - PAD, 15, meta or '', size=9, color=MUTE)]
    if body:
        by = y + PAD + ISZ + 7
        bh = LH * len(body) + (12 if bubble else 0)
        if bubble:
            out.append(R(key + '/bb', x + PAD, by, w - 2 * PAD, bh, prst='roundRect', radius=10, fill=GRAY_FILL, line=None))
        out.append(T(key + '/b', x + PAD + (9 if bubble else 0), by + (6 if bubble else 0), w - 2 * PAD - (18 if bubble else 0), LH * len(body) + 4, body,
                     size=10.5, color=BODY, lnspc=LH * 0.75))
    return out


def scenario(s, key, y, h, tag, title, say_label, say, desc, columns, res_icon, res_head, res_lines, res_note=None):
    """장면 하나(한 줄). 왼쪽부터 말이나 계기 → 기록 두 칸 → 건네는 것. 모든 덩이를 줄의 세로 가운데에 맞춘다."""
    cy = y + h / 2
    s.add(key + '/bg', [box(key + '/bg', 70, y, 1140, h, radius=18)])
    # 왼쪽: 꼬리표와 제목, 말(작은 이름 + 글), 한 줄 설명
    sl = wrapl(say, 11.5, W_SAY - 24, 'm')
    dl = wrapl(desc, 10, W_SAY)
    sh = 9 + 14 + lh_of(11.5, 1.4) * len(sl) + 8
    dh = lh_of(10, 1.45) * len(dl)
    th = 24 + 8 + sh + 8 + dh
    assert th <= h - 28, '%s: 왼쪽 글이 줄보다 큼 (%d)' % (key, th)
    ty = y + 18                                  # 제목은 줄마다 같은 높이에(위에서 18)
    c, cw = chip(key + '/tag', X_SAY, ty + 2, tag, 'fill' if tag == '미래' else 'soft', pt=9.5, h=20, padx=9)
    s.add(key + '/say', c + [
        T(key + '/t', X_SAY + cw + 8, ty, W_SAY - cw - 8, 24, title, size=13, color=INK, weight='b', anchor='ctr'),
        R(key + '/sb', X_SAY, ty + 32, W_SAY, sh, prst='roundRect', radius=12, fill=GRAY_BG, line=None),
        T(key + '/sl', X_SAY + 12, ty + 32 + 8, W_SAY - 24, 14, say_label, size=9, color=MUTE, weight='b'),
        T(key + '/st', X_SAY + 12, ty + 32 + 9 + 14, W_SAY - 24, lh_of(11.5, 1.4) * len(sl) + 4, sl, size=11.5, color=INK, weight='m', lnspc=lh_of(11.5, 1.4) * 0.75),
        T(key + '/d', X_SAY, ty + 32 + sh + 8, W_SAY, dh + 4, dl, size=10, color=SUB, lnspc=lh_of(10, 1.45) * 0.75)])
    ay = ty + 32 + sh / 2                         # 첫 화살표는 말 상자의 가운데에서 나감
    s.add(key + '/a1', [arrow(key + '/a1', (X_SAY + W_SAY + 8, ay), (X_REC - 8, ay), color='B9B2C9', w=1.6)])
    # 기록 두 칸
    assert 1 <= len(columns) <= 2, key
    for ci, col in enumerate(columns):
        cx = X_REC + ci * (W_REC + G_REC)
        hs = [rec_h(W_REC, **r) for r in col]
        tot = sum(hs) + 8 * (len(col) - 1)
        assert tot <= h - 20, '%s: 기록 칸이 줄보다 큼 (%d > %d)' % (key, tot, h - 20)
        yy = cy - tot / 2
        for ri, (r, rh) in enumerate(zip(col, hs)):
            s.add('%s/r%d_%d' % (key, ci, ri), rec('%s/r%d_%d' % (key, ci, ri), cx, yy, W_REC, **r))
            yy += rh + 8
    s.add(key + '/a2', [arrow(key + '/a2', (X_REC + 2 * W_REC + G_REC + 8, cy), (X_OUT - 8, cy), w=1.8)])
    # 건네는 것
    rl = []
    for ln in res_lines:
        rl += wrapl(ln, 11.5, W_OUT - 32, 'b')
    rh = 14 + 22 + 8 + lh_of(11.5, 1.4) * len(rl) + (22 if res_note else 0) + 12
    assert rh <= h - 16, '%s: 결과 카드가 줄보다 큼 (%d)' % (key, rh)
    oy = cy - rh / 2
    out = [box(key + '/o/bg', X_OUT, oy, W_OUT, rh, on=True, radius=16, shadow=False),
           P(key + '/o/ic', IC[res_icon], X_OUT + 16, oy + 14, 22, 22),
           T(key + '/o/h', X_OUT + 46, oy + 14, W_OUT - 62, 22, res_head, size=10.5, color=PURPLE, weight='b', anchor='ctr'),
           T(key + '/o/t', X_OUT + 16, oy + 44, W_OUT - 32, lh_of(11.5, 1.4) * len(rl) + 4, rl, size=11.5, color=INK, weight='b', lnspc=lh_of(11.5, 1.4) * 0.75)]
    if res_note:
        out.append(T(key + '/o/n', X_OUT + 16, oy + rh - 30, W_OUT - 32, 18, res_note, size=9.5, color=SUB, anchor='ctr'))
    s.add(key + '/o', out)


def page(key, code, title_runs, scenes):
    s = page_slide(key, code, title_runs)
    for i, sc in enumerate(scenes):
        scenario(s, 'qe/%d' % i, ROW_Y + i * (ROW_H + ROW_GAP), ROW_H, **sc)
    return s


# ------------------------------------------------------------------ 장면 (글은 Carbon의 안. 바꾼 곳은 대본 md에)
E1 = [dict(tag='기본', title='취업 준비 때의 일기', say_label='검색창에 입력', say='취업 준비 때 우울할 때마다 썼던 일기',
           desc='캘린더로 시기를 알고, 마음이 드러난 일기를 찾습니다',
           columns=[[dict(icon='cal', name='상반기 공채 서류 마감', meta='캘린더 · 2024년 3월 18일 (월)')],
                    [dict(icon='note', name='집에 오는 길', meta='삼성노트 · 2024년 3월 29일 (금)', lines=['불합격 문자 보고 한참 그냥 걸었다.', '나만 제자리인 것 같아 마음이 무겁다.'])]],
           res_icon='weave', res_head='Weave가 건네는 것', res_lines=['2024년 봄 취업 준비 시기에 작성한 일기 2건을 찾았어요.'],
           res_note='‘우울’이라는 단어가 없어도 찾습니다'),
      dict(tag='기본', title='새집 치수와 손볼 곳', say_label='검색창에 입력', say='새로 이사 갈 집 치수랑 손볼 곳 모아 줘',
           desc='집 보러 간 날의 메모와 중개사 대화를 엮습니다',
           columns=[[dict(icon='cal', name='집 계약 및 내부 확인', meta='캘린더 · 2026년 10월 17일 (토)'),
                     dict(icon='note', name='거실 창가 쪽 메모', meta='삼성노트 · 2026년 10월 17일 (토)', lines=['냉장고 칸 가로 98cm로 쟀다.', '작은방 방충망이 찢어져 있다.'])],
                    [dict(icon='talk', name='김정호 공인중개사', meta='카카오톡 · 2026년 10월 19일 (월)', lines=['집주인분이 입주 전까지 안방', '도배는 새로 해 주기로 했어요'], bubble=True)]],
           res_icon='weave', res_head='Weave가 건네는 것', res_lines=['냉장고 칸은 가로 98cm이고 작은방 방충망 수리가 필요해요.', '안방 도배는 입주 전에 집주인이 해 주기로 했어요.']),
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
           res_icon='weave', res_head='Weave가 건네는 것', res_lines=['작년 10월 검진 소견서 사진을 메일에 첨부했어요.'], res_note='병원 이름이 기억나지 않아도 찾습니다'),
      dict(tag='미래', title='엄마 생신에 갔던 식당', say_label='차에 타서 말로', say='작년 엄마 생신 때 모시고 갔던 식당으로 안내해 줘',
           desc='안부 메시지의 날짜와 메뉴로 결제한 식당을 찾습니다',
           columns=[[dict(icon='talk', name='엄마', meta='카카오톡 · 2025년 10월 18일 (토)', lines=['생일 챙겨 줘서 고맙다 잘 가렴', '오늘 먹은 만두전골 속이 편하더라'], bubble=True)],
                    [dict(icon='wallet', name='윤가네 손만두', meta='삼성 월렛 · 2025년 10월 18일 (토)', lines=['종로구 부암동', '카드 결제 148,000원'])]],
           res_icon='car', res_head='내비게이션이 하는 말', res_lines=['작년 10월 어머니 생신에 다녀오신 종로구 부암동 윤가네 손만두로 안내할게요.'])]
E3 = [dict(tag='기본', title='아빠의 안과 진료일', say_label='계기', say='저녁 퇴근길, 엄마와의 카카오톡 대화창 열기',
           desc='엄마의 부탁과 병원 예약 문자를 연락처로 잇습니다',
           columns=[[dict(icon='talk', name='엄마', meta='카카오톡 · 2026년 11월 8일 (일)', lines=['날 추워지는데 감기 조심해라', '아빠 안과 예약 잡히면 알려 주렴'], bubble=True)],
                    [dict(icon='msg', name='새한병원', meta='메시지 · 2026년 11월 16일 (월)', lines=['김영수님 망막 진료 예약 완료', '11월 21일(토) 10시 30분'], bubble=True)]],
           res_icon='weave', res_head='Weave가 건네는 것', res_lines=['아빠 안과 예약은 11월 21일 토요일 10시 30분으로 잡았어요'], res_note='키보드 위에 보낼 말로 제안합니다'),
      dict(tag='미래', title='남편 생일 미역국', say_label='계기', say='남편 생일 하루 전, 일요일 저녁',
           desc='생일 일정과 남편의 말, 냉장고 속 재료를 잇습니다',
           columns=[[dict(icon='cal', name='남편 생일', meta='캘린더 · 내일, 11월 16일 (월)'), dict(icon='fridge', name='보관 중인 식재료', meta='냉장고 · 오늘', lines=['건미역 있음, 국간장 있음', '국거리 소고기 없음'])],
                    [dict(icon='talk', name='남편', meta='카카오톡 · 10월 18일 (일)', lines=['나 이번 생일엔 다른 거 말고', '자기가 끓여준 소고기 미역국 먹고 싶어'], bubble=True)]],
           res_icon='fridge', res_head='냉장고가 먼저 건네는 말', res_lines=['내일은 남편분 생일이에요.', '미역국에 넣을 국거리 소고기를 준비해 볼까요?']),
      dict(tag='미래', title='알림장의 체육복', say_label='계기', say='수요일 저녁, 빨래 돌리기 전',
           desc='알림장의 준비물 안내를 전날 저녁에 챙깁니다',
           columns=[[dict(icon='school', name='2학년 3반 주간 안내', meta='알림장 · 11월 16일 (월)', lines=['목요일 3교시는 강당 체육 활동입니다.', '아이들 동복 체육복 꼭 챙겨 입혀 보내주세요.'])],
                    [dict(icon='washer', name='세탁 기록', meta='세탁기 · 11월 14일 (토)', lines=['주간 의류 세탁 후 4일 경과'])]],
           res_icon='washer', res_head='세탁기가 먼저 건네는 말', res_lines=['내일 학교 체육 수업에 체육복이 필요해요.', '오늘 저녁 세탁할 때 체육복도 함께 돌릴까요?'], res_note='알림장은 서드파티 앱의 알림으로 읽습니다')]


def s_e1():
    return page('qe_ux1', 'E-1', [('UX1 기록 통합 검색: 시나리오 더 보기', INK)], E1)


def s_e2():
    return page('qe_ux2', 'E-2', [('UX2 단서로 찾는 기억: 시나리오 더 보기', INK)], E2)


def s_e3():
    return page('qe_ux3', 'E-3', [('UX3 먼저 건네는 기억: 시나리오 더 보기', INK)], E3)


CARBON = '장면의 글은 Carbon(Gemini)이 썼음(11-15에 사용자의 씨앗 여섯을 다듬었고, 11-16에 장마다 셋째 장면을 새로 씀).'
PAGES = [
    Page('E-1', 'UX1 시나리오 더 보기', s_e1,
         q='기록 통합 검색은 다른 어떤 상황에서 쓰나요?',
         a='세 가지를 준비했습니다. 첫째는 취업 준비 때 우울할 때마다 썼던 일기를 찾는 장면입니다. 캘린더의 공채 일정과 삼성노트의 일기를 함께 읽어, '
           '취업 준비 시절 마음이 힘들 때 남긴 글만 모아 보여 줍니다. '
           '둘째는 이사 갈 집을 보고 온 뒤입니다. 캘린더의 계약 일정으로 집을 보러 간 날짜를 찾고, 당일에 적어 둔 치수 메모와 공인중개사의 카카오톡 안내를 한데 모아 요약해 줍니다. '
           '셋째는 요리하다가 손을 쓸 수 없을 때입니다. 엄마가 알려 준 갈비찜 양념 비율을 Bixby에게 물으면, 삼성노트에 적어 둔 레시피와 냉장고 속 식재료를 함께 확인해 '
           '양념 비율은 물론 부족한 배까지 음성으로 알려 줍니다.',
         more=[('일기에 우울이라는 말이 없으면요?', '찾습니다. 예시의 일기에는 우울이라는 단어가 없고 마음이 무겁다고만 적혀 있습니다.'),
               ('일기처럼 민감한 기록도 다 읽나요?', '어느 앱을 색인할지는 사용자가 정합니다. 읽은 것은 기기 밖으로 나가지 않습니다.'),
               ('냉장고의 재료는 어떻게 아나요?', '2026년형 패밀리허브의 AI 비전이 알아보는 재료를 SmartThings로 받는 것을 전제로 한 미래 장면입니다.')],
         basis=[CARBON + ' 일기 장면은 1안에서 캘린더와 일기 하나를 썼고, 입력하는 말은 사용자의 씨앗에 가깝게 ‘취업 준비 때 우울할 때마다 썼던 일기’로 함(Carbon의 안은 ‘취준할 때 우울해서 썼던 일기들’). 캘린더 카드의 본문 ‘오후 5시 최종 제출 잊지 말기’는 뺌.',
                '이사 장면은 11-16의 후보 1-A 그대로. 제목만 칸 폭에 맞춰 ‘이사 갈 집 치수와 수리’ → ‘새집 치수와 손볼 곳’. 고르지 않은 후보 1-B는 Galaxy Watch가 달리기 전에 무릎 주의사항을 알려 주는 미래 장면.',
                '갈비찜 장면은 1안 그대로. 설 연휴(2026년 2월 16~18일) 전날인 2월 15일의 메모.',
                '날짜와 요일: 2024-03-18 월, 2024-03-29 금, 2026-02-15 일, 2026-10-17 토, 2026-10-19 월.']),
    Page('E-2', 'UX2 시나리오 더 보기', s_e2,
         q='단서로 찾는 기억은 글자만 찾아 주나요? 사진이나 파일도 되나요?',
         a='사진과 파일도 되고, 휴대폰 밖에서도 됩니다. 첫째는 카카오톡 대화 중에 ‘눈 오던 날 팔공산에서 신나게 논 사진’이라고 입력하고 실타래 버튼을 누른 경우입니다. '
           '친구와 나눈 카카오톡으로 팔공산에 간 날짜를 찾고, 갤러리에서 눈 배경과 밝은 표정의 사진을 골라 대화창에 바로 첨부합니다. '
           '둘째는 메일을 쓰면서 작년에 다른 병원에서 받은 건강검진 소견서를 찾는 장면입니다. '
           '검진센터 안내 문자의 날짜와 갤러리의 문서 사진을 엮어 소견서를 메일에 곧바로 넣어 줍니다. '
           '셋째는 차 안입니다. 식당 이름이 기억나지 않아도 어머니의 카카오톡에서 생신 날짜와 메뉴 단서를 찾고, 삼성 월렛의 당일 결제 내역과 이어 내비게이션 목적지로 바로 설정합니다.',
         more=[('사진의 표정이나 배경은 어떻게 아나요?', '색인할 때 사진을 벡터로 바꿔 둡니다. EmbeddingGemma 2는 글과 사진을 같은 공간에 놓기 때문에 ‘눈’, ‘웃는 모습’ 같은 말로 사진을 찾습니다.'),
               ('엉뚱한 사진을 보내면요?', '바로 보내지 않고 입력 칸에 첨부만 합니다. 보내기는 사용자가 누릅니다.'),
               ('차에서는 어떻게 동작하나요?', '검색은 휴대폰이 하고, 찾은 식당의 이름과 주소만 차의 내비게이션에 건넵니다. 35쪽의 가전 연동과 같은 방식입니다.')],
         basis=[CARBON + ' 팔공산 장면은 입력하는 말과 결과는 1안, 카카오톡은 2안(이름 동현. 1안의 민수는 UX1의 민수님과 겹침). 갤러리 이름은 카드 폭에 맞춰 줄임(‘눈 내리는 산길에서 환하게 웃는 모습’ → ‘눈길에서 환하게 웃는 모습’, ‘눈 쌓인 정상 표지석 앞 브이 포즈’ → ‘정상 표지석 앞 브이’).',
                '건강검진 장면은 2안(안내 문자와 문서 사진). 1안의 파일 이름 ‘종합검진_소견서_스캔본.pdf’는 단어가 겹쳐 한 번의 검색으로 찾아지므로 쓰지 않음. 입력하는 말은 ‘병원서’를 ‘병원에서’로.',
                '식당 장면은 11-16의 후보 2-A. 가게 이름은 실제 가게(자하손만두)여서 지어낸 이름 ‘윤가네 손만두’로 바꾸고 주소는 ‘종로구 부암동’까지만 적음(본 발표가 실제 쇼핑몰 대신 지어낸 ‘새봄몰’을 쓴 것과 같은 까닭). 화면 설명의 ‘안부 카톡’ → ‘안부 메시지’. 고르지 않은 후보 2-B는 노트북에서 출장 숙소비를 채우는 장면.',
                '날짜와 요일: 2025-01-11 토, 2025-10-24 금, 2025-10-18 토. 병원과 가게 이름은 지어낸 이름.']),
    Page('E-3', 'UX3 시나리오 더 보기', s_e3,
         q='먼저 건네는 기억은 공항 말고 어떤 상황이 있나요?',
         a='세 장면입니다. 첫째는 휴대폰에서입니다. 퇴근길에 어머니와의 카카오톡을 열면, 지난주 어머니가 부탁한 안과 예약 메시지와 '
           '오늘 받은 아버지 성함의 망막 진료 문자를 연락처로 묶어 보낼 답장을 키보드 위에 먼저 제안합니다. '
           '나머지 둘은 집 안 기기와 이어지는 장면입니다. 남편의 생일 전날에는 캘린더의 생일 일정과 지난달 남편의 카카오톡, 냉장고 재료 상태를 이어 '
           '부족한 미역국 재료를 냉장고가 먼저 챙겨 줍니다. 아이의 체육 수업 전날 저녁에는 학교 알림장의 준비물 안내를 읽고 세탁기가 체육복 세탁을 먼저 챙겨 줍니다. '
           '가전 장면에서도 기억을 찾는 일은 휴대폰이 하고, 가전은 답을 건네는 자리입니다.',
         more=[('병원 문자의 이름이 아버지인 줄은 어떻게 아나요?', '색인할 때 연락처와 맞춰 봅니다. 연락처의 아빠가 김영수라는 이름과 묶여 있어서 병원 문자의 이름을 아버지로 알아봅니다.'),
               ('망막 진료가 안과 예약인 줄은 어떻게 아나요?', '단어는 다르지만 망막 진료가 안과에서 받는 진료라는 상식으로 이어집니다. Reasoning Embedding이 맡는 연결이고 D-5에 정리했습니다.'),
               ('냉장고가 재료를 정확히 알아야 하지 않나요?', '재료를 모를 때는 생일과 부탁만 알려 줍니다. 재료는 냉장고가 알아보는 범위에서만 더합니다.'),
               ('가족이 함께 보는 화면에 개인 대화가 뜨면 곤란하지 않나요?', '가전에는 찾아낸 답만 건네고 대화 원문은 건네지 않습니다. 누구에게 보여 줄지는 Voice ID로 본인이 확인됐을 때로 한정합니다.'),
               ('알림장 같은 서드파티 앱은 어떻게 읽나요?', '카카오톡과 같습니다. 사용자가 허용한 알림으로 읽습니다.')],
         basis=[CARBON + ' 진료일 장면은 11-16의 후보 3-B. 병원 이름은 실제 병원(서울성모병원)이어서 지어낸 이름 ‘새한병원’으로 바꿈. 제목은 칸 폭에 맞춰 ‘엄마에게 알릴 아빠 진료일’ → ‘아빠의 안과 진료일’. 건네는 것은 ‘…를 보낼까요?’ 꼴을 빼고 보낼 말만 적음(본 발표 19쪽의 자동 완성 추천과 같은 꼴). 고르지 않은 후보 3-A는 출장지 건물에서 렌터카 번호를 건네는 장면.',
                '미역국 장면은 1안. 카카오톡 끝의 ‘(웃는 얼굴)’은 그림이 없어 뺌. 체육복 장면은 1안. 세탁기 기록 카드(‘주간 의류 세탁 후 4일 경과’)는 11-15에 뺐다가 11-16에 기록 두 칸을 맞추려고 다시 넣음(이름 ‘세탁 기록’과 날짜는 내가 붙임).',
                '날짜와 요일: 2026-11-08 일, 2026-11-16 월, 2026-11-21 토, 2026-10-18 일, 2026-11-14 토(체육 수업은 11-19 목, 계기는 11-18 수).',
                '가전 장면은 35쪽(미래의 Weave)의 SmartThings 연동을 전제로 함.']),
]
