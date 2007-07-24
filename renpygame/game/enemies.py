
import renpygame as pygame
import constants
import levels
import players

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, driver, payload):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.driver = driver
        self.payload = payload
        self.rect = image.get_rect().move(driver.pos)
        self.startframe = levels.current.frame
        self.add(levels.current.enemy_group)
        self.power = 10
        self.max_power = 10

    def update(self):
        self.driver.tick()
        self.payload.tick(self.driver.pos, levels.current.frame - self.startframe)
        self.rect.center = self.driver.pos

        if self.rect.right < 0 or self.rect.left > constants.game_width or \
           self.rect.bottom < 0 or self.rect.top > constants.game_height:
            self.really_kill()

    def kill(self):
        self.power = self.power - 1
        if self.power <= 0:
            self.really_kill()
            players.current.score = players.current.score + self.max_power

    def really_kill(self):
        pygame.sprite.Sprite.kill(self)

