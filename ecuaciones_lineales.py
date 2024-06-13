import ast
import os
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label

import numpy as np
import sympy as sp
from modulos.sistema_ecuaciones_module import Gauss_s, pivot
from modulos.sistema_ecuaciones_module import Gauss_s_sumas
from modulos.sistema_ecuaciones_module import eliminacion_gaussiana
import tkinter as tk

class Ecuaciones_lineales:
    def __init__(self, root):
        self.root = root
        self.assets_path = Path(os.getcwd()) / "assets/ecuaciones_lineales_assets"



        self.root.geometry("1080x780")
        self.root.configure(bg="#FFC7C7")
        self.canvas = self.create_canvas()
        self.images = {}
        self.buttons = self.create_buttons()
        self.entries = self.create_entries()
        self.texts = self.create_texts()
        self.canvas_images = self.create_images()

        # text
        self.polinomio_label = tk.Label(self.root, text="", bg="#FFC7C7", font=("InriaSans Regular", 14))
        self.polinomio_label.place(x=250, y=645)

        # Excepciones
        self.error_label = tk.Label(self.root, text="", bg="#FFC7C7", font=("InriaSans Regular", 14))
        self.error_label.place(x=210, y=720)

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

    def parseData(self, A_str, b_str):
        # Remover espacios en blanco
        A_str = A_str.replace(" ", "")
        b_str = b_str.replace(" ", "")

        # Evaluar y convertir la matriz A
        if A_str[:2] != '[[':
            A_str = '[' + A_str + ']'

        # Evaluar las expresiones numéricas usando sympify
        A_eval = eval(A_str, {'__builtins__': None}, {'sympify': sp.sympify})
        A = np.array([[float(sp.sympify(val)) for val in row] for row in A_eval])

        # Convertir el vector b
        if b_str[0] != '[':
            b_str = '[' + b_str + ']'
        b_str = eval(b_str, {'__builtins__': None})
        b = np.array(b_str)

        return A, b

    def handleEliminacion(self):
        self.error_label.config(text="")
        A_str = self.entries["entry_1"].get("1.0", "end-1c")
        b_str = self.entries["entry_2"].get("1.0", "end-1c")

        # check if the entries are empty
        if not A_str or not b_str:
            print("Error: One or more entries are empty")
            return

        A, b = self.parseData(A_str, b_str)

        result = eliminacion_gaussiana(A, b)

        self.polinomio_label.config(text=str(result))

        print(result)

    def handlePivoteo(self):
        self.error_label.config(text="")
        A_str = self.entries["entry_1"].get("1.0", "end-1c")
        b_str = self.entries["entry_2"].get("1.0", "end-1c")

        # check if the entries are empty
        if not A_str or not b_str:
            print("Error: One or more entries are empty")
            return

        A, b = self.parseData(A_str, b_str)

        result = pivot(A, b)

        self.polinomio_label.config(text=str(result))

        print(result)

    def handleGsMatricial(self):
        self.error_label.config(text="")
        A_str = self.entries["entry_1"].get("1.0", "end-1c")
        b_str = self.entries["entry_2"].get("1.0", "end-1c")

        # check if the entries are empty
        if not A_str or not b_str:
            print("Error: One or more entries are empty")
            return

        A, b = self.parseData(A_str, b_str)

        tol = 1e-3
        try:
            result = Gauss_s(A, b, tol)

            self.polinomio_label.config(text=str(result))
        except:
            self.error_label.config(text="El método no converge a la solución del sistema")

    def handleGsSumas(self):
        self.error_label.config(text="")
        A_str = self.entries["entry_1"].get("1.0", "end-1c")
        b_str = self.entries["entry_2"].get("1.0", "end-1c")

        # check if the entries are empty
        if not A_str or not b_str:
            print("Error: One or more entries are empty")
            return

        A, b = self.parseData(A_str, b_str)

        try:
            result = Gauss_s_sumas(A, b)

            self.polinomio_label.config(text=str(result))
        except:
            self.error_label.config(text="El método no converge a la solución del sistema")


    def create_buttons(self):
        buttons = {
            "button_1": self.create_button("button_1.png", 724.0, 91.0, 247.0, 121.078125, self.handleEliminacion),
            "button_2": self.create_button("button_2.png", 730.0, 217.0, 247.0, 121.078125, self.handlePivoteo),
            "button_3": self.create_button("button_3.png", 730.0, 475.0, 247.0, 121.078125, self.handleGsMatricial),
            "button_4": self.create_button("button_4.png", 730.0, 613.0, 247.0, 121.078125, self.handleGsSumas),
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
        entry.place(x=x-width/2, y=y-height/2, width=width, height=height)
        return entry

    def create_entries(self):
        entries = {
            "entry_1": self.create_entry("entry_1.png", 281.0, 289.5, 384.0, 199.0),
            "entry_2": self.create_entry("entry_2.png", 293.5, 523.5, 409.0, 81.0),

        }
        return entries

    def create_text(self, x: float, y: float, text: str, font: str) -> None:
        self.canvas.create_text(x, y, anchor="nw", text=text, fill="#000000", font=(font, 40 * -1))

    def create_texts(self):
        self.create_text(81.0, 33.0, "Sistema de ecuaciones lineales", "InriaSans Regular")
        self.create_text(81.0, 132.0, "Ingresa la matriz A del sistema:", "InriaSans Regular")
        self.create_text(81.0, 416.0, "Ingresa la matriz B del sistema:", "InriaSans Regular")
        self.create_text(62.0, 627.0, "solucion:", "InriaSans Regular")
        self.create_text(727.0, 38.0, "-Metodos directos:", "InriaSans Regular")
        self.create_text(712.0, 416.0, "-Metodos iterativos:", "InriaSans Regular")

        self.create_text(712.0, 416.0, "", "InriaSans Regular")

    def create_image(self, image_file: str, x: float, y: float) -> int:
        image = self.get_image(image_file)
        return self.canvas.create_image(x, y, image=image)

    def create_images(self):
        images = {
            "image_1": self.create_image("image_1.png", 1073.0, 725.0),
            "image_2": self.create_image("image_2.png", 1096.0, 512.0),
            "image_3": self.create_image("image_3.png", 1100.0, 106.0),
            "image_4": self.create_image("image_4.png", 27.0, 30.0),
            "image_5": self.create_image("image_5.png", 77.0, 796.0),
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
    app = Ecuaciones_lineales()
    app.run()
