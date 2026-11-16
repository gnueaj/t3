#!/usr/bin/env python3
"""암시된 단서 검색의 작은 확인 실험(Appendix D-5, D-6의 주장을 우리 시나리오의 기록으로 직접 재 봄).

  ~/.cache/weave-tools/age-venv/bin/python -I tools/exp_retrieval_pilot.py --hf-home ~/.cache/weave-tools/exp-models/hf

확인하려는 주장: "키워드 검색(BM25)과 일반 임베딩은 단어도 뜻도 겹치지 않는 단서 기록을 놓치기 쉽다. 그래서 추론용으로 튜닝한 임베딩이 필요하다."

무엇을 쟀나
  기록 83건의 풀 하나에서 질의 21개마다 정답 기록(질의마다 하나)이 몇 위에 오는지를 방법마다 잰다.
  - 기록: Appendix의 시나리오 카드 33건(qna_c.py의 C2_DATA·C3_DATA·C4_DATA, qna_d.py의 D5_EX, qna_e.py의 E1·E2·E3. 카드 하나 = 기록 하나)에
    같은 말투로 지어 넣은 일상 기록 50건(지어낸 질의의 정답 8건, 헷갈리는 기록 33건, 평범한 기록 9건)을 더했다.
    검색에 쓰는 글은 '앱 이름 + 보낸 사람이나 제목 + 본문'을 이은 한 줄이고, 기록의 날짜(카드의 회색 줄)는 넣지 않는다. 사진은 사진을 묘사한 이름만.
    본문에 적힌 시각(예약 시각 '11월 21일(토) 10시 30분' 등)은 본문이라 그대로 둔다. 카드의 본문 줄은 빈칸 하나로 잇는다.
    지은의 카카오톡과 아내의 카카오톡은 Appendix 카드가 줄여 적은 것이라 본 발표 화면의 온전한 문장을 썼다.
    '현재 위치', 냉장고, 세탁기, 알림장 카드도 카드에 적힌 이름 그대로 기록 하나로 넣었다.
  - 질의: 암시 질의 15개(정답 기록에 질의의 핵심 낱말이 없고 상식으로 한 번 이어야 함. 시나리오에서 7개, 같은 꼴로 지어낸 것 8개)와
    쉬운 질의 6개(정답 기록에 질의와 같은 낱말이 있음. 모두 시나리오 카드).
  - 기록과 질의는 방법을 돌리기 전에 정했고, 결과를 본 뒤에 고치지 않았다(DATA_SHA256으로 확인).
  - 시나리오 카드는 10차(커밋 b9e2a03, 11-16 낮)의 글이다. 실험을 돌리는 사이에 덱이 11차로 바뀌어 E-1의 첫 장면이 달라졌다
    (입력 '취업 준비 때 기뻤던 날 썼던 일기', 일기 '합격 문자 확인하고 엄마한테 전화했다. 발걸음이 가벼워서 집까지 걸어왔다.').
    이 실험의 a02와 r13은 10차의 글(우울, 불합격 문자) 그대로다. 11차의 글로 바꾸려면 a14(취업에 성공한 날)의 정답이 둘이 되므로 함께 손봐야 한다.

어떻게 쟀나
  - BM25: Okapi BM25(k1 1.2, b 0.75. IDF는 ln(1 + (N - df + 0.5) / (df + 0.5))). 형태소 분석기 없이 글자 2-gram
    (한글이 이어진 덩이마다 겹치는 2-gram, 한 글자짜리 덩이는 1-gram, 영문과 숫자는 덩이째. Lucene CJKAnalyzer와 같은 꼴).
    정답 기록의 점수가 0이면(겹치는 토큰이 없음) 검색되지 않은 것으로 치고 순위를 주지 않는다(MRR에는 0).
  - 임베딩 넷: 모델 카드의 사용법(질의 접두어나 instruction, pooling, 정규화)을 그대로 따르고 코사인 유사도로 줄을 세운다.
      intfloat/multilingual-e5-small   일반 임베딩. 질의 'query: ', 기록 'passage: ', 평균 pooling
      BAAI/bge-m3                      일반 임베딩. 접두어 없음, CLS pooling(dense)
      Qwen/Qwen3-Embedding-0.6B        아래 모델의 바탕. 질의에만 'Instruct: …\\nQuery:', 마지막 토큰 pooling(왼쪽 padding)
      AQ-MedAI/Diver-Retriever-0.6B    추론용으로 튜닝한 임베딩(BRIGHT 25.2). 사용법은 바탕 모델과 같음
    Qwen3와 Diver의 instruction은 카드와 모델 설정(config_sentence_transformers.json)에 적힌 기본 문장을 쓴 것이 본 결과다.
    카드가 과제에 맞는 영어 instruction을 권해서, 미리 정한 맞춤 문장 하나로 한 번 더 돌린 값을 '맞춤 instruction' 줄로 따로 적는다(민감도 확인용).
  - 모델을 바르게 썼는지는 모델 카드의 예시 점수를 다시 내어 확인한다(e5-small의 카드에는 기대 점수가 없어 건너뜀).
    bge-m3와 Qwen3는 카드의 점수가 그대로 나온다. Diver는 나오지 않는다(카드 [[0.753, 0.115], [0.032, 0.626]], 나온 값 [[0.794, 0.389], [0.400, 0.721]]).
    확인한 것: 파일의 가중치 310개가 빠짐없이 같은 값으로 실렸고, 토큰은 바탕 모델과 같고, padding 방향·한 문장씩·bfloat16으로 바꿔도 값이 같다.
    Diver의 다른 카드 셋(4B, 1.7B, 4B-1020)은 예시 점수가 서로 똑같이 적혀 있어, 카드의 예시 점수가 이 가중치로 낸 값이 아닌 것으로 보인다.
  - 첫 실행 뒤에 더한 줄 하나: 저자들의 BRIGHT 평가 코드(github.com/AQ-MedAI/Diver, Retriever/retrievers.py)는 카드와 달리 문서 앞에
    'Represent this text:'를 붙인다. 그 방식으로 Diver를 한 번 더 돌려 '저자 평가 코드 방식' 줄로 적는다(이 방식도 카드의 예시 점수는 내지 못함).
    카드대로 돌린 줄이 본 결과이고, 이 줄은 결과를 본 뒤에 사용법을 확인하다가 더한 것이라 참고용이다.
  - 지표: 질의 묶음마다 정답이 1위인 질의 수, 3위 안인 질의 수, MRR(정답 순위의 역수의 평균).
    순위는 '정답보다 점수가 높은 기록 수 + 1'이고, 정답과 점수가 같은 기록의 수(동점)를 따로 적는다.

  - 덧붙임(첫 실행의 결과를 본 뒤에 더한 확인): '~한 날' 꼴의 질의 여럿에서 평범한 기록으로 넣은 '캘린더 분리수거 하는 날'(r77)이
    위쪽에 올랐다. 기록은 그대로 두고, 이 기록이 없는 풀이었다면의 지표를 따로 셈해 적는다(본 결과는 r77이 있는 풀).

읽을 때 주의
  - 암시 질의는 '정답 기록에 핵심 낱말이 없게' 만들었으므로 BM25가 놓치는 것은 정의에서 나오는 결과다. 볼 것은 임베딩끼리의 차이다.
  - 기록 83건, 질의 21개의 작은 풀이고 기록과 질의를 한 사람이 지었다. 여러 사람의 휴대폰에 있을 법한 기록이 한 풀에 섞여 있다.
  - Diver는 영어와 중국어의 추론 데이터로 튜닝한 모델이라 한국어 일상 기록은 학습 분포 밖이다.

모델 파일은 --hf-home 아래에 받는다(없으면 로그인 없이 내려받음. revision 고정, 필요한 파일만). 원격 코드는 실행하지 않는다.
결과는 out/exp_retrieval_pilot.json에 남긴다.
"""
import argparse
import hashlib
import json
import math
import os
import platform
import re
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'out' / 'exp_retrieval_pilot.json'
HF_DEFAULT = Path.home() / '.cache' / 'weave-tools' / 'exp-models' / 'hf'

# ------------------------------------------------------------------ 기록 풀
# (id, 출처, 앱 이름, 보낸 사람이나 제목, 본문 줄들). 출처: C2~E3은 Appendix의 카드, '지음'은 이 실험을 위해 지어 넣은 기록.
RECORDS = [
    # --- Appendix 시나리오 카드 33건
    ('r01', 'C2', '캘린더', '삼성기술전 시연', ['오후 2시, 수원 3번 부스']),
    ('r02', 'C2', '삼성노트', '주간 회의', ['문제 상황부터 → 라이브 데모 → 관람객 체험']),
    ('r03', 'C2', '메일', '민수', ['최종본 공유드려요', '첨부: Demo_Final.pptx']),
    ('r04', 'C3·D5', '카카오톡', '지은', ['박스 정리 다 했어! 이따 올 때 휴지 안 사 와도 돼']),            # 본 발표 18쪽 화면의 온전한 문장
    ('r05', 'C3', '갤러리', '와인 라벨 사진', []),
    ('r06', 'C4', '현재 위치', '인천공항 면세점', []),
    ('r07', 'C4', '삼성 월렛', '탑승권', ['인천 → 싱가포르']),
    ('r08', 'C4', '카카오톡', '아내', ['여보, 동생이 이 갈색병 좋대. 면세점에서 판다더라']),               # 본 발표 19쪽과 모션그래픽의 온전한 문장
    ('r09', 'C4', '카카오톡', '링크 미리보기', ['새봄몰 에스티로더 50ml']),
    ('r10', 'D5', '캘린더', '성빈이 신혼집들이', []),
    ('r11', 'D5', '삼성노트', '소믈리에 추천', ['샤토 마고']),
    ('r12', 'E1', '캘린더', '상반기 공채 서류 마감', []),
    ('r13', 'E1', '삼성노트', '집에 오는 길', ['불합격 문자 보고 한참 그냥 걸었다.', '나만 제자리인 것 같아 마음이 무겁다.']),
    ('r14', 'E1', '캘린더', '집 계약 및 내부 확인', []),
    ('r15', 'E1', '삼성노트', '거실 창가 쪽 메모', ['냉장고 칸 가로 98cm로 쟀다.', '작은방 방충망이 찢어져 있다.']),
    ('r16', 'E1', '카카오톡', '김정호 공인중개사', ['집주인분이 입주 전까지 안방', '도배는 새로 해 주기로 했어요']),
    ('r17', 'E1', '삼성노트', '엄마표 갈비찜 레시피', ['간장 6, 설탕 2, 다진 마늘 2, 참기름 1', '사과 1개랑 배 2개는 꼭 갈아 넣기!']),
    ('r18', 'E1', '냉장고', '보관 중인 과일', ['사과 3개', '배 없음']),
    ('r19', 'E2', '카카오톡', '동현', ['케이블카 타기 전에 팔공산 입구 도착!', '눈 엄청 오는데 패딩 단단히 입고 와']),
    ('r20', 'E2', '갤러리', '눈길에서 환하게 웃는 모습', []),
    ('r21', 'E2', '갤러리', '정상 표지석 앞 브이', []),
    ('r22', 'E2', '갤러리', '눈사람 들고 장난치는 모습', []),
    ('r23', 'E2', '메시지', '한빛건강검진센터', ['검진 결과지 수령 및 전문의 상담 안내드립니다.', '신분증 지참 후 내원 바랍니다.']),
    ('r24', 'E2', '갤러리', '책상 위에 놓인 검진 결과지', []),
    ('r25', 'E2', '카카오톡', '엄마', ['생일 챙겨 줘서 고맙다 잘 가렴', '오늘 먹은 만두전골 속이 편하더라']),
    ('r26', 'E2', '삼성 월렛', '윤가네 손만두', ['종로구 부암동', '카드 결제 148,000원']),
    ('r27', 'E3', '카카오톡', '엄마', ['날 추워지는데 감기 조심해라', '아빠 안과 예약 잡히면 알려 주렴']),
    ('r28', 'E3', '메시지', '새한병원', ['김영수님 망막 진료 예약 완료', '11월 21일(토) 10시 30분']),
    ('r29', 'E3', '캘린더', '남편 생일', []),
    ('r30', 'E3', '냉장고', '보관 중인 식재료', ['건미역 있음, 국간장 있음', '국거리 소고기 없음']),
    ('r31', 'E3', '카카오톡', '남편', ['나 이번 생일엔 다른 거 말고', '자기가 끓여준 소고기 미역국 먹고 싶어']),
    ('r32', 'E3', '알림장', '2학년 3반 주간 안내', ['목요일 3교시는 강당 체육 활동입니다.', '아이들 동복 체육복 꼭 챙겨 입혀 보내주세요.']),
    ('r33', 'E3', '세탁기', '세탁 기록', ['주간 의류 세탁 후 4일 경과']),
    # --- 지어낸 암시 질의의 정답 8건(질의의 핵심 낱말이 없음)
    ('r34', '지음', '카카오톡', '누나', ['서준이가 청진기 잡았어! 의사 되려나 봐.', '한복 입은 사진 보내 줄게']),
    ('r35', '지음', '카카오톡', '수진', ['와 줘서 고마워! 부케까지 받아 주고.', '신혼여행 다녀와서 밥 살게']),
    ('r36', '지음', '캘린더', '도로주행 2차', ['오전 9시, 강서']),
    ('r37', '지음', '카카오톡', '태민', ['월급 들어오면 바로 보낼게.', '30만 원 진짜 고맙다']),
    ('r38', '지음', '갤러리', '학사모 던지는 순간', []),
    ('r39', '지음', '메시지', '튼튼내과의원', ['인플루엔자 예방접종이 완료되었습니다.', '접종 부위는 문지르지 마세요.']),
    ('r40', '지음', '메일', '도담소프트 인사팀', ['최종 전형 결과 안내', '귀하와 함께하게 되어 기쁩니다. 입사 서류는 첨부한 양식을 참고해 주세요.']),
    ('r41', '지음', '카카오톡', '현우', ['장작은 내가 살게.', '너는 텐트랑 랜턴만 챙겨 와']),
    # --- 헷갈리는 기록 33건: 같은 사람이 다른 날 보낸 메시지
    ('r42', '지음', '삼성노트', '지은이네 주소', ['망원동 가람빌 302호']),
    ('r43', '지음', '카카오톡', '지은', ['이번 주 토요일 러닝 모임 나올 거지?', '아침 7시 반포 한강공원']),
    ('r44', '지음', '카카오톡', '지은', ['나 오늘 너희 회사 근처에서 미팅 있는데', '점심 같이 먹을래?']),
    ('r45', '지음', '카카오톡', '아내', ['여보, 오는 길에 우유랑 계란 좀 사다 줘']),
    ('r46', '지음', '카카오톡', '엄마', ['김치 보냈다 내일 택배 받으면', '바로 냉장고에 넣어라']),
    ('r47', '지음', '카카오톡', '남편', ['오늘 회식이라 늦을 것 같아 먼저 자']),
    ('r48', '지음', '카카오톡', '동현', ['다음 달 풋살 대회 참가비', '2만 원씩 걷는대']),
    ('r49', '지음', '카카오톡', '수진', ['다음 주 독서 모임 장소 바뀌었대.', '합정역 근처래']),
    ('r50', '지음', '카카오톡', '누나', ['서준이 어린이집 적응 잘하고 있어.', '걱정 마']),
    ('r51', '지음', '카카오톡', '태민', ['이번 주 금요일 저녁에 삼겹살 어때?', '자리는 내가 예약할게']),
    ('r52', '지음', '카카오톡', '현우', ['지난주 풋살 사진 보냈어.', '확인해 봐']),
    ('r53', '지음', '메일', '민수', ['회식 장소 투표 부탁드려요', '금요일까지 답장 주세요.']),
    # --- 헷갈리는 기록: 질의와 낱말이 겹치지만 답이 아닌 기록, 주제가 비슷한 기록
    ('r54', '지음', '캘린더', '민재 결혼식', ['낮 12시 30분, 강남']),
    ('r55', '지음', '캘린더', '조카 유치원 발표회', []),
    ('r56', '지음', '삼성노트', '할 일', ['민지한테 빌려준 우산 돌려받기']),
    ('r57', '지음', '메일', '숲속아웃도어', ['캠핑 용품 특가 안내', '텐트와 타프 최대 40% 할인']),
    ('r58', '지음', '메시지', '도로교통공단', ['운전면허 갱신 기간입니다.', '기간 안에 적성검사를 받으시기 바랍니다.']),
    ('r59', '지음', '캘린더', '토익 시험', ['오전 9시 20분까지 입실']),
    ('r60', '지음', '캘린더', '사촌 동생 졸업식', ['오전 11시']),
    ('r61', '지음', '카카오톡', '대학 동기방', ['요즘 독감 유행이래. 다들 조심해']),
    ('r62', '지음', '메일', '취업 박람회 사무국', ['사전 등록이 완료되었습니다', '입장권은 현장에서 받으세요.']),
    ('r63', '지음', '삼성노트', '여행 일기', ['제주 둘째 날. 바람이 세서 우도에는 못 들어갔다.', '대신 해안도로를 오래 걸었다.']),
    ('r64', '지음', '삼성노트', '독서 메모', ['우울에 관한 책을 3장까지 읽었다.', '운동과 햇빛이 도움이 된다고 한다.']),
    ('r65', '지음', '삼성노트', '비 오는 밤', ['헤어지고 돌아오는 길.', '아무것도 하기 싫고 잠도 안 온다.']),
    ('r66', '지음', '삼성노트', '퇴근길', ['팀장님이 보고서 좋았다고 따로 불러서 말해 줬다.', '발걸음이 가볍다.']),
    ('r67', '지음', '메시지', '밝은눈안경', ['주문하신 안경이 준비되었습니다.', '방문 전에 연락 주세요.']),
    ('r68', '지음', '메시지', '바른정형외과', ['물리치료 예약 완료', '화요일 오후 6시']),
    ('r69', '지음', '메시지', '(광고) 뷰티온', ['화장품 전 품목 20% 할인 쿠폰이 도착했습니다.']),
    ('r70', '지음', '삼성노트', '주간 회의', ['다음 분기 예산안 검토, 신입 채용 일정 공유']),
    ('r71', '지음', '메일', '재무팀', ['3분기 실적 보고 자료 송부드립니다', '첨부: 3Q_report.xlsx']),
    ('r72', '지음', '메시지', '새솔초등학교', ['11월 급식비가 자동이체될 예정입니다.']),
    ('r73', '지음', '삼성노트', '출장 준비물', ['여권, 멀티 어댑터, 명함 50장']),
    ('r74', '지음', '메시지', '(광고) 고운한복', ['돌잔치 한복 대여 30% 할인']),
    # --- 평범한 일상 기록 9건
    ('r75', '지음', '메시지', '바로택배', ['고객님의 상품이 문 앞에 배송 완료되었습니다.']),
    ('r76', '지음', '메시지', '한결카드', ['12,500원 승인', '가온커피 성수점']),
    ('r77', '지음', '캘린더', '분리수거 하는 날', []),
    ('r78', '지음', '캘린더', '팀 워크숍', ['1박 2일, 가평']),
    ('r79', '지음', '삼성노트', '장 볼 것', ['두부, 대파, 계란, 주방 세제']),
    ('r80', '지음', '메일', '관리사무소', ['11월 관리비 고지서가 발행되었습니다.']),
    ('r81', '지음', '갤러리', '바닷가에서 찍은 노을', []),
    ('r82', '지음', '갤러리', '생일 케이크 촛불 부는 모습', []),
    ('r83', '지음', '갤러리', '벚꽃 아래 단체 사진', []),
]

# ------------------------------------------------------------------ 질의
# (id, 묶음, 질의, 정답 기록, 출처, 이어 주는 상식이나 겹치는 낱말)
QUERIES = [
    # --- 암시 질의 15개: 정답 기록에 질의의 핵심 낱말이 없음
    ('a01', '암시', '지은이네 집들이는 언제였지?', 'r04', 'C-3의 Sub-query ①', '새집에 갈 때 휴지를 사 간다 → 집들이 초대'),
    ('a02', '암시', '취업 준비 때 우울했던 날의 일기', 'r13', 'E-1', '불합격 문자 → 취업 준비, 마음이 무겁다 → 우울'),
    ('a03', '암시', '아빠 안과 예약', 'r28', 'E-3', '망막 진료 → 안과, 김영수님 → 아빠'),
    ('a04', '암시', '가족이 사다 달라고 한 화장품', 'r08', 'C-4의 Sub-query ①', '갈색병 → 화장품의 별명, 좋대·판다더라 → 사다 달라는 뜻'),
    ('a05', '암시', '시연은 어떤 순서로 진행하지?', 'r02', 'C-2의 Sub-query ②(순서)', '라이브 데모 → 시연, 화살표로 이은 차례 → 순서'),
    ('a06', '암시', '시연 때 쓸 발표 자료', 'r03', 'C-2의 Sub-query ②(자료)', 'Demo → 시연, pptx 첨부 → 발표 자료'),
    ('a07', '암시', '아이 학교 준비물이 뭐였지?', 'r32', 'E-3', '알림장의 체육복 챙겨 보내기 → 준비물'),
    ('a08', '암시', '조카 돌잔치가 언제였지?', 'r34', '지음', '청진기를 잡았다 → 돌잡이, 누나의 아이 → 조카'),
    ('a09', '암시', '수진이 결혼식이 언제였지?', 'r35', '지음', '부케, 신혼여행 → 결혼식'),
    ('a10', '암시', '운전면허 시험 본 날', 'r36', '지음', '도로주행 → 운전면허 시험'),
    ('a11', '암시', '친구한테 돈 빌려준 날', 'r37', '지음', '월급 들어오면 보낼게, 고맙다 → 돈을 빌려 감'),
    ('a12', '암시', '졸업식 날 찍은 사진', 'r38', '지음', '학사모 → 졸업식'),
    ('a13', '암시', '독감 주사 맞은 날', 'r39', '지음', '인플루엔자 예방접종 → 독감 주사'),
    ('a14', '암시', '취업에 성공한 날', 'r40', '지음', '함께하게 되어 기쁩니다, 입사 서류 → 합격'),
    ('a15', '암시', '캠핑 갔던 날', 'r41', '지음', '장작, 텐트, 랜턴 → 캠핑'),
    # --- 쉬운 질의 6개: 정답 기록에 질의와 같은 낱말이 있음
    ('e01', '쉬움', '삼성기술전 시연은 언제 어디서?', 'r01', 'C-2의 Sub-query ①', '삼성기술전, 시연'),
    ('e02', '쉬움', '성빈이 집들이는 언제지?', 'r10', 'D-5의 Level 1 예시', '성빈이, 집들이'),
    ('e03', '쉬움', '엄마가 알려준 갈비찜 양념 비율', 'r17', 'E-1', '엄마, 갈비찜'),
    ('e04', '쉬움', '팔공산 케이블카 타러 간 날', 'r19', 'E-2', '팔공산, 케이블카'),
    ('e05', '쉬움', '남편이 생일에 먹고 싶다던 미역국', 'r31', 'E-3', '남편, 생일, 먹고 싶, 미역국'),
    ('e06', '쉬움', '소믈리에가 추천한 와인', 'r11', 'D-5의 Level 2 예시의 기록', '소믈리에, 추천'),
]
GROUPS = ['암시', '쉬움']

# ------------------------------------------------------------------ 방법
# Qwen3와 Diver의 instruction. 본 결과는 카드와 모델 설정에 적힌 기본 문장(INSTRUCT_CARD), 맞춤 문장은 민감도 확인용으로 돌리기 전에 정해 둠.
INSTRUCT_CARD = 'Given a web search query, retrieve relevant passages that answer the query'
INSTRUCT_TASK = ("Given a question about a user's personal records on a phone (messages, notes, calendar events, photos and emails), "
                 'retrieve the record that contains the clue to answer the question')
SMALL_FILES = ['config.json', 'tokenizer.json', 'tokenizer_config.json', 'special_tokens_map.json', 'added_tokens.json', 'vocab.json', 'merges.txt',
               'sentencepiece.bpe.model', 'modules.json', '1_Pooling/config.json', 'config_sentence_transformers.json', 'sentence_bert_config.json']
# 모델 카드의 예시(질의 둘, 문서 둘)와 카드에 적힌 점수. 모델을 카드대로 썼는지 확인하는 데 씀.
EX_QWEN = (['What is the capital of China?', 'Explain gravity'],
           ['The capital of China is Beijing.',
            'Gravity is a force that attracts two bodies towards each other. It gives weight to physical objects and is responsible for the movement of planets around the sun.'])
EX_BGE = (['What is BGE M3?', 'Defination of BM25'],
          ['BGE M3 is an embedding model supporting dense retrieval, lexical matching and multi-vector interaction.',
           'BM25 is a bag-of-words retrieval function that ranks a set of documents based on the query terms appearing in each document'])
MODELS = [
    dict(key='e5-small', name='multilingual-e5-small', kind='일반 임베딩', repo='intfloat/multilingual-e5-small', rev='614241f622f53c4eeff9890bdc4f31cfecc418b3',
         weights='model.safetensors', pool='mean', pad='right', max_len=512, q_prefix='query: ', d_prefix='passage: ', instruct=False,
         usage="질의 'query: ', 기록 'passage: ', 평균 pooling, L2 정규화, max_length 512", card_ex=None),
    dict(key='bge-m3', name='bge-m3 (dense)', kind='일반 임베딩', repo='BAAI/bge-m3', rev='5617a9f61b028005a4858fdac845db406aefb181',
         weights='pytorch_model.bin', pool='cls', pad='right', max_len=8192, q_prefix='', d_prefix='', instruct=False,
         usage='접두어 없음, CLS pooling(dense_vecs), L2 정규화, max_length 8192', card_ex=(EX_BGE, [[0.6265, 0.3477], [0.3499, 0.678]])),
    dict(key='qwen3-0.6b', name='Qwen3-Embedding-0.6B', kind='일반 임베딩(Diver의 바탕)', repo='Qwen/Qwen3-Embedding-0.6B', rev='97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3',
         weights='model.safetensors', pool='last', pad='left', max_len=8192, q_prefix='', d_prefix='', instruct=True,
         usage="질의에만 'Instruct: {과제}\\nQuery:{질의}', 기록은 그대로, 왼쪽 padding, 마지막 토큰 pooling, L2 정규화, max_length 8192",
         card_ex=(EX_QWEN, [[0.7645568251609802, 0.14142508804798126], [0.13549736142158508, 0.5999549627304077]])),
    dict(key='diver-0.6b', name='Diver-Retriever-0.6B', kind='추론용으로 튜닝한 임베딩', repo='AQ-MedAI/Diver-Retriever-0.6B', rev='9ce2a1e8acae4342c453e1a18b71d468c4c81e39',
         weights='model.safetensors', pool='last', pad='left', max_len=8192, q_prefix='', d_prefix='', instruct=True,
         usage="질의에만 'Instruct: {과제}\\nQuery:{질의}', 기록은 그대로, 왼쪽 padding, 마지막 토큰 pooling, L2 정규화, max_length 8192",
         card_ex=(EX_QWEN, [[0.7534257769584656, 0.1146894246339798], [0.03198453038930893, 0.6258305311203003]]),
         # 첫 실행 뒤에 더한 줄: 저자들의 BRIGHT 평가 코드(github.com/AQ-MedAI/Diver의 Retriever/retrievers.py)는 문서 앞에 이 말을 붙인다
         alt_tag=' · 저자 평가 코드 방식', alt_doc_prefix='Represent this text:',
         alt_usage="질의 'Instruct: {카드 기본 과제}\\nQuery:{질의}', 기록 앞에 'Represent this text:', 나머지는 카드와 같음",
         note='카드의 예시 점수가 재현되지 않음(가중치는 파일과 같게 실리고 토큰도 바탕 모델과 같음). 까닭은 맨 위 설명에'),
]
K1, B = 1.2, 0.75
SOURCE_NOTE = ('시나리오 카드는 10차(커밋 b9e2a03)의 글. 그 뒤 11차에서 E-1의 첫 장면이 바뀜(입력 ‘취업 준비 때 기뻤던 날 썼던 일기’, '
               '일기 ‘합격 문자 확인하고 엄마한테 전화했다. 발걸음이 가벼워서 집까지 걸어왔다.’). 이 실험의 a02와 r13은 10차의 글 그대로임')
POSTHOC_DROP = 'r77'        # 덧붙임에서 '없었다면'을 셈해 보는 기록(캘린더 분리수거 하는 날). 본 결과에는 쓰지 않음


# ------------------------------------------------------------------ 글과 토큰
def record_text(rec):
    """검색에 쓰는 한 줄: 앱 이름 + 보낸 사람이나 제목 + 본문. 날짜는 없다."""
    _, _, app, name, body = rec
    return '%s %s: %s' % (app, name, ' '.join(body)) if body else '%s %s' % (app, name)


_RUN = re.compile(r'[가-힣]+|[a-z]+|[0-9]+')


def grams(text):
    """글자 2-gram. 한글 덩이는 겹치는 2-gram(한 글자면 1-gram), 영문과 숫자는 덩이째. 문장부호와 빈칸에서 끊는다."""
    out = []
    for run in _RUN.findall(text.lower()):
        if '가' <= run[0] <= '힣' and len(run) > 1:
            out += [run[i:i + 2] for i in range(len(run) - 1)]
        else:
            out.append(run)
    return out


def data_sha256():
    blob = json.dumps([[r[0], record_text(r)] for r in RECORDS] + [list(q[:4]) for q in QUERIES], ensure_ascii=False)
    return hashlib.sha256(blob.encode('utf-8')).hexdigest()


# ------------------------------------------------------------------ BM25
def bm25_matrix(q_texts, d_texts):
    docs = [grams(t) for t in d_texts]
    n = len(docs)
    avgdl = sum(len(d) for d in docs) / n
    df = Counter(t for d in docs for t in set(d))
    idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
    tfs = [Counter(d) for d in docs]
    rows = []
    for q in q_texts:
        qt = grams(q)                                   # 질의에 두 번 나온 토큰은 두 번 센다
        row = []
        for d, tf in zip(docs, tfs):
            norm = K1 * (1 - B + B * len(d) / avgdl)
            row.append(sum(idf[t] * tf[t] * (K1 + 1) / (tf[t] + norm) for t in qt if t in tf))
        rows.append(row)
    return rows


# ------------------------------------------------------------------ 임베딩
def fetch(spec, hf_home):
    """모델 파일의 자리를 돌려준다. 이미 받아 둔 것이 있으면 그것을 쓰고, 없으면 로그인 없이 내려받는다."""
    from huggingface_hub import snapshot_download
    kw = dict(repo_id=spec['repo'], revision=spec['rev'], allow_patterns=SMALL_FILES + [spec['weights']], cache_dir=str(Path(hf_home) / 'hub'))
    try:
        return snapshot_download(local_files_only=True, **kw), 0.0
    except Exception:
        t0 = time.perf_counter()
        return snapshot_download(token=False, **kw), time.perf_counter() - t0


def encode(tok, model, texts, spec, batch=16):
    """모델 카드의 코드 그대로: tokenizer(padding, truncation, max_length) → pooling → L2 정규화."""
    import torch
    import torch.nn.functional as F
    out = []
    with torch.inference_mode():
        for i in range(0, len(texts), batch):
            bd = tok(texts[i:i + batch], padding=True, truncation=True, max_length=spec['max_len'], return_tensors='pt')
            hid = model(**bd).last_hidden_state
            mask = bd['attention_mask']
            if spec['pool'] == 'mean':                  # e5: average_pool
                emb = hid.masked_fill(~mask[..., None].bool(), 0.0).sum(dim=1) / mask.sum(dim=1)[..., None]
            elif spec['pool'] == 'cls':                 # bge-m3: dense_vecs = 첫 토큰
                emb = hid[:, 0]
            else:                                       # Qwen3, Diver: last_token_pool
                if bool(mask[:, -1].sum() == mask.shape[0]):
                    emb = hid[:, -1]
                else:
                    emb = hid[torch.arange(hid.shape[0]), mask.sum(dim=1) - 1]
            out.append(F.normalize(emb.float(), p=2, dim=1))
    return torch.cat(out)


def q_form(spec, q, instruct=INSTRUCT_CARD):
    return 'Instruct: %s\nQuery:%s' % (instruct, q) if spec['instruct'] else spec['q_prefix'] + q


def run_model(spec, hf_home, q_texts, d_texts):
    """돌려줌: [(줄 이름, 점수 행렬, 덧붙일 정보)]. instruction을 쓰는 모델은 기본 문장과 맞춤 문장의 두 줄, Diver는 저자 평가 코드 방식의 줄 하나 더."""
    import torch
    from transformers import AutoModel, AutoTokenizer
    t0 = time.perf_counter()
    path, t_dl = fetch(spec, hf_home)
    tok = AutoTokenizer.from_pretrained(path, padding_side=spec['pad'])
    # 원격 코드는 쓰지 않음. bge-m3의 .bin은 weights_only로 읽힘. 파일의 가중치가 빠짐없이 실렸는지도 받아 둔다
    model, loaded = AutoModel.from_pretrained(path, dtype=torch.float32, output_loading_info=True)
    model.eval()
    weights = {k: sorted(v)[:8] if k != 'error_msgs' else list(v)[:3] for k, v in loaded.items() if v}
    t_load = time.perf_counter() - t0 - t_dl
    check = None
    if spec['card_ex']:                                                # 모델 카드의 예시 점수를 다시 내 봄
        (eq, ed), want = spec['card_ex']
        e = encode(tok, model, [q_form(spec, q) for q in eq] + [spec['d_prefix'] + d for d in ed], spec)
        got = (e[:2] @ e[2:].T).tolist()
        diff = max(abs(g - w) for gr, wr in zip(got, want) for g, w in zip(gr, wr))
        check = dict(card=want, got=[[round(v, 4) for v in r] for r in got], max_abs_diff=round(diff, 4), reproduced=diff < 0.01)
    variants = [('', INSTRUCT_CARD, spec['d_prefix'], spec['usage'])]
    if spec['instruct']:
        variants.append((' · 맞춤 instruction', INSTRUCT_TASK, spec['d_prefix'], spec['usage']))
    if spec.get('alt_doc_prefix'):
        variants.append((spec['alt_tag'], INSTRUCT_CARD, spec['alt_doc_prefix'], spec['alt_usage']))
    rows, d_embs, t_docs = [], {}, {}
    for tag, ins, d_prefix, usage in variants:
        if d_prefix not in d_embs:
            t1 = time.perf_counter()
            d_embs[d_prefix] = encode(tok, model, [d_prefix + d for d in d_texts], spec)
            t_docs[d_prefix] = time.perf_counter() - t1
        d_emb = d_embs[d_prefix]
        t2 = time.perf_counter()
        q_emb = encode(tok, model, [q_form(spec, q, ins) for q in q_texts], spec)
        t_q = time.perf_counter() - t2
        info = dict(model=spec['repo'], revision=spec['rev'], kind=spec['kind'], usage=usage, dim=int(d_emb.shape[1]),
                    params_m=round(sum(p.numel() for p in model.parameters()) / 1e6, 1), card_check=check, weights_not_loaded=weights,
                    sec=dict(download=round(t_dl, 1), load=round(t_load, 1), encode_records=round(t_docs[d_prefix], 2), encode_queries=round(t_q, 2)))
        if spec['instruct']:
            info['instruction'] = ins
            info['main'] = not tag
        if tag == spec.get('alt_tag'):
            info['added_after_first_run'] = True
        if spec.get('note'):
            info['note'] = spec['note']
        rows.append((spec['name'] + tag, (q_emb @ d_emb.T).tolist(), info))
    del model
    return rows


# ------------------------------------------------------------------ 순위와 지표
def rank_rows(scores, zero_is_miss=False):
    """질의마다: 정답의 순위(정답보다 점수가 높은 기록 수 + 1), 동점 수, 위에서 셋, 정답보다 위에 온 기록들."""
    ids = [r[0] for r in RECORDS]
    out = {}
    for (qid, _, _, gold, _, _), row in zip(QUERIES, scores):
        g = row[ids.index(gold)]
        order = sorted(range(len(ids)), key=lambda i: (-row[i], i))
        miss = zero_is_miss and g <= 0
        out[qid] = dict(rank=None if miss else 1 + sum(1 for s in row if s > g), ties=sum(1 for s in row if s == g) - 1, gold_score=round(g, 4),
                        top3=[dict(id=ids[i], score=round(row[i], 4)) for i in order[:3]], above=[ids[i] for i in order if row[i] > g])
    return out


def metrics(ranks):
    out = {}
    for grp in GROUPS:
        rs = [ranks[q[0]]['rank'] for q in QUERIES if q[1] == grp]
        out[grp] = dict(n=len(rs), top1=sum(1 for r in rs if r == 1), top3=sum(1 for r in rs if r and r <= 3),
                        mrr=round(sum(1 / r for r in rs if r) / len(rs), 3))
    return out


def cpu_name():
    try:
        for ln in open('/proc/cpuinfo', encoding='utf-8'):
            if ln.startswith('model name'):
                return ln.split(':', 1)[1].strip()
    except OSError:
        pass
    return platform.processor()


# ------------------------------------------------------------------ 실행
def main():
    ap = argparse.ArgumentParser(description='암시된 단서 검색의 작은 확인 실험')
    ap.add_argument('--hf-home', default=str(HF_DEFAULT), help='모델을 받아 두는 HF_HOME 폴더')
    ap.add_argument('--only', default='', help='쉼표로 나눈 모델 key만 돌림(점검용). 예: e5-small')
    ap.add_argument('--no-save', action='store_true', help='결과 파일을 쓰지 않음(점검용)')
    args = ap.parse_args()
    hf_home = str(Path(args.hf_home).expanduser())
    os.environ['HF_HOME'] = hf_home                          # huggingface_hub와 transformers를 들이기 전에 정한다
    os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY', '1')
    os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')

    t_all = time.perf_counter()
    ids = [r[0] for r in RECORDS]
    assert len(set(ids)) == len(ids) and len({q[0] for q in QUERIES}) == len(QUERIES)
    assert all(q[3] in ids for q in QUERIES) and len({q[3] for q in QUERIES}) == len(QUERIES)
    d_texts = [record_text(r) for r in RECORDS]
    q_texts = [q[2] for q in QUERIES]
    assert len(set(d_texts)) == len(d_texts), '같은 글의 기록이 둘'
    print('기록 %d건(시나리오 카드 %d, 지어 넣은 것 %d), 질의 %d개(암시 %d, 쉬움 %d)  DATA_SHA256 %s' % (
        len(RECORDS), sum(1 for r in RECORDS if r[1] != '지음'), sum(1 for r in RECORDS if r[1] == '지음'), len(QUERIES),
        sum(1 for q in QUERIES if q[1] == '암시'), sum(1 for q in QUERIES if q[1] == '쉬움'), data_sha256()[:16]))

    # 질의를 지은 대로인지: 질의와 정답 기록이 함께 가진 2-gram
    overlap = {}
    for qid, grp, q, gold, _, _ in QUERIES:
        overlap[qid] = sorted(set(grams(q)) & set(grams(d_texts[ids.index(gold)])))
    print('\n질의와 정답 기록이 함께 가진 2-gram')
    for qid, grp, q, gold, _, _ in QUERIES:
        print('  %s %s  %-32s %s' % (qid, grp, q, ', '.join(overlap[qid]) or '(없음)'))

    methods = []                                             # (줄 이름, 순위, 정보)
    t0 = time.perf_counter()
    bm = bm25_matrix(q_texts, d_texts)
    methods.append(('BM25 (글자 2-gram)', rank_rows(bm, zero_is_miss=True),
                    dict(kind='키워드 검색', usage='Okapi BM25, k1 %.1f, b %.2f, 한글 2-gram' % (K1, B), sec=dict(total=round(time.perf_counter() - t0, 3)))))
    failed = []
    only = [k for k in args.only.split(',') if k]
    for spec in MODELS:
        if only and spec['key'] not in only:
            continue
        print('\n[%s] 돌리는 중…' % spec['repo'], flush=True)
        try:
            for name, scores, info in run_model(spec, hf_home, q_texts, d_texts):
                methods.append((name, rank_rows(scores), info))
                print('  %s  %s' % (name, info['sec']), flush=True)
            if info.get('card_check'):
                c = info['card_check']
                print('  모델 카드의 예시 점수와의 차이(최대): %.4f → %s' % (c['max_abs_diff'], '재현됨' if c['reproduced'] else '재현되지 않음(카드 %s, 나온 값 %s)' % (
                    [[round(v, 4) for v in r] for r in c['card']], c['got'])))
            print('  실리지 않은 가중치: %s' % (info['weights_not_loaded'] or '없음'))
        except Exception as e:                               # 받지 못했거나 읽지 못한 모델은 이유를 남기고 넘어간다
            failed.append(dict(model=spec['repo'], reason='%s: %s' % (type(e).__name__, e)))
            print('  실패: %s: %s' % (type(e).__name__, e), flush=True)

    # 표 1: 묶음마다의 지표
    table = {name: metrics(ranks) for name, ranks, _ in methods}
    print('\n방법마다의 결과 (정답이 1위인 질의 수 / 3위 안인 질의 수 / MRR)')
    print('  %-46s %-22s %-22s' % ('방법', '암시 질의 %d개' % table[methods[0][0]]['암시']['n'], '쉬운 질의 %d개' % table[methods[0][0]]['쉬움']['n']))
    for name, _, _ in methods:
        m = table[name]
        print('  %-46s %-22s %-22s' % (name, '%2d / %2d / %.3f' % (m['암시']['top1'], m['암시']['top3'], m['암시']['mrr']),
                                       '%2d / %2d / %.3f' % (m['쉬움']['top1'], m['쉬움']['top3'], m['쉬움']['mrr'])))

    # 표 2: 질의마다의 정답 순위
    print('\n질의마다 정답 기록의 순위 (-: BM25에서 겹치는 토큰이 없어 검색되지 않음)')
    print('  열: ' + ' | '.join('%d %s' % (i + 1, name) for i, (name, _, _) in enumerate(methods)))
    for qid, grp, q, gold, _, _ in QUERIES:
        cells = ['%3s' % (ranks[qid]['rank'] or '-') for _, ranks, _ in methods]
        print('  %s %s %s  %s → %s' % (qid, grp, ' '.join(cells), q, gold))
    missed = [q[0] for q in QUERIES if all((ranks[q[0]]['rank'] or 999) > 3 for _, ranks, _ in methods)]
    print('\n모든 방법이 3위 안에 넣지 못한 질의: %s' % (', '.join(missed) or '없음'))

    # 추론용으로 튜닝한 임베딩과 그 바탕 모델을 질의마다 짝지어 봄(암시 질의, 같은 instruction끼리)
    by_name = {name: ranks for name, ranks, _ in methods}
    pairs = {}
    for label, base_tag, tuned_tag in (('카드 기본 instruction', '', ''), ('맞춤 instruction', ' · 맞춤 instruction', ' · 맞춤 instruction'),
                                       ('Diver만 저자 평가 코드 방식', '', MODELS[3]['alt_tag'])):
        base, tuned = by_name.get(MODELS[2]['name'] + base_tag), by_name.get(MODELS[3]['name'] + tuned_tag)
        if not base or not tuned:
            continue
        qs = [q[0] for q in QUERIES if q[1] == '암시']
        pairs[label] = dict(
            tuned_better=[q for q in qs if tuned[q]['rank'] < base[q]['rank']], same=[q for q in qs if tuned[q]['rank'] == base[q]['rank']],
            tuned_worse=[q for q in qs if tuned[q]['rank'] > base[q]['rank']])
    for tag, p in pairs.items():
        print('Diver와 바탕 모델(Qwen3)의 짝 비교, 암시 질의, %s: Diver가 더 높은 순위 %d, 같음 %d, 더 낮은 순위 %d' % (
            tag, len(p['tuned_better']), len(p['same']), len(p['tuned_worse'])))

    # 덧붙임(첫 실행의 결과를 본 뒤에 더한 확인. 본 결과는 위의 표): '~한 날' 꼴의 질의 여럿에서 평범한 기록으로 넣은
    # '캘린더 분리수거 하는 날'(r77)이 위쪽에 올랐다. 이 기록 하나가 결론을 좌우하는지 보려고 r77이 없는 풀이었다면의 지표를 다시 셈한다.
    table_drop = {}
    for name, ranks, _ in methods:
        adj = {q[0]: dict(rank=ranks[q[0]]['rank'] and ranks[q[0]]['rank'] - (POSTHOC_DROP in ranks[q[0]]['above'])) for q in QUERIES}
        table_drop[name] = metrics(adj)
    hit = {name: sum(1 for q in QUERIES if q[1] == '암시' and POSTHOC_DROP in ranks[q[0]]['above']) for name, ranks, _ in methods}
    print('\n덧붙임: %s(%s)이 없는 풀이었다면 (암시 질의. 1위 / 3위 안 / MRR, 괄호는 이 기록이 정답보다 위에 온 질의 수)' % (
        POSTHOC_DROP, d_texts[ids.index(POSTHOC_DROP)]))
    for name, _, _ in methods:
        m = table_drop[name]['암시']
        print('  %-46s %2d / %2d / %.3f   (%d)' % (name, m['top1'], m['top3'], m['mrr'], hit[name]))
    total = time.perf_counter() - t_all
    print('전체 %.1f초' % total)

    import torch
    import transformers
    res = dict(
        what='암시된 단서 검색의 작은 확인 실험: 기록 풀 하나에서 질의마다 정답 기록의 순위',
        date=time.strftime('%Y-%m-%d %H:%M'), data_sha256=data_sha256(),
        env=dict(cpu=cpu_name(), torch=torch.__version__, transformers=transformers.__version__, threads=torch.get_num_threads(), dtype='float32', device='cpu'),
        counts=dict(records=len(RECORDS), records_scenario=sum(1 for r in RECORDS if r[1] != '지음'), records_made=sum(1 for r in RECORDS if r[1] == '지음'),
                    queries=len(QUERIES), implied=sum(1 for q in QUERIES if q[1] == '암시'), easy=sum(1 for q in QUERIES if q[1] == '쉬움')),
        rank_rule='순위 = 정답보다 점수가 높은 기록 수 + 1. BM25에서 정답의 점수가 0이면 순위 없음(null), MRR에는 0',
        source_note=SOURCE_NOTE,
        metrics=table,
        methods=[dict(name=name, **info) for name, _, info in methods],
        failed=failed,
        missed_by_all_top3=missed,
        tuned_vs_base=pairs,
        posthoc_without_record=dict(note='결과를 본 뒤에 더한 확인. 본 결과는 metrics', dropped=POSTHOC_DROP, dropped_text=d_texts[ids.index(POSTHOC_DROP)],
                                    implied_queries_where_it_outranked_gold=hit, metrics=table_drop),
        queries=[dict(id=qid, group=grp, query=q, gold=gold, gold_text=d_texts[ids.index(gold)], source=src, link=link, shared_grams=overlap[qid],
                      results={name: ranks[qid] for name, ranks, _ in methods})
                 for qid, grp, q, gold, src, link in QUERIES],
        records=[dict(id=r[0], source=r[1], app=r[2], name=r[3], text=t) for r, t in zip(RECORDS, d_texts)],
        seconds_total=round(total, 1),
    )
    if args.no_save:
        print('(--no-save: 결과 파일을 쓰지 않음)')
        return
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print('결과: %s' % OUT)


if __name__ == '__main__':
    main()
