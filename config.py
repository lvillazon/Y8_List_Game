""" TODO read any constants that might need to be changed from a txt file """
from collections import namedtuple

import pygame

GAME_NAME = "Untitled List Game"
VERSION = "0.0"
MSG_VERBOSITY = 9

WINDOW_SIZE = (1600,900)

BLOCK_SIZE = 256

# Colour palette
SKY_BLUE = pygame.Color(138, 198, 224)

Point = namedtuple('Point', ['x', 'y'])