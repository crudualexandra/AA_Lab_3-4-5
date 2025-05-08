import numpy as np

def floyd_warshall(mat):
    dist = np.array(mat, dtype=np.float64)
    n = dist.shape[0]
    for k in range(n):                      # O(V³) but C-level math
        dist = np.minimum(dist,
                          dist[:, k, None] + dist[None, k, :])
    return dist.tolist()
