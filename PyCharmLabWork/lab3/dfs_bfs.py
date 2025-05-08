from collections import deque

def dfs(graph, start):
    stack, visited = [start], set()
    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v)
            stack.extend(n for n in graph[v] if n not in visited)
    return visited

def bfs(graph, start):
    q, visited = deque([start]), set([start])
    while q:
        v = q.popleft()
        for n in graph[v]:
            if n not in visited:
                visited.add(n); q.append(n)
    return visited