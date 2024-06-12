from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import sympy as sp
from modulos.interpolacion_module import  Poly, Pol_simple_2, minimos_cuadrados, langrange_polinomio


class Interpolacion:
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
        self.canvas_images = self.create_images()

        # new
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self.root)

        # place the canvas on the right side of the window
        self.figure_canvas.get_tk_widget().place(x=81, y=320)

        self.canvas_images = self.create_images()

        # text
        self.solution_label = tk.Label(self.root, text="", bg="#FFC7C7")
        self.solution_label.place(x=100, y=210)

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
            "polinomial": self.create_button("button_1.png", 724.0, 91.0, 247.0, 121.078125, self.handlePolinomial),
            "minimos": self.create_button("button_2.png", 727.0, 243.0, 247.0, 121.078125, self.handleMinimos),
            "lagrange": self.create_button("button_3.png", 727.0, 390.0, 247.0, 121.078125, self.handleLagrage),
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
            "entry_1": self.create_entry("entry_1.png", 453.0, 155.5, 202.0, 31.0),
            "entry_2": self.create_entry("entry_2.png", 190.0, 697.5, 202.0, 31.0),
            "entry_3": self.create_entry("entry_3.png", 453.0, 233.5, 202.0, 31.0),
        }
        return entries

    def create_text(self, x: float, y: float, text: str, font: str) -> None:
        self.canvas.create_text(x, y, anchor="nw", text=text, fill="#000000", font=(font, 32 * -1))

    def create_texts(self):
        self.create_text(320.0, 25.0, "Interpolacion y ajuste", "InriaSans Regular")
        self.create_text(81.0, 137.0, "dependientes:", "InriaSans Regular")
        self.create_text(81.0, 212.0, "independientes:", "InriaSans Regular")

    def create_image(self, image_file: str, x: float, y: float) -> int:
        image = self.get_image(image_file)
        return self.canvas.create_image(x, y, image=image)

    def create_images(self):
        images = {
            "image_1": self.create_image("image_1.png", 1073.0, 725.0),
            "image_2": self.create_image("image_2.png", 1096.0, 512.0),
            "image_3": self.create_image("image_3.png", 1047.0, 106.0),
            "image_4": self.create_image("image_4.png", 97.0, 30.0),
            "image_5": self.create_image("image_5.png", 77.0, 796.0),
        }
        return images

    def get_image(self, image_file: str) -> PhotoImage:
        if image_file not in self.images:
            self.images[image_file] = PhotoImage(file=self.relative_to_assets(image_file))
        return self.images[image_file]

    def handlePolinomial(self):
        # get the values from the entries
        x_data_str = self.entries["entry_1"].get("1.0", "end-1c")
        y_data_str = self.entries["entry_3"].get("1.0", "end-1c")


        # check if the entries are empty or end with a comma
        # check if the entries are empty or end with a comma
        if not x_data_str.strip() or not y_data_str.strip() or x_data_str.strip().endswith(
                ',') or y_data_str.strip().endswith(','):
            print("Error: Invalid entry")
            return

        # convert the entries to appropriate types
        x_data = list(map(float, x_data_str.split(',')))
        y_data = list(map(float, y_data_str.split(',')))

        x_data = np.array(x_data)
        y_data = np.array(y_data)

        # apply the polynomial interpolation method
        a_i = Pol_simple_2(x_data, y_data)

        # clear the current plot
        self.figure.clear()

        # prepare data
        ux = np.linspace(min(x_data), max(x_data), 100)
        poly_values = Poly(a_i, ux)

        # create axes
        axes = self.figure.add_subplot()

        # create the plot
        axes.plot(x_data, y_data, 'vr', label='Datos O')
        axes.plot(ux, poly_values, 'b', label='Polinomio')

        # draw the graph
        self.figure_canvas.draw()

    def handleMinimos(self):
        x_data_str = self.entries["entry_1"].get("1.0", "end-1c")
        y_data_str = self.entries["entry_3"].get("1.0", "end-1c")

        # check if the entries are empty or end with a comma
        # check if the entries are empty or end with a comma
        if not x_data_str.strip() or not y_data_str.strip() or x_data_str.strip().endswith(
                ',') or y_data_str.strip().endswith(','):
            print("Error: Invalid entry")
            return

        # convert the entries to appropriate types
        x_data = list(map(float, x_data_str.split(',')))
        y_data = list(map(float, y_data_str.split(',')))

        x_data = np.array(x_data)
        y_data = np.array(y_data)

        # apply the least squares method
        a0, a1 = minimos_cuadrados(np.array(x_data), np.array(y_data))

        # clear the current plot
        self.figure.clear()

        # prepare data
        ux = np.linspace(min(x_data), max(x_data), 100)
        poly_values = a0 + a1 * ux

        # create axes
        axes = self.figure.add_subplot()

        # create the plot
        axes.plot(x_data, y_data, 'vr', label='Datos O')
        axes.plot(ux, poly_values, 'b', label='Ajuste lineal')

        # draw the graph
        self.figure_canvas.draw()

    def handleLagrage(self):
        x_data_str = self.entries["entry_1"].get("1.0", "end-1c")
        y_data_str = self.entries["entry_3"].get("1.0", "end-1c")

        # check if the entries are empty or end with a comma
        # check if the entries are empty or end with a comma
        if not x_data_str.strip() or not y_data_str.strip() or x_data_str.strip().endswith(
                ',') or y_data_str.strip().endswith(','):
            print("Error: Invalid entry")
            return

        # convert the entries to appropriate types
        x_data = list(map(float, x_data_str.split(',')))
        y_data = list(map(float, y_data_str.split(',')))

        x_data = np.array(x_data)
        y_data = np.array(y_data)

        # construct the Lagrange interpolating polynomial
        P = langrange_polinomio(x_data, y_data)
        P_lambdified = sp.lambdify('x', P)

        # clear the current plot
        self.figure.clear()

        # prepare data
        ux = np.linspace(min(x_data), max(x_data), 100)
        poly_values = P_lambdified(ux)

        # create axes
        axes = self.figure.add_subplot()

        # create the plot
        axes.plot(x_data, y_data, 'vr', label='Datos O')
        axes.plot(ux, poly_values, 'b', label='Polinomio de Lagrange')

        # draw the graph
        self.figure_canvas.draw()



    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def run(self):
        self.root.resizable(False, False)
        self.root.mainloop()


if __name__ == "__main__":
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Users\Wilson\Proyectos\proyecto_analisis\assets\interpolacion_assets")
    root = Tk()
    app = Interpolacion(root, ASSETS_PATH)
    app.run()
