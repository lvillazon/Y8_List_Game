""" TODO read any constants that might need to be changed from a txt file """
from collections import namedtuple

import pygame

from point import Point

GAME_NAME = "Thingummy Farm"
VERSION = "0.0"
MSG_VERBOSITY = 9
BOUNDING_BOX = False

# retained for backward compatibility with code that uses ordinary
# tuples for X,Y pairs
X = 0
Y = 1
WINDOW_SIZE = Point(1600,830)

BLOCK_SIZE = 256
SMOOTH_ZOOM_THRESHOLD = 0.4  # zooms smaller than this use smoothscaling

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

# Filepaths
CODE_FONT_FILE = "assets\\DejaVuSansMono.ttf"
EDITOR_ICON_FILE = "assets\\editor icons.png"

