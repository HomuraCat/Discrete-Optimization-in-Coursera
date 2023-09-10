#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import numpy as np
import sys
Item = namedtuple("Item", ['index', 'value', 'weight'])
sum_weight = []
sum_value = []
optimal_value = 0
cur_taken = []

def calc_lp (i, items, capacity):
    global sum_weight, sum_value
    l, r = i + 1, len(items)

#    for now in range(l, r + 1):
#        if sum_weight[now] - sum_weight[i] > capacity:
#            r = now - 1
#            break

    while l < r:
        mid = (l + r + 1) // 2
        #print(l, r, mid)
        if sum_weight[mid] - sum_weight[i] > capacity:
            r = mid - 1
        else:
            l = mid
    value = sum_value[r] - sum_value[i]
    remain_capacity = capacity - (sum_weight[r] - sum_weight[i])
    if r < len(items):
        value += remain_capacity * items[r].value / items[r].weight
    return value

def dfs (i, items, taken, capacity, value):
    global optimal_value
    if capacity < 0:
        return
    if optimal_value < value:
        optimal_value = value
        global cur_taken
        cur_taken = taken.copy()
    #print(i, capacity, value, taken)
    if value + calc_lp(i, items, capacity) <= optimal_value:
        return
    #print("lp: ", calc_lp(i, items, capacity), i, capacity)
    taken[items[i].index - 1] = 1
    dfs(i + 1, items, taken, capacity - items[i].weight, value + items[i].value)
    taken[items[i].index - 1] = 0
    dfs(i + 1, items, taken, capacity, value)
    return


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    global sum_weight, sum_value, optimal_value, cur_taken
    optimal_value = 0
    sum_weight, sum_value, cur_taken = [], [], []
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i, int(parts[0]), int(parts[1])))

    value = 0
    weight = 0
    taken = [0]*len(items)
    valid = 0
    if item_count * capacity <= 0:#1e8 + 7:
        dp = np.zeros((item_count + 1, capacity + 1))
        for item in items:
            i = item.index
            v = int(item.value)
            w = int(item.weight)
            for j in range(capacity + 1):
                dp[i][j] = dp[i - 1][j]
            for j in range(w, capacity + 1):
                dp[i][j] = max(dp[i][j], dp[i - 1][j - w] + v)

        value = int(dp[item_count][capacity])
        now = capacity
        for i in range(item_count, 0, -1):
            if dp[i][now] == dp[i - 1][now]:
                taken[i - 1] = 0
            else:
                taken[i - 1] = 1
                now -= items[i - 1].weight
        valid = 1
    else:
        sys.setrecursionlimit(100000)
        items = sorted(items, key = lambda x: -x.value / x.weight)
        sum_weight.append(0)
        sum_value.append(0)
        for i in range(0, item_count):
            sum_weight.append(sum_weight[-1] + items[i].weight)
            sum_value.append(sum_value[-1] + items[i].value)
        dfs(0, items, taken, capacity, 0)
        value = optimal_value
        taken = cur_taken
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

