#!/usr/bin/env python3
"""256차원 벡터를 받는 작은 MLP(256 → 128 → 5)의 파라미터 수, 크기, 한 번 계산하는 시간(numpy, 코어 하나)."""
import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import time
import numpy as np

rng = np.random.default_rng(0)
for n_out in (2, 5):
    W1, b1 = rng.standard_normal((128, 256), dtype=np.float32), rng.standard_normal(128, dtype=np.float32)
    W2, b2 = rng.standard_normal((n_out, 128), dtype=np.float32), rng.standard_normal(n_out, dtype=np.float32)
    params = W1.size + b1.size + W2.size + b2.size
    x = rng.standard_normal(256, dtype=np.float32)

    def fwd(x):
        h = W1 @ x + b1
        np.maximum(h, 0, out=h)
        return W2 @ h + b2
    for _ in range(2000):
        fwd(x)
    ts = []
    for _ in range(31):
        t0 = time.perf_counter()
        for _ in range(10000):
            fwd(x)
        ts.append((time.perf_counter() - t0) / 10000)
    med = sorted(ts)[len(ts) // 2]
    print('256 → 128 → %d: 파라미터 %d개, float32 %.0fKB, int8 %.0fKB, 한 번 %.1f마이크로초(31번의 가운데 값)' % (n_out, params, params * 4 / 1000, params / 1000, med * 1e6))
# 층 하나짜리(지금 장에 적힌 Linear 층)
print('256 → 5 (층 하나): 파라미터 %d개' % (256 * 5 + 5))
