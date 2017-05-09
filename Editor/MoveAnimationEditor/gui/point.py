import numpy as np
from numpy import sin, cos


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        if type(item) != int:
            raise IndexError("Index not an int")
        if item < 0 or item > 1:
            raise IndexError("Index out of range")
        if item == 0:
            return self.x
        else:
            return self.y

    def __sub__(self, other):
        return Point(self.x - other[0], self.y - other[1])

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def as_tuple(self):
        return self.x, self.y

    def set(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)

    def distance_to(self, point):
        return ((self.x - point[0])**2 + (self.y - point[1])**2)**.5

    def midpoint(self, point):
        return Point(self.x + (point[0]-self.x)/2, self.y + (point[1]-self.y)/2)

    def rotate(self, about, angle):
        cx = about[0]
        cy = about[1]
        a = np.deg2rad(angle)
        rot = np.matrix([[cos(a), -sin(a), cx*(1-cos(a)) + cy*sin(a)],
                         [sin(a),  cos(a), cy*(1-cos(a)) - cx*sin(a)],
                         [0,       0,      1]])
        coord = np.matrix([[self.x], [self.y], [1]])
        res = rot * coord
        self.x = float(res[0])
        self.y = float(res[1])