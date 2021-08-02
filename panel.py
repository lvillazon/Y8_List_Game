import pygame
from config import *


class Panel:
    # UI element, overlaid on the game terrain view

    def __init__(self, display, position, size):
        self.display = display
        self.position = position
        self.size = size
        self._panel = pygame.Surface(size)
        self._panel.fill("red")  # for colour keying
        self._panel.set_colorkey("red")
        self.redraw()

    def redraw(self):
        border_width = 5
        # fill the middle
        pygame.draw.rect(self._panel, UI_BACKGROUND,
                         pygame.Rect(
                            border_width,
                            border_width,
                            self.size.x - border_width*2,
                            self.size.y - border_width*2
                         )
                        )
        pygame.draw.rect(self._panel, UI_FOREGROUND,
                         self._panel.get_rect(),
                         5,
                         10)

    def update(self):
        # draw the panel
        self.display.blit(self._panel, self.position)

    def mouse_over(self) -> bool:
        # return true if the mouse cursor is over the panel
        return self._panel.get_rect().collidepoint(pygame.mouse.get_pos())

