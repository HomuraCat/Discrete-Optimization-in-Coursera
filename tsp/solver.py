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


def greedy(points):
    n = len(points)
    vis = np.zeros(n)
    ans = []
    ans.append(0)
    u = 0
    vis[u] = 1
    for _ in range(n - 1):
        v = -1
        for i in range(n):
            if vis[i] == 1: continue
            if v == -1 or length(points[v], points[u]) > length(points[i], points[u]):
                v = i
        ans.append(v)
        vis[v] = 1
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

def local_search(points, ans, temp, sol, sol_dist):#, vis_time, T):
    n = len(points)
    ans = sol.copy()
    ans_dist = sol_dist
    for x in range(n - 1):
        for y in range(x + 1, n):
            #if temp > 0 and vis_time[(x, y)] + 100000 < T: continue
            length_now = length(points[ans[x]], points[ans[inc(x, n)]]) + length(points[ans[y]], points[ans[inc(y, n)]])
            length_nxt = length(points[ans[x]], points[ans[y]]) + length(points[ans[inc(x, n)]], points[ans[inc(y, n)]])
            delta = -length_now + length_nxt
            if delta < 0:
                ans[x + 1 : y + 1] = ans[x + 1 : y + 1][::-1]
                ans_dist += delta
                #vis_time[x + 1, y] = T
                if ans_dist < sol_dist:
                    sol = ans.copy()
                    sol_dist = ans_dist
            else:
                if temp > 0 and rd.random() < math.exp((sol_dist - ans_dist - delta) / temp): # -delta - 1e-5 ?
                    ans[x + 1 : y + 1] = ans[x + 1 : y + 1][::-1]
                    ans_dist += delta
                    #vis_time[x + 1, y] = T

    return ans, ans_dist, sol, sol_dist

def solve_tsp (points):
    n = len(points)
    if n > 30000:
        ans = list(range(0, n))
    else:
        ans = greedy(points)
    ans_dist = path_dist(points, ans)
    sol = ans.copy()
    sol_dist = ans_dist
    last_ans_dist = 0
    temp = 3000
    eps = 1e-5
    #vis_time = np.zeros((n, n))
    #for i in range(n):
    #    for j in range(n):
    #        vis_time[i][j] = -5e8
    for T in range(100000):
        ans, ans_dist, sol, sol_dist = local_search(points, ans, temp, sol, sol_dist)#, vis_time, T)
        temp *= 0.99
        if (last_ans_dist - ans_dist < eps and ans_dist - last_ans_dist < eps):
            temp = 7000
            last_ans = []
            while 1:
                ans, ans_dist, sol, sol_dist = local_search(points, ans, 0, sol, sol_dist)#, vis_time, T)
                if ans == last_ans: break
                last_ans = ans
            print("HERE")
            print(ans_dist, sol_dist, T)
        last_ans_dist = ans_dist

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
    #plot_path(points, solution)
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
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

