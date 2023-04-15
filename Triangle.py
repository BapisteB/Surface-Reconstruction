import pygame
from numpy import sqrt

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def draw(self, screen, color = "blue"):
        pygame.draw.line(screen, color, self.p1, self.p2)
        pygame.draw.line(screen, color, self.p1, self.p3)
        pygame.draw.line(screen, color, self.p2, self.p3)

    def __eq__(self, t):
        return ((t.p1 == self.p1 and t.p2 == self.p2 and t.p3 == self.p3)
        or (t.p1 == self.p2 and t.p2 == self.p3 and t.p3 == self.p1)
        or (t.p1 == self.p3 and t.p2 == self.p1 and t.p3 == self.p2)

        or (t.p2 == self.p1 and t.p3 == self.p2 and t.p1 == self.p3)
        or (t.p2 == self.p2 and t.p3 == self.p3 and t.p1 == self.p1)
        or (t.p2 == self.p3 and t.p3 == self.p1 and t.p1 == self.p2)

        or (t.p3 == self.p1 and t.p1 == self.p2 and t.p2 == self.p3)
        or (t.p3 == self.p2 and t.p1 == self.p3 and t.p2 == self.p1)
        or (t.p3 == self.p3 and t.p1 == self.p1 and t.p2 == self.p2))

    def circumscribed(self, point):
        ax = self.p1.x
        ay = self.p1.y
        bx = self.p2.x
        by = self.p2.y
        cx = self.p3.x
        cy = self.p3.y

        # compute the center coordinates
        d = 2 * (ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
        if (d == 0):
            return False
        ad = ax*ax + ay*ay
        bd = bx*bx + by*by
        cd = cx*cx + cy*cy
        x = (ad*(by-cy) + bd*(cy-ay) + cd*(ay-by))/d
        y = (ad*(cx-bx) + bd*(ax-cx) + cd*(bx-ax))/d

        # compute the radius
        dx = x - ax
        dy = y - ay
        r = sqrt(dx ** 2 + dy ** 2)

        #pygame.draw.circle(screen, "red", pygame.Vector2(x, y), r, width=1)
        if (point.x - x) ** 2 + (point.y - y) ** 2 <= r ** 2:
            #pygame.draw.circle(screen, "green", pygame.Vector2(x, y), r, width=1)
            return True
        return False
