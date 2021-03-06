from PIL import Image
import sys
from math import ceil


SCALE = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """
START = """
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body><font style="font-family:monospace;font-size:10;background-color:black;font-weight:bolder;">
"""
END = """</font></body></html>"""
SQUASH_VALUE = 25


def get_pixel_values(image):
    pixels = image.load()
    pixel_matrix = []
    row, col = image.size
    for i in range(row):
        pixel_matrix.append([])
        for j in range(col):
            r, g, b = pixels[i, j]
            pixel_matrix[-1].append({
                "r": r,
                "g": g,
                "b": b,
            })

    return pixel_matrix


def scale_rgb(value):
    if not value: return SCALE[0]
    sl = len(SCALE)  # length of SCALE
    return SCALE[(ceil(sl / (((256 * 3 - value) / value) + 1))) - 1]


def populate_letters(matrix):
    for row in matrix:
        for pixel in row:
            letter = scale_rgb(pixel["r"] + pixel["g"] + pixel["b"])
            pixel["letter"] = letter if letter != " " else "&nbsp"


def squash_pixels(matrix):
    new_matrix = []
    S = SQUASH_VALUE
    row, col = len(matrix) // S, len(matrix[0]) // S
    for i in range(row):
        new_matrix.append([])
        for j in range(col):
            new_r = new_g = new_b = 0
            for inner_row in range(i * S, i * S + S):
                for inner_col in range(j * S, j * S + S):
                    v = matrix[inner_row][inner_col]
                    new_r += v["r"]
                    new_g += v["g"]
                    new_b += v["b"]
            new_matrix[-1].append({
                "r": new_r // (S * S),
                "g": new_g // (S * S),
                "b": new_b // (S * S)
            })
    return new_matrix


def rotate_matrix(matrix):
    new_matrix = []
    for i in range(len(matrix[0])):
        new_matrix.append([])
        for j in range(len(matrix)):
            new_matrix[-1].append(matrix[j][i])
    return new_matrix


def main():
    try:
        image_name = sys.argv[1]
    except IndexError:
        print("Provide an image name as argument. Aborting mission")
        exit()

    try:
        image = Image.open(image_name, 'r')
    except Exception as e:
        print(e)
        print("Image not found! Aborting mission")
        exit()

    print("Getting image pixel values")
    pixel_matrix = get_pixel_values(image)
    print("Squashing pixels to reasonable size")
    pixel_matrix = squash_pixels(pixel_matrix)
    print("Creating appropriate letters for pixels")
    populate_letters(pixel_matrix)
    print("rotating the picture matrix")
    pixel_matrix = rotate_matrix(pixel_matrix)

    html_string = START
    for row in pixel_matrix:
        for pix in row:
            r, g, b = pix["r"], pix["g"], pix["b"]
            html_string += (
                "<span style=\"color:rgb({},{},{});\">{}</span>".format(
                    r, g, b, pix["letter"]))
        html_string += ("</br>")
    html_string += (END)
    filename = image_name[:image_name.index(".")]
    with open(filename + ".html", "w") as f:
        f.write(html_string)
    print("HTML file created")

if __name__ == '__main__':
    main()
