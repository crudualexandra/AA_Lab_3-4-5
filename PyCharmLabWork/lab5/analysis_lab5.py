
"""Prim vs Kruskal enhanced empirical study: Execution time & memory usage on sparse and dense graphs."""
import csv
import statistics as st
import matplotlib.pyplot as plt
from utils.graph_generator import generate_random_weighted_graph
from utils.metrics import measure_time_mem
from lab5.prim import prim
from lab5.kruskal import kruskal

TRIALS = 5

def edge_count(adj):
    return sum(len(neighs) for neighs in adj.values()) // 2

def one_trial(n, p):
    g, _ = generate_random_weighted_graph(n, p)
    edges = edge_count(g)
    _, pt, pm, _ = measure_time_mem(prim, g)
    _, kt, km, _ = measure_time_mem(kruskal, g)
    return edges, pt, pm, kt, km

def analyze(vertices, p_sparse=0.01, p_dense=0.7):
    rows = []  # V, E_s, pt_s, pm_s, kt_s, km_s, E_d, pt_d, pm_d, kt_d, km_d
    for n in vertices:
        stats = {k: [] for k in ('E_s','pt_s','pm_s','kt_s','km_s','E_d','pt_d','pm_d','kt_d','km_d')}
        for _ in range(TRIALS):
            E, pt, pm, kt, km = one_trial(n, p_sparse)
            stats['E_s'].append(E); stats['pt_s'].append(pt); stats['pm_s'].append(pm)
            stats['kt_s'].append(kt); stats['km_s'].append(km)
            E, pt, pm, kt, km = one_trial(n, p_dense)
            stats['E_d'].append(E); stats['pt_d'].append(pt); stats['pm_d'].append(pm)
            stats['kt_d'].append(kt); stats['km_d'].append(km)
        a = lambda lst: st.mean(lst)
        s = lambda lst: st.pstdev(lst)
        rows.append([
            n,
            a(stats['E_s']), s(stats['E_s']),
            a(stats['pt_s']), s(stats['pt_s']),
            a(stats['pm_s']), s(stats['pm_s']),
            a(stats['kt_s']), s(stats['kt_s']),
            a(stats['km_s']), s(stats['km_s']),
            a(stats['E_d']), s(stats['E_d']),
            a(stats['pt_d']), s(stats['pt_d']),
            a(stats['pm_d']), s(stats['pm_d']),
            a(stats['kt_d']), s(stats['kt_d']),
            a(stats['km_d']), s(stats['km_d']),
        ])
    # Write CSV
    header = [
        'Vertices',
        'Edges_sparse_avg','Edges_sparse_sd',
        'Prim_sparse_time_avg','Prim_sparse_time_sd',
        'Prim_sparse_mem_avg_kB','Prim_sparse_mem_sd_kB',
        'Kruskal_sparse_time_avg','Kruskal_sparse_time_sd',
        'Kruskal_sparse_mem_avg_kB','Kruskal_sparse_mem_sd_kB',
        'Edges_dense_avg','Edges_dense_sd',
        'Prim_dense_time_avg','Prim_dense_time_sd',
        'Prim_dense_mem_avg_kB','Prim_dense_mem_sd_kB',
        'Kruskal_dense_time_avg','Kruskal_dense_time_sd',
        'Kruskal_dense_mem_avg_kB','Kruskal_dense_mem_sd_kB'
    ]
    with open('lab5_results_enhanced.csv','w',newline='') as f:
        csv.writer(f).writerows([header] + rows)
    print('[Lab5] detailed CSV ➜ lab5_results_enhanced.csv')

    # Extract for plotting
    V = [r[0] for r in rows]
    Es = [r[1] for r in rows]; Ed = [r[11] for r in rows]
    pt_s = [r[3] for r in rows]; pt_s_sd = [r[4] for r in rows]
    kt_s = [r[7] for r in rows]; kt_s_sd = [r[8] for r in rows]
    pm_s = [r[5] for r in rows]; pm_s_sd = [r[6] for r in rows]
    km_s = [r[9] for r in rows]; km_s_sd = [r[10] for r in rows]
    pt_d = [r[13] for r in rows]; pt_d_sd = [r[14] for r in rows]
    kt_d = [r[17] for r in rows]; kt_d_sd = [r[18] for r in rows]
    pm_d = [r[15] for r in rows]; pm_d_sd = [r[16] for r in rows]
    km_d = [r[19] for r in rows]; km_d_sd = [r[20] for r in rows]

    # Helper error-bar plot
    def err_plot(x, y, yerr, label, style, title, xlabel, ylabel, fname):
        plt.figure()
        plt.errorbar(x, y, yerr=yerr, marker=style[0], linestyle=style[1:], capsize=3, label=label)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(); plt.grid(True)
        plt.savefig(fname); plt.close()

    # Sparse Execution Time
    plt.figure()
    plt.errorbar(V, pt_s, yerr=pt_s_sd, marker='o', linestyle='-', capsize=3, label="Prim's Algorithm")
    plt.errorbar(V, kt_s, yerr=kt_s_sd, marker='s', linestyle='-', capsize=3, label="Kruskal's Algorithm")
    plt.title('Execution Time Comparison (Sparse Graph)')
    plt.xlabel('Graph Size (Vertices)')
    plt.ylabel('Time (seconds)')
    plt.legend(); plt.grid(True)
    plt.savefig('lab5_sparse_time.png'); plt.close()

    # Sparse Memory Usage
    plt.figure()
    plt.errorbar(V, pm_s, yerr=pm_s_sd, marker='o', linestyle='-', capsize=3, label="Prim's Algorithm Memory")
    plt.errorbar(V, km_s, yerr=km_s_sd, marker='s', linestyle='-', capsize=3, label="Kruskal's Algorithm Memory")
    plt.title('Memory Usage Comparison (Sparse Graph)')
    plt.xlabel('Graph Size (Vertices)')
    plt.ylabel('Memory (kB)')
    plt.legend(); plt.grid(True)
    plt.savefig('lab5_sparse_mem.png'); plt.close()

    # Dense Execution Time
    plt.figure()
    plt.errorbar(V, pt_d, yerr=pt_d_sd, marker='o', linestyle='--', capsize=3, label="Prim's Algorithm")
    plt.errorbar(V, kt_d, yerr=kt_d_sd, marker='s', linestyle='--', capsize=3, label="Kruskal's Algorithm")
    plt.title('Execution Time Comparison (Dense Graph)')
    plt.xlabel('Graph Size (Vertices)')
    plt.ylabel('Time (seconds)')
    plt.legend(); plt.grid(True)
    plt.savefig('lab5_dense_time.png'); plt.close()

    # Dense Memory Usage
    plt.figure()
    plt.errorbar(V, pm_d, yerr=pm_d_sd, marker='o', linestyle='--', capsize=3, label="Prim's Algorithm Memory")
    plt.errorbar(V, km_d, yerr=km_d_sd, marker='s', linestyle='--', capsize=3, label="Kruskal's Algorithm Memory")
    plt.title('Memory Usage Comparison (Dense Graph)')
    plt.xlabel('Graph Size (Vertices)')
    plt.ylabel('Memory (kB)')
    plt.legend(); plt.grid(True)
    plt.savefig('lab5_dense_mem.png'); plt.close()