#!/usr/bin/python3

def sum_table(list):
    sum = 0
    for i in range(0, len(list)):
        for j in range(0, len(list[i])):
            sum += list[i][j]
    return sum

import sys

myfile = open(sys.argv[1], "r")

line1 = myfile.readline().split()
nr_alfabeti = int(line1[0])
alfabeti = [x for x in line1[1:]]

line2 = myfile.readline().split()
nr_gjendje = int(line2[0])
gjendje = [int(x) for x in line2[1:]]

line3 = myfile.readline().split()
nr_gjendje_perfundimtare = int(line3[0])
gjendje_perfundimtare = [int(x) for x in line3[1:]]

gjendje_fillestare = int(myfile.readline().split()[0])

print("Automati i fundem jo-determinist me epsilon kalime me karaktere %s, me gjendje %s, gjendje fillestare [%d] dhe gjendje perfundimtare %s" %(alfabeti, gjendje, gjendje_fillestare, gjendje_perfundimtare))

# Data structure
# [
#     [
#         [...],
#         [...],
#         ...
#     ],
#     ...
# ]

data = [[[] for i in range(0, nr_alfabeti)] for j in range(0, nr_gjendje)]

for i in range(0, nr_gjendje):
    for j in range(0, nr_alfabeti):
        line = myfile.readline().split()
        line = [int(x) for x in line]
        data[i][j] = line[1:]

print("\nAUTOMATI I FUNDEM DETERMINIST")
print("=============================")

for i in range(0, nr_gjendje):
    for j in range(0, nr_alfabeti):
        print("[{}] --{}-> [{}]".format(gjendje[i], alfabeti[j], data[i][j][0]), end="")
        if data[i][j][0] in gjendje_perfundimtare:
            print("[F]")
        else:
            print("")

myfile.close()

# Minimization of AFD

gjendjet_arritshme = [gjendje_fillestare]
for i in range(0, nr_gjendje):
    for j in range(0, nr_alfabeti):
        if data[i][j][0] != i:
            gjendjet_arritshme.append(data[i][j][0])

for c in gjendje:
    if c not in gjendjet_arritshme:
        gjendje.remove(c)
        nr_gjendje += -1

klasa_ekuivalence = [[], []]

klasa_ekuivalence[0] = [x for x in gjendje if x not in gjendje_perfundimtare]
klasa_ekuivalence[1] = [x for x in gjendje_perfundimtare]

table = [[0]*nr_gjendje for i in range(0, nr_gjendje)]

for i, r in enumerate(gjendje):
    for j, c in enumerate(gjendje):

        if r in klasa_ekuivalence[0] and c in klasa_ekuivalence[1] or r in klasa_ekuivalence[1] and c in klasa_ekuivalence[0] or j > i:
            table[i][j] = 1
        if i == j:
            table[i][j] = -1

print(table)

flag = True

while flag:

    gjendjet_tolook = []
    for i in range(1, nr_gjendje):
        for j in range(0, i):
            if table[i][j] == 0:
                gjendjet_tolook.append([i, j])

    s1 = sum_table(table)

    for pair in gjendjet_tolook:
        for c in range(0, nr_alfabeti):
            q1 = gjendje[pair[0]]
            q2 = gjendje[pair[1]]

            q1_c = data[q1][c][0]
            q2_c = data[q2][c][0]

            q1_r = gjendje.index(q1_c)
            q2_r = gjendje.index(q2_c)

            if table[q1_r][q2_r] == 1:
                table[pair[0]][pair[1]] = 1

    s2 = sum_table(table)
    if s1 == s2:
        flag = False

print("Gjendjet e automatit jane:")
print(gjendje)

if gjendjet_tolook:
    print("Gjendjet ekuivalente jane ciftet e gjendjeve:")
    
    for x in gjendjet_tolook:
        print("[{}, {}]".format(gjendje[x[0]], gjendje[x[1]]))
else:
    print("Automati eshte i determinizuar")