
import renpygame as pygame
import levels
import constants
import math
import players

class Missile(pygame.sprite.Sprite):
    def __init__(self, image, pos, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.pos = pos
        self.speed = speed
        self.rect = image.get_rect()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.add(levels.current.enemy_missile_group)

    def tick(self):
        pass

    def update(self):
        self.tick()

        self.pos[0] = self.pos[0] + self.speed[0]
        self.pos[1] = self.pos[1] + self.speed[1]
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

        if self.rect.right < -100 or self.rect.left > constants.game_width + 100 or \
           self.rect.bottom < -100 or self.rect.top > constants.game_height + 100:
            self.kill()

class GravMissile(Missile):
    def __init__(self, image, pos, speed):
        Missile.__init__(self, image, pos, speed)
        self.startframe = levels.current.frame

    def tick(self):
        if (levels.current.frame + self.startframe) % 10 == 0:
            self.speed[1] = self.speed[1] + 1

class AngledMissile(Missile):
    def __init__(self, image, pos, speed, angle):
        speed = [math.sin(angle)*speed, math.cos(angle)*speed]
        Missile.__init__(self, image, pos, speed)

class AimedMissile(AngledMissile):
    def __init__(self, image, pos, speed, mod):
        p1 = pos
        p2 = players.current.pos
        angle = math.atan((p2[0] - p1[0]) / (p2[1] - p1[1])) + mod
        AngledMissile.__init__(self, image, pos, speed, angle)

class DelayedAimedMissile(AngledMissile):
    def __init__(self, image, pos, speed, mod):
        AngledMissile.__init__(self, image, pos, speed, mod)
        self.startframe = levels.current.frame

    def tick(self):
        if levels.current.frame - self.startframe == 50:
            p1 = self.pos
            p2 = players.current.pos
            angle = math.atan((p2[0] - p1[0]) / (p2[1] - p1[1]))
            sp = math.sqrt(self.speed[0]*self.speed[0] + self.speed[1]*self.speed[1])
            self.speed = [math.sin(angle)*sp, math.cos(angle)*sp]

class Bullet(Missile):
    def __init__(self, image, pos, speed):
        Missile.__init__(self, image, pos, speed)
        self.remove(levels.current.enemy_missile_group)
        self.add(levels.current.player_missile_group)

