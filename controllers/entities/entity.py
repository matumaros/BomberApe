

class Entity:
    type = None

    def __init__(self, uid, pos, size=(1, 1), speed=.1):
        self.uid = uid
        self.pos = pos
        self.size = size
        self.speed = speed

    def move(self, x, y):
        self.pos = self.pos[0] + x, self.pos[1] + y
