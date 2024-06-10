import math
import pandas as pd
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from math import factorial


class TaylorSeries:
    def __init__(self, f, x0, n):
        self.f = f
        self.x0 = x0
        self.n = n
        self.x = sp.symbols("x")
        self.P = self.S_taylor()

    def S_taylor(self):
        P = 0
        for k in range(self.n + 1):
            df = sp.diff(self.f, self.x, k)
            dfx0 = df.subs(self.x, self.x0)
            P += dfx0 * (self.x - self.x0) ** k / factorial(k)
        return P

    def evaluate(self, X):
        P = sp.lambdify(self.x, self.P)
        F = sp.lambdify(self.x, self.f)
        D = []
        for i in X:
            D.append([i, F(i), P(i), np.abs(F(i) - P(i)) / np.abs(F(i)), np.abs(F(i) - P(i))])
        df = pd.DataFrame(data=D, columns=['X', 'F(x)', 'P(x)', '|F(x) - P(x)|/|F(x)|', "|F(x) - P(x)|"])
        return df

    def plot(self, X):
        P = sp.lambdify(self.x, self.P)
        F = sp.lambdify(self.x, self.f)
        w = np.linspace(min(X), max(X), 100)
        plt.plot(w, F(w), label="Function")
        plt.plot(w, P(w), label=f"Taylor Series (degree {self.n})")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    x = sp.symbols("x")
    f = (x - 1) * sp.log(x)
    x0 = 1
    n = 3
    X = [0.1, 1.5, 2.5]
    taylor = TaylorSeries(f, x0, n)
    print(f"Taylor Series: {taylor.P}")
    df = taylor.evaluate(X)
    print(df)
    taylor.plot(X)
