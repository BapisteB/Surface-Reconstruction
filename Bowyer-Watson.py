# Example file showing a circle moving on screen
import pygame
from time import sleep
import numpy as np
from random import randint

class Mesh:
    def __init__(self, nbPoints, screen):
        self.screen = screen
        self.points = [pygame.Vector2(randint(0, screen.get_width()), randint(0, screen.get_height())) for i in range(nbPoints)]
        #self.points = [pygame.Vector2(randint(0, 500), randint(0, 500)) for i in range(nbPoints)]

    def display(self):
        for pt in self.points:
            pygame.draw.circle(screen, "red", pt, 10)

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        # if (p2.x - p1.x)*(p3.y - p1.y)-(p3.x - p1.x)*(p2.y - p1.y) > 0:
            # self.p3 = p2
            # self.p2 = p3

    def display(self, color = "blue"):
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

def computeSuperTriangle(w, h):
    # We compute f(x) = ax + b with f(w) = h
    # Brute force for now
    # Other solution would be to find the triangle using inscribed circle with r = diag(rectangle)
    b = 2 * w
    a = (w - b) / h
    return Triangle(pygame.Vector2(0, 0), pygame.Vector2(b, 0), pygame.Vector2(0, (-b) / a))

def circumscribed(triangle, point):
    ax = triangle.p1.x
    ay = triangle.p1.y
    bx = triangle.p2.x
    by = triangle.p2.y
    cx = triangle.p3.x
    cy = triangle.p3.y

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
    r = np.sqrt(dx ** 2 + dy ** 2)

    #pygame.draw.circle(screen, "red", pygame.Vector2(x, y), r, width=1)
    if (point.x - x) ** 2 + (point.y - y) ** 2 <= r ** 2:
        #pygame.draw.circle(screen, "green", pygame.Vector2(x, y), r, width=1)
        return True
    return False


def edgeNotShared(tr, edge, triangles):
    for triangle in triangles:
        if tr == triangle:
            continue
        edges = [(triangle.p1, triangle.p2), (triangle.p1, triangle.p3), (triangle.p2, triangle.p3)]
        for e in edges:
            if e == edge or (e[1], e[0]) == edge:
                return False
    return True


def BowyerWatson(mesh, w, h):
    sup = computeSuperTriangle(w, h)
    triangulation = [sup]
    for pt in mesh.points:
        badTriangle = []
        for triangle in triangulation:
            if circumscribed(triangle, pt):
                pygame.draw.circle(screen, "purple", pt, 10)
                badTriangle.append(triangle)
        polygon = []
        # This double for can be optimised :)
        for triangle in badTriangle:
            edges = [(triangle.p1, triangle.p2), (triangle.p1, triangle.p3), (triangle.p2, triangle.p3)]
            for edge in edges:
                if edgeNotShared(triangle, edge, badTriangle):
                    #print("shared", edge)
                    polygon.append(edge)

        res = triangulation[:]
        for triangle in badTriangle:
            for tr in triangulation:
                if tr == triangle:
                    #tr.display("grey")
                    res.remove(tr)
        triangulation = res

        for edge in polygon:
            t = Triangle(pt, edge[1], edge[0])
            #t.display("yellow")
            triangulation.append(t)

    res = triangulation[:]
    for tr in triangulation:
        if (tr.p1 == sup.p1 or tr.p1 == sup.p2 or tr.p1 == sup.p3
                or tr.p2 == sup.p1 or tr.p2 == sup.p2 or tr.p2 == sup.p3
                or tr.p3 == sup.p1 or tr.p3 == sup.p2 or tr.p3 == sup.p3):
            res.remove(tr)

    return res


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True

# Setup display
screen.fill("black")
pt_nb = 100

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screen.fill("black")
                m = Mesh(pt_nb, screen)
                m.display()
                triangulation = BowyerWatson(m, 1920, 1080)
                for triangle in triangulation:
                    triangle.display()

            if event.key == pygame.K_UP:
                pt_nb += 1

            if event.key == pygame.K_DOWN:
                pt_nb += 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
