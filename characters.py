import string
import pygame
import spritesheet
from config import Point
from terrain import Terrain


class Character:
    # sprites that animate around the grid
    # currently just the farmer
    def __init__(self, image_file: string, start_position: Point, zoom):
        self.poses = spritesheet.SpriteSheet(image_file, 420, 780, 1)
        sprite_rect = pygame.Rect(
            (0, 0),
            (self.poses.get_tile_width(),
             self.poses.get_tile_height())
        )
        self._sprite = self.poses.image_at(sprite_rect, -1)
        self._zoom = 1.0
        self.zoom(zoom)
        self.position = start_position  # grid coords on the terrain

    def zoom(self, magnification):
        # appply a fixed conversion factor so that the sprite looks
        # right for the terrain tiles. This will change if the characters
        # are redrawn at a different resolution
        magnification *= 0.5
        if self._zoom != magnification or self._zoomed_sprite == None:
            self._zoom = magnification
            self._zoomed_sprite = pygame.transform.scale(
                self._sprite,
                (
                    int(self._sprite.get_width() * self._zoom),
                    int(self._sprite.get_height() * self._zoom)
                )
            )

    def get_sprite(self):
        if self._zoomed_sprite != None:
            return self._zoomed_sprite
        else:
            return self._sprite