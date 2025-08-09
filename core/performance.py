import functools
import numpy as np

def memoize(func):
    """Memoize decorator for caching expensive computations."""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def compute_heavy_operation(data):
    # Example: optimized matrix computation
    return np.linalg.inv(data)

def batch_process(items, func):
    """Efficiently process items in batches."""
    results = []
    for batch in np.array_split(items, max(1, len(items)//100)):
        results.extend([func(item) for item in batch])
    return results