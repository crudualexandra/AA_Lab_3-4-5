import random

def generate_random_unweighted_graph(n, p):
    """Erdős–Rényi undirected graph (adjacency‑list)."""
    g = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                g[i].append(j)
                g[j].append(i)
    return g

# Pre‑canned topologies for Lab 3

def generate_complete_graph(n):
    return {i: [j for j in range(n) if j != i] for i in range(n)}

def generate_tree_graph(n):  # simple binary‑like chain tree
    g = {i: [] for i in range(n)}
    for i in range(1, n):
        parent = (i - 1) // 2
        g[parent].append(i)
        g[i].append(parent)
    return g

def generate_cycle_graph(n):
    g = {i: [ (i - 1) % n, (i + 1) % n ] for i in range(n)}
    return g

def generate_bipartite_graph(n, ratio=.5):
    left = range(int(n * ratio))
    right = range(int(n * ratio), n)
    g = {i: [] for i in range(n)}
    for u in left:
        for v in right:
            if random.random() < 0.3:
                g[u].append(v)
                g[v].append(u)
    return g

def generate_multigraph(n):
    g = {i: [] for i in range(n)}
    for i in range(n - 1):
        g[i].extend([i + 1, i + 1])
        g[i + 1].extend([i, i])
    return g

def generate_pseudograph(n):
    g = generate_multigraph(n)
    g[0].append(0)
    return g

def generate_regular_graph(n, degree=3):
    g = {i: [] for i in range(n)}
    k = degree // 2
    for i in range(n):
        for d in range(1, k + 1):
            j = (i + d) % n
            g[i].append(j); g[j].append(i)
    return g

# Weighted version for Labs 4/5 (also returns matrix for FW)

def generate_random_weighted_graph(n, p, w_range=(1, 10)):
    g = {i: [] for i in range(n)}
    m = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        m[i][i] = 0
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                w = random.randint(*w_range)
                g[i].append((j, w)); g[j].append((i, w))
                m[i][j] = m[j][i] = w
    return g, m
