import pygame
from random import randint

class Delaunay:

    def __init__(self, screen, nbPoints = -1, pointSet = []):
        self.screen = screen
        if nbPoints == -1:
            self.points = pointSet
        else:
            self.points = [pygame.Vector2(randint(0, screen.get_width()), randint(0, screen.get_height())) for i in range(nbPoints)]
        self.triangulation = []
        self.tesselation = []
        self.tesspoints = []

    def draw(self, color = "red"):
        for pt in self.points:
            if pt.x >= 0 and pt.y >= 0:
                pygame.draw.circle(self.screen, color, pt, 5)

    def drawDelaunay(self, color = "blue"):
        for t in self.triangulation:
            t.draw(self.screen)

    def drawVoronoi(self, color = "yellow"):
        for i, j in self.tesselation:
            pygame.draw.line(self.screen, color, i, j)

    def Voronoi(self):
        for i in range(len(self.triangulation)):
            t = self.triangulation[i]
            if t.circ is None:
                x, y, _ = t.getCircumscribed()
                t.circ = pygame.Vector2(x, y)
                self.tesspoints.append(t.circ)
            edges = [(t.p1, t.p2, False),
                     (t.p1, t.p3, False),
                     (t.p2, t.p3, False)]
            added = 0
            for j in range(i + 1, len(self.triangulation)):
                adj = self.triangulation[j]
                edges_ = [(adj.p1, adj.p2),
                      (adj.p1, adj.p3),
                      (adj.p2, adj.p3)]
                for i in range(3):
                    edge = edges[i]
                    if (edge[0], edge[1]) in edges_ or (edge[1], edge[0]) in edges_:
                        edges[i] = (edge[0], edge[1], True)
                        if adj.circ is None:
                            x, y, _ = adj.getCircumscribed()
                            adj.circ = pygame.Vector2(x, y)
                        added += 1
                        self.tesselation.append((t.circ, adj.circ))
                        self.tesspoints.append(adj.circ)
                if added == 3:
                    break

            # Useless for the crust algorithm
            # if added != 3:
                # for p1, p2, b in edges:
                    # if not b:
                        # # Point between p1 and p2
                        # midp = pygame.Vector2((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
                        # # TODO: Find closest between half-line
                        # self.tesselation.append((t.circ, midp))
