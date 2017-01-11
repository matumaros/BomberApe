

class Entity:
    def __init__(self, uid, controller, pos, skin, size=(1, 1), speed=1):
        self.uid = uid
        self.controller = controller
        self.pos = pos
        self.skin = skin
        self.size = size
        self.speed = speed

    def move(self, x, y):
        self.pos = self.pos[0] + x, self.pos[1] + y
