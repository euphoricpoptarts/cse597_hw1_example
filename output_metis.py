def output_metis(row_map, entries, fname):
    n = len(row_map) - 1
    with open(fname, "w") as f:
        print("{} {}".format(n, len(entries)//2), file=f)
        for i in range(n):
            row = entries[row_map[i]:row_map[i+1]]
            row = [str(x + 1) for x in row]
            print(" ".join(row), file=f)