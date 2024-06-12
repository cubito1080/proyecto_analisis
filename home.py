import ast
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label

import numpy as np

from ceros import Ceros
from ecuaciones_diferenciales import Ecuaciones_diferenciales
from ecuaciones_lineales import Ecuaciones_lineales
from interpolacion import Interpolacion
from modulos.sistema_ecuaciones_module import Gauss_s, pivot
from modulos.sistema_ecuaciones_module import Gauss_s_sumas
from modulos.sistema_ecuaciones_module import eliminacion_gaussiana
import tkinter as tk
from typing import Callable, Dict

from taylor import Taylor


class Home:
    def __init__(self, root: tk.Tk, assets_path: Path):
        self.root = root
        self.assets_path = assets_path
        self.root.geometry("1080x780")
        self.root.configure(bg="#FFC7C7")
        self.canvas = self.create_canvas()
        self.images = {}
        self.buttons = self.create_buttons()
        self.canvas_images = self.create_images()
        self.interpolacion_object = Interpolacion(root)
        self.ceros_object = Ceros(root)
        self.taylor_object = Taylor(root)
        self.ec_lineales_object = Ecuaciones_lineales(root)
        self.ec_diferenciales_object = Ecuaciones_diferenciales(root)




    def create_canvas(self) -> tk.Canvas:
        canvas = tk.Canvas(
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

    def create_button(self, image_file: str, x: float, y: float, width: float, height: float, command: Callable[[], None]) -> tk.Button:
        image = self.get_image(image_file)
        button = tk.Button(
            image=image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        button.place(x=x, y=y, width=width, height=height)
        return button

    def create_buttons(self) -> Dict[str, tk.Button]:
        buttons = {
            "button_1": self.create_button("button_1.png", 540.0, 473.0, 387.0, 146.0, lambda: print("button_1 clicked")),
            "button_2": self.create_button("button_2.png", 540.0, 630.0, 387.0, 146.0, seri),
            "button_3": self.create_button("button_3.png", 540.0, 7.0, 387.0, 146.0, lambda: print("button_3 clicked")),
            "button_4": self.create_button("button_4.png", 540.0, 161.0, 387.0, 146.0, lambda: print("button_4 clicked")),
            "button_5": self.create_button("button_5.png", 543.0, 317.0, 395.0, 146.0, lambda: print("button_5 clicked")),
        }
        return buttons

    def create_image(self, image_file: str, x: float, y: float) -> int:
        image = self.get_image(image_file)
        return self.canvas.create_image(x, y, image=image)

    def create_images(self) -> Dict[str, int]:
        images = {
            "image_1": self.create_image("image_1.png", 1073.0, 725.0),
            "image_2": self.create_image("image_2.png", 235.74986267089844, 57.0),
            "image_3": self.create_image("image_3.png", 1047.0, 106.0),
            "image_4": self.create_image("image_4.png", 107.00000762939453, 73.99999713897705),
            "image_5": self.create_image("image_5.png", 114.00001525878906, 775.0),
            "image_6": self.create_image("image_6.png", 285.0, 375.0),
        }
        return images

    def get_image(self, image_file: str) -> tk.PhotoImage:
        if image_file not in self.images:
            self.images[image_file] = tk.PhotoImage(file=self.relative_to_assets(image_file))
        return self.images[image_file]

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def run(self):
        self.root.resizable(False, False)
        self.root.mainloop()


if __name__ == "__main__":
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Users\Wilson\Proyectos\proyecto_analisis\assets\home_assets")
    root = tk.Tk()
    app = Home(root, ASSETS_PATH)
    app.run()
