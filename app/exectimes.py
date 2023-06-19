import time

from PIL import Image, ImageColor

from rasters import Rasters

rasters = Rasters(
    image=Image.new("RGBA", (400, 400), "white")
)


def circle_exec_times(
        circle_rasters: Rasters,
        output_fname: str,
        radius_incr: int
):
    image_dim = circle_rasters.image.size
    results = open(f"./output/{output_fname}", "w")

    circle_params = {
        'xc': image_dim[0] // 2,  # Circle center at half the image dimensions
        'yc': image_dim[1] // 2,
        'color': ImageColor.getcolor("black", "RGBA")
    }

    def measure(func, img_fname):
        for i in range(0, min(image_dim) // 2, radius_incr):
            circle_rasters.clear_img()

            start = time.perf_counter_ns()
            func(radius=i, **circle_params)
            end = time.perf_counter_ns()

            circle_rasters.save_img(f"{img_fname}_{i}.png")
            results.write(f"radius: {i:3d}, exec-time: {end - start} ns\n")

    results.write(f"Image dimensions: {image_dim[0]} x {image_dim[1]}\n\n"
                  f"Circunference parameters:\n"
                  f"Xc: {circle_params['xc']}\n"
                  f"Yc: {circle_params['yc']}\n"
                  f"Color: {circle_params['color']}\n")

    results.write("\nCírculo paramétrico:\n")
    measure(circle_rasters.circulo_parametrico, "circulo_parametrico")

    results.write("\nCírculo incremental simétrico:\n")
    measure(circle_rasters.circulo_simetrico, "circulo_simetrico")

    results.close()


circle_exec_times(rasters, "circle_exec_times.txt", 10)
