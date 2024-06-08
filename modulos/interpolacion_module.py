import numpy as np
from typing import List, Union, Tuple
import sympy as sp
import matplotlib.pyplot as plt


# Polinomial simple (interpolación) (usamos Gauss-Seidel)
def Pol_simple_2(x_data: Union[np.ndarray, List[float]], y_data: Union[np.ndarray, List[float]]) -> np.ndarray:
    n: int = len(x_data)
    M_p: np.ndarray = np.zeros([n, n])

    for i in range(n):
        M_p[i, 0] = 1
        for j in range(1, n):
            M_p[i, j] = M_p[i, j - 1] * x_data[i]

    resultado: np.ndarray = np.linalg.solve(M_p, y_data)

    return resultado


# Convertir a polinomio (polinomial simple)
def Poly(a_i: List[float], ux: Union[int, float, np.ndarray]) -> Union[int, float, np.ndarray]:
    P: Union[int, float, np.ndarray] = 0
    for i in range(len(a_i)):
        P = P + a_i[i] * ux ** i
    return P


# --------

# Lagrange
def langrange_polinomio(x_d: List[float], y_d: List[float]) -> sp.Expr:
    x = sp.symbols('x')
    n = len(x_d)
    S = 0

    for i in range(n):
        L = 1
        for j in range(n):
            if j != i:
                L = L * ((x - x_d[j]) / (x_d[i] - x_d[j]))

        S += L * y_d[i]

    return sp.expand(S)


# Mínimos cuadrados
def minimos_cuadrados(Dx: np.ndarray, Dy: np.ndarray) -> Tuple[float, float]:
    n = len(Dx)
    Sx = sum(Dx)
    Sf = sum(Dy)
    Sfx = sum(Dx * Dy)
    Sx2 = sum(Dx ** 2)

    a0 = (Sf * Sx2 - Sx * Sfx) / (n * Sx2 - Sx ** 2)
    a1 = (n * Sfx - Sf * Sx) / (n * Sx2 - Sx ** 2)

    return a0, a1


#graficar polinomios
def plot_graph(Px: np.ndarray, Ty: np.ndarray, ux: np.ndarray, poly_values: Union[int, float, np.ndarray],
               xlabel: str, ylabel: str, title: str, label_data: str = 'Datos O', label_poly: str = 'Polinomio'):
    plt.plot(Px, Ty, 'vr', label=label_data)
    plt.plot(ux, poly_values, 'b', label=label_poly)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()


# transformar polinomios
def plot_transformed_data(x_a, y_p):
    plt.figure(figsize=(9, 9))

    # Plot original data
    plt.subplot(331)
    plt.plot(x_a, y_p, 'pb', label='Observados')
    plt.xlabel('Años')
    plt.ylabel('Poblacion')
    plt.legend()

    # Plot x squared
    plt.subplot(332)
    plt.plot(x_a * 2, y_p, 'dr', label='$x^2$')
    plt.legend()

    # Plot x cubed
    plt.subplot(333)
    plt.plot(x_a * 3, y_p, 'dr', label='$x^3$')
    plt.legend()

    # Plot square root of y
    plt.subplot(334)
    plt.plot(x_a, np.sqrt(y_p), 'dr', label='$\sqrt{y}$')
    plt.legend()

    # Plot 1 divided by the square root of y
    plt.subplot(335)
    plt.plot(x_a, 1. / np.sqrt(y_p), 'dg', label='$1/\sqrt{y}$')
    plt.legend()

    # Plot natural log of x
    plt.subplot(336)
    plt.plot(np.log(x_a), y_p, 'dc', label='$\log(x)$')
    plt.legend()

    # Plot natural log of x and y
    plt.subplot(337)
    plt.plot(np.log(x_a), np.log(y_p), 'dg', label='$\log(x) \log(y)$')
    plt.legend()

    # Plot natural log of y
    plt.subplot(338)
    plt.plot(x_a, np.log(y_p), 'db', label='$\log(y)$')
    plt.legend()

    # Plot y squared
    plt.subplot(339)
    plt.plot(x_a, y_p ** 2, 'dm', label='$y^2$')
    plt.legend()

    # Show plot
    plt.show()
