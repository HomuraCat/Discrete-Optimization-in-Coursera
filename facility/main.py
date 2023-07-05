from z3 import *
import numpy as np
solver = Solver()

p = np.zeros((10, 10), dtype = object)
C = 10
F = 10
for i in range(C):
    for j in range(F):
        p[i][j] = Int(f"p{i,j}")
        solver.add(p[i][j] <= 1)
        solver.add(p[i][j] >= 0)

if solver.check() == sat:
    model = solver.model()
    print(type(model))
else:
    print("Constraints are unsatisfiable.")

