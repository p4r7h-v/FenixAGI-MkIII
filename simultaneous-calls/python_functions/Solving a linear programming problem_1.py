import numpy as np
from scipy.optimize import linprog

def solve_linear_programming(c, A_ub, b_ub, A_eq=None, b_eq=None, bounds=None):
    """
    Solves a linear programming problem defined by objective function vector c, inequality constraint
    matrix A_ub, inequality constraint vector b_ub, equality constraint matrix A_eq, equality constraint
    vector b_eq, and variable bounds.

    Parameters:
    c (array_like): 1-D array specifying the coefficients of the linear objective function to be minimized.
    A_ub (array_like): 2-D array specifying the coefficients of the linear inequality constraints (optional).
    b_ub (array_like): 1-D array specifying the upper bounds of the linear inequality constraints (optional).
    A_eq (array_like): 2-D array specifying the coefficients of the linear equality constraints (optional).
    b_eq (array_like): 1-D array specifying the right-hand side of the linear equality constraints (optional).
    bounds (sequence): A sequence of (min, max) bounds for each element in the solution vector (optional).

    Returns:
    res (OptimizeResult): The result of the optimization, including status and solution vector.
    """
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    return res

# Example usage:

c = [-1, 4]
A_ub = [[-3, 1], [1, 2]]
b_ub = [6, 4]
bounds = [(None, None), (-3, None)]

res = solve_linear_programming(c, A_ub, b_ub, bounds=bounds)
print(res)