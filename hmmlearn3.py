import json
import sys

f = open(sys.argv[1], "r", encoding='utf8')

tg = {}
eg = {}

line_count = 0
word_count = 0

first_tag_prob = {}

for line in f:
    words = line.split(' ')
    k = 0
    prev = ""

    for word in words:
        x = word.split('/')

        x[0:-1] = ["/".join(x[0:-1])]
        w = x[0].lower()
        #w = x[0]

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

eg["q0"] = {}
tg["q0"] = {}
for node in first_tag_prob:
    # first_tag_prob[node] /= line_count
    tg["q0"][node] = first_tag_prob[node]

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

# print("\nNumber of lines : " + str(line_count))
# print("\nnumber of tags found : " + str(len(tg)))

with open('hmmmodel.txt', 'w', encoding='utf8') as fp:
    fp.write(json.dumps(tg, ensure_ascii=False))
    fp.write("\n")
    fp.write(json.dumps(eg, ensure_ascii=False))
    fp.write("\n")

# with open('emissionMatrix.json', 'w', encoding='utf8') as fp:
#    json.dump(eg, fp, ensure_ascii=False)


'''with open("/Users/diptejsaner/Desktop/NLP_HMM/transitionMatrix.txt", "w") as file:
	for node in tg:
		tags.append(node)
		file.write("%s " % node)

	file.write("\n")

	for node in tags:
		for adjNode in tags:
			if adjNode in tg[node]:
				file.write("%f " % tg[node][adjNode])
			else:
				file.write("%i " % 0)
		file.write("\n")

with open("/Users/diptejsaner/Desktop/NLP_HMM/emissionMatrix.txt", "w") as file:
	for tag in tags:
		file.write("%s " % tag)
	file.write("\n")

	for word in wordset:
		file.write("%s " % word)
	file.write("\n")

	ind = 0
	for node in tags:
		ind = 0
		for eword in wordset:
			if eword in eg[node]:
				file.write("%i:%f " % (ind, eg[node][eword]))
			ind += 1
		file.write("\n")
'''
