import pygame
from random import randint
from Triangle import Triangle

def edgeNotShared(tr, edge, triangles):
    for triangle in triangles:
        if tr == triangle:
            continue
        edges = [(triangle.p1, triangle.p2), (triangle.p1, triangle.p3), (triangle.p2, triangle.p3)]
        for e in edges:
            if e == edge or (e[1], e[0]) == edge:
                return False
    return True

class BowyerWatson:
    def __init__(self, nbPoints, screen):
        self.screen = screen
        self.points = [pygame.Vector2(randint(0, screen.get_width()), randint(0, screen.get_height())) for i in range(nbPoints)]
        #self.points = [pygame.Vector2(randint(0, 500), randint(0, 500)) for i in range(nbPoints)]

    def display(self, color = "red"):
        for pt in self.points:
            pygame.draw.circle(self.screen, color, pt, 5)

    def computeSuperTriangle(self):
        # We compute f(x) = ax + b with f(w) = h
        # Brute force for now
        # Other solution would be to find the triangle using inscribed circle with r = diag(rectangle)
        w = self.screen.get_width()
        h = self.screen.get_height()
        b = 2 * w
        a = (w - b) / h
        return Triangle(pygame.Vector2(0, 0), pygame.Vector2(b, 0), pygame.Vector2(0, (-b) / a))

    def BowyerWatson(self, w, h):
        sup = self.computeSuperTriangle()
        triangulation = [sup]
        for pt in self.points:
            badTriangle = []
            for triangle in triangulation:
                if triangle.circumscribed(pt):
                    badTriangle.append(triangle)
            polygon = []
            # This double for can be optimised :)
            for triangle in badTriangle:
                edges = [(triangle.p1, triangle.p2), (triangle.p1, triangle.p3), (triangle.p2, triangle.p3)]
                for edge in edges:
                    if edgeNotShared(triangle, edge, badTriangle):
                        polygon.append(edge)

            res = triangulation[:]
            for triangle in badTriangle:
                for tr in triangulation:
                    if tr == triangle:
                        res.remove(tr)
            triangulation = res

            for edge in polygon:
                triangulation.append(Triangle(pt, edge[1], edge[0]))

        res = triangulation[:]
        for tr in triangulation:
            if (tr.p1 == sup.p1 or tr.p1 == sup.p2 or tr.p1 == sup.p3
                    or tr.p2 == sup.p1 or tr.p2 == sup.p2 or tr.p2 == sup.p3
                    or tr.p3 == sup.p1 or tr.p3 == sup.p2 or tr.p3 == sup.p3):
                res.remove(tr)

        return res

