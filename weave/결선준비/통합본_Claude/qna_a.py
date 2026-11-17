"""Appendix A 묶음: 기존 기술과의 차이 (11-16 3판, 저녁에 11차로 고침).

A-1 비교 지도(cmp_new 그대로), A-2 기능별 비교(표 하나), A-3 Finder(팀원 SB-Jo의 장을 옮겨 옴), A-4 Personal Data Engine(Knowledge Graph)과의 차이(두 줄 흐름 그림),
A-5 PDE와 함께 쓰는 방법(주고받는 그림 + 세 단계), A-6 AI Agent(Pickle, Muse)와의 관계, A-7 Apple과 Google의 개인 기록 검색, A-8 Galaxy AI 안에서의 구성.
11차(팀 검토): 10차의 A-7(LLM에게 전부 읽히는 방식과의 차이)은 Q1만 속도 1 장(D-3)으로 옮기고 뺌. Apple과 Google 장(10차 A-8 → A-7)은 기능마다 무엇을 하는지를
더 자세히 적고 쓰는 자리(진입점)를 보탬. A-3의 Q2는 Query Rewriting을 Reasoning Embedding 앞으로. 새 장 A-8(Galaxy AI에 들어간다면 어떤 구성인지).
13차 뒤(11-17, 사용자의 지시. 그날 저녁에 Q2와 자리를 바꿔 지금은 Q2): A-3의 Q3('멀티홉 기능만 붙이면')을 현재 Finder 사용 통계(앱 검색 67%, 다른 용도로 한 번 이상 55% 이하)로 바꿈. 뺀 질문은 대본의 '더 물으면'에 남음.
3판: 문장 제목과 부제를 버리고, A-6과 A-7은 질문과 답 세 줄 + 작은 그림(A-3과 같은 짜임), A-4와 A-5는 그림 + 짧은 설명, A-2와 A-8은 표 하나.
(11-15: '가전과 TV에서는 이미 하고 있지 않나요?' 장은 만들었다가 필요 없다는 검토를 받아 뺌.)
숫자와 출처는 `Appendix_QnA_대본.md`의 근거에 있다.
"""
import copy
import json
from pathlib import Path

from ui import (BODY, INK, LAV, LAV2, MUTE, PURPLE, PURPLE2, RING, SUB, R, T)

import qna_num as NUM
from qna_lib import (GRAY_BG, Page, Slide, arrow, box, footnote, frame, label, lh_of, notes3, page_slide, pipeline, points, qrow, rwrap, step, tbl, vis_bars, vis_nums,
                     vis_steps, vis_xo)

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
A2_S = [['키워드 검색 (BM25)', '같은 단어가 있는 기록을 검색', '‘집들이’라는 단어가 없는 초대 메시지도 검색 (D-8)'],
        ['일반 임베딩 검색', '의미가 비슷한 기록을 한 번에 검색', 'Reasoning Embedding으로 추론 단서를 찾고, Query Rewriter로 연쇄 탐색']]


def s_a2():
    s = page_slide('qa_tbl', 'A-2', [('기존 기능, 검색 방식과의 비교', INK)])
    y = 98
    y += label(s, 'qa/l1', X, y, 'Galaxy AI와 다른 서비스 (Apple과 Google은 A-7)') + 4
    y += tbl(s, 'qa/t', X, y, W, [19, 39, 42], ['기능', '하는 일', 'Weave가 다른 점'], A2, pady=10) + 22
    y += label(s, 'qa/l2', X, y, '검색 방식') + 4
    y += tbl(s, 'qa/t2', X, y, W, [19, 39, 42], ['방식', '하는 일', 'Weave가 다른 점'], A2_S, pady=10) + 12
    footnote(s, ['¹ Samsung 지원, "Understanding Finder on Galaxy phones" (One UI 8.5부터 자연어 검색)   ² Samsung Newsroom, Galaxy S26 발표 (2026. 02)   ³ Samsung 지원, Writing Assist   '
                 '⁴ 카카오 보도자료 (2025. 09. 23)'], y)
    return s


# ------------------------------------------------------------------ A-3 Finder (옮겨 온 장을 손봄)
FINDER_FOOT = ('Finder 자연어 검색의 공식 대상은 음성 녹음, 통화 녹음, 캘린더, 노트, 리마인더, 내 파일입니다 '
               '(Samsung 지원, "Understanding Finder on Galaxy phones").')
# Q3(11-17, 사용자의 지시): '현재 finder 사용 통계를 보면 ~~가 67%고, -이하만 다른 용도로 사용한다 … 기존 덱 질문 페이지에서 중요하지 않은 거 하나 지우거나 하나 추가'.
# 비율은 사내 Finder 사용 통계의 세 지표로 셈함(모두 Finder 전체 사용 대비): 앱 검색 = 67%, 다른 용도로 한 번 이상 사용 = 55%.
# 사용자의 설명(11-17): '28/51만 다른 용도로 한 번 이상 사용했다는 건데'. 두 지표는 한 사용자가 양쪽에 모두 셈될 수 있어(사용자: '중복 통계도 있는 듯') '이하'로 적음.
# 처음에는 둘째 숫자를 전체에서 앱 검색을 뺀 33%로 잘못 적었다가 고침. 원래 값과 지표의 이름은 저장소에 올리지 않는 `원본/사내자료.json`에만 둔다(있으면 아래에서 비율을 확인).
FU_APP, FU_ETC = 67, 55
# Q2의 셋째 줄(11-17). 처음에는 '통화 화면과 키보드에서 바로 씁니다'로 적었고, 사용자의 말('통화 화면 → 다른 앱 사용 중에서도 진입 가능하며, 키보드 위에서')로 고침
# 둘을 한데 섞어 적었다가 다시 고침('UX1은 다른 앱 사용 중에도 가능한 거고 키보드는 따로잖아. 두 개 다 간단하게 묶는 그런 문장'): 진입점은 둘
FINDER_UX = ['진입점도 다릅니다. Weave는 ', '다른 앱 사용 중에도, 키보드 위에서도 바로', ' 진입합니다. ', '(A-8)']
FU_Q = '현재 Finder는 주로 어떤 용도로 쓰이나요?'
FU_A = '현재 Finder 사용 통계를 보면 앱 검색이 %d%%이고, %d%% 이하만 다른 용도로 한 번 이상 사용했습니다.' % (FU_APP, FU_ETC)
FU_NOTE = '넓은 범위를 검색할 수 있지만 앱 검색 말고는 잘 쓰이지 않습니다.'
FU_CAP = 'Weave는 기록을 찾는 쓰임을 넓힙니다'
FU_FOOT = ('   A2의 비율은 사내 Finder 사용 통계에서 셈한 값입니다(Finder 전체 사용 대비. 한 사용자가 양쪽에 모두 셈될 수 있습니다).')
# 11-17 저녁(사용자의 지시): ① Q2와 Q3의 자리를 바꿈(사용 통계가 Q2, 의도 분류가 Q3. 그래서 각주도 A3 → A2)
# ② Q1의 답 'Finder도 임베딩 검색을 지원하지만, 검색어 의도 분류가 되지 않아 / 검색 결과가 일정하지 않습니다.'를 아래 두 줄로.
#    첫 줄은 사용자의 글 그대로. 둘째 줄은 사용자의 초안('Q2(바뀐 Q2)에 따라서 Weave를 통해 고도화하면 좋을것이다?')을 내가 다듬은 문장이고 끝의 (Q2)가 사용 통계를 가리킴
# ③ Q3의 '단서 추론을 위한' → '더 깊이 있는 단서 추론을 위한'(사용자의 글 '깊이있는'의 띄어쓰기만 고침).
#    그 줄에 '(D-5, D-8)'을 둘 자리가 없어져(답 상자는 줄이 넘어가지 않음) 오른쪽 그림의 'Weave가 더하는 두 가지' 옆으로 옮김
FINDER_A1 = ['Finder도 임베딩 검색을 지원하지만, 사용 맥락을 충분히 반영하지는 못하고 있습니다.',
             'Weave를 통해 고도화하면 더 다양한 용도로 쓰일 수 있습니다. ', '(Q2)']
FINDER_DEEP = '과, 더 깊이 있는 단서 추론을 위한 '
FINDER_REF = '  (D-5, D-8)'              # 굵은 글 뒤라 빈칸 하나로는 붙어 보여 둘을 둠
FINDER_DY = 175.7                      # 카드와 카드 사이(둘째 312.0, 셋째 487.7)
_fu = HERE / '원본' / '사내자료.json'
if _fu.exists():
    _u = json.loads(_fu.read_text(encoding='utf-8'))['finder_usage']
    assert round(_u['app'] / _u['all'] * 100) == FU_APP and round(_u['etc'] / _u['all'] * 100) == FU_ETC, '사내 자료의 값과 장의 비율이 다름'


def patch_finder(slide):
    """옮겨 온 Finder 장: 멀티홉 질문을 Finder 사용 통계로 바꿔 Q2에 두고(의도 분류가 Q3), Q1의 답과 참조를 고친다. 돌려줌: 틀 위에 더 그릴 Slide."""
    from qna_lib import A_NS, P_NS as PN, live_tree
    tree = live_tree(slide)
    by_id = {}
    for el in tree:
        c = el.find('.//{%s}cNvPr' % PN)
        if c is not None:
            by_id[c.get('id')] = el
    # 팀원 덱의 Q3(도형 번호는 팀원 덱의 것. 아래에서 둘째 카드로 옮김): 질문 22, 답 24(문단 셋: 12.5pt 두 줄 + 11.5pt 회색 한 줄), 오른쪽 그림 62 ~ 75
    qt = list(by_id['22'].iter('{%s}t' % A_NS))
    assert [t.text for t in qt] == ['Finder에 멀티홉 기능만 붙이면 되는 거 아닌가요?'], [t.text for t in qt]
    qt[0].text = FU_Q
    paras = list(by_id['24'].iter('{%s}p' % A_NS))
    runs = [list(pp.findall('{%s}r' % A_NS)) for pp in paras]
    assert [len(r) for r in runs] == [3, 1, 1], [len(r) for r in runs]

    def settext(run, text):
        run.find('{%s}t' % A_NS).text = text
    head, tail = FU_A.split('앱 검색이 %d%%' % FU_APP)
    tail1, tail2 = tail.split('%d%% 이하' % FU_ETC)
    settext(runs[0][0], head)                                  # '현재 Finder 사용 통계를 보면 '
    settext(runs[0][1], '앱 검색이 %d%%' % FU_APP)            # 보라, 굵게
    settext(runs[0][2], tail1.rstrip())                        # '이고,'
    hi = copy.deepcopy(runs[0][1])
    settext(hi, '%d%% 이하' % FU_ETC)
    paras[1].insert(list(paras[1]).index(runs[1][0]), hi)
    settext(runs[1][0], tail2)                                 # '만 다른 용도로 한 번 이상 사용했습니다.'
    settext(runs[2][0], FU_NOTE)
    for i in range(62, 76):                                    # 멀티홉 그림(파이프라인 세 칸과 빨간 테두리, 아래 한 줄)
        tree.remove(by_id[str(i)])
    foot = [t for t in tree.iter('{%s}t' % A_NS) if t.text and t.text.startswith('* A1의 검색 예시는')]
    assert len(foot) == 1, len(foot)
    foot[0].text += FU_FOOT
    n = 0
    for t in tree.iter('{%s}t' % A_NS):
        if t.text and '(자세한 설명은 Appendix 참조)' in t.text:
            t.text = t.text.replace('(자세한 설명은 Appendix 참조)', '(자세한 설명은 D-5, D-8)')
            n += 1
    assert n == 1, 'Finder 장의 글이 바뀜: Appendix 참조 %d곳' % n
    # 11차(11-16) 'q2 query rewriting이랑 reasoning embedding 순서 바꾸기': 파이프라인의 차례(02 질의 재작성 → 03 연쇄 탐색)대로 Query Rewriting을 앞에.
    # 답의 글 토막 셋을 바꾸고, 오른쪽 그림의 두 칸(Reasoning Embedding 144px, Query Rewriting 119px)과 그 사이의 +를 자리만 맞바꾼다
    swaps = [('검색어 의도 분류만으로는 충분하지 않습니다. 단서 추론을 위한', '검색어 의도 분류만으로는 충분하지 않습니다. 여러 단서를 연달아 찾기 위한'),
             ('과, 여러 단서를 연달아 찾기 위한', '과, 단서 추론을 위한')]
    done = 0
    for t in live_tree(slide).iter('{%s}t' % A_NS):
        for old, new in swaps:
            if t.text == old:
                t.text = new
                done += 1
    assert done == 2, done
    names = [t for t in live_tree(slide).iter('{%s}t' % A_NS) if t.text in ('Reasoning Embedding', 'Query Rewriting')]
    in_answer = [t for t in names if int(t.getparent().find('{%s}rPr' % A_NS).get('sz')) == 1250]      # 답 안의 보라 낱말 둘(12.5pt). 그림 속 이름은 10pt
    assert [t.text for t in in_answer] == ['Reasoning Embedding', 'Query Rewriting'], [t.text for t in in_answer]
    in_answer[0].text, in_answer[1].text = 'Query Rewriting', 'Reasoning Embedding'
    # 11-17 'Q2에 UX 진입점도 답에 조금 넣으면 좋을 것 같아. 공간 충분하니 한 줄 정도': 답(도형 19)은 세 줄이 들어가는 높이라 줄을 더 놓을 수 없음.
    # 짧던 둘째, 셋째 줄을 한 줄로 모으고(그래서 '(자세한 설명은 D-5, D-8)'을 '(D-5, D-8)'로 줄임) 셋째 줄에 진입점을 적는다
    p1, p2 = list(by_id['19'].iter('{%s}p' % A_NS))[1:]
    r1, r2 = list(p1.findall('{%s}r' % A_NS)), list(p2.findall('{%s}r' % A_NS))
    got = [r.find('{%s}t' % A_NS).text for r in r1 + r2]
    assert got == ['Query Rewriting', '과, 단서 추론을 위한', 'Reasoning Embedding', '이 필요합니다. ', '(자세한 설명은 D-5, D-8)'], got
    settext(r1[1], FINDER_DEEP)
    line3 = [copy.deepcopy(r1[1]), copy.deepcopy(r1[0]), copy.deepcopy(r1[1]), copy.deepcopy(r2[2])]      # 검정, 보라 굵게, 검정, 회색 작은 글
    small = copy.deepcopy(r2[2])                                # 회색 작은 글(11.5pt): Q1의 (Q2)에 씀
    for r in r2[:2]:
        p1.append(r)
    settext(r2[1], '이 필요합니다.')
    p2.remove(r2[2])                                            # '(자세한 설명은 …)'은 이 줄에서 빼고 아래에서 그림의 글 옆에 적음
    for r, text in zip(line3, FINDER_UX):
        settext(r, text)
        p2.append(r)
    cap = by_id['61'].find('.//{%s}r' % A_NS)                   # 그림 아래의 보라 글 'Weave가 더하는 두 가지'(9pt)
    assert cap.find('{%s}t' % A_NS).text == 'Weave가 더하는 두 가지', cap.find('{%s}t' % A_NS).text
    ref = copy.deepcopy(small)                                  # 답 안의 참조와 같은 회색 보통 굵기로, 크기만 그림의 글(9pt)에 맞춤
    ref.find('{%s}rPr' % A_NS).set('sz', '900')
    settext(ref, FINDER_REF)
    cap.addnext(ref)
    # Q1의 답(도형 14: 12.5pt 두 줄 + 11.5pt 회색 한 줄)
    a1 = [pp.find('{%s}r' % A_NS) for pp in by_id['14'].iter('{%s}p' % A_NS)]
    got = [r.find('{%s}t' % A_NS).text for r in a1]
    assert got == ['Finder도 임베딩 검색을 지원하지만, 검색어 의도 분류가 되지 않아', '검색 결과가 일정하지 않습니다.', '같은 뜻이라도 어떤 말로 검색하느냐에 따라 결과가 달라집니다.'], got
    settext(a1[0], FINDER_A1[0])
    settext(a1[1], FINDER_A1[1])
    settext(small, FINDER_A1[2])
    a1[1].addnext(small)
    from make import box as box_of, place
    P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    sps = {sp.find('.//{%s}cNvPr' % P_NS).get('id'): sp for sp in live_tree(slide).iter('{%s}sp' % P_NS)}
    re_box, plus, qr_box = [sps[i] for i in ('52', '53', '54')], sps['55'], [sps[i] for i in ('56', '57', '58')]      # 도형 번호는 팀원 덱의 것(원본/…SB-Jo.pptx)
    x0, w_re, w_plus, w_qr = box_of(re_box[0])[0], box_of(re_box[0])[2], box_of(plus)[2], box_of(qr_box[0])[2]
    assert abs(x0 - 898.6) < 1 and abs(w_re - 144.0) < 1 and abs(w_qr - 119.0) < 1, (x0, w_re, w_qr)
    for sp in qr_box:
        place(sp, x=x0)
    place(plus, x=x0 + w_qr)
    for sp in re_box:
        place(sp, x=x0 + w_qr + w_plus)
    # Q2와 Q3의 자리 바꾸기: 카드, 'Q2.'와 'Q3.', 'A.', 그림의 바탕은 두고 내용(질문, 답, 그림)만 위아래로 옮긴다
    from make import shift
    for i in ['17', '19'] + [str(k) for k in range(48, 62)]:      # 의도 분류의 질문과 답, 그림 → 셋째 카드
        shift(by_id[i], dy=FINDER_DY)
    for i in ('22', '24'):                                        # 사용 통계의 질문과 답 → 둘째 카드
        shift(by_id[i], dy=-FINDER_DY)
    s = Slide('qa_finder', trans=('fade', 400), bar=False, notes='')
    frame(s, 'A-3')
    s.add('qa/ffoot', [T('qa/ffoot', 50, 678, 1180, 18, FINDER_FOOT, size=8.5, color='8E88A0')])   # 옮겨 온 장의 각주(x=50)에 맞춤
    # 사용 통계(Q2)의 그림: 그 장의 오른쪽 칸(763.2, 326.4, 424.3 × 130.6. 11-17 저녁까지는 셋째 카드의 502.1) 안에 막대 두 줄(둘 다 Finder 전체 사용 대비라 겹침. 한 줄로 나누지 않음).
    # 글씨는 그 장의 다른 그림과 같게(9pt 이름, 보라 굵은 한 줄). 사용자가 가장 중요하다고 한 쪽(다른 용도)을 보라로, 앱 검색은 옅은 색으로
    px, py, pw = 763.2, 502.1 - FINDER_DY, 424.3
    lx, lw_ = px + 20, 136
    bx = lx + lw_ + 4
    bw = 158
    vx = bx + bw + 10
    rows_ = [(py + 19, '앱 검색', dict(color=SUB), FU_APP, 'C9C0E6', '%d%%' % FU_APP, INK),
             (py + 55, '다른 용도 (한 번 이상)', dict(color=PURPLE, weight='b'), FU_ETC, PURPLE, '%d%% 이하' % FU_ETC, PURPLE)]
    out = []
    for k, (ry, name, st, pct, col, val, vcol) in enumerate(rows_):
        out += [T('qa/fu/l%d' % k, lx, ry, lw_, 26, name, size=10, anchor='ctr', **st),
                R('qa/fu/t%d' % k, bx, ry + 3, bw, 20, prst='roundRect', radius=10, fill='FFFFFF', line='DDD6F3', line_w=1),
                R('qa/fu/f%d' % k, bx, ry + 3, bw * pct / 100, 20, prst='roundRect', radius=10, fill=col, line=None),
                T('qa/fu/v%d' % k, vx, ry, px + pw - 10 - vx, 26, val, size=12.5, color=vcol, weight='b', anchor='ctr')]
    out.append(T('qa/fu/cap', px, py + 98.9, pw, 19.2, FU_CAP, size=9, color=PURPLE, weight='b', align='c', anchor='ctr'))
    s.add('qa/fu', out)
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
def vis_layers(top, bottom, mid):      # 13차까지 Q1 옆에 쓰던 두 층 그림(14차부터 쓰지 않음)
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


# 14차(11-17 밤, 사용자의 글 '[Appendix 내용 추가]'): 세 물음의 내용과 차례를 받은 글로.
#   Q1의 답: 일을 대신 하는 층과 기록을 찾는 층, 서버에서 동작한다는 설명 → Context Window에 다 담을 수 없어 검색 도구를 불러야 한다는 설명
#   Q2: 'Agent가 직접 검색하면 무엇이 문제인가요?' → '그러면 Agent가 기존 검색 툴을 써서 찾으면 무엇이 문제인가요?', 답의 첫 문장도 받은 글로
#   Q3은 그대로. Q1 옆의 그림은 답에 맞춰 내가 바꿈(두 층 그림 → 넣기 ✕, 검색 도구 호출 ✓). 각주 ¹(Agent가 서버에서 동작)은 그 그림의 '서버로 전송'에 붙임.
#   답이 길어져 칸의 높이를 글의 줄 수에 맞춤(A6_H)
A6_Q = [('Pickle이나 Muse 같은 AI Agent에게 찾아 달라고 하면 되지 않나요?',
         '수백만 건의 개인 데이터를 LLM의 **컨텍스트 윈도우(Context Window)에 한 번에 다 담을 수 없습니다.** 사진, 메모, 메시지 등 방대한 기기 데이터를 모델에 직접 주입하는 것은 '
         '물리적 한계 및 비용/보안상 불가능합니다. 따라서 Agent가 개인 기록을 참조하려면 반드시 **외부 검색 도구(Tool Calling)를 호출**해야만 합니다.'),
        ('그러면 Agent가 기존 검색 툴을 써서 찾으면 무엇이 문제인가요?',
         'Agent가 활용하는 기존 검색 툴은 개인 맥락 이해도가 낮아, Agent가 정답을 찾을 때까지 **탐색을 반복**합니다. 공개 실험에서 이런 방식은 질의 하나에 **10~27초**가 걸렸습니다.² '
         'Weave는 기록을 미리 색인해 두고 sLLM을 두 번만 불러서 **1초 안에** 답합니다.'),
        ('그러면 Agent와는 어떤 관계인가요?',
         'Weave는 **Agent가 호출하는 도구**가 됩니다. Agent가 사용자의 기억이 필요할 때 Weave에 묻고, Weave는 기기 안에서 찾은 답만 건넵니다. 기록 전체와 색인은 기기에 남습니다.')]


def a6_heights(vw=420, a_pt=13, base=150):
    """A-6 세 칸의 높이: 답의 줄 수에 맞춤(세 줄까지는 150)."""
    aw = W - 76 - 24 - (vw + 16)
    lh = lh_of(a_pt, 1.5)
    return [max(base, round(52 + lh * len(rwrap(a, a_pt, aw)) + 3 + 16)) for _, a in A6_Q]


def s_a6():
    s = page_slide('qa_agent', 'A-6', [('AI Agent(Pickle, Muse)와의 관계', INK)])
    y, gap = 98, 12
    hs = a6_heights()
    vis = [vis_xo(['기록 전체를 Context Window에 넣기', '용량과 비용의 한계, 보안 (서버로 전송¹)'], ['검색 도구를 호출 (Tool Calling)', '필요한 기록만 찾아서 읽음']),
           vis_bars('질의 1건의 소요 시간', [('Self-Ask²', 27.47, '27.5초', False), ('Iter-RetGen²', 9.68, '9.7초', False), ('Weave (UX2)', NUM.total('ux2', NUM.REF, NUM.REF), NUM.T_UX2, True)], vmax=34,
                    note='Self-Ask와 Iter-RetGen은 서버 실험값, Weave는 온디바이스 값 (D-4)'),
           vis_steps([('Agent', '무엇을 주문할지 질의'), ('Weave', '기기 안에서 검색'), ('Agent', '주문 실행')], on=(1,), note='예: “집들이 때 마신 와인 다시 주문해 줘”')]
    for i, ((q, a), h) in enumerate(zip(A6_Q, hs)):
        qrow(s, 'qa/q%d' % (i + 1), y, h, q, a, n=i + 1, vis=vis[i])
        y += h + gap
    footnote(s, ['¹ Pickle은 격리된 클라우드 실행 환경에서, Meta Muse(2026. 09)는 자체 클라우드 컴퓨터에서 동작함(각 사 소개와 보도 기준).',
                 '² Zhuang et al., "EfficientRAG", EMNLP 2024: LLM이 검색을 반복하는 방식의 질의당 소요 시간(MuSiQue).'], y - gap + 12)
    return s


# ------------------------------------------------------------------ A-7 Apple과 Google (10차의 A-8. 10차의 A-7 'LLM에게 전부 읽히면'은 Q1만 D-3으로 옮기고 뺌)
A7 = [[['Apple Siri AI', '(2026. 09)'], '메시지, 메일, 사진에서 필요한 정보를 찾아 답하는 개인 맥락 이해. 화면 인식과 앱 동작까지 Siri 안에서 제공¹', '기기 + 서버 (Private Cloud Compute)',
       'Apple 기본 앱, App Intents를 연동한 앱', 'Siri를 호출'],
      [['Gemini Personal Intelligence', '(2026. 01)'], 'Gemini 앱에 Gmail, Google 포토, YouTube, 검색을 연결해 여러 출처를 함께 보고 답변²', '서버 (Google 계정의 데이터)',
       'Google 서비스 (연결할 앱을 사용자가 선택)', 'Gemini 앱을 실행'],
      [['Pixel Magic Cue', '(2025. 08)'], '메시지나 통화 화면의 내용에 맞춰 Gmail, 캘린더, 스크린샷의 정보를 먼저 제안³', '기기 (Gemini Nano)',
       'Google 앱 중심. Pixel 10, 한국 미제공', '쓰던 화면에 자동 표시'],
      [['Pixel Screenshots', '(2024. 08)'], '사용자가 찍은 스크린샷을 기기 안에서 분석해 두고 자연어로 검색⁴', '기기 (Gemini Nano)', '스크린샷', '전용 앱을 실행'],
      [('Weave', HI), ('여러 앱의 기록을 단서로 이어서 답하고, 상황에 맞춰 먼저 제안', HI), ('전부 기기 안에서 처리', HI), ('갤러리, 노트, 캘린더, 메일 등 기기 안의 기록', HI),
       ('키보드의 버튼, 통화 중 검색창', HI)]]


def s_a7():
    s = page_slide('qa_apple', 'A-7', [('Apple, Google의 개인 기록 검색과의 차이', INK)])
    y = 98
    y += tbl(s, 'qa/t', X, y, W, [19, 33, 17, 18, 13], ['서비스', '하는 일', '처리 위치', '대상 기록', 'UX 진입점'], A7, hi=(4,), pady=8, pt=11.5) + 22
    # 14차(11-17 밤, 사용자의 글): 아래 세 칸의 이름과 글, 차례를 받은 글로(UX 진입점 → 찾는 방식 → 처리 위치). 그 전의 차례는 쓰는 자리 → 처리 위치 → 찾는 방식.
    #   받은 글의 '의미기반검색'은 띄어 쓰고 'query rewriting과 reasoning embedding'은 덱의 표기(대문자)로 적음. 표의 칸 이름 '쓰는 자리'는 그대로(받은 범위는 아래 부분)
    y += notes3(s, 'qa/n', y, [('UX 진입점: 쓰던 화면에서 바로', 'Siri는 비서를 부르고, Gemini와 Pixel Screenshots는 앱을 엽니다. Weave는 언제 어디서든 **쓰던 화면에서 바로** 씁니다. 글을 입력하는 화면에서는 키보드의 버튼으로, 통화\u00a0중에는 화면을 쓸어 올려 엽니다.'),      # 낱말이 줄에서 갈리지 않게 붙임
                               ('찾는 방식: Multi-hop 탐색', '한 번 찾고 끝나지 않고 **찾은 단서로 다시 찾습니다.** 이로써 복잡한 질문에서도 높은 정확도를 제공할 수 있습니다. 단순\u00a0의미 기반 검색을 넘어, Query\u00a0Rewriting과 Reasoning\u00a0Embedding을 기반으로 하기 때문입니다.'),
                               ('처리 위치: 전부 기기 안에서', 'Siri AI와 Gemini는 클라우드 서버를 함께 사용합니다. Weave는 색인부터 답변까지 **기기 안에서** 작동합니다.')], pt=12) + 18
    footnote(s, ['¹ Apple Newsroom, Siri AI 발표 (2026. 09. 14, 한국어는 10. 26): "These latest models run on device and on servers using Private Cloud Compute"   ² Google, Personal Intelligence 발표 (2026. 01. 14)',
                 '³ Google, Pixel 10 발표 (2025. 08). 제공 국가는 Google 지원 페이지 기준   ⁴ Google, Pixel 9 발표 (2024. 08)'], y)
    return s


# ------------------------------------------------------------------ A-8 Galaxy AI 안에서의 구성 (11차에 새로 넣음)
A8 = [('진입점', ['삼성 키보드 (Writing Assist)', 'Now Nudge, Now Brief', 'Bixby'], ['통화 중 Swipe-up 검색창 (UX1)', '키보드의 실타래 버튼 (UX2)', '키보드 위의 제안 (UX3)', 'Bixby와 Agent가 호출하는 도구 (A-6)']),
      ('데이터와 보안', ['Personal Data Engine (Knowledge Graph)', 'PDI: 알림에서 예약 정보 수집', 'KEEP, Knox Vault'], ['원문의 벡터 색인과 메타데이터', 'PDE의 사실을 필터로 사용 (A-5)', '같은 보호 구조 위에서 동작 (B-5)']),
      ('모델', ['기기에 탑재된 Samsung Gauss', 'NPU'], ['Reasoning Embedding 약 0.19GB', 'Query Rewriter Adapter 수십 MB', 'sLLM은 새로 탑재하지 않음 (D-2)'])]


def s_a8():
    s = page_slide('qa_gai', 'A-8', [('Galaxy AI 안에서의 구성', INK)])
    y, gap = 102, 18
    cw = (W - 2 * gap) / 3
    lh = lh_of(11.5, 1.6)
    rows = max(len(a) for _, a, _ in A8), max(len(b) for _, _, b in A8)
    h1, h2 = 30 + lh * rows[0] + 12, 30 + lh * rows[1] + 12
    ch = 46 + h1 + 30 + h2 + 16
    for i, (name, have, add) in enumerate(A8):
        x = X + i * (cw + gap)
        out = [box('qa/g%d/bg' % i, x, y, cw, ch, radius=18),
               T('qa/g%d/t' % i, x + 22, y + 14, cw - 44, 26, name, size=15, color=INK, weight='b', anchor='ctr'),
               R('qa/g%d/a' % i, x + 14, y + 46, cw - 28, h1, prst='roundRect', radius=12, fill=GRAY_BG, line=None),
               T('qa/g%d/al' % i, x + 28, y + 46 + 8, cw - 56, 20, 'Galaxy AI에 이미 있는 것', size=10, color=MUTE, weight='b', anchor='ctr'),
               T('qa/g%d/at' % i, x + 28, y + 46 + 30, cw - 56, lh * len(have) + 4, have, size=11.5, color=BODY, lnspc=lh * 0.75),
               arrow('qa/g%d/ar' % i, (x + cw / 2, y + 46 + h1 + 4), (x + cw / 2, y + 46 + h1 + 26), w=1.8),
               R('qa/g%d/b' % i, x + 14, y + 46 + h1 + 30, cw - 28, h2, prst='roundRect', radius=12, fill=LAV, line=RING, line_w=1.4),
               T('qa/g%d/bl' % i, x + 28, y + 46 + h1 + 30 + 8, cw - 56, 20, 'Weave가 더하는 것', size=10, color=PURPLE, weight='b', anchor='ctr'),
               T('qa/g%d/bt' % i, x + 28, y + 46 + h1 + 30 + 30, cw - 56, lh * len(add) + 4, add, size=11.5, color=INK, weight='m', lnspc=lh * 0.75)]
        s.add('qa/g%d' % i, out)
    y += ch + 22
    y += points(s, 'qa/p', X, y, W, ['**새로 만드는 것은 검색 계층 하나입니다.** 진입점은 키보드, 데이터와 보안은 PDE와 KEEP, sLLM은 Gauss를 그대로 씁니다.',
                                    '**기존 기능과 역할이 나뉩니다.** Writing Assist는 쓴 글을 다듬고, Now Nudge는 지금 화면에 맞춰 제안하고, Finder는 앱과 파일을 찾습니다. Weave는 여러 앱의 기록을 이어 찾습니다. (A-2)',
                                    '**적용 순서도 Galaxy AI와 같습니다.** 플래그십에서 시작해 One UI 업데이트로 넓힙니다. (B-3)'], gap=8, pt=12.5) + 14
    footnote(s, 'Galaxy AI의 기능과 구조는 A-2, A-4, A-5, B-5에 적은 공개 자료 기준. Weave가 더하는 것의 크기는 D-2.', y)
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
                '기록을 찾는 순간은 대부분 무언가를 입력하는 순간입니다. 어느 화면에서든 글을 입력할 때는 키보드가 떠 있어서, 앱을 옮기지 않고 그 자리에서 찾아 넣을 수 있습니다. 통화 중이나 조용한 곳에서는 음성 비서를 부르기 어렵습니다.')],
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
           'Finder도 임베딩으로 의미 검색을 합니다. 하지만 사용 맥락을 충분히 반영하지는 못하고 있습니다. '
           '‘주문’이라고 검색하면 배달의민족과 요기요가 나오지만, ‘음식 주문’이나 ‘배고파’라고 검색하면 나오지 않습니다. '
           'Weave를 통해 고도화하면 더 다양한 용도로 쓰일 수 있습니다.',
         more=[(FU_Q, FU_A + ' ' + FU_NOTE + ' Weave는 이 쓰임을 넓힙니다.'),
               ('Finder에 검색어 의도 분류가 들어가면 Weave 아닌가요?',
                '의도 분류가 들어와도 충분하지 않습니다. 여러 단서를 연달아 찾게 해 주는 Query Rewriting과, 말에 숨은 단서를 알아보는 Reasoning Embedding이 함께 있어야 합니다. '
                '진입점도 다릅니다. Weave는 다른 앱 사용 중에도, 키보드 위에서도 바로 진입합니다. A-8에 정리했습니다.'),
               ('Finder에 멀티홉 기능만 붙이면 되는 거 아닌가요?',
                '멀티홉 기능만 붙이면 연쇄 탐색 한 칸만 생깁니다. 상황 인식, 질의 재작성, 연쇄 탐색이 한 파이프라인으로 돌아야 완성도 높은 결과가 나옵니다. C-4에 정리했습니다.')],
         basis=['장과 대본은 팀원(SB-Jo)의 `Appendix_Finder와의_차별점_QA.pptx`가 바탕. 검색 예시는 Galaxy 기기의 Finder에서 직접 검색한 결과(그 장의 각주).',
                '11-17 저녁(사용자의 지시): Q2와 Q3의 자리를 바꿈. 지금은 Q2가 Finder 사용 통계, Q3이 의도 분류(Query Rewriting, Reasoning Embedding, 진입점)이고 각주의 ‘A3의 비율’도 ‘A2의 비율’로 고침. 아래 줄의 Q2, Q3은 바꾸기 전의 번호.',
                '같은 날 Q1의 답: ‘Finder도 임베딩 검색을 지원하지만, 검색어 의도 분류가 되지 않아 / 검색 결과가 일정하지 않습니다.’ → ‘Finder도 임베딩 검색을 지원하지만, 사용 맥락을 충분히 반영하지는 못하고 있습니다.’(사용자의 글 그대로) / '
                '‘Weave를 통해 고도화하면 더 다양한 용도로 쓰일 수 있습니다. (Q2)’(사용자의 초안 ‘Q2(바뀐 Q2)에 따라서 Weave를 통해 고도화하면 좋을것이다?’를 내가 다듬은 문장. 사용자의 확인은 아직 없음). 회색 줄은 그대로.',
                '같은 날 Q3의 답: ‘단서 추론을 위한’ → ‘더 깊이 있는 단서 추론을 위한’(사용자의 글 ‘깊이있는’의 띄어쓰기만 고침). 줄이 길어져 ‘(D-5, D-8)’은 오른쪽 그림의 ‘Weave가 더하는 두 가지’ 옆으로 옮김. '
                '말할 답의 ‘더 물으면’은 표현이 달라(‘말에 숨은 단서를 알아보는 Reasoning Embedding’) 그대로 둠.',
                '덧붙인 것: 공식 검색 대상 각주, 팀원 장의 ‘Appendix 참조’를 코드(D-5, D-8)로.',
                'Q2(11-17, 사용자의 지시): 답에 진입점 한 줄을 더함(‘진입점도 다릅니다. Weave는 다른 앱 사용 중에도, 키보드 위에서도 바로 진입합니다. (A-8)’). 답의 높이가 세 줄이라 둘째, 셋째 줄을 한 줄로 모았고, '
                '대본의 답도 화면의 차례(Query Rewriting, Reasoning Embedding)에 맞춤. 진입점은 둘: 다른 앱을 쓰는 중에 여는 검색창(UX1, Swipe-up)과 키보드(UX2의 실타래 버튼, UX3의 키보드 위 제안). A-8의 표와 같음.',
                'Q3(11-17, 사용자의 지시): ‘Finder에 멀티홉 기능만 붙이면 되는 거 아닌가요?’를 화면에서 빼고 Finder 사용 통계로 바꿈. 뺀 질문과 답은 위의 ‘더 물으면’에 남김.',
                '67%와 55% 이하: 사내 Finder 사용 통계(사용자가 11-16에 전달)의 지표로 셈함. 둘 다 Finder 전체 사용 대비이고, 앱 검색이 67%, 다른 용도로 한 번 이상 쓴 것이 55%. '
                '한 사용자가 양쪽에 모두 셈될 수 있어 둘을 더하면 100%를 넘고, 그래서 ‘이하’로 적음(사용자의 설명, 11-17: ‘28/51만 다른 용도로 한 번 이상 사용했다’).',
                '원래 값과 지표의 이름은 공개 저장소에 적지 않고 `원본/사내자료.json`에만 둠. 답한 분의 성함도 적지 않음(사용자: 성함까지는 필요 없음).']),
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
               ('그러면 그래프는 필요 없다는 말인가요?', '아닙니다. 날짜와 사람, 장소처럼 정리된 사실은 그래프가 가장 빠르고 정확합니다. 다음 장처럼 함께 쓸 때 가장 좋습니다.'),
               ('PDE의 Knowledge Graph나 차세대 Bixby 과제와 겹치지 않나요?', '겹치기보다 이어집니다. PDE는 기록이 들어올 때 사실을 정리하고, Weave는 질의가 들어올 때 원문에서 단서를 찾습니다. Bixby는 일을 대신 하는 쪽이고, Weave는 그때 필요한 내 기록을 찾아 주는 쪽입니다. 함께 쓰는 구성은 A-5와 A-8에 있습니다.')],
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
         a='에이전트도 개인 기록을 찾으려면 검색 도구를 불러야 합니다. 수백만 건의 개인 데이터를 LLM의 컨텍스트 윈도우에 한 번에 다 담을 수 없기 때문입니다. '
           '사진, 메모, 메시지 등 방대한 기기 데이터를 모델에 직접 주입하는 것은 물리적 한계와 비용, 보안 때문에 불가능합니다. '
           '그런데 에이전트가 활용하는 기존 검색 툴은 개인 맥락 이해도가 낮아, 정답을 찾을 때까지 탐색을 반복합니다. '
           '공개 실험에서 이런 방식은 질의 하나에 10초에서 27초가 걸렸습니다. '
           'Weave는 기록을 미리 색인해 두고 sLLM을 두 번만 불러서 1초 안에 답합니다. '
           '그래서 Weave는 에이전트가 호출하는 도구가 됩니다. 에이전트가 사용자의 기억이 필요할 때 Weave에 묻고, Weave는 기기 안에서 찾은 답만 건넵니다.',
         more=[('컨텍스트 윈도우가 더 커지면 해결되지 않나요?',
                '윈도우에 들어가더라도 많이 넣을수록 정확도가 떨어집니다. 공개 벤치마크에서 정답 기록 하나만 주면 88점인 모델이 기록 30건 가운데서는 23점이었습니다. '
                '무엇을 읽힐지 고르는 검색이 여전히 필요합니다.'),
               ('에이전트와 Weave는 무엇이 다른가요?',
                '에이전트는 예약이나 주문처럼 일을 대신 해 주는 층이고, Weave는 그 아래에서 내 기록을 찾아 주는 층입니다. '
                '지금의 에이전트는 서버에서 동작하기 때문에, 기기 안의 메모와 사진, 받은 메시지를 찾으려면 서버로 올려야 합니다.'),
               ('에이전트가 Weave를 부르면 결국 기록이 서버로 가는 것 아닌가요?', '에이전트에게 가는 것은 찾아낸 답 한 줄입니다. 기록 전체와 색인은 기기 안에 남고, 무엇을 건넬지는 사용자가 정합니다.'),
               ('Bixby가 에이전트가 되면 Weave는 필요 없지 않나요?', 'Bixby가 일을 대신 하게 될수록 내 기록을 정확히 찾아 주는 검색이 더 필요합니다. Weave는 그 검색을 맡습니다.')],
         basis=['Zhuang et al., "EfficientRAG", EMNLP 2024: MuSiQue 200문항에서 질문당 Iter-RetGen 9.68초, SelfAsk 27.47초, EfficientRAG 3.62초.',
                'Pickle(Pickle, Inc.): 전화, 예약, 쇼핑을 대신 하는 개인 AI 에이전트 앱. 격리된 클라우드 실행 환경과 가상 브라우저에서 일하고, 연결한 계정(캘린더, 메일, 쇼핑)을 씀(소개 글 기준).',
                'Meta Muse: 2026. 09. 08 발표. 자체 클라우드 컴퓨터(격리된 가상 머신과 브라우저)에서 일하고 기억 기능이 있음(보도 기준).',
                'Weave의 %s는 UX2의 온디바이스 값(D-4).' % NUM.T_UX2,
                '14차(11-17 밤, 사용자의 글): 화면의 세 물음을 받은 글로 바꿈. Q1의 답은 Context Window에 다 담을 수 없어 검색 도구(Tool Calling)를 불러야 한다는 설명으로, '
                'Q2는 ‘그러면 Agent가 기존 검색 툴을 써서 찾으면 무엇이 문제인가요?’와 ‘기존 검색 툴은 개인 맥락 이해도가 낮아, Agent가 정답을 찾을 때까지 탐색을 반복합니다’로. Q3은 그대로. '
                '말할 답도 그 차례로 다시 엮음(받은 문장을 이음). 13차까지 Q1의 답이던 두 층 설명과 서버 이야기는 ‘더 물으면’으로 옮김. Q1 옆의 그림(넣기 ✕, 검색 도구 호출 ✓)은 내가 답에 맞춰 바꾼 것.',
                '‘더 물으면’의 88점과 23점: Taghavi et al., "ImpliRet", arXiv:2506.14407, Table 3(정답 기록을 주고 답하게 한 실험, ROUGE-1 recall의 평균). GPT-4.1이 정답 기록 1건만 받으면 88.05, '
                '10건 가운데서는 35.06, 30건 가운데서는 22.90. 30건은 Context Window의 극히 일부라 윈도우의 크기와는 다른 문제임을 보여 줌(11-17에 원문에서 확인. 화면에는 넣지 않음).']),
    Page('A-7', 'Apple, Google과의 차이', s_a7,
         q='Apple의 Siri AI나 Google의 Gemini, Pixel도 개인 기록을 찾아 주지 않나요? 무엇이 다른가요?',
         a='방향은 같지만 세 가지가 다릅니다. UX 진입점과 찾는 방식, 그리고 처리 위치입니다. '
           '첫째는 UX 진입점입니다. Siri는 비서를 부르고, Gemini와 Pixel Screenshots는 앱을 엽니다. Weave는 언제 어디서든 쓰던 화면에서 바로 씁니다. '
           '글을 입력하는 화면에서는 키보드의 버튼으로, 통화 중에는 화면을 쓸어 올려 엽니다. '
           '둘째는 찾는 방식입니다. 한 번 찾고 끝나지 않고 찾은 단서로 다시 찾습니다. 이로써 복잡한 질문에서도 높은 정확도를 제공할 수 있습니다. '
           '단순 의미 기반 검색을 넘어, Query Rewriting과 Reasoning Embedding을 기반으로 하기 때문입니다. '
           '셋째는 처리 위치입니다. Siri AI와 Gemini는 클라우드 서버를 함께 사용합니다. Weave는 색인부터 답변까지 기기 안에서 작동합니다. '
           'Apple은 Siri AI에서 메시지와 메일, 사진을 이어 답하는 기능을 내놓았고, Google은 Gemini의 Personal Intelligence와 Pixel의 Magic Cue를 내놓았습니다. '
           '저희는 이것을 개인 기록 검색이 스마트폰 AI의 다음 경쟁 축이라는 신호로 봅니다.',
         more=[('Apple이 먼저 한 것 아닌가요?', '방향은 같습니다. 그래서 Galaxy에도 필요하다고 봅니다. 저희는 기기 안 처리와 키보드라는 자리로 차별화합니다.'),
               ('Pixel의 Magic Cue는요?',
                'Gmail과 캘린더, 스크린샷을 이어 먼저 제안하는 기능으로 방향이 같습니다. 다만 Google 앱이 중심이고 한국에는 제공되지 않습니다.'),
               ('Pixel Screenshots는요?', '사용자가 찍은 스크린샷만 대상입니다. 기기 안에서 분석해 두고 자연어로 찾는 전용 앱입니다. Weave는 스크린샷을 포함해 여러 앱의 기록을 함께 봅니다.'),
               ('왜 꼭 키보드인가요?', '기록을 찾는 순간은 대부분 무언가를 입력하는 순간입니다. 어느 화면에서든 글을 입력할 때는 키보드가 떠 있어서, 앱을 옮기지 않고 그 자리에서 찾아 넣을 수 있습니다. 통화 중이나 조용한 곳에서는 음성 비서를 부르기 어렵습니다.')],
         basis=['Apple Newsroom(2026. 09. 14): "if a user asks Siri what a family member suggested as an activity during an upcoming visit, Siri can search the user\'s messages … pull up the cooking instructions from an email … add the ingredients to their grocery list in the Reminders app". "These latest models run on device and on servers using Private Cloud Compute." 한국어는 2026. 10. 26.',
                'Siri AI의 구성(11-16 저녁 검색으로 다시 확인, WWDC26 보도): 개인 맥락 이해(메시지, 메일, 사진에서 정보를 찾음), 화면 인식(화면의 내용을 보고 답하거나 동작), 앱 동작(App Intents로 앱이 내용과 기능을 Siri AI에 내어 줌).',
                'Google(2026. 01. 14): "Personal Intelligence has two core strengths: reasoning across complex sources and retrieving specific details from, say, an email or photo". "this data already lives at Google". Gmail, 포토, YouTube, 검색을 연결하고 연결은 기본으로 꺼져 있음(사용자가 고름). 처음에는 미국의 AI Pro, AI Ultra 구독자 대상 베타.',
                'Pixel Magic Cue(2025. 08. 20): Gmail, 캘린더, 스크린샷, 메시지를 이어 먼저 제안. Google의 소개 글은 Tensor G5와 Gemini Nano로 기기에서 돈다고 설명(11-16 검색으로 확인). 제공 국가 9곳에 한국은 없음(Google 지원 페이지). 2026년 5월에 Wallet, Tasks가 더해짐(9to5Google).',
                'Pixel Screenshots(2024. 08. 13, Pixel 9): 사용자가 찍은 스크린샷을 기기 안의 Gemini Nano로 분석해 색인하고 자연어로 검색. 화면을 계속 찍어 두는 방식이 아니라 사용자가 찍은 스크린샷만 대상(9to5Google, Android Authority).',
                '11차(11-16): 팀 검토(표만 보고는 어떤 기능인지 모르겠다, 차별점을 더 보충, UX 진입점을 넣기)로 표의 ‘하는 일’을 풀어 쓰고 ‘쓰는 자리’ 칸과 Pixel Screenshots 줄을 더함. 아래 설명 세 칸을 쓰는 자리, 처리 위치, 찾는 방식으로 다시 씀. 답에서는 예시를 들지 않고 차이만 설명함.',
                '14차(11-17 밤, 사용자의 글): 아래 세 칸을 UX 진입점(‘쓰는 자리’에서 이름을 바꿈. ‘언제 어디서든’을 더함), 찾는 방식: Multi-hop 탐색(‘단서를 이어서’에서. 글도 받은 글로), '
                '처리 위치(‘클라우드 서버를 함께 사용합니다’, ‘기기 안에서 작동합니다’. ‘기기에서만 처리 설정에서도 그대로 동작합니다’는 뺌)의 차례로 놓음. 말할 답도 같은 차례와 문장으로 맞춤. '
                '표의 칸 이름 ‘쓰는 자리’는 그대로 둠. ‘단순 의미 기반 검색에 그치는 경쟁사’는 사용자의 문장이고, Google의 발표문은 Personal Intelligence의 강점으로 ‘reasoning across complex sources’를 든다는 점을 사용자에게 알림.',
                '같은 밤에 사용자의 승낙(‘그래’)을 받아 둘을 고침: 표의 칸 이름 ‘쓰는 자리’ → ‘UX 진입점’(아래 칸과 같은 말), ‘단순 의미 기반 검색에 그치는 경쟁사와 달리, … 기반으로 제공할 수 있기 때문입니다’ → ‘단순 의미 기반 검색을 넘어, Query Rewriting과 Reasoning Embedding을 기반으로 하기 때문입니다’(화면과 말할 답).',
                '11-16 저녁: 서드파티 앱과 메신저를 차별점으로 적은 곳을 뺌(사용자의 지시: 협약이 필요할 수도 있어 장점으로 내세우지 않음). 표의 대상 기록 ‘삼성 기본 앱, 알림으로 받는 외부 메신저’ → ‘갤러리, 노트, 캘린더, 메일 등 기기 안의 기록’, 설명 칸과 답의 ‘카카오톡 같은 외부 메신저의 단서도 알림으로 읽어’를 뺌.']),
    Page('A-8', 'Galaxy AI 안에서의 구성', s_a8,
         q='이 기능이 Galaxy AI에 들어간다면 어떤 구성이 되나요? 기존 기능이나 진행 중인 과제와 겹치지 않나요?',
         a='기존 Galaxy AI의 자산을 그대로 쓰고, 그 위에 검색 계층 하나를 더하는 구성입니다. '
           '진입점은 삼성 키보드와 통화 화면의 검색창입니다. 키보드에는 Writing Assist가 있는 자리에 실타래 버튼을 두고, 먼저 건네는 제안은 Now Nudge처럼 키보드 위에 띄웁니다. '
           '데이터와 보안은 PDE와 PDI가 모으는 경로, 그리고 KEEP과 Knox Vault의 보호 구조를 그대로 쓰고, Weave는 여기에 원문의 벡터 색인을 더합니다. '
           '모델은 기기에 탑재된 Gauss를 함께 쓰고, 새로 탑재하는 것은 임베딩 모델 하나와 작은 어댑터입니다. '
           '기존 기능과는 역할이 나뉩니다. Writing Assist는 쓴 글을 다듬고, Now Nudge는 지금 화면에 맞춰 제안하고, Finder는 앱과 파일을 찾습니다. '
           'Weave는 그 사이에서 여러 앱의 기록을 단서로 이어 찾는 일을 맡습니다.',
         more=[('PDE 과제나 차세대 Bixby와 겹치지 않나요?', 'PDE는 기록이 들어올 때 사실을 정리하고, Weave는 질의가 들어올 때 원문에서 단서를 찾습니다. Bixby가 일을 대신 하게 될수록 내 기록을 정확히 찾아 주는 검색이 더 필요합니다. 겹치기보다 이어지는 관계입니다. A-4, A-5, A-6에 정리했습니다.'),
               ('별도 앱으로 내는 건가요?', '아닙니다. 키보드의 버튼과 키보드 위의 제안, 통화 화면의 검색창으로 들어갑니다. 따로 여는 앱이 없습니다.'),
               ('어느 기기부터 넣나요?', '임베딩 검색은 가벼워서 넓게 적용하고, sLLM이 필요한 기능은 Gauss가 탑재된 플래그십부터 넣습니다. B-3에 정리했습니다.')],
         basis=['11차(11-16)에 새로 넣은 장: 팀 검토의 질문("Galaxy AI 안에 이게 편입된다면 어떤 구성 전략을 취할 수 있는지")과 예상 질문 1번(사내 기술 중복성).',
                '이미 있는 것은 A-2(Writing Assist, Now Nudge, Finder), A-4와 A-5(PDE), B-5(KEEP, Knox Vault), B-7(PDI)의 공개 자료 기준. Weave가 더하는 것의 크기는 D-2.',
                'Finder 검색 결과에 Weave를 넣는 구성은 적지 않음(Finder의 업그레이드판이라는 인상을 피함).']),
]
