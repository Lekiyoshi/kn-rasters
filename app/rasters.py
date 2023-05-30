from PIL import Image, ImageColor


class Rasters:
    def __init__(self, front, image):
        self.front = front
        self.image = image

        self.draw_line()

        # Bindings
        self.front.p1_x_var.trace("w", self.redraw_line)
        self.front.p1_y_var.trace("w", self.redraw_line)
        self.front.p2_x_var.trace("w", self.redraw_line)
        self.front.p2_y_var.trace("w", self.redraw_line)
        self.front.raster_options_var.trace("w", self.redraw_line)

    def clear_img(self):
        # 'Apaga' a imagem, pintando de branco
        for x in range(0, self.image.width):
            for y in range(0, self.image.height):
                self.image.putpixel((x, y), ImageColor.getcolor("white", "RGBA"))

    def draw_line(self):
        x1 = self.front.p1_x_var.get()
        y1 = self.front.p1_y_var.get()
        x2 = self.front.p2_x_var.get()
        y2 = self.front.p2_y_var.get()
        metodo = self.front.raster_options_var.get()

        if metodo == "Método Analítico":
            self.analitico(x1, y1, x2, y2, ImageColor.getcolor("red", "RGBA"))
        elif metodo == "DDA":
            self.dda(x1, y1, x2, y2, ImageColor.getcolor("blue", "RGBA"))
        else:
            self.dda(x1, y1, x2, y2, ImageColor.getcolor("blue", "RGBA"))
            self.analitico(x1, y1, x2, y2, ImageColor.getcolor("red", "RGBA"))

        self.front.update_canvas(
            self.image.resize((320, 320), Image.NEAREST).transpose(Image.FLIP_TOP_BOTTOM)
        )

    def redraw_line(self, a=None, b=None, c=None):
        # 'a', 'b', e 'c' são parâmetros extra recebidos pelos callbacks, não foram usados
        self.clear_img()
        self.draw_line()

    def analitico(self, x1, y1, x2, y2, color):
        if x1 != x2:
            m = (y2 - y1) / (x2 - x1)
            b = y2 - m * x2

            for x in range(x1, x2 + 1):
                y = m * x + b

                self.image.putpixel((round(x), round(y)), color)
        else:
            for y in range(y1, y2 + 1):
                self.image.putpixel((round(x1), round(y)), color)

        self.image.transpose(Image.FLIP_TOP_BOTTOM).save("./output/linha-metodo-analitico.png")

    def dda(self, x1, y1, x2, y2, color):
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

        self.image.transpose(Image.FLIP_TOP_BOTTOM).save("./output/linha-dda.png")
