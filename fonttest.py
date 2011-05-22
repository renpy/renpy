import pygame
import ftfont

pygame.font.init()
pygame.display.init()

ftfont.init()

f = file("common/DejaVuSans.ttf", "rb")
font = ftfont.FTFont(f, 0)


screen = pygame.display.set_mode((640, 480))
s = pygame.Surface((640, 480))
s = s.convert_alpha()

for kern in range(0, 11):

    font.setup(24, False, False, 0)
    glyphs = font.glyphs(u"Using additional kerning of -{:.1f} px/char.".format(kern / 10.0))
    
    for i in glyphs:
        i.advance -= (kern / 10.0)

    font.draw(s, 0, kern * font.lineskip + font.ascent, glyphs)
    
screen.blit(s, (0, 0))
pygame.image.save(screen, '/tmp/kerning.png')

pygame.display.flip()



while True:
    ev = pygame.event.wait()
    
    if ev.type in [ pygame.MOUSEBUTTONDOWN, pygame.QUIT, pygame.KEYDOWN ]:
        break
    
