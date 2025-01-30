from create_csr import create_csr

def create_csr_from_edge_pairs(sources, dests, n):
    adj = [[] for i in range(n)]

    for i in range(n):
        u = sources[i]
        v = dests[i]
        adj[u].append(v)
        adj[v].append(u)

    return create_csr(adj, n)