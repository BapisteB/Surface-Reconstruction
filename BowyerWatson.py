import pygame
from random import randint
from Triangle import Triangle
from Delaunay import Delaunay

def edgeNotShared(edge, triangles, tr):
    for triangle in triangles:
        if triangle == tr:
            continue
        edges = [(triangle.p1, triangle.p2), (triangle.p1, triangle.p3), (triangle.p2, triangle.p3)]
        if edge in edges or (edge[1], edge[0]) in edges:
            return False
    return True

class BowyerWatson(Delaunay):

    def __init__(self, nbPoints, screen):
        super().__init__(nbPoints, screen)

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
            for badT in badTriangle:
                edges = [(badT.p1, badT.p2),
                         (badT.p1, badT.p3),
                         (badT.p2, badT.p3)]
                for edge in edges:
                    if edgeNotShared(edge, badTriangle, badT):
                        polygon.append(edge)

            res = triangulation[::]
            for triangle in badTriangle:
                for tr in triangulation:
                    if tr == triangle:
                        res.remove(tr)
            triangulation = res

            for edge in polygon:
                triangulation.append(Triangle(pt, edge[1], edge[0]))

        res = triangulation[::]
        for tr in triangulation:
            if (tr.p1 == sup.p1 or tr.p1 == sup.p2 or tr.p1 == sup.p3
                    or tr.p2 == sup.p1 or tr.p2 == sup.p2 or tr.p2 == sup.p3
                    or tr.p3 == sup.p1 or tr.p3 == sup.p2 or tr.p3 == sup.p3):
                res.remove(tr)

        self.triangulation = res
