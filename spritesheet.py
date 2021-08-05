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
                 block_x: int, block_y:int = 0,
                 scale: float = 1.0):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error:
            console_msg("Failed to load spritesheet:" + filename, 0)
            raise SystemExit
        self.scale = scale
        if block_y:
            self.block_size = Point(block_x, block_y)
        else:
            self.block_size = Point(block_x, block_x)
    
    def get_rows(self) -> int:
        return self.sheet.get_height() // self.block_size.y

    def get_columns(self) -> int:
        return self.sheet.get_width() // self.block_size.x

    def get_tile_width(self) -> int:
        return self.block_size.x

    def get_tile_height(self) -> int:
        return self.block_size.y

    def image_at(self, rectangle, color_key: Optional = None) -> pygame.Surface:
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)
        final_size = (int(rect.width * self.scale), int(rect.height * self.scale))
        return pygame.transform.scale(image, final_size)

