import csv
import time
from create_csr_from_edge_pairs import create_csr_from_edge_pairs
from output_metis import output_metis

ids = {}

# convert string id to integer id
def get_cont_id(name):
    global ids
    total = len(ids)
    if name not in ids:
        ids[name] = total
        return total
    else:
        return ids[name]

# each edge (u, v) is represented as sources[x] = u; dests[x] = v for some index x
sources = []
dests = []

start = time.time()

with open('title.crew.tsv', 'r') as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    # skip header
    next(tsv_reader)
    for row in tsv_reader:
        title = row[0]
        tid = get_cont_id(title)
        directors = row[1]
        crew = row[2]
        if directors != "\\N":
            names = directors.split(",")
            for name in names:
                nid = get_cont_id(name)
                sources.append(tid)
                dests.append(nid)
        if crew != "\\N":
            names = crew.split(",")
            for name in names:
                nid = get_cont_id(name)
                sources.append(tid)
                dests.append(nid)

with open('title.principals.tsv', 'r', encoding="utf8") as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    # skip header
    next(tsv_reader)
    for row in tsv_reader:
        title = row[0]
        name = row[2]
        tid = get_cont_id(title)
        nid = get_cont_id(name)
        sources.append(tid)
        dests.append(nid)

parse_end = time.time()

total_ids = len(ids)
# clear ids mapping to save memory
# could also export this to file for later usage
ids.clear()

print(parse_end - start)
print(len(sources))

row_map, entries = create_csr_from_edge_pairs(sources, dests, total_ids)

end_create = time.time()
print(end_create - parse_end)
output_metis(row_map, entries, "imdb_1.graph")