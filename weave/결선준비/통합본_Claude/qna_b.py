"""Appendix B 묶음(상품화와 사업성)의 장과, D 묶음으로 옮긴 메모리와 속도 세 장 (11-16 4판, 13차 11-17에 다시 묶음).

13차(사용자의 지시): '상품화 부분의 1, 2, 3은 D로 옮기고, 4, 5는 데이터와 사업과 합쳐 줘. 합친 카테고리 제목을 새롭게'.
  B 상품화와 사업성: B-1 사용자 설문조사 결과(새 장), B-2 사업 효과, B-3 1년 상품화 계획(다시 씀), B-4 가전과 TV로의 확장,
                    B-5 왜 온디바이스인가(팀원 ysy19의 apx_new.s_ondevice), B-6 읽을 수 있는 기록의 범위, B-7 카카오톡 같은 외부 앱의 대화를 읽는 방법, B-8 데이터 접근 권한과 사생활 보호
  D 모델과 성능, Query Rewriter(이 파일에 있는 것): D-2 메모리와 저장 공간, D-3 속도 1(검색 시간과 기준 모델), D-4 속도 2(UX별 응답 시간). D-1은 qna_d.py
차례는 왜 필요한가(설문, 사업 효과) → 어떻게 내놓는가(1년 계획, 가전으로의 확장) → 무엇을 전제로 하는가(온디바이스, 읽는 범위, 카카오톡, 권한).
11차의 코드와의 짝: B-1 → D-2, B-2 → D-3, B-3 → D-4, B-4 → B-3, B-5 → B-4, B-6 → B-5, B-7 → B-6, B-8 → B-7, B-9 → B-8, B-10 → B-2.
13차에 고친 것: 1년 계획 장은 UX를 차례로 켜는 그림을 버리고 분기별로 데이터, 모델, 평가, UX와 통합, 검증과 출시에서 할 일을 적음.
  메모리 장에 Query Rewriter를 전용 모델로 따로 두는 구성을 더함. 속도 장 둘에서 FunctionGemma를 뺌(구성은 기준 속도와 Gemma 3 1B 실측 둘).
  설문 장은 210명의 응답을 CSV에서 다시 집계해 한 장에 그림(11차의 '직접 측정하거나 확인한 것' 장을 빼고 넣음).
시간은 `qna_num.py`가 셈한다. 근거는 `Appendix_QnA_대본.md`.
"""
from pathlib import Path

from ui import (BODY, INK, LAV, LAV2, MUTE, PURPLE, PURPLE2, RING, SUB, C, R, T, chip, tw)

import qna_num as NUM
from qna_lib import (BAR_SOFT, GRAY_BG, Page, arrow, box, data_row, footnote, frame, hbars, label, lh_of, notes3, page_slide, panel, pipeline, points, qrow, rich,
                     ring_gauge, rwrap, tbl, timebar, vis_bars, vis_nums, vis_rows, vis_steps, vis_text, wrapl)

HERE = Path(__file__).resolve().parent
X, W = 70, 1140


# ------------------------------------------------------------------ D-2 메모리와 저장 공간
RAM, GAUSS, ADD = 12.0, 3.0, 0.25             # GB: Galaxy S26 Ultra, Gauss 3B 8bit의 가중치(30억 × 1바이트), Weave가 추가로 사용하는 것(임베딩 0.19 + 색인 0.026 + Adapter 수십 MB)
QR_OWN = (0.5, 1.0)                           # GB: Query Rewriter를 1B급 전용 모델로 따로 둘 때(10억 파라미터 × 4bit ~ 8bit로 셈한 가중치)
ADD_OWN = (0.19 + 0.026 + QR_OWN[0], 0.19 + 0.026 + QR_OWN[1])      # 그때 추가로 사용하는 메모리: 0.72 ~ 1.22GB
# 13차(11-17) 'Query Rewriter를 Adapter 말고도 쓸 수도 있을 것 같은데, 만약 쓰게 되면 추가해 줘': 표의 Query Rewriter를 두 줄로(기본 구성과 전용 모델)
B1 = [['Reasoning Embedding', '약 0.19GB', 'EmbeddingGemma 2의 텍스트 구성을 Pixel 11 Pro에서 잰 값(191MB)¹. 사진 내용까지 색인하는 전체 구성은 약 0.57GB이고, 충전 중에 색인할 때만 올림'],
      ['벡터 색인 (Vector Index)', '26MB²', '기록 10만 건 기준 (256-dim int8, 기록 하나에 256바이트). 저장 공간에 두고 필요한 부분만 메모리에 올림'],
      [['Query Rewriter', '기본: Gauss + LoRA Adapter'], '수십 MB³', '검색 계획 생성을 튜닝한 Adapter를 Gauss에 얹음. 기능마다 갈아 끼움. 튜닝 전에는 프롬프트만으로 시작할 수 있고 그때는 추가 메모리가 없음'],
      [['Query Rewriter', '전용 모델로 따로 둘 때'], '약 0.5~1GB⁶', '1B급 모델을 통째로 튜닝해 따로 올리는 구성. Gauss가 없는 기기에서도 쓸 수 있고, Gauss를 올리지 않고 검색 계획만 만들 수 있음. 모델 하나를 더 관리해야 함'],
      ['sLLM (Samsung Gauss 3B)', '추가 없음', '기기에 탑재된 Gauss 3B(8bit)를 공유. 가중치는 30억 파라미터 × 8bit로 약 3GB⁴']]
B1_ST = [['벡터 색인의 크기 (저장 공간)²', '26MB', '256MB', '2.56GB'], ['하루 1,000건씩 쌓일 때 걸리는 기간', '약 100일', '약 2년 9개월', '약 27년']]


def s_mem():
    s = page_slide('qb_mem', 'D-2', [('메모리와 저장 공간', INK)])
    y, h = 100, 44
    wa = round(ADD / RAM * W)
    wg = round(GAUSS / RAM * W)
    wr = W - wa - wg - 8
    s.add('qb/m', [R('qb/m/rest', X, y, wr, h, prst='roundRect', radius=10, fill='EFECF4', line=None),
                   T('qb/m/rest/t', X + 18, y, wr - 36, h, '시스템과 다른 앱', size=12, color=SUB, anchor='ctr'),
                   R('qb/m/gauss', X + wr + 4, y, wg, h, prst='roundRect', radius=10, fill=LAV, line=RING, line_w=1.2),
                   T('qb/m/gauss/t', X + wr + 4, y, wg, h, '탑재된 sLLM: Gauss 3B (8bit), 약 3GB⁴', size=11, color=PURPLE, weight='b', align='c', anchor='ctr'),
                   R('qb/m/add', X + W - wa, y, wa, h, prst='roundRect', radius=7, fill=PURPLE, line=None),
                   C('qb/m/lead', [(X + W - wa / 2, y + h + 2)] * 2 + [(X + W - wa / 2, y + h + 14)] * 2, color=PURPLE, w=1.6),
                   T('qb/m/add/t', X + W - 640, y + h + 12, 640, 26, [[('Weave가 추가로 사용하는 메모리 ', dict(color=INK)), ('약 0.25GB', dict(color=PURPLE)), (' (12GB의 2%)', dict(color=INK))]],
                     size=14, weight='b', align='r', anchor='ctr'),
                   T('qb/m/all', X, y + h + 12, 400, 26, 'Galaxy S26 Ultra의 메모리 12GB⁵', size=11.5, color=SUB, anchor='ctr')])
    s.add('qb/m/own', [T('qb/m/own', X + W - 640, y + h + 38, 640, 18, '기본 구성(Gauss + Adapter) 기준. Query Rewriter를 전용 모델로 따로 두면 약 %.1f~%.1fGB (12GB의 %d~%d%%)'
                         % (ADD_OWN[0], ADD_OWN[1], round(ADD_OWN[0] / RAM * 100), round(ADD_OWN[1] / RAM * 100)), size=10.5, color=SUB, align='r', anchor='ctr')])
    y += h + 12 + 26 + 18 + 8
    y += tbl(s, 'qb/t', X, y, W, [22, 13, 65], ['구성 요소', '메모리', '설명'], B1, pady=6, pt=11.5, hi=(0, 1, 2), head_h=30) + 12
    y += label(s, 'qb/l2', X, y, '기록이 쌓일 때의 저장 공간') + 4
    y += tbl(s, 'qb/t2', X, y, W, [35, 21, 22, 22], ['', '10만 건', '100만 건', '1,000만 건'], B1_ST, pady=6, pt=11.5, hi=(0,), head_h=30) + 10
    footnote(s, ['¹ Google, "EmbeddingGemma 2" (2026. 10): Pixel 11 Pro에서 텍스트 가중치 약 191MB, 전체 약 567MB   ³ Apple, On-Device Foundation Models (2024. 06): Adapter 하나는 수십 MB',
                 '² 256-dim int8 벡터로 셈한 값. 원문은 각 앱에 그대로 있고 색인에는 벡터와 메타데이터만 둠   ⁴ 30억 파라미터 × 1바이트로 셈한 가중치의 크기   '
                 '⁵ 256GB와 512GB 모델은 12GB, 1TB 모델은 16GB   ⁶ 10억 파라미터 × 4bit~8bit로 셈한 가중치의 크기'], y)
    return s


# ------------------------------------------------------------------ D-3 속도 ①: 검색 시간과 기준 모델
def _tok(v):
    return '초당 %d토큰' % round(v)


def vis_hop():
    """qrow의 그림: Hop 1회의 내역(가로 막대 셋)과 합계."""
    items = [('질의 임베딩 (NPU 실측)', 8, '8ms', True), ('벡터 검색 (10만 건에서 %d건)' % NUM.TOPK, 10, '10ms', False), ('필터링, Slot 채우기', 2, '2ms', False)]

    def draw(x, y, w, h):
        bars, bh = hbars('vh', x + 16, 0, w - 32, items, vmax=13, pt=10.5, bar_h=13, gap=7)
        top = y + (h - (20 + 6 + bh)) / 2
        bars, _ = hbars('vh', x + 16, top + 26, w - 32, items, vmax=13, pt=10.5, bar_h=13, gap=7)
        return [T('vh/t', x + 16, top, w - 32, 20, 'Hop 1회 = 8 + 10 + 2 = 약 0.02초', size=10.5, color=INK, weight='b', anchor='ctr')] + bars
    return draw


B2_MODELS = [['EmbeddingGemma 2 (텍스트 2.7억)', 'Galaxy S26 Ultra', '모델 카드: GPU 25.9ms, CPU 27.1ms¹', ('**NPU 실측 8ms** (GPU의 %.1f배, CPU의 %.1f배)' % (NUM.R_GPU, NUM.R_CPU), dict(color=INK))],
             ['Gemma 4 E2B', 'Galaxy S26 Ultra GPU', '출력 ' + _tok(NUM.E2B.dec) + '²', ('**기준 속도**: NPU 환산 %s (× %.1f)' % (_tok(NUM.E2B.dec_npu), NUM.R_GPU), dict(color=INK))],
             ['Gemma 3 1B', 'Galaxy S25 Ultra NPU', '출력 ' + _tok(NUM.G1B.dec) + '²', 'NPU 실측 그대로 ' + _tok(NUM.G1B.dec_npu)]]
B2_SCALE = [['Hop 1회 (휴대폰 기준으로 잡은 값)', '약 0.01초', '0.02초', '약 0.11초'],
            ['벡터 검색만, PC에서 직접 잰 값³', '%.1fms' % NUM.PC_SEARCH_MS[10_000], '%.1fms' % NUM.PC_SEARCH_MS[100_000], '%.0fms' % NUM.PC_SEARCH_MS[1_000_000]],
            ['벡터 색인의 크기', '2.6MB', '26MB', '256MB']]


def s_speed():
    s = page_slide('qb_speed', 'D-3', [('속도 1: 검색 시간과 기준 모델', INK)])
    y, h = 96, 168
    qrow(s, 'qb/q1', y, h, '기록을 전부 LLM에게 읽히면 되지 않나요? 왜 임베딩으로 찾나요?',
         'LLM은 토큰마다 연산해서 수만 건의 기록을 질의마다 읽기 어렵습니다. 임베딩은 기록마다 한 번만 미리 계산해 두고, 질의가 오면 벡터끼리만 비교합니다. '
         '기록 10만 건에서 가까운 %d건을 고르는 **Hop 1회가 0.02초**입니다.' % NUM.TOPK,
         vis=vis_hop(), vw=430)
    y += h + 10
    y += label(s, 'qb/l3', X, y, '기록 수에 따른 검색 시간과 색인 크기') + 2
    y += tbl(s, 'qb/t', X, y, W, [37, 21, 21, 21], ['', '1만 건', '10만 건', '100만 건'], B2_SCALE, pady=5, pt=11.5, hi=(0,), head_h=28) + 10
    y += label(s, 'qb/l0', X, y, 'sLLM의 시간을 셈한 기준 모델 (Samsung Gauss는 공개된 속도가 없어 같은 크기의 공개 모델로 셈함)') + 2
    y += tbl(s, 'qb/tm', X, y, W, [26, 20, 26, 28], ['모델', '측정한 기기', '공개 측정값', 'NPU 기준'], B2_MODELS, pady=6, pt=11.5, hi=(0, 1), head_h=28) + 10
    footnote(s, ['¹ litert-community/embeddinggemma-2-text-270m-litert-lm 모델 카드 (128토큰, 5회 평균). 8ms는 같은 모델을 양자화해 팀이 잰 값   ² LiteRT-LM 모델 카드의 공개 측정값',
                 '³ %s, 코어 1개, 256-dim int8 벡터를 모두 비교해 상위 %d건을 고르는 시간 (30회의 중앙값, 11월 16일 측정). 휴대폰은 그 두 배인 10ms로 잡음'
                 % ('Intel Core i7-1360P', NUM.TOPK),
                 'NPU 환산: EmbeddingGemma 2가 같은 기기의 GPU보다 NPU에서 %.1f배 빨랐던 비율을, GPU에서 잰 Gemma 4 E2B의 값에 곱함' % NUM.R_GPU], y)
    return s


# ------------------------------------------------------------------ D-4 속도 ②: UX별 응답 시간
def _bars(ux, names, texts, total, pins=()):
    rw, se, an = NUM.BAR[ux]
    return [(names[0], rw, texts[0], 'gen'), (None, se, '', 'emb'), (names[1], an, texts[1], 'gen')], total, pins


UXT = [('UX2 단서로 찾는 기억',) + _bars('ux2', ('재작성', '답변'), (NUM.T_RW2, NUM.T_AN2), NUM.T_UX2),
       ('UX1 기록 통합 검색',) + _bars('ux1', ('재작성', '요약'), (NUM.T_RW1, NUM.T_AN1), NUM.T_UX1, [(1, '찾은 기록을 먼저 표시: ' + NUM.T_REC1)]),
       ('UX3 먼저 건네는 기억',) + _bars('ux3', ('재작성', '제안'), (NUM.T_RW3, NUM.T_AN3), NUM.T_UX3 + ' (백그라운드)')]
# 13차: 구성이 둘(Query Rewriter와 답변 생성에 같은 모델)로 줄어 두 칸에 같은 이름이 놓이던 것을 모델, 속도의 근거, 측정한 기기로 바꿈
B3_CONF = [[rw.name, '기준 속도 (NPU 환산)' if rw is NUM.REF else rw.kind, '%s %s' % (rw.dev, rw.proc), NUM.sec(NUM.TOT['ux2'][i]),
            '%s (기록은 %s)' % (NUM.sec(NUM.TOT['ux1'][i]), NUM.sec(NUM.REC1[i])), NUM.sec(NUM.TOT['ux3'][i])]
           for i, (rw, an) in enumerate(NUM.CONFIGS)]


def s_uxtime():
    s = page_slide('qb_uxt', 'D-4', [('속도 2: UX별 응답 시간', INK)])
    y = 98
    y += label(s, 'qb/l2', X, y, '질의부터 답까지 (보라: sLLM 생성, 파랑: 검색 %d~%d회)' % (2, 3)) + 10
    span_ = NUM.UX1_T[1] * 1.42
    for i, (name, segs, total, pins) in enumerate(UXT):
        y += timebar(s, 'qb/tb%d' % i, X, y, W, segs, total, title=name, title_w=176, span=span_, total_w=10, pt=10.5, pins=pins) + 14
    y += 4
    y += label(s, 'qb/l4', X, y, '기준 모델별 응답 시간 (3줄 요약은 80토큰 기준)') + 4
    y += tbl(s, 'qb/tc', X, y, W, [17, 19, 20, 11, 22, 11], ['sLLM의 기준 모델', '속도의 근거', '공개 측정값을 잰 기기', 'UX2', 'UX1', 'UX3'], B3_CONF, pady=8, hi=(0,), pt=11.5) + 16
    y += points(s, 'qb/p', X, y, W, ['**시간은 sLLM이 출력하는 토큰 수에 달려 있습니다.** 기준 속도는 출력 %s입니다. 검색 계획 40~100토큰은 %s, 이름 추출 10토큰은 %s, 3줄 요약 80~150토큰은 %s입니다.'
                                    % (_tok(NUM.REF.dec_npu), NUM.T_RW, NUM.T_AN2, NUM.T_AN1),
                                    '**검색은 시간을 거의 쓰지 않습니다.** 3-hop이어도 0.06초입니다. Hop이 하나 늘면 검색 0.02초와 계획 10토큰쯤(약 0.06초)이 늘어납니다.',
                                    '**발열과 배터리 부담도 줄였습니다.** sLLM은 질의마다 두 번만 실행하고 합쳐서 250토큰 안쪽만 생성합니다. 대량 색인은 충전 중에 실행합니다. (B-8)'], gap=7, pt=12) + 10
    footnote(s, '기준 속도는 Gemma 4 E2B의 공개 측정값을 NPU 기준으로 환산한 값(D-3). 표의 둘째 줄은 Gemma 3 1B를 Galaxy S25 Ultra의 NPU에서 잰 공개 측정값 그대로임.', y)
    return s


# ------------------------------------------------------------------ B-1 사용자 설문조사 결과 (13차에 새로 넣음)
# 13차(11-17): '설문조사 결과를 한눈에 시각화한 페이지를 하나 만들면 좋을 것 같아'(11차의 '직접 측정하거나 확인한 것' 장 대신).
#   숫자는 12_설문의 CSV(210명)를 문항마다 다시 집계한 값(11-17). 복수 선택 문항은 ';'로 나눠 셈. 비율은 전체 210명 기준(본 발표 7쪽과 33쪽의 93.8%, 83.8%, 82.4%와 같은 분모)이고,
#   94.9%만 본 발표 8쪽과 같이 6번에 예라고 답한 197명 기준.
#   짜임: 조사 개요 한 줄 → 불편 넷(고리 그래프: 본 발표 7쪽, 33쪽과 같은 모양) → 아래 세 칸(남기는 곳, 대신 기억나는 것, 지금 찾는 방법과 쓰겠다는 조건).
SV_PAIN = [(89.5, 188, ['바로 찾지 못해', '“찾아보고 다시 알려 줄게”라고 했다'], '발표 첫 장면의 통화'),
           (83.8, 176, ['어느 앱에 남겼는지 몰라', '앱을 하나씩 열어 봤다'], 'UX1 기록 통합 검색'),
           (93.8, 197, ['정확한 이름이 떠오르지 않아', '검색으로 찾지 못했다'], 'UX2 단서로 찾는 기억'),
           (82.4, 173, ['챙겨야 할 부탁이나 약속을', '나중에야 떠올렸다'], 'UX3 먼저 건네는 기억')]
SV_SAVE = [('화면 캡처', 76.7), ('카카오톡 ‘나와의 채팅’', 75.7), ('메모 앱', 65.2), ('사진 촬영', 59.5), ('캘린더', 53.3), ('지도 앱에 저장', 25.7), ('이메일', 14.8)]
# (이름, 비율, 내용으로 찾는 단서인지): 날짜, 장소, 사람은 색인의 메타데이터로 거르고(C-4) 상황, 모습, 대화는 Reasoning Embedding이 찾음
SV_CLUE = [('언제였는지', 59.0, False), ('어디였는지', 57.1, False), ('어떤 상황이었는지', 48.6, True), ('관련된 사람', 47.6, False), ('눈으로 본 모습', 39.5, True), ('주고받은 대화 일부', 36.2, True)]
SV_USE = [('휴대폰 안에서만 처리된다면 쓰겠다', 80.5, PURPLE), ('서버로 보내져도 쓰겠다', 12.4, 'B9A6FF'), ('쓰지 않겠다', 7.1, 'D8D3E3')]
SV_SRC = "스마트폰 내 개인 기록 탐색 및 재검색 행태에 관한 자체 설문조사 (응답자 210명, '26.11)"


def s_survey():
    s = page_slide('qb_survey', 'B-1', [('사용자 설문조사 결과', INK)])
    y = 96
    # 조사 개요 한 줄
    meta = [('응답자', '210명'), ('기간', '2026. 10. 28 ~ 11. 04 (온라인)'), ('기기', 'Galaxy 145명, iPhone 62명, 그 외 3명'), ('연령', '20대 이하 73명, 30대 47명, 40대 5명, 50대 이상 85명')]
    runs = []
    for k, (a, b) in enumerate(meta):
        runs += [(('      ' if k else '') + a + '  ', dict(color=PURPLE, weight='b')), (b, dict(color=BODY))]
    s.add('qb/sv/meta', [R('qb/sv/meta/bg', X, y, W, 32, prst='roundRect', radius=10, fill=GRAY_BG, line=None),
                         T('qb/sv/meta/t', X + 18, y, W - 36, 32, [runs], size=11.5, anchor='ctr')])
    y += 32 + 12
    # 불편 넷: 고리 그래프(가운데에 비율과 사람 수), 그 불편을 맡는 기능, 문항
    n, gap, ch, ro = 4, 14, 176, 39
    cw = (W - gap * (n - 1)) / n
    lh = lh_of(11.5, 1.4)
    for i, (pct, cnt, tl, tagt) in enumerate(SV_PAIN):
        cx = X + i * (cw + gap)
        mx, cy = cx + cw / 2, y + 42 + ro
        k = 'qb/sv/p%d' % i
        c, _ = chip(k + '/tag', mx, y + 12, tagt, 'soft', pt=9.5, h=20, padx=9, align='c')
        assert all(tw(t, 11.5, 'm') <= cw - 28 for t in tl), tl
        s.add(k, [box(k + '/bg', cx, y, cw, ch, radius=16, shadow=False)] + c + ring_gauge(k + '/r', mx, cy, ro, pct) +
              [T(k + '/n', mx - ro, cy - 17, 2 * ro, 24, '%.1f%%' % pct, size=14.5, color=PURPLE, weight='b', align='c', anchor='ctr'),
               T(k + '/c', mx - ro, cy + 6, 2 * ro, 14, '%d명' % cnt, size=9, color=MUTE, align='c', anchor='ctr'),
               T(k + '/t', cx + 16, y + 42 + 2 * ro + 9, cw - 32, lh * len(tl) + 4, tl, size=11.5, color=INK, weight='m', align='c', lnspc=lh * 0.75)])
    y += ch + 9
    y += rich(s, 'qb/sv/all', X, y, W, '넷 가운데 하나라도 겪은 사람은 **209명 (99.5%)**, 세 UX가 겨냥한 불편 셋을 모두 겪은 사람은 **150명 (71.4%)**', pt=11.5, color=BODY, align='c') + 11
    # 아래 세 칸
    ws = [372, 384, W - 372 - 384 - 2 * gap]
    xs = [X, X + ws[0] + gap, X + ws[0] + ws[1] + 2 * gap]
    ph = 300
    clh = lh_of(11, 1.45)

    def card(key, px, py, pw, hh, title):
        return [box(key + '/bg', px, py, pw, hh, radius=16, shadow=False),
                T(key + '/t', px + 18, py + 12, pw - 36, 22, title, size=12.5, color=PURPLE, weight='b', anchor='ctr')]

    def caption(key, px, py, pw, hh, text):
        cl = rwrap(text, 11, pw - 36)
        return [T(key, px + 18, py + hh - 14 - clh * len(cl), pw - 36, clh * len(cl) + 4, cl, size=11, color=BODY, lnspc=clh * 0.75)]
    # ① 기록을 남기는 곳
    px, pw = xs[0], ws[0]
    bars, _ = hbars('qb/sv/b0', px + 18, y + 48, pw - 36, [(nm, v, '%.1f%%' % v, j < 2) for j, (nm, v) in enumerate(SV_SAVE)], vmax=100, pt=11, bar_h=13, gap=9, val_w=50)
    s.add('qb/sv/c0', card('qb/sv/c0', px, y, pw, ph, '기록을 남기는 곳 (복수 선택)') + bars +
          caption('qb/sv/c0/cap', px, y, pw, ph, '한 사람이 평균 **3.8곳**에 나눠 남깁니다. 세 곳 이상에 남기는 사람이 **74.8%**입니다.'))
    # ② 이름 대신 기억나는 것: 내용으로 찾는 단서는 진한 막대, 메타데이터로 거르는 단서는 옅은 막대
    px, pw = xs[1], ws[1]
    lg = []
    lx = px + 18
    for col, lab in ((BAR_SOFT, '메타데이터 필터'), (PURPLE, 'Reasoning Embedding')):
        lg += [R('qb/sv/lg%s' % col, lx, y + 46, 10, 10, prst='roundRect', radius=3, fill=col, line=None),
               T('qb/sv/lgt%s' % col, lx + 15, y + 41, 220, 20, lab, size=9.5, color=SUB, anchor='ctr')]
        lx += 15 + tw(lab, 9.5) + 18
    assert lx - 18 <= px + pw - 14, '범례가 칸을 넘침 (%d > %d)' % (lx - 18, px + pw - 14)
    bars, _ = hbars('qb/sv/b1', px + 18, y + 72, pw - 36, [(nm, v, '%.1f%%' % v, hi) for nm, v, hi in SV_CLUE], vmax=100, pt=11, bar_h=13, gap=7, val_w=50)
    s.add('qb/sv/c1', card('qb/sv/c1', px, y, pw, ph, '이름 대신 기억나는 것 (복수 선택, 평균 2.9개)') + lg + bars +
          caption('qb/sv/c1/cap', px, y, pw, ph, '날짜, 장소, 사람은 **메타데이터 필터**로 거르고 상황, 모습, 대화는 **Reasoning Embedding**으로 찾습니다. (C-4)'))
    # ③ 지금 찾는 방법 / AI가 찾아 준다면
    px, pw = xs[2], ws[2]
    h1 = 132                                 # 94.9%는 본 발표 8쪽의 숫자(이름이 떠오르지 않았던 197명 가운데 187명). 전체 210명 가운데서는 198명(94.3%)
    tl = wrapl('이름이 떠오르지 않을 때 단서가 될 다른 기록부터 차례로 찾아봤다', 11, pw - 36 - 100)
    out = card('qb/sv/c2', px, y, pw, h1, '지금은 직접 이어서 찾습니다') + [
        T('qb/sv/c2/n', px + 18, y + 38, 96, 32, '94.9%', size=21, color=PURPLE, weight='b', anchor='ctr'),
        T('qb/sv/c2/nc', px + 18, y + 70, 96, 14, '197명 중 187명', size=9, color=MUTE, anchor='ctr'),
        T('qb/sv/c2/b', px + 18 + 100, y + 40 + (44 - clh * len(tl)) / 2, pw - 36 - 100, clh * len(tl) + 4, tl, size=11, color=INK, weight='m', lnspc=clh * 0.75),
        R('qb/sv/c2/ln', px + 18, y + 94, pw - 36, 1, fill='E6E0F5', line=None),
        T('qb/sv/c2/m', px + 18, y + 100, pw - 36 - 64, 22, '휴대폰 기본 검색 기능을 자주 쓴다', size=11, color=BODY, anchor='ctr'),
        T('qb/sv/c2/mv', px + pw - 18 - 60, y + 100, 60, 22, '33.8%', size=11.5, color=SUB, weight='b', align='r', anchor='ctr')]
    s.add('qb/sv/c2', out)
    y2, h2 = y + h1 + 12, ph - h1 - 12
    out = card('qb/sv/c3', px, y2, pw, h2, 'AI가 내 기록을 살펴 찾아 준다면')
    bx, bw_, by_ = px + 18, pw - 36, y2 + 44
    cx_ = bx
    for j, (nm, v, col) in enumerate(SV_USE):                # 하나로 이어진 띠(세 조각)
        sw = bw_ * v / 100
        out.append(R('qb/sv/u%d' % j, cx_, by_, sw - (2 if j < 2 else 0), 18, prst='roundRect', radius=5, fill=col, line=None))
        cx_ += sw
    for j, (nm, v, col) in enumerate(SV_USE):
        ry = by_ + 28 + j * 24
        out += [R('qb/sv/ud%d' % j, bx, ry + 6, 10, 10, prst='roundRect', radius=3, fill=col, line=None),
                T('qb/sv/ut%d' % j, bx + 17, ry, bw_ - 77, 22, nm, size=11, color=INK if j == 0 else BODY, weight='b' if j == 0 else 'r', anchor='ctr'),
                T('qb/sv/uv%d' % j, bx + bw_ - 60, ry, 60, 22, '%.1f%%' % v, size=11.5, color=PURPLE if j == 0 else SUB, weight='b', align='r', anchor='ctr')]
    s.add('qb/sv/c3', out)
    y += ph + 10
    footnote(s, SV_SRC + '. 비율은 전체 응답자 210명 기준이고, 94.9%만 정확한 이름이 떠오르지 않은 적이 있다고 답한 197명 기준(본 발표 8쪽과 같음).', y)
    return s


# ------------------------------------------------------------------ B-3 1년 상품화 계획
# 13차(11-17): 'UX를 단계적으로 적용하겠다는 게 아니고, 이것을 1년 안에 상품화한다면 어떤 것을 먼저 하고, 데이터 수집은 어떻게, 모델 선정과 학습은, 평가는, UX 등은
#   어떤 절차로, 실제 회사 상품화를 위해 필요한 것들을 단계적으로 적어 놓으라는 거야' → 분기(가로) × 일의 갈래(세로)의 표 하나와 아래 세 칸.
#   11차의 장(1단계 UX1 → 2단계 UX2 → 3단계 UX3 → 4단계 가전)은 뺌. 표의 칸은 다른 장에 적은 내용(데이터 D-11, 튜닝 D-7과 D-9, 측정 D-2 ~ D-4, 권한 B-6 ~ B-8)을 일정으로 옮긴 것
PLAN_Q = ['1분기: 기준과 데이터', '2분기: 모델 튜닝', '3분기: 통합과 사내 베타', '4분기: 검증과 출시']
PLAN = [['데이터 수집', '합성 데이터 구축: 학습 6만~9만 쌍, 평가 600문항 (D-11)', 'Hard Negative 보강, 한국어 원어민 검수',
         '사내 베타 참여자가 동의한 질의로 평가 문항 보강', '기록은 수집하지 않고 기기 안에서 Gate 기준값만 조정'],
        ['모델 선정과 학습', 'Baseline 측정: 튜닝 전 임베딩, 프롬프트만 쓴 Gauss', '**임베딩, Query Rewriter, Gate 모델 튜닝** (D-9, D-7, C-7)',
         'NPU 변환과 Quantization, 메모리와 속도 측정 (D-2 ~ D-4)', '탑재 기기별 최적화'],
        ['평가', '**지표와 출시 기준 확정** (지표 여섯 개, D-11)', '평가셋으로 비교: BM25, 튜닝 전 임베딩, 서버의 대형 임베딩',
         '실기기 측정: 응답 시간, 발열, 배터리, 제안 수락률', '베타 지표 확인, 업데이트마다 회귀 평가'],
        ['UX와 통합', '진입점과 색인 범위 확정: 키보드, 통화 화면 (A-8, B-6)', '색인 파이프라인(충전 중 색인)과 검색 프로토타입',
         'Samsung Keyboard와 통화 화면에 통합, 근거 카드 UI', '설정 화면: 앱별 색인 허용, 색인 초기화 (B-8)'],
        ['검증과 출시', '개인정보와 보안 검토 착수', '권한 설계 검토: 알림 접근, 내보낸 파일 (B-7)', '**사내 베타** (임직원 대상)', 'One UI 베타 프로그램을 거쳐 **플래그십에 정식 탑재**'],
        # 맨 아랫줄: 그 분기를 마치고 다음으로 넘어가는 기준
        [('통과 기준', dict(color=PURPLE)), '✓ 평가셋과 출시 기준에 합의', '✓ 평가셋의 Recall과 Chain 성공률', '✓ 실기기의 응답 시간과 메모리', '✓ 베타의 오답 신고와 제안 수락률']]
PLAN_COLS = [13, 22, 22, 22, 21]


def s_road():
    s = page_slide('qb_road', 'B-3', [('1년 안에 상품화한다면: 분기별 계획', INK)])
    y = 100
    th = tbl(s, 'qb/t', X, y, W, PLAN_COLS, [''] + PLAN_Q, PLAN, pady=8, pt=11.5, hi=(len(PLAN) - 1,), head_h=34)
    cx = X                                                    # 분기 사이의 화살표(머리글 줄)
    out = []
    for j, c in enumerate(PLAN_COLS[:-1]):
        cx += W * c / sum(PLAN_COLS)
        if j:
            out.append(arrow('qb/t/ar%d' % j, (cx - 26, y + 17), (cx - 6, y + 17), color=PURPLE2, w=1.6))
    s.add('qb/t/ar', out)
    y += th + 22
    y += notes3(s, 'qb/n', y, [('가장 먼저 하는 일', '**평가셋과 출시 기준**부터 만듭니다. 한국어 일상 기록에서 암시된 단서를 찾는 공개 벤치마크가 없어서, 기준이 없으면 튜닝한 모델이 나아졌는지 알 수 없습니다.'),
                               ('1년 안에 가능한 까닭', '새로 탑재하는 모델은 **임베딩 하나**이고 sLLM은 탑재된 Gauss를 그대로 씁니다. 진입점인 키보드와 통화 화면도 이미 있습니다. (D-1, A-8)'),
                               ('출시 범위와 그 뒤', '첫 출시는 **Gauss 3B가 탑재된 플래그십**과 삼성 기본 앱, 허용한 알림까지입니다. 그 뒤 One UI 업데이트로 기기를 넓히고¹ 가전과 TV로 잇습니다. (B-4)')], pt=12) + 18
    footnote(s, ['¹ Samsung Newsroom, "New One UI 6.1 Update Brings Galaxy AI to More Galaxy Devices" (2024. 02. 22): Galaxy AI도 Galaxy S24에서 시작해 업데이트로 S23, Z Fold5, Z Flip5, Tab S9에 적용함',
                 '분기별 일정은 1년 안의 상품화를 가정해 세운 계획. 학습에는 합성 데이터만 쓰고 실제 사용자의 기록은 쓰지 않음.'], y)
    return s


# ------------------------------------------------------------------ B-4 가전과 TV로의 확장 (11차에 새로 넣음)
B5 = [['냉장고 (패밀리허브)', '손님의 알레르기나 부족한 재료처럼 챙길 것을 먼저 안내', '캘린더, 카카오톡, 삼성노트의 레시피', '식재료 인식(AI 비전)¹, 화면과 음성 안내'],
      ['스마트 TV', '상황을 말하면 그날의 사진과 노래를 찾아 재생', '갤러리, 음악 재생 기록', 'Bixby로 듣고 큰 화면에서 재생'],
      ['세탁기', '알림장의 준비물처럼 날짜가 정해진 일을 전날 저녁에 안내', '알림장 앱의 알림, 캘린더', '세탁 기록과 맞춰 세탁 제안']]


def s_home():
    s = page_slide('qb_home', 'B-4', [('가전과 TV로의 확장: 제공하려는 기능', INK)])
    y, bh = 102, 84
    lw, rw_ = 400, 400
    mx, mw = X + lw, W - lw - rw_

    def side(key, x, w, title, lines, on):
        return [box(key + '/bg', x, y, w, bh, on=on, radius=18, shadow=False),
                T(key + '/t', x + 22, y + 12, w - 44, 24, title, size=14, color=PURPLE if on else INK, weight='b', anchor='ctr'),
                T(key + '/b', x + 22, y + 38, w - 44, 40, lines, size=11.5, color=BODY, lnspc=lh_of(11.5, 1.4) * 0.75)]
    s.add('qb/h/l', side('qb/h/l', X, lw, '휴대폰의 Weave', ['색인과 검색은 휴대폰에서 실행', '기록의 원문은 휴대폰 밖으로 나가지 않음'], True))
    s.add('qb/h/r', side('qb/h/r', X + W - rw_, rw_, '가전과 TV', ['Bixby가 듣고 화면과 음성으로 답을 전달', '함께 쓰는 화면이라 Voice ID로 본인 확인'], False))
    s.add('qb/h/m', [T('qb/h/m/t', mx, y + 12, mw, 22, 'SmartThings', size=12.5, color=PURPLE, weight='b', align='c', anchor='ctr'),
                     arrow('qb/h/m/a', (mx + 22, y + bh / 2), (mx + mw - 22, y + bh / 2), w=2.0),
                     T('qb/h/m/b', mx, y + bh / 2 + 6, mw, 20, '찾은 답만 전달', size=11, color=BODY, align='c', anchor='ctr')])
    y += bh + 20
    y += tbl(s, 'qb/t', X, y, W, [16, 36, 24, 24], ['기기', '목표 기능', '함께 보는 기록', '가전이 맡는 일'], B5, pady=9, pt=12) + 22
    y += notes3(s, 'qb/n', y, [('1단계: 물으면 답함', 'TV나 냉장고에 말로 물으면 **휴대폰이 찾은 답**을 화면과 음성으로 전합니다. 본 발표 35쪽의 TV 장면입니다.'),
                               ('2단계: 가전이 먼저 챙김', '냉장고의 재료나 세탁 기록 같은 **가전의 상태를 Trigger**로 삼아 먼저 알립니다. 35쪽의 냉장고 장면입니다. (C-7)'),
                               ('지키는 원칙', '가전에는 **답만** 건네고 대화 원문은 건네지 않습니다. 어떤 앱의 기록을 가전에 건넬지는 사용자가 정합니다.')], pt=12) + 18
    footnote(s, ['¹ 2026년형 Bespoke AI 패밀리허브의 AI 비전, LLM 기반 Bixby를 탑재한 2026년형 가전 (Samsung Newsroom, 2026. 03). 목소리를 알아보고 그 사람의 Now Brief를 보여 주는 냉장고는 CES 2026에서 공개',
                 'SmartThings의 등록 사용자는 4억 7천만 명 (Samsung Newsroom, 2026. 10). 가전 장면은 C-1과 C-3에도 있음.'], y)
    return s


# ------------------------------------------------------------------ B-5 왜 온디바이스인가 (팀원의 장)
def s_ondev():
    import apx_new
    return frame(apx_new.s_ondevice(), 'B-5')


# ------------------------------------------------------------------ B-6 읽을 수 있는 기록의 범위 (11차에 새로 넣음)
B7 = [('n', '바로 읽음', '삼성 기본 앱', '갤러리, 삼성노트, 캘린더, 연락처, 메시지, 이메일, 내 파일, 월렛. 사용자 동의 아래 기기 안에서 연동', 'Finder가 이미 검색하는 범위'),
      ('n', '바로 읽음', 'PDE가 정리한 개인 정보', '예약, 여행, 쿠폰 앱의 알림에서 모아 둔 정보 등', 'Finder와 Now Brief가 쓰는 범위'),      # 줄이 '알림에서' 뒤에서 바뀌게 뒤의 낱말을 붙여 둠
      ('n', '알림으로 읽음', '외부 메신저의 받은 메시지', '카카오톡, WhatsApp, Line처럼 알림에 내용이 담기는 앱. 사용자가 허용한 앱만 (B-7)', 'Android의 알림 접근 권한'),
      ('n', '파일로 읽음', '내보낸 대화와 받은 파일', '사용자가 내보낸 카카오톡 대화, 내려받은 첨부 파일. 사용자가 고른 것만', '내 파일의 폴더')]
B7_FINDER = [['삼성 기본 기능 (1P)', '설치된 앱, 설정, 연락처, 캘린더, 갤러리, 노트, 파일, 음성 녹음 등'],
             ['PDE 개인 정보', '예약, 여행, 쿠폰 등'],
             ['서드파티 앱', '계약을 맺은 외부 앱'],      # 11-17 사용자의 지시: 구분은 '서드파티 앱', 검색 대상은 '계약을 맺은 외부 앱'
             ['그 밖', '웨어러블 기기, 스토어']]


def s_scope():
    s = page_slide('qb_scope', 'B-6', [('읽을 수 있는 기록의 범위', INK)])
    y = 100
    y += pipeline(s, 'qb/f', y, None, B7, gap=16, name_pt=13.5, desc_pt=11.5, arrows=False) + 10
    s.add('qb/no', [R('qb/no/bg', X, y, W, 34, prst='roundRect', radius=10, fill='FDF0F0', line=None),
                    T('qb/no/t', X + 16, y, W - 32, 34, [[('읽지 않는 것  ', dict(color='B4232B', weight='b')), ('통화 내용과 녹음, 알림을 꺼 둔 대화방, 다른 앱의 화면', dict(color=BODY))]],
                      size=12, anchor='ctr')])
    y += 34 + 20
    # Finder 사용 통계는 A-3의 Q2에 있음(11-17: 'Finder 페이지를 따로 만들지 않고 기존 덱에'. 그날 저녁에 Q3에서 Q2로 자리를 바꿈). 답한 분의 성함은 적지 않음('성함까지는 필요 없고')
    label(s, 'qb/l1', X, y, 'Finder가 지금 검색하는 범위 (Finder 개발 파트장 서면 답변, 2026. 11)')
    h1 = tbl(s, 'qb/t', X, y + 30, W, [30, 70], ['구분', '검색 대상'], B7_FINDER, pady=7, pt=11.5)
    y += 30 + h1 + 18
    y += points(s, 'qb/p', X, y, W, ['**Weave는 Finder가 이미 검색하는 범위에서 시작합니다.** 필요한 기록의 대부분은 삼성 기본 앱과 PDE의 개인 정보에 있습니다. 녹음은 색인하지 않습니다.',
                                    '**외부 앱의 기록은 사용자가 허용한 알림으로 읽습니다.** 삼성의 Galaxy Watch 등이 이미 쓰는 권한입니다.'], gap=7, pt=12) + 12
    footnote(s, ['Finder의 범위는 서면 답변의 내용 그대로임. Finder가 실제로 쓰이는 비율은 A-3. 알림과 내보낸 파일로 읽는 방법은 B-7, 권한과 사생활 보호는 B-8.'], y)
    return s


# ------------------------------------------------------------------ B-7 카카오톡 같은 외부 앱의 대화를 읽는 방법
def s_kakao():
    s = page_slide('qb_kakao', 'B-7', [('카카오톡 같은 외부 앱의 대화를 읽는 방법', INK)])
    y, h, gap = 98, 170, 10
    qrow(s, 'qb/q1', y, h, '카카오톡은 삼성 앱이 아닌데 대화를 어떻게 읽나요?',
         '두 가지 경로로 읽습니다. **받는 메시지는 알림**으로 읽습니다. 사용자가 허용한 앱의 알림이 도착하면 보낸 사람과 내용, 시각을 받아 기기 안에서 색인합니다. '
         '**지난 대화는 사용자가 내보낸 파일**로 읽습니다. 사용자가 직접 고른 대화방만 대상입니다.',
         n=1, vis=vis_rows([('받는 메시지', 'Android의 알림 접근 권한¹'), ('지난 대화', '카카오톡의 ‘대화 내용 내보내기’ 파일²'), ('읽지 않는 것', '알림을 꺼 둔 대화방, 화면의 내용')], kw=86))
    qrow(s, 'qb/q2', y + h + gap, h, '이미 쓰이는 방식인가요?',
         '새 권한을 만들지 않습니다. 삼성의 Personal Data Intelligence가 이미 카카오톡, WhatsApp, Line, Gmail의 **알림에서 예약 정보를 모아** Finder와 Now Brief에 쓰고 있습니다.³ '
         'Galaxy Watch가 휴대폰의 알림을 보여 주는 것도 같은 권한입니다. 화면을 읽거나 앱의 저장소에 접근하지 않습니다.',
         n=2, vis=vis_rows([('Samsung PDI', '앱 알림에서 예약 정보를 수집³'), ('Now Brief', '알림으로 받은 정보를 요약에 사용'), ('Galaxy Watch', '휴대폰의 알림을 워치에 표시')], kw=96))
    qrow(s, 'qb/q3', y + 2 * (h + gap), h, '알림으로 읽는 방식의 한계는 무엇이고, 어떻게 채우나요?',
         '알림은 **받은 메시지**에만, **알림을 켜 둔 대화방**에만 옵니다. 그래서 시나리오의 단서는 모두 상대가 보낸 메시지로 잡았습니다. '
         '내가 보낸 말이나 알림을 꺼 둔 대화방, PC로 주고받은 대화가 필요하면 **사용자가 그 대화방을 내보내서** 채웁니다.',
         n=3, vis=vis_rows([('내가 보낸 말', '내보낸 대화 파일로 읽음'), ('알림을 끈 대화방', '필요한 대화방만 내보내서 색인'), ('PC 카카오톡 사용 중', '늦게 오는 알림은 내보낸 파일로 보완')], kw=132))
    footnote(s, ['¹ Android Developers, "NotificationListenerService"   ² 삼성전자서비스 안내: 채팅방 설정에서 대화 내용 내보내기를 누르면 내 파일의 KakaoTalk 폴더에 저장됨',
                 '³ Samsung 지원, "Understanding Finder on Galaxy phones": "Personal data intelligence (PDI): This feature collects reservation details from notifications in apps like '
                 'Messages, Gmail, Naver, Line, WhatsApp, KakaoTalk, and Wallet."'], y + 3 * h + 2 * gap + 10)
    return s


# ------------------------------------------------------------------ B-8 데이터 접근 권한과 사생활 보호
DAY_N = 1000                                    # 하루에 쌓이는 새 기록(건). 11차: 300 → 1,000


def s_data():
    s = page_slide('qb_priv', 'B-8', [('데이터 접근 권한과 사생활 보호', INK)])
    y, h, gap = 98, 170, 10
    qrow(s, 'qb/q1', y, h, '어떤 기록을 어떤 권한으로 읽나요?',
         '삼성 기본 앱(갤러리, 노트, 캘린더, 메일, 월렛)은 사용자의 동의를 받아 기기 안에서 연동합니다. 카카오톡 같은 외부 메신저는 **사용자가 허용한 알림만** 색인합니다.¹ '
         '통화 내용은 듣지도 저장하지도 않습니다. 읽을 수 있는 범위는 B-6에 정리했습니다.',
         n=1, vis=vis_rows([('삼성 앱', '사용자 동의 후 기기 안에서 연동'), ('외부 앱', '허용한 알림만 색인 (B-7)'), ('통화', '듣지도 저장하지도 않음')], kw=72))
    qrow(s, 'qb/q2', y + h + gap, h, '배터리와 발열은 괜찮나요?',
         '처음의 대량 색인과 사진 색인은 **충전 중이거나 기기가 쉴 때만** 백그라운드로 실행합니다.² 평소에는 글로 된 새 기록 한 건에 임베딩 한 번(EmbeddingGemma 2, 8ms)을 실행합니다. '
         '하루에 새 기록이 %s건 쌓여도 %d초입니다. sLLM은 질의할 때 추려진 기록 몇 건에만 실행합니다.' % (format(DAY_N, ','), round(DAY_N * NUM.EMB)),
         n=2, vis=vis_nums([('8ms', ['새 기록 1건의', '색인 (글 기준)']), ('%ds' % round(DAY_N * NUM.EMB), ['하루 %s건을' % format(DAY_N, ','), '색인하는 시간'])], pt=20))      # 11차: 두 숫자의 단위를 같은 꼴로(8ms와 8s)
    qrow(s, 'qb/q3', y + 2 * (h + gap), h, '사생활은 어떻게 지키나요?',
         '원본 기록과 색인은 모두 **기기 안에만** 저장하고, 암호화 키는 하드웨어 보안 영역에 둡니다.³ 어느 앱을 색인할지는 사용자가 정합니다. '
         '그럼에도 불안하다면 원하는 앱만 켜 두고 쓰다가, 언제든 색인을 한 번에 지울 수 있습니다.',
         n=3, vis=vis_rows([('저장', '원본과 색인 모두 기기 안'), ('제어', '앱별 색인 허용, 색인 초기화'), ('삭제', '원본을 지우면 색인도 함께 삭제')], kw=56))
    footnote(s, ['¹ Android Developers, "NotificationListenerService"   ² Android Developers, "WorkManager: Define work requests" (RequiresCharging, RequiresDeviceIdle)   '
                 '³ Android Developers, "Android Keystore system"'], y + 3 * h + 2 * gap + 10)
    return s


# ------------------------------------------------------------------ B-2 사업 효과 (숫자는 9차 후보 장(biz_new.py)의 것)
def s_biz():
    s = page_slide('qb_biz', 'B-2', [('사업 효과', INK)])
    y, h, gap = 98, 170, 10
    qrow(s, 'qb/q1', y, h, '사용자를 Galaxy에 머물게 하는 효과가 있나요?',
         '쓸수록 떠나기 어려워집니다. 기록은 한 달에 평균 41개의 앱에 흩어져 쌓이고¹, 사람들은 그 기록을 지우지 않습니다.² 사진과 메모는 다른 휴대폰으로 옮길 수 있지만, '
         'Weave가 그 사이를 **이어 둔 기억은 Galaxy끼리만 옮길 수 있습니다.**',
         n=1, vis=vis_nums([('41개', ['한 달에 쓰는', '앱의 수¹']), ('69%', ['기록을 지우지 않고', '쌓아 두는 사람²'])], pt=22))
    qrow(s, 'qb/q2', y + h + gap, h, '새로운 사용자를 끌어올 수 있나요?',
         '기록을 찾지 못하는 불편은 기기를 가리지 않습니다. 저희 설문에서 iPhone 사용자 62명 가운데 61명이 같은 불편을 겪었고 **60명이 쓰겠다**고 답했습니다.³ '
         '10대의 Galaxy 사용률은 61%인데, 다음에 사고 싶은 휴대폰으로 Galaxy를 고른 비율은 47%입니다.⁴ Weave는 다음 세대가 Galaxy를 고를 이유가 됩니다.',
         n=2, vis=vis_nums([('62명 중 60명', ['iPhone 사용자의', '사용 의향³']), ('61% → 47%', ['10대의 Galaxy 사용과', '다음 구매 의향⁴'])], pt=19))
    # 14차(11-17 밤, 사용자의 글): Q3의 물음과 답을 받은 글로(받은 글의 '사용하는데'는 띄어 씀). 그 전: '적용하는 데 비용이 많이 들지 않나요?',
    #   '새 부품이 필요 없는 소프트웨어입니다. Galaxy AI가 들어가는 기기는 2026년 말 8억 대이고⁵, 업데이트만으로 적용할 수 있습니다. 새로 탑재하는 모델은 임베딩 하나이고,
    #   sLLM은 기기에 탑재된 Gauss를 그대로 씁니다. (D-1, D-2)'. 그림의 숫자 둘은 답에 맞춰 내가 바꿈: '8억 대, 1개(새로 탑재하는 모델)' → '0원(사용량이 늘 때 더 드는 서버 비용), 8억 대'
    qrow(s, 'qb/q3', y + 2 * (h + gap), h, '해당 AI 서비스를 사용하는 데 비용이 계속 들지 않나요?',
         'Weave는 온디바이스 방식이기에 사용자가 많아지고, 서비스를 많이 사용할수록 **비용이 늘어나는 구조가 아닙니다.** 비용 투자는 초기 개발 단계에만 발생하고, '
         '갤럭시 사용자가 많아질수록 **1인당 총비용은 오히려 낮아집니다.**',
         n=3, vis=vis_nums([('0원', ['사용량이 늘 때', '더 드는 서버 비용']), ('8억 대', ['2026년 말', 'Galaxy AI 기기⁵'])], pt=22))
    footnote(s, ['¹ Ofcom, "Online Nation 2025" (영국 스마트폰 이용자)   ² Compare and Recycle, "Digital Declutter Statistics 2025" (스스로를 디지털 호더라고 답한 비율)   '
                 "³ 자체 설문조사 (응답자 210명 가운데 iPhone 사용자 62명, '26.11)",
                 '⁴ 한국갤럽, 「스마트폰 관련 조사 2012-2026」 (2026. 07), 13~18세 200명   ⁵ 삼성전자 발표: Reuters 인터뷰 (2026. 01), Galaxy Unpacked (2026. 02, 2026. 07)'],
             y + 3 * h + 2 * gap + 10)
    return s


# ------------------------------------------------------------------ 물음과 답
PAGES = [
    Page('D-2', '메모리와 저장 공간', s_mem,
         q='AI 모델이 늘면 메모리가 부족해질 텐데, Weave는 얼마나 쓰나요? 몇 년 치 기록이 쌓이면 저장 공간은요?',
         a='Weave가 추가로 사용하는 메모리는 약 0.25기가바이트로, Galaxy S26 Ultra의 메모리 12기가바이트의 2% 정도입니다. '
           '내역은 임베딩 모델이 약 0.19기가바이트, 기록 10만 건의 색인이 26메가바이트, Query Rewriter 어댑터가 수십 메가바이트입니다. '
           '가장 무거운 sLLM은 새로 탑재하지 않고, 기기에 이미 있는 Gauss 3B를 함께 쓰면서 그 위에 작은 어댑터만 얹습니다. '
           '저장 공간도 작습니다. 기록 하나의 벡터가 256바이트라서 100만 건이 쌓여도 256메가바이트, 1,000만 건이어도 2.56기가바이트입니다. '
           '하루에 1,000건씩 쌓인다고 해도 100만 건까지 3년 가까이 걸립니다.',
         more=[('글자가 없는 사진까지 찾으려면 메모리가 더 들지 않나요?',
                '사진의 내용으로 찾으려면 EmbeddingGemma 2의 전체 구성이 필요하고, 약 0.57기가바이트입니다. 다만 사진의 벡터는 충전 중에 미리 만들어 두기 때문에, 글로 질의할 때는 텍스트 구성 0.19기가바이트만 올리면 됩니다.'),
               ('기록이 100만 건이면 메모리는요?', '색인 256메가바이트는 저장 공간에 두고 필요한 부분만 메모리에 올리기 때문에 메모리 부담은 그보다 작습니다.'),
               ('오래된 기록은 지우거나 줄이나요?', '지우지 않습니다. 1,000만 건이어도 2.56기가바이트라서 그대로 둡니다. 원본을 지우면 그 기록의 색인도 함께 지웁니다.'),
               ('Gauss가 메모리에서 내려가 있으면요?', '그때는 다른 Galaxy AI 기능과 마찬가지로 모델을 올리는 시간이 한 번 듭니다. 검색 결과는 그 전에 먼저 보여 줄 수 있습니다.'),
               ('Query Rewriter를 어댑터 말고 전용 모델로 둘 수도 있나요?',
                '둘 수 있습니다. 1B급 모델을 통째로 튜닝해 따로 올리면 가중치가 0.5에서 1기가바이트라서, Weave가 추가로 사용하는 메모리가 0.7에서 1.2기가바이트가 됩니다. '
                'Gauss가 없는 기기에서도 쓸 수 있는 대신 모델 하나를 더 관리해야 합니다. 그래서 기본 구성은 탑재된 Gauss에 어댑터를 얹는 쪽으로 잡았습니다.'),
               ('튜닝하기 전에는 Query Rewriter가 없는 건가요?', '프롬프트만으로 시작할 수 있습니다. Gauss에 검색 계획의 형식을 프롬프트로 주는 방식이고, 그때는 추가 메모리가 없습니다. 어댑터는 그 뒤에 정확도를 올리려고 얹습니다.')],
         basis=['Google, "EmbeddingGemma 2"(2026. 10. 06): "~191MB active RAM for text-only weights and ~567MB for the full multimodal model on a Google Pixel 11 Pro".',
                '색인 크기는 256차원 8비트 벡터(기록 하나에 256바이트)로 셈: 1만 건 2.6MB, 10만 건 25.6MB, 100만 건 256MB, 1,000만 건 2.56GB. Android ML Kit의 Embeddings API도 8비트로 양자화한 벡터를 AppSearch에 저장함.',
                '하루 1,000건 기준: 10만 건 100일, 100만 건 1,000일(2.7년), 1,000만 건 10,000일(27.4년). 하루 1,000건은 11차에 사용자가 정한 값(10차는 300건).',
                'Apple, "Introducing Apple\'s On-Device and Server Foundation Models"(2024. 06. 10): "the parameters for a rank 16 adapter typically require 10s of megabytes", "can be dynamically loaded, temporarily cached in memory, and swapped".',
                'sLLM: 11차에 사용자의 지시로 Llama 3.2의 측정값(3B 4비트 RSS 3,726MiB, ExecuTorch, OnePlus 12) 대신 Gauss 3B(8bit)로 적음. 약 3GB는 30억 파라미터 × 1바이트로 셈한 가중치의 크기이고 Gauss를 잰 값이 아님.',
                'Galaxy S26 Ultra 메모리: 256GB와 512GB 모델 12GB, 1TB 모델 16GB(사양표).',
                '합계: 0.19GB + 0.026GB + 어댑터 수십 MB ≈ 0.25GB. 0.25 ÷ 12 = 2.1%.',
                '글로 질의할 때 텍스트 구성만 올린다는 것은 설계: 사진의 벡터를 색인 때 미리 만들어 두면 질의 쪽에는 텍스트 인코더만 필요함(Carbon이 짚은 빈 곳, 11-16).',
                '‘오래된 데이터는 핵심 요약본만 남긴다’는 말은 쓰지 않음(11차 검토).',
                '13차(11-17, 사용자의 지시 "Query Rewriter를 Adapter 말고도 쓸 수도 있을 것 같은데, 만약 쓰게 되면 추가해 줘"): 표의 Query Rewriter를 두 줄로 나눔. '
                '기본은 Gauss + LoRA Adapter(수십 MB. 튜닝 전에는 프롬프트만으로 시작하고 그때는 추가 메모리 없음), 전용 모델은 1B급을 통째로 튜닝해 따로 올리는 구성. '
                '전용 모델의 0.5~1GB는 10억 파라미터 × 4bit~8bit로 셈한 가중치의 크기이고, 그때의 합계는 0.19 + 0.026 + 0.5~1.0 = 0.72~1.22GB(12GB의 6~10%). 1B급 모델의 속도는 속도 2 장(D-4) 표의 둘째 줄.']),
    Page('D-3', '속도 1: 검색 시간, 기준 모델', s_speed,
         q='기록을 전부 LLM에게 읽히면 되지 않나요? 검색 한 번에 0.02초라는 숫자는 어떻게 나온 건가요?',
         a='기록이 수만 건이면 질의마다 전부 읽히기에는 연산량이 너무 큽니다. 그래서 찾는 일은 임베딩에 맡겼습니다. '
           '기록의 벡터는 충전 중에 미리 만들어 두기 때문에, 질의가 들어오면 질의 하나만 벡터로 바꿔 비교하면 됩니다. '
           '0.02초의 내역은 이렇습니다. 질의를 벡터로 바꾸는 데 8밀리초, 기록 10만 건과 모두 비교해 가장 가까운 20건을 고르는 데 10밀리초, 날짜와 사람으로 거르는 데 2밀리초입니다. '
           '8밀리초는 EmbeddingGemma 2를 Galaxy S26 Ultra의 NPU에 올려 직접 잰 값입니다. '
           '벡터 검색은 PC에서 직접 재 보니 10만 건에 5밀리초가 걸렸고, 휴대폰은 그 두 배로 잡았습니다. '
           '세 번 이어 찾아도 0.06초라서, 시간은 대부분 sLLM이 질의를 다시 쓰고 답변을 만드는 데 듭니다.',
         more=[('기록이 100만 건이면요?', '모두 비교하는 방식으로도 한 번 찾는 데 0.11초입니다. 색인은 256메가바이트입니다.'),
               ('후보를 많이 넣어 주면 LLM이 고를 수 있지 않나요?', '후보가 많아지면 LLM의 정확도가 크게 떨어집니다. 공개 벤치마크에서 정답 기록만 주면 GPT-4.1이 88점을 내지만, 헷갈리는 기록 29건과 함께 주면 23점이 됩니다. 먼저 정확히 찾아야 합니다.'),
               ('NPU 환산을 믿을 수 있나요?', '임베딩 모델에서 확인한 비율을 적용한 추정입니다. NPU에서 직접 잰 Gemma 3 1B의 값으로 셈해도 단서로 찾는 기억은 1초 남짓입니다. D-4의 표에 함께 적었습니다.'),
               ('Gauss로 직접 재지 않은 이유는요?', 'Gauss의 온디바이스 속도는 공개되어 있지 않아서, 같은 크기의 공개 모델을 기준으로 삼았습니다.'),
               ('키워드 검색과 비교하면요?', '둘 다 밀리초 단위라서 함께 써도 차이를 느끼기 어렵습니다. 그래서 Weave는 두 검색을 함께 씁니다.'),
               ('임베딩 검색이 놓치면 LLM도 볼 수 없지 않나요?', '그래서 후보를 20건 가져오고 키워드 검색(BM25)도 함께 씁니다. 그래도 근거가 없으면 찾지 못했다고 답합니다.'),
               ('숫자 가운데 어디까지가 직접 잰 값인가요?',
                '임베딩 속도와 벡터 검색 시간입니다. 임베딩은 Galaxy S26 Ultra의 NPU에서 8밀리초가 나왔고, 벡터 검색은 PC에서 10만 건에 5밀리초, 100만 건에 52밀리초가 나왔습니다. '
                'sLLM의 응답 시간은 공개된 측정값으로 셈한 값이고, 검색 정확도는 한국어 평가셋을 만들어 잽니다.'),
               ('PC에서 잰 값을 휴대폰 값으로 써도 되나요?', '쓰지 않았습니다. PC에서 잰 값은 5밀리초이고, 휴대폰은 그 두 배인 10밀리초로 잡았습니다. 256차원 벡터 10만 건의 비교는 연산량이 작아서 기기 차이가 크지 않을 것으로 봅니다.')],
         basis=['임베딩 8ms: EmbeddingGemma 2(텍스트 구성), Galaxy S26 Ultra NPU 실측(팀 측정). 모델 카드(litert-community/embeddinggemma-2-text-270m-litert-lm, 128토큰, 5회 평균)의 값은 S26 Ultra GPU 25.9ms, CPU 27.1ms, Pixel 11 Pro TPU 8.3ms.',
                '벡터 검색 10ms: 256차원 벡터 10만 건을 모두 비교해 상위 %d건을 고르는 시간으로 잡은 값. 11월 16일에 이 PC(Intel Core i7-1360P, 코어 1개, numpy)에서 직접 잰 값은 1만 건 %.2fms, 10만 건 %.2fms, 100만 건 %.2fms(30회의 중앙값, `tools/exp_search_time.py`). '
                '사용자의 검토 자료(11-14)도 x86 코어 하나에서 5.1ms를 재고 휴대폰은 10ms로 잡음. sqlite-vec v0.1은 Mac M1 mini에서 128차원 100만 건을 17ms에 비교함. 모두 비교하는 방식이라 고르는 건수(20건)는 시간에 거의 영향이 없음.'
                % (NUM.TOPK, NUM.PC_SEARCH_MS[10_000], NUM.PC_SEARCH_MS[100_000], NUM.PC_SEARCH_MS[1_000_000]),
                '상위 20건은 설계값: Hop마다 임베딩 검색과 BM25가 각각 후보를 내고 순위를 합친 뒤 메타데이터로 거름(C-4).',
                '기록 수별 Hop 시간: 1만 건 8 + 1 + 2 = 11ms, 10만 건 8 + 10 + 2 = 20ms, 100만 건 8 + 100 + 2 = 110ms(모두 비교하는 방식 기준).',
                'NPU 환산 비율: 25.9 ÷ 8 = %.2f(GPU), 27.1 ÷ 8 = %.2f(CPU). 11-16에 사용자가 이 비율로 셈하라고 함.' % (NUM.R_GPU, NUM.R_CPU),
                '생성 속도(LiteRT-LM 공개값, 입력과 출력의 초당 토큰): Gemma 4 E2B는 S26 Ultra GPU에서 3,808과 52.1 → NPU 환산 %d과 %d(기준 속도). Gemma 3 1B는 S25 Ultra NPU에서 5,836과 85(실측 그대로).'
                % (round(NUM.E2B.pre_npu), round(NUM.E2B.dec_npu)),
                'ImpliRet(arXiv 2506.14407): 정답 문서만 줄 때와 30건을 줄 때 GPT-4.1 88.05 → 22.90, o4-mini 92.74 → 55.54, Llama 3.3 70B 81.92 → 10.71.',
                '공개된 NPU 측정 가운데 Qualcomm AI Hub의 Galaxy S26 값은 Qwen3-0.6B 출력 초당 88.8토큰, Qwen3-1.7B 42.4토큰, Qwen3-4B 21.8토큰. NPU 환산값(Gemma 4 E2B %d토큰)은 이보다 빠른 쪽의 추정임.' % round(NUM.E2B.dec_npu),
                '10차의 A-7(LLM에게 전부 읽히면) 가운데 Q1을 이 장으로 옮기고 그 장은 뺌(11차 검토: "1번만 쓸모 있는 질문"). Q2와 Q3의 내용은 ‘더 물으면’에 남김.',
                '13차(11-17): 11차의 ‘직접 측정하거나 확인한 것’ 장을 빼면서(사용자: "따로 뺄 필요 없을 것 같고, 대신 설문조사 결과 한눈에 시각화한 페이지를") 그 장의 물음 둘(직접 잰 값의 범위, PC에서 잰 값)을 ‘더 물으면’으로 옮김. '
                '그 장의 네 줄은 이 장(임베딩 8ms, 벡터 검색 시간), A-3(Finder의 의미 검색), B-1(설문)에 그대로 있음.']),
    Page('D-4', '속도 2: UX별 응답 시간', s_uxtime,
         q='실제로 답이 나오기까지 몇 초가 걸리나요? 발열이나 배터리는 괜찮나요?',
         a='단서로 찾는 기억은 %s입니다. 시간은 sLLM이 출력하는 토큰 수에 달려 있습니다. '
           '질의 재작성은 검색 계획의 길이에 따라 0.2초에서 0.6초, 답변 생성은 이름 추출이 약 0.1초, 세 줄 요약이 0.5초에서 0.9초입니다. '
           '기록 통합 검색은 요약까지 1.1초에서 1.5초가 걸리는데, 찾은 기록은 0.6초쯤에 먼저 보여 줍니다. '
           '먼저 건네는 기억은 백그라운드에서 %s에 준비합니다. '
           '발열과 배터리 부담을 줄이려고 sLLM은 질의마다 두 번만 실행하고, 무거운 색인은 충전 중에만 실행합니다. '
           '이 값은 2B급 공개 모델의 속도를 NPU 기준으로 환산해 셈한 것이고, NPU에서 직접 잰 1B 모델의 속도로 셈해도 단서로 찾는 기억은 1초 남짓입니다.' % (NUM.T_UX2, NUM.T_UX3),
         more=[('Hop이 늘면 더 느려지지 않나요?', '질의 재작성은 질의마다 한 번뿐입니다. Hop이 하나 늘면 검색 0.02초와 계획 한 줄을 더 생성하는 시간만 늘어납니다. 합쳐서 0.1초 안쪽입니다.'),
               ('통화 중에 쓰기에는 느리지 않나요?', '찾은 기록 목록은 0.6초쯤에 먼저 뜹니다. 요약은 그 뒤에 글자가 나타나는 대로 읽으면 됩니다.'),
               ('배터리가 적거나 기기가 뜨거울 때는요?', 'sLLM을 쓰기 어려운 상황에서는 원래 질의로 한 번 검색한 결과를 먼저 보여 줍니다. 검색은 0.02초라 이때도 부담이 없습니다.'),
               ('토큰 수는 어떻게 가정했나요?', '재작성은 입력 130토큰에 검색 계획 72에서 82토큰, 답변은 이름 추출 10토큰, 보낼 메시지 25토큰, 세 줄 요약 80토큰으로 잡았습니다. 한도는 검색 계획 100토큰, 요약 150토큰입니다.'),
               ('왜 0.2초에서 0.6초로 차이가 나나요?', '출력하는 토큰 수가 달라서입니다. 짧은 계획은 40토큰, 긴 계획은 100토큰까지 씁니다. 토큰 하나에 약 6밀리초가 듭니다.')],
         basis=['기준 속도: ' + NUM.BASIS + '. 11차(11-16)에 사용자의 지시로 내세우는 숫자를 이 속도 하나에 출력 토큰 수만 바꿔 셈함(전에는 세 구성의 가장 빠른 값과 가장 느린 값을 범위로 적어 0.2~1.0초처럼 넓었음).',
                '재작성: 입력 130, 출력 40~100토큰 → %.2f~%.2f초. 답변: 이름 추출(입력 170, 출력 10) %.2f초, 메시지 제안(입력 500, 출력 25) %.2f초, 3줄 요약(입력 540, 출력 80~150) %.2f~%.2f초.'
                % (NUM.RW_T[0], NUM.RW_T[1], NUM.AN_NAME, NUM.AN_MSG, NUM.AN_SUM[0], NUM.AN_SUM[1]),
                '표의 두 줄(Query Rewriter와 답변 생성에 같은 모델): Gemma 4 E2B(NPU 환산, 기준 속도), Gemma 3 1B(NPU 실측). 아래 세 줄의 값도 이 차례. 13차(11-17)에 세 줄에서 두 줄로 줄임.',
                'UX2(재작성 130 → 72토큰, 검색 2회, 답변 170 → 10토큰): ' + ', '.join(NUM.sec(v) for v in NUM.TOT['ux2']) + '.',
                'UX1(재작성 130 → 82토큰, 검색 3회, 요약 540 → 80토큰): ' + ', '.join(NUM.sec(v) for v in NUM.TOT['ux1']) + '. 찾은 기록이 먼저 뜨는 때는 ' + ', '.join(NUM.sec(v) for v in NUM.REC1) + '.',
                'UX3(재작성 130 → 72토큰, 검색 2회, 제안 500 → 25토큰): ' + ', '.join(NUM.sec(v) for v in NUM.TOT['ux3']) + '.',
                '출력 한도(검색 계획 100토큰, 요약 150토큰)는 11차에 내가 둔 값: 검토 자료의 계획 72~82토큰과 화면의 3줄 요약 예시에 여유를 둠. 토큰 수의 가정은 사용자의 검토 자료(11-14) 6장.',
                'sLLM의 출력 합계: UX1 82 + 80 = 162토큰(요약이 150토큰이면 232토큰), UX2 82토큰, UX3 97토큰.']),
    Page('B-3', '1년 상품화 계획', s_road,
         q='이 아이디어를 1년 안에 상품화한다면 무엇부터 어떤 순서로 진행하나요?',
         a='평가셋과 출시 기준부터 만들고, 분기마다 기준을 통과해야 다음으로 넘어가는 순서로 진행합니다. '
           '1분기에는 한국어 일상 기록을 합성해 학습 데이터와 평가 문항 600개를 만들고, 튜닝하지 않은 모델의 성능을 먼저 잽니다. '
           '2분기에는 그 데이터로 Reasoning Embedding과 Query Rewriter 어댑터를 튜닝하고, 키워드 검색과 튜닝 전 임베딩, 서버의 대형 임베딩과 비교합니다. '
           '3분기에는 NPU에 맞게 변환해 실제 기기에서 메모리와 속도를 재고, Samsung Keyboard와 통화 화면에 통합해 사내 베타를 시작합니다. '
           '4분기에는 One UI 베타 프로그램으로 검증한 뒤 플래그십에 정식 탑재합니다. '
           '학습에는 합성 데이터만 쓰고 실제 사용자의 기록은 쓰지 않습니다.',
         more=[('왜 평가셋부터 만드나요?', '기준이 없으면 튜닝한 모델이 나아졌는지 알 수 없기 때문입니다. 한국어 일상 기록에서 암시된 단서를 찾는 공개 벤치마크가 없어서 직접 만들어야 합니다. 만드는 방법은 D-11에 있습니다.'),
               ('데이터는 어떻게 모으나요? 사용자의 기록을 쓰나요?',
                '쓰지 않습니다. 가상의 인물 300명과 그 사람들의 사건을 만들고, 사건을 카카오톡과 캘린더, 사진 같은 앱의 기록으로 바꿔 씁니다. '
                '평가 문항은 한국어 원어민이 검수하고, 3분기부터는 사내 베타 참여자가 동의한 질의를 보탭니다.'),
               ('모델은 어떻게 고르나요?',
                '1분기에 튜닝하지 않은 EmbeddingGemma 2와 프롬프트만 쓴 Gauss의 성능을 평가셋에서 먼저 잽니다. '
                '2분기에는 그 값보다 얼마나 오르는지를 보고, 기준에 못 미치면 Teacher 모델과 학습 데이터를 바꿔 다시 튜닝합니다.'),
               ('세 가지 기능을 따로 개발하나요?', '세 기능은 같은 색인과 같은 모델을 쓰기 때문에 함께 개발하고 함께 내놓습니다. 기능마다 다른 것은 진입점과 Gate의 기준값이고, 그 값은 3분기 사내 베타에서 정합니다.'),
               ('1년 안에 가능한 일정인가요?', '새로 탑재하는 모델이 임베딩 하나이고, sLLM은 이미 탑재된 Gauss를 그대로 씁니다. 진입점인 키보드와 통화 화면도 이미 있습니다. 새로 만드는 것은 색인과 튜닝 데이터, 그리고 작은 어댑터입니다.'),
               ('보급형에서는 어디까지 되나요?', '첫 출시는 Gauss 3B가 탑재된 플래그십입니다. 임베딩 검색은 0.2기가바이트와 0.02초면 되기 때문에 그 뒤 One UI 업데이트로 넓힐 수 있고, sLLM이 필요한 기능은 Gauss가 탑재된 기기에서 동작합니다.'),
               ('가장 큰 위험은 무엇인가요?', '튜닝한 임베딩이 기준에 못 미치는 경우입니다. 그래서 2분기에 통과 기준을 두었고, 못 미치면 학습 데이터의 Hard Negative를 보강하거나 후보로 둔 다른 방식을 적용합니다. D-9에 정리했습니다.'),
               ('가전과 TV는 언제 하나요?', '휴대폰에 탑재한 뒤입니다. 검색은 휴대폰이 하고 가전은 답만 받기 때문에 가전에 모델을 올릴 필요가 없습니다. B-4에 정리했습니다.')],
         basis=['13차(11-17)에 다시 쓴 장. 사용자의 지시: "그런 식으로 UX를 단계적으로 적용하겠다는 게 아니고, 만약 이것을 1년 안에 상품화한다면 어떤 것을 먼저 하고(데이터 수집은 어떻게, 모델 선정과 학습은, 평가는, UX 등은, 어떤 절차로) '
                '실제 회사 상품화를 위해 필요한 것들을 단계적으로 적어 놓으라는 것". 11차의 장(1단계 기록 통합 검색 → 2단계 단서로 찾는 기억 → 3단계 먼저 건네는 기억 → 가전)은 뺌.',
                '분기별 일정과 통과 기준은 내가 짠 안(1년을 네 분기로 나눔). 표의 칸은 다른 장에 적은 내용을 일정으로 옮긴 것: 데이터와 평가는 D-11(검토 자료 4장의 Persona 300명, 학습 6만~9만 쌍, 평가 600문항, 여섯 지표), '
                '튜닝은 D-7과 D-9, 측정은 D-2 ~ D-4, 진입점은 A-8, 읽는 범위와 권한, 설정은 B-6 ~ B-8, Gate 모델은 C-7.',
                '삼성 내부의 개발 절차 이름(검증 단계의 이름 등)은 알지 못해 일반적인 말(사내 베타, 개인정보와 보안 검토)로 적음. One UI 베타 프로그램은 Samsung Members에서 신청하는 공개 베타.',
                'Samsung Newsroom, "New One UI 6.1 Update Brings Galaxy AI to More Galaxy Devices"(2024. 02. 22): Galaxy S23 시리즈, S23 FE, Z Fold5, Z Flip5, Tab S9에 3월 말부터.',
                'Gauss 3B와 1B의 온디바이스 탑재는 팀 조사 기준.']),
    Page('B-4', '가전과 TV로의 확장', s_home,
         q='휴대폰만의 이야기 같은데, TV와 가전 같은 DX 전체로는 어떻게 넓히나요? 어떤 기능까지 생각하고 있나요?',
         a='기억을 찾는 일은 휴대폰의 Weave가 맡고, 찾아낸 답만 SmartThings로 가전과 TV에 건네는 구조로 넓힙니다. '
           '가전마다 모델을 올리거나 기록을 옮길 필요가 없습니다. 목표로 하는 기능은 기기마다 다릅니다. '
           '냉장고는 손님의 알레르기나 부족한 재료처럼 챙길 것을 먼저 알려 줍니다. '
           'TV는 상황을 말하면 그날의 사진과 노래를 찾아 틀어 줍니다. '
           '세탁기는 알림장의 준비물처럼 날짜가 정해진 일을 전날 저녁에 알려 줍니다. '
           '순서는 두 단계입니다. 먼저 말로 물으면 답하는 기능부터 시작하고, 다음에 가전의 상태를 Trigger로 삼아 먼저 챙기는 기능으로 넓힙니다. '
           '함께 쓰는 화면이라 Voice ID로 본인이 확인됐을 때만 보여 주고, 가전에는 답만 건넵니다.',
         more=[('웨어러블은요?', 'Galaxy Watch는 지금도 휴대폰의 알림을 받아 보여 줍니다. 같은 경로로 Weave가 찾은 답을 워치에서 받는 것부터 시작할 수 있습니다.'),
               ('가전에 모델을 올려야 하나요?', '아닙니다. 검색은 휴대폰이 하고, 가전은 Bixby로 듣고 답을 보여 주거나 말합니다.'),
               ('냉장고는 재료를 어떻게 아나요?', '2026년형 패밀리허브의 AI 비전이 알아보는 재료를 SmartThings로 받는 것을 전제로 했습니다. 재료를 모를 때는 일정과 부탁만 알려 줍니다.'),
               ('가족이 함께 보는 화면에 개인 기록이 뜨면요?', '찾아낸 답만 건네고 대화 원문은 건네지 않습니다. Voice ID로 본인이 확인됐을 때만 보여 주고, 어떤 앱의 기록을 가전에 건넬지는 사용자가 정합니다.'),
               ('휴대폰이 집에 없으면요?', '기억은 휴대폰에 있어서 휴대폰이 연결되어 있을 때 동작합니다. 가전만으로 답하게 하려면 기록을 옮겨야 해서 그 방식은 택하지 않았습니다.')],
         basis=['11차(11-16)에 새로 넣은 장: 팀 검토의 예상 질문 10번("DX 전체로는 어떻게 확장하나, 가전과 TV를 위한 구체 장표를 하나 더, 어떤 기능까지 제공을 목표로 하는지").',
                '기기별 기능은 본 발표 35쪽(냉장고가 친구의 알레르기를 먼저 알림, TV가 벚꽃 보러 간 날 듣던 노래를 재생)과 시나리오 더 보기의 미래 장면(C-1 갈비찜, C-3 미역국과 체육복)에서 가져옴. 새 기능을 지어내지 않음.',
                'Samsung Newsroom: 2026년형 Bespoke AI 패밀리허브의 AI 비전, LLM 기반 Bixby 탑재 가전(패밀리허브, 에어컨, 로봇청소기, 정수기, 7형 화면 세탁가전, 2026. 03. 31). CES 2026 "보고, 듣고, 말하는 가전"(2026. 01. 06): 냉장고가 목소리를 알아보고 그 사람의 Now Brief를 보여 줌.',
                'SmartThings: 등록 사용자 4억 7천만 명(Samsung Global Newsroom, 2026. 10).',
                'Galaxy Watch가 휴대폰의 알림을 보여 주는 것은 B-7의 근거와 같음.',
                '‘휴대폰이 집에 없으면’의 답은 설계에서 나오는 한계를 그대로 말한 것(색인과 검색을 휴대폰에 두는 구성).']),
    Page('B-5', '왜 온디바이스인가', s_ondev,
         q='왜 꼭 온디바이스여야 하나요? 성능 좋은 서버 LLM을 API로 부르면 되지 않나요?',
         a='온디바이스여야 하는 이유는 두 가지입니다. 휴대폰 속 기록에는 나만 아는 정보와 대화 상대의 정보까지 섞여 있어서, '
           '외부 LLM 서버로 보내는 순간 어디에 남고 어떻게 쓰이는지 사용자가 통제할 수 없습니다. '
           '사용자도 같은 답을 했습니다. 저희 설문에서 80.5%가 내 기록이 휴대폰 안에서만 처리된다면 쓰겠다고 답했고, '
           '서버로 나가도 쓰겠다는 답은 12.4%에 그쳤습니다. '
           '갤럭시는 개인 데이터를 기기 안에서 처리하는 PDE와, 이를 암호화해 지키는 KEEP과 Knox Vault를 갖추고 있고, '
           'Weave도 이 구조 위에서 기록을 밖으로 내보내지 않고 동작합니다.',
         more=[('보안 말고, API로 부르면 무엇이 비효율인가요?',
                '질의할 때마다 관련 기록을 서버로 올리고 답을 기다려야 합니다. 통신이 끊기면 쓸 수 없고, 호출할 때마다 비용이 듭니다. '
                '무엇보다 어떤 기록이 관련 있는지 고르려면 결국 기기 안에서 먼저 찾아야 합니다.'),
               ('삼성의 정책과는 맞나요?', 'Galaxy AI 설정에는 기기에서만 데이터를 처리하게 하는 스위치가 있습니다. Weave는 그 스위치를 켠 상태에서도 그대로 동작합니다.'),
               ('서버 모델보다 답이 나쁘지 않나요?', 'Weave에서 sLLM이 하는 일은 짧은 검색 계획을 쓰고 찾은 기록 몇 건을 요약하는 일입니다. 이런 좁은 일은 작은 모델로도 충분하다는 근거를 D-6에 모았습니다.'),
               ('35쪽처럼 냉장고와 TV로 넘어가면 결국 클라우드로 가는 것 아닌가요?',
                '기억과 색인은 휴대폰 안에 두고, 가전에는 찾아낸 답만 건네는 구성입니다. 누구에게 보여 줄지는 Voice ID로 본인이 확인됐을 때로 한정하고, 어떤 기록을 가전에 건넬지는 사용자가 정합니다. B-4에 정리했습니다.'),
               ('내 기록을 AI가 다 읽는다는 것 자체가 불편하다는 사용자는요?',
                '읽는 범위를 사용자가 정합니다. 처음에는 원하는 앱만 켜 두고 쓰다가, 언제든 앱별로 끄거나 색인을 한 번에 지울 수 있습니다. B-8에 정리했습니다.'),
               ('설문은 누구에게 어떻게 물었나요?',
                '2026년 10월 28일부터 11월 4일까지 온라인으로 210명에게 물었습니다. 갤럭시 사용자가 145명, 아이폰 사용자가 62명입니다. 결과는 B-1에 정리했습니다.')],
         basis=['장과 대본은 팀원(ysy19)의 `apx_new.py`. 10차에 붉은 상자 한 곳을 바꿨고(API 호출의 비효율을 보탬), 11차(11-16)에 팀 검토로 셋을 고침: '
                '①의 글이 오른쪽이 비어 보여 글자를 12 → 13pt로 키우고 가운뎃점을 풀어 씀, ②의 상자 셋(PDE, KEEP, Knox Vault)을 같은 모양으로, ②와 ③의 자리를 바꿈(말할 글의 차례도 함께).',
                'Samsung Newsroom, "Samsung Introduces Future-Ready Mobile Security for Personalized AI Experiences"(2025. 07): "These insights stay entirely on-device, protected by KEEP and further secured by Knox Vault".',
                '설문 13번(210명): 휴대폰 안에서만 처리된다면 쓰겠다 169명(80.5%), 밖으로 보내져도 쓰겠다 26명(12.4%), 어느 쪽이든 쓰지 않겠다 15명(7.1%). CSV로 다시 셈.',
                'Samsung 지원(ANS10000753): Galaxy AI의 "Process data only on device" 스위치. Knox 문서: 클라우드에서 처리하는 기능의 데이터는 모델 학습에 쓰일 수 있음.']),
    Page('B-6', '읽을 수 있는 기록의 범위', s_scope,
         q='한국 사용자는 카카오톡이나 인스타그램 같은 외부 앱을 많이 쓰는데, 그런 앱이 데이터를 열어 주지 않으면 반쪽짜리가 되지 않나요?',
         a='필요한 기록의 대부분은 지금도 읽을 수 있는 범위에 있습니다. Finder를 개발하는 파트에 서면으로 확인했는데, '
           'Finder는 이미 삼성 기본 앱과 PDE가 정리한 예약, 여행, 쿠폰 정보, 계약을 맺은 외부 앱, 웨어러블까지 검색하고 있습니다. Weave는 이 범위에서 시작합니다. '
           '여기에 없는 카카오톡 같은 외부 메신저는 안드로이드의 알림 접근 권한으로 읽습니다. 사용자가 허용한 앱의 받은 메시지를 기기 안에서 색인하는 방식이고, '
           '삼성의 Galaxy Watch 등이 이미 쓰는 권한입니다. 지난 대화나 내가 보낸 메시지는 사용자가 내보낸 대화 파일로 채웁니다.',
         more=[('인스타그램의 메시지도 읽을 수 있나요?', '알림에 메시지 내용이 담기는 앱이면 같은 방식으로 읽습니다. 피드처럼 알림이 오지 않는 화면의 내용은 읽지 않습니다.'),
               ('통화 녹음이나 음성 녹음은요?', 'Weave는 통화 내용을 듣지도 저장하지도 않고, 녹음 파일도 색인하지 않습니다. 사용자가 화면에 직접 입력했을 때만 동작합니다.'),
               ('Finder가 이미 그 범위를 검색하면 Weave는 왜 필요한가요?', 'Finder는 찾은 기록을 목록으로 보여 주고, Weave는 그 기록들을 단서로 이어 답을 만듭니다. A-3에 정리했습니다.'),
               ('외부 앱과 계약이 필요하지 않나요?', '알림 접근과 내보낸 파일은 안드로이드에서 사용자 동의로 동작하는 방식입니다. 다만 상품화할 때는 해당 앱과의 협의가 필요할 수 있습니다.')],
         basis=['11차(11-16)에 새로 넣은 장: 팀 검토의 예상 질문 5번(서드파티 데이터 권한). 어떤 앱은 이미 되고 어떤 앱은 알림으로 간접적으로 되는지를 한 장에.',
                '11-16 저녁: 서드파티 앱을 장점으로 적은 문장을 뺌(사용자의 지시: 협약이 필요할 수도 있음). ‘외부 메신저는 제휴를 기다리지 않고 알림으로 읽습니다’, ‘제휴하면 그만큼 범위가 넓어집니다’, ‘외부 앱과의 제휴를 기다리지 않아도 시작할 수 있고’를 빼고, 협의를 묻는 물음에는 협의가 필요할 수 있다고 답함.',
                'Finder의 범위는 Finder 개발 파트장의 서면 답변(2026. 11, 사용자가 전달)을 표로 옮긴 것: 삼성 기본 기능(설치된 앱, 설정, 연락처, 캘린더, 갤러리, 노트, 파일, 음성 녹음 등), '
                'PDE 개인 정보(예약, 여행, 쿠폰 등), 계약을 맺은 외부 앱(Spotify, Melon, YouTube, Netflix, TikTok), 웨어러블 기기와 스토어. 답변의 원문과 답한 분의 이름은 적지 않음(사용자: 성함까지는 필요 없음, 11-17).',
                '11-17 저녁(사용자의 지시): 표의 셋째 줄을 구분 ‘서드파티 앱’, 검색 대상 ‘계약을 맺은 외부 앱’으로 바꿈. 앱 이름 다섯은 화면에서 빠지고 이 근거에만 남음. '
                '둘째 카드의 ‘예약, 여행, 쿠폰. PDI가 앱의 알림에서 모아 둔 정보’를 ‘예약, 여행, 쿠폰 앱의 알림에서 모아 둔 정보 등’으로, 아래 요점의 ‘삼성의 PDI와 Galaxy Watch가’를 ‘삼성의 Galaxy Watch 등이’로 바꿈. '
                '말할 답의 같은 문장도 화면에 맞춰 ‘삼성의 Galaxy Watch 등이 이미 쓰는 권한입니다’로 고침. PDI의 설명은 B-7과 A-8에 그대로 있음.',
                'Finder 사용 통계는 A-3의 Q2에 비율(앱 검색 67%, 다른 용도로 한 번 이상 55% 이하)로 넣음(11-17, 사용자의 지시. 처음에는 Q3이었고 그날 저녁에 Q2와 자리를 바꿈). 11차부터 13차까지는 사내 수치라 따로 만든 덱의 이 장에만 넣었음. '
                '원래 값은 `원본/사내자료.json`(저장소에 올리지 않음)에만 둠.',
                '알림으로 읽는 방법과 근거(NotificationListenerService, Samsung PDI)는 B-7. Weave가 읽는 삼성 기본 앱의 목록은 B-8과 시나리오(문자, 연락처)에 맞춤.',
                'Finder의 범위에는 음성 녹음이 있지만 Weave는 녹음을 색인하지 않는 것으로 적음: 사용자의 기준(통화 녹음과 음성 녹음은 근거로 쓰지 않음, 11-03)과 B-8의 ‘통화 내용은 듣지도 저장하지도 않습니다’에 맞춤(Carbon이 짚은 어긋남, 11-16).']),
    Page('B-7', '카카오톡을 읽는 방법', s_kakao,
         q='카카오톡은 삼성 앱이 아닌데, 대화를 어떻게 읽나요?',
         a='받는 메시지는 알림으로 읽고, 지난 대화는 사용자가 내보낸 파일로 읽습니다. '
           '알림은 사용자가 허용한 앱의 것만 도착할 때마다 기기 안에서 색인하고, 내보낸 파일은 사용자가 직접 고른 대화방만 대상이 됩니다. '
           '새로운 방식은 아닙니다. 삼성의 PDI가 이미 카카오톡과 WhatsApp 같은 앱의 알림에서 예약 정보를 모아 Finder와 Now Brief에 쓰고 있고, '
           'Galaxy Watch가 휴대폰 알림을 보여 주는 것도 같은 권한입니다. '
           'Weave는 이미 쓰이는 경로 위에서, 읽는 범위를 예약 정보에서 대화 속 단서로 넓힙니다. '
           '알림은 받은 메시지에만 오기 때문에, 내가 보낸 말이나 알림을 꺼 둔 대화방은 사용자가 내보낸 파일로 채웁니다.',
         more=[('내가 보낸 메시지는 못 읽는 것 아닌가요?', '맞습니다. 알림은 받은 메시지에만 옵니다. 그래서 시나리오의 단서는 모두 상대가 보낸 메시지로 잡았습니다. 내가 보낸 말까지 필요하면 내보낸 파일로 읽습니다.'),
               ('알림을 꺼 둔 단체방은요?', '읽지 않습니다. 필요하면 사용자가 그 대화방을 내보내서 색인할 수 있습니다.'),
               ('PC 카카오톡을 쓰는 동안은요?', 'PC 카카오톡을 쓰는 동안에는 휴대폰 알림이 늦게 옵니다. 그 사이의 대화도 내보낸 파일로 채울 수 있습니다.'),
               ('카카오와 협의가 있어야 하나요?', '알림 접근과 내보낸 파일은 안드로이드에서 사용자 동의로 동작하는 방식입니다. 다만 상품화할 때는 카카오와의 협의가 필요할 수 있습니다.'),
               ('키보드나 접근성 권한으로 화면을 읽는 건가요? 약관 문제는 없나요?',
                '화면을 읽지 않습니다. 사용자가 허용한 알림 접근 권한과 직접 내보낸 파일만 씁니다. 삼성 PDI와 Galaxy Watch가 이미 쓰는 권한입니다.')],
         basis=['Android Developers, "NotificationListenerService": 사용자가 알림 접근을 허용한 앱은 다른 앱의 알림 내용을 받을 수 있음.',
                'Samsung 지원 "Understanding Finder on Galaxy phones": "Personal data intelligence (PDI): This feature collects reservation details from notifications in apps like Messages, Gmail, Naver, Line, WhatsApp, KakaoTalk, and Wallet." 회상 카드: "relevant reservation information is displayed in a card format at the top".',
                'Galaxy S26 발표문의 Now Brief 각주: "Recalled data available from supported app notifications, Messages, Gmail and Samsung Wallet".',
                '카카오톡 대화 내용 내보내기: 채팅방 설정 > 대화 내용 내보내기 > 모든 메시지 내부저장소에 저장. 내 파일의 KakaoTalk 폴더 안 Chats에 저장됨(삼성전자서비스와 삼성 커뮤니티의 안내).',
                'Galaxy Watch: Galaxy Wearable 앱이 휴대폰의 알림 접근 권한을 받아 워치에 알림을 보여 줌(Samsung 지원과 개발자 문서의 안내).',
                '11차(11-16): Q3 ‘내가 보낸 메시지는 읽지 못하는 것 아닌가요?’를 ‘알림으로 읽는 방식의 한계는 무엇이고, 어떻게 채우나요?’로 바꿈(팀 검토: Q3을 지우고 새 질문으로 바꾸거나 나머지를 더 자세히). '
                '‘더 물으면’에 있던 알림을 꺼 둔 대화방과 PC 카카오톡의 답을 화면으로 올리고, Q1에는 알림에서 받는 것(보낸 사람, 내용, 시각)을, Q2에는 화면과 저장소를 읽지 않는다는 말을 보탬.']),
    Page('B-8', '권한과 사생활 보호', s_data,
         q='내 대화와 사진을 AI가 다 읽고 엮는다는 게 불안한데, 사생활은 어떻게 지키나요?',
         a='읽는 범위는 사용자가 정하고, 읽은 것은 기기 밖으로 나가지 않습니다. 삼성 기본 앱은 사용자 동의 아래 기기 안에서 연동하고, '
           '카카오톡 같은 외부 메신저는 사용자가 허용한 알림만 색인합니다. 통화 내용은 듣지도 저장하지도 않습니다. '
           '원본 기록과 색인은 모두 기기 안에만 저장하고, 암호화 키는 하드웨어 보안 영역에 둡니다. 원본을 지우면 색인도 함께 지웁니다. '
           '그럼에도 불안하다면 처음에는 원하는 앱만 켜 두고 쓰다가, 언제든 앱별로 끄거나 색인을 한 번에 지울 수 있습니다.',
         more=[('사용자는 이 방식을 받아들이나요?', '저희 설문에서 80.5%가 내 기록이 휴대폰 안에서만 처리된다면 쓰겠다고 답했습니다. 서버로 나가도 쓰겠다는 답은 12.4%였습니다. B-5에 정리했습니다.'),
               ('배터리는 괜찮나요?', '처음의 대량 색인은 충전 중이거나 기기가 쉴 때만 합니다. 쓰는 동안에는 가벼운 벡터 검색과, 추려진 기록 한두 건에 대한 sLLM만 실행합니다.'),
               ('기록을 지우면 색인은요?', '원본을 지우면 그 기록의 벡터와 메타데이터도 함께 지웁니다.'),
               ('하루에 기록이 수백, 수천 건 쌓이는데 배터리는 괜찮나요?',
                '새 기록 한 건을 색인하는 데는 임베딩 한 번, 8밀리초가 듭니다. 하루 1,000건이면 8초입니다. 사진처럼 무거운 것은 충전 중에 모아서 합니다.'),
               ('휴대폰을 바꾸면 색인은 어떻게 옮기나요?',
                '새 Galaxy로 바꾸면 Smart Switch로 원본 기록을 옮긴 뒤 새 기기에서 색인을 다시 만듭니다. 텍스트 기록 10만 건을 다시 색인하는 데 13분 정도입니다. 그래서 이어 둔 기억은 Galaxy끼리는 그대로 이어집니다.'),
               ('가족이 함께 보는 TV나 냉장고에 개인 기록이 뜨면요?',
                '가전에는 찾아낸 답만 건네고 대화 원문은 건네지 않습니다. 누구에게 보여 줄지는 Voice ID로 본인이 확인됐을 때로 한정하고, 어떤 앱의 기록을 가전에 건넬지는 사용자가 정합니다.')],
         basis=['How it works Appendix에 있던 장(q_data)의 내용을 질문과 답 세 줄로 다시 짬. Android Developers: NotificationListenerService, WorkManager(RequiresCharging, RequiresDeviceIdle), Android Keystore.',
                '8ms × 1,000건 = 8초(텍스트 기록 기준). 11차(11-16)에 하루 300건을 1,000건으로, ‘새 메시지’를 ‘새 기록’으로 바꿈(팀 검토).',
                'Q3 끝의 ‘그럼에도 불안하다면 …’은 11차에 팀 검토로 붙인 문장(Carbon의 안을 줄여 씀).',
                '설문 13번(210명): 휴대폰 안에서만 처리된다면 쓰겠다 169명(80.5%). 예상 질문 6번(프라이버시 거부감)의 답으로 B-5와 이 장을 함께 씀. 설문 숫자는 이 장의 화면에 없어 ‘더 물으면’으로 옮김(Carbon의 지적).',
                'Q2의 8ms는 글로 된 기록 한 건의 값이어서 화면에 ‘글 기준’이라고 적고 사진 색인은 충전 중이라고 적음(Carbon의 지적).']),
    Page('B-1', '사용자 설문조사 결과', s_survey,
         q='설문은 누구에게 어떻게 물었고, 무엇을 확인했나요?',
         a='올해 10월 28일부터 11월 4일까지 온라인으로 210명에게 물었습니다. 갤럭시 사용자가 145명, 아이폰 사용자가 62명입니다. 확인한 것은 세 가지입니다. '
           '첫째, 기록을 찾지 못하는 불편은 일상적입니다. 83.8%가 어느 앱에 남겼는지 몰라 앱을 하나씩 열어 봤고, 93.8%가 정확한 이름이 떠오르지 않아 검색으로 찾지 못했고, '
           '82.4%가 챙겨야 할 부탁이나 약속을 나중에야 떠올렸습니다. '
           '둘째, 이름 대신 기억하는 것은 날짜와 장소, 상황, 사람 같은 단서입니다. 그래서 이름이 떠오르지 않았던 사람의 94.9%는 지금도 단서가 될 다른 기록부터 직접 차례로 찾아보고 있습니다. '
           '셋째, 80.5%는 내 기록이 휴대폰 안에서만 처리된다면 쓰겠다고 답했습니다.',
         more=[('응답자가 한쪽으로 치우치지 않았나요?',
                '온라인으로 모은 210명입니다. 갤럭시 사용자와 아이폰 사용자, 20대 이하와 30대, 50대 이상으로 나눠 봐도 세 가지 불편은 모두 77% 이상이었습니다. 40대는 5명이어서 따로 비교하지 않았습니다.'),
               ('아이폰 사용자도 같은 불편을 겪나요?', '겪습니다. 아이폰 사용자 62명 가운데 61명이 정확한 이름이 떠오르지 않아 찾지 못한 적이 있다고 답했고, 60명이 기록을 찾아 주는 AI를 쓰겠다고 답했습니다. B-2에 정리했습니다.'),
               ('기본 검색 기능은 얼마나 쓰나요?', '자주 쓴다는 답은 33.8%였습니다. 가끔 쓴다가 36.2%이고, 나머지 30%는 거의 쓰지 않거나 써 본 적이 없거나 있는 줄 몰랐다고 답했습니다.'),
               ('다시 찾는 데 시간을 얼마나 쓰나요?', '일주일에 5분에서 15분이라는 답이 45.7%로 가장 많았고, 15분 이상이라는 답이 23.8%였습니다.'),
               ('기록은 주로 어디에 남기나요?', '화면 캡처가 76.7%, 카카오톡의 나와의 채팅이 75.7%, 메모 앱이 65.2%입니다. 한 사람이 평균 3.8곳에 나눠 남기고, 세 곳 이상에 남기는 사람이 74.8%입니다.'),
               ('단서를 둘로 나눈 기준은 무엇인가요?', '날짜와 장소, 사람은 기록에 붙어 있는 메타데이터라서 필터로 거릅니다. 상황이나 눈으로 본 모습, 대화의 일부는 기록의 내용이라서 Reasoning Embedding으로 찾습니다. C-4에 정리했습니다.')],
         basis=['13차(11-17)에 새로 넣은 장. 사용자의 지시: "설문조사 결과 한눈에 시각화한 페이지를 하나 만들면 좋을 것 같아"(11차의 ‘직접 측정하거나 확인한 것’ 장을 빼는 대신).',
                '숫자는 모두 `12_설문/갤럭시AI 신규 기능 개발을 위한 사용자 설문.csv`를 11-17에 문항마다 다시 집계한 값. 응답 210건(구글 폼 194, 사내 게시판 16), 2026-10-28 ~ 11-04. 비율의 분모는 210명(본 발표 7쪽과 33쪽의 93.8%, 83.8%, 82.4%와 같음). 94.9%만 본 발표 8쪽과 같이 197명이 분모.',
                '2번 연령: 20대 이하 73, 30대 47, 40대 5, 50대 이상 85. 3번 기기: 삼성 갤럭시 145, 애플 아이폰 62, 그 외 3.',
                '4번(복수 선택): 화면 캡처 161(76.7%), 카카오톡 나와의 채팅 159(75.7%), 메모 앱 137(65.2%), 사진 촬영 125(59.5%), 캘린더 112(53.3%), 지도 앱 저장 54(25.7%), 이메일 31(14.8%). 평균 3.76곳, 2곳 이상 192명(91.4%), 3곳 이상 157명(74.8%).',
                '5번(어느 앱에 남겨 뒀는지 기억나지 않아 하나씩 열어 봄) 예 176. 6번(정확한 이름이 떠오르지 않아 검색으로 바로 찾지 못함) 예 197, 아니오 12, 무응답 1. '
                '9번(부탁, 약속을 챙겨야 할 때 떠올리지 못하고 나중에야 생각남) 예 173, 아니오 36, 무응답 1. 10번("찾아보고 다시 알려 줄게"라고 함) 예 188.',
                '넷 가운데 하나 이상에 예라고 답한 사람 209명(99.5%), 5번과 6번과 9번에 모두 예라고 답한 사람 150명(71.4%), 넷 모두 146명(69.5%).',
                '7번(복수 선택): 언제였는지 124(59.0%), 어디였는지 120(57.1%), 어떤 상황이었는지 102(48.6%), 관련된 사람 100(47.6%), 눈으로 본 모습 83(39.5%), 주고받은 대화 일부 76(36.2%). 평균 2.90개.',
                '8번(단서가 될 만한 다른 기록부터 차례로 찾아봄): 그렇게 해서 찾았다 176, 그래도 결국 못 찾았다 22, 없다 12 → 있다 198명(전체의 94.3%). 6번에 예라고 답한 197명 가운데서는 187명(94.9%)이고 화면과 답에는 본 발표 8쪽(“그중 94.9%는 단서가 될 기록부터 직접 여러 앱을 뒤져 다시 찾고 있었습니다”)과 같은 이 숫자를 적음.',
                '11번(일주일 동안 다시 찾는 데 쓰는 시간): 5분 미만 64(30.5%), 5~15분 96(45.7%), 15~30분 34, 30분~1시간 6, 1~2시간 6, 2시간 이상 4 → 15분 이상 50명(23.8%). '
                '12번(기본 검색 기능): 자주 71(33.8%), 가끔 76(36.2%), 거의 쓰지 않음 30, 있는 줄은 알지만 써 본 적 없음 16, 있는 줄 몰랐음 17.',
                '13번: 휴대폰 안에서만 처리된다면 쓰겠다 169(80.5%), 서버로 보내져도 쓰겠다 26(12.4%), 쓰지 않겠다 15(7.1%).',
                '기기와 연령대별(5번, 6번, 9번에 예): 갤럭시 86.9%, 91.7%, 84.8%. 아이폰 77.4%, 98.4%, 79.0%. 20대 이하 82.2%, 97.3%, 79.5%. 30대 80.9%, 93.6%, 80.9%. 50대 이상 85.9%, 90.6%, 84.7%.',
                '단서를 둘로 나눈 것(메타데이터로 거르는 날짜, 장소, 사람과 내용으로 찾는 상황, 모습, 대화)은 내 정리: 색인에 붙이는 메타데이터가 시각, 앱, 보낸 사람, 장소여서(C-4).',
                '12_설문 폴더의 분석 그림(설문분석_210명_한눈에.png)은 일부 문항의 분모가 209명이어서(94.3%, 82.8%) 숫자를 가져오지 않고 본 발표와 같은 분모로 다시 셈함.']),
    Page('B-2', '사업 효과', s_biz,
         q='기본 기능으로 넣으면 개발 비용만 드는 것 아닌가요? 사업적으로는 무엇이 남나요?',
         a='세 가지입니다. 첫째, 쓸수록 Galaxy를 떠나기 어려워집니다. 사람들은 한 달에 평균 41개의 앱을 쓰고, 69%는 기록을 지우지 않고 쌓아 둡니다. '
           '사진과 메모는 다른 휴대폰으로 옮길 수 있지만, Weave가 그 사이를 이어 둔 기억은 Galaxy끼리만 옮길 수 있습니다. '
           '둘째, 새로운 사용자가 Galaxy를 고를 이유가 됩니다. 기록을 찾지 못하는 불편은 기기를 가리지 않습니다. '
           '저희 설문에서 아이폰을 쓰는 응답자 62명 중 61명이 같은 불편을 겪었고, 60명이 기록을 찾아 주는 AI가 있다면 쓰겠다고 답했습니다. '
           '셋째, 쓸수록 비용이 늘어나는 구조가 아닙니다. Weave는 온디바이스 방식이기에 사용자가 많아지고 서비스를 많이 사용해도 비용이 늘지 않습니다. '
           '비용 투자는 초기 개발 단계에만 발생하고, 갤럭시 사용자가 많아질수록 1인당 총비용은 오히려 낮아집니다.',
         more=[('적용하는 데 비용이 많이 들지 않나요?',
                '새 부품이 필요 없는 소프트웨어입니다. Galaxy AI가 들어가는 기기는 올해 말 8억 대이고, 업데이트만으로 적용할 수 있습니다. '
                '새로 탑재하는 모델은 임베딩 하나이고, sLLM은 기기에 탑재된 Gauss를 그대로 씁니다. D-1과 D-2에 정리했습니다.'),
               ('돈을 받을 수 있는 기능인가요?', '기능 하나로 과금하기보다, Galaxy AI의 한 축으로 기기를 고르고 계속 쓰게 하는 이유로 봅니다.'),
               ('아이폰 사용자 60명이 갤럭시로 바꾸겠다고 한 건가요?', '아닙니다. 기록을 찾아 주는 AI를 쓰겠다는 답입니다. 이 필요가 기기를 가리지 않는다는 근거로만 씁니다.'),
               ('10대 숫자는 무슨 뜻인가요?', '한국갤럽 조사에서 지금 Galaxy를 쓰는 10대는 61%인데, 다음에 사고 싶은 휴대폰으로 Galaxy를 고른 10대는 47%였습니다. 다음 세대가 Galaxy를 고를 이유가 더 필요하다는 뜻으로 읽었습니다.'),
               ('Galaxy끼리만 옮길 수 있다는 건 무슨 뜻인가요?', '새 Galaxy로 바꾸면 Smart Switch로 원본 기록을 옮기고 색인을 다시 만들어 그대로 이어 씁니다. 다른 회사의 휴대폰에는 Weave가 없어서 이어 둔 기억을 쓸 수 없습니다.'),
               ('69%는 무슨 숫자인가요?', '영국 조사에서 스스로를 디지털 호더라고 답한 비율입니다. 늘 그렇다는 답과 가끔 그렇다는 답을 더한 값입니다.'),
               ('새로 탑재하는 모델은 무엇인가요?', '임베딩 모델 하나이고 약 0.19기가바이트입니다. sLLM은 기기에 탑재된 Gauss를 그대로 쓰고, 그 위에 수십 메가바이트의 어댑터를 얹습니다. D-1과 D-2에 정리했습니다.')],
         basis=['Ofcom, "Online Nation 2025"(2025. 12): 영국 18세 이상 스마트폰 이용자가 한 달에 쓰는 앱은 평균 41개.',
                'Compare and Recycle, "Digital Declutter Statistics 2025": 스스로를 디지털 호더로 여기는 비율 69%(늘 26%, 가끔 42%).',
                '자체 설문(210명) 가운데 아이폰 사용자 62명: 6번(정확한 이름이 떠오르지 않아 검색으로 찾지 못한 경험) 예 61명. 13번에서 휴대폰 안에서만 처리된다면 쓰겠다 52명, 밖으로 보내져도 쓰겠다 8명, 쓰지 않겠다 2명.',
                '한국갤럽 「스마트폰 관련 조사 2012-2026」(2026. 07): 13~18세 200명, 지금 삼성 61%, 다음에 사고 싶은 휴대폰 삼성 47%.',
                'Galaxy AI 기기: 2025년 말 4억 대 → 2026년 말 8억 대(Reuters 2026. 01. 05 인터뷰, Galaxy Unpacked 2026. 02와 07).',
                '숫자와 문장은 9차에 본 발표에서 뺀 비즈니스 임팩트 장과 그 후보(biz_new.py)의 것. 11차(11-16)에 팀 검토로 Q1의 ‘옮길 수 없습니다’를 ‘갤럭시끼리만 옮길 수 있습니다’로 바꾸고, '
                'Q2의 답을 그 후보 장(‘다음 세대가 갤럭시를 고를 이유’)의 흐름으로 보완함: 같은 불편 61명 → 쓰겠다 60명 → 다음 세대가 고를 이유. 이탈률이나 매출 추정치는 넣지 않음(검토에서 필요 없다고 함).',
                '14차(11-17 밤, 사용자의 글): Q3을 ‘해당 AI 서비스를 사용하는 데 비용이 계속 들지 않나요?’와 그 답(온디바이스라 쓸수록 비용이 늘어나는 구조가 아니고, 사용자가 많아질수록 1인당 총비용이 낮아짐)으로 바꿈. '
                '13차까지의 Q3(‘적용하는 데 비용이 많이 들지 않나요?’와 새 부품이 필요 없는 소프트웨어라는 답)은 ‘더 물으면’으로 옮김. 그림의 ‘0원’은 기기 안에서 처리해 질의가 늘어도 서버 추론 비용이 더 들지 않는다는 뜻으로 내가 적은 것이고, 8억 대와 각주 ⁵는 그대로.',
                '13차(11-17): Q3의 ‘1단계인 기록 통합 검색은 새로 튜닝할 모델도 없습니다’와 그림의 ‘0개’를 뺌(1년 계획 장이 UX를 단계로 나누지 않게 되어서). 대신 새로 탑재하는 모델이 임베딩 하나(약 0.19GB)라는 것을 적음.']),
]
