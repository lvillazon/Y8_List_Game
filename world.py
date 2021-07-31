import random
from collections import namedtuple

import pygame
from pygame import time

import isometric_spritesheet
from config import BLOCK_SIZE, SKY_BLUE
from console_messages import console_msg
from terrain import Terrain

Point = namedtuple('Point', ['x', 'y'])

class World:
    def __init__(self, screen):
        console_msg('Initialising world', 0)
        self.display = screen
        self.terrain = Terrain(screen, 15, 10)
        self.viewpoint = Point(screen.get_width() // 2,
                               screen.get_height() // 2)
        self.old_viewpoint = Point(0,0)
        self.drag_start = Point(0,0)
        self.running = True

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

        if pygame.mouse.get_pressed()[0]:  # LMB held down
            drag_x = self.drag_start.x - pygame.mouse.get_pos()[0]
            drag_y = self.drag_start.y - pygame.mouse.get_pos()[1]
            self.viewpoint = Point(self.old_viewpoint.x - drag_x,
                                   self.old_viewpoint.y - drag_y)

        # render all onscreen objects
        self.display.fill(SKY_BLUE)
        self.terrain.update(self.viewpoint)
        pygame.display.update()
