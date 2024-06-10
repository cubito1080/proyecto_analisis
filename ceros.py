from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label
from typing import Callable, Dict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import sympy as sp
from modulos.ceros_module import biseccion
from modulos.ceros_module import newton
import tkinter as tk

class Ceros:
    def __init__(self, root: Tk, assets_path: Path):
        self.root = root
        self.assets_path = assets_path
        self.root.geometry("1080x780")
        self.root.configure(bg="#FFC7C7")
        self.canvas = self.create_canvas()
        self.images = {}

        self.entries = self.create_entries()
        self.buttons = self.create_buttons()

        self.texts = self.create_texts()

        # new
        self.figure = Figure(figsize=(4, 3), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self.root)

        # place the canvas on the right side of the window
        self.figure_canvas.get_tk_widget().place(x=100, y=400)

        self.canvas_images = self.create_images()

        # text
        self.solution_label = tk.Label(self.root, text="", bg="#FFC7C7")
        self.solution_label.place(x=100, y=410)

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

    def create_buttons(self):
        buttons = {

            "biseccion": self.create_button("button_2.png", 590.0, 71.0, 319.0, 128.0, self.handleBiseccion),
            "newton": self.create_button("button_3.png", 590.0, 208.0, 319.0, 128.0, self.handleNewton),
            "falsa_posicion": self.create_button("button_4.png", 590.0, 345.0, 319.0, 128.0, lambda: print("falsa_posicion clicked")),
            "secante": self.create_button("button_5.png", 590.0, 482.0, 319.0, 128.0, lambda: print("secante clicked")),
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
            "entry_1": self.create_entry("entry_1.png", 369.0, 232.0, 174.0, 46.0),
            "entry_2": self.create_entry("entry_2.png", 369.0, 144.0, 174.0, 46.0),
            "entry_3": self.create_entry("entry_3.png", 369.0, 310.0, 174.0, 46.0),
        }
        return entries

    def create_text(self, x: float, y: float, text: str, font: str) -> None:
        self.canvas.create_text(x, y, anchor="nw", text=text, fill="#000000", font=(font, 40 * -1))

    def create_texts(self):
        self.create_text(320.0, 25.0, "Ceros de funciones", "InriaSans Regular")
        self.create_text(115.0, 200.0, "Punto a:", "InriaSans Regular")
        self.create_text(115.0, 114.0, "Funcion:", "InriaSans Regular")
        self.create_text(115.0, 286.0, "Punto b:", "InriaSans Regular")


    def create_image(self, image_file: str, x: float, y: float) -> int:
        image = self.get_image(image_file)
        return self.canvas.create_image(x, y, image=image)


    def create_images(self) -> Dict[str, int]:
        images = {
            "image_1": self.create_image("image_1.png", 1073.0, 725.0),
            "image_2": self.create_image("image_2.png", 225.74986267089844, 57.0),
            "image_3": self.create_image("image_3.png", 1047.0, 106.0),
            "image_4": self.create_image("image_4.png", 85.00000762939453, 33.99999713897705),
            "image_5": self.create_image("image_5.png", 114.00001525878906, 775.0),

        }
        return images

    def get_image(self, image_file: str) -> PhotoImage:
        if image_file not in self.images:
            self.images[image_file] = PhotoImage(file=self.relative_to_assets(image_file))
        return self.images[image_file]

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    # Manejo de botones
    def handleBiseccion(self):
        # get the values from the entries
        a_str = self.entries["entry_1"].get("1.0", "end-1c")
        f_str = self.entries["entry_2"].get("1.0", "end-1c")
        b_str = self.entries["entry_3"].get("1.0", "end-1c")

        # check if the entries are empty
        if not a_str or not f_str or not b_str:
            print("Error: One or more entries are empty")
            return

        # convert the entries to appropriate types
        a = float(a_str)
        b = float(b_str)

        # parse the function string to a sympy expression
        x = sp.symbols("x")
        f = sp.sympify(f_str)
        f_lambda = sp.lambdify(x, f)

        # apply the bisection method
        tol = 1e-6  # tolerance
        root_biseccion = biseccion(f_lambda, a, b, tol)

        # check if root_biseccion is None
        if root_biseccion is None:
            print("Error: Bisection method could not find a root")
            return

        # clear the current plot
        self.figure.clear()

        # prepare data
        w = np.linspace(a - 5, a + 5, 100)

        # create axes
        axes = self.figure.add_subplot()

        # create the plot

        axes.plot(w, f_lambda(w), label="Function")
        axes.scatter([root_biseccion], [f_lambda(root_biseccion)], color='red')
        axes.legend()

        axes.axhline(0, color='black', linewidth=0.5)
        axes.axvline(0, color='black', linewidth=0.5)

        # draw the graph
        self.figure_canvas.draw()

        # update the polynomial label
        self.solution_label.config(text=str(root_biseccion))

    def handleNewton(self):
        # get the values from the entries
        x0_str = self.entries["entry_1"].get("1.0", "end-1c")
        f_str = self.entries["entry_2"].get("1.0", "end-1c")

        # check if the entries are empty
        if not x0_str or not f_str:
            print("Error: One or more entries are empty")
            return

        # convert the entries to appropriate types
        x0 = float(x0_str)

        # parse the function string to a sympy expression
        x = sp.symbols("x")
        f = sp.sympify(f_str)

        # apply the Newton's method
        tol = 1e-6  # tolerance
        root_newton = newton(f, x0, tol)

        # clear the current plot
        self.figure.clear()

        # prepare data
        F = sp.lambdify(x, f)
        w = np.linspace(x0 - 5, x0 + 5, 100)

        # create axes
        axes = self.figure.add_subplot()

        # create the plot
        axes.plot(w, F(w), label="Function")
        axes.scatter([root_newton], [F(root_newton)], color='red')
        axes.legend()

        # draw the graph
        self.figure_canvas.draw()

    def handleFalsaPosicion(self):
        pass

    def handleSecante(self):
        pass

    def run(self):
        self.root.resizable(False, False)
        self.root.mainloop()


if __name__ == "__main__":
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Proyecto_final_analisis\build\assets\Ceros_assets")
    root = Tk()
    app = Ceros(root, ASSETS_PATH)
    app.run()
