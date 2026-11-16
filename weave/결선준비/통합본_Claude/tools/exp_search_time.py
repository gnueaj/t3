#!/usr/bin/env python3
"""벡터 검색 시간을 직접 잰다(Appendix의 'Hop 1회 0.02초' 가운데 검색 10ms의 근거).

  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python tools/exp_search_time.py

256-dim int8 벡터 N건(무작위)을 메모리에 두고, 질의 벡터 하나와 모두 비교(내적)해 가장 가까운 20건을 고르는 시간을 잰다.
색인 구조(HNSW 같은 근사 검색) 없이 전부 비교하는 가장 단순한 방식이다. 코어 하나만 쓰고, 30번 되풀이해 가운데 값을 적는다.
이 값은 PC(x86)의 것이고 휴대폰의 값이 아니다. Appendix는 10만 건에 10ms로 잡았다(팀의 온디바이스 검토 자료가 PC에서 5.1ms를 재고 휴대폰은 그 두 배로 잡은 값).
결과는 out/exp_search_time.json에도 남긴다.
"""
import json
import platform
import time
from pathlib import Path

import numpy as np

DIM, TOPK, REPEAT = 256, 20, 30
OUT = Path(__file__).resolve().parent.parent / 'out' / 'exp_search_time.json'


def cpu_name():
    try:
        for ln in open('/proc/cpuinfo', encoding='utf-8'):
            if ln.startswith('model name'):
                return ln.split(':', 1)[1].strip()
    except OSError:
        pass
    return platform.processor()


def bench(n, rng):
    db8 = rng.integers(-127, 128, size=(n, DIM), dtype=np.int8)       # 저장하는 꼴: 기록 하나에 256바이트
    db = db8.astype(np.float32)                                       # 비교는 실수 행렬 곱 한 번(BLAS). 기기에서는 int8 그대로 SIMD로 비교함
    ts = []
    for _ in range(REPEAT):
        q = rng.integers(-127, 128, size=DIM, dtype=np.int8).astype(np.float32)
        t0 = time.perf_counter()
        s = db @ q
        top = np.argpartition(s, -TOPK)[-TOPK:]
        top = top[np.argsort(s[top])[::-1]]
        ts.append(time.perf_counter() - t0)
    return dict(n=n, index_mb=round(db8.nbytes / 1e6, 1), ms_median=round(float(np.median(ts)) * 1000, 2), ms_min=round(min(ts) * 1000, 2),
                ms_max=round(max(ts) * 1000, 2))


def main():
    rng = np.random.default_rng(0)
    rows = [bench(n, rng) for n in (10_000, 100_000, 1_000_000)]
    res = dict(cpu=cpu_name(), threads=1, dim=DIM, topk=TOPK, repeat=REPEAT, numpy=np.__version__, rows=rows)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print(res['cpu'], '| 코어 1개 | %d-dim int8 | 상위 %d건 | %d번의 가운데 값' % (DIM, TOPK, REPEAT))
    for r in rows:
        print('  %9d건  색인 %7.1f MB  %7.2f ms (%.2f ~ %.2f)' % (r['n'], r['index_mb'], r['ms_median'], r['ms_min'], r['ms_max']))


if __name__ == '__main__':
    main()
