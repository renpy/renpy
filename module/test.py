import pygame
import _renpy
import time

pygame.init()

screen = pygame.display.set_mode((800, 600), 0, 32)

s = pygame.image.load("../game/washington.jpg")
# s = s.convert_alpha()
s2 = pygame.Surface(s.get_size(), 0, s)


px = 2

for r in range(10):

    for px in range(1, 10) + range(10, 0, -1):
        start = time.time()
        px = 2 ** px

        for i in range(1):
            _renpy.pixellate(s, s2, px, px, px, px)

        print px, ( time.time() - start ) / 1.0

        screen.blit(s2, (0, 0))
        pygame.display.flip()

        time.sleep(.05)

while True:

    if pygame.event.wait().type == pygame.constants.QUIT:
        break
