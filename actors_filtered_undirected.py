import csv
import time
from create_csr_from_edge_pairs import create_csr_from_edge_pairs
from output_metis import output_metis

tids = {}
nids = {}
title_filter = set()
name_filter = set()

def get_cont_id(name, container):
    total = len(container)
    if name not in container:
        container[name] = total
        return total
    else:
        return container[name]

cliques = []

start = time.time()

with open('title.basics.tsv', 'r', encoding="utf8") as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    # skip header
    next(tsv_reader)
    for row in tsv_reader:
        title = row[0]
        tt = row[1]
        if tt != "movie":
            continue
        adult = row[4]
        if adult != "0":
            continue
        year = row[5]
        if year == "\\N":
            continue
        if int(year) <= 2000:
            continue
        title_filter.add(title)

with open('name.basics.tsv', 'r', encoding="utf8") as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    # skip header
    next(tsv_reader)
    for row in tsv_reader:
        name = row[0]
        death = row[3]
        if death != "\\N":
            continue
        name_filter.add(name)

with open('title.principals.tsv', 'r', encoding="utf8") as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    # skip header
    next(tsv_reader)
    for row in tsv_reader:
        title = row[0]
        order = int(row[1])
        if order > 5:
            continue
        if title not in title_filter:
            continue
        name = row[2]
        if name not in name_filter:
            continue
        role = row[3]
        if role != "actor" and role != "actress":
            continue
        tid = get_cont_id(title, tids)
        nid = get_cont_id(name, nids)
        if(len(cliques) < len(tids)):
            cliques.append(set())
        cliques[tid].add(nid)

parse_end = time.time()

print(parse_end - start)

cliques = [list(x) for x in cliques]

sources = []
dests = []

for clique in cliques:
    for i in range(0, len(clique)):
        for j in range(i + 1, len(clique)):
            if clique[i] != clique[j]:
                sources.append(clique[i])
                dests.append(clique[j])

row_map, entries = create_csr_from_edge_pairs(sources, dests, len(nids))

end_create = time.time()
print(end_create - parse_end)
output_metis(row_map, entries, "imdb_3.graph")