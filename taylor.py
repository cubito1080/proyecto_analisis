import os
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label

import numpy as np
import sympy as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import Callable, Dict
import tkinter as tk

from graph import show_graph
from modulos.taylor_module import TaylorSeries


class Taylor:
    def __init__(self, root):
        self.root = root
        self.assets_path = Path(os.getcwd()) / "assets/taylor_assets"

        self.root.geometry("1080x780")
        self.root.configure(bg="#FFC7C7")
        self.canvas = self.create_canvas()
        self.images = {}
        self.buttons = self.create_buttons()
        self.entries = self.create_entries()
        self.texts = self.create_texts()
        self.image_label = Label(self.root)  # Label to display the image
        self.polinomio_label = Label(self.root)  # Label to display the generated polynomial

        self.canvas_images = self.create_images()

        #new
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self.root)

        # place the canvas on the right side of the window
        self.figure_canvas.get_tk_widget().place(x=540, y=165)


        #text
        self.polinomio_label = tk.Label(self.root, text="", bg="#FFC7C7")
        self.polinomio_label.place(x=440, y=570)
        self.canvas.pack()

    def create_canvas(self) -> Canvas:
        canvas = Canvas(
            self.root,
            bg="#FFC7C7",
            height=780,
            width=1080,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        return canvas

    def create_button(self, image_file: str, x: float, y: float, width: float, height: float, command) -> Button:
        image = self.get_image(image_file)
        button = Button(
            self.root,
            image=image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        button.place(x=x, y=y, width=width, height=height)
        return button

    def create_buttons(self):
        buttons = {
            "button_1": self.create_button("button_1.png", 26.0, 472.0, 387.0, 146.0, self.on_button_click),
        }
        return buttons

    def create_entry(self, image_file: str, x: float, y: float, width: float, height: float) -> Text:
        image = self.get_image(image_file)
        entry_bg = self.canvas.create_image(x, y, image=image)
        entry = Text(
            self.root,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry.place(x=x - width / 2, y=y - height / 2, width=width, height=height)
        return entry

    def create_entries(self):
        entries = {
            "entry_1": self.create_entry("entry_1.png", 302.0, 318.0, 312.0, 46.0),
            "entry_2": self.create_entry("entry_2.png", 302.0, 201.99999999999997, 312.0, 46.0),
            "entry_3": self.create_entry("entry_3.png", 302.0, 438.0, 312.0, 46.0),
        }
        return entries

    def create_text(self, x: float, y: float, text: str, font: str) -> None:
        self.canvas.create_text(x, y, anchor="nw", text=text, fill="#000000", font=(font, 23 * -1))

    def create_texts(self):
        self.create_text(138.0, 255.99999999999997, "Ingresa un punto x_o:", "Inter")
        self.create_text(138.0, 139.99999999999997, "Ingresa la funcion", "Inter")
        self.create_text(138.0, 376.0, "Ingresa el grado del polinomio:", "Inter")

    def create_image(self, image_file: str, x: float, y: float) -> int:
        image = self.get_image(image_file)
        return self.canvas.create_image(x, y, image=image)


    def create_images(self) -> Dict[str, int]:
        images = {
            "image_1": self.create_image("image_1.png", 1073.0, 725.0),
            "image_2": self.create_image("image_2.png", 265.74986267089844, 57.0),
            "image_3": self.create_image("image_3.png", 1047.0, 106.0),
            "image_4": self.create_image("image_4.png", 107.00000762939453, 73.99999713897705),
            "image_5": self.create_image("image_5.png", 114.00001525878906, 775.0),

        }
        return images

    def get_image(self, image_file: str) -> PhotoImage:
        if image_file not in self.images:
            self.images[image_file] = PhotoImage(file=self.relative_to_assets(image_file))
        return self.images[image_file]

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def on_button_click(self):
        # get the values from the entries
        x0 = float(self.entries["entry_1"].get("1.0", "end-1c"))
        f = self.entries["entry_2"].get("1.0", "end-1c")
        n = int(self.entries["entry_3"].get("1.0", "end-1c"))

        # parse the function string to a sympy expression
        x = sp.symbols("x")
        f = sp.sympify(f)

        # create a TaylorSeries object
        taylor = TaylorSeries(f, x0, n)

        # clear the current plot
        self.figure.clear()

        # prepare data
        P = sp.lambdify(x, taylor.P)
        F = sp.lambdify(x, f)
        w = np.linspace(x0 - 5, x0 + 5, 100)

        # create axes
        axes = self.figure.add_subplot()

        # create the plot
        axes.plot(w, F(w), label="Function")
        axes.plot(w, P(w), label=f"Taylor Series (degree {n})")
        axes.legend()

        # draw the graph
        self.figure_canvas.draw()

        # update the polynomial label
        self.polinomio_label.config(text=str(taylor.P))

    def run(self):
        self.root.resizable(False, False)
        self.root.mainloop()


if __name__ == "__main__":

    app = Taylor()
    app.run()
