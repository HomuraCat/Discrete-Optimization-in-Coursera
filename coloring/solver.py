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


def sat_build (edge_set, node_num, col_num):
    sat = []
    literals = []
    var_num = 0
    k = col_num
    for i in range(1, node_num + 1):
        for j in range(i + 1, node_num + 1):
            literals.append(Bool(f"s{i, j}"))
            var_num += 1

            if (i, j) in edge_set:
                sat.append([Not(Bool(f"s{i, j}"))])
    return sat, literals, var_num
ans = 0
def sat_check (solver, n, k, edge_set, T):

    for (i, j, k) in T:
        solver.add(Or([Not(Bool(f"s{i, j}")), Not(Bool(f"s{i, k}")), Bool(f"s{j, k}")]))
        solver.add(Or([Not(Bool(f"s{i, j}")), Not(Bool(f"s{j, k}")), Bool(f"s{i, k}")]))
    global ans
    if solver.check() == sat:
        model = solver.model()
        #print(model)
        #print(([model.evaluate(c[i]) for i in range(2, n + 1)]))
        #print(([model.evaluate(c[i]) for i in range(2, n + 1)]).count(True))
        #print("HERE")
        lamb = set()
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                lamb.add((i, j, 1 if model[(Bool(f"s{i, j}"))] else 0))
        T = check(lamb, k, n)
        #print(len(T))
        ans += len(T)
        print(ans)
        #print(T)
        if len(T) > 0:
            return sat_check(solver, n, k, edge_set, T)
        else:
            print(model)
            return True
    else:
        return False

def sat_force (n, edge_set):
    #ans = {50: 6, 70: 17, 100: 16, 200: 78, 500: 16, 1000: 100}
    solver = Optimize()
    k = 4
    sat_instance, literals, var_num = sat_build(edge_set, n, k);
    for clause in sat_instance:
        solver.add(Or([lit for lit in clause]))

####
    c = [0] * (n + 1)
    for i in range(2, n + 1):
        c[i] = And([Not(Bool(f"s{j, i}")) for j in range(1, i)])
    solver.add(Sum([If (c[i], 1, 0) for i in range(2, n + 1)]) <= k - 1)

    if not sat_check(solver, n, k, edge_set, set()):
        print("miao")

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

