import renpygame as pygame
import payloads
import images
import levels
import constants

current = None

def init():
    global current
    current = Player([constants.game_width/2, constants.game_height-20], [0.0, 0.0])

class GrazeZone(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.image = images.invisible
        self.rect = player.rect
        self.rect.width = 4
        self.rect.height = 4
        self.rect.center = player.rect.center
        self.add(levels.current.player_group)

    def update(self):
        self.rect.center = self.player.rect.center

    def kill(self):
        self.player.power = self.player.power + 1

    def really_kill(self):
        pygame.sprite.Sprite.kill(self)

class KillZone(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.image = images.invisible
        self.rect = player.rect.inflate(-12, -12)
        self.add(levels.current.player_group)

    def update(self):
        self.rect.center = self.player.rect.center

    def kill(self):
        self.player.power = self.player.power - 100
        if self.player.power < 0:
            self.player.really_kill()

    def really_kill(self):
        pygame.sprite.Sprite.kill(self)

    
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        pygame.sprite.Sprite.__init__(self)

        self.ship = pygame.image.load(constants.datadir + "ship.png")
        self.ship_left = pygame.image.load(constants.datadir + "ship_left.png")
        self.ship_right = pygame.image.load(constants.datadir + "ship_right.png")

        self.image = self.ship
        self.pos = pos
        self.speed = speed
        self.firing = False
        self.payloads = [payloads.Laser(), payloads.DualLaser()]
        self.payload_id = 0
        self.rect = self.image.get_rect().move(pos)

        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.slow = False

        self.power = 100
        self.score = 0

        self.add(levels.current.player_group)
        self.grazezone = GrazeZone(self)
        self.killzone = KillZone(self)

    def __do_movement(self):
        if self.slow:
            speed = 1
        else:
            speed = 3

        if self.left:    self.speed[0] = -speed
        elif self.right: self.speed[0] = speed
        else:            self.speed[0] = 0

        if self.up:     self.speed[1] = -speed
        elif self.down: self.speed[1] = speed
        else:           self.speed[1] = 0

        self.pos[0] = self.pos[0] + self.speed[0]
        self.pos[1] = self.pos[1] + self.speed[1]
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

        if self.rect.left < 0 or self.rect.right > constants.game_width:
            self.speed[0] = 0
        if self.rect.top < 0 or self.rect.bottom > constants.game_height:
            self.speed[1] = 0

    def __do_firing(self):
        if self.firing:
            payload = self.payloads[self.payload_id]
            if payload.power > self.power:
                self.payload_id = 0
                payload = self.payloads[0]
            self.power = self.power - payload.power
            payload.tick(self.pos)

    def __do_image(self):
        if self.speed[0] < 0:
            self.image = self.ship_left
        elif self.speed[0] > 0:
            self.image = self.ship_right
        else:
            self.image = self.ship

    def update(self):
        self.__do_movement()
        self.__do_firing()
        self.__do_image()

    def next_payload(self):
        self.payload_id = self.payload_id + 1
        if self.payload_id > len(self.payloads)-1:
            self.payload_id = 0
        if self.payload_id < 0:
            self.payload_id = len(self.payloads)-1

    def kill(self):
        pass

    def really_kill(self):
        pygame.sprite.Sprite.kill(self)
        self.grazezone.really_kill()
        self.killzone.really_kill()

