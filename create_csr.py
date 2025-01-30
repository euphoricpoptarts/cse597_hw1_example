def create_csr(adj, n):
    # remove duplicates
    adj = [tuple(set(x)) for x in adj]
    row_map = [len(x) for x in adj]
    row_map.append(0)

    sum = 0
    for i in range(n + 1):
        sum = sum + row_map[i]
        row_map[i] = sum

    entries = [0 for i in range(sum)]
    j = 0
    for x in adj:
        for v in x:
            entries[j] = v
            j = j + 1

    return row_map, entries