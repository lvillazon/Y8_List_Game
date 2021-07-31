# handles the relative viewpoint offset,
# rotation and zoom for the terrain
import pygame


class Camera:
    def __init__(self):
        self._offset = [0, 0]
        self._rotation = 0
        self._zoom = 1.0

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    @property
    def x(self):
        return self._offset[0]

    @x.setter
    def x(self, value):
        self._offset[0] = value

    @property
    def y(self):
        return self._offset[1]

    @y.setter
    def y(self, value):
        self._offset[1] = value

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

