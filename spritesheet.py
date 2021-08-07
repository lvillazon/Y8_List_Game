from typing import Optional

import pygame
from pygame.surface import Surface

from config import Point
from console_messages import console_msg

def default_image():
    return pygame.Surface((0,0)).convert()

class SpriteSheet():
    """ grabs individual sprites from a sheet
    modified from the flat version used in BitQuest """

    def __init__(self, filename,
                 rows: int = 1, cols:int = 0,
                 scale: float = 1.0):
        try:
            sheet = pygame.image.load(filename).convert()
            self.sheet = trim_sprite(sheet)
        except pygame.error:
            console_msg("Failed to load spritesheet:" + filename, 0)
            raise SystemExit
        self.scale = scale
        self.sprites = []  # the individual sprites in the sheet - a 2D array
        size = Point(self.sheet.get_width() // cols,
                     self.sheet.get_height() // rows)
        for col in range(cols):
            sprite_row = []
            for row in range(rows):
                sprite_rect = pygame.Rect((col * size.x,
                                          row * size.y),
                                          size)
                sprite = self.image_at(sprite_rect, -1)
                sprite_row.append(sprite)
            self.sprites.append(sprite_row)

    def get_rows(self) -> int:
        return len(self.sprites)

    def get_columns(self) -> int:
        return len(self.sprites[0])

    def get_tile_width(self) -> int:
        return self.sprites[0][0].get_width()

    def get_tile_height(self) -> int:
        return self.sprites[0][0].get_height()

    def image_at(self, rectangle, color_key: Optional = None) -> pygame.Surface:
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)
        final_size = (int(rect.width * self.scale), int(rect.height * self.scale))
        return trim_sprite(pygame.transform.scale(image, final_size))
        return pygame.transform.scale(image, final_size)

def trim_sprite(source: pygame.Surface) -> pygame.Surface:
    # removes unnecessary background around the edges
    old_colorkey = source.get_colorkey()  # so we can restore later
    if source.get_colorkey() is None:
        # bounding rects only seem to work if there is a color key set
        # so we use the top left pixel colour, if there isn't one already
        source.set_colorkey(source.get_at((0,0)))

    trim_rect = source.get_bounding_rect()
    # restore original colorkey, to avoid side-effects
    source.set_colorkey(old_colorkey)

    trimmed = pygame.Surface(trim_rect.size).convert()
    trimmed.blit(source, (0, 0), trim_rect)
    # set the colorkey to black
    # I think this is because the colorkey was already set to the original
    # image background by the image_at method. So the background pixels
    # are already black? Not sure, but if you try copying the colorkey of
    # the source image, then it displays black background pixels
    # Setting the colorkey to black, seems to fix this.
    trimmed.set_colorkey((0,0,0,255))
    return trimmed
