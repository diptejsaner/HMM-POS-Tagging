import json
import sys
from operator import itemgetter


def get_pos_tags_viterbi(line):
    #line = line.lower()
    words = line.split(' ')
    pos_tags = []

    probs = [[0 for i in range(len(words))] for j in range(len(tg) + 1)]
    backpointer = [[0 for i in range(len(words))] for j in range(len(tg))]

    states = [s for s in tg]

    words[-1] = words[-1].rstrip()
    sindex = 0
    for state in states:
        if words[0] in eg[state] and state in tg["q0"]:
            probs[sindex][0] = tg["q0"][state] * eg[state][words[0]]
        sindex += 1

    for windex in range(1, len(words)):
        word = words[windex]
        for sindex in range(0, len(states)):
            plist = []
            state = states[sindex]
            # loop for calculating the max
            for ind in range(0, len(states)):
                prevstate = states[ind]
                if state in tg[prevstate] and word in eg[state]:
                    p = probs[ind][windex - 1] * eg[state][word] * tg[prevstate][state]
                    plist.append([ind, p])
                else:
                    plist.append([ind, 0])

            smax, pmax = max(plist, key=itemgetter(1))
            probs[sindex][windex] = pmax
            backpointer[sindex][windex] = smax

    maxp = probs[0][-1]
    ind = -1
    for sindex in range(0, len(states)):
        if maxp < probs[sindex][-1]:
            maxp = probs[sindex][-1]
            ind = sindex

    pos_tags.append(states[ind])
    for col in range(len(words) - 1, 0, -1):
        pos_tags.append(states[backpointer[ind][col]])
        ind = backpointer[ind][col]

    pos_tags.reverse()
    return pos_tags


def tag_sentence(line, pos_tags):
    words = line.split(' ')
    tagged_words = []

    for word, tag in list(zip(words, pos_tags)):
        word = word.rstrip()
        word += "/" + tag
        tagged_words.append(word)

    tagged_words[-1] += "\n"

    return " ".join(tagged_words[:])


tg = {}
eg = {}

with open('hmmmodel.txt', 'r', encoding='utf8') as f:
    str = f.readlines()
    tg = json.loads(str[0])
    eg = json.loads(str[1])

# with open('emissionMatrix.json', 'r', encoding='utf8') as f:
#    eg = json.load(f)

outputFile = open("hmmoutput.txt", "w", encoding='utf8')

with open(sys.argv[1]) as f:
    pos_tags = []
    for line in f:
        pos_tags = get_pos_tags_viterbi(line)
        outputFile.write(tag_sentence(line, pos_tags))

outputFile.close()