def find(p,i):
    if p[i]!=i: p[i]=find(p,p[i])
    return p[i]

def union(p,r,x,y):
    xr,yr = find(p,x),find(p,y)
    if xr==yr: return
    if r[xr]<r[yr]: p[xr]=yr
    elif r[xr]>r[yr]: p[yr]=xr
    else: p[yr]=xr; r[xr]+=1

def kruskal(g):
    edges=[]
    for u in g:
        for v,w in g[u]:
            if u<v: edges.append((w,u,v))
    edges.sort()
    p={i:i for i in g}; r={i:0 for i in g}; total=0
    for w,u,v in edges:
        if find(p,u)!=find(p,v):
            union(p,r,u,v); total+=w
    return total