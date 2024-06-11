import numpy as np
import sympy as sp


def biseccion(f, a, b, tol):
    if (f(a) * f(b) > 0):
        print("pailas")
        return

    contador = 0
    while abs(a - b) > tol:
        c = (a + b) / 2

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        contador += 1

    print("Iteraciones bisección: ", contador)
    return c


def posicion_falsa(f, a, b, tol):
    if f(a) * f(b) > 0:
        print("pailas")
        return

    contador = 0
    while True:
        c = (a - f(a) * (a - b)) / (f(a) - f(b))

        if abs(f(c)) <= tol:
            break

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        contador += 1

    print("Iteraciones posición falsa: ", contador)
    return c



def secante(f, h0, h1, tol):
    h = [h0, h1]

    while abs(h[-1] - h[-2]) > tol:
        next_h = h[-1] - (f(h[-1]) * (h[-2] - h[-1])) / (f(h[-2]) - f(h[-1]))
        h.append(next_h)

        print(h[-1])

    return h[-1]




def newton(f, x0, tol, variable = None):
    if not variable:
      variable = sp.symbols('x')  # Define 'x' as a symbol

    df = sp.diff(f, variable)
    xv = [x0]

    next_x = sp.lambdify(variable, variable - f/df)

    while True:
        xv.append(next_x(xv[-1]))

        if abs(xv[-1] - xv[-2]) < tol:
            break

    return xv[-1]

