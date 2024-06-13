import numpy as np
from sympy import sympify

def parseData(A_str, b_str):
    # Remover espacios en blanco
    A_str = A_str.replace(" ", "")
    b_str = b_str.replace(" ", "")

    # Evaluar y convertir la matriz A
    if A_str[:2] != '[[':
        A_str = '[' + A_str + ']'

    # Evaluar las expresiones numéricas usando sympify
    A_eval = eval(A_str, {'__builtins__': None}, {'sympify': sympify})
    A = np.array([[float(sympify(val)) for val in row] for row in A_eval])

    # Convertir el vector b
    if b_str[0] != '[':
        b_str = '[' + b_str + ']'
    b_str = eval(b_str, {'__builtins__': None})
    b = np.array(b_str)

    return A, b


A_str = "[[1, 1, 1, 1, 1, 1, 1], [1, 2, 2**2, 2**3, 2**4, 2**5, 2**6], [1, 5, 5**2, 5**3, 5**4, 5**5, 5**6], [1, 10, 10**2, 10**3, 10**4, 10**5, 10**6], [1, 20, 20**2, 20**3, 20**4, 20**5, 20**6], [1, 30, 30**2, 30**3, 30**4, 30**5, 30**6], [1, 40, 40**2, 40**3, 40**4, 40**5, 40**6]]"
b_str = "[1, 2, 3, 4, 5, 6, 7]"

A, b = parseData(A_str, b_str)
print("Matriz A:")
print(A)
print("\nVector b:")
print(b)