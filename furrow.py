import string
from point import Point


class GrowingPlot:
    """ a growing plot is the patch of ground that can contain a single plant.
    On the terrain, one tile = one plot. The plot tracks the status of the
    plant growing on it, plus the amount of moisture, fertiliser, bugs etc """
    def __init__(self, coords: Point):
        self.water = 0
        self.coords = coords

class Furrow(list):
    """ A furrow is a list of growing plots. Actions that modify the furrow,
     or the plots within it, should be reflected in some way on the screen.
     In particular, Farmer Bob, should move to the list elements being accessed
     or modified. """

    def __init__(self, name: string, start: Point, end: Point):
        self.name = name
        # create a set of all tile coords in the furrow
        self.tiles_coords = set()
        for i in range(start.x, end.x+1):
            for j in range(start.y, end.y+1):
                self.append(GrowingPlot(Point(i, j)))
                self.tiles_coords.add(GrowingPlot(Point(i, j)))
