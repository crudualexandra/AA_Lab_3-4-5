"""NumPy‑accelerated Floyd‑Warshall (≈30‑50× faster than pure‑Python loops)."""
import numpy as np

def floyd_warshall(mat):
    dist = np.array(mat, dtype=np.float64)
    n = dist.shape[0]
    for k in range(n):              # still O(V³) but inner ops in C
        dist = np.minimum(dist, dist[:, k, None] + dist[None, k, :])
    return dist.tolist()

# ========================= lab4/analysis_lab4.py ===========================
"""Dijkstra vs Floyd‑Warshall — produces *four* explicit graphs matching
lab‑report Figure 6 style:
  • Sparse Graphs – Execution Time
  • Dense Graphs – Execution Time
  • Sparse Graphs – Memory Usage
  • Dense Graphs – Memory Usage
and writes a CSV with both time & memory statistics (avg ± sd).
"""
import csv, statistics as st, matplotlib.pyplot as plt
from utils.graph_generator import generate_random_weighted_graph
from utils.metrics import measure_time_mem
from lab4.dijkstra import dijkstra
from lab4.floyd_warshall import floyd_warshall

TRIALS = 5


def edge_cnt(adj):
    return sum(len(v) for v in adj.values()) // 2

def one_trial(n, p):
    g, m = generate_random_weighted_graph(n, p)
    e = edge_cnt(g)
    _, dt, dm, _ = measure_time_mem(dijkstra, g, 0)
    _, ft, fm, _ = measure_time_mem(floyd_warshall, m)
    return e, dt, dm, ft, fm

def analyze(verts, p_sparse=0.01, p_dense=0.7):
    rows = []
    for n in verts:
        agg = {k: [] for k in ('e_s','dt_s','dm_s','ft_s','fm_s',
                                'e_d','dt_d','dm_d','ft_d','fm_d')}
        for _ in range(TRIALS):
            e, dt, dm, ft, fm = one_trial(n, p_sparse)
            agg['e_s'].append(e); agg['dt_s'].append(dt); agg['dm_s'].append(dm)
            agg['ft_s'].append(ft); agg['fm_s'].append(fm)
            e, dt, dm, ft, fm = one_trial(n, p_dense)
            agg['e_d'].append(e); agg['dt_d'].append(dt); agg['dm_d'].append(dm)
            agg['ft_d'].append(ft); agg['fm_d'].append(fm)
        a, sd = lambda l: st.mean(l), lambda l: st.pstdev(l)
        rows.append([
            n,
            a(agg['e_s']), sd(agg['e_s']),
            a(agg['dt_s']), sd(agg['dt_s']), a(agg['dm_s']), sd(agg['dm_s']),
            a(agg['ft_s']), sd(agg['ft_s']), a(agg['fm_s']), sd(agg['fm_s']),
            a(agg['e_d']), sd(agg['e_d']),
            a(agg['dt_d']), sd(agg['dt_d']), a(agg['dm_d']), sd(agg['dm_d']),
            a(agg['ft_d']), sd(agg['ft_d']), a(agg['fm_d']), sd(agg['fm_d'])
        ])

    hdr = ['V',
           'E_s_avg','E_s_sd',
           'Dij_s_t_avg','Dij_s_t_sd','Dij_s_m_avg','Dij_s_m_sd',
           'FW_s_t_avg','FW_s_t_sd','FW_s_m_avg','FW_s_m_sd',
           'E_d_avg','E_d_sd',
           'Dij_d_t_avg','Dij_d_t_sd','Dij_d_m_avg','Dij_d_m_sd',
           'FW_d_t_avg','FW_d_t_sd','FW_d_m_avg','FW_d_m_sd']
    csv.writer(open('lab4_results_enhanced.csv','w',newline='')).writerows([hdr]+rows)
    print('[Lab4] CSV ➜ lab4_results_enhanced.csv')

    # Extract columns for plotting
    V = [r[0] for r in rows]
    Dij_t_s, FW_t_s = [r[3] for r in rows], [r[7] for r in rows]
    Dij_t_d, FW_t_d = [r[13] for r in rows], [r[17] for r in rows]
    Dij_m_s, FW_m_s = [r[5] for r in rows], [r[9] for r in rows]
    Dij_m_d, FW_m_d = [r[15] for r in rows], [r[19] for r in rows]

    # Helper for plotting
    def line_plot(x, ys, title, fname, ylab):
        plt.figure()
        for y,l,sty in ys:
            plt.plot(x, y, sty, label=l)
        plt.xlabel('Graph Size (Vertices)'); plt.ylabel(ylab); plt.title(title)
        plt.legend(); plt.grid(True); plt.savefig(fname); plt.close()

    line_plot(V,
              [(Dij_t_s,'Dijkstra','o-'),(FW_t_s,'Floyd‑Warshall','s-')],
              'Sparse Graphs – Execution Time', 'lab4_sparse_time.png', 'Time (s)')
    line_plot(V,
              [(Dij_t_d,'Dijkstra','o--'),(FW_t_d,'Floyd‑Warshall','s--')],
              'Dense Graphs – Execution Time', 'lab4_dense_time.png', 'Time (s)')
    line_plot(V,
              [(Dij_m_s,'Dijkstra Mem','o-'),(FW_m_s,'Floyd Mem','s-')],
              'Sparse Graphs – Memory Usage', 'lab4_sparse_mem.png', 'Memory (kB)')
    line_plot(V,
              [(Dij_m_d,'Dijkstra Mem','o--'),(FW_m_d,'Floyd Mem','s--')],
              'Dense Graphs – Memory Usage', 'lab4_dense_mem.png', 'Memory (kB)')
