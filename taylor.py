from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label

class Taylor:
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
        self.image_label = Label(self.root)  # Label to display the image
        self.polinomio_label = Label(self.root)  # Label to display the generated polynomial

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
            "button_1": self.create_button("button_1.png", 26.0, 472.0, 387.0, 146.0, self.on_button_click),
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

    def get_image(self, image_file: str) -> PhotoImage:
        if image_file not in self.images:
            self.images[image_file] = PhotoImage(file=self.relative_to_assets(image_file))
        return self.images[image_file]

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def on_button_click(self):
        # This function will be called when the button is clicked
        # You can add the code to generate the image and the polynomial here
        pass

    def run(self):
        self.root.resizable(False, False)
        self.root.mainloop()





if __name__ == "__main__":
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Proyecto_final_analisis\build\assets\taylor_assets")
    root = Tk()
    app = Taylor(root, ASSETS_PATH)
    app.run()
