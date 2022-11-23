import numpy as np
from piece import Block
from colorsys import hsv_to_rgb


def grille_to_image(grille, pxl_size=32):
    h = len(grille)

    if h < 1:
        return None

    score_h = 64
    w = len(grille[0])
    img_h, img_w = h * pxl_size + score_h, w * pxl_size
    img = np.zeros(shape=(img_h, img_w, 3), dtype='uint8')
    img[0:score_h, 0:img_w] = [32] * 3

    for y in range(h):
        img_y0 = y * pxl_size + score_h
        img_y1 = (y + 1) * pxl_size + score_h
        for x in range(w):
            if grille[y][x] is not None:

                img_x0 = x * pxl_size
                img_x1 = (x + 1) * pxl_size
                img[img_y0:img_y1, img_x0:img_x1] = grille[y][x].display_texture
    return img


def print_grille(grille):
    h = len(grille)

    w = len(grille[0])
    s = ''
    for y in range(h):
        for x in range(w):
            if grille[y][x] is not None:
                s += '#'
            else:
                s += ' '
        s += '\n'
    print(s)
