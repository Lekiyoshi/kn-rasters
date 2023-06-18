from math import cos, sin, radians
from PIL import Image, ImageColor

from ui import MainUI


class Rasters:
    def __init__(
            self,
            front: MainUI = None,
            image: Image = Image.new("RGBA", (40, 40), "white")
    ):
        self.front = front
        self.image = image

        # Initial states for each canvas in UI
        self.draw_line()
        self.redraw_circle()

        # Bindings
        if front is not None:
            # Line tab
            self.front.fr_tab_line.p1x_var.trace("w", self.redraw_line)
            self.front.fr_tab_line.p1y_var.trace("w", self.redraw_line)
            self.front.fr_tab_line.p2x_var.trace("w", self.redraw_line)
            self.front.fr_tab_line.p2y_var.trace("w", self.redraw_line)
            self.front.fr_tab_line.line_options_var.trace("w", self.redraw_line)
            # Circle tab
            self.front.fr_tab_circle.xc_var.trace("w", self.redraw_circle)
            self.front.fr_tab_circle.yc_var.trace("w", self.redraw_circle)
            self.front.fr_tab_circle.radius_var.trace("w", self.redraw_circle)
            self.front.fr_tab_circle.circle_options_var.trace("w", self.redraw_circle)

    def clear_img(self):
        # 'Clears' the image, painting with white
        for x in range(0, self.image.width):
            for y in range(0, self.image.height):
                self.image.putpixel((x, y), ImageColor.getcolor("white", "RGBA"))

    def draw_line(self):
        if self.front is None:
            return

        x1 = self.front.fr_tab_line.p1x_var.get()
        y1 = self.front.fr_tab_line.p1y_var.get()
        x2 = self.front.fr_tab_line.p2x_var.get()
        y2 = self.front.fr_tab_line.p2y_var.get()
        method = self.front.fr_tab_line.line_options_var.get()

        if method == "Analítico":
            self.linha_analitico(x1, y1, x2, y2, ImageColor.getcolor("red", "RGBA"))
        elif method == "DDA":
            self.linha_dda(x1, y1, x2, y2, ImageColor.getcolor("blue", "RGBA"))
        elif method == "Bresenham":
            ...  # TODO: Implementar o algoritmo de Bresenham.
        else:
            self.linha_dda(x1, y1, x2, y2, ImageColor.getcolor("blue", "RGBA"))
            self.linha_analitico(x1, y1, x2, y2, ImageColor.getcolor("red", "RGBA"))

        self.front.fr_tab_line.update_canvas(
            self.image.resize((320, 320), Image.NEAREST).transpose(Image.FLIP_TOP_BOTTOM)
        )

    def redraw_line(self, a=None, b=None, c=None):
        # 'a', 'b', e 'c' are unused parameters received by the callbacks
        self.clear_img()
        self.draw_line()

    def draw_circle(self):
        if self.front is None:
            return

        xc = self.front.fr_tab_circle.xc_var.get()
        yc = self.front.fr_tab_circle.yc_var.get()
        radius = self.front.fr_tab_circle.radius_var.get()
        method = self.front.fr_tab_circle.circle_options_var.get()

        if method == "Paramétrico":
            self.circulo_parametrico(xc, yc, radius, 1, ImageColor.getcolor("red", "RGBA"))
        elif method == "Simétrico":
            self.circulo_simetrico(xc, yc, radius, ImageColor.getcolor("blue", "RGBA"))
        elif method == "Bresenham":
            ...  # TODO: Implementar o algoritmo de Bresenham.
        else:
            self.circulo_parametrico(xc, yc, radius, 1, ImageColor.getcolor("red", "RGBA"))
            self.circulo_simetrico(xc, yc, radius, ImageColor.getcolor("blue", "RGBA"))

        self.front.fr_tab_circle.update_canvas(
            self.image.resize((320, 320), Image.NEAREST).transpose(Image.FLIP_TOP_BOTTOM)
        )

    def redraw_circle(self, a=None, b=None, c=None):
        self.clear_img()
        self.draw_circle()

    def save_img(self, filename: str):
        self.image.transpose(Image.FLIP_TOP_BOTTOM).save("./output/" + filename, format="png")

    def paint_pixel(self, x, y, color):
        x = round(x)
        y = round(y)

        try:
            # Prevent Pillow from using negative indexes to paint pixels
            if x >= 0 and y >= 0:
                self.image.putpixel((x, y), color)
        except IndexError:
            pass  # Pixel would have been drawn out of bounds

    def linha_analitico(self, x1, y1, x2, y2, color):
        if x1 != x2:
            m = (y2 - y1) / (x2 - x1)
            b = y2 - m * x2

            for x in range(x1, x2 + 1):
                y = m * x + b
                self.paint_pixel(x, y, color)
        else:
            for y in range(y1, y2 + 1):
                self.paint_pixel(x1, y, color)

    def linha_dda(self, x1, y1, x2, y2, color):
        if abs(x2 - x1) > abs(y2 - y1):
            inc = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 0
            y = y1

            for x in range(x1, x2 + 1):
                self.paint_pixel(x, y, color)
                y += inc
        else:
            inc = (x2 - x1) / (y2 - y1) if (y2 - y1) != 0 else 0
            x = x1

            for y in range(y1, y2 + 1):
                self.paint_pixel(x, y, color)
                x += inc

    def circulo_parametrico(self, xc, yc, radius, step, color):
        x = xc + radius
        y = yc

        for theta in range(0, 360, step):
            # Theta increases by 1 each loop
            # A sufficiently large circumference will start showing gaps because of this
            self.paint_pixel(x, y, color)
            x = xc + radius * cos(radians(theta))
            y = yc + radius * sin(radians(theta))

    def circulo_simetrico(self, xc, yc, radius, color):
        x = radius
        y = 0

        try:
            theta = 1/radius  # Value in radians
        except ZeroDivisionError:
            # Paint only one pixel in case radius = 0
            self.paint_pixel(xc, yc, color)
            return

        while x > y:
            # Quadrant I
            self.paint_pixel(x + xc, y + yc, color)
            self.paint_pixel(y + xc, x + yc, color)
            # Quadrant II
            self.paint_pixel(-y + xc, x + yc, color)
            self.paint_pixel(-x + xc, y + yc, color)
            # Quadrant III
            self.paint_pixel(-x + xc, -y + yc, color)
            self.paint_pixel(-y + xc, -x + yc, color)
            # Quadrant IV
            self.paint_pixel(y + xc, -x + yc, color)
            self.paint_pixel(x + xc, -y + yc, color)

            xn = x
            yn = y
            x = xn * cos(theta) - yn * sin(theta)
            y = yn * cos(theta) + xn * sin(theta)
