"""Appendix B 묶음: 상품화 (11-16 3판).

B-1 왜 온디바이스인가(팀원 ysy19의 apx_new.s_ondevice), B-2 카카오톡 같은 외부 앱의 대화를 읽는 방법(알림과 내보낸 파일, 이미 쓰이는 방식이라는 근거),
B-3 데이터 접근 권한과 사생활 보호, B-4 메모리, B-5 속도 1(기준 모델과 검색 시간), B-6 속도 2(UX별 응답 시간), B-7 단계적 적용, B-8 사업 효과.
3판: B-2, B-3, B-8은 질문과 답 세 줄 + 작은 그림. B-4는 메모리 띠 + 표 하나, B-5는 기준 모델 표 + Hop의 내역 막대, B-6은 UX별 시간 띠 + 구성별 표, B-7은 단계 흐름 + 짧은 설명.
시간은 `qna_num.py`가 셈한다: EmbeddingGemma 2를 Galaxy S26 Ultra NPU에서 잰 8ms가 기준이고, 같은 모델의 모델 카드 값(GPU 25.9ms, CPU 27.1ms)과의 비율로
GPU나 CPU에서 잰 sLLM의 공개 측정값을 NPU 값으로 환산한다(11-16 사용자의 지시). NPU에서 잰 Gemma 3 1B는 그대로 쓴다. 근거는 `Appendix_QnA_대본.md`.
"""
from pathlib import Path

from ui import (BODY, INK, LAV, MUTE, PURPLE, RING, SUB, C, R, T)

import qna_num as NUM
from qna_lib import (Page, data_row, footnote, frame, hbars, label, notes3, page_slide, panel, pipeline, points, qrow, rich, tbl, timebar, vis_nums, vis_rows, vis_text)

HERE = Path(__file__).resolve().parent
X, W = 70, 1140


# ------------------------------------------------------------------ B-1 (팀원의 장)
def s_ondev():
    import apx_new
    return frame(apx_new.s_ondevice(), 'B-1')


# ------------------------------------------------------------------ B-2 카카오톡 같은 외부 앱의 대화를 읽는 방법
def s_kakao():
    s = page_slide('qb_kakao', 'B-2', [('카카오톡 같은 외부 앱의 대화를 읽는 방법', INK)])
    y, h, gap = 100, 150, 14
    qrow(s, 'qb/q1', y, h, '카카오톡은 삼성 앱이 아닌데 대화를 어떻게 읽나요?',
         '두 가지 경로로 읽습니다. **받는 메시지는 알림**으로 읽습니다. 사용자가 허용한 앱의 알림 내용만, 도착할 때마다 기기 안에서 색인합니다. '
         '**지난 대화는 사용자가 내보낸 파일**로 읽습니다. 사용자가 직접 고른 대화방만 대상입니다.',
         n=1, vis=vis_rows([('받는 메시지', 'Android의 알림 접근 권한¹'), ('지난 대화', '카카오톡의 ‘대화 내용 내보내기’ 파일²'), ('읽지 않는 것', '알림을 꺼 둔 대화방, 화면의 내용')], kw=86))
    qrow(s, 'qb/q2', y + h + gap, h, '이미 쓰이는 방식인가요? 권한이나 약관 문제는 없나요?',
         '새 권한을 만들지 않습니다. 삼성의 Personal Data Intelligence가 이미 카카오톡, WhatsApp, Line, Gmail의 **알림에서 예약 정보를 모아** Finder와 Now Brief에 쓰고 있습니다.³ '
         'Galaxy Watch가 휴대폰의 알림을 보여 주는 것도 같은 권한입니다.',
         n=2, vis=vis_rows([('Samsung PDI', '앱 알림에서 예약 정보를 수집³'), ('Now Brief', '알림으로 받은 정보를 요약에 사용'), ('Galaxy Watch', '휴대폰의 알림을 워치에 표시')], kw=96))
    qrow(s, 'qb/q3', y + 2 * (h + gap), h, '내가 보낸 메시지는 읽지 못하는 것 아닌가요?',
         '맞습니다. 알림은 받은 메시지에만 옵니다. 그래서 시나리오의 단서는 모두 **상대가 보낸 메시지**로 잡았습니다. 내가 보낸 말까지 필요하면 내보낸 파일로 읽습니다.',
         n=3, vis=vis_text([[('UX2  ', dict(color=PURPLE, weight='b')), ('지은의 메시지 ‘휴지 안 사 와도 돼’', dict(color=INK))],
                            [('UX3  ', dict(color=PURPLE, weight='b')), ('아내의 메시지 ‘동생이 이 갈색병 좋대’', dict(color=INK))],
                            [('두 단서 모두 받은 메시지여서 알림으로 읽을 수 있음', dict(color=SUB))]]))
    footnote(s, ['¹ Android Developers, "NotificationListenerService"   ² 삼성전자서비스 안내: 채팅방 설정에서 대화 내용 내보내기를 누르면 내 파일의 KakaoTalk 폴더에 저장됨',
                 '³ Samsung 지원, "Understanding Finder on Galaxy phones": "Personal data intelligence (PDI): This feature collects reservation details from notifications in apps like '
                 'Messages, Gmail, Naver, Line, WhatsApp, KakaoTalk, and Wallet."'], y + 3 * h + 2 * gap + 12)
    return s


# ------------------------------------------------------------------ B-3 데이터 접근 권한과 사생활 보호
def s_data():
    s = page_slide('qb_priv', 'B-3', [('데이터 접근 권한과 사생활 보호', INK)])
    y, h, gap = 100, 150, 14
    qrow(s, 'qb/q1', y, h, '어떤 기록을 어떤 권한으로 읽나요?',
         '삼성 기본 앱(갤러리, 노트, 캘린더, 메일, 월렛)은 사용자의 동의를 받아 기기 안에서 연동합니다. 카카오톡 같은 외부 메신저는 **사용자가 허용한 알림만** 색인합니다.¹ '
         '통화 내용은 듣지도 저장하지도 않습니다.',
         n=1, vis=vis_rows([('삼성 앱', '사용자 동의 후 기기 안에서 연동'), ('외부 앱', '허용한 알림만 색인 (B-2)'), ('통화', '듣지도 저장하지도 않음')], kw=72))
    qrow(s, 'qb/q2', y + h + gap, h, '배터리와 발열은 괜찮나요?',
         '처음의 대량 색인은 **충전 중이거나 기기가 쉴 때만** 백그라운드로 실행합니다.² 평소에는 새 메시지 한 건에 임베딩 한 번(EmbeddingGemma 2, 8ms)과, 질의할 때 추려진 기록 몇 건에 대한 sLLM만 실행합니다.',
         n=2, vis=vis_nums([('8ms', ['새 메시지 1건의', '색인']), ('2.4초', ['하루 300건을', '색인하는 시간'])], pt=20))
    qrow(s, 'qb/q3', y + 2 * (h + gap), h, '사생활은 어떻게 지키나요?',
         '원본 기록과 색인은 모두 **기기 안에만** 저장하고, 암호화 키는 하드웨어 보안 영역에 둡니다.³ 어느 앱을 색인할지와 색인을 지우는 일은 사용자가 언제든 정할 수 있습니다.',
         n=3, vis=vis_rows([('저장', '원본과 색인 모두 기기 안'), ('제어', '앱별 색인 허용, 색인 초기화'), ('삭제', '원본을 지우면 색인도 함께 삭제')], kw=56))
    footnote(s, ['¹ Android Developers, "NotificationListenerService"   ² Android Developers, "WorkManager: Define work requests" (RequiresCharging, RequiresDeviceIdle)   '
                 '³ Android Developers, "Android Keystore system"'], y + 3 * h + 2 * gap + 12)
    return s


# ------------------------------------------------------------------ B-4 메모리
RAM, GAUSS, ADD = 12.0, 3.7, 0.25             # GB: Galaxy S26 Ultra, 3B급 4비트 sLLM, Weave가 더하는 것(임베딩 0.19 + 색인 0.026 + Adapter 수십 MB)
B4 = [['Reasoning Embedding', '약 0.19GB', 'EmbeddingGemma 2의 텍스트 구성을 Pixel 11 Pro에서 잰 값(191MB)¹. 사진 내용까지 색인하는 전체 구성은 약 0.57GB이고, 충전 중에 색인할 때만 올림'],
      ['벡터 색인 (Vector Index)', '26MB²', '기록 10만 건 기준 (256-dim int8). 1만 건 2.6MB, 100만 건 256MB. 저장 공간에 두고 필요한 부분만 메모리에 올림'],
      ['Query Rewriter Adapter', '수십 MB³', 'Gauss에 얹는 LoRA Adapter. 기능마다 갈아 끼움'],
      ['sLLM (Samsung Gauss)', '추가 없음', '기기에 탑재된 모델을 공유. 같은 크기의 공개 모델 Llama 3.2는 3B가 약 3.7GB, 1B가 약 1.9GB (4비트, OnePlus 12에서 잰 값)⁴']]


def s_mem():
    s = page_slide('qb_mem', 'B-4', [('메모리 사용량', INK)])
    y, h = 104, 46
    wa = round(ADD / RAM * W)
    wg = round(GAUSS / RAM * W)
    wr = W - wa - wg - 8
    s.add('qb/m', [R('qb/m/rest', X, y, wr, h, prst='roundRect', radius=10, fill='EFECF4', line=None),
                   T('qb/m/rest/t', X + 18, y, wr - 36, h, '시스템과 다른 앱', size=12, color=SUB, anchor='ctr'),
                   R('qb/m/gauss', X + wr + 4, y, wg, h, prst='roundRect', radius=10, fill=LAV, line=RING, line_w=1.2),
                   T('qb/m/gauss/t', X + wr + 4, y, wg, h, '탑재된 sLLM 약 3.7GB (Llama 3.2 3B 기준⁴)', size=11, color=PURPLE, weight='b', align='c', anchor='ctr'),
                   R('qb/m/add', X + W - wa, y, wa, h, prst='roundRect', radius=7, fill=PURPLE, line=None),
                   C('qb/m/lead', [(X + W - wa / 2, y + h + 2)] * 2 + [(X + W - wa / 2, y + h + 14)] * 2, color=PURPLE, w=1.6),
                   T('qb/m/add/t', X + W - 620, y + h + 12, 620, 26, [[('Weave가 새로 더하는 메모리 ', dict(color=INK)), ('약 0.25GB', dict(color=PURPLE)), (' (12GB의 2%)', dict(color=INK))]],
                     size=14, weight='b', align='r', anchor='ctr'),
                   T('qb/m/all', X, y + h + 12, 400, 26, 'Galaxy S26 Ultra의 메모리 12GB⁵', size=11.5, color=SUB, anchor='ctr')])
    y += h + 12 + 26 + 20
    y += tbl(s, 'qb/t', X, y, W, [22, 13, 65], ['구성 요소', '메모리', '설명'], B4, pady=10, hi=(0, 1, 2)) + 20
    y += points(s, 'qb/p', X, y, W, ['**가장 무거운 sLLM은 새로 싣지 않습니다.** 가벼운 임베딩 모델과 색인, Adapter만 더합니다.',
                                    '**글로 질의할 때는 텍스트 구성만 올립니다.** 사진의 벡터는 충전 중에 미리 만들어 두기 때문입니다.'], gap=8) + 14
    footnote(s, ['¹ Google, "EmbeddingGemma 2" (2026. 10): Pixel 11 Pro에서 텍스트 가중치 약 191MB, 전체 약 567MB   ² 256-dim int8 벡터로 셈한 값   '
                 '³ Apple, On-Device Foundation Models (2024. 06): Adapter 하나는 수십 MB',
                 '⁴ ExecuTorch 공개 측정 (Llama 3.2 3B와 1B, 4비트, OnePlus 12): 3,726MiB, 1,921MiB   ⁵ 256GB와 512GB 모델은 12GB, 1TB 모델은 16GB'], y)
    return s


# ------------------------------------------------------------------ B-5 속도 ①: 기준 모델과 검색 시간
def _tok(v):
    return '초당 %d토큰' % round(v)


B5_MODELS = [['EmbeddingGemma 2 (텍스트 2.7억)', 'Galaxy S26 Ultra', '모델 카드: GPU 25.9ms, CPU 27.1ms¹', ('**NPU 실측 8ms** (GPU의 %.1f배, CPU의 %.1f배)' % (NUM.R_GPU, NUM.R_CPU), dict(color=INK))],
             ['Gemma 3 1B', 'Galaxy S25 Ultra NPU', '출력 ' + _tok(NUM.G1B.dec) + '²', ('**NPU 실측** 그대로 ' + _tok(NUM.G1B.dec_npu), dict(color=INK))],
             ['Gemma 4 E2B', 'Galaxy S26 Ultra GPU', '출력 ' + _tok(NUM.E2B.dec) + '²', 'NPU 환산 %s (× %.1f)' % (_tok(NUM.E2B.dec_npu), NUM.R_GPU)],
             ['FunctionGemma 270M', 'Galaxy S25 Ultra CPU', '출력 ' + _tok(NUM.FG.dec) + '²', 'NPU 환산 %s (× %.1f)' % (_tok(NUM.FG.dec_npu), NUM.R_CPU)]]
HOP = [('임베딩: EmbeddingGemma 2, NPU 실측', 8, '8ms', True), ('벡터 검색: 기록 10만 건³', 10, '10ms', False), ('필터링, Slot 채우기', 2, '2ms', False)]
B5_SCALE = [['Hop 1회', '약 0.01초', '0.02초', '약 0.11초'], ['벡터 색인의 크기', '2.6MB', '26MB', '256MB']]


def s_speed():
    s = page_slide('qb_speed', 'B-5', [('속도 1: 기준 모델과 검색 시간', INK)])
    y = 98
    y += label(s, 'qb/l0', X, y, '시간을 셈한 기준 모델과 NPU 기준 값') + 4
    y += tbl(s, 'qb/tm', X, y, W, [26, 20, 26, 28], ['모델', '측정한 기기', '공개 측정값', 'NPU 기준'], B5_MODELS, pady=8, hi=(0,)) + 8
    y += rich(s, 'qb/rn', X, y, W, 'NPU 환산: EmbeddingGemma 2가 같은 기기에서 GPU와 CPU보다 NPU에서 **%.1f~%.1f배** 빨랐던 비율을, GPU와 CPU에서 잰 sLLM의 값에 곱했습니다. '
                                   'Samsung Gauss는 공개된 속도가 없어 같은 크기의 공개 모델로 셈했습니다.' % (NUM.R_GPU, NUM.R_CPU), pt=11.5, color=SUB) + 18
    lw = 470
    label(s, 'qb/l1', X, y, '검색: Hop 1회 = 약 0.02초')
    label(s, 'qb/l3', X + lw + 30, y, '기록 수에 따른 Hop 시간과 색인 크기')
    bars, bh = hbars('qb/h', X + 16, y + 48, lw - 32, HOP, vmax=12, pt=11, bar_h=15, gap=11)
    ph = 16 + bh + 16
    s.add('qb/hop', [panel('qb/hp', X, y + 32, lw, ph)] + bars)
    h2 = tbl(s, 'qb/t', X + lw + 30, y + 32, W - lw - 30, [34, 22, 22, 22], ['', '1만 건', '10만 건', '100만 건'], B5_SCALE, pady=8, hi=(0,))
    y += 32 + max(ph, h2) + 12
    footnote(s, ['¹ litert-community/embeddinggemma-2-text-270m-litert-lm 모델 카드 (128토큰, 5회 평균). 8ms는 같은 모델을 양자화해 팀이 잰 값   '
                 '² LiteRT-LM 모델 카드의 공개 측정값',
                 '³ 256-dim 벡터 10만 건을 모두 비교하는 시간으로 잡은 값. 100만 건은 그 10배로 셈함. 색인 크기는 256-dim int8 벡터 기준'], y)
    return s


# ------------------------------------------------------------------ B-6 속도 ②: UX별 응답 시간
def _bars(ux, names, texts, total, pins=()):
    rw, se, an = NUM.SLOW[ux]
    return [(names[0], rw, texts[0], 'gen'), (None, se, '', 'emb'), (names[1], an, texts[1], 'gen')], total, pins


UXT = [('UX2 단서로 찾는 기억',) + _bars('ux2', ('재작성', '답변'), (NUM.T_RW2, NUM.T_AN2), NUM.T_UX2),
       ('UX1 기록 통합 검색',) + _bars('ux1', ('재작성', '요약'), (NUM.T_RW1, NUM.T_AN1), NUM.T_UX1, [(1, '찾은 기록을 먼저 표시: ' + NUM.T_REC1)]),
       ('UX3 먼저 건네는 기억',) + _bars('ux3', ('재작성', '제안'), (NUM.T_RW3, NUM.T_AN3), NUM.T_UX3 + ' (백그라운드)')]
B6_CONF = [[rw.name, an.name, rw.kind, NUM.sec(NUM.TOT['ux2'][i]), '%s (기록은 %s)' % (NUM.sec(NUM.TOT['ux1'][i]), NUM.sec(NUM.REC1[i])), NUM.sec(NUM.TOT['ux3'][i])]
           for i, (rw, an) in enumerate(NUM.CONFIGS)]


def s_uxtime():
    s = page_slide('qb_uxt', 'B-6', [('속도 2: UX별 응답 시간', INK)])
    y = 98
    y += label(s, 'qb/l2', X, y, '질의부터 답까지 (보라: sLLM 생성, 파랑: 검색 %d~%d회)' % (2, 3)) + 10
    span_ = max(NUM.TOT['ux1']) * 1.42
    for i, (name, segs, total, pins) in enumerate(UXT):
        y += timebar(s, 'qb/tb%d' % i, X, y, W, segs, total, title=name, title_w=176, span=span_, total_w=10, pt=10.5, pins=pins) + 14
    y += 6
    y += label(s, 'qb/l4', X, y, '기준 모델별 응답 시간') + 4
    y += tbl(s, 'qb/tc', X, y, W, [20, 16, 12, 14, 24, 14], ['Query Rewriter', '답변 생성', '기준', 'UX2', 'UX1', 'UX3'], B6_CONF, pady=8, hi=(2,), pt=11.5) + 16
    y += points(s, 'qb/p', X, y, W, ['**시간은 sLLM의 생성에서 듭니다.** 검색은 3-hop이어도 0.06초여서 Hop이 늘어도 차이가 거의 없습니다.',
                                    '**토큰 수의 가정.** 재작성 입력 130토큰, 검색 계획 72~82토큰, 답변은 이름 추출 10토큰, 보낼 메시지 25토큰, 3줄 요약 80토큰입니다.'], gap=8) + 12
    footnote(s, '기준 모델의 측정값과 NPU 환산은 B-5. 가장 느린 줄은 Gemma 3 1B를 Galaxy S25 Ultra의 NPU에서 잰 공개 측정값 그대로임.', y)
    return s


# ------------------------------------------------------------------ B-7 단계적 적용
B6 = [('n', '1단계', '기록 통합 검색 (UX1)', '임베딩 색인과 BM25로 검색하고, 탑재된 Gauss가 요약', '검색은 보급형까지, 요약은 Gauss 탑재 기기'),
      ('n', '2단계', '단서로 찾는 기억 (UX2)', 'Query Rewriter와 Reasoning Embedding으로 여러 앱의 단서를 연쇄 탐색', 'Gauss 3B 탑재 플래그십부터'),
      ('n', '3단계', '먼저 건네는 기억 (UX3)', '위치, 일정, 대화 상대 같은 계기 신호가 맞을 때 먼저 제안', '플래그십'),
      ('n', '4단계', '가전과 TV', '휴대폰이 찾은 답을 SmartThings로 냉장고, TV, 세탁기에 전달', 'Bixby 탑재 가전과 TV')]
B6_NEW = [('q', dict(head='추가 튜닝 없음', lines=['탑재된 Gauss와 공개된 임베딩 모델로 바로 시작'])),
          ('q', dict(head='모델 튜닝 2종', lines=['Query Rewriter Adapter와 Reasoning Embedding (D-4, D-6)'])),
          ('q', dict(head='계기 신호 연결', lines=['Now Nudge, Personal Data Engine의 신호와 Gate 기준 조정'])),
          ('q', dict(head='기기 사이 연동', lines=['전달 방식과 권한을 정함. 검색은 휴대폰에서 실행']))]


def s_road():
    s = page_slide('qb_road', 'B-7', [('단계적 적용 계획', INK)])
    y = 104
    y += pipeline(s, 'qb/f', y, None, B6, gap=18, name_pt=14.5, desc_pt=12)
    y += data_row(s, 'qb/d', y, B6_NEW, gap=18) + 34
    y += notes3(s, 'qb/n', y, [('가벼운 기능부터 넓게', '임베딩 검색은 **약 0.2GB와 0.02초**면 되어서 넓게 적용할 수 있습니다. sLLM이 필요한 기능은 플래그십부터 시작합니다.'),
                               ('앞 단계를 그대로 사용', '단계마다 앞 단계의 색인과 모델을 그대로 씁니다. 1단계에서 만든 색인이 2~4단계의 기반입니다.'),
                               ('Galaxy AI와 같은 순서', 'Galaxy AI도 Galaxy S24에서 시작해 One UI 6.1 업데이트로 S23, Z Fold5, Z Flip5, Tab S9에 적용했습니다.¹')], pt=12.5) + 22
    footnote(s, '¹ Samsung Newsroom, "New One UI 6.1 Update Brings Galaxy AI to More Galaxy Devices" (2024. 02. 22): 2024년 3월 말부터 적용.', y)
    return s


# ------------------------------------------------------------------ B-8 사업 효과 (본 발표만 본 사람이 물을 질문으로 Carbon이 꼽음. 숫자는 9차 후보 장(biz_new.py)의 것)
def s_biz():
    s = page_slide('qb_biz', 'B-8', [('사업 효과', INK)])
    y, h, gap = 100, 150, 14
    qrow(s, 'qb/q1', y, h, '사용자를 Galaxy에 머물게 하는 효과가 있나요?',
         '쓸수록 떠나기 어려워집니다. 기록은 한 달에 평균 41개의 앱에 흩어져 쌓이고¹, 사람들은 그 기록을 지우지 않습니다.² 사진과 메모는 다른 휴대폰으로 옮길 수 있지만, '
         'Weave가 그 사이를 **이어 둔 기억은 옮길 수 없습니다.**',
         n=1, vis=vis_nums([('41개', ['한 달에 쓰는', '앱의 수¹']), ('69%', ['기록을 지우지 않고', '쌓아 두는 사람²'])], pt=22))
    qrow(s, 'qb/q2', y + h + gap, h, '새로운 사용자를 끌어올 수 있나요?',
         '기록을 찾아 주는 기능은 다른 기기의 사용자도 원합니다. 저희 설문에서 iPhone 사용자 62명 가운데 **60명이 쓰겠다**고 답했습니다.³ Galaxy를 쓰는 10대는 61%인데, '
         '다음에 사고 싶은 휴대폰으로 Galaxy를 고른 10대는 47%입니다.⁴',
         n=2, vis=vis_nums([('62명 중 60명', ['iPhone 사용자의', '사용 의향³']), ('61% → 47%', ['10대의 Galaxy 사용과', '다음 구매 의향⁴'])], pt=19))
    qrow(s, 'qb/q3', y + 2 * (h + gap), h, '적용하는 데 비용이 많이 들지 않나요?',
         '새 부품이 필요 없는 소프트웨어입니다. Galaxy AI가 들어가는 기기는 2026년 말 **8억 대**이고⁵, 업데이트만으로 적용할 수 있습니다. 1단계인 기록 통합 검색은 새로 튜닝할 모델도 없습니다. (B-7)',
         n=3, vis=vis_nums([('8억 대', ['2026년 말', 'Galaxy AI 기기⁵']), ('0개', ['1단계에서 새로', '튜닝할 모델'])], pt=22))
    footnote(s, ['¹ Ofcom, "Online Nation 2025" (영국 스마트폰 이용자)   ² Compare and Recycle, "Digital Declutter Statistics 2025" (스스로를 디지털 호더라고 답한 비율)   '
                 "³ 자체 설문조사 (응답자 210명 가운데 iPhone 사용자 62명, '26.11)",
                 '⁴ 한국갤럽, 「스마트폰 관련 조사 2012-2026」 (2026. 07), 13~18세 200명   ⁵ 삼성전자 발표: Reuters 인터뷰 (2026. 01), Galaxy Unpacked (2026. 02, 2026. 07)'],
             y + 3 * h + 2 * gap + 12)
    return s


# ------------------------------------------------------------------ 물음과 답
PAGES = [
    Page('B-1', '왜 온디바이스인가', s_ondev,
         q='왜 꼭 온디바이스여야 하나요? 성능 좋은 서버 LLM을 API로 부르면 되지 않나요?',
         a='온디바이스여야 하는 이유는 두 가지입니다. 휴대폰 속 기록에는 나만 아는 정보와 대화 상대의 정보까지 섞여 있어서, '
           '외부 LLM 서버로 보내는 순간 어디에 남고 어떻게 쓰이는지 사용자가 통제할 수 없습니다. '
           '갤럭시는 개인 데이터를 기기 안에서 처리하는 PDE와, 이를 암호화해 지키는 KEEP과 Knox Vault를 갖추고 있고, '
           'Weave도 이 구조 위에서 기록을 밖으로 내보내지 않고 동작합니다. '
           '사용자도 같은 답을 했습니다. 저희 설문에서 80.5%가 내 기록이 휴대폰 안에서만 처리된다면 쓰겠다고 답했고, '
           '서버로 나가도 쓰겠다는 답은 12.4%에 그쳤습니다.',
         more=[('보안 말고, API로 부르면 무엇이 비효율인가요?',
                '질의할 때마다 관련 기록을 서버로 올리고 답을 기다려야 합니다. 통신이 끊기면 쓸 수 없고, 호출할 때마다 비용이 듭니다. '
                '무엇보다 어떤 기록이 관련 있는지 고르려면 결국 기기 안에서 먼저 찾아야 합니다.'),
               ('삼성의 정책과는 맞나요?', 'Galaxy AI 설정에는 기기에서만 데이터를 처리하게 하는 스위치가 있습니다. Weave는 그 스위치를 켠 상태에서도 그대로 동작합니다.'),
               ('서버 모델보다 답이 나쁘지 않나요?', 'Weave에서 sLLM이 하는 일은 짧은 검색 계획을 쓰고 찾은 기록 몇 건을 요약하는 일입니다. 이런 좁은 일은 작은 모델로도 충분하다는 근거를 D-3에 모았습니다.'),
               ('35쪽처럼 냉장고와 TV로 넘어가면 결국 클라우드로 가는 것 아닌가요?',
                '기억과 색인은 휴대폰 안에 두고, 가전에는 찾아낸 답 한 줄만 건네는 구성입니다. 누구에게 보여 줄지는 Voice ID로 본인이 확인됐을 때로 한정하고, 어떤 기록을 가전에 건넬지는 사용자가 정합니다.'),
               ('설문은 누구에게 어떻게 물었나요?',
                '2026년 10월 28일부터 11월 4일까지 온라인으로 210명에게 물었습니다. 갤럭시 사용자가 145명, 아이폰 사용자가 62명입니다.')],
         basis=['장과 대본은 팀원(ysy19)의 `apx_new.py` 그대로. 붉은 상자 한 곳만 바꿈(API 호출의 비효율을 보탬).',
                'Samsung Newsroom, "Samsung Introduces Future-Ready Mobile Security for Personalized AI Experiences"(2025. 07): "These insights stay entirely on-device, protected by KEEP and further secured by Knox Vault".',
                '설문 13번(210명): 휴대폰 안에서만 처리된다면 쓰겠다 169명(80.5%), 밖으로 보내져도 쓰겠다 26명(12.4%), 어느 쪽이든 쓰지 않겠다 15명(7.1%). CSV로 다시 셈.',
                'Samsung 지원(ANS10000753): Galaxy AI의 "Process data only on device" 스위치. Knox 문서: 클라우드에서 처리하는 기능의 데이터는 모델 학습에 쓰일 수 있음.']),
    Page('B-2', '카카오톡을 읽는 방법', s_kakao,
         q='카카오톡은 삼성 앱이 아닌데, 대화를 어떻게 읽나요?',
         a='받는 메시지는 알림으로 읽고, 지난 대화는 사용자가 내보낸 파일로 읽습니다. '
           '알림은 사용자가 허용한 앱의 것만 도착할 때마다 기기 안에서 색인하고, 내보낸 파일은 사용자가 직접 고른 대화방만 대상이 됩니다. '
           '새로운 방식은 아닙니다. 삼성의 PDI가 이미 카카오톡과 WhatsApp 같은 앱의 알림에서 예약 정보를 모아 Finder와 Now Brief에 쓰고 있고, '
           'Galaxy Watch가 휴대폰 알림을 보여 주는 것도 같은 권한입니다. '
           'Weave는 이미 쓰이는 경로 위에서, 읽는 범위를 예약 정보에서 대화 속 단서로 넓힙니다.',
         more=[('내가 보낸 메시지는 못 읽는 것 아닌가요?', '맞습니다. 알림은 받은 메시지에만 옵니다. 그래서 시나리오의 단서는 모두 상대가 보낸 메시지로 잡았습니다. 내가 보낸 말까지 필요하면 내보낸 파일로 읽습니다.'),
               ('알림을 꺼 둔 단체방은요?', '읽지 않습니다. 필요하면 사용자가 그 대화방을 내보내서 색인할 수 있습니다.'),
               ('PC 카카오톡을 쓰는 동안은요?', 'PC 카카오톡을 쓰는 동안에는 휴대폰 알림이 늦게 옵니다. 그 사이의 대화도 내보낸 파일로 채울 수 있습니다.'),
               ('카카오와 협의가 있어야 하나요?', '알림 접근과 내보낸 파일은 지금 안드로이드에서 사용자 동의만으로 되는 방식입니다. 협력이 있으면 더 넓힐 수 있습니다.'),
               ('키보드나 접근성 권한으로 화면을 읽는 건가요? 약관 문제는 없나요?',
                '화면을 읽지 않습니다. 사용자가 켜는 알림 접근 권한과, 사용자가 직접 내보낸 파일만 씁니다. 삼성 PDI와 Galaxy Watch가 이미 쓰는 권한입니다.')],
         basis=['Android Developers, "NotificationListenerService": 사용자가 알림 접근을 허용한 앱은 다른 앱의 알림 내용을 받을 수 있음.',
                'Samsung 지원 "Understanding Finder on Galaxy phones": "Personal data intelligence (PDI): This feature collects reservation details from notifications in apps like Messages, Gmail, Naver, Line, WhatsApp, KakaoTalk, and Wallet." 회상 카드: "relevant reservation information is displayed in a card format at the top".',
                'Galaxy S26 발표문의 Now Brief 각주: "Recalled data available from supported app notifications, Messages, Gmail and Samsung Wallet".',
                '카카오톡 대화 내용 내보내기: 채팅방 설정 > 대화 내용 내보내기 > 모든 메시지 내부저장소에 저장. 내 파일의 KakaoTalk 폴더 안 Chats에 저장됨(삼성전자서비스와 삼성 커뮤니티의 안내).',
                'Galaxy Watch: Galaxy Wearable 앱이 휴대폰의 알림 접근 권한을 받아 워치에 알림을 보여 줌(Samsung 지원과 개발자 문서의 안내).']),
    Page('B-3', '권한과 사생활 보호', s_data,
         q='내 기록을 AI가 다 본다는 게 불안한데, 사생활은 어떻게 지키나요?',
         a='읽는 범위는 사용자가 정하고, 읽은 것은 기기 밖으로 나가지 않습니다. 삼성 기본 앱은 사용자 동의 아래 기기 안에서 연동하고, '
           '카카오톡 같은 외부 메신저는 사용자가 허용한 알림만 색인합니다. 통화 내용은 듣지도 저장하지도 않습니다. '
           '원본 기록과 색인은 모두 기기 안에만 저장하고, 어느 앱을 색인할지와 색인을 지우는 일은 사용자가 언제든 직접 정할 수 있습니다.',
         more=[('배터리는 괜찮나요?', '처음의 대량 색인은 충전 중이거나 기기가 쉴 때만 합니다. 쓰는 동안에는 가벼운 벡터 검색과, 추려진 기록 한두 건에 대한 sLLM만 실행합니다.'),
               ('기록을 지우면 색인은요?', '원본을 지우면 그 기록의 벡터와 메타데이터도 함께 지웁니다.'),
               ('하루에 카카오톡이 수백 건 오는데 배터리는 괜찮나요?',
                '메시지 한 건을 색인하는 데는 임베딩 한 번, 8밀리초가 듭니다. 300건이면 2.4초입니다. 사진처럼 무거운 것은 충전 중에 모아서 합니다.'),
               ('휴대폰을 바꾸면 색인은 어떻게 옮기나요?',
                '색인은 옮기지 않아도 됩니다. Smart Switch로 원본 기록을 옮긴 뒤 새 기기에서 다시 만듭니다. 텍스트 기록 10만 건을 다시 색인하는 데 13분 정도입니다.'),
               ('가족이 함께 보는 TV나 냉장고에 개인 기록이 뜨면요?',
                '가전에는 찾아낸 답만 건네고 대화 원문은 건네지 않습니다. 누구에게 보여 줄지는 Voice ID로 본인이 확인됐을 때로 한정하고, 어떤 앱의 기록을 가전에 건넬지는 사용자가 정합니다.')],
         basis=['How it Works Appendix에 있던 장(q_data)의 내용을 질문과 답 세 줄로 다시 짬. Android Developers: NotificationListenerService, WorkManager(RequiresCharging, RequiresDeviceIdle), Android Keystore.',
                '8ms × 300건 = 2.4초(텍스트 메시지 기준).']),
    Page('B-4', '메모리 사용량', s_mem,
         q='AI 모델이 늘면 메모리가 부족해질 텐데, Weave는 얼마나 쓰나요?',
         a='Weave가 새로 더하는 메모리는 약 0.25기가바이트로, Galaxy S26 Ultra의 메모리 12기가바이트의 2% 정도입니다. '
           '내역은 임베딩 모델이 약 0.19기가바이트, 기록 10만 건의 색인이 26메가바이트, Query Rewriter 어댑터가 수십 메가바이트입니다. '
           '가장 무거운 sLLM은 새로 싣지 않고, 기기에 이미 탑재된 Gauss를 함께 쓰면서 그 위에 작은 어댑터만 얹습니다. '
           'Apple도 온디바이스 모델 하나에 기능별 어댑터를 갈아 끼우는 같은 방식을 씁니다.',
         more=[('글자가 없는 사진까지 찾으려면 메모리가 더 들지 않나요?',
                '사진의 내용으로 찾으려면 EmbeddingGemma 2의 전체 구성이 필요하고, 약 0.57기가바이트입니다. 다만 사진의 벡터는 충전 중에 미리 만들어 두기 때문에, 글로 질의할 때는 텍스트 구성 0.19기가바이트만 올리면 됩니다.'),
               ('기록이 100만 건이면요?', '색인이 256메가바이트가 됩니다. 저장 공간에 두고 필요한 부분만 메모리에 올리기 때문에 메모리 부담은 그보다 작습니다.'),
               ('Gauss가 메모리에서 내려가 있으면요?', '그때는 다른 Galaxy AI 기능과 마찬가지로 모델을 올리는 시간이 한 번 듭니다. 검색 결과는 그 전에 먼저 보여 줄 수 있습니다.'),
               ('색인이 저장 공간을 많이 차지하지 않나요?',
                '기록 하나에 256바이트입니다. 100만 건이어도 256메가바이트로, 사진 수십 장 분량입니다.'),
               ('Query Rewriter를 전용 모델로 따로 올리면요?',
                '2.7억 파라미터급 전용 모델을 따로 올려도 0.5기가바이트 안팎이라, 합쳐서 1기가바이트를 넘지 않습니다.')],
         basis=['Google, "EmbeddingGemma 2"(2026. 10. 06): "~191MB active RAM for text-only weights and ~567MB for the full multimodal model on a Google Pixel 11 Pro".',
                '색인 크기는 256차원 8비트 벡터(기록 하나에 256바이트)로 셈: 1만 건 2.6MB, 10만 건 25.6MB, 100만 건 256MB. Android ML Kit의 Embeddings API도 8비트로 양자화한 벡터를 AppSearch에 저장함.',
                'Apple, "Introducing Apple\'s On-Device and Server Foundation Models"(2024. 06. 10): "the parameters for a rank 16 adapter typically require 10s of megabytes", "can be dynamically loaded, temporarily cached in memory, and swapped".',
                'ExecuTorch 공개 측정(OnePlus 12, CPU, Llama 3.2 4비트): 1B RSS 1,921MiB, 3B RSS 3,726MiB. Gauss의 값이 아니라 같은 크기 모델의 값.',
                'Galaxy S26 Ultra 메모리: 256GB와 512GB 모델 12GB, 1TB 모델 16GB(사양표).',
                '합계: 0.19GB + 0.026GB + 어댑터 수십 MB ≈ 0.25GB. 0.25 ÷ 12 = 2.1%.',
                '글로 질의할 때 텍스트 구성만 올린다는 것은 설계: 사진의 벡터를 색인 때 미리 만들어 두면 질의 쪽에는 텍스트 인코더만 필요함(Carbon이 짚은 빈 곳, 11-16).']),
    Page('B-5', '속도 1: 기준 모델, 검색 시간', s_speed,
         q='기록이 수십만 건으로 늘거나, 여러 번 이어 찾으면 느려지지 않나요? 숫자는 어떻게 나온 건가요?',
         a='검색 자체는 가볍습니다. 질의를 벡터로 바꾸는 데 8밀리초, 기록 10만 건과 비교하는 데 10밀리초, 합쳐서 한 번에 0.02초입니다. '
           '세 번 이어 찾아도 0.06초라서 차이를 느끼기 어렵습니다. 8밀리초는 EmbeddingGemma 2를 Galaxy S26 Ultra의 NPU에 올려 직접 잰 값입니다. '
           '공개된 모델 카드에는 같은 기기의 GPU에서 26밀리초, CPU에서 27밀리초로 나와 있어서, NPU가 세 배 넘게 빠릅니다. '
           'sLLM의 시간은 같은 크기의 공개 모델로 계산했는데, NPU에서 잰 값은 그대로 쓰고 GPU와 CPU에서 잰 값은 이 비율로 NPU 값을 환산했습니다.',
         more=[('기록이 100만 건이면요?', '모두 비교하는 방식으로도 한 번 찾는 데 0.11초입니다. 색인은 256메가바이트입니다.'),
               ('NPU 환산을 믿을 수 있나요?', '임베딩 모델에서 확인한 비율을 적용한 추정입니다. 그래서 가장 느린 값은 Gemma 3 1B를 Galaxy S25 Ultra의 NPU에서 잰 공개 측정값 그대로 두었습니다. 이 값으로도 단서로 찾는 기억은 1초 남짓입니다.'),
               ('Gauss로 직접 재지 않은 이유는요?', 'Gauss의 온디바이스 속도는 공개되어 있지 않아서, 같은 크기의 공개 모델을 기준으로 삼았습니다.'),
               ('키워드 검색과 비교하면요?', '둘 다 밀리초 단위라서 함께 써도 차이를 느끼기 어렵습니다. 그래서 Weave는 두 검색을 함께 씁니다.')],
         basis=['임베딩 8ms: EmbeddingGemma 2(텍스트 구성), Galaxy S26 Ultra NPU 실측(팀 측정). 모델 카드(litert-community/embeddinggemma-2-text-270m-litert-lm, 128토큰, 5회 평균)의 값은 S26 Ultra GPU 25.9ms, CPU 27.1ms, Pixel 11 Pro TPU 8.3ms.',
                'NPU 환산 비율: 25.9 ÷ 8 = %.2f(GPU), 27.1 ÷ 8 = %.2f(CPU). 11-16에 사용자가 이 비율로 셈하라고 함.' % (NUM.R_GPU, NUM.R_CPU),
                '생성 속도(LiteRT-LM 공개값, 입력과 출력의 초당 토큰): FunctionGemma 270M은 S25 Ultra CPU에서 2,238과 154 → NPU 환산 %d과 %d. Gemma 4 E2B는 S26 Ultra GPU에서 3,808과 52.1 → NPU 환산 %d과 %d. Gemma 3 1B는 S25 Ultra NPU에서 5,836과 85(실측 그대로).'
                % (round(NUM.FG.pre_npu), round(NUM.FG.dec_npu), round(NUM.E2B.pre_npu), round(NUM.E2B.dec_npu)),
                '벡터 검색 10ms: 256차원 벡터 10만 건을 모두 비교하는 시간으로 잡은 값. 사용자의 검토 자료(11-14)는 x86 코어 하나에서 5.1ms를 재고 휴대폰은 10ms로 잡음. sqlite-vec v0.1은 Mac M1 mini에서 128차원 100만 건을 17ms에 비교함.',
                '기록 수별 Hop 시간: 1만 건 8 + 1 + 2 = 11ms, 10만 건 8 + 10 + 2 = 20ms, 100만 건 8 + 100 + 2 = 110ms(모두 비교하는 방식 기준).',
                '공개된 NPU 측정 가운데 Qualcomm AI Hub의 Galaxy S26 값은 Qwen3-0.6B 출력 초당 88.8토큰, Qwen3-1.7B 42.4토큰, Qwen3-4B 21.8토큰. NPU 환산값(Gemma 4 E2B %d토큰)은 이보다 빠른 쪽의 추정임.' % round(NUM.E2B.dec_npu)]),
    Page('B-6', '속도 2: UX별 응답 시간', s_uxtime,
         q='실제로 답이 나오기까지 몇 초가 걸리나요?',
         a='단서로 찾는 기억은 1초 안팎입니다. 시간은 대부분 sLLM이 생성하는 두 곳에서 듭니다. 질의 재작성이 0.2초에서 1초, 답변 생성이 길어도 1초입니다. '
           '기록 통합 검색은 세 줄 요약까지 1초에서 2초가 걸리는데, 찾은 기록은 1초 안에 먼저 보여 줍니다. '
           '먼저 건네는 기억은 백그라운드에서 1초 안팎에 준비합니다. '
           '가장 느린 값은 Gemma 3 1B를 NPU에서 잰 공개 측정값을 그대로 쓴 것이고, 빠른 값은 더 가벼운 구성을 NPU 기준으로 환산한 것입니다.',
         more=[('Hop이 늘면 더 느려지지 않나요?', '질의 재작성은 질의마다 한 번뿐입니다. Hop이 하나 늘면 검색 0.02초와 계획 한 줄을 더 생성하는 시간만 늘어납니다.'),
               ('통화 중에 쓰기에는 느리지 않나요?', '찾은 기록 목록은 1초 안에 먼저 뜹니다. 요약은 그 뒤에 글자가 나타나는 대로 읽으면 됩니다.'),
               ('배터리가 적거나 기기가 뜨거울 때는요?', 'sLLM을 쓰기 어려운 상황에서는 원래 질의로 한 번 검색한 결과를 먼저 보여 줍니다. 검색은 0.02초라 이때도 부담이 없습니다.'),
               ('토큰 수는 어떻게 가정했나요?', '재작성은 입력 130토큰에 검색 계획 72에서 82토큰, 답변은 이름 추출 10토큰, 보낼 메시지 25토큰, 세 줄 요약 80토큰으로 잡았습니다.')],
         basis=['구성 셋(Query Rewriter + 답변 생성): FunctionGemma 270M + Gemma 4 E2B(NPU 환산), Gemma 4 E2B 둘 다(NPU 환산), Gemma 3 1B 둘 다(NPU 실측).',
                'UX2(재작성 130 → 72토큰, 검색 2회, 답변 170 → 10토큰): ' + ', '.join(NUM.sec(v) for v in NUM.TOT['ux2']) + '.',
                'UX1(재작성 130 → 82토큰, 검색 3회, 요약 540 → 80토큰): ' + ', '.join(NUM.sec(v) for v in NUM.TOT['ux1']) + '. 찾은 기록이 먼저 뜨는 때는 ' + ', '.join(NUM.sec(v) for v in NUM.REC1) + '.',
                'UX3(재작성 130 → 72토큰, 검색 2회, 제안 500 → 25토큰): ' + ', '.join(NUM.sec(v) for v in NUM.TOT['ux3']) + '.',
                '재작성 1회 %s, 답변 생성 %s. 토큰 수의 가정은 사용자의 검토 자료(11-14) 6장.' % (NUM.T_RW, NUM.T_AN),
                'NPU 환산을 하기 전(공개 측정값 그대로)의 값은 UX2 0.80/1.69/1.06초, UX1 2.33/3.35/2.08초, UX3 1.19/2.07/1.29초였음(검토 자료).']),
    Page('B-7', '단계적 적용 계획', s_road,
         q='실제 상품화는 어떤 순서로 하나요?',
         a='가벼운 기능부터 넓게 적용하고, sLLM이 필요한 기능은 플래그십부터 적용합니다. 1단계는 기록 통합 검색입니다. '
           '임베딩 색인과 이미 탑재된 Gauss의 요약만으로 동작해서, 새로 튜닝할 모델이 없습니다. '
           '2단계는 단서로 찾는 기억입니다. Query Rewriter 어댑터와 Reasoning Embedding 튜닝이 필요해서, Gauss 3B가 올라간 플래그십부터 시작하고 1B 모델로 넓힙니다. '
           '3단계는 먼저 건네는 기억으로, Now Nudge와 PDE의 계기 신호와 연결합니다. 마지막으로 SmartThings를 통해 가전과 TV로 넓힙니다. '
           'Galaxy AI가 S24에서 시작해 One UI 업데이트로 이전 기기에 넓혀 간 것과 같은 순서입니다.',
         more=[('보급형에서는 어디까지 되나요?', '임베딩 검색은 0.2기가바이트와 0.02초면 되기 때문에 보급형에서도 됩니다. sLLM이 필요한 요약과 이어 찾기는 Gauss가 올라간 기기부터입니다.'),
               ('2단계의 튜닝에는 무엇이 필요한가요?', '한국어 일상 기록으로 만든 단서 데이터입니다. 만드는 방법과 평가 지표는 D-4, D-6, D-8에 있습니다.'),
               ('가전의 칩으로 이게 돌아갑니까?',
                '가전에서는 돌리지 않습니다. 검색은 휴대폰이 하고, 가전은 답을 받아 보여 주거나 말합니다.'),
               ('가장 먼저 만들 최소 기능은 무엇인가요?',
                '1단계인 기록 통합 검색입니다. 삼성 기본 앱의 기록부터 색인하고, 카카오톡 알림은 사용자가 허용했을 때 더합니다.')],
         basis=['Samsung Newsroom, "New One UI 6.1 Update Brings Galaxy AI to More Galaxy Devices"(2024. 02. 22): Galaxy S23 시리즈, S23 FE, Z Fold5, Z Flip5, Tab S9에 3월 말부터.',
                'Gauss 3B와 1B의 온디바이스 탑재는 팀 조사 기준.']),
    Page('B-8', '사업 효과', s_biz,
         q='편해 보이기는 하는데, 사업적으로는 무엇이 남나요?',
         a='세 가지입니다. 첫째, 쓸수록 Galaxy를 떠나기 어려워집니다. 사람들은 한 달에 평균 41개의 앱을 쓰고, 69%는 기록을 지우지 않고 쌓아 둡니다. '
           '사진과 메모는 다른 휴대폰으로 옮길 수 있지만, Weave가 그 사이를 이어 둔 기억은 옮길 수 없습니다. '
           '둘째, 새로운 사용자가 Galaxy를 고를 이유가 됩니다. 저희 설문에서 아이폰을 쓰는 응답자 62명 중 60명이 기록을 찾아 주는 AI가 있다면 쓰겠다고 답했습니다. '
           '셋째, 새 부품이 필요 없는 소프트웨어입니다. Galaxy AI가 들어가는 기기는 올해 말 8억 대이고, 업데이트만으로 적용할 수 있습니다.',
         more=[('돈을 받을 수 있는 기능인가요?', '기능 하나로 과금하기보다, Galaxy AI의 한 축으로 기기를 고르고 계속 쓰게 하는 이유로 봅니다.'),
               ('아이폰 사용자 60명이 갤럭시로 바꾸겠다고 한 건가요?', '아닙니다. 기록을 찾아 주는 AI를 쓰겠다는 답입니다. 이 필요가 기기를 가리지 않는다는 근거로만 씁니다.'),
               ('69%는 무슨 숫자인가요?', '영국 조사에서 스스로를 디지털 호더라고 답한 비율입니다. 늘 그렇다는 답과 가끔 그렇다는 답을 더한 값입니다.')],
         basis=['Ofcom, "Online Nation 2025"(2025. 12): 영국 18세 이상 스마트폰 이용자가 한 달에 쓰는 앱은 평균 41개.',
                'Compare and Recycle, "Digital Declutter Statistics 2025": 스스로를 디지털 호더로 여기는 비율 69%(늘 26%, 가끔 42%).',
                '자체 설문(210명) 가운데 아이폰 사용자 62명: 13번에서 휴대폰 안에서만 처리된다면 쓰겠다 52명, 밖으로 보내져도 쓰겠다 8명, 쓰지 않겠다 2명.',
                '한국갤럽 「스마트폰 관련 조사 2012-2026」(2026. 07): 13~18세 200명, 지금 삼성 61%, 다음에 사고 싶은 휴대폰 삼성 47%.',
                'Galaxy AI 기기: 2025년 말 4억 대 → 2026년 말 8억 대(Reuters 2026. 01. 05 인터뷰, Galaxy Unpacked 2026. 02와 07).',
                '숫자와 문장은 9차에 본 발표에서 뺀 비즈니스 임팩트 장과 그 후보(biz_new.py)의 것.']),
]
