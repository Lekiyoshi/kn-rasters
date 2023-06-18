import tkinter as tk
from PIL import Image

from ui import MainUI
from rasters import Rasters


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Rasters")

        # self.image = Image.new("RGBA", (40, 40), "white")
        self.front = MainUI(self)
        self.back = Rasters(self.front)


if __name__ == '__main__':
    app = App()
    app.mainloop()
