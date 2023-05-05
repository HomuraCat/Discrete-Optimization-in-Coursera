#!/usr/bin/python
# -*- coding: utf-8 -*-
import networkx as nx
import time
import sys
def brute_dfs (n, edge, cur_color, color_num):
    if n == 0: return True
    select_color = set(range(1, color_num + 1))
    for e in edge[n]:
        if cur_color[e] > 0 and cur_color[e] in select_color:
            select_color.remove(cur_color[e])
    #print(cur_color, n, select_color)
    for i in select_color:
        cur_color[n] = i
        flag = brute_dfs(n - 1, edge, cur_color, color_num)
        if flag: return True
        cur_color[n] = 0
    return False

def brute_force (edge, n, m):
    l, r = 1, n
    ans_color = []
    while l < r:
        mid = (l + r) // 2
        cur_color = [0 for i in range(n + 1)]
        if brute_dfs(n, edge, cur_color, mid):
            r = mid
            ans_color = cur_color[1:].copy()
            for i in range(n): ans_color[i] -= 1
        else:
            l = mid + 1
    return r, ans_color

def trick_dfs (d, n, edge, cur_color, color_num, neighbor_color):
    if d == n + 1: return True
    max_len = -1
    for i in range(1, n + 1):
        if cur_color[i]: continue
        if len(neighbor_color[i]) > max_len:
            max_len = len(neighbor_color[i])
            max_pos = i
    for i in range(1, color_num + 1):
        if i in neighbor_color[max_pos]: continue
        cur_color[max_pos] = i
        for e in edge[max_pos]:
            if i in neighbor_color[e]:
                neighbor_color[e][i] += 1
            else:
                neighbor_color[e][i] = 1
        flag = dfs(d + 1, n, edge, cur_color, color_num, neighbor_color)
        if flag: return True
        for e in edge[max_pos]:
            if neighbor_color[e][i] > 1:
                neighbor_color[e][i] -= 1
            else:
                del neighbor_color[e][i]

        cur_color[max_pos] = 0
    return False

def trick_force (edge, n, m):
    l, r = 1, n
    ans_color = []
    while l < r:
        mid = (l + r) // 2
        cur_color = [0 for i in range(n + 1)]
        neighbor_color = [dict() for i in range(n + 1)]
        if dfs(1, n, edge, cur_color, mid, neighbor_color):
            r = mid
            ans_color = cur_color[1:].copy()
            for i in range(n): ans_color[i] -= 1
        else:
            l = mid + 1
    return r, ans_color

def add_color (edge, cur_color, neighbor_color, color, node, color_cnt):
    color_cnt[color] += 1
    cur_color[node] = color
    for e in edge[node]:
        if color in neighbor_color[e]:
            neighbor_color[e][color] += 1
        else:
            neighbor_color[e][color] = 1

def del_color (edge, cur_color, neighbor_color, color, node, color_cnt):
    color_cnt[color] -= 1
    cur_color[node] = 0
    for e in edge[node]:
        if neighbor_color[e][color] > 1:
            neighbor_color[e][color] -= 1
        else:
            del neighbor_color[e][color]

count = 0
Vertex = namedtuple("Vertex", ['i', 'len'])
def magic_dfs (d, n, edge, cur_color, color_num, neighbor_color, color_cnt, last_pos):
    global count
    count += 1
    if count * n > 2000000000: return False
    if d == n + 1: return True
    #print(cur_color)
    for i in range(1, n + 1):
        if cur_color[i]: continue
        if len(neighbor_color[i]) == color_num: # No color to choose for this node
            return False
        if len(neighbor_color[i]) == color_num - 1: # One color to choose for this node
            for color in range(1, color_num + 1):
                if color not in neighbor_color[i]:
                    choose_color = color
                    break
            add_color(edge, cur_color, neighbor_color, choose_color, i, color_cnt, last_pos)
            if magic_dfs(d + 1, n, edge, cur_color, color_num, neighbor_color, color_cnt):
                return True
            del_color(edge, cur_color, neighbor_color, choose_color, i, color_cnt, last_pos)
            return False

    now = last_pos + 1
    while cur_color[now]: now += 1
    for i in range(1, color_num + 1):
        if i in neighbor_color[now]: continue
        add_color(edge, cur_color, neighbor_color, i, now, color_cnt)
        if magic_dfs(d + 1, n, edge, cur_color, color_num, neighbor_color, color_cnt, now):
            return True
        del_color(edge, cur_color, neighbor_color, i, now, color_cnt)
        if color_cnt[i] == 0: return False
    return False

def magic_force (edge, n, m):
    l, r = 1, n
    ans_color = []
    node = []
    for i in range(1, n + 1):
        node.append(Vertex(i, len(edge[i])))
    sorted(node, key = lambda x: -len[x])
    node = [0] + node
    while l < r:
        mid = (l + r) // 2
        global count
        count = 0
        cur_color = [0 for i in range(n + 1)]
        neighbor_color = [dict() for i in range(n + 1)]
        color_cnt = [0 for i in range(mid + 1)]
        #print(mid)
        if magic_dfs(1, n, edge, cur_color, mid, neighbor_color, color_cnt, 1):
            r = mid
            ans_color = cur_color[1:].copy()
            for i in range(n): ans_color[i] -= 1
        else:
            l = mid + 1
    return r, ans_color


from random import sample
from pysat.formula import CNF
from pysat.solvers import Solver
def sat_build (edge_set, n, k):
    sat = []
    var_num = 1  # t variables codes a vertex
    while (1 << var_num) < k: var_num += 1
    for i in range(1, n + 1):
        for state in range(k, 1 << var_num):
            clause = []
            first_varible = (i - 1) * var_num + 1  # the first varible index of i-th vertex
            for j in range(0, var_num):
                if (state >> j) & 1:
                    clause.append(-(first_varible + j))
                else:
                    clause.append(first_varible + j)
            sat.append(clause)
    for edge in edge_set:
        for state in range(0, k):
            clause = []
            for i in edge:
                first_varible = (i - 1) * var_num + 1
                for j in range(0, var_num):
                    if (state >> j) & 1:
                        clause.append(-(first_varible + j))
                    else:
                        clause.append(first_varible + j)
            sat.append(clause)
    return sat, var_num

def sat_check (n, k, edge_set):
    sat_instance, var_num = sat_build(edge_set, n, k);
    answer = []
    cnf = CNF(from_clauses=sat_instance)
    with Solver(bootstrap_with=cnf) as solver:
        return solver.solve()
    '''
    for i in range(1, n + 1):
        color = 0
        for j in range(0, var_num):
            result = answer[(i - 1) * var_num + j]
            if result > 0:
                color += 1 << j
        print("%d-th vertex is %d-th color" % (i, color))
    '''
def sat_print (n, k, edge_set):
    sat_instance, var_num = sat_build(edge_set, n, k);
    answer = []
    cnf = CNF(from_clauses=sat_instance)
    with Solver(bootstrap_with=cnf) as solver:
        solver.solve()
        answer = solver.get_model()
    ans = []
    for i in range(1, n + 1):
        color = 0
        for j in range(0, var_num):
            result = answer[(i - 1) * var_num + j]
            if result > 0:
                color += 1 << j
        ans.append(color)
    return ans


def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')
    sys.setrecursionlimit(int(1e9))
    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    edge = [[] for i in range(node_count + 1)]
    edge_set = []
    global count
    count = 0
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        u = int(parts[0]) + 1
        v = int(parts[1]) + 1
        edge[u].append(v)
        edge[v].append(u)
        edge_set.append((u, v))
    start_time = time.time()
    #color_count, solution = brute_force(edge, node_count, edge_count)
    #color_count, solution = trick_force(edge, node_count, edge_count)
    color_count, solution = magic_force(edge, node_count, edge_count)
    #color_count, solution = sat_force(node_count, edge_set)
    end_time = time.time()
    #print("time:", end_time - start_time)
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

