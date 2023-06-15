import numpy as np
from scipy.optimize import linprog

def linear_programming_solver(c, A, b, x_bounds):
    """
    Solves a linear programming problem.

    Parameters
    ----------
    c : list or array-like
        Coefficients of the objective function to minimize.
        
    A : list or array-like
        Coefficients of the inequality constraints (Ax <= b)
        
    b : list or array-like
        Right-hand side values of the inequality constraints (Ax <= b)
        
    x_bounds : tuple or list of tuples
        Bounds for the variables in the form (min, max)

    Returns
    -------
    result: dict
        A dictionary containing the optimized result.

    Example
    -------
    >>> c = [-1, 4]
    >>> A = [[-3, 1], [1, 2]]
    >>> b = [6, 4]
    >>> x_bounds = [(0, None), (0, None)]
    >>> result = linear_programming_solver(c, A, b, x_bounds)
    >>> print(result)
    {'x': array([10.,  4.]), 'fun': -18.0, 'success': True}
    """
    c = np.array(c)
    A = np.array(A)
    b = np.array(b)

    result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')
    
    if result.success:
        optimized_result = {
            'x': result.x,
            'fun': result.fun,
            'success': result.success
        }
    else:
        optimized_result = {
            'x': None,
            'fun': None,
            'success': result.success,
            'message': result.message
        }
    
    return optimized_result