import tkinter as tk
from PIL import Image

from ui import UI
from rasters import Rasters


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Line Rasters")
        # self.geometry("960x540")

        self.image = Image.new("RGBA", (40, 40), "white")

        self.front = UI(self)
        self.back = Rasters(self.front, self.image)


if __name__ == '__main__':
    app = App()
    app.mainloop()
