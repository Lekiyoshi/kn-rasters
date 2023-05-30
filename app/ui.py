import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from ttkwidgets import TickScale


class UI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=8)
        self.pack(fill=tk.BOTH, expand=True)

        # Styles
        self.style = ttk.Style()
        self.style.theme_use("default")

        # Bar for all sliders
        self.toolbar = ttk.Frame(self)
        self.toolbar.grid(row=0, column=0, pady=(0, 8), sticky=tk.NSEW)

        # Sliders for P1 coordinates
        self.p1_sliders = ttk.LabelFrame(self.toolbar, padding=4, text="P1")
        self.p1_sliders.grid(row=0, column=0, padx=(0, 8), sticky=tk.W)

        # P1.x slider
        self.fr_p1_x = ttk.Frame(self.p1_sliders)
        self.fr_p1_x.grid(row=0, column=0, sticky=tk.NSEW)

        self.p1_x_label = ttk.Label(self.fr_p1_x, text="X:")
        self.p1_x_label.grid(row=0, column=0, padx=(0, 2))

        self.p1_x_var = tk.IntVar(self.fr_p1_x)
        self.p1_x_scale = TickScale(
            self.fr_p1_x,
            orient=tk.HORIZONTAL,
            length=80,
            from_=0,
            to=39,
            resolution=1,
            variable=self.p1_x_var,
            showvalue=True
        )
        self.p1_x_scale.set(0)
        self.p1_x_scale.grid(row=0, column=1)

        # Separator
        self.sep1 = ttk.Separator(self.p1_sliders, orient=tk.VERTICAL)
        self.sep1.grid(row=0, column=1, padx=4, sticky=tk.NS)

        # P1.y slider
        self.fr_p1_y = ttk.Frame(self.p1_sliders)
        self.fr_p1_y.grid(row=0, column=2, sticky=tk.NSEW)

        self.p1_y_label = ttk.Label(self.fr_p1_y, text="Y:")
        self.p1_y_label.grid(row=0, column=0, padx=(0, 2))

        self.p1_y_var = tk.IntVar(self.fr_p1_y)
        self.p1_y_scale = TickScale(
            self.fr_p1_y,
            orient=tk.HORIZONTAL,
            length=80,
            from_=0,
            to=39,
            resolution=1,
            variable=self.p1_y_var,
            showvalue=True
        )
        self.p1_y_scale.set(0)
        self.p1_y_scale.grid(row=0, column=1)

        # Sliders for P2 coordinates
        self.p2_sliders = ttk.LabelFrame(self.toolbar, padding=4, text="P2")
        self.p2_sliders.grid(row=0, column=1, padx=(0, 0), sticky=tk.W)

        # P2.x slider
        self.fr_p2_x = ttk.Frame(self.p2_sliders)
        self.fr_p2_x.grid(row=0, column=0, sticky=tk.NSEW)

        self.p2_x_label = ttk.Label(self.fr_p2_x, text="X:")
        self.p2_x_label.grid(row=0, column=0, padx=(0, 2))

        self.p2_x_var = tk.IntVar(self.fr_p2_x)
        self.p2_x_scale = TickScale(
            self.fr_p2_x,
            orient=tk.HORIZONTAL,
            length=80,
            from_=0,
            to=39,
            resolution=1,
            variable=self.p2_x_var,
            showvalue=True
        )
        self.p2_x_scale.set(39)
        self.p2_x_scale.grid(row=0, column=1)

        # Separator
        self.sep2 = ttk.Separator(self.p2_sliders, orient=tk.VERTICAL)
        self.sep2.grid(row=0, column=1, padx=4, sticky=tk.NS)

        # P2.y slider
        self.fr_p2_y = ttk.Frame(self.p2_sliders)
        self.fr_p2_y.grid(row=0, column=2, sticky=tk.NSEW)

        self.p2_y_label = ttk.Label(self.fr_p2_y, text="Y:")
        self.p2_y_label.grid(row=0, column=0, padx=(0, 2))

        self.p2_y_var = tk.IntVar(self.fr_p2_y)
        self.p2_y_scale = TickScale(
            self.fr_p2_y,
            orient=tk.HORIZONTAL,
            length=80,
            from_=0,
            to=39,
            resolution=1,
            variable=self.p2_y_var,
            showvalue=True
        )
        self.p2_y_scale.set(39)
        self.p2_y_scale.grid(row=0, column=1)

        # Raster options dropdown menu
        self.fr_raster_options = ttk.Frame(self)
        self.fr_raster_options.grid(row=1, column=0, pady=(0, 8), sticky=tk.NSEW)

        self.raster_options_label = ttk.Label(self.fr_raster_options, text="Opções de rasterização:")
        self.raster_options_label.grid(row=0, column=0, padx=(0, 4), sticky=tk.W)

        self.raster_options_var = tk.StringVar(self)
        self.raster_options_list = ["Método Analítico", "DDA", "Ambos"]
        self.raster_options_menu = ttk.OptionMenu(
            self.fr_raster_options,
            self.raster_options_var,
            self.raster_options_list[0],
            *self.raster_options_list
        )
        self.raster_options_menu.grid(row=0, column=1, sticky=tk.W)

        # Display canvas
        self.fr_img_view = ttk.Frame(self, borderwidth=1, relief=tk.SUNKEN)
        self.fr_img_view.grid(row=2, column=0, sticky=tk.NSEW)

        self.canvas = tk.Canvas(self.fr_img_view, borderwidth=-2)
        self.canvas.config(width=320, height=320)
        self.canvas.pack()

        self.photoimage = None

    def update_canvas(self, image: Image):
        self.canvas.delete("all")
        self.photoimage = ImageTk.PhotoImage(image)  # Reference needed to prevent gargabe collection
        self.canvas.create_image(0, 0, image=self.photoimage, anchor=tk.NW)
