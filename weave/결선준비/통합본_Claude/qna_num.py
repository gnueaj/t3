"""Appendix에 적는 시간과 크기의 숫자를 한곳에서 셈한다 (11-16).

기준: EmbeddingGemma 2(텍스트 구성 2.7억 파라미터)를 Galaxy S26 Ultra의 NPU에서 잰 8ms(팀 실측).
같은 모델의 공개 모델 카드(LiteRT-LM)는 같은 기기에서 GPU 25.9ms, CPU 27.1ms라서, NPU가 GPU의 3.2배, CPU의 3.4배 빠르다.
sLLM의 공개 측정값 가운데 GPU에서 잰 것(Gemma 4 E2B)은 이 비율로 NPU 값을 어림하고(사용자의 지시, 11-16),
NPU에서 잰 것(Gemma 3 1B)은 그대로 쓴다. 토큰 수의 가정은 사용자의 검토 자료(Weave 파이프라인 온디바이스 검토, 11-14) 6장의 것.
13차(11-17): FunctionGemma 270M은 뺌('쿼리 재작성에 알맞지 않은 모델이니 들어간 페이지 모두 빼 줘'). 구성은 둘만 남음: 기준 속도(Gemma 4 E2B 환산)와 Gemma 3 1B 실측.

11차(11-16 저녁): '0.2~1.0초는 범위가 너무 크다. 0.2~0.6초로, 출력 토큰에 따라 다르다고 하자. 답변 생성도 요약은 최대 1초쯤, 짧은 출력이나 자동 완성은 0.1초쯤'이라는
검토를 받고 내세우는 숫자의 기준을 바꿈. 전에는 여러 구성의 가장 빠른 값과 가장 느린 값을 범위로 적어서
모델이 달라 생기는 차이와 출력 길이가 달라 생기는 차이가 한 범위에 섞였다. 이제 내세우는 숫자는 기준 속도 하나(REF = Gemma 4 E2B의 NPU 환산, 초당 169토큰)에
출력 토큰 수만 바꿔 셈한다: 검색 계획 40~100토큰 → 0.2~0.6초, 이름 추출 10토큰 → 약 0.1초, 3줄 요약 80~150토큰 → 0.5~0.9초.
두 구성의 값은 속도 2 장(D-4)의 표에 남긴다(느린 줄이 Gemma 3 1B의 NPU 실측).

  python qna_num.py        셈한 값을 모두 찍는다
"""
EMB = 0.008                                   # 질의 하나를 벡터로: EmbeddingGemma 2, Galaxy S26 Ultra NPU 실측
CARD_GPU, CARD_CPU = 0.0259, 0.0271           # 같은 모델, 같은 기기의 모델 카드 값
R_GPU, R_CPU = CARD_GPU / EMB, CARD_CPU / EMB  # 3.24, 3.39
SEARCH, FILTER = 0.010, 0.002                 # 벡터 검색(256-dim, 10만 건을 모두 비교해 상위 20건), 필터링과 Slot
HOP = EMB + SEARCH + FILTER                   # 0.020
TOPK = 20                                     # Hop마다 가져오는 후보 수
# 이 PC(Intel Core i7-1360P, 코어 하나)에서 직접 잰 벡터 검색 시간(ms): tools/exp_search_time.py, 11-16. 256-dim int8, 모두 비교, 상위 20건, 30번의 가운데 값
PC_SEARCH_MS = {10_000: 0.31, 100_000: 4.85, 1_000_000: 51.83}
VEC_BYTES = 256                               # 기록 하나의 벡터 크기(256-dim int8)


class Model:
    """공개 측정값(입력과 출력의 초당 토큰)과 NPU 기준 값."""

    def __init__(self, name, dev, proc, pre, dec):
        self.name, self.dev, self.proc, self.pre, self.dec = name, dev, proc, pre, dec
        self.r = {'NPU': 1.0, 'GPU': R_GPU, 'CPU': R_CPU}[proc]
        self.pre_npu, self.dec_npu = pre * self.r, dec * self.r
        self.kind = 'NPU 실측' if proc == 'NPU' else 'NPU 환산'

    def t(self, n_in, n_out):
        return n_in / self.pre_npu + n_out / self.dec_npu


E2B = Model('Gemma 4 E2B', 'Galaxy S26 Ultra', 'GPU', 3808, 52.1)
G1B = Model('Gemma 3 1B', 'Galaxy S25 Ultra', 'NPU', 5836, 85)
REF = E2B                                              # 내세우는 숫자의 기준 속도(2B급을 S26 Ultra의 NPU 기준으로 환산: 출력 초당 169토큰)
CONFIGS = [(E2B, E2B), (G1B, G1B)]                    # (Query Rewriter, 답변 생성): 속도 2 장의 표. 앞이 기준 속도, 뒤가 NPU 실측
# UX마다: 재작성 입력, 검색 계획 출력, Hop 수, 답변 입력, 답변 출력 (토큰)
UX = {'ux1': (130, 82, 3, 540, 80), 'ux2': (130, 72, 2, 170, 10), 'ux3': (130, 72, 2, 500, 25)}
RW_IN, RW_OUT = 130, (40, 100)                         # Query Rewriter: 입력, 출력(짧은 계획 ~ 출력 한도)
SUM_OUT = (80, 150)                                    # 3줄 요약의 출력(예시의 요약 ~ 출력 한도)


def parts(ux, rw, ans):
    i, o, hops, ai, ao = UX[ux]
    return rw.t(i, o), hops * HOP, ans.t(ai, ao)


def total(ux, rw, ans):
    return sum(parts(ux, rw, ans))


def span(vals, unit='초'):
    """범위를 글로: 0.248, 0.603 → '0.2~0.6초'. 두 끝이 같게 읽히면 '약 0.1초'."""
    a, b = '%.1f' % min(vals), '%.1f' % max(vals)
    return ('약 %s%s' % (a, unit)) if a == b else '%s~%s%s' % (a, b, unit)


def about(v):
    return '약 %.1f초' % v


def sec(v):
    return '%.2f초' % v


# ---- 내세우는 숫자(기준 속도 REF, 출력 토큰 수에 따라)
RW_T = [REF.t(RW_IN, n) for n in RW_OUT]                # 질의 재작성: 0.25, 0.60
T_RW = span(RW_T)                                       # '0.2~0.6초'
T_RW1, T_RW2, T_RW3 = (about(parts(u, REF, REF)[0]) for u in ('ux1', 'ux2', 'ux3'))
AN_NAME, AN_MSG = REF.t(170, 10), REF.t(500, 25)        # 이름 추출(자동 완성), 보낼 메시지 제안
AN_SUM = [REF.t(540, n) for n in SUM_OUT]               # 3줄 요약: 0.52, 0.93
T_AN1, T_AN2, T_AN3 = span(AN_SUM), about(AN_NAME), about(AN_MSG)
T_AN = span([AN_NAME] + AN_SUM)                         # '0.1~0.9초'
UX1_T = [parts('ux1', REF, REF)[0] + 3 * HOP + v for v in AN_SUM]
T_UX1, T_UX2, T_UX3 = span(UX1_T), about(total('ux2', REF, REF)), about(total('ux3', REF, REF))
T_REC1 = about(parts('ux1', REF, REF)[0] + 3 * HOP)     # UX1에서 찾은 기록이 먼저 뜨는 때
TOK_MS = '약 %.0fms' % (1000 / REF.dec_npu)             # 토큰 하나를 생성하는 시간
T_EXP = '약 %.0f초' % (500 / REF.dec_npu)               # 500토큰을 생성하는 시간
# 시간 띠의 폭: 기준 속도의 값(UX1의 요약은 긴 쪽)
BAR = {'ux1': (parts('ux1', REF, REF)[0], 3 * HOP, AN_SUM[1]), 'ux2': parts('ux2', REF, REF), 'ux3': parts('ux3', REF, REF)}
SLOW = BAR                                             # (예전 이름)
BASIS = 'Gemma 4 E2B를 Galaxy S26 Ultra의 GPU에서 잰 공개 측정값을 NPU 기준으로 환산한 속도(출력 초당 %d토큰)' % round(REF.dec_npu)
# ---- 두 구성의 값(표)
TOT = {ux: [total(ux, rw, an) for rw, an in CONFIGS] for ux in UX}
REC1 = [parts('ux1', rw, an)[0] + parts('ux1', rw, an)[1] for rw, an in CONFIGS]


def index_mb(n):
    """기록 n건의 벡터 색인 크기(MB)."""
    return n * VEC_BYTES / 1e6


if __name__ == '__main__':
    print('비율 GPU %.2f, CPU %.2f' % (R_GPU, R_CPU))
    for m in (E2B, G1B):
        print('%-20s %s %s  측정 %d / %.1f tok/s → NPU %.0f / %.0f tok/s (%s)' % (m.name, m.dev, m.proc, m.pre, m.dec, m.pre_npu, m.dec_npu, m.kind))
    print('기준 속도:', BASIS)
    print('재작성 %s (%s) | UX1 %s UX2 %s UX3 %s' % (T_RW, ', '.join('%.3f' % v for v in RW_T), T_RW1, T_RW2, T_RW3))
    print('답변 %s | 이름 %.3f 메시지 %.3f 요약 %s | UX1 %s UX2 %s UX3 %s' % (T_AN, AN_NAME, AN_MSG, ', '.join('%.3f' % v for v in AN_SUM), T_AN1, T_AN2, T_AN3))
    print('합계 UX1 %s (%s, 기록 %s) UX2 %s (%.3f) UX3 %s (%.3f)' % (T_UX1, ', '.join('%.3f' % v for v in UX1_T), T_REC1, T_UX2, total('ux2', REF, REF), T_UX3,
                                                                   total('ux3', REF, REF)))
    print('토큰 하나', TOK_MS, '| 500토큰', T_EXP)
    for ux in ('ux2', 'ux1', 'ux3'):
        for (rw, an), t in zip(CONFIGS, TOT[ux]):
            p = parts(ux, rw, an)
            print('%s  %-20s + %-12s 재작성 %.3f  검색 %.3f  답변 %.3f  합계 %.3f' % (ux, rw.name, an.name, p[0], p[1], p[2], t))
    print('색인', ['%d건 %.1fMB' % (n, index_mb(n)) for n in (10_000, 100_000, 1_000_000, 10_000_000)])
