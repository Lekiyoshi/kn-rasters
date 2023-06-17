from math import cos, sin, radians
from PIL import Image, ImageColor


class Rasters:
    def __init__(self, front, image):
        self.front = front
        self.image = image

        self.draw_line()
        self.redraw_circle()

        # Bindings
        self.front.fr_tab_line.p1x_var.trace("w", self.redraw_line)
        self.front.fr_tab_line.p1y_var.trace("w", self.redraw_line)
        self.front.fr_tab_line.p2x_var.trace("w", self.redraw_line)
        self.front.fr_tab_line.p2y_var.trace("w", self.redraw_line)
        self.front.fr_tab_line.line_options_var.trace("w", self.redraw_line)

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
        x1 = self.front.fr_tab_line.p1x_var.get()
        y1 = self.front.fr_tab_line.p1y_var.get()
        x2 = self.front.fr_tab_line.p2x_var.get()
        y2 = self.front.fr_tab_line.p2y_var.get()
        metodo = self.front.fr_tab_line.line_options_var.get()

        if metodo == "Analítico":
            self.linha_analitico(x1, y1, x2, y2, ImageColor.getcolor("red", "RGBA"))
        elif metodo == "DDA":
            self.linha_dda(x1, y1, x2, y2, ImageColor.getcolor("blue", "RGBA"))
        elif metodo == "Bresenham":
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
        xc = self.front.fr_tab_circle.xc_var.get()
        yc = self.front.fr_tab_circle.yc_var.get()
        radius = self.front.fr_tab_circle.radius_var.get()
        metodo = self.front.fr_tab_circle.circle_options_var.get()

        if metodo == "Paramétrico":
            self.circulo_parametrico(xc, yc, radius, 1, ImageColor.getcolor("red", "RGBA"))
        elif metodo == "Simétrico":
            self.circulo_simetrico(xc, yc, radius, ImageColor.getcolor("blue", "RGBA"))
        else:
            self.circulo_simetrico(xc, yc, radius, ImageColor.getcolor("blue", "RGBA"))
            self.circulo_parametrico(xc, yc, radius, 1, ImageColor.getcolor("red", "RGBA"))

        self.front.fr_tab_circle.update_canvas(
            self.image.resize((320, 320), Image.NEAREST).transpose(Image.FLIP_TOP_BOTTOM)
        )

    def redraw_circle(self, a=None, b=None, c=None):
        self.clear_img()
        self.draw_circle()

    def save_img(self, filename: str):
        self.image.transpose(Image.FLIP_TOP_BOTTOM).save("./output/" + filename, format="png")

    def linha_analitico(self, x1, y1, x2, y2, color):
        if x1 != x2:
            m = (y2 - y1) / (x2 - x1)
            b = y2 - m * x2

            for x in range(x1, x2 + 1):
                y = m * x + b
                self.image.putpixel((round(x), round(y)), color)
        else:
            for y in range(y1, y2 + 1):
                self.image.putpixel((round(x1), round(y)), color)

    def linha_dda(self, x1, y1, x2, y2, color):
        if abs(x2 - x1) > abs(y2 - y1):
            inc = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 0
            y = y1

            for x in range(x1, x2 + 1):
                self.image.putpixel((round(x), round(y)), color)
                y += inc
        else:
            inc = (x2 - x1) / (y2 - y1) if (y2 - y1) != 0 else 0
            x = x1

            for y in range(y1, y2 + 1):
                self.image.putpixel((round(x), round(y)), color)
                x += inc

    def circulo_parametrico(self, xc, yc, radius, step, color):
        x = xc + radius
        y = yc

        for theta in range(0, 360, step):
            # Variable 'theta' increases by 1 each loop
            # A sufficiently large circumference will start showing gaps because of this
            try:
                # Prevent pillow from using negative indexes
                if x >= 0 and y >= 0:
                    self.image.putpixel((round(x), round(y)), color)
            except IndexError:
                pass  # Pixel would have been drawn out of bounds
            x = xc + radius * cos(radians(theta))
            y = yc + radius * sin(radians(theta))

    def circulo_simetrico(self, xc, yc, radius, color):
        x = radius
        y = 0
        theta = 1/radius  # Here, 'theta' is in radians

        while x > y:
            try:
                # Quadrant I
                self.image.putpixel((round(x + xc), round(y + yc)), color)
                self.image.putpixel((round(y + xc), round(x + yc)), color)
                # Quadrant II
                self.image.putpixel((round(-y + xc), round(x + yc)), color)
                self.image.putpixel((round(-x + xc), round(y + yc)), color)
                # Quadrant III
                self.image.putpixel((round(-x + xc), round(-y + yc)), color)
                self.image.putpixel((round(-y + xc), round(-x + yc)), color)
                # Quadrant IV
                self.image.putpixel((round(y + xc), round(-x + yc)), color)
                self.image.putpixel((round(x + xc), round(-y + yc)), color)
            except IndexError:
                pass  # Pixel would have been drawn out of bounds

            xn = x
            yn = y
            x = xn * cos(theta) - yn * sin(theta)
            y = yn * cos(theta) + xn * sin(theta)
