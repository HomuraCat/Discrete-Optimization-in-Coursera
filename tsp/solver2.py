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

def local_search (points, ans, temp, final_swap, final_delta):
    n = len(points)
    x, y = 0, 0
    final_delta = 0
    while x == y or x == 0 and y == n - 1:
        x = rd.randint(0, n - 1)
        y = rd.randint(0, n - 1)
    if x > y: x, y = y, x
    x_left = x - 1 if x > 0 else n - 1
    y_right = y + 1 if y < n - 1 else 0
    length_now = length(points[ans[x_left]], points[ans[x]]) + length(points[ans[y]], points[ans[y_right]])
    length_nxt = length(points[ans[x_left]], points[ans[y]]) + length(points[ans[x]], points[ans[y_right]])
    delta = -length_now + length_nxt
    if delta < final_delta:
        final_delta = delta
        final_swap = (x, y)

    return final_swap, final_delta


def solve_tsp (points):
    n = len(points)
    if n > 30000:
        ans = list(range(0, n))
    else:
        ans = greedy(points)
    dist = path_dist(points, ans)
    temp = 300
    for T in range(500):
        final_swap, final_delta = (-1, -1), 0
        for _ in range(100):
            final_swap, final_delta = local_search(points, ans, temp, final_swap, final_delta)
        if final_swap[0] > -1:
            ans[final_swap[0] : final_swap[1] + 1] = ans[final_swap[0] : final_swap[1] + 1][::-1]
        #print(final_swap, ans, temp)
    return ans


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
    for i in range(10):
        cur_solution = solve_tsp(points)
        if path_dist(points, cur_solution) < path_dist(points, solution):
            solution = cur_solution.copy()
    plot_path(points, solution)
    # calculate the length of the tour
    obj = length(points[solution[len(points) - 1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(nodeCount) + '\n'
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

