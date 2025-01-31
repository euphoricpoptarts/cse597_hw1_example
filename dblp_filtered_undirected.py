from parse import *
from create_csr_from_edge_pairs import create_csr_from_edge_pairs
import time
from output_metis import output_metis

filter = set(["Mohamed Almekkawy",
             "Anton Bankevich",
             "Antonio Blanca",
             "Guohong Cao",
             "Kyusun Choi",
             "Robert Collins",
             "Griselda L&oacute;pez",
             "Christopher L. Dancy",
             "Chita R. Das",
             "Debarati Das 0001",
             "Debarati Das 0002",
             "Debarati Das 0003",
             "Mahfuza Farooque",
             "Junichiro Fukuyama",
             "Martin F&uuml;rer",
             "Oren Z. Gall",
             "Swaroop Ghosh",
             "Mahanth Gowda",
             "Sean Hallgren",
             "Ting He",
             "Ting He 0001",
             "Krishna Kambhampaty",
             "Mahmut T. Kandemir",
             "George Kesidis",
             "Arslan Khan",
             "Daniel Kifer",
             "Young Kun Ko",
             "David Koslicki",
             "Thomas F. La Porta",
             "Wang-Chien Lee",
             "Bin Li",
             "Yanxi Liu",
             "Kamesh Madduri",
             "Kiwan Maeng",
             "Mehrdad Mahdavi",
             "Mark Mahon",
             "Paul Medvedev",
             "Shagufta Mehnaz",
             "Vijaykrishnan Narayanan",
             "Ruslan Nikolaev 0001",
             "Ruslan Nikolaev 0002",
             "Rebecca J. Passonneau",
             "Yana Safonova",
             "Suman Saha",
             "John (Jack) Morgan Sampson",
             "Steven Shaffer",
             "Mingfu Shao",
             "Irish Singh",
             "Madhusudan Singh",
             "Anand Sivasubramaniam",
             "Gang Tan",
             "Bhuvan Urgaonkar",
             "Abhinav Verma",
             "Chunhao Wang",
             "Pei Wu",
             "Dong Xie",
             "Dong Xie 0001",
             "Dong Xie 0002",
             "Dong Xie 0003",
             "Dong Xie 0004",
             "Huijuan Xu",
             "Wenpeng Yin 0001",
             "Rui Zhang",
             "Sencun Zhu",
             "Timothy Zhu"])

author_lists = []

mkultra_activation_code = "<inproceedings"
mkultra_deactivation_code = "</inproceedings>"
code2 = "<article"
de_code2 = "</article>"
informal = "publtype=\"informal\""
activated = 0

start = time.time()

author_tags = 0

with open("dblp.xml", "r", encoding="utf8") as file:
    for line in file:
        if line.isspace():
            continue
        if activated > 0:
            deactivate = mkultra_deactivation_code
            if activated == 2:
                deactivate = de_code2
            # check for appropriate close tag
            index = line.find(deactivate)
            if index != -1:
                activated = 0
            elif line.find("<author") != -1:
                # only add lines with an author tag
                author_lists[-1].append(line)
                author_tags = author_tags + 1
        if activated == 0:
            index = line.find(mkultra_activation_code)
            # check for open inproceedings tag
            if index != -1:
                activated = 1
            if activated == 0:
                #check for open article tag
                index = line.find(code2)
                if index != -1:
                    activated = 2
            if index > -1:
                # check if document is not informal
                if line[index:].find(informal) == -1:
                    author_lists.append([])
                else:
                    activated = 0

end_import = time.time()
print(end_import - start)
print("Total author tags: {}".format(author_tags))

def extract_author_name(line):
    # find start of open author tag
    author_begin = line.find("<author")
    # find end of open author tag
    author_begin = line[author_begin:].find(">")
    # find start of close author tag
    author_end = line.find("</author>")
    author = line[author_begin + 1:author_end]
    return author

author_lists = [[extract_author_name(x) for x in y] for y in author_lists]
author_lists = [tuple([x for x in y if x in filter]) for y in author_lists]

end_parse = time.time()
total_titles = len(author_lists)
print(end_parse - end_import)

author_id = {}

def get_cont_id(name, container):
    total = len(container)
    if name not in container:
        container[name] = total
        return total
    else:
        return container[name]

author_lists = [tuple([get_cont_id(x, author_id) for x in y]) for y in author_lists]

total_authors = len(author_id)

sources = []
dests = []

for clique in author_lists:
    for i in range(0, len(clique)):
        for j in range(i + 1, len(clique)):
            sources.append(clique[i])
            dests.append(clique[j])

row_map, entries = create_csr_from_edge_pairs(sources, dests, total_authors)

end = time.time()
print(end - end_parse)
output_metis(row_map, entries, "dblp_3.graph")