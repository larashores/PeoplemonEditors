import numpy as np
from math import cos, sin


def rotation(x, y, center, angle):
    cx = center[0]
    cy = center[1]
    a = np.deg2rad(angle)
    rot = np.matrix([[cos(a), -sin(a), cx*(1-cos(a)) + cy*sin(a)],
                     [sin(a),  cos(a), cy*(1-cos(a)) - cx*sin(a)],
                     [0,       0,      1]])
    coord = np.matrix([[x], [y], [1]])

    res = rot * coord
    return float(res[0]), float(res[1])
