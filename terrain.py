# Handles isometric ground tiles and static scenery elements

import random
import pygame
import pygame.gfxdraw
import spritesheet
from camera import Camera
from config import *


class Terrain:
    def __init__(self, display, length, width, zoom, cultivated):
        # create an isometric tile grid, of width x length tiles
        self._display = display
        self.original_block_size = 256  # default for zoom = 1.0
        self.zoom = zoom
        self.cultivated = cultivated
        # signals that the landscape should be regenerated from tiles
        self.landscape_cache_dirty = True

        # load all tile images from the spritesheet
        # replaced by procedurally drawn tiles, for now
        # self.tile_palette = isometric_spritesheet.SpriteSheet(
        #     "assets\iso_blocks_hi-res.png", BLOCK_SIZE, 1)
        # self.zoomed_tiles = []
        # for row in range(self.tile_palette.get_rows()):
        #     for col in range(self.tile_palette.get_columns()):
        #         tile_rect = pygame.Rect(
        #             col * BLOCK_SIZE,
        #             row * BLOCK_SIZE,
        #             BLOCK_SIZE,
        #             BLOCK_SIZE
        #         )
        #         self.zoomed_tiles.append(
        #             self.tile_palette.image_at(tile_rect, -1).copy())
        # self.base_tiles = tuple(self.zoomed_tiles)  # master copy

        self.tile_colours = {
            "light green": LIGHT_GREEN,
            "teal"       : TEAL,
            "dark green" : DARK_GREEN,
            "straw"      : STRAW,
            "gold"       : GOLD,
            "tan"        : TAN,
            "brown"      : BROWN,
        }

        # build a dict all all tile types, keyed by colour
        # the change_zoom() function recreates all the tiles anyway, so
        # we can just use that
        self.all_tiles = {}
        self.change_zoom(self.zoom)

        # build the grid of tile colours representing the terrain tiles
        # this might eventually be read from a file
        self.columns = width
        self.rows = length
        self.tile_grid = []
        for x in range(width):
            row = []
            for y in range(length):
                if Point(x,y) in self.cultivated:
                    tile = BROWN
                else:
                    tile = DARK_GREEN
                row.append(tile)
            self.tile_grid.append(row)

        # set the colour of all furrows


        # generate a single image composed of the tiles arranged in the grid
        self.landscape = self.regen_landscape()

    @property
    def display(self):
        return self._display

    def update(self, centred_on):
        # render the current landscape with the correct x,y panning
        if self.landscape_cache_dirty:
            self.landscape = self.regen_landscape()
        return self.landscape

    def regen_landscape(self) -> pygame.Surface:
        # assembles all the tiles in the map into a single image
        # this only needs to be done when one of the tiles changes
        # or the map is zoomed or rotated.
        # The rest of the time, the cached landscape can be used.

        tile_inc = self.get_tile_increment()
        # calculate the space needed for the whole tile grid
        rows = self.get_rows()
        cols = self.get_cols()
        min_x = -tile_inc.x * rows
        max_x = tile_inc.x * cols
        min_y = 0
        max_y = tile_inc.y * (rows + cols+1) #+ tile_x_increment
        size = (max_x - min_x, max_y - min_y)
        landscape = pygame.Surface(size)
        landscape.fill(SKY_BLUE)

        # calculate the start position for the top left of the grid
        # so that it exactly fits on the grid
        start_x = (rows-1) * tile_inc.x
        start_y = 0

        for row in self.tile_grid:
            x = start_x
            y = start_y
            for colour in row:
                landscape.blit(
                    self.get_tile(colour),
                    (x, y))
                x += tile_inc.x
                y += tile_inc.y
            start_x -= tile_inc.x
            start_y += tile_inc.y
        self.landscape_cache_dirty = False  # because we have just updated
        return landscape

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
        self.landscape_cache_dirty = True

    def get_tile(self, colour) -> pygame.Surface:
        # returns a pre-zoomed tile surface from the cached dict
        return self.all_tiles[colour]

    def change_zoom(self, new_zoom):
        # rescale all the tiles in the cached dict
        for colour in self.tile_colours.values():
            self.all_tiles[colour] = self.draw_tile(new_zoom, colour)
        self.landscape_cache_dirty = True

    def draw_tile(self, zoom, top_face_colour) -> pygame.Surface:
        # procedurally create a single, flat terrain tile
        self.block_size = int(self.original_block_size * zoom)
        canvas = pygame.Surface((self.block_size, self.block_size))
        # the tile is sized to fill the canvas
        # turn lines off when the grid is too small
        line_width = min(1, int(6 * zoom))
        line_colour = "black"
        mid_width = canvas.get_width() // 2
        tile_height = canvas.get_height() // 4
        top_north = (mid_width, 0)
        top_south = (mid_width, tile_height * 2)
        top_east = (canvas.get_width()-line_width, tile_height)
        top_west = (0, tile_height)
        # bottom_north isn't needed because it is always hidden
        bottom_south = (mid_width, tile_height * 3)
        bottom_east = (canvas.get_width()-line_width, tile_height * 2)
        bottom_west = (0, tile_height * 2)
        top_face = (top_north, top_east, top_south, top_west)
        left_face = (top_west, top_south, bottom_south, bottom_west)
        right_face = (top_east, bottom_east, bottom_south, top_south)
        canvas.fill("red")  # for colour keying - don't use red on tiles
        canvas.set_colorkey("red")
        #pygame.draw.rect(canvas, "blue", canvas.get_rect(), 1)  # TEST bounding box
        pygame.draw.polygon(canvas, top_face_colour, top_face)
        pygame.draw.polygon(canvas, self.tile_colours["brown"], left_face)
        pygame.draw.polygon(canvas, self.tile_colours["tan"], right_face)
        pygame.draw.lines(canvas, line_colour, True, top_face, line_width)
        pygame.draw.lines(canvas, line_colour, True, left_face, line_width)
        pygame.draw.lines(canvas, line_colour, True, right_face, line_width)
        return canvas

    def get_rows(self) -> int:
        # number of tiles per column
        return len(self.tile_grid)

    def get_cols(self) -> int:
        # number of tiles per row):
        return len(self.tile_grid[0])

    def get_tile_increment(self) -> Point:
        return Point(self.block_size // 2, self.block_size // 4)

    def get_ground_coords(self, grid_position: Point) -> Point:
        # convert tile grid coords to pixel coords
        # the x coord of the bottom-left corner of the bottom-left tile
        # is always 0, and the top-right corner of the top-right tile is
        # always at x = terrain width
        # because the terrain surface is sized to exactly fit
        # so we can calculate the position of any tile using just the terrain
        # rectangle and the size of one tile

        tx = self. get_tile_increment().x
        ty = self.get_tile_increment().y
        r = self.get_rows()
        screen_pos = Point(
            (tx * (r - grid_position.y) + tx * grid_position.x),
            (r * ty - (r - grid_position.y) * ty + ty * grid_position.x)
        )
        return screen_pos
