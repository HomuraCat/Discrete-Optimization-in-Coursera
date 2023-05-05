#!/usr/bin/python
# -*- coding: utf-8 -*-

def find_maximal_degree (edge, n, forbid):
    node = 0
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        if forbid[i]: continue
        for e in edge[i]:
            if forbid[e]: continue
            degree[i] += 1
    for i in range(1, n + 1):
        if forbid[i]: continue
        if node == 0 or degree[node] < degree[i]:
            node = i
    #print(forbid, degree, node)
    return node

def RLF (edge, n, m):
    vis = [0] * (n + 1)
    color = [0] * (n + 1)
    cnt = 0
    cur_color = -1
    while cnt < n:
        cur_color += 1
        forbid = vis.copy()
        node = find_maximal_degree(edge, n, forbid)
        while node:
            vis[node] = 1
            cnt += 1
            color[node] = cur_color
            forbid[node] = 1
            for e in edge[node]:
                forbid[e] = 1
            node = find_maximal_degree(edge, n, forbid)
    return cur_color + 1, color[1:]

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')
    sys.setrecursionlimit(int(1e9))
    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    edge = [[] for i in range(node_count + 1)]
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        u = int(parts[0]) + 1
        v = int(parts[1]) + 1
        edge[u].append(v)
        edge[v].append(u)
    color_count, solution = RLF(edge, node_count, edge_count)
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
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

