import pygame

import isometric_spritesheet
from console_messages import console_msg


class World:
    def __init__(self, screen):
        console_msg('Initialising world', 0)
        self.display = screen
        # load placeholder grass tile
        grass_tiles = isometric_spritesheet.SpriteSheet("assets\Grass-Spritesheet_Blocks.png", 0.2)
        tile_rect = pygame.Rect(50, 80, 400, 360)
        self.floor_tile = grass_tiles.image_at(tile_rect, -1)

    def update(self):
        # TODO separate this into a separate renderer
        # for the background tiles and the foreground sprites

        self.display.fill("white")

        # test render of the screen filled with grass tiles
        TILE_X_INCREMENT = self.floor_tile.get_width() // 2
        TILE_Y_INCREMENT = 20
        row_start = self.display.get_width()
        for row in range(25):
            x = row_start - row * self.floor_tile.get_width()
            y = 0
            for col in range(30):
                x += TILE_X_INCREMENT
                y += TILE_Y_INCREMENT
                self.display.blit(self.floor_tile, (x, y))
        pygame.display.update()
