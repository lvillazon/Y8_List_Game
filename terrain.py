# Handles isometric ground tiles and static scenery elements

import random
import pygame
import isometric_spritesheet
from camera import Camera
from config import BLOCK_SIZE

class Terrain:
    def __init__(self, display, width, length):
        # create an isometric tile grid, of width x length tiles
        self._display = display
        self.camera = Camera()
        self.display_centre = (display.get_width() // 2,
                               display.get_height() // 2)
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

    @property
    def display(self):
        return self._display

    def update(self, pos):
        # test render of the screen filled with grass tiles
        TILE_X_INCREMENT = self.tile_palette.block_size // 2
        TILE_Y_INCREMENT = self.tile_palette.block_size // 4
        # calculate the start position for the top left of the grid
        # so that the centre of the grid is positioned
        # over the centre of the screen +/- the camera offset
        start_x, start_y = pos #self.display_centre
        start_x += (self.camera.x -
                   (self.rows // 2) * TILE_X_INCREMENT +
                   (self.columns // 2) * TILE_X_INCREMENT -
                   BLOCK_SIZE // 2
                   )
        start_y += (self.camera.y -
                   (self.columns // 2) * TILE_Y_INCREMENT -
                   (self.rows // 2) * TILE_Y_INCREMENT +
                   4  # FUDGE FACTOR - is it TILE_Y_INCREMENT // 4?
                   )
        for row in self.tile_grid:
            x = start_x
            y = start_y
            for tile in row:
                self.display.blit(tile, (x, y))
                x += TILE_X_INCREMENT
                y += TILE_Y_INCREMENT
            start_x -= TILE_X_INCREMENT
            start_y += TILE_Y_INCREMENT

        self.camera.draw_crosshairs(self.display)

    def rotate(self):
        # transpose the terrain grid to rotate the landscape through 90 degrees
        # this is a relatively slow method
        # could use zip() or the numpy library, if we need more speed
        rotated = []
        for i in range(len(self.tile_grid[0])):
            transposed_row = []
            for row in self.tile_grid:
                transposed_row.insert(0, row[i])
            rotated.append(transposed_row)
        self.tile_grid = rotated
