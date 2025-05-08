"""5‑trial averaged analysis for DFS vs BFS over various graph families."""
import csv, statistics as st, matplotlib.pyplot as plt
from utils.metrics import measure_time_mem
from lab3.dfs_bfs import dfs, bfs
from utils.graph_generator import (
    generate_random_unweighted_graph, generate_complete_graph,
    generate_tree_graph, generate_cycle_graph, generate_bipartite_graph,
    generate_multigraph, generate_pseudograph, generate_regular_graph)

TRIALS = 5
VERTICES = [100, 500, 1000]
FAMILIES = {
    'Sparse': lambda n: generate_random_unweighted_graph(n, 0.05),
    'Dense': lambda n: generate_random_unweighted_graph(n, 0.6),
    'Complete': generate_complete_graph,
    'Tree': generate_tree_graph,
    'Cycle': generate_cycle_graph,
    'Bipartite': generate_bipartite_graph,
    'Multigraph': generate_multigraph,
    'Pseudograph': generate_pseudograph,
    '3‑Regular': generate_regular_graph
}

def run_once(gen, n):
    g = gen(n)
    _, t_d, m_d, _ = measure_time_mem(dfs, g, 0)
    _, t_b, m_b, _ = measure_time_mem(bfs, g, 0)
    return t_d, m_d, t_b, m_b

def analyze():
    for name, gen in FAMILIES.items():
        rows = []
        for n in VERTICES:
            d_t, d_m, b_t, b_m = [], [], [], []
            for _ in range(TRIALS):
                td, md, tb, mb = run_once(gen, n)
                d_t.append(td); d_m.append(md); b_t.append(tb); b_m.append(mb)
            rows.append([n, st.mean(d_t), st.pstdev(d_t), st.mean(b_t), st.pstdev(b_t),
                          st.mean(d_m), st.pstdev(d_m), st.mean(b_m), st.pstdev(b_m)])
        # CSV
        hdr = ['V','DFS_t_avg','DFS_t_sd','BFS_t_avg','BFS_t_sd','DFS_m_kB_avg','DFS_m_sd','BFS_m_kB_avg','BFS_m_sd']
        csv_name = f'lab3_{name.lower().replace(" ","_")}.csv'
        csv.writer(open(csv_name,'w',newline='')).writerows([hdr]+rows)
        # Charts
        V  = [r[0] for r in rows]
        Dt, Ds, Bt, Bs = [r[1] for r in rows], [r[2] for r in rows], [r[3] for r in rows], [r[4] for r in rows]
        Dm, Dms, Bm, Bms = [r[5] for r in rows], [r[6] for r in rows], [r[7] for r in rows], [r[8] for r in rows]
        def err(x,y,e,l,s): plt.errorbar(x,y,yerr=e,marker=s[0],linestyle=s[1:],capsize=3,label=l)
        plt.figure(); err(V,Dt,Ds,'DFS', 'o-'); err(V,Bt,Bs,'BFS','x-')
        plt.xlabel('Vertices'); plt.ylabel('Time (s)'); plt.title(f'Time – {name}'); plt.legend(); plt.grid(True)
        plt.savefig(f'lab3_{name}_time.png'); plt.close()
        plt.figure(); err(V,Dm,Dms,'DFS mem','o-'); err(V,Bm,Bms,'BFS mem','x-')
        plt.xlabel('Vertices'); plt.ylabel('Memory (KB)'); plt.title(f'Memory – {name}'); plt.legend(); plt.grid(True)
        plt.savefig(f'lab3_{name}_mem.png'); plt.close()
