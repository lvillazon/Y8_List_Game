from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

def add_points(a: Point, b: Point) -> Point:
    # simple addition of the x and y coords
    return Point(a.x + b.x, a.y + b.y)