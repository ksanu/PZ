#https://nlp.stanford.edu/projects/glove/

#from scipy.spatial.distance import cosine
import math
fs = open("C:\\Users\\s0146074\\Desktop\\glove.6B.100d.txt", 'r', encoding = 'utf8')

def cosine(v1, v2):
    v1v2 = 0
    for i in range(100):
        v1v2 += v1[i] * v2[i]
    v1norm = 0
    for i in range(100):
        v1norm += v1[i] * v1[i]
    v1norm = math.sqrt(v1norm)
    v2norm = 0
    for i in range(100):
        v2norm += v2[i] * v2[i]
    v2norm = math.sqrt(v2norm)
    return v1v2/(v1norm*v2norm)

def TOEFLparser(filename):
    tF = open(filename, 'r')
    state = 0
    question_words = []
    possibilities_bag = []
    answers = []
    for line in tF:
        if len (line.split()) == 0:
            question_words.append(question_word)
            possibilities_bag.append(possibilities)
            state = 0
        elif len(line.split()) == 2:
            if state == 1:
                possibilities.append(line.split()[1])
            if state == 0:
                question_word = line.split()[1]
                possibilities = []
                state = 1


model = {}
for i, line in enumerate(fs):
    if i%1000 == 0:
        print(i)
    tokens = line.split()
    vec = [0 for i in range(100)]
    for i in range(100):
        vec[i] = float(tokens[i+1])
    model[tokens[0]] = vec


king_vec = model["king"]
queen_vec = model["queen"]
man_vec = model["men"]
woman_vec = model["woman"]

print(cosine(king_vec, queen_vec))
print(cosine(king_vec, man_vec))
print(cosine(queen_vec, woman_vec))


