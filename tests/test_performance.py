import numpy as np
from core.performance import compute_heavy_operation, batch_process

def test_compute_heavy_operation():
    data = np.eye(3)
    inv1 = compute_heavy_operation(data)
    inv2 = compute_heavy_operation(data)  # Memoized, should not recompute
    assert np.allclose(inv1, np.linalg.inv(data))
    assert np.allclose(inv2, inv1)

def test_batch_process():
    items = list(range(1000))
    func = lambda x: x * 2
    results = batch_process(items, func)
    assert results == [x*2 for x in items]