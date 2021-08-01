from typing import Optional

import pygame
from pygame.surface import Surface

from config import BLOCK_SIZE
from console_messages import console_msg

def default_image():
    return pygame.Surface(BLOCK_SIZE).convert()

class SpriteSheet():
    """ grabs individual sprites from a sheet
    modified from the flat version used in BitQuest """

    def __init__(self, filename, block_size: int, scale: float = 1.0):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error:
            console_msg("Failed to load spritesheet:" + filename, 0)
            raise SystemExit
        self.scale = scale
        self.block_size = int(block_size * scale)
    
    def get_rows(self) -> int:
        return self.sheet.get_height() // BLOCK_SIZE

    def get_columns(self) -> int:
        return self.sheet.get_width() // BLOCK_SIZE

    def get_tile_width(self) -> int:
        return BLOCK_SIZE

    def get_tile_height(self) -> int:
        return BLOCK_SIZE

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

