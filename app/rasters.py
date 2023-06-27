import sys
from math import cos, sin, radians

import yaml
from PIL import Image, ImageColor

from ui import MainUI

sys.setrecursionlimit(20000)

yaml_file = open("./app/preenchimento.yaml")
fill_coords = yaml.full_load(yaml_file)
yaml_file.close()


class Rasters:
    def __init__(
            self,
            front: MainUI = None,
            image: Image = Image.new("RGBA", (160, 160), "white")
    ):
        self.front = front
        self.image = image

        # Initial states for each canvas in UI
        self.draw_line()
        self.redraw_circle()
        self.refill_area()

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
            # Area fill tab
            self.front.fr_tab_fill.fill_options_var.trace("w", self.refill_area)
            self.front.fr_tab_fill.figure_options_var.trace("w", self.refill_area)

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

        self.front.fr_tab_line.update_canvas(self.image)

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
            self.circulo_parametrico(xc, yc, radius, ImageColor.getcolor("red", "RGBA"))
        elif method == "Simétrico":
            self.circulo_simetrico(xc, yc, radius, ImageColor.getcolor("blue", "RGBA"))
        elif method == "Bresenham":
            ...  # TODO: Implementar o algoritmo de Bresenham.
        else:
            self.circulo_parametrico(xc, yc, radius, ImageColor.getcolor("red", "RGBA"))
            self.circulo_simetrico(xc, yc, radius, ImageColor.getcolor("blue", "RGBA"))

        self.front.fr_tab_circle.update_canvas(self.image)

    def redraw_circle(self, a=None, b=None, c=None):
        self.clear_img()
        self.draw_circle()

    def fill_area(self):
        if self.front is None:
            return

        figure_map = {
            'Retângulo': "rectangle",
            'Figura A': "figure_a",
            'Figura B': "figure_b",
            'Figura C': "figure_c",
            'Figura D': "figure_d",
        }

        method = self.front.fr_tab_fill.fill_options_var.get()
        figure = self.front.fr_tab_fill.figure_options_var.get()
        figure_option = figure_map[figure]
        shape_coords = fill_coords[figure_option]

        if method == "Flood Fill":
            # Create the polygon shape with lines to form an enclosed area
            for i in range(0, len(shape_coords['vertices'])):
                x1 = shape_coords['vertices'][i - 1]['x']
                x2 = shape_coords['vertices'][i]['x']
                y1 = shape_coords['vertices'][i - 1]['y']
                y2 = shape_coords['vertices'][i]['y']

                if abs(x2 - x1) > abs(y2 - y1):
                    if x2 > x1:
                        self.linha_dda(x1, y1, x2, y2, ImageColor.getcolor("black", "RGBA"))
                    else:
                        self.linha_dda(x2, y2, x1, y1, ImageColor.getcolor("black", "RGBA"))
                else:
                    if y2 > y1:
                        self.linha_dda(x1, y1, x2, y2, ImageColor.getcolor("black", "RGBA"))
                    else:
                        self.linha_dda(x2, y2, x1, y1, ImageColor.getcolor("black", "RGBA"))

            # Starting points for each enclosed area
            for i in range(0, len(shape_coords['seeds'])):
                self.flood_fill(
                    shape_coords['seeds'][i]['x'],
                    shape_coords['seeds'][i]['y'],
                    ImageColor.getcolor("white", "RGBA"),
                    ImageColor.getcolor("red", "RGBA")
                )
        elif method == "Varredura com Análise Geométrica":
            # Build edges table
            edges_table = []
            for i in range(0, len(shape_coords['vertices'])):
                x1 = shape_coords['vertices'][i - 1]['x']
                y1 = shape_coords['vertices'][i - 1]['y']
                x2 = shape_coords['vertices'][i]['x']
                y2 = shape_coords['vertices'][i]['y']
                m = (y2 - y1) / (x2 - x1) if (x2 - x1) else None  # Vertical edges default to None

                if m == 0:
                    continue  # Skip horizontal edges
                elif y2 >= y1:
                    edges_table.append((y1, y2, x1, m))
                else:
                    edges_table.append((y2, y1, x2, m))

            self.analise_geom_fill(edges_table, ImageColor.getcolor("blue", "RGBA"))

        self.front.fr_tab_fill.update_canvas(self.image)

    def refill_area(self, a=None, b=None, c=None):
        self.clear_img()
        self.fill_area()

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

    def circulo_parametrico(self, xc, yc, radius, color, step=1):
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

        while x >= y:
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

    def flood_fill(self, x, y, old_color, new_color):
        current_color = self.image.getpixel((x, y))
        if current_color == old_color:
            self.image.putpixel((x, y), new_color)
            self.flood_fill(x, y + 1, old_color, new_color)
            self.flood_fill(x + 1, y, old_color, new_color)
            self.flood_fill(x, y - 1, old_color, new_color)
            self.flood_fill(x - 1, y, old_color, new_color)

    def analise_geom_fill(self, edges_table, color):
        min_y = min([e[0] for e in edges_table])
        max_y = max([e[1] for e in edges_table])

        # Scan happens from 'min_y' to 'max_y'
        for cur_y in range(min_y, max_y + 1):
            intersections = []
            for edge in edges_table:
                min_y = edge[0]
                max_y = edge[1]
                x_of_min_y = edge[2]
                m = edge[3]

                if min_y <= cur_y <= max_y:
                    if m is None:
                        # Vertical edge, use x of min_y instead
                        intersections.append(x_of_min_y)
                        continue

                    # Find the point of intersection ('x') for the current edge
                    x = (cur_y - min_y) / m + x_of_min_y
                    intersections.append(x)

            print(cur_y, intersections)

            intersections.sort()  # Sorting intersection values is needed
            next_x = intersections.pop(0)
            paint_count = 0

            for cur_x in range(0, self.image.width):
                # Increment 'paint_count' each time scan crosses an intersection
                if cur_x >= next_x:
                    paint_count += 1
                    try:
                        next_x = intersections.pop(0)
                    except IndexError:
                        next_x = float('inf')

                # Paint if 'inside' geometry
                if paint_count % 2 == 1:
                    self.paint_pixel(cur_x, cur_y, color)
