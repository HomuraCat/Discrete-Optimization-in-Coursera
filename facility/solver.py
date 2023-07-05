#/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
from z3 import *
import numpy as np
Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_Z3 (customer, facility):
    solver = Optimize()
    solver.set(timeout=10000)
    C = len(customer)
    F = len(facility)
    p = np.zeros((C, F), dtype = object)
    a = np.zeros(F, dtype = object)
    print(C, F)
    for c in range(C):
        sum1 = 0
        for f in range(F):
            p[c][f] = Int(f"p{c,f}")
            solver.add(p[c][f] <= 1)
            solver.add(p[c][f] >= 0)
            sum1 += p[c][f]
        solver.add(sum1 == 1)
    for f in range(F):
        a[f] = Int(f"a{f}")
        solver.add(a[f] <= 1)
        solver.add(a[f] >= 0)
        for c in range(C):
            solver.add(p[c][f] <= a[f])
    for f in facility:
        sum1 = 0
        for c in customer:
            sum1 += c.demand * p[c.index][f.index]
        solver.add(sum1 <= f.capacity)

    obj = 0
    for f in facility:
        obj += f.setup_cost * a[f.index]
        for c in customer:
            obj += p[c.index][f.index] * length(f.location, c.location)
    solver.minimize(obj)
    solution = np.zeros(C, dtype = int)
    used = np.zeros(F, dtype = int)
    if solver.check() == sat:
        model = solver.model()
        print(model)
        for c in range(C):
            for f in range(F):
                if model[p[c][f]] == 1:
                    solution[c] = f
                    used[f] = 1
    else:
        print("no solution")
    print(solution)
    return solution, used

def calculate_by_fixed_facility (customer, facility, used):  #greedy
    used_facility = []
    F = len(facility)
    for i in range(F):
        if used[i]:
            used_facility.append(facility[i])
    UF = len(used_facility)
    C = len(customer)
    sum_distance = 0
    assignment = [0] * C
    used_capacity = [0] * UF
    for i in range(C):
        cur_length = 1e20
        facility_index = -1
        for j in range(UF):
            if used_facility[j].capacity - used_capacity[j] >= customer[i].demand:
                distance = length(used_facility[j].location, customer[i].location)
                if distance < cur_length:
                    cur_length = distance
                    facility_index = j
        if facility_index == -1:
            return -1, []
        sum_distance += cur_length
        used_capacity[facility_index] += customer[i].demand
        assignment[i] = used_facility[facility_index].index
    return sum_distance, assignment

def solve_ls (customer, facility):
    C = len(customer)
    F = len(facility)
    ITER_TIMES = 10000
    temperature = 100
    T = temperature
    used = [1] * F
    final_setup_ans = 0
    for i in range(F):
        final_setup_ans += facility[i].setup_cost
    final_ans = final_setup_ans + calculate_by_fixed_facility(customer, facility, used)[0]
    print(final_ans, final_setup_ans)
    for _ in range(ITER_TIMES):
        #index_change = -1
        #per_F = np.random.permutation(F)
        flag = 0
        for i in range(F):
            now_setup_ans = final_setup_ans
            used[i] ^= 1
            if used[i] == 1: now_setup_ans += facility[i].setup_cost
            else: now_setup_ans -= facility[i].setup_cost
            distance_sum = calculate_by_fixed_facility(customer, facility, used)[0]
            if distance_sum == -1:
                used[i] ^= 1
                continue
            now_ans = now_setup_ans + distance_sum
            if now_ans < final_ans:
                final_setup_ans = now_setup_ans
                final_ans = now_ans
                flag = 1
            else:
                if now_ans < final_ans:
                else:
                    used[i] ^= 1
        if flag == 0:
            break
    return calculate_by_fixed_facility(customer, facility, used)[1]

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])

    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))
    print(facility_count, customer_count, facilities[0])
    # solution, used = solve_Z3(customers, facilities)
        # build a trivial solution
        # pack the facilities one by one until all the customers are served
        #solution = [-1]*len(customers)
        #capacity_remaining = [f.capacity for f in facilities]

        #facility_index = 0
        #for customer in customers:
        #    if capacity_remaining[facility_index] >= customer.demand:
        #        solution[customer.index] = facility_index
        #        capacity_remaining[facility_index] -= customer.demand
        #    else:
        #        facility_index += 1
        #        assert capacity_remaining[facility_index] >= customer.demand
        #        solution[customer.index] = facility_index
        #        capacity_remaining[facility_index] -= customer.demand
        #used = [0]*len(facilities)
        #for facility_index in solution:
        #    used[facility_index] = 1
        ## end of trivla solution

    solution = solve_ls(customers, facilities)
    used = [0]*len(facilities)
    for facility_index in solution:
        used[facility_index] = 1
    print(solution, used)
    # calculate the cost of the solution
    obj = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

