import random

import pygame
from pygame import time

import isometric_spritesheet
from config import BLOCK_SIZE, SKY_BLUE
from console_messages import console_msg
from terrain import Terrain


class World:
    def __init__(self, screen):
        console_msg('Initialising world', 0)
        self.display = screen
        self.terrain = Terrain(30, 20)

    def update(self):
        self.display.fill(SKY_BLUE)
        self.terrain.update(self.display)
        pygame.display.update()
