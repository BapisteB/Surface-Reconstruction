import pygame
from random import randint

class Delaunay:

    def __init__(self, nbPoints, screen):
        self.screen = screen
        self.points = [pygame.Vector2(randint(0, screen.get_width()), randint(0, screen.get_height())) for i in range(nbPoints)]
        self.triangulation = []

    def draw(self, color = "red"):
        for pt in self.points:
            pygame.draw.circle(self.screen, color, pt, 5)

    def drawTriangulation(self, color = "blue"):
        for t in self.triangulation:
            t.draw(self.screen)

