import numpy as np


def afficher_piece(piece):
    forme = piece.forme

    for y in range(5):
        for x in range(5):
            if (y, x) in forme:
                print('#', end='')
            else:
                print(' ', end='')
        print()
    print('.' * 8)


def multiplier_couleur(n, couleur):
    return tuple(a * n / 255 for a in couleur)


def colorer_image(img, couleur):
    h, w = img.shape
    img_temp = np.zeros(shape=(h, w, len(couleur)), dtype='uint8')
    for y in range(h):
        for x in range(w):
            pxl = int(img[y, x])
            pxl = multiplier_couleur(pxl, couleur)
            img_temp[y, x] = pxl
    #cv2.imwrite(f'test_{couleur}.png', img_temp)
    return img_temp

