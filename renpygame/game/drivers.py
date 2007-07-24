
class Driver:
    def __init__(self, pos):
        self.pos = pos

    def tick(self):
        pass

class StraightDriver(Driver):
    def __init__(self, pos, speed):
        self.pos = pos
        self.speed = speed

    def tick(self):
        self.pos[0] = self.pos[0] + self.speed[0]
        self.pos[1] = self.pos[1] + self.speed[1]
