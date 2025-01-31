from create_csr import create_csr

def create_csr_from_edge_pairs(sources, dests, n):
    adj = [[] for i in range(n)]

    for i in range(len(sources)):
        u = sources[i]
        v = dests[i]
        # add edges to appropriate adjacency lists
        adj[u].append(v)
        adj[v].append(u)
    # clear these lists to save memory
    sources.clear()
    dests.clear()

    return create_csr(adj, n)