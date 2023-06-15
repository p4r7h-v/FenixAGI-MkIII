import sympy as sp

def solve_complex_equation(equation, variable):
    """Solves a complex mathematical equation.

    Parameters:
    equation (str): The equation to be solved.
    variable (str): The variable to be solved for.

    Returns:
    sympy.Solveset: The set of solutions.
    """
    x = sp.Symbol(variable)
    eq = sp.sympify(equation)
    solutions = sp.solveset(eq, x)
    
    return solutions

# Example usage
equation = "x**2 - 4"
variable = "x"
solutions = solve_complex_equation(equation, variable)
print(solutions)