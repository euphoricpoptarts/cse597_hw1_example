from itertools import chain

def create_csr(adj, n):
    # remove duplicates 
    # replace elements of adj in-place to save memory
    adj[:] = [tuple(set(x)) for x in adj]
    row_map = [len(x) for x in adj]
    row_map.append(0)

    # exclusive prefix sum over row_map
    sum = 0
    for i in range(n + 1):
        val = row_map[i]
        row_map[i] = sum
        sum = sum + val

    entries = list(chain.from_iterable(adj))

    return row_map, entries