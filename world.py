import random
import pygame
from pygame import time
from math import copysign

import isometric_spritesheet
from config import BLOCK_SIZE, SKY_BLUE, Point
from console_messages import console_msg
from terrain import Terrain



class World:
    def __init__(self, screen):
        console_msg('Initialising world', 0)
        self.display = screen
        self.zoom = 0.25
        self.terrain = Terrain(screen, 20, 15, self.zoom)
        self.viewpoint = Point(screen.get_width() // 2,
                               screen.get_height() // 2)
        self.old_viewpoint = Point(0,0)
        self.drag_start = Point(0,0)
        self.running = True
        self.frame_counter = 0
        self.clock = pygame.time.Clock()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # left button
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
                #print(self.zoom, min(1, int(4 * self.zoom)))

        if pygame.mouse.get_pressed()[0]:  # LMB held down
            drag_x = self.drag_start.x - pygame.mouse.get_pos()[0]
            drag_y = self.drag_start.y - pygame.mouse.get_pos()[1]
            self.viewpoint = Point(self.old_viewpoint.x + drag_x,
                                   self.old_viewpoint.y + drag_y)

        # render all onscreen objects
        self.display.fill(SKY_BLUE)
        self.terrain.update(self.viewpoint)
        pygame.display.update()
        self.clock.tick()
        self.frame_counter += 1
        if self.frame_counter > 50:  # to avoid slowdown due to fps spam
            #print(self.clock.get_fps())
            self.frame_counter = 0

