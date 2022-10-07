import pygame, sys
from game_loop import *


"""
pygame.init()

grid_size = width, height = 300, 400

screen = pygame.display.set_mode(grid_size)
screen.fill((0, 0, 0))"""

if __name__ == "__main__":
    game_loop(24, 16, tick_delay=0.250)

    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()"""


