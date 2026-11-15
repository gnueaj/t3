#!/usr/bin/env python3
"""Appendix(질의응답용)의 대본 → Appendix_QnA_대본.md

  python qna_doc.py

장마다 물음(Q), 답(A, 실제로 말할 문장), 이어서 나올 물음과 답, 근거를 적는다. 글은 qna_a.py ~ qna_r.py의 PAGES에서 가져온다(덱의 노트와 같은 글).
쪽 번호는 통합본 기준이다(목차가 40쪽).
"""
import re
from pathlib import Path

import make as M  # noqa: F401  (How it Works 엔진의 경로를 잡아 줌)
import qna as Q

HERE = Path(__file__).resolve().parent
DST = HERE / 'Appendix_QnA_대본.md'
FIRST = 40
RATE = 5.0                       # 말하는 속도(음절/초). 본 발표의 낭독은 299음절에 54초(쉬는 틈 포함 5.5음절/초)


def syllables(text):
    """말할 때의 음절 수 어림: 한글 글자 + 숫자는 자리마다 1.4 + 영문은 글자의 0.6."""
    t = text.replace('(클릭)', '')
    return round(len(re.findall('[가-힣]', t)) + 1.4 * len(re.findall(r'\d', t)) + 0.6 * len(re.findall('[A-Za-z]', t)))


def secs(text):
    return syllables(text) / RATE


HEAD = """# Weave Appendix 질의응답 대본

발표 뒤 질문이 나왔을 때 쓰는 대본이에요. 덱(`Weave_통합본_Claude.pptx`)의 40쪽부터가 Appendix이고, 같은 장을 `Weave_Appendix_Claude.pptx`에 따로 담아 두었어요(그 덱에서는 목차가 1쪽).

## 쓰는 법

- 질문을 들으면 아래 '질문으로 찾기' 표에서 쪽을 찾아 오퍼레이터에게 "Appendix NN쪽 가 주세요"라고 말해요. 발표 중인 PowerPoint에서 쪽 번호를 누르고 Enter를 치면 그 장이 열려요.
- 40쪽 목차의 항목을 눌러도 그 장으로 가고, 장마다 오른쪽 위의 '목차'를 누르면 목차로 돌아와요.
- 화면에는 답의 뼈대(그림, 숫자, 질문과 답)가 있어요. A를 말하고, 더 물으면 그 아래의 답을 써요.
- A는 실제로 말할 문장으로 적었고 30초에서 1분 30초 사이예요. 시간은 1초에 5음절로 어림한 값이에요.
- 근거는 말하지 않아도 되는 확인용 자료예요. 숫자를 되물으면 여기서 찾아요.
"""


def main():
    pgs = Q.pages()
    num = Q.numbers(FIRST, pgs)
    L = [HEAD, '## 질문으로 찾기', '', '| 쪽 | 코드 | 이런 질문이 나오면 | 답하는 시간 |', '| --- | --- | --- | --- |']
    for p in pgs:
        if p.plain:
            continue
        L.append('| %d | %s | %s | 약 %d초 |' % (num[p.code], p.code, p.q, round(secs(p.a) / 5) * 5))
    L += ['', '출처 장: ' + ', '.join('%d쪽 %s' % (num[p.code], p.toc) for p in pgs if p.plain), '']
    sec = None
    over = []
    for p in pgs:
        if p.plain:
            continue
        if p.code[0] != sec:
            sec = p.code[0]
            L += ['## %s. %s' % (sec, p.sec), '']
        t = secs(p.a)
        if not 25 <= t <= 95:
            over.append((p.code, round(t)))
        L += ['### %s (%d쪽) %s' % (p.code, num[p.code], p.toc), '',
              '**Q.** %s' % p.q, '',
              '**A.** %s' % p.a, '',
              '약 %d초, %d음절%s' % (round(t), syllables(p.a), '. (클릭)에서 한 번 눌러요' if p.clicks else ''), '']
        if p.more:
            L += ['더 물으면', '']
            L += ['- **%s** %s' % (q, a) for q, a in p.more]
            L.append('')
        if p.basis:
            L += ['근거', '']
            L += ['- %s' % b for b in p.basis]
            L.append('')
    tail = (HERE / 'Appendix_QnA_덧붙임.md')
    if tail.exists():
        L.append(tail.read_text(encoding='utf-8').rstrip() + '\n')
    DST.write_text('\n'.join(L), encoding='utf-8')
    n = sum(1 for p in pgs if not p.plain)
    print('→', DST.name, '%d장, 더 물으면 %d개' % (n, sum(len(p.more) for p in pgs)))
    for code, t in over:
        print('   ! %s: 답이 약 %d초' % (code, t))


if __name__ == '__main__':
    main()
