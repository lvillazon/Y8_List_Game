import pygame

import spritesheet
from panel import Panel


class TalkingHead(Panel):
    def __init__(self, display, position, size):
        super().__init__(display, position, size)
        # load all head images from the spritesheet
        head_size = 600
        head_sprites = spritesheet.SpriteSheet(
             "assets\\farmer_bear_heads.png", head_size, 0.38)
        self.head_palette = []
        for row in range(head_sprites.get_rows()):
            for col in range(head_sprites.get_columns()):
                head_source = pygame.Rect(
                    col * head_size,
                    row * head_size,
                    head_size,
                    head_size
                )
                head = head_sprites.image_at(head_source, -1)
                self.head_palette.append(head)

        self._selected_head = 0
        self.draw_head(self._selected_head)

    def draw_head(self, head_number):
        self.redraw()
        self._panel.blit(self.head_palette[head_number], (10, -33))

    def update(self):
        super().update()

    def cycle_head(self):
        # TEST cycle through each of the heads in turn
        self._selected_head = (self._selected_head + 1) \
                              % len(self.head_palette)
        self.draw_head(self._selected_head)
