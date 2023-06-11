import math
from PIL import Image, ImageColor


class Rasters:
    def __init__(self, front, image):
        self.front = front
        self.image = image

        self.draw_line()

        # Bindings
        self.front.p1x_var.trace("w", self.redraw_line)
        self.front.p1y_var.trace("w", self.redraw_line)
        self.front.p2x_var.trace("w", self.redraw_line)
        self.front.p2y_var.trace("w", self.redraw_line)
        self.front.line_options_var.trace("w", self.redraw_line)
        # TODO: Update bindings.

    def clear_img(self):
        # 'Clears' the image, painting with white
        for x in range(0, self.image.width):
            for y in range(0, self.image.height):
                self.image.putpixel((x, y), ImageColor.getcolor("white", "RGBA"))

    def draw_line(self):
        x1 = self.front.p1x_var.get()
        y1 = self.front.p1y_var.get()
        x2 = self.front.p2x_var.get()
        y2 = self.front.p2y_var.get()
        metodo = self.front.line_options_var.get()

        if metodo == "Analítico":
            self.linha_analitico(x1, y1, x2, y2, ImageColor.getcolor("red", "RGBA"))
        elif metodo == "DDA":
            self.linha_dda(x1, y1, x2, y2, ImageColor.getcolor("blue", "RGBA"))
        elif metodo == "Bresenham":
            ...  # TODO: Implementar o algoritmo de Bresenham.
        else:
            self.linha_dda(x1, y1, x2, y2, ImageColor.getcolor("blue", "RGBA"))
            self.linha_analitico(x1, y1, x2, y2, ImageColor.getcolor("red", "RGBA"))

        self.front.update_canvas(
            self.image.resize((320, 320), Image.NEAREST).transpose(Image.FLIP_TOP_BOTTOM)
        )

    def redraw_line(self, a=None, b=None, c=None):
        # 'a', 'b', e 'c' are unused parameters received by the callbacks
        self.clear_img()
        self.draw_line()

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

    def circulo_parametrico(self, xc, yc, radius, color):
        x = xc + radius
        y = yc

        for t in range(360):
            # Variable 't' increases by 1 each loop
            # A sufficiently large circumference will start showing gaps because of this
            self.image.putpixel((round(x), round(y)), color)
            x = xc + math.cos(t * math.pi / 180)
            y = yc + math.sin(t * math.pi / 180)

    def circulo_simetrico(self):
        ...  # TODO: Implementar a resterização incremental simétrica de circunferências.
