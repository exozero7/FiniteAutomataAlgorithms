#!/usr/bin/python3 

from graphviz import Digraph
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

print("Automati i fundem jodeterminist me karaktere %s, me gjendje %s, gjendje fillestare [%d] dhe gjendje perfundimtare %s" %(alfabeti, gjendje, gjendje_fillestare, gjendje_perfundimtare))

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

for i in range(0, nr_gjendje):
    for j in range(0, nr_alfabeti):
        for k in data[i][j]:
            print("[{}] --{}-> [{}]".format(gjendje[i], alfabeti[j], k), end="")
            if k in gjendje_perfundimtare:
                print("[F]")
            else:
                print("")

myfile.close()

print("\nAUTOMATI I FUNDEM DETERMINIST")
print("=============================")

gjendjet_patrajtuara = [[gjendje_fillestare]]
gjendjet_trajtuara = []
error_state_exist = 0

dataDFA = [[[] for i in range(0, nr_alfabeti)] for j in range(0, nr_gjendje)]

# GUI
f = Digraph('dfa', filename='dfa.png')
f.attr(rankdir='LR', size='8')

while gjendjet_patrajtuara:
    
    gjendje_trajtohet = gjendjet_patrajtuara[0]

    for i in range(0, nr_alfabeti):
        gjendje_sapoformuar = []
        for gjendje_individuale in gjendje_trajtohet:
            for j in data[gjendje_individuale][i]:
                if j not in gjendje_sapoformuar:
                    gjendje_sapoformuar.append(j)
        gjendje_sapoformuar.sort()

        check = any(item in gjendje_sapoformuar for item in gjendje_perfundimtare)

        ### GUI ###

        if check:
            f.attr('node', shape='doublecircle')
            f.node(str(gjendje_sapoformuar))
            f.edge(str(gjendje_trajtohet), str(gjendje_sapoformuar), label=str(alfabeti[i]))
        else:
            f.attr('node', shape='circle')
            f.node(str(gjendje_sapoformuar))
            f.edge(str(gjendje_trajtohet), str(gjendje_sapoformuar), label=str(alfabeti[i]))

        ### GUI ###

        print("{} --{}-> ".format(gjendje_trajtohet, alfabeti[i]), end="")

        if not gjendje_sapoformuar:
            print("[D]")
            error_state_exist = 1
        elif check:
            print(str(gjendje_sapoformuar) + "[F]")
        else:
            print(str(gjendje_sapoformuar))

        if gjendje_sapoformuar not in gjendjet_patrajtuara and gjendje_sapoformuar not in gjendjet_trajtuara and gjendje_sapoformuar:
            gjendjet_patrajtuara.append(gjendje_sapoformuar)

    gjendjet_trajtuara.append(gjendjet_patrajtuara.pop(0))

if error_state_exist:
    for c in alfabeti:
        print("[D] --{}-> [D]".format(c))

prompt = input("Shfaq paraqitjen grafike [Y][N]: ")

if prompt in ['Y', 'y']:
    f.view()