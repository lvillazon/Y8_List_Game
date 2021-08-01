# Handles isometric ground tiles and static scenery elements

import random
import pygame
import isometric_spritesheet
from camera import Camera
from config import BLOCK_SIZE, SKY_BLUE


class Terrain:
    def __init__(self, display, width, length):
        # create an isometric tile grid, of width x length tiles
        self._display = display
        # load all tile images from the spritesheet
        self.tile_palette = isometric_spritesheet.SpriteSheet(
            "assets\iso_blocks_hi-res.png", BLOCK_SIZE, 1)
        self.zoomed_tiles = []
        for row in range(self.tile_palette.get_rows()):
            for col in range(self.tile_palette.get_columns()):
                tile_rect = pygame.Rect(
                    col * BLOCK_SIZE,
                    row * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
                self.zoomed_tiles.append(
                    self.tile_palette.image_at(tile_rect, -1).copy())
        self.base_tiles = tuple(self.zoomed_tiles)  # master copy

        # build the 'map' of tile numbers representing the terrain tiles
        # this might eventually be read from a file
        self.columns = width
        self.rows = length
        self.tile_grid = []
        for x in range(width):
            row = []
            for y in range(length):
                tile = random.randint(0, len(self.base_tiles)-1)
                row.append(tile)
            self.tile_grid.append(row)

    @property
    def display(self):
        return self._display

    def update(self, centred_on, zoom):
        # render the terrain tiles with the correct pan and zoom
        # transform all tiles to the current zoom level
        new_size = (int(self.tile_palette.get_tile_width() * zoom),
                    int(self.tile_palette.get_tile_height() * zoom))
        #new_size = (32, 32)
        for i in range(len(self.base_tiles)):
            tile = self.base_tiles[i].copy()
            scaled_tile = pygame.transform.smoothscale(tile, new_size)
            color_key = scaled_tile.get_at((0, 0))
            scaled_tile.set_colorkey(color_key, pygame.RLEACCEL)
            self.zoomed_tiles[i] = scaled_tile.copy()
        zoomed_block_size = int(self.tile_palette.block_size * zoom)
        #BLOCK_SIZE = 256
        tile_x_increment = zoomed_block_size // 2
        tile_y_increment = zoomed_block_size // 4
        # calculate the start position for the top left of the grid
        # so that the centre of the grid is positioned
        # over the centred_on coords
        start_x = (centred_on.x -
                   (self.rows / 2) * tile_x_increment +
                   (self.columns / 2) * tile_x_increment -
                   zoomed_block_size // 2
                   )
        start_y = (centred_on.y -
                   (self.columns / 2) * tile_y_increment -
                   (self.rows / 2) * tile_y_increment -
                   12 # FUDGE FACTOR - BLOCK_SIZE * 3 / 16?? WHY THIS?
                   )
        for row in self.tile_grid:
            x = start_x
            y = start_y
            for tile in row:
                self.display.blit(self.zoomed_tiles[tile], (x, y))
                #pygame.display.update()
                #pygame.time.wait(100)
                x += tile_x_increment
                y += tile_y_increment
            start_x -= tile_x_increment
            start_y += tile_y_increment

        self.draw_crosshairs(self.display)

    def old_update(self, centred_on, zoom):
        # render the terrain tiles with the correct pan and zoom
        # draw initially onto a temp surface, then zoom it
        canvas_width = self.display.get_width() * 1
        canvas_height = self.display.get_height() * 1
        canvas = pygame.Surface((canvas_width, canvas_height))
        canvas.fill(SKY_BLUE)
        TILE_X_INCREMENT = self.tile_palette.block_size // 2
        TILE_Y_INCREMENT = self.tile_palette.block_size // 4
        # calculate the start position for the top left of the grid
        # so that the centre of the grid is positioned
        # over the centred_on coords
        start_x = (centred_on.x -
                   (self.rows / 2) * TILE_X_INCREMENT +
                   (self.columns / 2) * TILE_X_INCREMENT -
                   BLOCK_SIZE // 2
                   )
        start_y = (centred_on.y -
                   (self.columns / 2) * TILE_Y_INCREMENT -
                   (self.rows / 2) * TILE_Y_INCREMENT -
                   12 # FUDGE FACTOR - BLOCK_SIZE * 3 / 16?? WHY THIS?
                   )
        for row in self.tile_grid:
            x = start_x
            y = start_y
            for tile in row:
                canvas.blit(tile, (x, y))
                x += TILE_X_INCREMENT
                y += TILE_Y_INCREMENT
            start_x -= TILE_X_INCREMENT
            start_y += TILE_Y_INCREMENT

        new_size = (int(canvas.get_width()*zoom),
                    int(canvas.get_height()*zoom))
        canvas = pygame.transform.smoothscale(canvas, new_size)
        # copy the temp canvas onto the actual display surface
        new_position = (self.display.get_width() // 2 - canvas.get_width() // 2,
                        self.display.get_height() // 2 - canvas.get_height() // 2)
        self.display.blit(canvas, new_position)
        self.draw_crosshairs(self.display)

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

    def draw_crosshairs(self, display):
        # add a cross at the current camera position
        cross_hairs_length = 20
        cx = display.get_width() // 2
        cy = display.get_height() // 2
        pygame.draw.line(display, "red",
                         (cx - cross_hairs_length, cy),
                         (cx + cross_hairs_length, cy))
        pygame.draw.line(display, "red",
                          (cx, cy - cross_hairs_length),
                          (cx, cy + cross_hairs_length))

