#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
from collections import namedtuple
import random as rd

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

import matplotlib.pyplot as plt

def plot_path(points, ans):
    n = len(points)
    x_coords = [points[t].x for t in ans]
    y_coords = [points[t].y for t in ans]
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])
    plt.plot(x_coords, y_coords, 'o-')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Path Plot')
    plt.grid(True)
    plt.show()


def greedy(points, k_neighbor):
    n = len(points)
    vis = np.zeros(n)
    u = rd.randint(0, n - 1)
    ans = [u]
    vis[u] = 1
    for _ in range(n - 1):
        flag = 0
        for dist, v in k_neighbor[u]:
            if vis[v] == 1: continue
            ans.append(v)
            vis[v] = 1
            u = v
            flag = 1
            break
        if flag == 0:
            v = -1
            for i in range(n):
                if vis[i] == 1: continue
                if v == -1 or length(points[i], points[u]) < length(points[v], points[u]):
                    v = i
            ans.append(v)
            vis[v] = 1
            u = v
    return ans

def path_dist(points, solution):
    n = len(points)
    obj = length(points[solution[n - 1]], points[solution[0]])
    for index in range(0, n-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj

def inc(x, n):
    x += 1
    if x == n: return 0
    else: return x

def local_search(points, ans, temp, sol, sol_dist, K, k_neighbor, pos):
    n = len(points)
    ans_dist = path_dist(points, ans)
    for _ in range(n * 10):
        x = rd.randint(0, n - 1)
        y = pos[rd.choice(k_neighbor[x])[1]] - 1
        if y == -1: y = n - 1
        if x != y:
            if x > y: x, y = y, x
            length_now = length(points[ans[x]], points[ans[inc(x, n)]]) + length(points[ans[y]], points[ans[inc(y, n)]])
            length_nxt = length(points[ans[x]], points[ans[y]]) + length(points[ans[inc(x, n)]], points[ans[inc(y, n)]])
            delta = -length_now + length_nxt
            if delta < 0:
                ans[x + 1 : y + 1] = ans[x + 1 : y + 1][::-1]
                for i in range(x + 1, y + 1): pos[ans[i]] = i
                ans_dist += delta
                if ans_dist < sol_dist:
                    sol = ans.copy()
                    sol_dist = ans_dist
            else:
                if rd.random() < math.exp((sol_dist - ans_dist - delta) / temp): # -delta - 1e-5 ?
                    ans[x + 1 : y + 1] = ans[x + 1 : y + 1][::-1]
                    for i in range(x + 1, y + 1): pos[ans[i]] = i
                    ans_dist += delta
    return ans, ans_dist, sol, sol_dist

def complete_local_search(points, ans, sol, sol_dist, K, k_neighbor, pos):
    n = len(points)
    ans = sol.copy()
    ans_dist = sol_dist
    x_list = np.random.permutation(n)
    for x in x_list:  # the fixed order makes local convergence.
        for (dis, y) in k_neighbor[x]:
            y = pos[y] - 1
            if y == -1: y = n - 1
            if x != y:
                if x > y: x, y = y, x
                length_now = length(points[ans[x]], points[ans[inc(x, n)]]) + length(points[ans[y]], points[ans[inc(y, n)]])
                length_nxt = length(points[ans[x]], points[ans[y]]) + length(points[ans[inc(x, n)]], points[ans[inc(y, n)]])
                delta = -length_now + length_nxt
                if delta < 0:
                    ans[x + 1 : y + 1] = ans[x + 1 : y + 1][::-1]
                    for i in range(x + 1, y + 1): pos[ans[i]] = i
                    ans_dist += delta
                    if ans_dist < sol_dist:
                        sol = ans.copy()
                        sol_dist = ans_dist

    return ans, ans_dist, sol, sol_dist

def solve_tsp (points):
    n = len(points)
    K = 40
    k_neighbor = [[]] * n
    for i in range(n):
        for j in range(n):
            if i == j: continue
            k_neighbor[i].append((length(points[i], points[j]), j))
        k_neighbor[i] = sorted(k_neighbor[i], key = lambda x: x[0])[:K]
    #print(k_neighbor[1])
    count = 0
    temperature = 0
    for i in range(50000):
        x = rd.randint(0, n - 1)
        y = rd.randint(0, n - 1)
        if x != y:
            temperature += length(points[x], points[y])
            count += 1
    temperature /= count
    sol = greedy(points, k_neighbor)
    sol_dist = path_dist(points, sol)
    for i in range(100):
        ans = greedy(points, k_neighbor)
        ans_dist = path_dist(points, ans)
        pos = [0] * n
        for i in range(n): pos[ans[i]] = int(i)
        last_ans_dist = 0
        temp = temperature
        eps = 1e-9
        theta = 1
        last_reheat_ans_dist = 1e18
        #for T in range(100000):
            #ans, ans_dist, sol, sol_dist = local_search(points, ans, temp, sol, sol_dist, K, k_neighbor, pos)
            #print(ans_dist, sol_dist, T, temp)
            #temp *= 0.9

            #if (last_ans_dist - ans_dist < eps and ans_dist - last_ans_dist < eps):
                #      temp = temperature * theta
                #while 1:
                #    cur_ans = ans.copy()
                #    cur_ans, cur_ans_dist, sol, sol_dist = complete_local_search(points, cur_ans, 0, sol, sol_dist, K, k_neighbor, pos)
                #    if cur_ans == last_ans: break
                #    last_ans = cur_ans
            #    print("HERE")
         #       print(ans_dist, sol_dist, T, temp)
                #if last_reheat_ans_dist - ans_dist < eps and ans_dist - last_reheat_ans_dist < eps:
                #    theta = theta * 1.1
                #else:
                #    theta = 1
             #   last_reheat_ans_dist = ans_dist

        #    last_ans_dist = ans_dist
        ans, ans_dist, sol, sol_dist = complete_local_search(points, ans, sol, sol_dist, K, k_neighbor, pos)

        plot_path(points, sol)

    return sol


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))


    # build a trivial solution
    # visit the nodes in the order they appear in the file
    #solution = list(range(nodeCount))
    #solution = local_search_tsp(points)
    solution = solve_tsp(points)
    #for i in range(10):
    #    cur_solution = solve_tsp(points)
    #    if path_dist(points, cur_solution) < path_dist(points, solution):
    #        solution = cur_solution.copy()
    # calculate the length of the tour
    obj = length(points[solution[len(points) - 1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    print(obj)
    plot_path(points, solution)
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(points[0][0]) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

