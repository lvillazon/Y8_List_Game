""" TODO read any constants that might need to be changed from a txt file """
from collections import namedtuple

import pygame

GAME_NAME = "Untitled List Game"
VERSION = "0.0"
MSG_VERBOSITY = 9

WINDOW_SIZE = (1600,830)

BLOCK_SIZE = 256

# Colour palette
SKY_BLUE = (138, 198, 224)
LIGHT_GREEN = (186, 212, 173)
TEAL = (85, 145, 133)
DARK_GREEN = (127, 147, 98)
STRAW = (226, 212, 147)
GOLD = (224, 153, 63)
TAN = (209, 188, 157)
BROWN = (151, 56, 54)
BEAR_BROWN = (183, 142, 112)
UI_BACKGROUND = BEAR_BROWN
UI_FOREGROUND = STRAW

Point = namedtuple('Point', ['x', 'y'])