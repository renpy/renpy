
import missiles
import images
import math
import levels

class Payload:
    def __init__(self):
        self.power = 0

    def tick(self, pos):
        pass

class DualGravPayload(Payload):
    def tick(self, pos, frame):
        if frame % 100 > 75 and frame % 100 < 100 and frame % 5 == 0:
            missiles.GravMissile(images.missile3, [pos[0], pos[1]], [-2.0, 0.0])
            missiles.GravMissile(images.missile3, [pos[0], pos[1]], [ 2.0, 0.0])

class CircleShotPayload(Payload):
    def tick(self, pos, frame):
        if frame % 100 == 0 or frame % 100 == 10 or frame % 100 == 20:
            density = 24
            for n in range(0, density):
                missiles.AngledMissile(images.missile1, [pos[0], pos[1]], 2, math.pi*2/density*n)

class GuidedCircleShotPayload(Payload):
    def tick(self, pos, frame):
        if frame % 100 == 0:
            density = 24
            for n in range(0, density):
                missiles.DelayedAimedMissile(images.missile1, [pos[0], pos[1]], 2, math.pi*2/density*n)

class ShotgunPayload(Payload):
    def tick(self, pos, frame):
        if frame % 66 == 0:
            missiles.AimedMissile(images.missile1, [pos[0], pos[1]], 2, -0.1)
            missiles.AimedMissile(images.missile1, [pos[0], pos[1]], 2,  0.0)
            missiles.AimedMissile(images.missile1, [pos[0], pos[1]], 2, +0.1)
            missiles.AimedMissile(images.missile1, [pos[0], pos[1]], 3, -0.1)
            missiles.AimedMissile(images.missile1, [pos[0], pos[1]], 3,  0.0)
            missiles.AimedMissile(images.missile1, [pos[0], pos[1]], 3, +0.1)
            missiles.AimedMissile(images.missile1, [pos[0], pos[1]], 4, -0.1)
            missiles.AimedMissile(images.missile1, [pos[0], pos[1]], 4,  0.0)
            missiles.AimedMissile(images.missile1, [pos[0], pos[1]], 4, +0.1)



class Laser(Payload):
    def __init__(self):
        self.power = 0

    def tick(self, pos):
        if levels.current.frame % 5 == 0:
            missiles.Bullet(images.bullet, [pos[0], pos[1]], [0, -5])

class DualLaser(Payload):
    def __init__(self):
        self.power = 1

    def tick(self, pos):
        if levels.current.frame % 5 == 0:
            missiles.Bullet(images.bullet, [pos[0]-6, pos[1]], [0, -5])
            missiles.Bullet(images.bullet, [pos[0]+6, pos[1]], [0, -5])

