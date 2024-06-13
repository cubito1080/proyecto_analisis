import os
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from modulos.ecuaciones_diferenciales_module import Euler, runge_kutta_4
import sympy as sp

import inspect


class Ecuaciones_diferenciales:
    def __init__(self):
        self.root = Tk()
        self.assets_path = Path(os.getcwd()) / "assets/Ecuaciones_diferenciales_assets"


        self.root.geometry("1080x780")
        self.root.configure(bg="#FFC7C7")
        self.canvas = self.create_canvas()
        self.images = {}
        self.buttons = self.create_buttons()
        self.entries = self.create_entries()
        self.texts = self.create_texts()
        self.canvas_images = self.create_images()



        # new
        self.figure = Figure(figsize=(4, 3), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self.root)

        # place the canvas on the right side of the window
        self.figure_canvas.get_tk_widget().place(x=445.0, y=380.0)

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
            image=image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        button.place(x=x, y=y, width=width, height=height)
        return button

    def handleEuler(self):
        equation1 = self.entries["entry_1"].get("1.0", "end-1c")
        condition1 = self.entries["entry_2"].get("1.0", "end-1c")
        equation2 = self.entries["entry_4"].get("1.0", "end-1c")
        condition2 = self.entries["entry_3"].get("1.0", "end-1c")

        a = self.entries["entry_5"].get("1.0", "end-1c")
        b = self.entries["entry_6"].get("1.0", "end-1c")

        if not equation1 or not condition1 or not a or not b:
            print("Error: One or more entries are empty")
            return

        a = int(a)
        b = int(b)
        h = 0.001

        n = int((b - a) / h)

        x = sp.symbols("y")
        t = sp.symbols("t")
        f = sp.sympify(equation1)

        f_lambda1 = sp.lambdify([x, t], f)

        condition1 = float(condition1)

        if equation2 == "":
            self.oneEquation(Euler, f_lambda1, a, b, condition1)
        else:
            if not condition2:
                print("Error: One or more entries are empty")
                return

            x1 = sp.symbols("x1")
            x2 = sp.symbols("x2")
            t = sp.symbols("t")

            f = sp.sympify(equation1)
            f_lambda1 = sp.lambdify([t, x1, x2], f)

            f = sp.sympify(equation2)
            f_lambda2 = sp.lambdify([t, x1, x2], f)

            condition2 = float(condition2)

            self.twoEquations(Euler, f_lambda1, f_lambda2, a, b, condition1, condition2)

    def handleRunge(self):
        equation1 = self.entries["entry_1"].get("1.0", "end-1c")
        condition1 = self.entries["entry_2"].get("1.0", "end-1c")
        equation2 = self.entries["entry_4"].get("1.0", "end-1c")
        condition2 = self.entries["entry_3"].get("1.0", "end-1c")

        a = self.entries["entry_5"].get("1.0", "end-1c")
        b = self.entries["entry_6"].get("1.0", "end-1c")

        if not equation1 or not condition1 or not a or not b:
            print("Error: One or more entries are empty")
            return

        a = int(a)
        b = int(b)
        h = 0.01

        condition1 = float(condition1)

        if equation2 == "":
            x = sp.symbols("x")
            t = sp.symbols("t")
            f = sp.sympify(equation1)

            f_lambda1 = sp.lambdify([x, t], f)

            self.oneEquation(runge_kutta_4, f_lambda1, a, b, condition1)
        else:
            if not condition2:
                print("Error: One or more entries are empty")
                return

            x1 = sp.symbols("x1")
            x2 = sp.symbols("x2")
            t = sp.symbols("t")

            f = sp.sympify(equation1)
            f_lambda1 = sp.lambdify([t, x1, x2], f)

            f = sp.sympify(equation2)
            f_lambda2 = sp.lambdify([t, x1, x2], f)

            condition2 = float(condition2)

            self.twoEquations(runge_kutta_4, f_lambda1, f_lambda2, a, b, condition1, condition2)

    def oneEquation(self, method, f, a, b, yo):
        h = 0.001
        t1, y = method(f, a, b, yo, h)

        self.figure.clear()

        # create axes
        axes = self.figure.add_subplot()

        # create the plot
        axes.plot(t1, y, label="Función 1")
        axes.legend()
        axes.grid()

        # draw the graph
        self.figure_canvas.draw()

    def twoEquations(self, method, f1, f2, a, b, yo1, yo2):
        h = 0.01
        yo = np.array([yo1, yo2])

        def F(t, y):
            n = len(y)
            x1 = y[0]
            x2 = y[1]
            F = np.zeros(n)
            F[0] = f1(t, x1, x2)
            F[1] = f2(t, x1, x2)
            return F

        t1, y = method(F, a, b, yo, h)

        y1 = np.array([y[i][0] for i in range(len(y))])
        y2 = np.array([y[i][1] for i in range(len(y))])

        self.figure.clear()

        # create axes
        axes = self.figure.add_subplot()

        # create the plot
        axes.plot(t1, y1, label="Función 1")
        axes.plot(t1, y2, label=f"Función 2")
        axes.legend()
        axes.grid()

        axes.legend()

        # draw the graph
        self.figure_canvas.draw()

    def create_buttons(self):
        buttons = {
            "button_1": self.create_button("button_1.png", 52.00000000000003, 495.0, 255.0, 121.078125, self.handleEuler),
            "button_2": self.create_button("button_2.png", 52.00000000000003, 626.0, 247.0, 121.078125, self.handleRunge),
        }
        return buttons

    def create_entry(self, image_file: str, x: float, y: float, width: float, height: float) -> Text:
        image = self.get_image(image_file)
        entry_bg = self.canvas.create_image(x, y, image=image)
        entry = Text(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry.place(x=x-width/2, y=y-height/2, width=width, height=height)
        return entry

    def create_entries(self):
        entries = {
            "entry_1": self.create_entry("entry_1.png", 200.00000000000003, 205.5, 222.0, 21.0),
            "entry_2": self.create_entry("entry_2.png", 200.00000000000003, 316.5, 222.0, 21.0),
            "entry_3": self.create_entry("entry_3.png", 564.0, 316.5, 222.0, 21.0),
            "entry_4": self.create_entry("entry_4.png", 564.0, 204.5, 222.0, 21.0),

            "entry_5": self.create_entry("entry_1.png", 928, 205.5, 222.5, 21.0),   #a
            "entry_6": self.create_entry("entry_1.png", 928, 316.5, 222.5, 21.0)   #b
        }
        return entries

    def create_text(self, x: float, y: float, text: str, font: str) -> None:
        self.canvas.create_text(x, y, anchor="nw", text=text, fill="#000000", font=(font, 20 * -1))

    def create_texts(self):
        self.create_text(81.00000000000003, 33.0, "Ecuaciones diferenciales", "InriaSans Regular")
        self.create_text(81.00000000000003, 132.0, "Ecuacion diferencial 1:", "InriaSans Regular")
        self.create_text(81.00000000000003, 253.0, "condicion inicial y(0)", "InriaSans Regular")
        self.create_text(445.0, 257.0, "condicion inicial y(0)", "InriaSans Regular")
        self.create_text(445.0, 132.0, "Ecuacion diferencial 2 (opcional):", "InriaSans Regular")
        self.create_text(81.00000000000003, 421.0, "Selecciona el metodo:", "InriaSans Regular")

        self.create_text(820, 132, "a", "InriaSans Regular")
        self.create_text(820, 257, "b", "InriaSans Regular")


    def create_image(self, image_file: str, x: float, y: float) -> int:
        image = self.get_image(image_file)
        return self.canvas.create_image(x, y, image=image)

    def create_images(self):
        images = {
            "image_1": self.create_image("image_1.png", 1073.0, 725.0),
            "image_2": self.create_image("image_2.png", 1096.0, 512.0),
            "image_3": self.create_image("image_3.png", 1047.0, 106.0),
            "image_4": self.create_image("image_4.png", 27, 30.0),
            "image_5": self.create_image("image_5.png", 76.99999999999997, 796.0),

        }
        return images

    def get_image(self, image_file: str) -> PhotoImage:
        if image_file not in self.images:
            self.images[image_file] = PhotoImage(file=self.relative_to_assets(image_file))
        return self.images[image_file]

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def run(self):
        self.root.resizable(False, False)
        self.root.mainloop()


if __name__ == "__main__":

    app = Ecuaciones_diferenciales()
    app.run()
