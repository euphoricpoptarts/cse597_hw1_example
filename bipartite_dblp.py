from parse import *
from create_csr import create_csr
import time
docs = []

mkultra_activation_code = "<inproceedings"
mkultra_deactivation_code = "</inproceedings>"
activated = False

start = time.time()

with open("dblp-2019-04-01.xml", "r", encoding="utf8") as file:
    for line in file:
        if line.isspace():
            continue
        if activated:
            index = line.find(mkultra_deactivation_code)
            if index != -1:
                activated = False
            else:
                docs[-1].append(line)
        if not activated:
            index = line.find(mkultra_activation_code)
            if index != -1:
                activated = True
                docs.append([])

author_lists = []

end_import = time.time()
print(end_import - start)

for doc in docs:
    authors = []
    for line in doc:
        author_begin = line.find("<author>")
        if author_begin != -1:
            author_end = line.find("</author>")
            author = line[author_begin + 8:author_end]
            authors.append(author)
    author_lists.append(authors)

end_parse = time.time()
total_titles = len(author_lists)
print(total_titles)
print(end_parse - end_import)

author_id = {}

def get_cont_id(name, container):
    total = len(container)
    if name not in container:
        container[name] = total
        return total
    else:
        return container[name]

for list in author_lists:
    for i in range(len(list)):
        author = list[i]
        id = get_cont_id(author, author_id)
        list[i] = id

total_authors = len(author_id)
print(total_authors)
title_lists = [[] for i in range(total_authors)]

for i in range(len(author_lists)):
    for id in author_lists[i]:
        title_lists[id].append(i + total_authors)

adj_lists = title_lists + author_lists

row_map, entries = create_csr(adj_lists, total_authors + total_titles)
end = time.time()
print(end - end_parse)