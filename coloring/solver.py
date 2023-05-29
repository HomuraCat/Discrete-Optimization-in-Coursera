#!/usr/bin/python
# -*- coding: utf-8 -*-
import networkx as nx
import time
import sys
from collections import namedtuple
from z3 import *
from random import sample

count = 0
total = 0
Vertex = namedtuple("Vertex", ['i', 'len'])

def check (lamb, k, n):
    T = set()
    c = [0] * (n + 1)
    for i in range(1, n + 1):
        c[i] = set(range(1, k + 1))
    for u in range(1, n + 1):
        if len(c[u]) > 0:
            i = list(c[u])[0]
            c[u] = set([i])
            for v in range(u + 1, n + 1):
                if (u, v, 0) in lamb:
                    c[v] = c[v] - c[u]
                    if len(c[v]) == 0:
                        for w in range(1, u):
                            if (w, v, 1) in lamb and c[w] == c[u]:
                                T.add((w, u, v))
                else:
                    c[v] = set([i]) if i in c[v] else set()
                    if len(c[v]) == 0:
                        for w in range(1, u):
                            if (w, v, 1) in lamb and c[w] != c[u] or (w, v, 0) in lamb and c[w] == c[u]:
                                T.add((w, u, v))

    return T


def sat_build (edge_set, node_num, col_num, T, lamb):
    sat = []
    literals = []
    var_num = 0

    k = col_num
    for (i, j) in edge_set:
        lamb.add((i, j, 0))
    #while 1:
    #    T = check(lamb, k, node_num)
    #    if len(T) == 0:
    #        break
    #    for (u, v, w) in T:
    #        lamb.add((u, v, 0))
    #        lamb.add((u, w, 0))
    #        lamb.add((u, w, 1))
    #        lamb.add((v, w, 0))
    #        lamb.add((v, w, 1))
    #print(len(lamb))
    for i in range(1, node_num + 1):
        for j in range(i + 1, node_num + 1):
            literals.append(Bool(f"s{i, j}"))
            var_num += 1

            if (i, j) in edge_set:
                sat.append([Not(Bool(f"s{i, j}"))])
            for k in range(j + 1, node_num + 1):
                if (i, j, 0) in lamb and (i, k, 0) in lamb and (j, k, 1) in lamb:
                    sat.append([Not(Bool(f"s{i, j}")), Not(Bool(f"s{i, k}")), Bool(f"s{j, k}")])
                if (i, j, 0) in lamb and (j, k, 0) in lamb and (i, k, 1) in lamb:
                    sat.append([Not(Bool(f"s{i, j}")), Not(Bool(f"s{j, k}")), Bool(f"s{i, k}")])
    return sat, literals, var_num

def sat_check (n, k, edge_set):
    sat_instance, literals, var_num = sat_build(edge_set, n, k);
    solver = Optimize()
    for clause in sat_instance:
        solver.add(Or([lit for lit in clause]))
        #print(Or([lit for lit in clause]))
        #solver.add(Or([literals[abs(lit) - 1] if lit > 0 else Not(literals[abs(lit) - 1]) for lit in clause]))
    c = [0] * (n + 1)
    for i in range(2, n + 1):
        c[i] = And([Not(Bool(f"s{j, i}")) for j in range(1, i)])
        #print(c[i])
        #solver.add(c[i])
    solver.add(Sum([If (c[i], 1, 0) for i in range(2, n + 1)]) <= k - 1)
    if solver.check() == sat:
        model = solver.model()
        print(model)
        print(([model.evaluate(c[i]) for i in range(2, n + 1)]))
        print(([model.evaluate(c[i]) for i in range(2, n + 1)]).count(True))

def sat_force (n, edge_set):
    #ans = {50: 6, 70: 17, 100: 16, 200: 78, 500: 16, 1000: 100}
    return sat_check(n, 2, edge_set)

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')
    sys.setrecursionlimit(int(1e9))
    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    edge = [[] for i in range(node_count + 1)]
    edge_set = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        u = int(parts[0]) + 1
        v = int(parts[1]) + 1
        edge[u].append(v)
        edge[v].append(u)
        edge_set.append((u, v))
    start_time = time.time()
    color_count, solution = sat_force(node_count, edge_set)
    end_time = time.time()
    output_data = str(color_count) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
        solver.add_soft(c[i], weight=1)
        solver.add_soft(c[i], weight=1)
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

