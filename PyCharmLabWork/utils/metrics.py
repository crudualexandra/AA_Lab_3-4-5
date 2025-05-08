import time, tracemalloc

def measure_time_mem(func, *args, **kwargs):
    """Return (result, time_s, current_kB, peak_kB)."""
    tracemalloc.start()
    start = time.perf_counter()
    res = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    cur, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return res, elapsed, cur / 1024, peak / 1024