import pygame
from BowyerWatson import BowyerWatson

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True

# Setup display
screen.fill("black")
pt_nb = 100

pointSet = [(254, 262),
            (249, 304),
            (250, 357),
            (250, 406),
            (250, 479),
            (260, 542),
            (270, 623),
            (283, 705),
            (305, 786),
            (337, 834),
            (417, 856),
            (495, 847),
            (534, 796),
            (549, 719),
            (562, 657),
            (577, 592),
            (586, 541),
            (603, 482),
            (638, 452),
            (670, 464),
            (701, 504),
            (713, 577),
            (718, 668),
            (727, 742),
            (757, 835),
            (794, 860),
            (875, 869),
            (1003, 870),
            (1075, 859),
            (1189, 845),
            (1249, 833),
            (1295, 812),
            (1325, 725),
            (1341, 633),
            (1345, 558),
            (1338, 480),
            (1332, 415),
            (1322, 344),
            (1301, 267),
            (1278, 226),
            (1243, 199),
            (1182, 182),
            (1118, 174),
            (1052, 171),
            (979, 172),
            (887, 175),
            (757, 180),
            (713, 184),
            (652, 186),
            (591, 187),
            (541, 188),
            (482, 189),
            (418, 192),
            (368, 195),
            (305, 206),
            (276, 223)]

emptySet = []

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screen.fill("black")
                m = BowyerWatson(screen, nbPoints = pt_nb)
                m.crust()

            if event.key == pygame.K_1:
                screen.fill("black")
                inria = BowyerWatson(screen, pointSet = [pygame.Vector2(x, y) for x, y in pointSet])
                inria.crust()

            if event.key == pygame.K_0:
                screen.fill("black")
                inria = BowyerWatson(screen, pointSet = [pygame.Vector2(x, y) for x, y in emptySet])
                inria.crust()

            if event.key == pygame.K_RETURN:
                emptySet = []
                screen.fill("black")

        if event.type == pygame.MOUSEBUTTONDOWN:
            emptySet.append(event.pos)
            pygame.draw.circle(screen, "yellow", event.pos, 5)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
