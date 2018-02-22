import json
import sys

f = open(sys.argv[1], "r", encoding='utf8')

tg = {}
eg = {}

line_count = 0
word_count = 0

first_tag_prob = {}
word_set = set()

for line in f:
    words = line.split(' ')
    k = 0
    prev = ""

    for word in words:
        x = word.split('/')

        x[0:-1] = ["/".join(x[0:-1])]
        w = x[0].lower()
        # w = x[0]
        word_set.add(w)

        tag = x[-1].rstrip()

        if k == 0:
            if tag not in first_tag_prob:
                first_tag_prob[tag] = 1
            else:
                first_tag_prob[tag] += 1

        if prev != "":
            if tag in tg[prev]:
                tg[prev][tag] += 1
            else:
                tg[prev][tag] = 1

        if tag not in tg:
            tg[tag] = {}

        if tag not in eg:
            eg[tag] = {}
            eg[tag][w] = 1
        elif w not in eg[tag]:
            eg[tag][w] = 1
        else:
            eg[tag][w] += 1

        prev = tag
        word_count += 1
        k += 1
    line_count += 1

initial_transition = {}

for node in first_tag_prob:
    first_tag_prob[node] /= line_count
    initial_transition[node] = first_tag_prob[node]

f.close()

# add one smoothing
tag_set = set()
for tag in tg:
    tag_set.add(tag)

for tag in tg:
    for ts in tag_set:
        if ts not in tg[tag]:
            tg[tag][ts] = 1
        else:
            tg[tag][ts] += 1

'''
for tag in eg:
    for ts in tag_set:
        if ts not in eg[tag]:
            eg[tag][ts] = 1
        else:
            eg[tag][ts] += 1
'''

for tag in tag_set:
    if tag in initial_transition:
        initial_transition[tag] += 1
        initial_transition[tag] /= len(tag_set)
    else:
        initial_transition[tag] = 1/len(tag_set)

# get count of words from each tag
word_count_from_tag = {}

# convert to probabilities
for tag in tg:
    count = 0

    for t in tg[tag]:
        count += tg[tag][t]

    for t in tg[tag]:
        tg[tag][t] /= count

for tag in eg:
    count = 0

    for wd in eg[tag]:
        count += eg[tag][wd]

    for wd in eg[tag]:
        eg[tag][wd] /= count
        word_count_from_tag[tag] = count

with open('hmmmodel.txt', 'w', encoding='utf8') as fp:
    fp.write(json.dumps(tg, ensure_ascii=False))
    fp.write("\n")
    fp.write(json.dumps(eg, ensure_ascii=False))
    fp.write("\n")
    fp.write(json.dumps(initial_transition, ensure_ascii=False))
    fp.write("\n")
    fp.write(json.dumps(list(word_set), ensure_ascii=False))
    fp.write("\n")
    fp.write(json.dumps(word_count_from_tag, ensure_ascii=False))
