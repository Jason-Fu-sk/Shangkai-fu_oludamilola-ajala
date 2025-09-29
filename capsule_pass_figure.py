#import the library
import math
import pandas as pd
import csv as csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon

RADIUS = 5#The radius length of the fixed circle

#Create a capsule graphic
def capsule(ax,x_initial,y_initial,x_end,y_end):
    circle_kwargs = dict(edgecolor='crimson', lw=2, fill=False)
    line_kwargs = dict(color='crimson', lw=2)
    rect_kwargs = dict(edgecolor='royalblue', lw=2, fill=False)
    ax.add_patch(Circle((x_initial, y_initial), RADIUS, **circle_kwargs))
    ax.add_patch(Circle((x_end, y_end), RADIUS, **circle_kwargs))

    # The straight-line distance between two players = A line
    ax.plot([x_initial, x_end], [y_initial, y_end], **line_kwargs)

    # Creat a vector represents the horizontal and vertical components
    vx, vy = (x_end - x_initial, y_end - y_initial)
    L = math.hypot(vx, vy)#returns the length of a two-dimensional vector

    # The unit vector n perpendicular to A (obtained by rotating (vx,vy) by +90° and normalizing it)
    nx, ny = (-vy / L, vx / L)

    # The endpoints of the perpendicular diameters on the two circles about players
    p1_top = (x_initial + nx * RADIUS, y_initial + ny * RADIUS)
    p1_bot = (x_initial - nx * RADIUS, y_initial - ny * RADIUS)
    p2_top = (x_end + nx * RADIUS, y_end + ny * RADIUS)
    p2_bot = (x_end - nx * RADIUS, y_end - ny * RADIUS)

    # Create a rectangle
    corners = [p1_top, p2_top, p2_bot, p1_bot]
    ax.add_patch(Polygon(corners, **rect_kwargs))
    return corners

#Check whether other players are inside the capsule
def point_in_circle(x,y, center, inclusive=True):
    """Determine whether the point is inside or on the edge of the circle"""
    cx, cy = center
    d2 = (x - cx)**2 + (y - cy)**2
    r2 = RADIUS**2
    return d2 <= r2 if inclusive else d2 < r2

def polygon_contains_point( x, y, poly, inclusive=True):
    """Determine whether the point is within the capsule poly."""
    sign = None
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        ex, ey = (x2 - x1), (y2 - y1)
        px, py = (x - x1), (y - y1)
        cross = ex * py - ey * px
        if cross == 0:
            if inclusive:
                continue
            else:
                return False
        current = 1 if cross > 0 else -1
        if sign is None:
            sign = current
        elif current != sign:
            return False
    return True

def rectangle_from_two_circles(p1,p2, RADIUS):
    """It is constructed by two circles (with the same radius): The endpoints of the diameters passing through each circle's center and perpendicular to the common center line → Form the four corners of a rectangle"""
    x1, y1 = p1
    x2, y2 = p2
    vx, vy = (x2 - x1, y2 - y1)
    L = math.hypot(vx, vy)
    if L == 0:
        raise ValueError("p1 and p2 can not same")

    # The unit normal vector perpendicular to the connecting line (rotated by +90°)
    nx, ny = (-vy / L, vx / L)
    p1_top = (x1 + nx*RADIUS, y1 + ny*RADIUS)
    p1_bot = (x1 - nx*RADIUS, y1 - ny*RADIUS)
    p2_top = (x2 + nx*RADIUS, y2 + ny*RADIUS)
    p2_bot = (x2 - nx*RADIUS, y2 - ny*RADIUS)
    return [p1_top, p2_top, p2_bot, p1_bot]

def classify_points(points, p1, p2):
    """Determine whether each point is within: Circle 1, Circle 2, and Rectangle."""
    rect = rectangle_from_two_circles(p1, p2, RADIUS)
    results = []
    for pt in points:
        x,y = pt
        in_c1 = point_in_circle(x,y, p1, inclusive=True)
        in_c2 = point_in_circle(x,y, p2, inclusive=True)
        in_rect = polygon_contains_point(x,y, rect, inclusive=True)
        results.append(dict(point=pt, in_circle1=in_c1, in_circle2=in_c2, in_rect=in_rect))
    return rect, results
