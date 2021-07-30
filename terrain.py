# Handles isometric ground tiles and static scenery elements

import random
import pygame
import isometric_spritesheet
from config import BLOCK_SIZE

class Terrain:
    def __init__(self, width, length):
        # create an isometric tile grid, of width x length tiles
        # load all tile images from the spritesheet
        self.tile_palette = isometric_spritesheet.SpriteSheet(
            "assets\iso_blocks_basic.png", BLOCK_SIZE, 1)
        self.ground_tiles = []
        for row in range(self.tile_palette.get_rows()):
            for col in range(self.tile_palette.get_columns()):
                tile_rect = pygame.Rect(
                    col * BLOCK_SIZE,
                    row * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
                self.ground_tiles.append(
                    self.tile_palette.image_at(tile_rect, -1))

        # build the grid of terrain tiles for this map
        # this might eventually be read from a file
        self.columns = width
        self.rows = length
        self.tile_grid = []
        for x in range(width):
            row = []
            for y in range(length):
                tile = random.choice(self.ground_tiles)
                row.append(tile.copy())
            self.tile_grid.append(row)

    def update(self, display):
        # test render of the screen filled with grass tiles
        TILE_X_INCREMENT = self.tile_palette.block_size // 2
        TILE_Y_INCREMENT = self.tile_palette.block_size // 4
        camera_x = display.get_width() // 2
        camera_y = display.get_height() // 2
        # calculate the start position for the top left of the grid
        # so that the grid is in the middle of the screen
        # TODO add a camera offset, to allow scrolling
        start_x = (camera_x -
                   (self.rows // 2) * TILE_X_INCREMENT +
                   (self.columns // 2) * TILE_X_INCREMENT -
                   BLOCK_SIZE // 2
                   )
        start_y = (camera_y -
                   (self.columns // 2) * TILE_Y_INCREMENT -
                   (self.rows // 2) * TILE_Y_INCREMENT +
                   4  # FUDGE FACTOR - is it TILE_Y_INCREMENT // 4?
                   )
        for row in self.tile_grid:
            x = start_x
            y = start_y
            for tile in row:
                display.blit(tile, (x, y))
                x += TILE_X_INCREMENT
                y += TILE_Y_INCREMENT
            start_x -= TILE_X_INCREMENT
            start_y += TILE_Y_INCREMENT

        # DEBUG - draw cross hairs in the centre, to check grid draws ok
        centre_x = display.get_width() // 2
        centre_y = display.get_height() // 2
        cross_hairs_length = 20
        pygame.draw.line(display, "red",
                         (centre_x - cross_hairs_length, centre_y),
                         (centre_x + cross_hairs_length, centre_y))
        pygame.draw.line(display, "red",
                          (centre_x, centre_y - cross_hairs_length),
                          (centre_x, centre_y + cross_hairs_length))
        # random.seed(self.rng_seed)
        # start_x = display.get_width()
        # while start_x > 0:
        #     y = 100  # horizon height
        #     x = start_x
        #     while x < display.get_width():
        #         x += TILE_X_INCREMENT
        #         y += TILE_Y_INCREMENT
        #         tile = random.choice(self.ground_tiles)
        #         display.blit(tile, (x, y))
        #     start_x -= self.tile_palette.block_size
