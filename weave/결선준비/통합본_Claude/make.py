#!/usr/bin/env python3
"""통합본(Claude) — 인트로 + 모션그래픽~How it Works + 뒷부분 + Appendix를 한 덱으로 → Weave_통합본_Claude.pptx

  python make.py                  덱만
  python make.py --png            + out/png/s01.png… 와 out/한눈에.png (PowerPoint로 렌더)

재료
- 인트로 2~5, 7~14쪽: 원본/통합본_인트로수정_87bf80b.pptx (jjun-0824/t3 87bf80b: 우리 3차 덱의 7~14쪽을 팀원이 손본 판)의 장을 그대로 옮긴다(도형·그림·전환·효과·노트).
  4·5쪽의 둘째 말풍선만 '그 이름이 뭐였지?' → '정확한 이름이 뭐였지?'로 바꾼다(patch_ask2).
  6차(11-13)에 더 손본 곳: 3쪽은 인물과 말풍선이 클릭해야 뜨고(patch_person_click), 3~5쪽의 옅은 기록 조각이 세 층으로 떠다닌다(patch_floats).
  7쪽 머리글, 9쪽 퍼센트와 이름의 글자 크기, 10쪽 AI 답변의 글(patch_heading7, patch_hub, patch_answer).
  7차(11-13): 3~5쪽 인물 뒤에 아주 옅은 보라 그라데이션(patch_aura).
  4차까지는 원본/Weave_결선_중간본_도입부수정.pptx의 장을 옮겨 손보고(patch_intro) 9, 11~12, 14쪽은 새로 그렸다(slides_new.py의 s_hub2, s_scat, s_link, s_bridge).
- 6쪽(수많은 기록): 새로 그린다(slides_new.py).
- 바꾸기 전의 장(12차부터는 덱에 넣지 않음. OLD_GROUPS = True일 때만): 원본/통합본_8차.pptx (git show c3a5b5d:…), 원본/통합본_7차.pptx (git show e0a4e14:…), 원본/통합본_6차.pptx (git show 9c91050:…), 원본/통합본_5차.pptx (git show fcf8346:…), 원본/통합본_4차.pptx (git show 406c351:…), 원본/통합본_3차.pptx (git show ab0c460:…), 원본/통합본_2차.pptx (git show 9a8bddb:…), 원본/통합본_1차.pptx (git show ab7ab74:…)에서 옮겨 덱 맨 뒤에 둔다.
- 표지와 모션그래픽 영상 장: 02_PPT/Weave_결선_중간본.pptx의 1쪽과 4쪽. 표지는 영상을 v9(10_표지영상/표지_루프.mp4, 18초)로 바꾸고 제목을 조금 줄인다(patch_cover).
  모션그래픽은 영상을 v24(08_인트로영상/Weave_모션그래픽.mp4: 제목의 색과 자간을 표지와 같게)로 바꿔 끼운다(patch_mg).
- 솔루션 3장 + How it Works 13장 + Appendix 15장: 09_HowItWorks/장표5_claude/build.py의 장을 그대로 그린다.
- 뒷부분: 원본/Weave_BI_아웃트로_통합_1110_v7.pptx (WIWLEE/t3-2)의 내용을 같은 엔진으로 다시 그린다(slides_new.py).
  6차: 기대효과는 한 장(fx_new.s_fx), 기존 기능과의 비교는 Appendix 맨 앞으로(cmp_new.s_cmp_apx), 제안 장표 묶음은 없앰.
  7차: 비교 장을 다시 본 발표로(cmp_new.s_cmp, 기대효과 다음), 맺는 인사를 하는 마지막 장(slides_new.s_bye)을 더함.
  8차(11-13 낮): 발표자가 다시 쓴 대본. 12쪽을 둘로 나눔(patch_gather: 기록 그림만 가운데로 옮겨 오는 장을 11쪽과 12쪽 사이에),
  10쪽 AI 답변 글자를 한 단계 작게 하고 말풍선의 네 변 여백을 맞춤(patch_answer), 15쪽 로고를 조금 오른쪽으로(patch_logo_center),
  비교 장은 다시 Appendix 맨 앞으로(cmp_new.s_cmp_apx2), 모션그래픽은 v25(03 장면의 대화, 탑승권, 링크, 병 사진).
  10차(11-15): Appendix를 발표 뒤 질의응답용으로 다시 짬(qna.py: 목차, A 기존 기술과의 차이, B 상품화, C 동작 방식, D 모델과 학습, E 시나리오 더 보기, 출처).
  장마다 코드와 쪽 번호가 있고 목차의 항목을 누르면 그 장으로 감. 9차의 Appendix에서 합치거나 고치거나 뺀 장은 덱 뒤쪽 '이전 판 (9차 Appendix)'에.
  9차(11-14): 비즈니스 임팩트(8차 34쪽)를 본 발표에서 빼고 연표 다음에 '미래의 Weave'(next2_new.s_next)를 넣음. 연표의 두 줄 사이를 조금 좁히고,
  맺는 장은 15쪽처럼 앱들이 실로 이어짐(slides_new.s_bye). How it Works 29, 30쪽의 대본은 '핵심 요소'를 짚는 말로(장표5_claude/build.py).
  11차(11-16): 팀 검토를 본 발표와 대본, Appendix에 넣음. 39쪽 뒤에 Q&A 장(slides_new.s_qa), Appendix 42장(41~82쪽).
  12차(11-16 밤): 2쪽의 통화 음성을 새로 받은 목소리로 바꾸고(tools/call_build.py) 통화 시간이 받는 소리부터 1초마다 올라가게(call_timer),
  10쪽 AI 답변을 15pt로(ANSWER_PT, ANS_PAD_B), 33쪽은 한 번의 클릭에 세 칸이 왼쪽부터 차례로(fx_new.FX_STEP),
  35쪽은 두 줄이 Weave 아이콘 아래에서 뻗어 나오게(next2_new.lane_bends). 덱 뒤쪽에 차수마다 쌓아 두던 '이전 판' 묶음은 덱에서 뺌
  (OLD_GROUPS = False: 'ppt에서 이전 판 장표는 이제 지워 줘'). 덱은 본 발표 39장 + Q&A + Appendix 42장 = 82장.
  13차(11-17): Appendix만 다시 짬(본 발표와 영상은 그대로). 묶음을 A 기존 기술과의 차이, B 상품화와 사업성, C 시나리오 더 보기와 동작 방식, D 모델과 성능, Query Rewriter / Reasoning Embedding과 데이터로
  다시 묶고(qna_lib.SECTIONS), 설문 장과 1년 상품화 계획 장을 새로 그리고, UX3 장과 Gate 장을 한 장으로 합침. Appendix 40장(41~80쪽), 덱은 80장.
  14차(11-17 밤): 본 발표의 대본 여덟 곳(1, 2, 3, 17, 18, 27, 33, 35쪽: slides_new.INTRO_NOTES, 장표5_claude/build.py의 NOTES, fx_new.FX_NOTE, next2_new.NOTE)과
  33쪽의 효과(숫자가 0까지 줄어드는 효과를 없애고 달라진 글이 곧바로 뜸, 클릭 4 → 3번: fx_new.s_fx). 화면의 글과 Appendix는 그대로. 본 발표의 클릭은 33 → 32번.
"""
import argparse
import copy
import hashlib
import itertools
import re
import shutil
import sys
from pathlib import Path

from lxml import etree
from pptx import Presentation

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
HIWDIR = ROOT / '09_HowItWorks' / '장표5_claude'
sys.path.insert(0, str(HIWDIR))
sys.path.insert(0, str(ROOT / '11_중간본'))
import build as HW  # noqa: E402  (How it Works 엔진: Slide, add_slides, 낭독·영상 도구)
import render_c  # noqa: E402
import samsung_fonts  # noqa: E402
from ui import P, Painter  # noqa: E402

import foreign as F  # noqa: E402

OUT = Path(__file__).resolve().parent / 'out'
OUT.mkdir(exist_ok=True)
for _f in ('blur_sol.png', 'blur_emb.png', 'blur_cloud.png'):       # How it Works의 흐린 배경 그림은 그쪽 것을 그대로
    if not (OUT / _f).exists():
        shutil.copyfile(HW.OUT / _f, OUT / _f)
HW.OUT = OUT                                                      # 낭독(out/tts)과 말에 맞춘 효과의 때를 이 폴더에서 읽고 씀

# ------------------------------------------------------------------ 읽는 소리: 숫자·영문을 소리 나는 대로(How it Works의 tts_text 앞에 한 번 더 거름)
READ_FIRST = [('Personal Data Engine', '퍼스널 데이터 엔진'), ('Weave Assist', '위브 어시스트'), ('Writing Assist', '라이팅 어시스트'), ('Galaxy AI', '갤럭시 에이아이'), ('Now Nudge', '나우 넛지'), ('Finder', '파인더'), ('RAG', '래그'),
              ('AgentIR', '에이전트 아이알'), ('Hi-Q', '하이큐'), ('NPU', '엔피유'), ('Lock-in', '락인'),
              ('SmartThings', '스마트싱스'), ('Bixby', '빅스비'), ('S펜', '에스펜'), ('TV', '티브이'),      # 9차: 미래의 Weave
              ('Multi-hop', '멀티홉'), ('PDE', '피디이'), ('KEEP', '킵'), ('AI', '에이아이'), ('Samsung', '삼성'), ('Galaxy', '갤럭시'), ("'", '')]
DIGIT = '영일이삼사오육칠팔구'


def say_pre(t):
    for k, v in READ_FIRST:
        t = t.replace(k, v)
    dec = lambda m: '%s 점 %s' % (HW._num_ko(int(m.group(1))), ''.join(DIGIT[int(d)] for d in m.group(2)))
    t = re.sub(r'(\d+)\.(\d+)\s*%', lambda m: dec(m) + ' 퍼센트', t)
    t = re.sub(r'(\d+)\s*%', lambda m: HW._num_ko(int(m.group(1))) + ' 퍼센트', t)
    t = re.sub(r'(\d+)\.(\d+)', dec, t)
    return t


_tts_text = HW.tts_text
HW.tts_text = lambda seg: _tts_text(say_pre(seg))

import slides_new as N  # noqa: E402

BASE = ROOT / '02_PPT' / 'Weave_결선_중간본.pptx'
INTRO = HERE / '원본' / 'Weave_결선_중간본_도입부수정.pptx'
PREV = HERE / '원본' / '통합본_1차.pptx'                 # 11월 11일 1차 통합본(바꾸기 전의 장을 여기서 옮김)
PREV2 = HERE / '원본' / '통합본_2차.pptx'                # 11월 11일 2차 통합본
PREV3 = HERE / '원본' / '통합본_3차.pptx'                # 11월 12일 3차 통합본
PREV4 = HERE / '원본' / '통합본_4차.pptx'                # 11월 12일 4차 통합본
PREV5 = HERE / '원본' / '통합본_5차.pptx'                # 11월 12일 5차 통합본(밤의 낱말 수정까지, fcf8346)
PREV6 = HERE / '원본' / '통합본_6차.pptx'                # 11월 13일 6차 통합본(9c91050)
PREV7 = HERE / '원본' / '통합본_7차.pptx'                # 11월 13일 7차 통합본(7차 뒤의 손질까지, e0a4e14)
PREV8 = HERE / '원본' / '통합본_8차.pptx'                # 11월 13일 8차 통합본(c3a5b5d)
PREV9 = HERE / '원본' / '통합본_9차.pptx'                # 11월 15일 9차 통합본(414bf78). Appendix를 질의응답용으로 다시 짜기 전
PREV10 = HERE / '원본' / '통합본_10차.pptx'              # 11월 16일 10차 통합본(b9e2a03). 11차(팀 검토를 모아 본문과 Appendix를 고침) 전
PREV11 = HERE / '원본' / '통합본_11차.pptx'              # 11월 16일 저녁 11차 통합본(e48463d). 12차(2쪽의 새 통화 음성과 통화 시간, 대본과 화면 손질) 전
# 12차(11-16 밤) 'ppt에서 이전 판 장표는 이제 지워 줘': 덱 뒤쪽에 차수마다 쌓아 두던 '이전 판' 묶음(11차 ~ 1차, 가름 장까지 214장)을 덱에 넣지 않는다.
#   바꾸기 전의 장은 그 차수의 덱(원본/통합본_N차.pptx. README에 git 주소)과 대본.md의 '바꾼 곳', 대본_이전판.md에 남아 있다. 다시 넣으려면 True
OLD_GROUPS = False
INTRO2 = HERE / '원본' / '통합본_인트로수정_87bf80b.pptx'   # 팀원이 7~14쪽을 손본 덱(jjun-0824/t3 87bf80b). 2~5쪽과 7~14쪽을 여기서 옮김
MG_MP4 = ROOT / '08_인트로영상' / 'Weave_모션그래픽.mp4'      # 모션그래픽 v25(111.1초). 중간본에 든 v23과 길이와 소리가 같음
COVER_MP4 = ROOT / '10_표지영상' / '표지_루프.mp4'      # 표지 영상 v9(18초)
COVER_JPG = ROOT / '10_표지영상' / '표지_포스터.jpg'
COVER_PT = 48                                          # 표지 제목 크기(54 → 48pt: 'Assist'의 t가 뒤 영상의 '부재중 전화' 조각에 닿지 않게)
INTRO_AS = HERE / 'assets' / 'intro'                   # 3~5쪽의 옅은 기록 조각, 13쪽의 흐린 배경

DST = HERE / 'Weave_통합본_Claude.pptx'
q = F.q
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
GRAD = ('<a:gradFill xmlns:a="%s" rotWithShape="1"><a:gsLst><a:gs pos="0"><a:srgbClr val="4E36CF"/></a:gs>'
        '<a:gs pos="100000"><a:srgbClr val="8F66FF"/></a:gs></a:gsLst><a:lin ang="0" scaled="1"/></a:gradFill>') % A


def drop_slides(prs, slides):
    parts = {s.part for s in slides}
    lst = prs.slides._sldIdLst
    for e in list(lst):
        if prs.part.related_part(e.get(q('r:id'))) in parts:
            prs.part.drop_rel(e.get(q('r:id')))
            lst.remove(e)


def reorder(prs, order):
    lst = prs.slides._sldIdLst
    by_part = {prs.part.related_part(e.get(q('r:id'))): e for e in list(lst)}
    assert len(order) == len(by_part) == len({id(s) for s in order}), (len(order), len(by_part))
    for e in list(lst):
        lst.remove(e)
    for s in order:
        lst.append(by_part[s.part])


def logo_style(slides):
    """이름이 logo_word로 끝나는 글상자를 표지 제목처럼: 글꼴 Samsung Sharp Sans, 보라 그라데이션."""
    from lxml import etree
    n = 0
    for sl in slides:
        for sp in sl._element.iter(q('p:sp')):
            nv = sp.find(q('p:nvSpPr') + '/' + q('p:cNvPr'))
            if nv is None or not nv.get('name', '').endswith('logo_word'):
                continue
            for rp in sp.iter('{%s}rPr' % A, '{%s}endParaRPr' % A):
                for tag in ('latin', 'ea', 'cs'):
                    e = rp.find('{%s}%s' % (A, tag))
                    if e is not None:
                        e.set('typeface', 'Samsung Sharp Sans')
                rp.set('b', '1')
                old = rp.find('{%s}solidFill' % A)
                if old is not None:
                    old.addprevious(etree.fromstring(GRAD))
                    rp.remove(old)
            n += 1
    return n


# 옮겨 오는 인트로 장: {키: INTRO2의 쪽}. in..의 숫자는 처음 인트로 덱의 쪽(이름을 그대로 둠). 6쪽은 새로 그림(hook)
# 8차: gath는 11쪽(scat)을 한 번 더 옮겨 기록 그림만 가운데에 둔 장(patch_gather). 덱에서는 11쪽과 예전 12쪽(link) 사이, 새 12쪽
FOREIGN = {'in02': 2, 'in03': 3, 'in04': 4, 'in05': 5, 'in07': 7, 'in08': 8, 'hub2': 9, 'in09': 10, 'scat': 11, 'gath': 11, 'link': 12, 'in12': 13,
           'bridge': 14}
INTRO_KEYS = list(FOREIGN)
RING_ADJ = ('7741', '9800')                        # 7·8쪽 고리 굵기(도형 크기의 7.7% → 9.8%, 298px에 23px → 29px)
OLD_SRC = '* 출처: 스마트폰 내 개인 기록 탐색 및 재검색 행태 설문조사 (응답 210명, 2026. 11)'
INTRO_TEXT = {                                      # 옮겨 온 장의 화면 글을 바꾸는 곳: {장: [(원래, 지금)]}
    'in07': [('검색으로 바로 찾지 못한 경험', '원하는 정보를 한 번에 찾지 못한 경험'), (OLD_SRC, N.SURVEY_SRC)],
    'in08': [(OLD_SRC, N.SURVEY_SRC)],
    'in12': [('내 폰에 바로 물을 순 없을까요?', '내 휴대폰에게 바로 물을 순 없을까요?')],
}
# 3~5쪽 말풍선: {장: {말풍선: 옆으로 옮기는 만큼(px)}}. 가운데 인물의 말풍선은 조금 오른쪽, 오른쪽 인물의 말풍선은 조금 왼쪽으로
BUBBLE_DX = {'in04': {'b2': 24}, 'in05': {'b2': 24, 'b3': -40}}
# 말풍선 꼬리(동그라미 둘)의 자리: 몸통 왼쪽 끝에서 큰 동그라미, 작은 동그라미의 가운데까지(px). 없으면 그대로(왼쪽 인물: 왼쪽에서)
BUBBLE_TAIL = {'b2': lambda w: (w / 2, w / 2 - 7),             # 가운데 인물: 말풍선 한가운데에서
               'b3': lambda w: (w - 128.5, w - 114)}           # 오른쪽 인물: 왼쪽 인물과 좌우가 뒤집힌 자리(오른쪽에서)
FLOATS_BOX = (0, 16, 1280, 236)                     # 3~5쪽 말풍선 위에 흩어진 옅은 기록 조각(assets/intro/floats.png). 제목은 빼고 그 자리까지 씀
NOTE_OLD_SHA1 = 'd9375bd6e2'                        # 가장자리에 흰 테가 남은 삼성노트 아이콘(sha1 앞 10자리). 옮겨 온 장에서는 다듬은 것으로 바꿔 끼움
# 덱 차례(본 발표). 글자 = 옮겨 온 장, ('own', 이름) = 새로 그린 묶음, 'mg' = 모션그래픽
SEQ = ['cover', 'in02', 'in03', 'in04', 'in05', ('own', 'hook'), 'in07', 'in08', 'hub2', 'in09', 'scat', 'gath', 'link', 'in12', 'bridge',
       'mg', ('own', 'hiw'), ('own', 'back')]
PREV_KEEP = list(range(2, 14)) + list(range(32, 42)) + [59]      # 1차 통합본에서 남겨 두는 장: 인트로 2~13쪽, 뒷부분 32~41쪽, 저장 채널 그림(59쪽)
PREV2_KEEP = list(range(2, 15)) + [26] + list(range(32, 42)) + [62]      # 2차 통합본에서: 인트로 2~14쪽, 빠진 고리(26쪽), 뒷부분 32~41쪽, 두 줄 연표 제안(62쪽)
# 5차 통합본에서: 6차에 화면이나 대본이 바뀐 장(2, 3, 7, 9, 10, 17, 18, 21~25, 28~30쪽), 기대효과 세 장(32~34), 비교 지도(35), 비즈니스 임팩트(36),
# 마무리 세 장(38~40), 제안 장표 묶음(57~60)
PREV5_KEEP = [2, 3, 7, 9, 10, 17, 18, 21, 22, 23, 24, 25, 28, 29, 30, 32, 33, 34, 35, 36, 38, 39, 40, 57, 58, 59, 60]
PREV4_KEEP = list(range(7, 15))                         # 4차 통합본에서: 우리가 그리거나 손본 7~14쪽(팀원이 손본 장으로 바뀜)
# 6차 통합본에서: 7차에 화면이나 대본이 바뀐 장. 인물 셋(3~5쪽), 기대효과(32), 비즈니스 임팩트(33), 연표(34), 마무리 ③(37), Appendix에 두었던 비교 장(39)
PREV6_KEEP = [3, 4, 5, 32, 33, 34, 37, 39]
PREV3_KEEP = [16] + list(range(21, 27)) + [30, 37]      # 3차 통합본에서: 16쪽(대본), 21쪽(뺀 장), 22~26쪽과 30쪽(화면 번호와 대본), 37쪽(비교 표)
# 7차 통합본에서: 8차에 화면이나 대본이 바뀐 장. 인트로 2~5, 7~12, 14쪽, 솔루션 ③(18), 기존 검색 물음(21), 키워드(22), 임베딩(23), step(24), 중간 단서(25),
# Hop 1(29), 결과 제공(31), 기대효과(32), 비교(33), 비즈니스 임팩트(34), 연표(35), 마무리 ①②(36, 37), 맺는 장(39)
PREV7_KEEP = [2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 14, 18, 21, 22, 23, 24, 25, 29, 31, 32, 33, 34, 35, 36, 37, 39]
# 8차 통합본에서: 9차에 화면이나 대본이 바뀐 장. 수많은 기록(6), 02 질의 재작성(29), Hop 1(30), Hop 2(31), 본 발표에서 뺀 비즈니스 임팩트(34), 연표(35),
# 마무리 ①(36), 맺는 장(39). 6쪽과 31쪽은 11월 14일 밤에 더함(6쪽 '기억' → '기록', 29~31쪽 Query Rewriting 판의 sLLM 뱃지),
# 2쪽은 11월 15일에 더함(통화 음성을 넣고 대본의 첫 문장을 뺌), 17~19쪽과 24, 26쪽도 11월 15일에 더함(17~19쪽의 손글씨 '쓱!', '톡!', '반짝!'을 빼고
# 17, 24, 26쪽의 대본을 발표자가 고침)
PREV8_KEEP = [2, 6, 17, 18, 19, 24, 26, 29, 30, 31, 34, 35, 36, 39]
# 9차 통합본에서: 10차(11-15)에 질의응답용으로 다시 짜면서 합치거나 고치거나 뺀 Appendix 장. 한눈에 보기(42), 모듈과 역할(43), Reasoning Embedding과 질의 재작성(44),
# AgentIR 후보 방식(45), 지식 그래프 두 장(46, 47), 검색 방식 비교(48, 뺌), 세 UX 공통 파이프라인(49), PDE 질문(50), 같은 날 사진(51), Apple(52), LLM(53)
PREV9_KEEP = list(range(42, 54))
# 10차 통합본에서: 11차(11-16)에 화면이나 대본이 바뀐 본 발표 장. 표지(소속), 통화(2쪽), 수많은 기록(6쪽)과 설문(7쪽)의 검색어, 10쪽(클릭과 글자 크기),
# 11쪽과 14쪽(글자 크기), 잇는 장(15쪽 대본), How it works(20쪽), 키워드(23), 임베딩(24), step(25), 중간 단서(26), 01 상황 인식(28), Hop 1(30), Hop 2(31),
# 04 결과 제공(32), 기대효과(33), 연표(34), 미래의 Weave(35). 그 뒤는 10차의 Appendix 가운데 11차에 고치거나 합치거나 뺀 장(PREV10_APX)
PREV10_KEEP = [1, 2, 6, 7, 10, 11, 14, 15, 20, 23, 24, 25, 26, 28, 30, 31, 32, 33, 34, 35]
# 10차의 Appendix(40~76쪽) 가운데: 목차(40), Finder(43), LLM에게 전부 읽히면(47, 뺌), Apple과 Google(48), B 묶음 가운데 화면이 바뀐 장(49~54, 56),
# C 묶음(57~62), 모델 스펙(63), Query Rewriting의 종류(64), 시나리오 더 보기 세 장(71~73). 낱말 하나나 참조 코드만 바뀐 장(42, 44, 46, 55, 66, 74, 75)은 넣지 않음
PREV10_APX = [40, 43, 47, 48, 49, 50, 51, 52, 53, 54, 56, 57, 58, 59, 60, 61, 62, 63, 64, 71, 72, 73]
# 11차 통합본에서: 12차(11-16 밤)에 화면이나 대본이 바뀐 본 발표 장. 표지(대본), 통화(2쪽: 음성과 통화 시간), 3쪽(대본), 10쪽(AI 답변의 글자 크기),
# step(25쪽 대본), 04 결과 제공(32쪽: 커서의 자리), 기대효과(33쪽: 세 칸이 한꺼번에 바뀌던 것), 미래의 Weave(35쪽: Weave 아이콘과 두 줄이 만나는 곳)
PREV11_KEEP = [1, 2, 3, 10, 25, 32, 33, 35]


def own_specs():
    """새로 그린 장의 묶음(덱과 낭독 영상이 같은 것을 씀)."""
    return dict(hook=[N.s_hook()],
                hiw=[f() for f in HW.SOL_SLIDES] + [f() for f in HW.SLIDES], back=[f() for f in N.SLIDES_BACK],
                prop=[f() for f in N.SLIDES_PROPOSAL])


def appendix_specs():
    """Appendix: 가름 장 → 기존 기능과의 비교 → How it Works Appendix → 사진과 음악 출처.
    비교 장은 6차에 여기 있다가 7차에 본 발표로 갔고, 8차에 다시 가름 장 바로 뒤로 옴(cmp_new.s_cmp_apx2: 기존 기능은 처음부터 떠 있고 클릭하면 Weave)."""
    import cmp_new
    hw = HW.appendix_specs()
    return [hw[0], cmp_new.s_cmp_apx2()] + hw[1:] + [N.s_credits2()]


# ------------------------------------------------------------------ 옮겨 온 장을 손보는 도구
def live_tree(slide):
    return slide._element.find(q('p:cSld')).find(q('p:spTree'))


def painter(slide):
    """옮겨 온 장에 엔진의 원시 도형을 그려 넣는 붓. 옮겨 온 장은 python-pptx의 shapes가 옛 도형 나무를 붙들고 있어서 지금 나무에 직접 넣는다."""
    pa = Painter(slide)
    pa.tree = live_tree(slide)
    ids = [int(e.get('id')) for e in pa.tree.iter() if e.tag.endswith('}cNvPr') and (e.get('id') or '').isdigit()]
    pa.ids = itertools.count(max(ids) + 1)
    return pa


def by_name(slide, name):
    """이름이 name인 도형(묶음, 그림 포함)의 요소."""
    hit = [e.getparent().getparent() for e in live_tree(slide).iter() if e.tag.endswith('}cNvPr') and e.get('name') == name]
    assert len(hit) == 1, (name, len(hit))
    return hit[0]


def has(slide, name):
    return any(e.get('name') == name for e in live_tree(slide).iter() if e.tag.endswith('}cNvPr'))


def xfrm(el):
    return el.find('.//{%s}xfrm' % A)


def shift(el, dx=0, dy=0):
    off = xfrm(el).find('{%s}off' % A)
    off.set('x', str(int(off.get('x')) + round(dx * 9525)))
    off.set('y', str(int(off.get('y')) + round(dy * 9525)))


def box(el):
    x = xfrm(el)
    off, ext = x.find('{%s}off' % A), x.find('{%s}ext' % A)
    return [int(off.get('x')) / 9525, int(off.get('y')) / 9525, int(ext.get('cx')) / 9525, int(ext.get('cy')) / 9525]


def place(el, x=None, y=None, w=None, h=None):
    xf = xfrm(el)
    off, ext = xf.find('{%s}off' % A), xf.find('{%s}ext' % A)
    for e, k, v in ((off, 'x', x), (off, 'y', y), (ext, 'cx', w), (ext, 'cy', h)):
        if v is not None:
            e.set(k, str(round(v * 9525)))


def repoint(slide, pic, path):
    """그림 도형이 다른 그림 파일을 가리키게 한다(같은 그림을 쓰는 다른 장은 그대로)."""
    blip = pic.find('.//{%s}blip' % A)
    old = blip.get(q('r:embed'))
    blip.set(q('r:embed'), slide.part.get_or_add_image_part(str(path))[1])
    if old != blip.get(q('r:embed')) and not any(old in e.attrib.values() for e in slide._element.iter()):
        slide.part.drop_rel(old)                            # 이 장에서 더 쓰지 않는 예전 그림과의 관계는 지움


def patch_cover(cover):
    """표지: 영상을 v9로, 포스터도 그 첫 장으로. 제목과 아이콘을 COVER_PT에 맞춰 줄인다(왼쪽 끝과 세로 가운데는 그대로)."""
    media = {r.target_part for r in cover.part.rels.values() if r.reltype.endswith(('/video', '/media'))}
    assert len(media) == 1, len(media)
    media.pop()._blob = COVER_MP4.read_bytes()
    repoint(cover, by_name(cover, 'Cover loop video'), COVER_JPG)
    ms = round(HW.video_len(COVER_MP4) * 1000)
    for c in cover._element.iter(q('p:cmd')):
        c.find(q('p:cBhvr')).find(q('p:cTn')).set('dur', str(ms))
    title = by_name(cover, '!!cover/title')
    k = COVER_PT / (int(next(title.iter('{%s}rPr' % A)).get('sz')) / 100)
    mark, icon = by_name(cover, '!!cover/mark'), by_name(cover, '!!cover/mark_icon')
    mx, my, mw, mh = box(mark)
    ix, iy, iw, ih = box(icon)
    tx = box(title)[0]
    cy = my + mh / 2
    place(mark, mx, cy - mh * k / 2, mw * k, mh * k)
    place(icon, mx + (mw - iw) * k / 2, cy - ih * k / 2, iw * k, ih * k)
    place(title, x=mx + (tx - mx) * k)
    for rp in title.iter('{%s}rPr' % A, '{%s}endParaRPr' % A):
        if rp.get('sz'):
            rp.set('sz', str(round(COVER_PT * 100)))
    patch_cover_names(cover)


COVER_NAMES = ['n00', 'n01', 'n11', 'n10', 'n20']           # 놓는 차례: 이재웅, 양서윤, 이지현, 장이준, 조성빈 (11-17: 장이준과 이지현의 순서를 바꿈. 도형 n10 = 장이준, n11 = 이지현)
COVER_NAME_Y = 616                                         # 이름 한 줄의 위 끝(px). 소속 두 줄이 있을 때 맨 아래 줄의 아래 끝(640)에 이름의 아래 끝을 맞춤


def patch_cover_names(cover):
    """11차(11-16) '첫 번째 장표에 소속 빼 줘': 이름 아래의 가는 줄과 소속 두 줄(Samsung Research / AI System Team 등)을 지우고,
    소속별로 묶여 있던 이름 다섯을 같은 간격(묶음 안에서 쓰던 간격)의 한 줄로 놓는다."""
    for i in range(3):
        for part in ('line', 'dept', 'team'):
            el = by_name(cover, '!!cover/%s%d' % (part, i))
            el.getparent().remove(el)
    x0 = box(by_name(cover, '!!cover/n00'))[0]
    step = box(by_name(cover, '!!cover/n01'))[0] - x0
    for i, n in enumerate(COVER_NAMES):
        place(by_name(cover, '!!cover/' + n), x=x0 + i * step, y=COVER_NAME_Y)


def patch_mg(mg):
    """모션그래픽 장: 중간본에 든 영상을 지금 것(MG_MP4)으로 바꿔 끼운다. 길이와 소리가 같아 재생 설정은 그대로 둔다."""
    media = {r.target_part for r in mg.part.rels.values() if r.reltype.endswith(('/video', '/media'))}
    assert len(media) == 1, len(media)
    media.pop()._blob = MG_MP4.read_bytes()


def patch_bubbles(key, sl):
    """3~5쪽: 제목('기억이 나지 않는 막막한 순간들')을 빼고 그 자리까지 옅은 기록 조각을 흩어 둠. 첫 말풍선의 글, 말풍선 자리와 꼬리도 바꿈."""
    title = by_name(sl, '!!title')
    title.getparent().remove(title)
    runs = list(by_name(sl, '!!b1/body').iter('{%s}r' % A))
    assert [r.find('{%s}t' % A).text for r in runs] == ['그게 ', '어디에', ' 있더라?'], [r.find('{%s}t' % A).text for r in runs]
    runs[0].getparent().remove(runs[0])                     # '그게 어디에 있더라?' → '어디에 적어 놨더라?'
    runs[2].find('{%s}t' % A).text = ' 적어 놨더라?'
    for b in ('b2', 'b3'):
        if not has(sl, '!!' + b):
            continue
        bx, _, bw, _ = box(by_name(sl, '!!%s/body' % b))
        for dot, cx in zip(('dot1', 'dot2'), BUBBLE_TAIL[b](bw)):
            d = by_name(sl, '!!%s/%s' % (b, dot))
            place(d, x=bx + cx - box(d)[2] / 2)
        shift(by_name(sl, '!!' + b), dx=BUBBLE_DX.get(key, {}).get(b, 0))
    pa = painter(sl)
    x, y, w, h = FLOATS_BOX
    pa.put('floats', [P('floats', str(INTRO_AS / 'floats.png'), x, y, w, h)])
    fl = pa.tree[-1]
    pa.tree.remove(fl)
    by_name(sl, 'Background · lavender').addnext(fl)        # 배경 바로 위, 인물·말풍선 아래


def patch_ai(sl):
    """10쪽: AI 표시를 글꼴의 ✦ 글자 대신 벡터 도형으로(솔루션 장의 '요약', '자동 완성 추천' 옆 표시와 같은 모양). 글꼴이 없는 컴퓨터에서도 같은 모양."""
    pa = painter(sl)
    icon = by_name(sl, 'AI icon')
    ts = list(icon.iter('{%s}t' % A))
    assert [t.text for t in ts] == ['✦'], [t.text for t in ts]
    ts[0].text = ''
    x, y, w, h = box(icon)
    icon.addnext(pa.el(N.spark_icon('ai/spark', x + w / 2 - 12.5, y + h / 2 - 11.5, size=25, color='FFFFFF')[0]))
    lab = by_name(sl, 'Answer label')
    ts = list(lab.iter('{%s}t' % A))
    assert [t.text for t in ts] == ['✦ AI 답변'], [t.text for t in ts]
    ts[0].text = 'AI 답변'
    x, y, w, h = box(lab)
    lab.addnext(pa.el(N.spark_icon('ai/spark2', x - 1, y + h / 2 - 8, size=16, color=N.PURPLE)[0]))
    shift(lab, dx=18)


def patch_intro(slides, note_tpl):
    """옮겨 온 인트로 장을 손본다: 노트(새 대본), 화면 글, 7·8쪽 고리 굵기, 3~5쪽 말풍선과 기록 조각, 10쪽 AI 표시, 13쪽 흐린 배경, 삼성노트 아이콘.
    slides = {키: 장}."""
    for key, sl in slides.items():
        F.set_notes(sl, N.INTRO_NOTES[key], note_tpl)
        for old, new in INTRO_TEXT.get(key, []):
            hit = [e for e in sl._element.iter('{%s}t' % A) if e.text == old]
            assert len(hit) == 1, (key, old, len(hit))
            hit[0].text = new
        if key in ('in07', 'in08'):
            n = 0
            for g in sl._element.iter('{%s}prstGeom' % A):
                if g.get('prst') in ('donut', 'blockArc'):
                    for gd in g.iter('{%s}gd' % A):
                        if gd.get('name') in ('adj', 'adj3') and gd.get('fmla') == 'val ' + RING_ADJ[0]:
                            gd.set('fmla', 'val ' + RING_ADJ[1])
                            n += 1
            assert n >= 2, (key, n)
        if key in ('in03', 'in04', 'in05'):
            patch_bubbles(key, sl)
        if key == 'in09':
            patch_ai(sl)
        if key == 'in12':                                   # 흐린 배경: 12쪽의 마지막 모습(기록이 이어진 모습)을 흐리게 한 그림
            f = INTRO_AS / 'blur_link.jpg'
            if f.exists():
                repoint(sl, by_name(sl, '!!blur8'), f)
            else:
                print('   ! assets/intro/blur_link.jpg 없음 → 13쪽 배경은 예전 그림 그대로 (make.py --png 뒤 tools/intro_assets.py --blur)')
        for pic in sl._element.iter(q('p:pic')):            # 삼성노트 아이콘
            rid = pic.find('.//{%s}blip' % A).get(q('r:embed'))
            if hashlib.sha1(sl.part.related_part(rid).blob).hexdigest().startswith(NOTE_OLD_SHA1):
                repoint(sl, pic, N.ICON['note'])


# 11-12 밤: 덱 전체에서 '이름이' → '정확한 이름이'(설문 6번의 말 '정확한 이름이 떠오르지 않아'와 같게).
# 옮겨 온 4·5쪽은 둘째 말풍선(b2) '그 이름이 뭐였지?' → '정확한 이름이 뭐였지?', 4쪽 노트는 slides_new.INTRO_NOTES
ASK2_OLD, ASK2_HEAD = '그 이름이 뭐였지?', ('그 ', '정확한 ')         # 말풍선의 글, 바꾸는 첫 토막
ASK2_KEYS = ('in04', 'in05')
NOTE_FIX = [(ASK2_OLD, ASK2_HEAD[1] + ASK2_OLD[len(ASK2_HEAD[0]):]),          # 옮겨 온 덱의 노트에서 우리가 바꾼 곳(견줄 때 먼저 바꿔 놓음)
            ('둘째, 이름이 떠오르지', '둘째, 정확한 이름이 떠오르지')]


def patch_ask2(sl):
    """둘째 말풍선(b2)의 첫 토막을 바꾸고, 글이 늘어난 만큼 말풍선을 양옆으로 넓힌다(가운데와 꼬리는 그대로)."""
    body = by_name(sl, '!!b2/body')
    runs = list(body.iter('{%s}r' % A))
    ts = [r.find('{%s}t' % A) for r in runs]
    assert ''.join(t.text for t in ts) == ASK2_OLD and ts[0].text == ASK2_HEAD[0], [t.text for t in ts]
    pt = int(runs[0].find('{%s}rPr' % A).get('sz')) / 100
    d = N.tw(ASK2_HEAD[1], pt, 'b') - N.tw(ASK2_HEAD[0], pt, 'b')
    ts[0].text = ASK2_HEAD[1]
    x, _, w, _ = box(body)
    place(body, x=x - d / 2, w=w + d)
    gx = by_name(sl, '!!b2').find(q('p:grpSpPr')).find('{%s}xfrm' % A)       # 묶음의 상자와 자식 좌표계도 같은 만큼(배율 1 그대로)
    for o, e in (('off', 'ext'), ('chOff', 'chExt')):
        off, ext = gx.find('{%s}%s' % (A, o)), gx.find('{%s}%s' % (A, e))
        off.set('x', str(int(off.get('x')) - round(d / 2 * 9525)))
        ext.set('cx', str(int(ext.get('cx')) + round(d * 9525)))


# ------------------------------------------------------------------ 6차(11-13): 옮겨 온 인트로 장에서 더 손보는 곳
P_NS = F.NS['p']
FLOAT_LAYERS = (('a', 7, -11, 4000), ('b', -6, 10, 4800), ('c', 5, 11, 3400))      # 층, 떠 가는 만큼(x, y px), 한쪽으로 가는 데 걸리는 시간(ms)
GROUP_XML = ('<p:par xmlns:p="%s"><p:cTn id="%%d" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0">'
             '<p:tn val="%%s"/></p:cond></p:stCondLst><p:childTnLst><p:par><p:cTn id="%%d" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst>'
             '<p:childTnLst/></p:cTn></p:par></p:childTnLst></p:cTn></p:par>') % P_NS
DRIFT_XML = ('<p:par xmlns:p="%s"><p:cTn id="%%d" presetID="0" presetClass="path" presetSubtype="0" repeatCount="indefinite" autoRev="1" '
             'accel="50000" decel="50000" fill="hold" nodeType="%%s"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
             '<p:animMotion origin="layout" path="M 0 0 L %%.5f %%.5f E" pathEditMode="relative" rAng="0" ptsTypes="">'
             '<p:cBhvr><p:cTn id="%%d" dur="%%d" fill="hold"/><p:tgtEl><p:spTgt spid="%%d"/></p:tgtEl>'
             '<p:attrNameLst><p:attrName>ppt_x</p:attrName><p:attrName>ppt_y</p:attrName></p:attrNameLst></p:cBhvr>'
             '<p:rCtr x="0" y="0"/></p:animMotion></p:childTnLst></p:cTn></p:par>') % P_NS


def patch_person_click(sl):
    """3쪽: 장이 열리면 저절로 뜨던 인물과 말풍선을 클릭해야 뜨게 한다(그 전에는 떠다니는 기록 조각만 보임).
    저절로 시작하던 묶음을 클릭 묶음으로 바꾸고, 첫 효과가 클릭하자마자 시작하게 앞의 틈을 없앤다."""
    (g, auto), = F.groups(sl)
    assert auto
    ct = g.find(q('p:cTn'))
    for c in ct.find(q('p:stCondLst')).findall(q('p:cond')):
        if c.get('evt') == 'onBegin':
            c.getparent().remove(c)
    effs = [e for e in ct.iter(q('p:cTn')) if e.get('presetID')]
    d0 = F._delay(effs[0])
    for e in effs:
        e.find(q('p:stCondLst')).find(q('p:cond')).set('delay', str(F._delay(e) - d0))
    effs[0].set('nodeType', 'clickEffect')


def patch_floats(sl):
    """3~5쪽: 옅은 기록 조각 한 장(!!floats)을 세 층으로 나눠 끼우고(assets/intro/floats-a·b·c.png), 층마다 다른 쪽으로 천천히 갔다가 되돌아오기를
    되풀이하게 한다(장이 열리면 저절로, 장이 넘어갈 때까지). 세 장의 층 이름이 같아 장이 넘어가도 이어진다."""
    old = by_name(sl, '!!floats')
    x, y, w, h = box(old)
    pa = painter(sl)
    prev, spids = old, []
    for n, *_ in FLOAT_LAYERS:
        el = pa.el(P('floats/' + n, str(INTRO_AS / ('floats-%s.png' % n)), x, y, w, h))
        prev.addnext(el)
        prev = el
        spids.append(int(el.find(q('p:nvPicPr')).find(q('p:cNvPr')).get('id')))
    rid = old.find('.//{%s}blip' % A).get(q('r:embed'))
    old.getparent().remove(old)
    if not any(rid in e.attrib.values() for e in sl._element.iter()):
        sl.part.drop_rel(rid)
    assert all(abs(a - b) < 1 for a, b in zip((x, y, w, h), FLOAT_BOX)), (x, y, w, h)      # 2쪽에 까는 자리(patch_hook_floats)와 같은지
    float_drift(sl, spids)


FLOAT_BOX = (0, 16, 1280, 236)                        # 3~5쪽의 옅은 기록 조각이 놓인 자리(옮겨 온 장의 '!!floats')


def patch_hook_floats(sl):
    """2쪽(14차 뒤, '그 음성 나올 때 배경은 그 다음 페이지 배경을 그대로 가야 할 거 같아'): 3쪽이 열릴 때의 배경과 같게 옅은 기록 조각 세 층을
    같은 자리에 깔고 같은 식으로 떠다니게 한다. 바탕의 위, 글의 아래. 층의 이름과 그림이 3쪽과 같다."""
    pa = painter(sl)
    prev, spids = by_name(sl, 'Background · lavender'), []
    for n, *_ in FLOAT_LAYERS:
        el = pa.el(P('floats/' + n, str(INTRO_AS / ('floats-%s.png' % n)), *FLOAT_BOX))
        prev.addnext(el)
        prev = el
        spids.append(int(el.find(q('p:nvPicPr')).find(q('p:cNvPr')).get('id')))
    float_drift(sl, spids)


def float_drift(sl, spids):
    """옅은 기록 조각의 층마다 다른 쪽으로 천천히 갔다가 되돌아오기를 되풀이하는 효과를 건다(장이 열리면 저절로)."""
    ids = itertools.count(F._next_id(sl))
    auto = next((g for g, a in F.groups(sl) if a), None)
    if auto is None:                                        # 저절로 시작하는 묶음이 없으면(3쪽) 맨 앞에 만든다
        main = sl._element.find('.//' + q('p:cTn') + '[@nodeType="mainSeq"]')
        auto = etree.fromstring(GROUP_XML % (next(ids), main.get('id'), next(ids)))
        main.find(q('p:childTnLst')).insert(0, auto)
    inner = auto.find(q('p:cTn')).find(q('p:childTnLst'))[0].find(q('p:cTn')).find(q('p:childTnLst'))
    for (n, dx, dy, ms), spid in zip(FLOAT_LAYERS, spids):
        node = 'withEffect' if len(inner) else 'afterEffect'
        inner.append(etree.fromstring(DRIFT_XML % (next(ids), node, dx / 1280, dy / 720, next(ids), ms, spid)))


HEAD7 = ('원하는 정보를 한 번에 찾지 못한 경험', '정확한 이름이 떠오르지 않아 검색으로 찾지 못한 경험')      # 7쪽 머리글: 설문 6번의 말 그대로(33쪽과 같은 숫자, 같은 말)


def patch_heading7(sl):
    hit = [e for e in by_name(sl, '!!stat1/heading').iter('{%s}t' % A) if e.text == HEAD7[0]]
    assert len(hit) == 1, len(hit)
    hit[0].text = HEAD7[1]


Q7_OLD = '지은이네 집들이 때 마셨던 와인'


def patch_query7(sl):
    """11차(11-16): 7쪽 검색 칸의 검색어를 6쪽과 같은 글(slides_new.HK_QUERY)로 바꾸고, 글이 길어진 만큼 칸을 넓힌다.
    칸의 가운데는 그대로 두고(위의 숫자와 가운데가 같음) 오른쪽의 '일치하는 결과가 없습니다'는 검색어와의 틈을 그대로 둔 채 옮긴다."""
    qs = by_name(sl, 'Mini query')
    hit = [r for r in qs.iter('{%s}r' % A) if r.find('{%s}t' % A).text == Q7_OLD]
    assert len(hit) == 1, len(hit)
    rp = hit[0].find('{%s}rPr' % A)
    assert rp.find('{%s}latin' % A).get('typeface').endswith('700')
    pt = int(rp.get('sz')) / 100
    d = N.tw(N.HK_QUERY, pt, 'b') - N.tw(Q7_OLD, pt, 'b')
    hit[0].find('{%s}t' % A).text = N.HK_QUERY
    for name in ('Mini query', 'Mini search'):
        el = by_name(sl, name)
        place(el, w=box(el)[2] + d)
    for name in ('Mini none', 'Mini none dot', 'Mini none text'):
        shift(by_name(sl, name), dx=d)
    gx = by_name(sl, '!!stat1/search').find(q('p:grpSpPr')).find('{%s}xfrm' % A)       # 묶음의 상자와 자식 좌표계도 같은 만큼(배율 1 그대로)
    off = gx.find('{%s}off' % A)
    off.set('x', str(int(off.get('x')) - round(d / 2 * 9525)))
    for e in ('ext', 'chExt'):
        ext = gx.find('{%s}%s' % (A, e))
        ext.set('cx', str(int(ext.get('cx')) + round(d * 9525)))


# 11차(11-16) '텍스트 크기 반 단계 정도만 크게 (10, 11, 14, 28, 32p)': 옮겨 온 10, 11, 14쪽의 큰 글. {장: (도형, 지금 크기, 새 크기(1/100pt))}
# 33 → 35pt, 40 → 42pt(PowerPoint의 글자 크기 단계 32 → 36, 40 → 44의 절반). 28쪽과 32쪽은 How it Works 쪽의 CAP_BIG(30 → 32pt)
CAP_UP = {'in09': ('!!cap8/1', 3300, 3500), 'scat': ('!!cap8/2', 3300, 3500), 'in12': ('!!q8', 4000, 4200)}


def patch_cap_size(key):
    """그 장의 큰 글을 CAP_UP의 크기로. 줄 간격도 같은 비율로 늘리고, 늘어난 높이의 절반만큼 위로 올려 글의 세로 가운데를 그대로 둔다."""
    def fn(sl):
        name, a, b = CAP_UP[key]
        el = by_name(sl, name)
        rps = [rp for rp in el.iter('{%s}rPr' % A, '{%s}endParaRPr' % A) if rp.get('sz')]
        assert rps and all(rp.get('sz') == str(a) for rp in rps), (key, [rp.get('sz') for rp in rps])
        for rp in rps:
            rp.set('sz', str(b))
        grown = 0
        for ls in el.iter('{%s}lnSpc' % A):
            sp = ls.find('{%s}spcPts' % A)
            old = int(sp.get('val'))
            new = round(old * b / a)
            sp.set('val', str(new))
            grown += (new - old) / 100 * 4 / 3
        shift(el, dy=-grown / 2)
    return fn


HUB_PT = {'p': (1550, 1800), 'n': (1200, 1300)}       # 9쪽: 퍼센트와 그 아래 이름의 글자 크기(1/100pt). 지금 → 6차(퍼센트는 한 단계, 이름은 반 단계)


def patch_hub(sl):
    for i in range(7):
        for part, (a, b) in HUB_PT.items():
            rps = list(by_name(sl, '!!hub2/l%d/%s' % (i, part)).iter('{%s}rPr' % A, '{%s}endParaRPr' % A))
            assert rps and all(rp.get('sz') == str(a) for rp in rps), (i, part, [rp.get('sz') for rp in rps])
            for rp in rps:
                rp.set('sz', str(b))


# 10쪽 AI 답변: 세 줄. 묶음을 키워도 글자 크기는 그대로임(묶음의 배율 1.25는 자리와 크기에만 듦).
# 6차: 가장 긴 첫 줄이 말풍선 오른쪽 끝에 거의 닿는 크기(17pt, 오른쪽 여백 7px).
# 8차(11-13): 글자를 한 단계 작게(17 → 16pt) 하고, 말풍선의 왼쪽, 오른쪽, 위, 아래 여백이 같아지게 말풍선 크기와 글 자리를 다시 잡음.
#   여백은 말풍선 가장자리에서 글자(잉크)까지 ANS_PAD px: 왼쪽은 이름표의 별과 본문 첫 글자, 오른쪽은 가장 긴 첫 줄의 끝, 위는 이름표, 아래는 셋째 줄.
# (글, 보라 굵게인가)
ANSWER = [[('임베딩 모델은 텍스트, 이미지, 오디오 같은 복잡한', 0)],
          [('데이터를 컴퓨터가 이해할 수 있도록 고차원의', 0)],
          [('숫자 배열(벡터)', 1), ('로 변환하는 모델입니다.', 0)]]
# 12차(11-16 밤) '글자 크기가 커지면서 박스 여백이 부족(글자 반 단계 정도만 줄이자, 하단 여백 좀만 더 주려고)': 글자를 반 단계 작게(16 → 15pt).
#   말풍선의 높이는 그대로 두어 줄어든 글의 높이(5.35px)가 모두 아래 여백으로 감(20 → 25.35px). 왼쪽, 오른쪽, 위 여백은 20px 그대로라 폭은 25px 줄어듦
ANSWER_PT, ANSWER_LN = 1500, 130000                   # 글자 크기(1/100pt), 줄 간격(1/1000 %)
ANS_PAD = 20                                          # 말풍선 가장자리에서 글자까지(px, 1280×720 기준): 왼쪽, 오른쪽, 위
ANS_PAD_B = 25.35                                     # 아래 여백(px)
# PowerPoint로 찍어 잰 값(16pt): 본문 잉크 폭 401.6, 높이 85.6, 이름표 잉크 높이 13.6, 이름표와 본문 사이 24.0. 15pt는 그 15/16
ANS_INK = (401.6 * ANSWER_PT / 1600, 85.6 * ANSWER_PT / 1600)
ANS_BOX = (ANS_PAD + ANS_INK[0] + ANS_PAD, ANS_PAD + 13.6 + 24.0 + ANS_INK[1] + ANS_PAD_B)      # 말풍선의 폭과 높이(px): 416.5 × 163.2 (16pt 때는 441.6 × 163.2, 17pt 때는 455 × 161.25)
ANS_LABEL = (40.4, 14.4)                              # 이름표('AI 답변') 글상자의 왼쪽 위(말풍선 왼쪽 위에서, px). 별은 그 왼쪽에 함께 옮김: 잉크가 왼쪽 20, 위 20
ANS_TEXT = (20 - 0.5 * ANSWER_PT / 1600, 57.6 - 8.2 * ANSWER_PT / 1600)      # 본문 글상자의 왼쪽 위(px): 잉크가 왼쪽 20, 위 57.6 (16pt 때 19.5, 49.4)


def patch_answer(sl):
    """10쪽: AI 답변의 글을 바꾸고(문단 셋의 틀은 그대로 두고 글 토막만 새로 넣음) 말풍선 크기와 글 자리를 다시 잡는다(ANS_*)."""
    body = by_name(sl, 'Answer text').find(q('p:txBody'))
    paras = body.findall('{%s}p' % A)
    assert len(paras) == len(ANSWER), len(paras)
    plain = copy.deepcopy(paras[0].findall('{%s}r' % A)[0])           # 보통 글 토막의 틀
    bold = copy.deepcopy(paras[0].findall('{%s}r' % A)[1])            # 보라 굵은 글 토막의 틀
    assert plain.find('{%s}rPr' % A).find('{%s}latin' % A).get('typeface').endswith('400')
    assert bold.find('{%s}rPr' % A).find('{%s}latin' % A).get('typeface').endswith('700')
    for p, runs in zip(paras, ANSWER):
        for r in p.findall('{%s}r' % A):
            p.remove(r)
        p.find('{%s}pPr' % A).find('{%s}lnSpc' % A).find('{%s}spcPct' % A).set('val', str(ANSWER_LN))
        end = p.find('{%s}endParaRPr' % A)
        for text, hl in runs:
            r = copy.deepcopy(bold if hl else plain)
            r.find('{%s}rPr' % A).set('sz', str(ANSWER_PT))
            r.find('{%s}t' % A).text = text
            if end is not None:
                end.addprevious(r)
            else:
                p.append(r)
        if end is not None:
            end.set('sz', str(ANSWER_PT))
    # 말풍선과 그 안의 자리. 묶음(!!ai/ans)의 자식 좌표는 배율 k(= 1.25)로 화면에 놓이므로 px를 k로 나눠 넣고, 묶음의 상자와 자식 좌표계도 말풍선에 맞춤
    grp = by_name(sl, '!!ai/ans')
    gx = grp.find(q('p:grpSpPr')).find('{%s}xfrm' % A)
    off, ext, cho, che = (gx.find('{%s}%s' % (A, t)) for t in ('off', 'ext', 'chOff', 'chExt'))
    k = int(ext.get('cx')) / int(che.get('cx'))
    bub, lab, spark, txt = (by_name(sl, n) for n in ('Answer bubble', 'Answer label', '!!ai/spark2', 'Answer text'))
    bx, by_, _, _ = box(bub)
    assert abs(bx - int(cho.get('x')) / 9525) < 0.01 and abs(by_ - int(cho.get('y')) / 9525) < 0.01      # 말풍선이 묶음의 왼쪽 위
    w, h = ANS_BOX[0] / k, ANS_BOX[1] / k
    place(bub, w=w, h=h)
    sx, _, _, _ = box(spark)
    lx0, ly0, _, _ = box(lab)
    lx, ly = bx + ANS_LABEL[0] / k, by_ + ANS_LABEL[1] / k
    shift(spark, dx=lx - lx0, dy=ly - ly0)                # 별은 이름표와 함께
    place(lab, x=lx, y=ly)
    place(txt, x=bx + ANS_TEXT[0] / k, y=by_ + ANS_TEXT[1] / k, w=(ANS_BOX[0] - ANS_TEXT[0] - 4) / k)
    ext.set('cx', str(round(ANS_BOX[0] * 9525)))
    ext.set('cy', str(round(ANS_BOX[1] * 9525)))
    che.set('cx', str(round(w * 9525)))
    che.set('cy', str(round(h * 9525)))


# 7차(11-13): 3~5쪽 인물 뒤에 아주 옅은 보라 그라데이션. 인물의 윤곽을 크게 흐린 그림(assets/intro/aura-N.png, tools/intro_assets.py --aura)을
# 모든 인물보다 아래 층에 깐다. 처음에는 그림의 빛 효과(윤곽을 따라 50pt 번짐)를 썼는데 '그라데이션이 아니라 테두리, 띠 같다'는 검토를 받아 바꿈:
# 흐린 윤곽은 몸 안쪽에서 가장 진하고 바깥으로 고르게 옅어져 띠가 생기지 않는다. 인물이 뜨는 장에서는 같은 효과로 함께 뜨고, 이름이 같아 Morph로 함께 옮겨 간다.
AURA_PAD = 170                                        # 그라데이션 그림이 인물 그림보다 왼쪽, 오른쪽, 위로 넓은 만큼(px). tools/intro_assets.py의 AURA_PAD와 같아야 함


def patch_aura(sl):
    pa = painter(sl)
    ids = itertools.count(F._next_id(sl))
    first = by_name(sl, '!!p1')
    for n in ('1', '2', '3'):
        if not has(sl, '!!p' + n):
            continue
        pic = by_name(sl, '!!p' + n)
        x, y, w, h = box(pic)
        el = pa.el(P('aura' + n, str(INTRO_AS / ('aura-%s.png' % n)), x - AURA_PAD, y - AURA_PAD, w + 2 * AURA_PAD, h + AURA_PAD))
        first.addprevious(el)                               # 세 인물 모두의 아래(이웃 인물의 몸 위에 얹히지 않게)
        spid = el.find(q('p:nvPicPr')).find(q('p:cNvPr')).get('id')
        pid = pic.find(q('p:nvPicPr')).find(q('p:cNvPr')).get('id')
        for par in sl._element.iter(q('p:par')):            # 그 인물이 이 장에서 뜨는 효과가 있으면 그라데이션도 같은 효과로 함께
            ct = par.find(q('p:cTn'))
            if ct is None or not ct.get('presetID') or {t.get('spid') for t in par.iter(q('p:spTgt'))} != {pid}:
                continue
            twin = copy.deepcopy(par)
            for c in twin.iter(q('p:cTn')):
                c.set('id', str(next(ids)))
            for t in twin.iter(q('p:spTgt')):
                t.set('spid', spid)
            twin.find(q('p:cTn')).set('nodeType', 'withEffect')
            par.addnext(twin)
            break


# ------------------------------------------------------------------ 8차(11-13 낮): 12쪽을 둘로, 15쪽 로고의 자리
GATH_DX = -289                                        # 11쪽의 기록 그림('지금의 나'의 가운데 x 929)을 화면 가운데(640)로 옮기는 만큼(px)


def patch_gather(sl):
    """새 12쪽: 11쪽(scat)을 한 번 더 옮긴 장에서 왼쪽의 물음을 빼고, 흩어진 기록 그림을 기울기와 흩어진 모양 그대로 화면 가운데로 옮긴다.
    11쪽에서 넘어올 때는 Morph로 그림만 가운데로 미끄러져 오고(물음은 걷힘), 다음 장(link)으로 넘어갈 때는 예전 12쪽의 움직임 그대로
    기록이 반듯해지며 선으로 이어진다. 11쪽의 뜨는 효과는 이 장에서는 필요 없어 없앤다."""
    cap = by_name(sl, '!!cap8/2')
    cap.getparent().remove(cap)
    n = 0
    for el in list(live_tree(sl)):
        nv = el.find('.//' + q('p:cNvPr'))
        name = nv.get('name') if nv is not None else ''
        if name.startswith('!!bg/') or not name.startswith('!!'):
            continue
        shift(el, dx=GATH_DX)                                 # 묶음은 묶음의 상자만 옮기면 자식이 따라옴
        n += 1
    assert n == 17, n                                       # 옅은 앱 넷, 선 여덟(작게 숨어 있음), 기록 넷, '지금의 나'
    for t in sl._element.findall(q('p:timing')):
        sl._element.remove(t)


LOGO_DX = 12                                          # 15쪽 로고(아이콘과 Weave Assist)를 오른쪽으로 옮기는 만큼(px)


def patch_logo_center(sl):
    """15쪽(잇는 장): 로고 묶음을 조금 오른쪽으로. 묶음의 좌우 끝은 화면 한가운데에 있었지만(잉크의 가운데 x 644),
    짙은 아이콘이 왼쪽에 있고 글자는 오른쪽으로 갈수록 옅어져 왼쪽으로 치우쳐 보였다(잉크의 무게중심 x 593). 아래 실의 가운데(x 654)와도 맞춤."""
    for name in ('!!br/mark', '!!br/logo/logo_word'):
        shift(by_name(sl, name), dx=LOGO_DX)


# ------------------------------------------------------------------ 9차(11-15): 2쪽의 통화 음성
# 장이 열리면 통화 음성이 저절로 나오고, 화면의 문장은 음성의 마지막 말("잠깐만요, 찾아보고 다시 알려 드릴게요.")에 맞춰 한 줄씩 뜬다.
# 음성: 사용자가 ElevenLabs(Chaerin, Eleven v4)로 만든 목소리를 Carbon이 전화 음질로 다듬은 최종후보 B(클래식 전화 음질, 첫 정적 1.85초).
#   통화 연결음 한 번 → 수화기 드는 소리 → "네, 삼성리서치 양서윤 프로입니다." → (정적) → "어... 네.. 그거요...?" → "아... 잠깐만요, 찾아보고 다시 알려 드릴게요."
#   → 끊는 소리. 그 전에는 임시로 Carbon이 이 컴퓨터에서 합성한 후보 3(10.2초)을 넣어 두었음
# 다른 음성으로 바꾸려면 파일을 바꾸고 아래 값을 그 음성에 맞춘다(때는 기기 안의 받아쓰기로 낱말마다 잰 값)
# 11-15 '통화 부분 볼륨만 살짝 높여서, 지금은 잘 안 들리네': 받은 파일은 연결음이 크고(-13.9 LUFS) 목소리가 작아서(-21.9 LUFS. 낭독은 -16 LUFS)
#   연결음은 그대로 두고 그 뒤의 목소리만 6dB 키운 파일로 바꿈(tools/call_gain.py → -17.6 LUFS). 길이와 말하는 때는 그대로. 덱에서 트는 크기도 80% → 100%
#   그 뒤 '벨소리 살짝만 더 크게, 뚜루루 소리 약간 작은 듯' → 연결음도 3dB 키움(--ring 3, -13.6 → -10.6 LUFS)
#   그 뒤 '벨소리 약간만 더 키워 주고, 받을 때 딸깍(받는 소리)이 명확히 있고 딜레이 0.2초 정도 주고 말하는 게 자연스러울 것 같아',
#   '0.2초 더 주라는 거였는데? 그럼 총 0.7초 정도 되겠지' → 연결음 5.5dB(-8.1 LUFS), 받는 소리를 또렷한 '딸깍'(1.36~1.47초)으로 바꾸고
#   딸깍이 끝나고 첫마디 '네'까지를 0.43초 → 0.63초로(딸깍의 첫 소리부터는 0.74초). 그래서 첫마디와 그 뒤가 모두 0.43초 늦어지고 길이는 14.02초 → 14.45초
CALL_MP3 = INTRO_AS / 'call-hook.mp3'
#   11차(11-16) '두 번째 장 음성에서도 소속 빼 줘 … 아.. 네.. 음.. 만 말하고 속도 1.1~1.2배 정도로 빠르고 자연스럽게, 편집 힘들면 음성 수정 예정':
#   tools/call_edit.py로 '삼성리서치'와 '그거요...?'를 덜어 내고 목소리 구간을 1.15배 빠르게 한 뒤 같은 크기 조정을 거침(목소리 -17.8 LUFS).
#   "네, 양서윤 프로입니다." → "어... 네.." → "아... 잠깐만요, 찾아보고 다시 알려 드릴게요." 길이 14.45초 → 11.62초.
#   '안녕하세요'는 녹음에 없어 넣지 못함(새 음성을 받으면 파일과 아래 값만 바꿈). 10차의 파일은 out/이전판_10차/call-hook_10차.mp3
#   12차(11-16 밤) '음성 첨부한 파일로 바꾸고 1.15배속 하기(기존 효과도 해야 함. "프로입니다." 이후 딜레이라든지는 넣어야 하고)':
#   사용자가 ElevenLabs에서 새로 만든 목소리(Chaerin, Eleven v4, 10.5초)로 바꿈. "네, 양서윤 프로입니다." → (듣는 틈) → "아, 그거요?" → 한숨
#   → 작게 "어디 적어놨더라" → "음, 잠깐만요. 찾아보고 다시 알려 드릴게요." 새 파일에는 앞선 손질이 없어서 tools/call_build.py가 같은 값으로 다시 입힘:
#   1.15배, "프로입니다." 뒤의 쉼 1.56초(11차 파일에서 잰 값), 전화 음질, 목소리 -17.8 LUFS, 연결음, 딸깍, 딸깍 뒤 0.63초, 끊는 소리.
#   작게 말한 "어디 적어놨더라"는 받은 파일에서 다른 말보다 6.5dB 작았고 3dB를 더 낮춤('엄청 작게 하려고'). 길이 11.62초 → 12.78초.
#   처음에는 받은 파일의 9.90초에서 잘라 12.38초로 만들었는데, 그 뒤 9.98~10.33초의 여린 소리는 숨소리가 아니라 끝말 '게요'였다
#   ('"알려드"에서 끝나잖아!! 수정해') → 끝까지(--end 10.36) 살려 다시 만듦. 자른 파일은 받아쓰기로 끝말까지 확인할 것
#   11차의 파일은 out/이전판_11차/call-hook_11차.mp3
#   14차 뒤(11-17 밤) '이거를 먼저 넣고(통화음 같은 것은 유지) … (ppt도 교체)', 곧이어 '아 통화가 아니니까 통화 아이콘 같은 건 빼서 장표 구성해야 했다.
#   텍스트는 알맞게 나오도록': 사용자가 새로 만든 목소리(Chaerin, Eleven v4, 9.4초)는 통화가 아니라 혼자 찾는 말이다.
#   "그 자료... 어디에 있지?" → "메신저에도 없고" → "메일함에도 없는데?" → "다시 전화해 봐야 하나?"
#   tools/hook_build.py가 1.15배, 목소리 -17.8 LUFS로 만들고(8.40초) 통화 연결음, 받는 소리, 전화 음질, 끊는 소리는 넣지 않는다(HOOK_CALL = False).
#   화면에서는 '통화 중 00:00' 알약과 통화 시간을 빼고, 문장 두 줄 대신 말하는 네 구절(HOOK_QUOTE)이 말에 맞춰 차례로 뜬다.
#   처음에는 구절마다 한 줄씩 네 줄(46pt)이었고, 같은 밤에 '혼잣말 부분 장표 4줄 → 두 줄로, 폰트 필요하면 조금 작게'라는 말을 받아 두 줄(42pt)로 바꿈:
#   한 줄에 구절이 둘이고 구절마다 글상자가 따로라서(hook_pieces) 뜨는 때는 네 줄일 때와 같다.
#   통화음을 그대로 둔 판은 out/hook_통화음유지.mp3(덱에는 넣지 않음), 14차까지의 통화 음성은 out/이전판_14차/call-hook_14차.mp3
HOOK_CALL = False                                     # 2쪽의 음성이 통화인지(12~14차: True). False면 통화 표시(알약, 통화 시간)를 빼고 HOOK_QUOTE를 띄움
CALL_LEN = 8.40 if not HOOK_CALL else 12.78           # 음성의 길이(초)
CALL_AT = 0.3                                         # 장이 열린 뒤 음성이 시작하는 때(초)
CALL_PICK, CALL_HANG = 1.45, 12.34                    # (통화일 때만) 음성 안에서 전화를 받는 때(딸깍의 '깍')와 끊는 소리가 시작하는 때(초): 통화 시간 표시가 이 사이에 1초마다 올라감
# 화면의 문장 두 줄: (음성 안에서 그 줄의 첫 말을 시작하는 때(초), 한 글자씩 뜨는 간격(ms)).
#   첫 줄 “잠깐만요, 찾아보고: '잠깐만요' 10.71초, 조금 쉬고 '찾아보고' 11.71초. 둘째 줄 다시 알려 드릴게요.”: '다시' 12.37초, 말이 끝나는 때 13.43초
#   (받아쓰기로 잰 10.28초, 11.94초에 첫마디를 늦춘 0.43초를 더한 값)
#   11차: '잠깐만요' 8.27초, '다시' 9.72초, 말이 끝나는 때 10.85초(원본의 때를 덜어 낸 만큼 당기고 1.15로 나눈 값. 소리 크기로 다시 확인)
#   12차: '잠깐만요' 9.30초, '찾아보고' 10.30초, '다시' 10.98초, '드릴'까지 11.63초, 여리게 끄는 '게요'가 11.70~12.03초
#   (받은 파일에서 0.01초마다 잰 소리 크기로 낱말의 첫 소리를 잡아 옮긴 값).
#   간격은 낭독 영상에서 재서 맞춤: 줄마다 글자가 열 개(사이 아홉)이고 줄의 첫 글자는 말보다 0.12초 먼저 뜬다. 처음 넣은 150, 55ms로는 두 줄이 말보다
#   0.3~0.4초 먼저 다 떠서, 마지막 글자가 말의 끝(10.93초, 12.03초) 바로 앞에 뜨게 185, 120ms로(첫 줄은 '잠깐만요'와 '찾아보고'가 말하는 때에 맞게 뜸)
#   14차 뒤(혼잣말): 받은 파일에서 구절이 시작하는 때 0.20, 2.78, 4.76, 7.82초를 만든 파일의 때로 옮김(0.10 + (t - 0.09) / 1.15).
#   줄마다 글자 수(빈칸 빼고)는 13, 8, 11, 11이고 말이 끝나는 때는 1.81, 3.22, 5.34, 7.92초. 첫 줄은 '어디에'(여덟째 글자)가 1.03초의 말에 맞게
CALL_LINES = [(0.20, 120), (2.44, 100), (4.16, 110), (6.82, 100)] if not HOOK_CALL else [(9.30, 185), (10.98, 120)]
# 혼잣말일 때 화면에 뜨는 줄: (글, 색). 색은 옮겨 온 장의 두 줄(짙은 색, 보라)에서 가져옴
# 혼잣말일 때 화면에 뜨는 구절: (글, 색, 놓이는 줄). 색은 옮겨 온 장의 두 줄(짙은 색, 보라)에서 가져옴. 구절의 차례는 CALL_LINES의 차례와 같음
#   색(같은 밤): 처음에는 마지막 구절 '다시 전화해 봐야 하나?'가 보라였고, "'그 자료 어디에 있지?'를 보라색으로"라는 말을 받아 첫 구절만 보라, 나머지는 짙은 색으로
HOOK_QUOTE = [('“그 자료... 어디에 있지?', 'purple', 0), ('메신저에도 없고,', 'dark', 0), ('메일함에도 없는데...', 'dark', 1), ('다시 전화해 봐야 하나?”', 'dark', 1)]
HOOK_PT, HOOK_LNPT = 42, 58                           # 글자 크기와 줄 간격(pt). 옮겨 온 글상자는 46pt에 64pt: 두 줄로 놓으면 둘째 줄이 1,079px(화면의 84%)라 42pt로(983px)
HOOK_SPC = -0.7                                       # 글자 사이(pt. 옮겨 온 글상자의 spc="-70")
HOOK_FONT = Path.home() / '.cache' / 'weave-tools' / 'fonts' / 'SamsungOneKorean-700.ttf'       # 구절의 나비를 잴 글꼴 파일(덱의 글꼴과 같음)


def hook_width(text):
    """구절의 나비(px): 글자 나비의 합 + 글자 사이. 네 줄일 때의 가장 긴 줄(46pt)이 계산 567px, PowerPoint 그림에서 잰 값 565px."""
    from PIL import ImageFont
    px = HOOK_PT * 4 / 3
    return ImageFont.truetype(str(HOOK_FONT), 1000).getlength(text) / 1000 * px + HOOK_SPC * 4 / 3 * len(text)
MEDIA_URI = '{DAA4B4D4-6D71-4841-9C94-3DE7FCFB9230}'
P14 = 'http://schemas.microsoft.com/office/powerpoint/2010/main'


def patch_call(sl):
    """2쪽: 통화 음성을 넣는다. 소리는 화면 밖 왼쪽 위의 전화 아이콘에 달려 있고 장이 열리면 저절로 재생된다(PowerPoint가 쓰는 모양 그대로:
    그림에 a:audioFile과 p14:media, 효과 나무에 재생 명령과 p:audio). 문장이 뜨는 효과는 음성의 마지막 말에 맞춰 한 줄씩 건다(CALL_LINES)."""
    from pptx.media import Video
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    pa = painter(sl)
    el = pa.el(P('callsound', HW.ICON['phone'], -64, 24, 40, 40))
    live_tree(sl).append(el)
    part = sl.part.package.get_or_add_media_part(Video.from_path_or_file_like(str(CALL_MP3), 'audio/mpeg'))
    media_rid, audio_rid = sl.part.relate_to(part, RT.MEDIA), sl.part.relate_to(part, RT.AUDIO)
    nv = el.find(q('p:nvPicPr'))
    c = nv.find(q('p:cNvPr'))
    spid = c.get('id')
    link = etree.Element('{%s}hlinkClick' % A)
    link.set(q('r:id'), '')
    link.set('action', 'ppaction://media')
    c.insert(0, link)
    nvpr = nv.find(q('p:nvPr'))
    etree.SubElement(nvpr, '{%s}audioFile' % A).set(q('r:link'), audio_rid)
    ext = etree.SubElement(etree.SubElement(nvpr, q('p:extLst')), q('p:ext'))
    ext.set('uri', MEDIA_URI)
    etree.SubElement(ext, '{%s}media' % P14, nsmap={'p14': P14}).set(q('r:embed'), media_rid)
    tm = sl._element.find(q('p:timing'))
    cts = list(tm.iter(q('p:cTn')))
    ids = itertools.count(max(int(e.get('id')) for e in cts) + 1)
    root = next(e for e in cts if e.get('nodeType') == 'tmRoot')
    first = next(g for g, auto in F.groups(sl) if auto)
    inner = first.find(q('p:cTn')).find(q('p:childTnLst'))[0].find(q('p:cTn'))       # 첫 묶음의 첫 안쪽 묶음(통화 중 표시가 뜨는 곳)
    par = etree.SubElement(inner.find(q('p:childTnLst')), q('p:par'))
    ct = etree.SubElement(par, q('p:cTn'), id=str(next(ids)), presetID='1', presetClass='mediacall', presetSubtype='0', fill='hold', nodeType='withEffect')
    etree.SubElement(etree.SubElement(ct, q('p:stCondLst')), q('p:cond'), delay=str(round(CALL_AT * 1000)))
    cmd = etree.SubElement(etree.SubElement(ct, q('p:childTnLst')), q('p:cmd'), type='call', cmd='playFrom(0.0)')
    cb = etree.SubElement(cmd, q('p:cBhvr'))
    etree.SubElement(cb, q('p:cTn'), id=str(next(ids)), dur=str(round(CALL_LEN * 1000)), fill='hold')
    etree.SubElement(etree.SubElement(cb, q('p:tgtEl')), q('p:spTgt'), spid=spid)
    node = etree.SubElement(etree.SubElement(root.find(q('p:childTnLst')), q('p:audio')), q('p:cMediaNode'), vol='100000', showWhenStopped='0')
    at = etree.SubElement(node, q('p:cTn'), id=str(next(ids)), fill='hold', display='0')
    etree.SubElement(etree.SubElement(at, q('p:stCondLst')), q('p:cond'), delay='indefinite')
    stop = etree.SubElement(etree.SubElement(at, q('p:endCondLst')), q('p:cond'), evt='onStopAudio', delay='0')
    etree.SubElement(etree.SubElement(stop, q('p:tgtEl')), q('p:sldTgt'))
    etree.SubElement(etree.SubElement(node, q('p:tgtEl')), q('p:spTgt'), spid=spid)
    if not HOOK_CALL:
        hook_plain(sl, tm)
    qid = by_name(sl, '!!quote').find(q('p:nvSpPr')).find(q('p:cNvPr')).get('id')
    # 문장이 한 글자씩 뜨는 효과(글상자 전체에 하나)를 떼어 내, 줄(문단)마다 하나씩 음성과 같은 묶음에 '앞 효과와 함께 + 지연'으로 다시 건다.
    # 원래 효과는 '앞 효과 다음에' 묶음에 따로 들어 있어서, 그대로 두면 PowerPoint가 음성이 끝난 뒤에야 시작한다(시험: 지연 값을 바꿔도 음성이 끝난 뒤)
    eff = next((e for e in tm.iter(q('p:cTn')) if e.get('presetClass') == 'entr' and {t.get('spid') for t in e.iter(q('p:spTgt'))} == {qid}), None)
    assert eff is not None, '2쪽: 문장이 뜨는 효과를 못 찾음'
    par_eff = eff.getparent()
    holder = par_eff.getparent().getparent().getparent()            # 이 효과만 담고 있던 안쪽 묶음(p:par)
    par_eff.getparent().remove(par_eff)
    if not len(holder.find(q('p:cTn')).find(q('p:childTnLst'))):
        holder.getparent().remove(holder)
    spids = None if HOOK_CALL else hook_pieces(sl, pa)             # 혼잣말: 구절마다 글상자가 따로(한 줄에 둘), 통화: 한 글상자의 문단마다
    for i, (at_, gap) in enumerate(CALL_LINES):
        one = copy.deepcopy(par_eff)
        e = one.find(q('p:cTn'))
        e.set('nodeType', 'withEffect')
        e.find(q('p:stCondLst')).find(q('p:cond')).set('delay', str(round((CALL_AT + at_) * 1000 - 80)))
        for c in one.iter(q('p:cTn')):
            c.set('id', str(next(ids)))
        for it in one.iter(q('p:tmAbs')):
            it.set('val', str(gap))
        for t in one.iter(q('p:spTgt')):
            if spids:                                               # 이 구절의 글상자
                t.set('spid', spids[i])
            else:                                                   # 이 줄(문단)만
                rg = etree.SubElement(etree.SubElement(t, q('p:txEl')), q('p:pRg'))
                rg.set('st', str(i))
                rg.set('end', str(i))
        inner.find(q('p:childTnLst')).append(one)
    for b_ in list(tm.iter(q('p:bldP'))):
        if b_.get('spid') != qid:
            continue
        if spids:                                                   # 구절의 글상자마다 하나씩(옮겨 온 글상자의 표시를 본떠서)
            for s_ in spids:
                nb = copy.deepcopy(b_)
                nb.set('spid', s_)
                b_.addprevious(nb)
            b_.getparent().remove(b_)
        else:                                                       # 글상자를 문단마다 따로 띄운다는 표시
            b_.set('build', 'p')
            b_.attrib.pop('animBg', None)
    if HOOK_CALL:
        call_timer(sl, pa, tm, inner, ids)


def hook_plain(sl, tm):
    """2쪽(혼잣말): 통화 표시('통화 중 00:00' 알약)와 그 알약이 뜨는 효과를 뺀다. 문장은 hook_pieces가 구절마다 글상자로 다시 놓는다."""
    grp = by_name(sl, '!!call')
    gid = grp.find(q('p:nvGrpSpPr')).find(q('p:cNvPr')).get('id')
    for par in list(tm.iter(q('p:par'))):                           # 알약이 뜨는 효과(그 도형만 가리키는 가장 안쪽 묶음)
        c = par.find(q('p:cTn'))
        if c is not None and c.get('presetClass') and {x.get('spid') for x in par.iter(q('p:spTgt'))} == {gid}:
            par.getparent().remove(par)
    for b_ in list(tm.iter(q('p:bldP'))):
        if b_.get('spid') == gid:
            b_.getparent().remove(b_)
    grp.getparent().remove(grp)


def hook_pieces(sl, pa):
    """2쪽(혼잣말): 옮겨 온 문장 글상자를 본떠 구절마다 글상자를 하나씩 만들어 두 줄로 놓고(HOOK_QUOTE), 옮겨 온 글상자는 뺀다.
    한 줄의 구절들은 빈칸 하나를 사이에 두고 이어 놓아 한 문장처럼 보이게 하고, 줄마다 가로 가운데에 맞춘다. 돌려줌: 구절 글상자의 id(구절의 차례)."""
    src = by_name(sl, '!!quote')
    ps = src.find(q('p:txBody')).findall('{%s}p' % A)
    assert len(ps) == 2, len(ps)
    kind = {'dark': ps[0], 'purple': ps[1]}
    lh = HOOK_LNPT * 4 / 3
    nline = max(ln for _, _, ln in HOOK_QUOTE) + 1
    y0 = (720 - lh * nline) / 2
    space = hook_width(' ')
    spids, last = [], src
    for ln in range(nline):
        row = [(k, text, col) for k, (text, col, l_) in enumerate(HOOK_QUOTE) if l_ == ln]
        ws = [hook_width(text) for _, text, _ in row]
        x = (1280 - sum(ws) - space * (len(row) - 1)) / 2
        assert x >= 100, '2쪽: %d째 줄이 너무 김(%dpx)' % (ln + 1, 1280 - 2 * x)
        for (k, text, col), w in zip(row, ws):
            el = copy.deepcopy(src)
            spid = str(next(pa.ids))
            c = el.find(q('p:nvSpPr')).find(q('p:cNvPr'))
            c.set('id', spid)
            c.set('name', '!!quote %d' % (k + 1))
            body = el.find(q('p:txBody'))
            for p_ in body.findall('{%s}p' % A):
                body.remove(p_)
            one = copy.deepcopy(kind[col])
            one.find('{%s}pPr' % A).set('algn', 'l')
            for sp_ in one.iter('{%s}spcPts' % A):
                if sp_.getparent().tag.endswith('}lnSpc'):
                    sp_.set('val', str(HOOK_LNPT * 100))
            rs = list(one.iter('{%s}rPr' % A))
            ts = list(one.iter('{%s}t' % A))
            assert len(rs) == len(ts) == 1, (len(rs), len(ts))
            rs[0].set('sz', str(HOOK_PT * 100))
            ts[0].text = text
            body.append(one)
            place(el, x=x, y=y0 + ln * lh, w=w + 2, h=lh)
            last.addnext(el)
            last = el
            spids.append((k, spid))
            x += w + space
    src.getparent().remove(src)
    return [s_ for _, s_ in sorted(spids)]


TICK_XML = ('<p:par xmlns:p="%s"><p:cTn id="%%d" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" nodeType="withEffect">'
            '<p:stCondLst><p:cond delay="%%d"/></p:stCondLst><p:childTnLst><p:set><p:cBhvr><p:cTn id="%%d" dur="1" fill="hold">'
            '<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="%%d"/></p:tgtEl>'
            '<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
            '</p:childTnLst></p:cTn></p:par>') % P_NS
TICK_INSET = 6                                        # 숫자 글상자의 흰 바탕을 위아래로 줄이는 만큼(px): 알약 모양의 테두리를 가리지 않게


def call_timer(sl, pa, tm, inner, ids):
    """12차(11-16 밤) '통화 중 0초에서, 받으면 1, 2, 3.. 이런 식으로 애니메이션 필요(통화음에 맞춰서)':
    통화 시간 표시를 00:48로 멈춰 두지 않고 00:00에서 시작해, 전화를 받는 소리(CALL_PICK)부터 끊는 소리(CALL_HANG)까지 1초마다 올린다.
    묶음 안의 도형은 따로 움직일 수 없어서, 묶음 안의 글은 00:00으로 두고 그 위에 00:01, 00:02 …를 적은 글상자를 같은 자리에 차례로 겹쳐 놓는다.
    글상자마다 알약과 같은 흰 바탕이 있어 뜨는 순간 앞의 숫자를 가린다(사라지는 효과가 필요 없고, 편집 화면과 PNG에는 맨 위의 마지막 숫자만 보임)."""
    base = by_name(sl, 'Call time')
    ts = list(base.iter('{%s}t' % A))
    assert [t.text for t in ts] == ['00:48'], [t.text for t in ts]
    ts[0].text = '00:00'
    x, y, w, h = box(base)
    bl = tm.find(q('p:bldLst'))
    prev = by_name(sl, '!!call')
    for k in range(1, int(CALL_HANG - CALL_PICK) + 1):
        el = copy.deepcopy(base)
        spid = next(pa.ids)
        c = el.find(q('p:nvSpPr')).find(q('p:cNvPr'))
        c.set('id', str(spid))
        c.set('name', 'Call time %02d' % k)
        next(el.iter('{%s}t' % A)).text = '00:%02d' % k
        sp = el.find(q('p:spPr'))
        no = sp.find('{%s}noFill' % A)
        fill = etree.Element('{%s}solidFill' % A)
        etree.SubElement(fill, '{%s}srgbClr' % A, val='FFFFFF')
        sp.replace(no, fill)
        place(el, y=y + TICK_INSET, h=h - 2 * TICK_INSET)
        prev.addnext(el)                                    # 묶음 바로 위에, 숫자가 큰 것이 더 위에
        prev = el
        inner.find(q('p:childTnLst')).append(etree.fromstring(TICK_XML % (next(ids), round((CALL_AT + CALL_PICK + k) * 1000), next(ids), spid)))
        etree.SubElement(bl, q('p:bldP'), spid=str(spid), grpId='0', animBg='1')


# 옮겨 온 덱의 노트와 견주지 않는 장: 6차에 우리가 노트를 바꾼 장과, 8차에 발표자가 대본을 다시 쓴 장
NOTE_OURS = {'in02', 'in03', 'in04', 'in05', 'in07', 'in08', 'hub2', 'in09', 'scat', 'gath', 'link', 'bridge'}
INTRO_PATCH = {                                       # 옮겨 온 장마다 6차부터 더 손보는 일
    'in02': [patch_call, patch_hook_floats],              # 14차 뒤: 음성이 나오는 동안에도 다음 장과 같은 배경(떠다니는 옅은 기록 조각)
    'in03': [patch_person_click, patch_floats, patch_aura], 'in04': [patch_floats, patch_aura], 'in05': [patch_floats, patch_aura],
    'in07': [patch_heading7, patch_query7], 'hub2': [patch_hub],
    'in09': [patch_answer, patch_cap_size('in09'), patch_person_click],      # 11차: 큰 글 35pt, 장이 열리면 빈 화면이고 클릭해야 글과 대화 화면이 뜸
    'scat': [patch_cap_size('scat')], 'gath': [patch_gather], 'in12': [patch_cap_size('in12')], 'bridge': [patch_logo_center],
}


def copy_any(prs, src, note_tpl):
    """foreign.copy_slide와 같되 영상이나 소리가 딸린 장도 옮긴다(이전 판에 두는 표지와 2쪽). 같은 파일은 덱 안에서 한 번만 저장된다."""
    import io
    from pptx.media import Video
    new = prs.slides.add_slide(F.same_layout(prs, src.slide_layout))
    rid, media = {}, {}
    for k, rel in src.part.rels.items():
        if rel.is_external:
            continue
        if rel.reltype.endswith('/image'):
            rid[k] = new.part.get_or_add_image_part(io.BytesIO(rel.target_part.blob))[1]
        elif rel.reltype.endswith(('/media', '/video', '/audio')):
            tp = rel.target_part
            if tp.partname not in media:
                # 같은 파일이 이미 덱에 있으면(지금 표지의 영상) 그 파일을 함께 씀: 바탕 덱에서 온 영상은 python-pptx의 목록에 없어 직접 찾음
                sha = hashlib.sha1(tp.blob).hexdigest()
                same = [p for p in new.part.package.iter_parts() if str(p.partname).startswith('/ppt/media/') and hashlib.sha1(p.blob).hexdigest() == sha]
                media[tp.partname] = same[0] if same else new.part.package.get_or_add_media_part(Video.from_blob(tp.blob, tp.content_type))
            rid[k] = new.part.relate_to(media[tp.partname], rel.reltype)
    # 다른 장으로 가는 링크(예전 Appendix 목차의 쪽 번호, 장마다의 '목차로')는 떼어 낸다: 이전 판에서는 가리키던 장이 그 자리에 없다
    jump = {k for k, rel in src.part.rels.items() if not rel.is_external and rel.reltype.endswith('/slide')}
    el = copy.deepcopy(src._element)
    for e in list(el.iter()):
        for k, v in list(e.attrib.items()):
            if k.startswith(F.RNS):
                if v == '':                                 # 소리나 영상을 트는 도형의 빈 링크(ppaction://media)는 그대로
                    continue
                if v in jump:
                    e.getparent().remove(e)
                    break
                assert v in rid, '옮기지 못하는 관계 %s=%s (%s)' % (k, v, src.part.partname)
                e.set(k, rid[v])
    dst = new._element
    for ch in list(dst):
        dst.remove(ch)
    for ch in list(el):
        dst.append(ch)
    for k, v in el.attrib.items():
        dst.set(k, v)
    if F.note_text(src):
        F.set_notes(new, F.note_text(src), note_tpl)
    return new


def copy_intro(prs, note_tpl):
    """팀원이 손본 덱(INTRO2)에서 인트로 장을 그대로 옮긴다. 노트는 INTRO_NOTES(그 덱의 노트와 같은 글인지 견줘 다르면 알림). 돌려줌: {키: 장}.
    4·5쪽은 둘째 말풍선의 글을 바꾸고(patch_ask2), 6차에 더 손본 곳은 INTRO_PATCH."""
    src = list(Presentation(str(INTRO2)).slides)
    out = {}
    for k, page in FOREIGN.items():
        sl = F.copy_slide(prs, src[page - 1], note_tpl)
        theirs = F.note_text(src[page - 1])
        for old_, new_ in NOTE_FIX:
            theirs = theirs.replace(old_, new_)
        if k not in NOTE_OURS and ' '.join(theirs.split()) != ' '.join(N.INTRO_NOTES[k].split()):
            print('   ! %s(%d쪽): INTRO_NOTES가 옮겨 온 덱의 노트와 다름' % (k, page))
        if k in ASK2_KEYS:
            patch_ask2(sl)
        for fn in INTRO_PATCH.get(k, []):
            fn(sl)
        F.set_notes(sl, N.INTRO_NOTES[k], note_tpl)
        out[k] = sl
    return out


def old_groups(prs, draw, note_tpl):
    """덱 뒤쪽에 두던 '이전 판' 묶음들(11차 ~ 1차): 묶음마다 가름 장 + 그 차수의 덱(원본/통합본_N차.pptx)에서 옮긴 장. 돌려줌: 묶음의 목록(새 차수부터).
    12차부터는 덱에 넣지 않는다(OLD_GROUPS = False)."""
    src = list(Presentation(str(INTRO)).slides)        # 처음 인트로 덱: '이전 판 (1차)'의 마지막 장에만 씀
    prev11, prev10, prev9, prev8, prev7, prev6, prev5, prev4, prev3, prev2, prev1 = (
        list(Presentation(str(f)).slides) for f in (PREV11, PREV10, PREV9, PREV8, PREV7, PREV6, PREV5, PREV4, PREV3, PREV2, PREV))
    old11 = draw([N.s_divider('o11', '이전 판 (11차)', ['11월 16일 저녁 11차 통합본에서 12차에 화면이나 대본이 바뀐 장: 표지(대본), 통화(2쪽), 3쪽(대본), 10쪽',
                                                      'Let’s think step by step!(25쪽 대본), 04 결과 제공(32쪽), 기대효과(33쪽), 미래의 Weave(35쪽)',
                                                      '노트에 그때의 대본이 그대로 있습니다'],
                              '여기부터는 바꾸기 전의 장입니다. 본 발표에서는 넘기지 않습니다.')])
    old11 += [copy_any(prs, prev11[i - 1], note_tpl) for i in PREV11_KEEP]
    old10 = draw([N.s_divider('o10', '이전 판 (10차)', ['11월 16일 10차 통합본에서 11차에 화면이나 대본이 바뀐 장: 표지, 통화(2쪽), 6, 7, 10, 11, 14, 15쪽',
                                                      'How it works(20쪽), 23~26, 28, 30~32쪽, 기대효과(33쪽), 연표(34쪽), 미래의 Weave(35쪽)',
                                                      '그 뒤는 10차의 Appendix 가운데 고치거나 합치거나 뺀 장. 노트에 그때의 대본이 그대로 있습니다'],
                              '여기부터는 바꾸기 전의 장입니다. 본 발표에서는 넘기지 않습니다.')])
    old10 += [copy_any(prs, prev10[i - 1], note_tpl) for i in PREV10_KEEP + PREV10_APX]
    old9 = draw([N.s_divider('o9', '이전 판 (9차 Appendix)', ['11월 15일 9차 통합본의 Appendix 가운데, 질의응답용으로 다시 짜면서 합치거나 고치거나 뺀 장',
                                                           '한눈에 보기, 모듈과 역할, Reasoning Embedding과 질의 재작성, AgentIR 후보 방식, 지식 그래프 두 장, 검색 방식 비교',
                                                           '세 UX 공통 파이프라인, PDE 질문, 같은 날 사진, Apple, LLM (9차의 42~53쪽)'],
                             '여기부터는 바꾸기 전의 장입니다. 본 발표에서는 넘기지 않습니다.')])
    old9 += [F.copy_slide(prs, prev9[i - 1], note_tpl) for i in PREV9_KEEP]
    old8 = draw([N.s_divider('o8', '이전 판 (8차)', ['11월 13일 8차 통합본에서 9차에 화면이나 대본이 바뀐 장: 통화(2쪽), 수많은 기록(6쪽), 솔루션 세 장(17~19쪽)',
                                                    '임베딩 검색(24쪽), 중간 단서(26쪽), 02 질의 재작성(29쪽), Hop 1(30쪽), Hop 2(31쪽), 본 발표에서 뺀 비즈니스 임팩트(34쪽)',
                                                    '연표(35쪽), 마무리 ①(36쪽), 맺는 장(39쪽). 노트에 그때의 대본이 그대로 있습니다'],
                             '여기부터는 바꾸기 전의 장입니다. 본 발표에서는 넘기지 않습니다.')])
    old8 += [F.copy_slide(prs, prev8[i - 1], note_tpl) for i in PREV8_KEEP]
    old7 = draw([N.s_divider('o7', '이전 판 (7차)', ['11월 13일 7차 통합본에서 8차에 화면이나 대본이 바뀐 장: 인트로 2~5, 7~12, 14쪽, 솔루션 ③(18쪽)',
                                                    'How it Works 21~25, 29, 31쪽, 기대효과(32쪽), 비교(33쪽), 비즈니스 임팩트(34쪽), 연표(35쪽)',
                                                    '마무리 ①②(36, 37쪽), 맺는 장(39쪽). 노트에 그때의 대본이 그대로 있습니다'],
                             '여기부터는 바꾸기 전의 장입니다. 본 발표에서는 넘기지 않습니다.')])
    old7 += [F.copy_slide(prs, prev7[i - 1], note_tpl) for i in PREV7_KEEP]
    old6 = draw([N.s_divider('o6', '이전 판 (6차)', ['11월 13일 6차 통합본에서 7차에 화면이나 대본이 바뀐 장: 인물 셋(3~5쪽), 기대효과(32쪽)',
                                                    '비즈니스 임팩트(33쪽), 연표(34쪽), 마무리 ③(37쪽), Appendix에 두었던 비교 장(39쪽)',
                                                    '노트에 그때의 대본이 그대로 있습니다'],
                             '여기부터는 바꾸기 전의 장입니다. 본 발표에서는 넘기지 않습니다.')])
    old6 += [F.copy_slide(prs, prev6[i - 1], note_tpl) for i in PREV6_KEEP]
    old5 = draw([N.s_divider('o5', '이전 판 (5차)', ['11월 12일 5차 통합본에서 6차에 화면이나 대본이 바뀐 장: 2, 3, 7, 9, 10, 17, 18, 21~25, 28~30쪽',
                                                    '기대효과 세 장(32~34쪽), 비교 지도(35쪽), 비즈니스 임팩트(36쪽), 마무리 세 장(38~40쪽), 제안 장표(57~60쪽)',
                                                    '노트에 그때의 대본이 그대로 있습니다'],
                             '여기부터는 바꾸기 전의 장입니다. 본 발표에서는 넘기지 않습니다.')])
    old5 += [F.copy_slide(prs, prev5[i - 1], note_tpl) for i in PREV5_KEEP]
    old4 = draw([N.s_divider('o4', '이전 판 (4차)', ['11월 12일 4차 통합본의 7~14쪽 (팀원이 손본 장으로 바뀌기 전)',
                                                    '노트에 그때의 대본이 그대로 있습니다'],
                             '여기부터는 바꾸기 전의 장입니다. 본 발표에서는 넘기지 않습니다.')])
    old4 += [F.copy_slide(prs, prev4[i - 1], note_tpl) for i in PREV4_KEEP]
    old3 = draw([N.s_divider('o3', '이전 판 (3차)', ['11월 12일 3차 통합본의 16쪽, 뺀 21쪽, 22~26쪽, 30쪽, 비교 표(37쪽)',
                                                    '노트에 그때의 대본이 그대로 있습니다'],
                             '여기부터는 바꾸기 전의 장입니다. 본 발표에서는 넘기지 않습니다.')])
    old3 += [F.copy_slide(prs, prev3[i - 1], note_tpl) for i in PREV3_KEEP]
    old2 = draw([N.s_divider('o2', '이전 판 (2차)', ['11월 11일 2차 통합본의 인트로 2~14쪽, 빠진 고리(26쪽), 뒷부분 32~41쪽, 두 줄 연표 제안(62쪽)',
                                                    '노트에 그때의 대본이 그대로 있습니다'],
                             '여기부터는 바꾸기 전의 장입니다. 본 발표에서는 넘기지 않습니다.')])
    old2 += [F.copy_slide(prs, prev2[i - 1], note_tpl) for i in PREV2_KEEP]
    old1 = draw([N.s_divider('o1', '이전 판 (1차)', ['11월 11일 1차 통합본의 인트로 2~13쪽, 뒷부분 32~41쪽, 저장 채널 그림(59쪽)', '그 뒤는 인트로 덱의 13쪽',
                                                    '노트에 그때의 대본이 그대로 있습니다'],
                             '여기부터는 바꾸기 전의 장입니다. 본 발표에서는 넘기지 않습니다.')])
    old1 += [F.copy_slide(prs, prev1[i - 1], note_tpl) for i in PREV_KEEP] + [F.copy_slide(prs, src[12], note_tpl)]
    return [old11, old10, old9, old8, old7, old6, old5, old4, old3, old2, old1]


def build(dst):
    prs = Presentation(str(BASE))
    old = list(prs.slides)
    cover, mg = old[0], old[3]
    layout = old[5].slide_layout                       # How it Works 장과 같은 틀
    note_tpl = [copy.deepcopy(sh._element) for sh in old[5].notes_slide.placeholders]
    intro = copy_intro(prs, note_tpl)
    patch_cover(cover)
    patch_mg(mg)
    F.set_notes(cover, N.INTRO_NOTES['cover'], note_tpl)
    report = []

    def draw(specs):
        slides, rep, _ = HW.add_slides(prs, layout, note_tpl, specs)
        report.extend(rep)
        return slides
    specs = own_specs()
    own = {k: draw(v) for k, v in specs.items() if k != 'prop'}
    main = []
    for item in SEQ:
        main += own[item[1]] if isinstance(item, tuple) else [cover if item == 'cover' else mg if item == 'mg' else intro[item]]
    n_main = len(main)
    qa = draw([N.s_qa()])                              # 11차(11-16): 본 발표와 Appendix 사이에 질의응답 동안 띄워 두는 장
    import qna as Q                                    # 10차(11-15): Appendix를 질의응답용으로 다시 짬(목차, 코드, 쪽 번호. qna.py)
    appx = Q.assemble(prs, layout, note_tpl, draw, n_main + len(qa) + 1)
    prop = draw([N.s_divider('p0', '제안 장표', ['본 발표에 넣을지 정하지 않은 장'],
                             '여기부터는 제안 장표입니다. 본 발표에서는 넘기지 않습니다.')] + specs['prop']) if specs['prop'] else []      # 6차: 없음
    olds = old_groups(prs, draw, note_tpl) if OLD_GROUPS else []      # 12차(11-16 밤): 이전 판 묶음은 덱에 넣지 않음
    order = [*main, *qa, *appx, *prop] + [s for g in olds for s in g]
    drop_slides(prs, [s for s in old if s not in (cover, mg)])
    reorder(prs, order)
    samsung_fonts.remap_prs(prs)
    logo_style(own['back'])                             # 맺는 장의 'Weave' 글자를 표지 제목처럼(Samsung Sharp Sans, 보라 그라데이션)
    build.n_main, build.n_qa, build.n_appx, build.n_prop, build.n_old = n_main, len(qa), len(appx), len(prop), [len(g) for g in olds]
    prs.save(str(dst))
    for key, nclick, nnote, _ in report:
        if nclick != nnote:
            print('   ! %s: 클릭 %d ≠ 노트 (클릭) %d' % (key, nclick, nnote))
    return order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--png', action='store_true')
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    order = build(DST)
    print('→', DST.name, '%.1f MB' % (DST.stat().st_size / 1e6), len(order), '장')
    if a.png:
        pngs = render_c.png(DST, OUT / 'png', 1600, 900)
        print('png', len(pngs))


if __name__ == '__main__':
    main()
