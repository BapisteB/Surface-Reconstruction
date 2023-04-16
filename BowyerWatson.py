import pygame
from random import randint
from Triangle import Triangle
from Delaunay import Delaunay
from Graph import Graph

def edgeNotShared(edge, triangles, tr):
    for triangle in triangles:
        if triangle == tr:
            continue
        edges = [(triangle.p1, triangle.p2),
                 (triangle.p1, triangle.p3),
                 (triangle.p2, triangle.p3)]
        if edge in edges or (edge[1], edge[0]) in edges:
            return False
    return True

class BowyerWatson(Delaunay):

    def __init__(self, screen, nbPoints = -1, pointSet = []):
        super().__init__(screen, nbPoints, pointSet)

    def computeSuperTriangle(self):
        # We compute f(x) = ax + b with f(w) = h
        # Brute force for now
        # Other solution would be to find the triangle using inscribed circle with r = diag(rectangle)
        w = self.screen.get_width()
        h = self.screen.get_height()
        b = 2 * w
        a = (w - b) / h
        return Triangle(pygame.Vector2(0, 0),
                        pygame.Vector2(b, 0),
                        pygame.Vector2(0, (-b) / a))

    def BowyerWatson(self):
        sup = self.computeSuperTriangle()
        self.triangulation = [sup]
        for pt in self.points:
            badTriangle = []
            for triangle in self.triangulation:
                if triangle.isInCircumscribed(pt):
                    badTriangle.append(triangle)

            polygon = []
            for badT in badTriangle:
                edges = [(badT.p1, badT.p2),
                         (badT.p1, badT.p3),
                         (badT.p2, badT.p3)]
                for edge in edges:
                    if edgeNotShared(edge, badTriangle, badT):
                        polygon.append(edge)

            for triangle in badTriangle:
                for tr in self.triangulation:
                    if tr == triangle:
                        self.triangulation.remove(tr)

            for edge in polygon:
                self.triangulation.append(Triangle(pt, edge[1], edge[0]))

        for tr in self.triangulation:
            if (tr.p1 == sup.p1 or tr.p1 == sup.p2 or tr.p1 == sup.p3
                    or tr.p2 == sup.p1 or tr.p2 == sup.p2 or tr.p2 == sup.p3
                    or tr.p3 == sup.p1 or tr.p3 == sup.p2 or tr.p3 == sup.p3):
                self.triangulation.remove(tr)

    def crust(self):
        self.draw()
        self.BowyerWatson()
        self.Voronoi()

        newDel = BowyerWatson(self.screen, pointSet = self.tesspoints + self.points)
        newDel.BowyerWatson()

        res = []

        for t in newDel.triangulation:
            if t.p1 in self.points and t.p2 in self.points:
                res.append((t.p1, t.p2))
            if t.p1 in self.points and t.p3 in self.points:
                res.append((t.p1, t.p3))
            if t.p2 in self.points and t.p3 in self.points:
                res.append((t.p2, t.p3))

        for p1, p2 in res:
            pygame.draw.line(self.screen, "green", p1, p2)
