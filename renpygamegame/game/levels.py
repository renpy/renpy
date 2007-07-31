import renpygame as pygame
import random

import enemies
import images
import drivers
import payloads
import constants

current = None

def init():
    global current
    current = Level1()

class Level:
    def __init__(self):
        self.player_group = pygame.sprite.Group()
        self.player_missile_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_missile_group = pygame.sprite.Group()
        self.npc_group = pygame.sprite.Group()
        self.frame = 0

        self.bgimg1 = images.invisible
        self.bgimg2 = images.invisible

    def update(self):
        self.enemy_group.update()
        self.enemy_missile_group.update()
        self.player_group.update()
        self.player_missile_group.update()
        self.npc_group.update()

        pygame.sprite.groupcollide(self.enemy_group, self.player_missile_group, True, False)
        pygame.sprite.groupcollide(self.player_group, self.enemy_missile_group, True, False)

    def draw(self, screen):
        self.npc_group.draw(screen)
        self.enemy_group.draw(screen)
        self.player_group.draw(screen)
        self.player_missile_group.draw(screen)
        self.enemy_missile_group.draw(screen)

class Level1(Level):
    def __init__(self):
        Level.__init__(self)
        self.bgimage1 = pygame.image.load(constants.datadir + "background1.png").convert()
        self.bgimage1to2 = pygame.image.load(constants.datadir + "background1-2.png").convert()
        self.bgimage2 = pygame.image.load(constants.datadir + "background2.png").convert()
        self.bgimage2to3 = pygame.image.load(constants.datadir + "background2-3.png").convert()
        self.bgimage3 = pygame.image.load(constants.datadir + "background3.png").convert()

        self.img_enemy01 = pygame.image.load(constants.datadir + "enemy01.png")
        self.img_enemy02 = pygame.image.load(constants.datadir + "enemy02.png")
        self.img_enemy03 = pygame.image.load(constants.datadir + "enemy03.png")

    def update(self):
        Level.update(self)

        if self.frame == 0:
            enemies.Enemy(
                self.img_enemy03,
                drivers.StraightDriver([constants.game_width/2, 60.0], [0.0, 0.0]),
                payloads.GuidedCircleShotPayload())

        if self.frame % 400 == 0:
            enemies.Enemy(
                self.img_enemy01,
                drivers.StraightDriver([constants.game_width/4, 0.0], [3.0, 1.0]),
                payloads.DualGravPayload())
        if self.frame % 50 == 0:
            enemies.Enemy(
                self.img_enemy02,
                drivers.StraightDriver([float(random.randint(20, constants.game_width-20)), 0.0], [float(random.randint(-3, 3)), 1.0]),
                payloads.ShotgunPayload())
        if self.frame % 2000 == 200:
            enemies.Enemy(
                self.img_enemy03,
                drivers.StraightDriver([float(random.randint(20, constants.game_width-20)), 20.0], [0.0, 0.0]),
                payloads.CircleShotPayload())

        global bgimg1, bgimg2
        if self.frame == 0:
            self.bgimg2 = self.bgimage1
            self.bgimg1 = self.bgimage1

        if self.frame == 480:
            self.bgimg2 = self.bgimage1to2
            self.bgimg1 = self.bgimage1
        if self.frame == 480*2:
            self.bgimg2 = self.bgimage2
            self.bgimg1 = self.bgimage1to2
        if self.frame == 480*3:
            self.bgimg2 = self.bgimage2
            self.bgimg1 = self.bgimage2

        if self.frame == 480*5:
            self.bgimg2 = self.bgimage2to3
            self.bgimg1 = self.bgimage2
        if self.frame == 480*6:
            self.bgimg2 = self.bgimage3
            self.bgimg1 = self.bgimage2to3
        if self.frame == 480*7:
            self.bgimg2 = self.bgimage3
            self.bgimg1 = self.bgimage3

        if self.frame == 5000*10:
            sys.exit()

        self.frame = self.frame + 1

