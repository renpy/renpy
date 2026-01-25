import pygame

pygame.init()

surface = pygame.display.set_mode((640, 480))

while True:

    surface.fill((255, 0, 0, 255))
    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
