import json
import sys
from operator import itemgetter


def get_pos_tags_viterbi(line):
    line = line.lower()
    words = line.split(' ')
    pos_tags = []

    probs = [[0 for i in range(len(words))] for j in range(len(tg))]
    backpointer = [[0 for i in range(len(words))] for j in range(len(tg))]

    states = [s for s in tg]

    words[-1] = words[-1].rstrip()

    sindex = 0
    for state in states:
        if words[0] in eg[state] and state in initial_transition:
            probs[sindex][0] = initial_transition[state] * eg[state][words[0]]
        sindex += 1

    for windex in range(1, len(words)):
        word = words[windex]

        if word not in word_set:
            for s in word_count_from_tag:
                eg[s][word] = 1 / (word_count_from_tag[s] + len(word_set))

        for sindex in range(0, len(states)):
            plist = []
            state = states[sindex]

            for ind in range(0, len(states)):
                prevstate = states[ind]

                # known word
                if state in tg[prevstate] and word in eg[state]:
                    p = probs[ind][windex - 1] * eg[state][word] * tg[prevstate][state]
                else:
                    p = 0

                plist.append([ind, p])

            smax, pmax = max(plist, key=itemgetter(1))
            probs[sindex][windex] = pmax
            backpointer[sindex][windex] = smax

        '''
        # check if column is 0
        flag = False
        for i in range(0, len(states)):
            if probs[i][windex] != 0:
                flag = True
                break
                
        if flag == True:
            print("non-zero")
        else:
            print("zero")
        '''

    maxp = probs[0][-1]
    ind = -1
    for sindex in range(0, len(states)):
        if maxp < probs[sindex][-1]:
            maxp = probs[sindex][-1]
            ind = sindex

    if ind == -1:
        pos_tags.append(states[10])
    else:
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

    return " ".join(tagged_words[:])


tg = {}
eg = {}
initial_transition = {}

with open('hmmmodel.txt', 'r', encoding='utf8') as f:
    str = f.readlines()
    tg = json.loads(str[0])
    eg = json.loads(str[1])
    initial_transition = json.loads(str[2])
    word_set = json.loads(str[3])
    word_count_from_tag = json.loads(str[4])

outputFile = open("hmmoutput.txt", "w", encoding='utf8')

with open(sys.argv[1]) as f:
    pos_tags = []
    for line in f:
        pos_tags = get_pos_tags_viterbi(line)
        tagged_line = tag_sentence(line, pos_tags)
        outputFile.write(tagged_line + "\n")

outputFile.close()
