import tkinter as tk

from rasters import Rasters
from ui import MainUI


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Rasters")

        self.front = MainUI(self)
        self.back = Rasters(self.front)


if __name__ == '__main__':
    app = App()
    app.mainloop()
