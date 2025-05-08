import heapq

def dijkstra(g, s):
    dist = {v: float('inf') for v in g}; dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, v = heapq.heappop(pq)
        if d != dist[v]: continue
        for u,w in g[v]:
            nd = d + w
            if nd < dist[u]:
                dist[u] = nd; heapq.heappush(pq,(nd,u))
    return dist