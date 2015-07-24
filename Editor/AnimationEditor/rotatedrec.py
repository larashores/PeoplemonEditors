__author__ = 'Vincent'

from math import cos, sin, pi

def rotatedRectangle(coord, width, height, rotation):
    """
    Purpose:    Calculated bounding box of a rotated rectangle from center
    Inputs:
        coords: (x,y) pair of cooridnates where the top left of the rectangle is located on a grid
        width:  width of the rectangle
        height: height of the rectangle
        rotation: Degrees to be rotatated by
    Output:
    """
    # Find four points
    rotation = -rotation
    x, y = coord
    center = (x+(width/2)), (y+(height/2))


    p1 = -(width/2), -(height/2)
    p2 = (width/2), -(height/2)
    p3 = -(width/2), (height/2)
    p4 = (width/2), (height/2)


    x_values = []
    y_values = []
    for p in (p1, p2, p3, p4):
        x, y = rotatedVector(p, rotation*(pi/180))
        x_values.append(x)
        y_values.append(y)

    min_coord = min(x_values), min(y_values)
    max_coord = max(x_values), max(y_values)

    new_coord = min_coord[0]+center[0], min_coord[1]+center[1]
    width = max_coord[0]-min_coord[0]
    height = max_coord[1]-min_coord[1]
    return new_coord, width, height


def rotatedVector(coord, rotation):
    x, y = coord
    r = rotation
    x1 = (x*cos(r)) + (y*sin(r))
    y1 = (-x*sin(r)) + (y*cos(r))
    return x1, y1
