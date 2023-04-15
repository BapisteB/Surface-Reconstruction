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

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screen.fill("black")
                m = BowyerWatson(pt_nb, screen)
                m.display()
                triangulation = m.BowyerWatson(1920, 1080)
                for triangle in triangulation:
                    triangle.display(screen)

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
