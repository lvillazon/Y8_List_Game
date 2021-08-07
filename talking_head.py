import pygame

import spritesheet
from panel import Panel


class TalkingHead(Panel):
    def __init__(self, display, position, size):
        super().__init__(display, position, size)
        # load all head images from the spritesheet
        head_sprites = spritesheet.SpriteSheet(
             "assets\\farmer_bear_heads.png", 2, 2, 0.37)
        self.head_palette = head_sprites.sprites[0]
        self.head_palette.extend(head_sprites.sprites[1])
        self._selected_head_number = 0
        self.draw_head(self._selected_head_number)

    def draw_head(self, head_number):
        self.redraw()
        self._panel.blit(self.head_palette[head_number],
                         (self.border_width, self.border_width))

    def update(self):
        super().update()

    def cycle_head(self):
        # TEST cycle through each of the heads in turn
        self._selected_head_number = (self._selected_head_number + 1) \
                                      % len(self.head_palette)
        self.draw_head(self._selected_head_number)
