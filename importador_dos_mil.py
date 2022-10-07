import cv2
import os
from piece import Piece


def case_noire(pixel_in):
    for a in pixel_in:
        if a != 0:
            return False
    return True


def import_piece(img):
    h, w, d = img.shape
    centre = float(h - 1) / 2.0, float(w - 1) / 2.0
    forme: list = []
    couleur: tuple = (0, 0, 0)
    valide = False
    for y in range(h):
        for x in range(w):
            pxl: tuple = img[y, x]
            case_pleine: bool = not case_noire(pxl)
            if case_pleine:
                forme.append((y, x))
                couleur: tuple = pxl
                valide = True

    if valide:
        return Piece(forme=forme, centre=centre, couleur=couleur)
    return None


def importar_las_pieces(dir_in='./pieces'):
    las_pieces = []     # initialise las_pieces comme vide

    for root, dirs, files in os.walk(dir_in):
        for file in files:
            path_in = os.path.join(root, file)

            path_split = path_in.split(os.sep)
            name, extension = os.path.splitext(path_split[-1])
            if extension in ('.png', '.jpg', '.jpeg', '.bmp'):
                img = cv2.imread(path_in)
                piece = import_piece(img)
                if piece is not None:
                    las_pieces.append(piece)
    return las_pieces


importer_les_pieces = importar_las_pieces

if __name__ == '__main__':
    las_pieces = importar_las_pieces()

