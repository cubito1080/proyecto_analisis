import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import sympy as sp


def show_graph(window, X, x, P, f, n):

    # prepare data
    P = sp.lambdify(x, P)
    F = sp.lambdify(x, f)
    w = np.linspace(min(X), max(X), 100)

    # create a figure
    figure = Figure(figsize=(6, 4), dpi=100)

    # create FigureCanvasTkAgg object
    figure_canvas = FigureCanvasTkAgg(figure, window)

    # create the toolbar
    NavigationToolbar2Tk(figure_canvas, window)

    # create axes
    axes = figure.add_subplot()

    # create the plot
    axes.plot(w, F(w), label="Function")
    axes.plot(w, P(w), label=f"Taylor Series (degree {n})")
    axes.legend()

    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1).place(x=50, y=50)