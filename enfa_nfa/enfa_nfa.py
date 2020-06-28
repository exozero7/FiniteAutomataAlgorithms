#!/usr/bin/env python3

import sys
from graphviz import Digraph

myfile = open(sys.argv[1], "r")

line1 = myfile.readline().split()
nr_alfabeti = int(line1[0])
alfabeti = [x for x in line1[1:]]
alfabeti.append('ε')

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

myfile.close()

print("\nAUTOMATI I FUNDEM JODETERMINIST ME EPSILON KALIME")
print("=================================================")

for i in range(0, nr_gjendje):
    for j in range(0, nr_alfabeti):
        for k in data[i][j]:
            print("[{}] --{}-> [{}]".format(gjendje[i], alfabeti[j], k), end="")
            if k in gjendje_perfundimtare:
                print("[F]")
            else:
                print("")

dataNFA = [[[] for i in range(0, nr_alfabeti-1)] for j in range(0, nr_gjendje)]

f = Digraph('nfa', filename='nfa.gv')
f.attr(rankdir='LR', size='8')

for i in range(0, nr_gjendje):
    
    gjendjet_epsilon_1 = data[i][nr_alfabeti-1].copy()

    gjendjet_epsilon_patrajtuara_1 = gjendjet_epsilon_1[1:].copy()

    while gjendjet_epsilon_patrajtuara_1:
        g = gjendjet_epsilon_patrajtuara_1.pop(0)
        for l in data[g][nr_alfabeti-1]:
            if l not in gjendjet_epsilon_patrajtuara_1 and l not in gjendjet_epsilon_1:
                gjendjet_epsilon_patrajtuara_1.append(l)
            if l not in gjendjet_epsilon_1:
                gjendjet_epsilon_1.append(l)

    for x in gjendjet_epsilon_1:
        if x in gjendje_perfundimtare and i not in gjendje_perfundimtare:
            gjendje_perfundimtare.append(i)

    for m in range(0, nr_alfabeti-1):
        gjendjet_epsilon_2 = []

        for n in gjendjet_epsilon_1:
            gjendje_kalueshme = []
            for o in data[n][m]:
                gjendje_kalueshme.append(o)
            
            gjendje_individuale_epsilon = []
            
            gjendje_kalueshme_patrajtuara = gjendje_kalueshme.copy()
            while gjendje_kalueshme_patrajtuara:
                gj = gjendje_kalueshme_patrajtuara.pop(0)
                for x in data[gj][nr_alfabeti-1]:
                    if x not in gjendje_individuale_epsilon:
                        gjendje_individuale_epsilon.append(x)
                    if x not in gjendje_kalueshme_patrajtuara and x not in gjendje_individuale_epsilon:
                        gjendje_kalueshme_patrajtuara.append(x)

            for c in gjendje_individuale_epsilon:
                if c not in gjendjet_epsilon_2:
                    gjendjet_epsilon_2.append(c)
        
        dataNFA[i][m] = gjendjet_epsilon_2

print("\nAUTOMATI I FUNDEM JODETERMINIST")
print("===============================")

for i in range(0, nr_gjendje):
    for j in range(0, nr_alfabeti-1):
        for k in dataNFA[i][j]:

            print("[{}] --{}-> [{}]".format(gjendje[i], alfabeti[j], k), end="")
            if k in gjendje_perfundimtare:
                f.attr('node', shape='doublecircle')
                f.node(str(gjendje[i]))
                f.edge(str(gjendje[i]), str(k), label=str(alfabeti[j]))
                print("[F]")
            else:
                f.attr('node', shape='circle')
                f.node(str(gjendje[i]))
                f.edge(str(gjendje[i]), str(k), label=str(alfabeti[j]))
                print("")

prompt = input("Shfaq paraqitjen grafike [Y][N]: ")

if prompt in ['Y', 'y']:
    f.view()
