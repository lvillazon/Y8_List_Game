import random
import pygame
from pygame import time
from math import copysign

import characters
import spritesheet
from config import BLOCK_SIZE, SKY_BLUE, Point
from console_messages import console_msg
from panel import Panel
from terrain import Terrain
from talking_head import TalkingHead


class World:
    def __init__(self, screen):
        console_msg('Initialising world', 0)
        self.display = screen
        self.zoom = 0.25
        self.terrain = Terrain(screen, 5, 8, self.zoom)
        self.viewpoint = Point(screen.get_width() // 2,
                               screen.get_height() // 2)
        self.old_viewpoint = Point(0,0)
        self.drag_start = Point(0,0)

        # UI panels
        self.talking_head = TalkingHead(screen, Point(0,0), Point(700, 200))
        self.basket = Panel(screen,
                            Point(screen.get_width()-200,0),
                            Point(200, screen.get_height())
                            )

        # Characters
        self.farmer = characters.Character("assets\\farmer cropped.png",
                                           Point(2,4),
                                           self.zoom)

        self.running = True
        self.frame_counter = 0
        self.clock = pygame.time.Clock()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # left button
                    # check which panel we are over
                    if self.talking_head.mouse_over():
                        self.talking_head.cycle_head()
                    else:
                        # terrain window, so we are dragging
                        self.drag_start = Point(*pygame.mouse.get_pos())
                        self.old_viewpoint = self.viewpoint
                elif pygame.mouse.get_pressed()[2]:  # right button
                    self.terrain.rotate()
            elif event.type == pygame.MOUSEWHEEL:
                min_zoom = .1
                max_zoom = 10
                # adjust zoom level by +/- 10%
                self.zoom *= 1 + .1 * copysign(1, event.y)
                # constrain zoom between min_ and max_
                self.zoom = min(max(self.zoom, min_zoom), max_zoom)
                self.terrain.change_zoom(self.zoom)
                self.farmer.zoom(self.zoom)
                #print(self.zoom, min(1, int(4 * self.zoom)))

        if pygame.mouse.get_pressed()[0]:  # LMB held down
            if not self.talking_head.mouse_over():
                drag_x = self.drag_start.x - pygame.mouse.get_pos()[0]
                drag_y = self.drag_start.y - pygame.mouse.get_pos()[1]
                self.viewpoint = Point(self.old_viewpoint.x + drag_x,
                                       self.old_viewpoint.y + drag_y)

        # render all onscreen objects
        self.display.fill(SKY_BLUE)
        landscape = self.terrain.update(self.viewpoint)
        offset_position = Point(self.display.get_width()
                                - landscape.get_width() // 2
                                - self.viewpoint.x,
                                self.display.get_height()
                                - landscape.get_height() // 2
                                - self.viewpoint.y)

        self.display.blit(landscape, offset_position)
        # calculate the pixel coords of the farmer's grid tile
        sprite = self.farmer.get_sprite()
        raw_ground_position = self.terrain.get_ground_coords(self.farmer.position)
        # offset this position so the sprite appears to be standing
        # in the middle of the tile
        sprite_position = Point((raw_ground_position.x
                                  - self.terrain.get_tile_increment().x
                                  ),
                                 (raw_ground_position.y
                                  - sprite.get_height()
                                  + self.terrain.get_tile_increment().y
                                  )
                                 )
        # add the viewpoint offset
        position = Point(sprite_position.x + offset_position.x,
                         sprite_position.y + offset_position.y)
        self.display.blit(sprite, position)
        self.talking_head.update()
        self.basket.update()
        pygame.display.update()

        self.clock.tick()
        self.frame_counter += 1
        if self.frame_counter > 50:  # to avoid slowdown due to fps spam
            #print(self.clock.get_fps())
            self.frame_counter = 0
