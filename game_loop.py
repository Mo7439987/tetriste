from grille import *
from piece import *
from importador_dos_mil import *
from time import time
import keyboard as kb
import cv2


def game_loop(h, w, las_pieces=None, tick_delay=0.5, window_name='tretristre'):
    if las_pieces is None:
        las_pieces = importar_las_pieces('./pieces')
        #las_pieces = [las_pieces[3]]

    grille = [[None for _ in range(w)] for _ in range(h)]
    alive = True
    piece = None
    score = 0

    key_down = kb.is_pressed('down arrow')
    key_left = kb.is_pressed('left arrow')
    key_right = kb.is_pressed('right arrow')
    key_rotate_right = kb.is_pressed('x')
    key_rotate_left = kb.is_pressed('w')

    while alive:
        if piece is None:
            piece = piece_random(las_pieces)
            y, x = 0, w // 2
            if not peut_poser(piece, grille, x, y):
                print("c'est perdu.")
                exit()

        game_img = grille_to_image(poser_piece(piece, grille, x, y))
        cv2.imshow(window_name, game_img)
        cv2.waitKey(16)

        tick_start = time()
        while (time() - tick_start) < tick_delay:
            if kb.is_pressed('esc'):
                print('ovoire')
                exit()

            prev_key_down = key_down
            prev_key_left = key_left
            prev_key_right = key_right
            prev_key_rotate_right = key_rotate_right
            prev_key_rotate_left = key_rotate_left

            key_down = kb.is_pressed('down arrow')
            key_left = kb.is_pressed('left arrow')
            key_right = kb.is_pressed('right arrow')
            key_rotate_right = kb.is_pressed('x')
            key_rotate_left = kb.is_pressed('w')

            new_x, new_y = x, y

            if key_down:# and not prev_key_down:
                new_y += 1
                if peut_poser(piece, grille, new_x, new_y):
                    y = new_y
                new_y = y
            if key_left and not prev_key_left:
                new_x -= 1
                if peut_poser(piece, grille, new_x, new_y):
                    x = new_x
                new_x = x
            if key_right and not prev_key_right:
                new_x += 1
                if peut_poser(piece, grille, new_x, new_y):
                    x = new_x
                new_x = x

            if key_rotate_left and not prev_key_rotate_left:
                new_piece = tourner_piece(piece, 3)
                if peut_poser(new_piece, grille, x, y):
                    piece = new_piece
            if key_rotate_right and not prev_key_rotate_right:
                new_piece = tourner_piece(piece, 1)
                if peut_poser(new_piece, grille, x, y):
                    piece = new_piece

            if peut_poser(piece, grille, x, y):
                grille_temp = poser_piece(piece, grille, x, y)
            else:
                break
            game_img = grille_to_image(grille_temp)

            cv2.putText(game_img, org=(32, 32), text=str(score), fontFace=cv2.FONT_HERSHEY_PLAIN,
                        fontScale=4, color=(255, 255, 255), thickness=2)
            cv2.imshow(window_name, game_img)
            cv2.waitKey(16)

        y += 1
        if not peut_poser(piece, grille, x, y):
            grille = grille_temp
            if not dans_la_grille(piece, grille, x, y):
                alive = False
                print("c'est perdu.")
                exit()
            piece = None
            lines_popped = pop_lignes(grille, window_name=window_name)
            if lines_popped > 0:
                print(f'+ {lines_popped ** 2 * w}')
                score += lines_popped ** 2 * w
                print(f'score: {score}')
        else:
            grille_temp = poser_piece(piece, grille, x, y)


def dans_la_grille(piece, grille, x, y):
    centre_y, centre_x = piece.centre
    centre_y, centre_x = centre_y + y, centre_x + x

    for pos in piece.forme:
        pos_y, pos_x = pos
        pos_y, pos_x = centre_y + pos_y, centre_x + pos_x
        if pos_y < 0 or pos_x < 0 or pos_x >= len(grille):
            return False
    return True


def pop_lignes(grille, window_name='tretristre', block_size=32):
    h = len(grille)
    empty_rows = []
    for y in range(h):
        row = grille[y]
        if None not in row:
            empty_rows.append(y)

    if empty_rows:
        white_texture = np.zeros(shape=(block_size, block_size), dtype='uint8')
        white_texture[0: block_size, 0: block_size] = 255
        white_block = Block(texture=white_texture)
        sequence = (white_block, None, white_block, None)
        for e in sequence:
            for y in empty_rows:
                row = grille[y]
                w = len(row)
                for x in range(w):
                    row[x] = e

            img = grille_to_image(grille)
            cv2.imshow(window_name, img)
            cv2.waitKey(128)
        for y in empty_rows:
            row = grille[y]
            grille.pop(y)
            grille.insert(0, [None for _ in row])
            img = grille_to_image(grille)
            cv2.imshow(window_name, img)
            cv2.waitKey(128)
    return len(empty_rows)

