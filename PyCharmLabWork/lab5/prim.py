import heapq

def prim(g):
    start = 0
    visited = {start}
    pq = [(w,start,u) for u,w in g[start]]; heapq.heapify(pq)
    total = 0
    while pq and len(visited)<len(g):
        w,u,v = heapq.heappop(pq)
        if v in visited: continue
        visited.add(v); total += w
        for to,wt in g[v]:
            if to not in visited:
                heapq.heappush(pq,(wt,v,to))
    return total