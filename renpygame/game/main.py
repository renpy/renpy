#!/usr/bin/env python

import sys
import renpygame as pygame
import math
from renpygame.locals import *

import players
import images
import levels
import constants

screen = None
game_area = None

def init_pygame():
    global screen, game_area

    pygame.init()
    screen = pygame.display.set_mode(constants.screen_size)
    pygame.display.set_caption('Blastwave')
    game_area = pygame.Surface(constants.game_size)

def init():
    init_pygame()
    images.init()
    levels.init()
    players.init()

def main():
    init()

    global frame
    clock = pygame.time.Clock()
    while 1:
        handle_events()
        run_engine()
        draw_world()
        clock.tick(60)
        if levels.current.frame % 10 == 0:
            pygame.display.set_caption("Blastwave // %ifps" % (clock.get_fps(), ))

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                players.current.up = True
            elif event.key == K_DOWN:
                players.current.down = True
            elif event.key == K_LEFT:
                players.current.left = True
            elif event.key == K_RIGHT:
                players.current.right = True
            elif event.key == K_LSHIFT:
                players.current.slow = True
            elif event.key == K_z:
                players.current.firing = True
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                sys.exit()
            elif event.key == K_a:
                players.current.next_payload()
            elif event.key == K_UP:
                players.current.up = False
            elif event.key == K_DOWN:
                players.current.down = False
            elif event.key == K_LEFT:
                players.current.left = False
            elif event.key == K_RIGHT:
                players.current.right = False
            elif event.key == K_LSHIFT:
                players.current.slow = False
            elif event.key == K_z:
                players.current.firing = False

def run_engine():
    levels.current.update()

def draw_world():
    screen.blit(images.background, [0, 0, 640, 480])

    game_area.blit(levels.current.bgimg2, pygame.Rect(0, -480 + (levels.current.frame * 1) % 480, 400, 460))
    game_area.blit(levels.current.bgimg1, pygame.Rect(0,    0 + (levels.current.frame * 1) % 480, 400, 460))

    levels.current.draw(game_area)

    font = pygame.font.Font(None, 36)
    text = font.render("Score: %i" % (players.current.score, ), 1, (210, 210, 210))
    textpos = text.get_rect()
    textpos.midleft = 440, 40
    screen.blit(text, textpos)

    text = font.render("Power: %i" % (players.current.power, ), 1, (210, 210, 210))
    textpos = text.get_rect()
    textpos.midleft = 440, 80
    screen.blit(text, textpos)

    screen.blit(game_area, [10, 10, 400, 480])

    pygame.display.flip()

if __name__ == "__main__":
    main()

