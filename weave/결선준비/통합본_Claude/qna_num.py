"""Appendix에 적는 시간 숫자를 한곳에서 셈한다 (11-16).

기준: EmbeddingGemma 2(텍스트 구성 2.7억 파라미터)를 Galaxy S26 Ultra의 NPU에서 잰 8ms(팀 실측).
같은 모델의 공개 모델 카드(LiteRT-LM)는 같은 기기에서 GPU 25.9ms, CPU 27.1ms라서, NPU가 GPU의 3.2배, CPU의 3.4배 빠르다.
sLLM의 공개 측정값 가운데 GPU나 CPU에서 잰 것(Gemma 4 E2B, FunctionGemma 270M)은 이 비율로 NPU 값을 어림하고(사용자의 지시, 11-16),
NPU에서 잰 것(Gemma 3 1B)은 그대로 쓴다. 토큰 수의 가정은 사용자의 검토 자료(Weave 파이프라인 온디바이스 검토, 11-14) 6장의 것.

  python qna_num.py        셈한 값을 모두 찍는다
"""
EMB = 0.008                                   # 질의 하나를 벡터로: EmbeddingGemma 2, Galaxy S26 Ultra NPU 실측
CARD_GPU, CARD_CPU = 0.0259, 0.0271           # 같은 모델, 같은 기기의 모델 카드 값
R_GPU, R_CPU = CARD_GPU / EMB, CARD_CPU / EMB  # 3.24, 3.39
SEARCH, FILTER = 0.010, 0.002                 # 벡터 검색(256-dim, 10만 건을 모두 비교), 필터링과 Slot
HOP = EMB + SEARCH + FILTER                   # 0.020


class Model:
    """공개 측정값(입력과 출력의 초당 토큰)과 NPU 기준 값."""

    def __init__(self, name, dev, proc, pre, dec):
        self.name, self.dev, self.proc, self.pre, self.dec = name, dev, proc, pre, dec
        self.r = {'NPU': 1.0, 'GPU': R_GPU, 'CPU': R_CPU}[proc]
        self.pre_npu, self.dec_npu = pre * self.r, dec * self.r
        self.kind = 'NPU 실측' if proc == 'NPU' else 'NPU 환산'

    def t(self, n_in, n_out):
        return n_in / self.pre_npu + n_out / self.dec_npu


FG = Model('FunctionGemma 270M', 'Galaxy S25 Ultra', 'CPU', 2238, 154)
E2B = Model('Gemma 4 E2B', 'Galaxy S26 Ultra', 'GPU', 3808, 52.1)
G1B = Model('Gemma 3 1B', 'Galaxy S25 Ultra', 'NPU', 5836, 85)
CONFIGS = [(FG, E2B), (E2B, E2B), (G1B, G1B)]          # (Query Rewriter, 답변 생성)
# UX마다: 재작성 입력, 검색 계획 출력, Hop 수, 답변 입력, 답변 출력 (토큰)
UX = {'ux1': (130, 82, 3, 540, 80), 'ux2': (130, 72, 2, 170, 10), 'ux3': (130, 72, 2, 500, 25)}


def parts(ux, rw, ans):
    i, o, hops, ai, ao = UX[ux]
    return rw.t(i, o), hops * HOP, ans.t(ai, ao)


def total(ux, rw, ans):
    return sum(parts(ux, rw, ans))


def span(vals, unit='초'):
    """범위를 글로: 0.268, 1.056 → '0.3~1.1초'. 두 끝이 같게 읽히면 '약 0.1초'."""
    a, b = '%.1f' % min(vals), '%.1f' % max(vals)
    return ('약 %s%s' % (a, unit)) if a == b else '%s~%s%s' % (a, b, unit)


def sec(v):
    return '%.2f초' % v


RW = {ux: [parts(ux, rw, an)[0] for rw, an in CONFIGS] for ux in UX}
AN = {ux: [parts(ux, rw, an)[2] for rw, an in CONFIGS] for ux in UX}
TOT = {ux: [total(ux, rw, an) for rw, an in CONFIGS] for ux in UX}
REC1 = [parts('ux1', rw, an)[0] + parts('ux1', rw, an)[1] for rw, an in CONFIGS]      # UX1에서 찾은 기록이 먼저 뜨는 때

T_RW = span(RW['ux1'] + RW['ux2'])            # 질의 재작성 한 번
T_AN = span(AN['ux1'] + AN['ux2'] + AN['ux3'])  # 답변 생성 한 번
T_RW1, T_RW2, T_RW3 = span(RW['ux1']), span(RW['ux2']), span(RW['ux3'])
T_AN1, T_AN2, T_AN3 = span(AN['ux1']), span(AN['ux2']), span(AN['ux3'])
T_UX1, T_UX2, T_UX3 = span(TOT['ux1']), span(TOT['ux2']), span(TOT['ux3'])
T_REC1 = span(REC1)
TOK_MS = '%.0f~%.0fms' % (1000 / max(m.dec_npu for m in (FG, E2B, G1B)), 1000 / min(m.dec_npu for m in (FG, E2B, G1B)))    # 토큰 하나를 생성하는 시간
T_EXP = '%.0f~%.0f초' % (500 / E2B.dec_npu, 500 / G1B.dec_npu)       # 500토큰을 생성하는 시간(2B급 환산 ~ 1B 실측)
SLOW = {ux: parts(ux, G1B, G1B) for ux in UX}  # 시간 띠의 폭은 가장 느린 구성(Gemma 3 1B, NPU 실측)의 값
BASIS = '빠른 쪽은 FunctionGemma 270M과 Gemma 4 E2B의 NPU 환산, 느린 쪽은 Gemma 3 1B의 Galaxy S25 Ultra NPU 실측'

if __name__ == '__main__':
    print('비율 GPU %.2f, CPU %.2f' % (R_GPU, R_CPU))
    for m in (FG, E2B, G1B):
        print('%-20s %s %s  측정 %d / %.1f tok/s → NPU %.0f / %.0f tok/s (%s)' % (m.name, m.dev, m.proc, m.pre, m.dec, m.pre_npu, m.dec_npu, m.kind))
    for ux in ('ux2', 'ux1', 'ux3'):
        for (rw, an), t in zip(CONFIGS, TOT[ux]):
            p = parts(ux, rw, an)
            print('%s  %-20s + %-12s 재작성 %.3f  검색 %.3f  답변 %.3f  합계 %.3f' % (ux, rw.name, an.name, p[0], p[1], p[2], t))
    print('기록이 먼저 뜨는 때(UX1)', ['%.3f' % v for v in REC1])
    print('재작성', T_RW, '| UX1', T_RW1, 'UX2', T_RW2, 'UX3', T_RW3)
    print('답변', T_AN, '| UX1', T_AN1, 'UX2', T_AN2, 'UX3', T_AN3)
    print('합계 UX1', T_UX1, '(기록', T_REC1, ') UX2', T_UX2, 'UX3', T_UX3)
    print('토큰 하나', TOK_MS, '| 500토큰', T_EXP)
