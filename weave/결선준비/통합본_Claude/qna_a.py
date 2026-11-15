"""Appendix A 묶음: 기존 기술과의 차이 (11-16 3판).

A-1 비교 지도(cmp_new 그대로), A-2 기능별 비교(표 하나), A-3 Finder(팀원 SB-Jo의 장을 옮겨 옴), A-4 Personal Data Engine(Knowledge Graph)과의 차이(두 줄 흐름 그림),
A-5 PDE와 함께 쓰는 방법(주고받는 그림 + 세 단계), A-6 AI Agent(Pickle, Muse)와의 관계, A-7 LLM에게 전부 읽히는 방식과의 차이, A-8 Apple과 Google의 개인 기록 검색.
3판: 문장 제목과 부제를 버리고, A-6과 A-7은 질문과 답 세 줄 + 작은 그림(A-3과 같은 짜임), A-4와 A-5는 그림 + 짧은 설명, A-2와 A-8은 표 하나.
(11-15: '가전과 TV에서는 이미 하고 있지 않나요?' 장은 만들었다가 필요 없다는 검토를 받아 뺌.)
숫자와 출처는 `Appendix_QnA_대본.md`의 근거에 있다.
"""
from pathlib import Path

from ui import (BODY, INK, LAV, LAV2, MUTE, PURPLE, PURPLE2, RING, SUB, R, T)

from qna_lib import (GRAY_BG, Page, Slide, arrow, box, footnote, frame, label, notes3, page_slide, pipeline, points, qrow, step, tbl, vis_bars, vis_nums, vis_steps)

HERE = Path(__file__).resolve().parent
FINDER_SRC = HERE / '원본' / 'Appendix_Finder와의_차별점_QA_SB-Jo.pptx'
X, W = 70, 1140
HI = dict(color=PURPLE, weight='b')


# ------------------------------------------------------------------ A-1 비교 지도
def s_a1():
    import cmp_new
    return frame(cmp_new.s_cmp_apx2(), 'A-1')


# ------------------------------------------------------------------ A-2 기능별 비교
A2 = [['Samsung Finder', '기기 안의 앱, 일정, 노트, 파일을 자연어로 검색해 목록으로 표시¹', '찾은 기록을 단서로 다음 기록까지 연쇄 탐색하고, 답을 입력하던 자리에 제공 (A-3)'],
      ['Samsung Now Nudge', '지금 화면의 대화에 맞는 사진이나 일정을 제안²', '화면에 없는 다른 앱의 기록까지 이어서 제안'],
      ['Samsung Writing Assist', '작성한 글의 문체 변환, 맞춤법과 문법 교정³', '글에 넣을 내용을 사용자의 기록에서 검색해 제안'],
      ['Kanana in KakaoTalk', '카카오톡 대화를 기기 안에서 읽고 먼저 제안⁴', '카카오톡 밖의 사진, 메모, 일정, 메일까지 함께 검색']]
A2_S = [['키워드 검색 (BM25)', '같은 단어가 있는 기록을 검색', '‘집들이’라는 단어가 없는 초대 메시지도 검색 (D-5)'],
        ['일반 임베딩 검색', '의미가 비슷한 기록을 한 번에 검색', 'Reasoning Embedding으로 추론 단서를 찾고, Query Rewriter로 연쇄 탐색']]


def s_a2():
    s = page_slide('qa_tbl', 'A-2', [('기존 기능, 검색 방식과의 비교', INK)])
    y = 98
    y += label(s, 'qa/l1', X, y, 'Galaxy AI와 다른 서비스 (Apple과 Google은 A-8)') + 4
    y += tbl(s, 'qa/t', X, y, W, [19, 39, 42], ['기능', '하는 일', 'Weave가 다른 점'], A2, pady=10) + 22
    y += label(s, 'qa/l2', X, y, '검색 방식') + 4
    y += tbl(s, 'qa/t2', X, y, W, [19, 39, 42], ['방식', '하는 일', 'Weave가 다른 점'], A2_S, pady=10) + 12
    footnote(s, ['¹ Samsung 지원, "Understanding Finder on Galaxy phones" (One UI 8.5부터 자연어 검색)   ² Samsung Newsroom, Galaxy S26 발표 (2026. 02)   ³ Samsung 지원, Writing Assist   '
                 '⁴ 카카오 보도자료 (2025. 09. 23)'], y)
    return s


# ------------------------------------------------------------------ A-3 Finder (옮겨 온 장을 손봄)
FINDER_FOOT = ('Finder 자연어 검색의 공식 대상은 음성 녹음, 통화 녹음, 캘린더, 노트, 리마인더, 내 파일입니다 '
               '(Samsung 지원, "Understanding Finder on Galaxy phones").')


def patch_finder(slide):
    """옮겨 온 Finder 장: 'Appendix 참조'를 코드로 바꾼다. 돌려줌: 틀 위에 더 그릴 Slide."""
    refs = iter(['(자세한 설명은 D-2, D-5)', '(자세한 설명은 C-1)'])
    from qna_lib import A_NS, live_tree
    n = 0
    for t in live_tree(slide).iter('{%s}t' % A_NS):
        if t.text and '(자세한 설명은 Appendix 참조)' in t.text:
            t.text = t.text.replace('(자세한 설명은 Appendix 참조)', next(refs))
            n += 1
    assert n == 2, 'Finder 장의 글이 바뀜: Appendix 참조 %d곳' % n
    s = Slide('qa_finder', trans=('fade', 400), bar=False, notes='')
    frame(s, 'A-3')
    s.add('qa/ffoot', [T('qa/ffoot', 50, 678, 1180, 18, FINDER_FOOT, size=8.5, color='8E88A0')])   # 옮겨 온 장의 각주(x=50)에 맞춤
    return s


# ------------------------------------------------------------------ A-4 Personal Data Engine과의 차이
def lane(s, key, y, title, sub, steps, on=(), h=96):
    lw = 214
    out = [box(key + '/bg', X, y, W, h, radius=18, shadow=False),
           T(key + '/t', X + 22, y + h / 2 - 26, lw - 30, 24, title, size=14, color=INK, weight='b', anchor='ctr'),
           T(key + '/s', X + 22, y + h / 2, lw - 30, 20, sub, size=11, color=PURPLE, weight='b', anchor='ctr')]
    n, gap = len(steps), 26
    bw = (W - lw - 20 - gap * (n - 1)) / n
    for i, (name, small) in enumerate(steps):
        bx = X + lw + i * (bw + gap)
        out += step('%s/p%d' % (key, i), bx, y + 16, bw, h - 32, name, small, style='on' if i in on else 'base', pt=12, sub_pt=10)
        if i < n - 1:
            out.append(arrow('%s/a%d' % (key, i), (bx + bw + 3, y + h / 2), (bx + bw + gap - 3, y + h / 2), color='A79FBD', w=1.6))
    s.add(key, out)


def s_a4():
    s = page_slide('qa_kg', 'A-4', [('Personal Data Engine(Knowledge Graph)과 Weave의 차이', INK)])
    y = 104
    lane(s, 'qa/k1', y, 'Personal Data Engine¹', '기록이 들어올 때 정리',
         [('앱의 기록', None), ('사실 추출', ['ML과 LLM으로', '사람, 일정, 장소를 추출']), ('Knowledge Graph', ['Ontology 규칙으로 추론한', '사실까지 저장 (RDFox)']), ('그래프 조회', '질의가 오면 바로 조회')], on=(1, 2))
    lane(s, 'qa/k2', y + 96 + 14, 'Weave', '질의가 들어올 때 연결',
         [('앱의 기록', None), ('원문 색인', ['벡터 + 메타데이터.', '사실을 미리 추출하지 않음']), ('검색 계획', ['Query Rewriter가', 'Sub-query로 분해']), ('원문 검색', ['Reasoning Embedding으로', '단서를 찾아 연결'])], on=(2, 3))
    y += 2 * 96 + 14 + 14
    s.add('qa/kn', [T('qa/kn', X, y, W, 22, '보라색 칸이 추론이 일어나는 곳입니다. PDE는 기록이 들어올 때, Weave는 질의가 들어올 때 추론합니다.', size=11.5, color=SUB, anchor='ctr')])
    y += 22 + 24
    y += notes3(s, 'qa/n', y, [('PDE가 강한 곳', '사람, 날짜, 장소처럼 **정리된 사실**을 빠르고 정확하게 조회합니다. Now Brief가 이 위에서 동작합니다.'),
                               ('Weave가 채우는 곳', '**미리 정리되지 않은 표현**입니다. ‘휴지 안 사 와도 돼’는 받는 순간에 집들이로 추출하기 어렵습니다. Weave는 질의가 들어온 뒤에 원문에서 찾습니다.'),
                               ('미리 추출하는 방식의 한계', '그래프 기반 검색의 오류 100건 가운데 **76건이 정보를 미리 추출하는 단계**에서 나왔습니다.² 추출이 놓친 부분을 원문 검색이 보완합니다.')]) + 20
    footnote(s, ['¹ Crocker, Horrocks, Nenov, "Semantic Technology in Your Pocket", ISWC 2025 Industry Track: PDE는 여러 앱의 데이터를 ML과 LLM으로 분석한 결과를 '
                 '개인 Knowledge Graph에 저장하고, Ontology가 함의하는 사실을 더해 둠.',
                 '² Gutiérrez et al., "HippoRAG", NeurIPS 2024, 부록 F (MuSiQue 오류 분석).'], y)
    return s


# ------------------------------------------------------------------ A-5 PDE와 함께 쓰는 방법
A5 = [('n', 'STEP 1', '메타데이터 필터링', '날짜, 사람, 앱으로 필터링합니다. Weave만으로 가능합니다.', '지금'),
      ('n', 'STEP 2', 'PDE의 사실을 필터로', 'PDE가 아는 사람, 일정, 장소를 Weave의 필터로 써서 검색 범위를 좁힙니다.', None),
      ('n', 'STEP 3', '찾은 연결을 그래프로', 'Weave가 찾은 연결을 그래프의 사실로 올려, 다음에는 그래프가 바로 답합니다.', None)]


def s_a5():
    s = page_slide('qa_kg2', 'A-5', [('Personal Data Engine과 Weave를 함께 쓰는 방법', INK)])
    y, bw, bh = 104, 300, 116

    def side(key, x, title, a, b, on):
        return [box(key + '/bg', x, y, bw, bh, on=on, radius=18, shadow=False),
                T(key + '/t', x + 22, y + 16, bw - 44, 26, title, size=14.5, color=PURPLE if on else INK, weight='b', anchor='ctr'),
                T(key + '/a', x + 22, y + 50, bw - 44, 20, a, size=11.5, color=SUB, anchor='ctr'),
                T(key + '/b', x + 22, y + 76, bw - 44, 22, b, size=12.5, color=INK, weight='m', anchor='ctr')]
    s.add('qa/k5/l', side('qa/k5/l', X, 'PDE Knowledge Graph', '기록이 들어올 때 정리한 사실', '사람, 일정, 장소, 예약', False))
    s.add('qa/k5/r', side('qa/k5/r', X + W - bw, 'Weave', '질의가 들어올 때 원문에서 찾는 단서', '대화, 메모, 사진, 파일', True))
    mx, mw = X + bw + 26, W - 2 * bw - 52
    rows = [('필터 제공', '그래프가 아는 사람, 일정, 장소로 Weave의 검색 범위를 좁힘', True),
            ('새 사실 제공', 'Weave가 찾고 사용자가 확인한 연결을 그래프에 추가', False)]
    for i, (title, text, fwd) in enumerate(rows):
        yy = y + 6 + i * 56
        a, b = ((mx, yy + 26), (mx + mw, yy + 26)) if fwd else ((mx + mw, yy + 26), (mx, yy + 26))
        s.add('qa/k5/m%d' % i, [T('qa/k5/m%d/t' % i, mx, yy, mw, 22, title, size=12.5, color=PURPLE, weight='b', align='c', anchor='ctr'),
                                arrow('qa/k5/m%d/a' % i, a, b, w=2.0),
                                T('qa/k5/m%d/b' % i, mx, yy + 31, mw, 20, text, size=11, color=BODY, align='c', anchor='ctr')])
    y += bh + 26
    y += label(s, 'qa/l', X, y, '적용 순서') + 4
    y += pipeline(s, 'qa/f', y, None, A5, gap=18, name_pt=13, desc_pt=11.5) + 24
    y += points(s, 'qa/p', X, y, W, ['**서로 잘하는 질의가 다릅니다.** 그래프 검색과 원문 검색을 함께 쓰면 성능이 일관되게 오른다는 비교 연구가 있습니다.¹',
                                    '**사용자가 확인한 연결만 그래프에 올립니다.** Weave가 찾기만 한 연결은 후보로 두고, 사용자가 그 답을 실제로 썼을 때만 사실로 올려서 잘못된 연결이 쌓이지 않게 합니다.'], gap=8) + 14
    footnote(s, ['¹ Han et al., "RAG vs. GraphRAG: A Systematic Evaluation and Key Insights", arXiv:2502.11371 (2025)',
                 'PDE의 다음 목표는 여러 앱과 여러 기기에 걸친 개인화 (Crocker, Horrocks, Nenov, ISWC 2025 Industry Track).'], y)
    return s


# ------------------------------------------------------------------ A-6 AI Agent
def vis_layers(top, bottom, mid):
    def draw(x, y, w, h):
        bh = 40
        t0 = y + (h - 2 * bh - 26) / 2
        return [R('vl/a', x + 22, t0, w - 44, bh, prst='roundRect', radius=10, fill='FFFFFF', line='CFC9DB', line_w=1.0),
                T('vl/at', x + 22, t0, w - 44, bh, top, size=11, color=BODY, weight='m', align='c', anchor='ctr'),
                arrow('vl/ar', (x + w / 2, t0 + bh + 23), (x + w / 2, t0 + bh + 3), color=PURPLE2, w=1.6),
                T('vl/m', x + w / 2 + 10, t0 + bh + 3, w / 2 - 20, 20, mid, size=9.5, color=PURPLE, weight='b', anchor='ctr'),
                R('vl/b', x + 22, t0 + bh + 26, w - 44, bh, prst='roundRect', radius=10, fill=LAV, line=RING, line_w=1.4),
                T('vl/bt', x + 22, t0 + bh + 26, w - 44, bh, bottom, size=11, color=PURPLE, weight='b', align='c', anchor='ctr')]
    return draw


def s_a6():
    s = page_slide('qa_agent', 'A-6', [('AI Agent(Pickle, Muse)와의 관계', INK)])
    y, h, gap = 100, 150, 14
    qrow(s, 'qa/q1', y, h, 'Pickle이나 Muse 같은 AI Agent에게 찾아 달라고 하면 되지 않나요?',
         'Agent는 예약이나 주문처럼 **일을 대신 하는 층**이고, Weave는 그 아래에서 **내 기록을 찾아 주는 층**입니다. 지금의 Agent는 서버의 가상 컴퓨터에서 동작해서¹, '
         '기기 안의 메모와 사진, 받은 메시지를 찾으려면 서버로 올려야 합니다.',
         n=1, vis=vis_layers('AI Agent: 예약, 주문, 전화 (서버에서 실행)', 'Weave: 개인 기록 검색 (온디바이스)', '찾은 답만 전달'))
    qrow(s, 'qa/q2', y + h + gap, h, 'Agent가 직접 검색하면 무엇이 문제인가요?',
         'Agent는 추론과 검색을 여러 번 반복합니다. 공개 실험에서 이런 방식은 질의 하나에 **10~27초**가 걸렸습니다.² Weave는 기록을 미리 색인해 두고 sLLM을 두 번만 불러서 **1~2초**에 답합니다.',
         n=2, vis=vis_bars('질의 1건의 소요 시간', [('Self-Ask²', 27.47, '27.5초', False), ('Iter-RetGen²', 9.68, '9.7초', False), ('Weave (UX2)', 1.69, '0.8~1.7초', True)], vmax=34,
                           note='Self-Ask와 Iter-RetGen은 서버 실험값, Weave는 온디바이스 추정값'))
    qrow(s, 'qa/q3', y + 2 * (h + gap), h, '그러면 Agent와는 어떤 관계인가요?',
         'Weave는 **Agent가 호출하는 도구**가 됩니다. Agent가 사용자의 기억이 필요할 때 Weave에 묻고, Weave는 기기 안에서 찾은 답만 건넵니다. 기록 전체와 색인은 기기에 남습니다.',
         n=3, vis=vis_steps([('Agent', '무엇을 주문할지 질의'), ('Weave', '기기 안에서 검색'), ('Agent', '주문 실행')], on=(1,), note='예: “집들이 때 마신 와인 다시 주문해 줘”'))
    footnote(s, ['¹ Pickle은 격리된 클라우드 실행 환경에서, Meta Muse(2026. 09)는 자체 클라우드 컴퓨터에서 동작함(각 사 소개와 보도 기준).',
                 '² Zhuang et al., "EfficientRAG", EMNLP 2024: LLM이 검색을 반복하는 방식의 질의당 소요 시간(MuSiQue).'], y + 3 * h + 2 * gap + 12)
    return s


# ------------------------------------------------------------------ A-7 LLM에게 전부 읽히면
def s_a7():
    s = page_slide('qa_llm', 'A-7', [('LLM에게 기록을 전부 읽히는 방식과의 차이', INK)])
    y, h, gap = 100, 150, 14
    qrow(s, 'qa/q1', y, h, '기록을 전부 LLM에게 읽히면 되지 않나요?',
         'LLM은 토큰마다 연산하기 때문에 수만 건의 기록을 질의마다 읽기 어렵습니다. 임베딩은 기록마다 한 번만 미리 계산해 두고, 질의가 오면 벡터끼리 비교해서 **0.02초**에 후보를 고릅니다. '
         'sLLM은 질의를 다시 쓸 때와 답변을 만들 때만 씁니다.',
         n=1, vis=vis_nums([('0.02초', ['임베딩 검색 1회']), ('2회', ['질의 1건의', 'sLLM 호출'])], pt=20))
    qrow(s, 'qa/q2', y + h + gap, h, '후보 기록을 많이 넣어 주면 LLM이 그중에서 고를 수 있지 않나요?',
         '후보가 많아지면 LLM의 정확도가 크게 떨어집니다. 암시된 사실을 찾는 벤치마크에서 GPT-4.1은 정답 기록만 받으면 88점을 내지만, 헷갈리는 기록 29건과 함께 받으면 23점이 됩니다.¹ '
         '먼저 정확히 검색해야 하는 이유입니다.',
         n=2, vis=vis_bars('GPT-4.1의 정답률¹', [('정답 기록만 제공', 88.05, '88.1', True), ('헷갈리는 기록 29건과 함께', 22.9, '22.9', False)], vmax=110))
    qrow(s, 'qa/q3', y + 2 * (h + gap), h, '임베딩 검색이 놓치면 LLM도 볼 수 없지 않나요?',
         '그래서 후보를 여러 건 가져오고 키워드 검색(BM25)도 함께 씁니다. 날짜와 사람 같은 메타데이터로 한 번 더 필터링하고, 그래도 근거가 없으면 찾지 못했다고 답합니다.',
         n=3, vis=vis_steps([('두 가지 검색', '임베딩 + BM25'), ('필터링', '날짜, 사람'), ('답변', '근거와 함께')], on=(2,)))
    footnote(s, '¹ Taghavi et al., "ImpliRet: Benchmarking the Implicit Fact Retrieval Challenge", arXiv:2506.14407. 정답 문서만 줄 때 88.05, 문서 30건(정답 1 + 헷갈리는 문서 29)을 줄 때 22.90.',
             y + 3 * h + 2 * gap + 12)
    return s


# ------------------------------------------------------------------ A-8 Apple과 Google
A8 = [[['Apple Siri AI', '(2026. 09)'], '메시지, 메일, 미리 알림을 이어서 답변¹', '기기 + 서버 (Private Cloud Compute)', 'Apple 기본 앱'],
      [['Gemini Personal Intelligence', '(2026. 01)'], 'Gmail, Google 포토의 기록을 이어서 답변²', '서버 (Google 계정의 데이터)', 'Google 서비스'],
      [['Pixel Magic Cue', '(2025. 08)'], 'Gmail, 캘린더, 스크린샷을 이어서 먼저 제안³', '기기 (Gemini Nano)', 'Google 앱. 한국 미제공'],
      [('Weave', HI), ('여러 앱의 기록을 단서로 이어서 답변하고 먼저 제안', HI), ('전부 기기 안에서 처리', HI), ('삼성 기본 앱과, 알림으로 받는 외부 메신저', HI)]]


def s_a8():
    s = page_slide('qa_apple', 'A-8', [('Apple, Google의 개인 기록 검색과의 차이', INK)])
    y = 100
    y += tbl(s, 'qa/t', X, y, W, [25, 30, 23, 22], ['서비스', '하는 일', '처리 위치', '대상'], A8, hi=(3,), pady=10) + 26
    y += notes3(s, 'qa/n', y, [('같은 방향이라는 신호', 'Apple과 Google이 모두 개인 기록을 이어 답하는 기능을 내놓았습니다. 개인 기록 검색이 스마트폰 AI의 **다음 경쟁 축**이라는 신호입니다.'),
                               ('키보드에서 바로', '음성 비서를 따로 부르지 않습니다. 검색창, 통화 화면, 메신저 어디서든 **키보드의 버튼 하나**로 동작합니다.'),
                               ('Galaxy 생태계와 결합', '삼성 기본 앱과 월렛, 위치 신호, Personal Data Engine, SmartThings로 이어집니다. ‘기기에서만 처리’ 설정에서도 그대로 동작합니다.')]) + 20
    footnote(s, ['¹ Apple Newsroom, Siri AI 발표 (2026. 09. 14, 한국어는 10. 26): "These latest models run on device and on servers using Private Cloud Compute"',
                 '² Google, Personal Intelligence 발표 (2026. 01)   ³ Google, Pixel 10 발표 (2025. 08). 제공 국가는 Google 지원 페이지 기준.'], y)
    return s


# ------------------------------------------------------------------ 물음과 답
PAGES = [
    Page('A-1', '기존 기능과 한눈에 비교', s_a1, clicks=1,
         q='기존 Galaxy AI 기능이나 다른 서비스와는 무엇이 다른가요?',
         a='Writing Assist는 지금 쓰는 글을 다듬고, 카나나는 카카오톡 내에서 대화 요약과 맞춤형 제안을 제공합니다. '
           'Now Nudge와 Finder 역시 지금 화면에 맞춰 제안하거나 한 번 탐색하는 데 그칩니다. '
           '(클릭) Weave는 여러 앱에 흩어진 단서를 찾을 뿐 아니라, 이들을 연결함으로써 사용자가 정말 원하는 답이 무엇인지 찾아줍니다.',
         more=[('가로와 세로는 무엇인가요?', '가로는 찾는 범위입니다. 한 앱 안인지, 여러 앱인지입니다. 세로는 찾는 깊이입니다. 한 번 찾고 끝나는지, 찾은 단서로 다시 찾는지입니다.'),
               ('왜 꼭 키보드인가요?',
                '기록을 찾는 순간은 대부분 무언가를 입력하는 순간입니다. 검색창이든 메신저든 메일이든 키보드는 떠 있어서, 앱을 옮기지 않고 그 자리에서 찾아 넣을 수 있습니다. 통화 중이나 조용한 곳에서는 음성 비서를 부르기 어렵습니다.')],
         basis=['대본은 8차에 발표자가 쓴 글 그대로(slides_new.NOTES의 cmp).']),
    Page('A-2', '기능별 비교', s_a2,
         q='하나씩 짚어 주시겠어요? 키워드 검색이나 임베딩 검색과는 무엇이 다른가요?',
         a='기존 기능은 한 앱이나 지금 화면 안에서 한 번 찾는 데 그치고, Weave는 여러 앱의 기록을 단서로 이어서 찾습니다. '
           'Finder는 기기 안의 앱과 일정, 노트, 파일을 찾아 목록으로 보여 주고, Now Nudge는 지금 화면의 대화에 맞춰 제안합니다. '
           'Writing Assist는 쓴 글을 다듬고, Kanana는 카카오톡 안의 대화를 읽습니다. '
           '검색 방식으로 보면 키워드 검색은 같은 단어가 있는 기록을, 일반 임베딩은 의미가 비슷한 기록을 한 번에 찾습니다. '
           'Weave는 여기에 추론 단서까지 찾는 Reasoning Embedding과, 찾은 단서로 다시 찾게 하는 Query Rewriter를 더했습니다.',
         more=[('Now Nudge도 사진을 찾아 주던데요?', '맞습니다. Now Nudge는 대화에 나온 말로 갤러리를 한 번 찾습니다. Weave는 화면에 없는 다른 앱의 기록을 단서로 삼아 한 번 더 찾습니다.')],
         basis=['Finder: Samsung 지원 "Understanding Finder on Galaxy phones". 자연어 검색의 공식 대상은 Voice Recorder, Recorded Calls, Calendar, Notes, Reminders, My Files.',
                'Now Nudge: Samsung Newsroom의 Galaxy S26 발표문 "If a friend asks for photos from a recent trip, Galaxy S26 automatically suggests photos from the Gallery".',
                'Kanana in KakaoTalk: 카카오 보도자료(2025. 09. 23), 기기 안 모델(Kanana Nano).',
                'Apple Siri AI: Apple Newsroom(2026. 09. 14).']),
    Page('A-3', 'Finder와의 차이', None, foreign=(FINDER_SRC, 1, patch_finder),
         q='Finder도 의미 검색을 하는데, Finder를 조금 고치면 되는 것 아닌가요?',
         a='Finder는 찾은 기록을 목록으로 보여 주는 검색창이고, Weave는 단서를 이어 답을 만들어 쓰던 자리에 넣어 주는 기능입니다. '
           'Finder도 임베딩으로 의미 검색을 합니다. 하지만 검색어 의도 분류가 되지 않아 결과가 일정하지 않습니다. '
           '‘주문’이라고 검색하면 배달의민족과 요기요가 나오지만, ‘음식 주문’이나 ‘배고파’라고 검색하면 나오지 않습니다.',
         more=[('Finder에 검색어 의도 분류가 들어가면 Weave 아닌가요?',
                '의도 분류가 들어와도 충분하지 않습니다. 말에 숨은 단서를 알아보는 Reasoning Embedding과, 여러 단서를 연달아 찾게 해 주는 Query Rewriting이 함께 있어야 합니다.'),
               ('Finder에 멀티홉 기능만 붙이면 되는 거 아닌가요?',
                '멀티홉 기능만 붙이면 연쇄 탐색 한 칸만 생깁니다. 상황 인식, 질의 재작성, 연쇄 탐색이 한 파이프라인으로 돌아야 완성도 높은 결과가 나옵니다.')],
         basis=['장과 대본은 팀원(SB-Jo)의 `Appendix_Finder와의_차별점_QA.pptx` 그대로. 검색 예시는 Galaxy 기기의 Finder에서 직접 검색한 결과(그 장의 각주).',
                '덧붙인 것: 공식 검색 대상 각주, ‘Appendix 참조’ 두 곳을 코드(D-2, D-5와 C-1)로.']),
    Page('A-4', 'Personal Data Engine과의 차이', s_a4,
         q='삼성에는 이미 Personal Data Engine, 개인 지식 그래프가 있습니다. 그걸로 되는 것 아닌가요?',
         a='두 기술은 추론하는 시점이 다릅니다. Personal Data Engine은 기록이 들어올 때 분석해서 사람과 일정, 장소 같은 사실을 그래프에 쌓아 두고, '
           'Weave는 질의가 들어올 때 그 질의에 맞춰 원문에서 단서를 찾습니다. 정리된 사실은 그래프가 빠르고 정확합니다. '
           '다만 와인 예시의 첫 단서인 지은이의 카카오톡에는 ‘집들이’라는 단어도, 캘린더 일정도 없어서 받는 순간에 집들이로 정리해 두기 어렵습니다. '
           'Weave는 이렇게 그래프에 아직 없는 단서를 채우는 역할을 합니다.',
         more=[('와인 예시에서는 누가 무엇을 하나요?', '첫 번째 검색인 집들이 날짜는 Weave가 맡습니다. 두 번째 검색인 그날 찍은 사진은 날짜 조건이어서 그래프로도 찾을 수 있습니다.'),
               ('모든 대화를 미리 그래프로 만들어 두면 되지 않나요?',
                '나중에 무엇을 물을지 모르는 상태에서 매일 쌓이는 메시지를 모두 미리 해석해 두려면 연산 부담이 큽니다. '
                '그래프 기반 검색을 분석한 연구에서도 오류 100건 가운데 76건이 정보를 미리 추출하는 단계에서 나왔습니다.'),
               ('그러면 그래프는 필요 없다는 말인가요?', '아닙니다. 날짜와 사람, 장소처럼 정리된 사실은 그래프가 가장 빠르고 정확합니다. 다음 장처럼 함께 쓸 때 가장 좋습니다.')],
         basis=['Crocker, Horrocks, Nenov, "Semantic Technology in Your Pocket", ISWC 2025 Industry Track (CEUR-WS Vol-4085): "The PDE analyses this data using appropriate AI technologies including machine learning and LLMs. The result of this analysis is stored in the user\'s personal knowledge graph where it is augmented with triples entailed by the ontology."',
                'Gutiérrez et al., "HippoRAG", NeurIPS 2024, 부록 F: MuSiQue 오류 100건 가운데 질의 개체 추출 48건 + 문서 정보 추출 28건 = 76건.',
                '삼성 PDE 자료에는 ‘knowledge graph’라는 말이 없고, 지식 그래프 기반이라는 근거는 OST(자회사)의 글과 발표. 그래서 "삼성이 지식 그래프라고 발표했다"고는 말하지 않음.']),
    Page('A-5', 'PDE와 함께 쓰는 방법', s_a5,
         q='그럼 Personal Data Engine과 Weave를 어떻게 같이 쓰나요?',
         a='두 기술은 서로 보완하는 관계입니다. 그래프가 아는 사람과 일정, 장소로 검색 범위를 좁히면 Weave의 정확도가 오릅니다. '
           '반대로 Weave가 찾아내고 사용자가 확인한 연결을 그래프에 올리면, 다음에는 그래프에서 바로 답할 수 있습니다. '
           '지금은 날짜와 앱 같은 메타데이터로 필터링하는 것부터 시작하고, 이후에 PDE와 직접 연결하는 순서로 넓힐 수 있습니다.',
         more=[('Weave가 틀린 연결을 그래프에 올리면요?', '사용자가 확인한 연결만 올립니다. Weave가 찾기만 한 것은 후보로 두고, 사용자가 그 답을 실제로 썼을 때만 사실로 올립니다.'),
               ('PDE 팀이 하는 일에 얹자는 건가요, 새로 만들자는 건가요?',
                '얹는 제안입니다. 기록을 모으고 지키는 구조는 PDE와 KEEP 위에서 그대로 쓰고, Weave는 그 위에 검색 계층을 더합니다.')],
         basis=['Han et al., "RAG vs. GraphRAG: A Systematic Evaluation and Key Insights", arXiv:2502.11371: 두 방식은 과제마다 강점이 다르고 함께 쓰면 성능이 오름.',
                'ISWC 2025 논문의 Future Vision: "a holistic and deeply personalised user experience not only across multiple apps but also across a wide range of different devices".',
                '그래프에 올리는 연결의 예: ‘3월 15일 = 지은이네 집들이’(사용자가 추천을 실제로 입력했을 때).']),
    Page('A-6', 'AI Agent (Pickle, Muse)', s_a6,
         q='요즘은 Pickle이나 Muse 같은 에이전트가 있습니다. 에이전트에게 찾아 달라고 하면 되지 않나요?',
         a='에이전트는 예약이나 주문처럼 일을 대신 해 주는 층이고, Weave는 그 아래에서 내 기록을 찾아 주는 층입니다. '
           '지금의 에이전트는 서버에서 동작하기 때문에, 기기 안의 메모와 사진, 받은 메시지를 찾으려면 서버로 올려야 합니다. '
           '또 추론과 검색을 여러 번 반복해서, 공개 실험에서는 질의 하나에 10초에서 27초가 걸렸습니다. '
           'Weave는 기기 안에서 미리 색인해 두고 1초에서 2초 사이에 답합니다. '
           '그래서 에이전트가 사용자의 기억이 필요할 때 호출하는 도구로 함께 쓸 수 있습니다.',
         more=[('에이전트가 Weave를 부르면 결국 기록이 서버로 가는 것 아닌가요?', '에이전트에게 가는 것은 찾아낸 답 한 줄입니다. 기록 전체와 색인은 기기 안에 남고, 무엇을 건넬지는 사용자가 정합니다.'),
               ('Bixby가 에이전트가 되면 Weave는 필요 없지 않나요?', 'Bixby가 일을 대신 하게 될수록 내 기록을 정확히 찾아 주는 검색이 더 필요합니다. Weave는 그 검색을 맡습니다.')],
         basis=['Zhuang et al., "EfficientRAG", EMNLP 2024: MuSiQue 200문항에서 질문당 Iter-RetGen 9.68초, SelfAsk 27.47초, EfficientRAG 3.62초.',
                'Pickle(Pickle, Inc.): 전화, 예약, 쇼핑을 대신 하는 개인 AI 에이전트 앱. 격리된 클라우드 실행 환경과 가상 브라우저에서 일하고, 연결한 계정(캘린더, 메일, 쇼핑)을 씀(소개 글 기준).',
                'Meta Muse: 2026. 09. 08 발표. 자체 클라우드 컴퓨터(격리된 가상 머신과 브라우저)에서 일하고 기억 기능이 있음(보도 기준).',
                'Weave의 0.8~1.7초는 UX2의 온디바이스 추정값(B-5).']),
    Page('A-7', 'LLM에게 전부 읽히면', s_a7,
         q='요즘 LLM은 긴 글도 읽습니다. 기록을 전부 LLM에게 읽히면 되지 않나요?',
         a='기록이 수만 건이면 질의마다 전부 읽히기에는 연산량이 너무 큽니다. 그래서 찾는 일은 임베딩에 맡겼습니다. '
           '기록의 벡터는 충전 중에 미리 만들어 두기 때문에, 질의가 들어왔을 때는 벡터끼리 비교만 하면 되고 0.02초면 끝납니다. '
           'sLLM은 질의를 다시 쓸 때와, 추려진 기록 몇 건으로 답변을 만들 때만 씁니다. '
           '후보를 많이 넣어 주는 것도 답이 아닙니다. 공개 벤치마크에서 헷갈리는 기록이 섞이면 GPT-4.1의 점수가 88점에서 23점으로 떨어졌습니다.',
         more=[('임베딩이 놓치면 LLM도 못 보는 것 아닌가요?', '그래서 후보를 여러 건 가져오고 키워드 검색도 함께 씁니다. 그래도 근거가 없으면 찾지 못했다고 답합니다.')],
         basis=['ImpliRet(arXiv 2506.14407): 정답 문서만 줄 때와 30건을 줄 때 GPT-4.1 88.05 → 22.90, o4-mini 92.74 → 55.54, Llama 3.3 70B 81.92 → 10.71.',
                'Hop 하나 0.02초 = 임베딩 8ms + 벡터 검색 10ms + 필터링과 Slot 2ms(B-5).',
                'How it Works Appendix에 있던 장(q_llm)의 답을 질문과 답 줄로 다시 짬.']),
    Page('A-8', 'Apple, Google과의 차이', s_a8,
         q='Apple의 Siri AI나 Google의 Gemini도 개인 기록을 찾아 주지 않나요?',
         a='맞습니다. Apple은 올해 9월 Siri AI에서 메시지와 메일, 미리 알림을 이어 답하는 예시를 보여 줬고, Gemini의 Personal Intelligence도 Gmail과 Google 포토를 이어 답합니다. '
           '저희는 이것을 개인 기록 검색이 스마트폰 AI의 다음 경쟁 축이라는 신호로 봅니다. Weave의 차이는 세 가지입니다. '
           '서버를 함께 쓰는 두 서비스와 달리 모든 처리를 기기 안에서 하고, 음성 비서를 부르지 않고 키보드에서 바로 쓰며, '
           '삼성 기본 앱과 PDE, SmartThings로 이어지는 Galaxy 생태계 위에서 동작합니다.',
         more=[('Apple이 먼저 한 것 아닌가요?', '방향은 같습니다. 그래서 Galaxy에도 필요하다고 봅니다. 저희는 기기 안 처리와 키보드라는 자리로 차별화합니다.'),
               ('Pixel의 Magic Cue는요?',
                'Gmail과 캘린더, 스크린샷을 이어 먼저 제안하는 기능으로 방향이 같습니다. 다만 Google 앱이 중심이고 한국에는 제공되지 않습니다.')],
         basis=['Apple Newsroom(2026. 09. 14): "if a user asks Siri what a family member suggested as an activity during an upcoming visit, Siri can search the user\'s messages … pull up the cooking instructions from an email … add the ingredients to their grocery list in the Reminders app". "These latest models run on device and on servers using Private Cloud Compute." 한국어는 2026. 10. 26.',
                'Google(2026. 01. 14): "Personal Intelligence has two core strengths: reasoning across complex sources and retrieving specific details from, say, an email or photo". "this data already lives at Google".',
                'Pixel Magic Cue(2025. 08. 20): Gmail, 캘린더, 스크린샷, 메시지를 이어 먼저 제안. Google의 소개 글은 Tensor G5와 Gemini Nano로 기기에서 돈다고 설명(11-16 검색으로 확인). 제공 국가 9곳에 한국은 없음(Google 지원 페이지).']),
]
