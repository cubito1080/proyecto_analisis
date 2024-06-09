from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label

class Interpolacion:
    def __init__(self, root: Tk, assets_path: Path):
        self.root = root
        self.assets_path = assets_path
        self.root.geometry("1080x780")
        self.root.configure(bg="#FFC7C7")
        self.canvas = self.create_canvas()
        self.images = {}
        self.buttons = self.create_buttons()
        self.entries = self.create_entries()
        self.texts = self.create_texts()

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
            "button_1": self.create_button("button_1.png", 5.0, 397.0, 322.0, 107.0, lambda: print("button_1 clicked")),
            "button_2": self.create_button("button_2.png", 7.0, 271.0, 247.0, 121.078125, lambda: print("button_2 clicked")),
            "button_3": self.create_button("button_3.png", 260.0, 269.0, 247.0, 121.078125, lambda: print("button_3 clicked")),
            "button_4": self.create_button("button_4.png", 513.0, 266.0, 247.0, 121.078125, lambda: print("button_4 clicked")),
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
            "entry_1": self.create_entry("entry_1.png", 369.0, 157.5, 174.0, 31.0),
            "entry_2": self.create_entry("entry_2.png", 453.0, 233.5, 202.0, 31.0),
        }
        return entries

    def create_text(self, x: float, y: float, text: str, font: str) -> None:
        self.canvas.create_text(x, y, anchor="nw", text=text, fill="#000000", font=(font, 23))

    def create_texts(self):
        self.create_text(320.0, 25.0, "Interpolacion y ajuste", "InriaSans Regular")
        self.create_text(25.0, 136.0, "Datos dependientes:", "InriaSans Regular")
        self.create_text(25.0, 212.0, "Datos independientes:", "InriaSans Regular")

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
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Proyecto_final_analisis\build\assets\interpolacion_assets")
    root = Tk()
    app = Interpolacion(root, ASSETS_PATH)
    app.run()
