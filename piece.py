import cv2
import numpy as np
from random import choice
from copy import deepcopy
from fonction_utiles import *

block_texture = cv2.imread('texture.png', cv2.IMREAD_GRAYSCALE)


class Block:
    def __init__(self, couleur=(255, 255, 255), texture=block_texture):
        self.couleur = couleur
        self.texture = texture
        self.display_texture = colorer_image(texture, couleur)

    def recolor(self, couleur):
        self.couleur = couleur
        self.display_texture = self.texture * couleur

    def retexture(self, texture):
        self.texture = texture
        self.display_texture = texture * self.couleur


class Piece:
    def __init__(self, forme, centre, couleur=(255, 255, 255), texture=block_texture):
        self.forme = forme
        self.centre = centre
        self.couleur = couleur
        self.texture = texture
        self.block = Block(couleur, texture)


def peut_poser(piece, grille, x, y, orientation=0):
    if orientation > 0:
        new_piece = tourner_piece(piece, orientation)
        return peut_poser(new_piece, grille, x, y, 0)

    centre_y, centre_x = piece.centre
    centre_y, centre_x = centre_y + y, centre_x + x

    for block in piece.forme:
        pos_y, pos_x = block
        pos_y, pos_x = centre_y + pos_y, centre_x + pos_x
        if not (0 <= pos_y < len(grille) and 0 <= pos_x < len(grille[y])):
            return False
        if grille[int(pos_y)][int(pos_x)] is not None:
            return False
    return True


def poser_piece(piece, grille, x, y, orientation=0):
    if orientation > 0:
        new_piece = tourner_piece(piece, orientation)
        return poser_piece(new_piece, grille, x, y, 0)

    if peut_poser(piece, grille, x, y, orientation):
        centre_y, centre_x = piece.centre
        centre_x, centre_y = centre_x + x, centre_y + y

        grille_temp = deepcopy(grille)
        for pos in piece.forme:
            pos_y, pos_x = pos
            pos_y, pos_x = int(centre_y + pos_y), int(centre_x + pos_x)
            grille_temp[pos_y][pos_x] = piece.block
        return grille_temp

    return grille


def tourner_piece(piece, n):
    if n <= 0:
        return piece
    forme = piece.forme
    forme_temp = []
    centre = piece.centre
    for b in forme:
        (y, x) = (b[0] - centre[0], b[1] - centre[1])
        forme_temp.append((-x + centre[0], y + centre[1]))
    piece_temp = Piece(forme=forme_temp, centre=centre, couleur=piece.couleur, texture=piece.texture)
    return tourner_piece(piece_temp, n - 1)


def piece_random(las_pieces):
    return choice(las_pieces)
