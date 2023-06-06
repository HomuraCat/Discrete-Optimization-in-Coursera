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

    # Add the starting point to complete the loop
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])


    plt.plot(x_coords, y_coords, 'o-')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Path Plot')
    plt.grid(True)
    #for i, point in enumerate(points):
    #    plt.text(point.x, point.y, i, ha='center', va='bottom')
    plt.show()


def greedy (points):
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

def path_dist (points, solution):
    n = len(points)
    obj = length(points[solution[n - 1]], points[solution[0]])
    for index in range(0, n-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj

def inc (x, n):
    x += 1
    if x == n: return 0
    else: return x

def local_search (points, ans, temp):
    n = len(points)
    K = 2
    len_x = 5e8
    x = 0
    x_next = 1
    for _ in range(1):
        now_x = rd.randint(0, n - 1)
        now_x_next = inc(now_x, n)
        if length(points[now_x], points[now_x_next]) > length(points[x], points[x_next]):
            x = now_x
            x_next = now_x_next

    swap_list = []
    for _ in range(K):
        y = x
        while y == x or y == inc(x, n) or y in swap_list: y = rd.randint(0, n - 1)
        swap_list.append(y)
    swap_list = sorted(swap_list, key = lambda f: f if f > x else f + 5e8)
    delta = 0
    cur_delta = 0
    cur_swap = (-1, [])
    final_delta = 0
    final_swap = (-1, [])
    #print("!!!", ans)
    for i, y in enumerate(swap_list):
        length_now = length(points[ans[x]], points[ans[x_next]]) + length(points[ans[y]], points[ans[inc(y, n)]])
        length_nxt = length(points[ans[x]], points[ans[y]]) + length(points[ans[x_next]], points[ans[inc(y, n)]])
        delta += -length_now + length_nxt
        if delta < final_delta:
            final_delta = delta
            final_swap = (x, swap_list[:i + 1])
            cur_delta = delta
            cur_swap = (x, swap_list[:i + 1])

        else:
            #   print(final_delta - delta)
            if rd.random() < math.exp((final_delta - delta) / temp):
                cur_delta = delta
                cur_swap = (x, swap_list[:i + 1])
        x_next = y
    return final_swap, final_delta, cur_swap, cur_delta


def solve_tsp (points):
    n = len(points)
    if n > 30000:
        ans = list(range(0, n))
    else:
        ans = greedy(points)
    dist = path_dist(points, ans)
    solution = ans.copy()
    temp = 30
    for T in range(10000000):
        #if T % 100000 == 0: temp = 30
        final_swap, final_delta, cur_swap, cur_delta = local_search(points, ans, temp)
        if final_swap[0] > -1:  # update answer
            solution = ans.copy()
            x = final_swap[0]
            for y in final_swap[1]:
                if y > x:
                    solution[x + 1 : y + 1] = solution[x + 1 : y + 1][::-1]
                else:
                    merge = solution[x + 1 : n + 1] + solution[0 : y + 1]
                    merge = merge[::-1]
                    solution[x + 1 : n + 1] = merge[0 : n - x]
                    solution[0 : y + 1] = merge[n - x : ]
        if cur_swap[0] > -1:  # has a solution
            x = cur_swap[0]
            for y in cur_swap[1]:
                if y > x:
                    ans[x + 1 : y + 1] = ans[x + 1 : y + 1][::-1]
                else:
                    merge = ans[x + 1 : n + 1] + ans[0 : y + 1]
                    merge = merge[::-1]
                    ans[x + 1 : n + 1] = merge[0 : n - x]
                    ans[0 : y + 1] = merge[n - x : ]
        #print(final_swap, ans, temp)
        temp *= 0.99
    return solution

def local_search_tsp(points): # 2 opt
    tour = list(range(len(points)))
    last_tour_len = path_dist(points, tour)
    while 1:
        cur_tour = tour
        cur_tour_len = path_dist(points, cur_tour)
        for i in range(len(tour)):
            for j in range(i + 2, len(tour)):
                    new_tour = tour[:]
                    new_tour[i:j] = new_tour[i:j][::-1]
                    new_tour_len = path_dist(points, new_tour)
                    if new_tour_len < cur_tour_len:
                        cur_tour_len = new_tour_len
                        cur_tour = new_tour
        tour = cur_tour
        if last_tour_len - cur_tour_len < 0.00001:
            break
        last_tour_len = cur_tour_len
    return tour

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
    solution = list(range(nodeCount))
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

