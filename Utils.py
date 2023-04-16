import pygame

def dichotomia(L, X):
    i = 0
    j = len(L) - 1
    m = (i + j) // 2
    while i < j :
        if L[m] == X:
            return m
        elif L[m] > X:
            j = m - 1
        else :
            i = m + 1
        m = (i + j) // 2
    return i

# Hash function as defined here https://stackoverflow.com/questions/919612/mapping-two-integers-to-one-in-a-unique-and-deterministic-way
def hash(p : pygame.Vector2):
    return int(p.x * p.x + p.x + p.y if p.x >= p.y else p.x + p.y * p.y)
