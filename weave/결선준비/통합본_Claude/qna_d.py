"""Appendix D 묶음: 모델과 학습 (11-16 3판).

D-1 모델 구성과 스펙, D-2 Query Rewriting의 종류와 Weave의 선택, D-3 작은 모델의 Query Rewriting(Rewrite-Retrieve-Read, ReALM),
D-4 Query Rewriter 튜닝 방법, D-5 Reasoning-intensive Retrieval의 정의와 유형(BRIGHT, ImpliRet), D-6 Reasoning Embedding의 선행 연구와 튜닝 방법,
D-7 Multi-hop Retrieval 연구와 Weave의 위치, D-8 한국어 일상 기록 데이터와 평가.
3판: 2판의 표 두세 개를 표 하나(꼭 필요한 장만)와 막대, 흐름 그림, 요점으로 줄였다. 표에서 뺀 세부 숫자는 대본 md의 '더 물으면'과 근거에 있다.
기술 용어는 통용되는 영어 이름을 그대로 쓴다(Query Decomposition, Hard Negative, Contrastive Learning 등). 억지 예시는 넣지 않는다(예시가 필요한 D-5만 본 발표의 기록으로).
논문의 숫자는 원문(초록, 본문의 표, 모델 카드)에서 확인한 것만 넣었다(대본 md의 근거).
"""
from ui import BODY, INK, MUTE, PURPLE, R, T

from qna_lib import (Page, box, data_row, footnote, hbars, label, lh_of, notes3, page_slide, panel, pipeline, points, rich, rwrap, tbl, vis_nums)

X, W = 70, 1140
HI = dict(color=PURPLE, weight='b')


# ------------------------------------------------------------------ D-1 모델 구성과 스펙
D1 = [[['검색', 'Reasoning Embedding'], ['EmbeddingGemma 2¹ (Google, 2026. 10)', '텍스트 2.7억 파라미터, 256-dim'], '필요. 한국어 일상 단서로 튜닝 (D-6)', ['질의 1건에 **8ms**', '(S26 Ultra NPU 실측)'], '약 0.19GB'],
      [['질의 재작성', 'Query Rewriter'], ['Samsung Gauss + LoRA Adapter', '(대안: 2.7억 파라미터 전용 모델)'], '필요. 검색 계획 생성을 튜닝 (D-4)', ['0.5~1.6초²', '(출력 40~80토큰)'], 'Adapter 수십 MB³'],
      ['답변 생성', ['Samsung Gauss 3B', '(탑재된 모델 그대로)'], '없음 (프롬프트로 시작)', ['0.2~1.7초²', '(출력 10~80토큰)'], '없음']]


def s_d1():
    s = page_slide('qd_model', 'D-1', [('모델 구성과 스펙', INK)])
    y = 100
    y += tbl(s, 'qd/t', X, y, W, [17, 29, 22, 19, 13], ['역할', '모델', '추가 튜닝', '속도', '추가 메모리'], D1, hi=(0, 1), pady=11) + 22
    y += label(s, 'qd/l', X, y, '입출력 길이 제한: 온디바이스에서는 생성 길이가 곧 지연 시간')
    s.add('qd/len', [panel('qd/len/bg', X, y + 4, W, 96)] +
          vis_nums([('128토큰 이하', ['질의']), ('256토큰 이하', ['기록 Chunk⁴']), ('40~80토큰', ['검색 계획 (Query Rewriter의 출력)']),
                    ('10~80토큰', ['답변 (이름 추출 10, 메시지 25, 3줄 요약 80)'])], pt=17)(X, y + 4, W, 96))
    y += 4 + 96 + 20
    y += points(s, 'qd/p', X, y, W, ['**새로 싣는 모델은 임베딩 하나입니다.** sLLM은 기기에 탑재된 Gauss를 그대로 쓰고, Query Rewriter는 그 위에 얹는 Adapter입니다. 상황 인식과 Slot 채우기는 모델 없이 Rule과 메타데이터로 처리합니다.',
                                    '**sLLM의 속도는 같은 크기의 공개 모델로 계산했습니다.** Gemma 3 1B와 Gemma 4 E2B를 Galaxy S25 Ultra와 S26 Ultra에서 잰 공개 측정값을 썼습니다.']) + 14
    footnote(s, ['¹ Google, "EmbeddingGemma 2" (2026. 10. 06)와 모델 카드: Apache 2.0, 전체 7.4억 파라미터(텍스트 2.7억), 768-dim을 256-dim으로 줄여도 MTEB multilingual 61.4 → 60.4',
                 '² LiteRT-LM 모델 카드의 공개 측정값으로 계산   ³ Apple, "Introducing Apple\'s On-Device and Server Foundation Models" (2024. 06)   ⁴ Android ML Kit GenAI Embeddings API의 입력 한도'], y)
    return s


# ------------------------------------------------------------------ D-2 Query Rewriting의 종류
D2 = [['Coreference Resolution', '대화나 화면을 가리키는 지시어를 풀어 독립된 질의로 만듦', ['ReALM (Apple, 2024)', 'ConvSearch-R1 (2025)'], '적합. 출력 10~30토큰'],
      ['Query Reformulation', '검색기에 맞는 표현으로 고쳐 씀', 'Rewrite-Retrieve-Read (2023)', '적합. 출력 10~30토큰'],
      [('Query Decomposition', HI), ('Multi-hop 질의를 순서가 있는 Sub-query로 분해', HI), ['RQ-RAG (2024)', 'Hi-Q (2026)'], ('Weave의 선택. 튜닝하면 가능, 출력 40~80토큰', HI)],
      ['Reasoning Expansion', '추론 과정을 길게 생성해 질의에 덧붙임', ['BRIGHT의 GPT-4 Reasoning (2025)', 'TongSearch-QR (2025)'], '지연 초과. 3B급 모델로 500토큰 생성에 약 10초'],
      ['HyDE', '가상의 답변 문서를 생성해 그 문서로 검색', ['HyDE (2023)', 'Query2doc (2023)'], '부적합. 출력이 길고, 생성한 내용이 틀리면 검색도 틀어짐']]


def s_d2():
    s = page_slide('qd_qr', 'D-2', [('Query Rewriting의 종류와 Weave의 선택', INK)])
    y = 100
    y += tbl(s, 'qd/t', X, y, W, [20, 33, 23, 24], ['종류', '하는 일', '대표 연구', '온디바이스 적합성'], D2, hi=(2,), pady=8) + 20
    y += points(s, 'qd/p', X, y, W, ['**선택 기준은 출력 길이입니다.** 온디바이스에서는 토큰 하나를 생성하는 데 6.5~19ms가 듭니다. 40~80토큰인 Decomposition은 0.5~1.6초에 끝나지만, 500토큰을 쓰는 Expansion은 3B급 모델로 약 10초가 걸립니다.',
                                    '**Decomposition에 Slot을 더했습니다.** 앞 Hop의 결과가 필요한 자리는 Slot으로 비워 두고, 검색된 기록의 메타데이터로 채웁니다. Hop 사이에 LLM을 부르지 않습니다.',
                                    '**추론은 임베딩이 맡습니다.** 추론을 글로 길게 쓰지 않고, Reasoning Embedding이 추론 단서를 직접 검색합니다. (D-5, D-6)'], gap=9) + 14
    footnote(s, '출력 길이와 지연은 팀의 온디바이스 검토(11-14) 기준. 연구의 출처는 R-1.', y)
    return s


# ------------------------------------------------------------------ D-3 두 연구
def study(s, key, x, y, w, h, title, cite, pts, bars_title, bars, vmax, take):
    """연구 하나: 이름과 출처, 요점, 결과 막대, 막대 아래 한 줄. 막대 칸은 카드의 아래쪽에 맞춘다."""
    s.add(key, [box(key + '/bg', x, y, w, h, radius=18),
                T(key + '/t', x + 24, y + 18, w - 48, 26, title, size=15, color=INK, weight='b', anchor='ctr'),
                T(key + '/c', x + 24, y + 44, w - 48, 18, cite, size=10, color=MUTE, anchor='ctr')])
    points(s, key + '/p', x + 24, y + 76, w - 48, pts, pt=12, gap=6)
    _, bh_ = hbars(key + '/b', 0, 0, w - 84, bars, vmax=vmax, pt=11, bar_h=14, gap=8)
    ph = 38 + bh_ + 34
    by = y + h - 16 - ph
    bars_, _ = hbars(key + '/b', x + 42, by + 38, w - 84, bars, vmax=vmax, pt=11, bar_h=14, gap=8)
    s.add(key + '/bars', [panel(key + '/bp', x + 16, by, w - 32, ph),
                          T(key + '/bt', x + 34, by + 10, w - 68, 20, bars_title, size=10.5, color=INK, weight='b', anchor='ctr')] + bars_ +
          [T(key + '/tk', x + 34, by + 38 + bh_ + 8, w - 68, 18, take, size=10.5, color=PURPLE, weight='b', anchor='ctr')])


def s_d3():
    s = page_slide('qd_two', 'D-3', [('작은 모델의 Query Rewriting: 근거 연구', INK)])
    y, h, cw = 100, 316, 562
    study(s, 'qd/l', X, y, cw, h, 'Rewrite-Retrieve-Read', 'Ma et al., EMNLP 2023¹',
          ['**모델**: T5-large (7.7억 파라미터)를 Rewriter로 튜닝', '**방법**: ChatGPT의 Rewriting 가운데 정답으로 이어진 것으로 Warm-up한 뒤, 검색과 정답 결과를 Reward로 강화학습(PPO)'],
          'HotpotQA 정답률 (EM)', [('Rewriting 없음', 30.5, '30.5', False), ('ChatGPT가 Rewriting', 32.8, '32.8', False), ('튜닝한 T5 (7.7억)', 34.4, '34.4', True)], 42,
          '7.7억 파라미터 모델의 Rewriting이 ChatGPT의 Rewriting보다 높음')
    study(s, 'qd/r', X + cw + 16, y, cw, h, 'ReALM', 'Moniz et al. (Apple), SIGDIAL 2024²',
          ['**과제**: 화면과 대화 속 지시어가 가리키는 대상을 찾는 Reference Resolution', '**모델**: FLAN-T5를 튜닝 (8천만~30억 파라미터). 온디바이스 탑재를 목표로 밝힘'],
          '화면 속 대상을 맞힌 정확도 (%)', [('GPT-4', 90.1, '90.1', False), ('ReALM (8천만)', 88.9, '88.9', True), ('ReALM (30억)', 93.0, '93.0', True)], 110,
          '8천만 파라미터 모델이 GPT-4와 비슷한 수준')
    y += h + 22
    y += label(s, 'qd/l3', X, y, '같은 방향의 최근 연구: 정답 문장 대신 검색 결과를 Reward로 쓰는 강화학습') + 6
    y += notes3(s, 'qd/n', y, [('DeepRetrieval (2025, 3B)', '검색 지표를 Reward로 학습. 문헌 검색 Recall **65.1%** (이전 최고 24.7%)'),
                               ('ConvSearch-R1 (EMNLP 2025, 3B)', '검색 순위를 Reward로 학습. 대화형 검색 **56.5** (ChatGPT 기반 방법 48.9)'),
                               ('TongSearch-QR (2025, 1.5B)', 'BRIGHT에서 BM25 14.5 → **24.6** (GPT-4o로 Rewriting하면 26.5)')], pt=11.5, title_pt=12.5) + 14
    footnote(s, ['¹ "Query Rewriting for Retrieval-Augmented Large Language Models" (표 2)   ² "ReALM: Reference Resolution As Language Modeling" (표 3)',
                 'DeepRetrieval arXiv:2503.00223, ConvSearch-R1 arXiv:2505.15776 (QReCC의 MRR@3), TongSearch-QR arXiv:2506.11603 (BRIGHT의 nDCG@10).'], y)
    return s


# ------------------------------------------------------------------ D-4 Query Rewriter 튜닝
D4 = [('n', 'STEP 1', 'Teacher Labeling', '서버의 대형 LLM이 합성 질의마다 검색 계획을 작성', None),
      ('n', 'STEP 2', 'Supervised Fine-tuning', 'Teacher의 계획을 정답으로 학습 (Warm-up)', 'Rewrite-Retrieve-Read¹'),
      ('n', 'STEP 3', 'Execution Filtering', '계획을 합성 기록에 실행해, 모든 Hop에서 정답 기록에 도달한 계획만 남김', None),
      ('n', 'STEP 4', 'Reinforcement Learning', '검색된 기록의 순위를 Reward로 추가 학습. 정답 계획이 없어도 됨', 'ConvSearch-R1, DeepRetrieval²'),
      ('n', 'STEP 5', '온디바이스 배포', 'LoRA Adapter로 Gauss에 얹고, Constrained Decoding으로 출력 형식을 강제', 'Apple³, FunctionGemma⁴')]
D4_M = [('형식 오류율', '실행할 수 없는 계획의 비율'), ('과분해율', '한 번에 검색되는 질의를 나눈 비율'), ('Slot 정확도', '날짜와 사람을 맞게 채운 비율')]


def deflist(s, key, x, y, w, rows, kw=150, pt=12):
    """이름과 설명을 한 줄씩(사이에 가는 줄). 돌려줌: 높이."""
    out, yy = [], y
    for i, (a, b) in enumerate(rows):
        if i:
            out.append(R('%s/ln%d' % (key, i), x, yy - 5, w, 1, fill='E3DDF2', line=None))
        out += [T('%s/a%d' % (key, i), x, yy, kw, 24, a, size=pt, color=INK, weight='b', anchor='ctr'),
                T('%s/b%d' % (key, i), x + kw, yy, w - kw, 24, b, size=pt - 0.5, color=BODY, anchor='ctr')]
        yy += 34
    s.add(key, out)
    return yy - 10 - y


def s_d4():
    s = page_slide('qd_train', 'D-4', [('Query Rewriter 튜닝 방법', INK)])
    y = 100
    y += pipeline(s, 'qd/f', y, None, D4, gap=14, name_pt=12.5, desc_pt=11) + 26
    lw = 640
    label(s, 'qd/l1', X, y, '학습 데이터')
    label(s, 'qd/l2', X + lw + 40, y, 'Query Rewriter의 지표 (검색 지표는 D-8)')
    h1 = points(s, 'qd/p', X, y + 32, lw, ['**합성 기록만 씁니다.** 실제 사용자의 기록은 학습에 쓰지 않습니다. 합성 기록은 정답 기록을 알고 있어서 맞는 계획만 골라 낼 수 있습니다. (D-8)',
                                         '**분해하지 않는 질의도 넣습니다.** 한 번에 검색되는 질의와 답이 없는 질의를 넣어 과분해를 막습니다. 항상 분해하면 정답률이 60.7에서 57.3으로 떨어집니다.⁵',
                                         '**작은 모델로도 됩니다.** 2.7억 파라미터 모델도 튜닝하면 정해진 형식으로 출력하는 정확도가 58%에서 85%로 오릅니다.⁴'], gap=9)
    h2 = deflist(s, 'qd/m', X + lw + 40, y + 32, W - lw - 40, D4_M)
    y += 32 + max(h1, h2) + 18
    footnote(s, ['¹ Ma et al., EMNLP 2023   ² Zhu et al., EMNLP 2025. Jiang et al., arXiv:2503.00223   ³ Apple (2024. 06): 기기 안의 모델 하나에 기능마다 Adapter를 얹음. Adapter 하나는 수십 MB',
                 '⁴ Google, FunctionGemma 모델 카드 (Gemma 3 270M 기반, Mobile Actions 평가)   ⁵ Kim et al., "Hi-Q", NeurIPS 2026 (EM)'], y)
    return s


# ------------------------------------------------------------------ D-5 Reasoning-intensive Retrieval
D5_LV = [('kw', 'LEVEL 1  Keyword', '같은 단어', '질의와 기록에 같은 단어가 있음', 'BM25'),
         ('sem', 'LEVEL 2  Semantic', '비슷한 의미', '단어는 달라도 의미가 비슷함', '일반 임베딩'),
         ('rsn', 'LEVEL 3  Reasoning', '추론이 필요한 연결', '단어도 의미도 다르고, 추론을 한 번 거쳐야 이어짐', 'Reasoning Embedding')]
D5_EX = [[('q', dict(head='질의', lines=['집들이'])), ('rec', dict(icon='cal', title='성빈이 신혼집들이', meta='캘린더 · 10월 18일 (토)'))],
         [('q', dict(head='질의', lines=['마셨던 와인'])), ('rec', dict(icon='note', title='소믈리에 추천', meta='삼성노트', body=['샤토 마고']))],
         [('q', dict(head='질의', lines=['지은이네 집들이는 언제였지?'])),
          ('rec', dict(icon='talk', title='지은', meta='카카오톡 · 3월 15일 (일)', body=['박스 정리 다 했어! 휴지 안 사 와도 돼'], bubble=True, on=True))]]
D5_TY = [['World Knowledge', ['“Who was in the UK?”', '↔ “Lenna was at Big Ben”'], ['‘휴지 안 사 와도 돼’ → 집들이 초대', '‘갈색병’ → 제품의 정식 이름'], ('Reasoning Embedding을 튜닝', HI)],
         ['Temporal', '“seven days ago”를 실제 날짜로 풀어야 함', '‘이따 올 때’ + 수신 시각 → 3월 15일 저녁', '색인할 때 날짜로 정규화'],
         ['Arithmetic', '“$2,000짜리보다 20% 싸다” → $1,600', '레시피의 ‘배 2개’ + 냉장고의 ‘배 없음’ → 2개 부족', '답변을 생성하는 sLLM']]


def s_d5():
    s = page_slide('qd_types', 'D-5', [('Reasoning-intensive Retrieval: 정의와 유형', INK)])
    y = 98
    y += label(s, 'qd/l1', X, y, '검색의 세 단계 (BRIGHT¹의 구분). 예시는 본 발표의 와인 질의') + 4
    y += pipeline(s, 'qd/lv', y, None, D5_LV, gap=18, name_pt=13.5, desc_pt=11.5, arrows=False)
    y += data_row(s, 'qd/ex', y, D5_EX, gap=18) + 14
    y += rich(s, 'qd/drop', X, y, W, 'MTEB 1위였던 일반 임베딩의 점수: Level 2 평가(BEIR) **59.0** → Level 3 평가(BRIGHT) **18.3** (nDCG@10)¹', pt=12.5, color=INK) + 16
    y += label(s, 'qd/l2', X, y, '기록에 사실이 간접적으로 적힌 세 유형 (ImpliRet²의 분류)') + 4
    y += tbl(s, 'qd/t', X, y, W, [16, 28, 34, 22], ['유형', '논문의 예', 'Weave의 예', 'Weave의 처리'], D5_TY, pt=11.5, hi=(0,), pady=7) + 10
    footnote(s, ['¹ Su et al., "BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval", ICLR 2025   '
                 '² Taghavi et al., "ImpliRet: Benchmarking the Implicit Fact Retrieval Challenge", arXiv:2506.14407'], y)
    return s


# ------------------------------------------------------------------ D-6 Reasoning Embedding
D6_BARS = [('일반 임베딩 (MTEB 1위, 7B)', 18.3, '18.3', False), ('LaSER (0.6B)', 23.1, '23.1', True), ('ReasonIR (8B)', 24.4, '24.4', False),
           ('DIVER-Retriever (0.6B)', 25.2, '25.2', True), ('DIVER-Retriever (4B)', 28.9, '28.9', False), ('ReasonEmbed (8B)', 38.1, '38.1', False)]
D6_STEPS = [('Base Model', 'EmbeddingGemma 2의 텍스트 구성 (2.7억 파라미터)'),
            ('학습 데이터', '합성한 (Sub-query, 단서 기록) 쌍 6만~9만 건과 Hard Negative (D-8)'),
            ('학습 방법', 'Contrastive Learning + Knowledge Distillation (Teacher: 서버의 대형 Reasoning Embedding)'),
            ('경량화', 'Matryoshka 학습으로 256-dim, int8 Quantization'),
            ('검증', 'NPU에 올린 뒤 한국어 평가셋의 Recall과 일반 검색 성능의 유지를 확인')]


def s_d6():
    s = page_slide('qd_re', 'D-6', [('Reasoning Embedding: 선행 연구와 튜닝 방법', INK)])
    y, lw = 100, 540
    label(s, 'qd/l1', X, y, 'Reasoning 검색용으로 튜닝한 임베딩 (BRIGHT, nDCG@10)')
    bars, bh = hbars('qd/b', X + 20, y + 52, lw - 40, D6_BARS, vmax=44, pt=11.5, bar_h=16, gap=12)
    cap = rwrap('**0.6B 모델이 8B ReasonIR과 같은 수준**입니다. 점수는 모델 크기보다 학습 데이터가 좌우합니다.', 11.5, lw - 44)
    ch = lh_of(11.5, 1.5) * len(cap)
    ph = 52 + bh + 16 + ch + 18
    s.add('qd/bars', [panel('qd/bp', X, y + 32, lw, ph - 32)] + bars +
          [T('qd/bc', X + 22, y + 52 + bh + 16, lw - 44, ch + 4, cap, size=11.5, color=BODY, lnspc=lh_of(11.5, 1.5) * 0.75)])
    rx, rw = X + lw + 36, W - lw - 36
    label(s, 'qd/l2', rx, y, 'Weave의 튜닝 순서')
    out, yy = [], y + 36
    for i, (a, b) in enumerate(D6_STEPS):
        bl = rwrap(b, 11.5, rw - 34)
        hh = 24 + lh_of(11.5, 1.45) * len(bl) + 14
        if i:
            out.append(R('qd/s/ln%d' % i, rx, yy - 7, rw, 1, fill='E3DDF2', line=None))
        out += [T('qd/s/n%d' % i, rx, yy, 26, 24, str(i + 1), size=13, color=PURPLE, weight='b', anchor='ctr'),
                T('qd/s/a%d' % i, rx + 34, yy, rw - 34, 24, a, size=12.5, color=INK, weight='b', anchor='ctr'),
                T('qd/s/b%d' % i, rx + 34, yy + 26, rw - 34, lh_of(11.5, 1.45) * len(bl) + 4, bl, size=11.5, color=BODY, lnspc=lh_of(11.5, 1.45) * 0.75)]
        yy += hh
    s.add('qd/s', out)
    y = max(y + ph, yy) + 12
    footnote(s, ['점수의 출처: BRIGHT (ICLR 2025), LaSER (SIGIR 2026), ReasonIR (COLM 2025), DIVER-Retriever 모델 카드, ReasonEmbed (ACL 2026). 모두 원 질의 기준.',
                 '2.7억 파라미터 모델의 점수는 한국어 평가셋에서 직접 측정함(D-8). Teacher 후보는 ReasonEmbed 8B와 한국어 임베딩 KURE-v2.'], y)
    return s


# ------------------------------------------------------------------ D-7 Multi-hop Retrieval
D7 = [['Iterative RAG', '추론 한 줄의 생성과 검색을 Hop마다 반복', 'IRCoT (ACL 2023), Self-Ask'],
      ['LLM-free Hop', '찾은 문서로 다음 질의를 구성. Hop 사이에 LLM 없음', 'MDR (ICLR 2021), EfficientRAG (EMNLP 2024)'],
      ['Adaptive Decomposition', '검색 결과로 답이 안 될 때만 질의를 분해', 'Hi-Q (NeurIPS 2026)'],
      ['Graph Index', '색인할 때 LLM이 Knowledge Graph를 만들고 질의할 때 탐색', 'HippoRAG (NeurIPS 2024)']]
D7_BARS = [('Self-Ask', 7.18, '7.2회 · 27.5초', False), ('Hi-Q', 5.7, '5.7회 · 13.5초', False), ('Iter-RetGen', 3, '3회 · 9.7초', False),
           ('EfficientRAG', 1, '1회 · 3.6초', False), ('Weave', 2, '2회 (계획 1, 답변 1)', True)]


def s_d7():
    s = page_slide('qd_hop', 'D-7', [('Multi-hop Retrieval 연구와 Weave의 위치', INK)])
    y, lw = 100, 690
    label(s, 'qd/l1', X, y, '연구의 네 갈래')
    h1 = tbl(s, 'qd/t', X, y + 30, lw, [26, 44, 30], ['계열', '방법', '대표 연구'], D7, pt=11.5, pady=9)
    rx, rw = X + lw + 24, W - lw - 24
    label(s, 'qd/l2', rx, y, '질의 1건의 LLM 호출 수와 소요 시간¹')
    _, bh = hbars('qd/b', rx + 16, 0, rw - 32, D7_BARS, vmax=7.18, pt=11, bar_h=14, gap=11, val_w=136)
    bars, _ = hbars('qd/b', rx + 16, y + 30 + (h1 - bh) / 2, rw - 32, D7_BARS, vmax=7.18, pt=11, bar_h=14, gap=11, val_w=136)
    s.add('qd/bars', [panel('qd/bp', rx, y + 30, rw, h1)] + bars)
    y += 30 + h1 + 22
    y += rich(s, 'qd/w', X, y, W, 'Weave = **Adaptive Decomposition** (필요할 때만 분해하고 계획은 한 번에 작성) + **LLM-free Hop** (Slot을 메타데이터로 채움)', pt=13.5, color=INK) + 14
    y += points(s, 'qd/p', X, y, W, ['**고른 이유.** 온디바이스에서는 LLM 호출 횟수가 지연과 전력을 정합니다. 그래서 호출을 계획 1회와 답변 1회로 고정했습니다.',
                                    '**한계와 보완.** 계획을 처음에 정하기 때문에 첫 Hop이 빗나가면 뒤 Hop도 영향을 받습니다. Slot 후보 2~3개를 모두 검색해서 보완합니다. (C-6)'], gap=8) + 14
    footnote(s, ['¹ Self-Ask, Iter-RetGen, EfficientRAG는 EfficientRAG 논문이 MuSiQue에서 잰 값. Hi-Q는 그 논문의 값(GPT-4o-mini). 모두 서버에서 잰 값이어서 Weave의 시간(0.8~1.7초, B-5)과 바로 견줄 수는 없음.'], y)
    return s


# ------------------------------------------------------------------ D-8 한국어 일상 데이터와 평가
D8 = [('n', 'STEP 1', 'Persona와 사건', '가상의 인물마다 가족, 친구, 직장 관계와 6~12개월 치 사건을 생성', None),
      ('n', 'STEP 2', '앱 기록으로 변환', '사건 하나를 카카오톡, 캘린더, 사진, 메모, 메일의 기록으로 작성. 단서 기록에는 사건의 이름을 쓰지 않음', None),
      ('n', 'STEP 3', '질의와 정답', '질의, 정답 계획, Hop별 정답 기록, 최종 답을 부여 (UX별로)', None),
      ('n', 'STEP 4', 'Hard Negative', '같은 사람의 다른 날, 같은 날의 다른 주제처럼 헷갈리는 기록을 삽입', None),
      ('n', 'STEP 5', '필터링과 검수', 'BM25나 튜닝 전 임베딩으로 풀리는 쉬운 문항을 분리. 한국어 원어민이 검수', None)]
D8_REF = [('ImpliRet (2025)', '암시된 사실을 찾는 문항의 구성'), ('LoCoMo (ACL 2024)', 'Persona와 사건 흐름으로 대화를 합성하는 방법'),
          ('LongMemEval (ICLR 2025)', '평가 항목 (시간 추론, 바뀐 사실, Abstention)'), ('Ko-StrategyQA, K-BrowseComp', '튜닝 후 한국어 기본 성능의 유지 확인')]
D8_MET = ['Hop별 Recall@k', 'Chain 성공률', 'Slot 정확도', '최종 정답률', 'Abstention 정확도', 'Latency']


def s_d8():
    s = page_slide('qd_data', 'D-8', [('한국어 일상 기록 데이터와 평가', INK)])
    y = 98
    y += label(s, 'qd/l0', X, y, '한국어 일상 기록에서 암시된 단서를 찾는 공개 벤치마크가 없어 직접 구축') + 4
    y += pipeline(s, 'qd/f', y, None, D8, gap=14, name_pt=12.5, desc_pt=11) + 24
    lw = 600
    label(s, 'qd/l1', X, y, '참고한 벤치마크와 가져온 것')
    label(s, 'qd/l2', X + lw + 40, y, '평가 지표')
    h1 = deflist(s, 'qd/r', X, y + 34, lw, D8_REF, kw=262)
    rx, rw = X + lw + 40, W - lw - 40
    out = []
    cw = (rw - 12) / 2
    for i, m in enumerate(D8_MET):
        cx, cy = rx + (i % 2) * (cw + 12), y + 34 + (i // 2) * 44
        out += [R('qd/mt/%d' % i, cx, cy, cw, 34, prst='roundRect', radius=10, fill='FFFFFF', line='D9CFFF', line_w=1.0),
                T('qd/mt/%dt' % i, cx, cy, cw, 34, m, size=12, color=INK, weight='m', align='c', anchor='ctr')]
    s.add('qd/mt', out)
    y += 34 + max(h1, 3 * 44 - 10) + 20
    y += rich(s, 'qd/sz', X, y, W, '규모: 학습용 **6만~9만 쌍** (Persona 300명), 평가용 **600문항** (UX마다 200). 비교 대상: BM25, 튜닝 전 EmbeddingGemma 2, 서버의 대형 임베딩(상한)', pt=12, color=INK) + 14
    footnote(s, '합성 순서와 규모는 팀의 온디바이스 검토(11-14) 기준. 말투는 공개된 한국어 메신저 말뭉치를 참고만 하고 원문은 학습에 넣지 않음. 출처는 R-1.', y)
    return s


PAGES = [
    Page('D-1', '모델 구성과 스펙', s_d1,
         q='어떤 모델을 쓰나요? 새로 만들어야 하는 모델이 있나요?',
         a='모델은 셋입니다. 검색은 Google이 지난달 공개한 EmbeddingGemma 2가 맡습니다. 텍스트 구성이 2억 7천만 파라미터이고, Galaxy S26 Ultra에서 질의 하나를 8밀리초에 벡터로 바꿉니다. '
           '질의 재작성과 답변 생성은 기기에 이미 탑재된 Gauss가 맡습니다. 새로 튜닝하는 것은 둘입니다. '
           '임베딩을 한국어 일상 단서에 맞게 튜닝해 Reasoning Embedding으로 만들고, Gauss에는 검색 계획 생성을 학습한 작은 어댑터를 얹습니다. '
           '새 모델을 통째로 싣지 않기 때문에 메모리 부담이 작습니다.',
         more=[('왜 EmbeddingGemma 2인가요?', '기기용으로 나온 임베딩 모델 가운데 가장 최근 것이고, 글과 사진을 같은 공간에 놓을 수 있습니다. 안드로이드가 공식 API로 제공하고 라이선스도 상업 이용이 됩니다.'),
               ('길이를 왜 제한하나요?', '기기 안에서는 읽고 쓰는 길이가 곧 시간입니다. 기록은 256토큰 단위로 색인하고, sLLM이 생성하는 글은 80토큰 안쪽으로 묶었습니다.'),
               ('Gauss 대신 다른 모델도 되나요?', '됩니다. 검색 계획 생성은 2억 7천만 파라미터급 전용 모델로도 할 수 있습니다. 다만 이미 탑재된 Gauss를 쓰면 메모리를 더 쓰지 않습니다.'),
               ('Gauss의 속도는 재 보셨나요?', '임베딩 속도는 Galaxy S26 Ultra에서 직접 쟀습니다. sLLM은 같은 크기의 공개 모델이 Galaxy S25 Ultra와 S26 Ultra에서 낸 속도로 계산했습니다.'),
               ('S펜 그림으로 사진을 찾는 것도 이 모델로 되나요?', 'EmbeddingGemma 2는 그림과 사진을 같은 공간에 놓습니다. 그림만으로는 부족해서, 함께 적은 글자와 메모, 대화를 단서로 같이 씁니다.')],
         basis=['Google, "EmbeddingGemma 2"(2026. 10. 06): Gemma 4 기반, 전체 7.4억 파라미터(글 전용 2.7억, 시각 1.7억, 소리 3억), 768차원(512, 256, 128로 줄일 수 있음), 8K 토큰, Apache 2.0. Pixel 11 Pro에서 글 전용 약 191MB.',
                '모델 카드: 256차원으로 줄이면 MTEB multilingual 평균 61.36 → 60.41. LiteRT-LM 카드(128토큰, 5회 평균): Pixel 11 Pro TPU 8.3ms(112MB), S26 Ultra CPU 27.1ms(334MB), GPU 25.9ms(333MB).',
                '생성 속도(LiteRT-LM 공개값): FunctionGemma 270M은 S25 Ultra CPU에서 초당 154토큰, Gemma 3 1B는 S25 Ultra NPU에서 85토큰, Gemma 4 E2B는 S26 Ultra GPU에서 52토큰. Apple의 3B는 iPhone 15 Pro에서 30토큰.',
                'Android ML Kit GenAI Embeddings API(Preview): EmbeddingGemma 2를 AICore가 관리, 입력 한도 256토큰.',
                '길이(검토 자료 6장의 가정): 재작성 입력 130토큰, 계획 출력 44~82토큰, 답 입력 170~540토큰, 출력 10~80토큰.',
                'Samsung Gauss2: SDC24 Korea(2024. 11. 21)에서 공개. 콤팩트(온디바이스용), 밸런스드, 슈프림. 3B와 1B의 온디바이스 탑재는 팀 조사 기준.']),
    Page('D-2', 'Query Rewriting의 종류', s_d2,
         q='질의를 다시 쓴다는 게 정확히 무엇인가요? 여러 방식이 있을 텐데 어떤 걸 쓰나요?',
         a='Query Rewriting에는 여러 종류가 있습니다. 앞 대화를 가리키는 말을 풀어 쓰는 것, 검색에 맞는 표현으로 고치는 것, 질의를 나누는 것, 그리고 질의에 긴 추론을 덧붙이는 것입니다. '
           'Weave가 쓰는 것은 질의를 나누는 Query Decomposition입니다. 한 번에 찾을 수 없는 질의를 순서가 있는 하위 질의로 나누고, 앞의 결과가 필요한 자리는 빈칸으로 둡니다. '
           '이 방식을 고른 이유는 출력 길이입니다. 검색 계획은 40에서 80토큰이라 기기에서 1초 안팎에 생성합니다. '
           '추론을 길게 덧붙이는 방식은 수백 토큰을 생성해야 해서 기기에서는 10초 가까이 걸립니다.',
         more=[('작은 모델이 질의를 나눌 수 있나요?', '튜닝을 전제로 합니다. 2억 7천만 파라미터 모델도 튜닝하면 정해진 형식으로 출력하는 정확도가 58%에서 85%로 오릅니다. 다음 장에 근거를 모았습니다.'),
               ('추론을 덧붙이는 방식이 성능은 더 좋지 않나요?', '긴 질의를 다루는 벤치마크에서는 그렇습니다. 다만 휴대폰에서 들어오는 질의는 짧고, 저희는 추론을 임베딩이 맡도록 튜닝하는 쪽을 골랐습니다.'),
               ('검색 서비스들도 Query Rewriting을 하나요?', '합니다. Azure AI Search는 질의마다 변형을 최대 10개 만드는 소형 모델을 두고 있고, OpenAI의 파일 검색도 질의를 다시 써서 찾습니다.')],
         basis=['종류와 길이는 사용자의 검토 자료(11-14) 8장과 11장. 500토큰 ÷ 초당 52토큰(Gemma 4 E2B, S26 Ultra GPU) = 9.6초. 검토 자료는 TongSearch-QR의 설정(최대 500토큰)을 더 느린 구성으로 16초로 적음.',
                'Google, FunctionGemma 모델 카드: Gemma 3 270M 기반, Mobile Actions 평가에서 기본 모델 58%, 학습 뒤 85%.',
                'RQ-RAG(Chan et al., arXiv 2404.00610): Llama2-7B 하나가 다시 쓰기, 나누기, 모호함 풀기를 학습. 단일 홉 QA에서 이전 최고보다 평균 1.9% 위.',
                'HyDE(Gao et al., ACL 2023), Query2doc(Wang et al., EMNLP 2023).',
                'Azure AI Search: 파인튜닝한 소형 모델로 질의당 변형 최대 10개, 32토큰 질의에 147ms(서버). Sadeghi & Lin(SIGIR-AP 2026): 0.5B 모델로 돌린 확장 기법의 62.8%가 키워드 검색보다 낮음(검토 자료).']),
    Page('D-3', '작은 모델의 Query Rewriting', s_d3,
         q='질의를 다시 쓰는 일을 작은 모델이 할 수 있다는 근거가 있나요? 보통은 큰 LLM이 하지 않나요?',
         a='두 연구를 근거로 삼았습니다. 첫째는 2023년 EMNLP에 나온 연구입니다. 7억 7천만 파라미터의 T5 모델에게 ChatGPT의 Rewriting을 따라 하게 한 뒤, '
           '검색과 정답 결과를 보상으로 강화학습을 했습니다. 그 결과 ChatGPT가 다시 쓴 것보다 조금 높은 정확도가 나왔습니다. '
           '둘째는 Apple의 ReALM입니다. 화면이나 앞 대화를 가리키는 말이 무엇을 가리키는지 맞히는 과제에서, 8천만 파라미터 모델이 GPT-4와 비슷한 정확도를 냈습니다. '
           'Apple은 이 연구에서 기기 안에 둘 수 있는 시스템을 목표로 밝혔습니다. 두 연구 모두 짧은 Rewriting은 튜닝한 작은 모델로 충분하다는 것을 보여 줍니다.',
         more=[('강화학습은 어떻게 했나요?', '다시 쓴 질의로 실제 검색을 하고, 읽는 모델이 답을 맞혔는지와 정답이 검색 결과에 들어 있는지를 보상으로 줬습니다.'),
               ('ReALM의 과제는 Weave와 다르지 않나요?', '과제는 다릅니다. 다만 ‘그날’, ‘거기’ 같은 지시어를 푸는 일이 같고, 출력이 짧다는 점이 같습니다.'),
               ('한국어로도 그만큼 되나요?', '한국어 평가셋을 먼저 만들고 거기서 측정합니다. 만드는 방법은 D-8에 있습니다.')],
         basis=['Ma et al., "Query Rewriting for Retrieval-Augmented Large Language Models", EMNLP 2023: T5-large(770M). 워밍업은 LLM의 다시 쓰기 가운데 읽는 모델이 맞힌 것만. PPO의 보상 = EM + F1 + Hit − β·KL. '
                '표 2(EM/F1): HotpotQA 직접 32.36/43.05, 검색 후 읽기 30.47/41.34, LLM 재작성 32.80/43.85, 학습형 34.38/45.97. AmbigNQ 47.80(LLM 46.40), PopQA 45.72(LLM 46.00). AmbigNQ 검색 적중률 76.4% → 77.5%(LLM) → 82.2%(학습형).',
                'Moniz et al., "ReALM", SIGDIAL 2024(Apple): 데이터(학습/시험) 대화 2.3k/1.2k, 합성 3.9k/1.1k, 화면 10.1k/1.9k. 정확도(대화/합성/화면/처음 보는 영역) GPT-4 97.0/58.7/90.1/98.4, ReALM-80M 96.7/99.5/88.9/99.3, ReALM-3B 97.9/99.8/93.0/97.8. '
                '"a practical reference resolution system that can exist on-device without compromising on performance".',
                'DeepRetrieval(arXiv 2503.00223): 3B, 문헌 검색 재현율 65.07%(이전 최고 24.68%), 13개 중 11개에서 GPT-4o와 Claude-3.5-Sonnet보다 위. ConvSearch-R1(EMNLP 2025): QReCC MRR@3 56.5, 학습 전 27.3, InfoCQR 48.9. '
                'TongSearch-QR(arXiv 2506.11603): 1.5B가 BRIGHT에서 BM25 14.5 → 24.6, GPT-4o 26.5(11-02 조사에서 원문 확인).']),
    Page('D-4', 'Query Rewriter 튜닝', s_d4,
         q='Query Rewriter는 어떤 데이터로 어떻게 튜닝하나요? 사용자의 기록을 쓰나요?',
         a='실제 사용자의 기록은 쓰지 않습니다. 한국어 일상 기록을 합성해서 씁니다. 순서는 이렇습니다. 먼저 서버의 큰 LLM이 쓴 검색 계획을 정답으로 학습합니다. '
           '그다음 그 계획을 합성 기록에 실제로 실행해 보고, 정답 기록에 도달한 계획만 남깁니다. 마지막으로 검색된 기록의 순위를 보상으로 주는 강화학습으로 다듬습니다. '
           '학습한 것은 Gauss에 얹는 작은 어댑터입니다. Gauss 자체는 바꾸지 않습니다. '
           '한 번에 찾을 수 있는 질의와 답이 없는 질의도 함께 넣어서, 나누지 말아야 할 때 나누지 않게 학습합니다.',
         more=[('강화학습까지 필요한가요?', '큰 모델을 따라 하는 것만으로는 우리 검색기에 맞는 계획인지 알 수 없습니다. 실제로 검색되는지를 보상으로 줘야 검색에 맞는 계획을 씁니다.'),
               ('어댑터 방식의 선례가 있나요?', 'Apple이 기기 안의 모델 하나에 기능마다 어댑터를 얹는 방식을 공개했습니다. 어댑터 하나가 수십 메가바이트입니다.'),
               ('형식이 깨진 출력이 나오면요?', '기기용 런타임이 정해진 형식으로만 출력하게 강제하는 기능을 제공합니다. 그래서 형식이 깨진 계획은 나오지 않습니다.'),
               ('다른 작업용 어댑터와 같이 쓸 수 있나요?', '됩니다. 어댑터는 필요할 때 불러와 갈아 끼우는 방식이라, 요약용과 계획용을 따로 둘 수 있습니다.')],
         basis=['학습 순서는 검토 자료 3장과 11-02 조사(온디바이스 질문 다시 쓰기 주체). RRR의 워밍업("Those that get correct predictions from the LLM reader are selected")과 PPO, ConvSearch-R1의 순위 보상.',
                'Apple, "Introducing Apple\'s On-Device and Server Foundation Models"(2024. 06. 10): "adapters, each fine-tuned for a specific feature", "the parameters for a rank 16 adapter typically require 10s of megabytes", "dynamically loaded, temporarily cached in memory, and swapped".',
                'LiteRT-LM의 constrained decoding(Google Developers Blog). Hi-Q: 늘 나누는 정책 60.7 → 57.3 EM.',
                '계획의 모양(검토 자료): 하위 질의, 빈칸, 검색할 앱, 필터. 예: 1 ‘지은이네 집들이는 언제였지?’(카카오톡, 캘린더, [그날] ← 날짜), 2 ‘[그날] 마셨던 와인은?’(갤러리).']),
    Page('D-5', 'Reasoning 검색의 정의와 유형', s_d5,
         q='Reasoning Embedding이 추론한다는 게 구체적으로 무엇인가요? 일반 임베딩과 무엇이 다른가요?',
         a='검색에는 세 단계가 있습니다. 같은 단어를 찾는 단계, 의미가 비슷한 것을 찾는 단계, 그리고 추론을 한 번 거쳐야 이어지는 것을 찾는 단계입니다. '
           '와인 예시에서 ‘집들이가 언제였지’라는 질의와 ‘박스 정리 다 했어, 휴지 안 사 와도 돼’라는 메시지는 단어도 의미도 다릅니다. 새집에 휴지를 사 간다는 것을 알아야 이어집니다. '
           '일반 임베딩은 둘째 단계까지 잘합니다. 셋째 단계를 재는 벤치마크에서는 점수가 59점에서 18점으로 떨어집니다. '
           '기록에 사실이 간접적으로 적힌 경우는 세 유형으로 나뉩니다. 관습이나 별칭 같은 상식이 필요한 유형, 시간 표현을 풀어야 하는 유형, 계산이 필요한 유형입니다. '
           'Reasoning Embedding이 배우는 것은 이 가운데 첫 번째로, 논문에서 World Knowledge라고 부르는 유형입니다. '
           '시간 표현은 색인할 때 날짜로 바꿔 두고, 계산은 답변을 생성하는 단계가 맡습니다.',
         more=[('World Knowledge라는 게 어떤 건가요?', '관습이나 별칭처럼 글에 쓰여 있지 않은 상식입니다. 집들이에 휴지를 사 간다는 것, 갈색병이 어느 제품의 별명인지 같은 것입니다.'),
               ('질의를 더 잘 쓰면 일반 임베딩으로도 되지 않나요?', '질의 쪽이 복잡한 경우에는 도움이 됩니다. 기록 쪽이 돌려 말한 경우에는 질의를 고쳐 써도 점수가 오르지 않았습니다. 그래서 임베딩을 튜닝합니다.'),
               ('LLM에게 후보를 다 읽히면 되지 않나요?', '정답 기록만 주면 GPT-4.1이 88점을 내지만, 헷갈리는 기록 29건과 함께 주면 23점으로 떨어졌습니다. 먼저 잘 찾아야 합니다.')],
         basis=['Su et al., "BRIGHT", ICLR 2025: level 1 keyword-based, level 2 semantic-based, level 3 reasoning-based. 12개 데이터셋 1,384질의(StackExchange 7, 코딩 2, 정리 기반 3). SFR-Embedding-Mistral이 BEIR 59.0, BRIGHT 18.3. 최고 24.3. LLM의 추론을 질의로 쓰면 최대 12.2점.',
                'Taghavi et al., "ImpliRet", arXiv 2506.14407: "relevance depends on information that is implicitly stated in the document". BRIGHT는 "the reasoning burden lies on the query side". 세 유형(temporal, arithmetic, world knowledge)과 예시는 논문 그대로(산술의 원문: "Which bag costs $1,600?" ↔ "The Prada bag costs $2,000, the Gucci bag is 20% cheaper"). '
                'nDCG@10: Dragon+ 14.91(세계 지식 17.46, 산술 14.61, 시간 12.66), ReasonIR 13.64, BM25 12.24. 정답 문서만 줄 때와 30건을 줄 때: GPT-4.1 88.05 → 22.90, o4-mini 92.74 → 55.54.',
                '세 단계의 예는 본 발표의 화면: 키워드 검색 장의 캘린더 ‘성빈이 신혼집들이’(10월 18일), 임베딩 장의 메모 ‘소믈리에 추천’(샤토 마고), 지은의 카카오톡(3월 15일).',
                'Weave의 예를 세 유형에 맞춘 것은 내 정리: 휴지와 집들이, 갈색병(세계 지식), ‘이따 올 때’(시간), 배 2개(산술, E-1의 갈비찜 장면).']),
    Page('D-6', 'Reasoning Embedding 튜닝', s_d6,
         q='Reasoning Embedding은 어떻게 만드나요? 그런 모델이 실제로 있나요?',
         a='작년부터 추론이 필요한 검색을 위해 튜닝한 임베딩이 잇달아 나왔습니다. ReasonIR은 어려운 질의와 헷갈리는 오답을 합성해 학습했고, 같은 벤치마크에서 일반 임베딩의 18점을 24점으로 올렸습니다. '
           '올해 나온 ReasonEmbed는 38점까지 올렸습니다. 저희가 눈여겨본 것은 크기입니다. 6억 파라미터 모델이 80억 파라미터 모델과 같은 수준의 점수를 냈습니다. '
           '크기보다 학습 데이터가 점수를 좌우한다는 뜻입니다. 그래서 저희는 기기용인 EmbeddingGemma 2를 바탕으로, 한국어 일상 단서 쌍을 합성해 튜닝합니다. '
           '서버의 큰 Reasoning Embedding을 Teacher로 삼고, 튜닝한 뒤에는 기기에 올릴 크기로 줄여 성능이 유지되는지 확인합니다.',
         more=[('2억 7천만 파라미터로 그만큼 되나요?', '6억 파라미터 모델이 80억 파라미터 모델과 같은 수준을 낸 결과가 가능성의 근거입니다. 저희 모델의 점수는 한국어 평가셋을 만들어 직접 측정합니다.'),
               ('튜닝하면 일반 검색 성능이 떨어지지 않나요?', '일반 한국어 검색 쌍을 섞어 학습하고, 튜닝 뒤에 한국어 검색 점수가 유지되는지 따로 확인합니다.'),
               ('AgentIR의 메모 방식은 쓰지 않나요?', '후보로 두고 있습니다. 메모를 쓰는 만큼 생성이 길어져 시간이 듭니다. 정확도가 그만큼 오르는지 측정한 뒤에 정합니다.'),
               ('엉뚱한 기록을 가깝다고 하면요?', '후보를 여러 개 가져와 날짜와 사람으로 한 번 더 필터링합니다. 키워드 검색도 함께 씁니다.')],
         basis=['Shao et al., "ReasonIR", COLM 2025: Llama3.1-8B, ReasonIR-Synthesizer(길이가 다양한 질의, 어려운 질의, 헷갈리는 오답). BRIGHT 24.4 → 29.9(GPT-4 재작성) → 36.9(재순위). 기존 학습 질의는 NQ 20토큰, MS MARCO 21토큰으로 짧음.',
                'Chen et al., "ReasonEmbed", ACL 2026(arXiv 2510.08252): ReMixer로 8.2만 건, Redapter, Qwen3-8B 백본이 BRIGHT 38.1.',
                'DIVER-Retriever 모델 카드(AQ-MedAI/Diver-Retriever-0.6B, 11-16 확인): BRIGHT 원 질의 평균 0.6B 25.2, 4B 28.9, ReasonIR-8B 24.4, BM25 14.5. DIVER 논문(arXiv 2508.07995 v5)의 전체 파이프라인은 46.8, 원 질의 31.9.',
                'Jin et al., "LaSER", SIGIR 2026: 0.6B 23.1, 다시 쓴 뒤 찾기 22.4. BRIGHT(ICLR 2025): SFR-Embedding-Mistral(7B) 18.3.',
                'Chen et al., "AgentIR", arXiv 2603.04384: "AgentIR-4B achieves 68% accuracy with the open-weight agent Tongyi-DeepResearch, compared to 50% with conventional embedding models twice its size, and 37% with BM25".',
                '튜닝 순서는 검토 자료 3장(대조 학습, 헷갈리는 오답의 종류, Teacher ReasonEmbed 8B와 AgentIR-4B와 KURE-v2, Matryoshka, 재양자화 확인). Google의 EmbeddingGemma 2 파인튜닝 안내(Sentence Transformers).']),
    Page('D-7', 'Multi-hop Retrieval 연구', s_d7,
         q='여러 번 이어 찾는 연구는 어디까지 와 있나요? 그 가운데 왜 이 방식을 골랐나요?',
         a='크게 두 갈래입니다. 하나는 Hop마다 LLM을 부르는 방식입니다. IRCoT가 대표적이고, 정확하지만 질의 하나에 LLM을 여러 번 부릅니다. 공개 실험에서 10초에서 27초가 걸렸습니다. '
           '다른 하나는 Hop 사이에 생성을 하지 않는 방식입니다. MDR은 찾은 문단을 질의에 붙여 다시 임베딩했고, EfficientRAG는 작은 분류기로 다음 질의를 만들었습니다. '
           '올해 나온 Hi-Q는 한 번에 안 풀릴 때만 질의를 나누는 쪽이 항상 나누는 것보다 정확하다는 것을 보였습니다. '
           'Weave는 이 둘을 합쳤습니다. 필요할 때만 나누되 계획은 한 번에 쓰고, Hop 사이의 빈칸은 찾은 기록의 날짜와 사람으로 채웁니다. '
           '그래서 LLM을 부르는 횟수가 계획과 답변, 두 번으로 고정됩니다.',
         more=[('왜 Hi-Q처럼 Hop마다 확인하지 않나요?', 'Hi-Q는 질의 하나에 큰 모델을 평균 다섯 번 넘게 부릅니다. 기기에서는 그만큼 부를 수 없어서, 계획은 한 번에 쓰고 확인은 모델 없이 합니다.'),
               ('계획을 처음에 정하면 중간에 틀렸을 때 못 고치지 않나요?', '그 위험이 있습니다. 그래서 빈칸의 후보가 갈리면 두세 개를 모두 검색합니다. 한 번에 0.02초라 부담이 없습니다.'),
               ('이 숫자들이 Weave의 성능인가요?', '아닙니다. 다른 연구진이 영어 데이터로 서버에서 잰 값입니다. 방식을 고른 근거로만 씁니다.'),
               ('Knowledge Graph를 쓰는 방식은요?', 'HippoRAG처럼 색인할 때 LLM이 그래프를 만들어 두는 방식입니다. 정리된 사실에 강하고, 저희 방식과는 서로 보완합니다. A-4와 A-5에 정리했습니다.')],
         basis=['Xiong et al., MDR, ICLR 2021: "matching the best published accuracy on HotpotQA while being 10 times faster at inference time". Trivedi et al., IRCoT, ACL 2023: 검색 최대 21점, QA 최대 15점.',
                'Zhuang et al., EfficientRAG, EMNLP 2024: MuSiQue 질문당 LLM 1회 3.62초, Iter-RetGen 3회 9.68초, Self-Ask 7.18회 27.47초.',
                'Gutiérrez et al., HippoRAG, NeurIPS 2024: "comparable or better performance than iterative retrieval like IRCoT while being 10-20 times cheaper and 6-13 times faster".',
                'Kim et al., Hi-Q, NeurIPS 2026: 질문당 LLM 평균 5.7회, 13.5초(GPT-4o-mini). 늘 나누면 60.7 → 57.3 EM.',
                'Weave의 2회와 0.8~1.7초는 UX2 기준(B-5).']),
    Page('D-8', '한국어 데이터와 평가', s_d8,
         q='성능은 무엇으로 어떻게 잴 건가요? 맞는 데이터가 있나요?',
         a='한국어 일상 기록에서 숨은 단서를 찾는 공개 벤치마크는 없습니다. 있는 것은 영어이고, 학술 문서나 긴 대화가 중심입니다. 그래서 직접 만듭니다. '
           '가상의 인물과 한 해 치 사건을 먼저 만들고, 사건 하나를 카카오톡과 캘린더, 사진 같은 여러 앱의 기록으로 나누어 씁니다. 단서가 되는 기록에는 사건의 이름을 쓰지 않습니다. '
           '여기에 질의와 정답, 헷갈리는 기록을 더하고 사람이 검수합니다. 평가 지표는 여섯 가지입니다. Hop마다 정답 기록을 찾았는지, 끝까지 이어졌는지, '
           '빈칸을 맞게 채웠는지, 답이 맞는지, 기록에 없을 때 답하지 않는지, 그리고 기기에서 걸리는 시간입니다.',
         more=[('직접 측정한 숫자가 있나요?', '임베딩 속도는 Galaxy S26 Ultra에서 직접 쟀습니다. 검색 정확도는 평가 문항 600개를 만들어 재는 것이 다음 단계이고, 지금은 같은 구성으로 잰 공개 연구의 값을 근거로 삼았습니다.'),
               ('왜 기존 벤치마크를 쓰지 않나요?', '기존 것은 영어 위키백과나 StackExchange가 대상입니다. 한국어 메신저 말투와 일상 단서는 들어 있지 않습니다. 만드는 방법은 그 연구들에서 가져왔습니다.'),
               ('합성 데이터가 실제와 다르면요?', '평가 문항은 한국어 원어민이 검수하고, 동의를 받은 내부 사용자의 실제 질의를 조금 보탭니다.'),
               ('규모는 어느 정도인가요?', '학습용은 6만에서 9만 쌍, 평가용은 UX마다 200문항씩 600문항을 생각하고 있습니다.')],
         basis=['합성 순서와 지표, 규모는 검토 자료 4장(가상의 사람 300명 × 체인 100개 = 3만 체인, 학습 쌍 6만~9만. ReasonEmbed의 합성 8.2만 건과 같은 자릿수).',
                'ImpliRet(arXiv 2506.14407), LoCoMo(Maharana et al., ACL 2024: 대화당 평균 600턴), LongMemEval(Wu et al., ICLR 2025: 500문항, LLM이 낸 질문의 약 5%만 남김), LoCoMo-Plus(Li et al., arXiv 2602.10715).',
                '한국어: Ko-StrategyQA(번역, 위키백과), K-BrowseComp(arXiv 2606.02404, 400문항). 한국어 일상 기록용은 찾지 못함(검토 자료).',
                '가상의 사람은 공개된 한국어 합성 페르소나(Nemotron-Personas-Korea, CC BY 4.0)를 씨앗으로 쓸 수 있음(검토 자료).']),
]
