

class Player:
    def __init__(self, uid, server):
        self.uid = uid
        self.server = server
        self.entity = None

    def start(self):
        self.server.start()

    def set_entity(self, entity):
        self.entity = entity

    def move(self, x=0, y=0):
        if x == y == 0:
            return
        self.server.move_entity(
            issuer=self.uid,
            euid=self.entity,
            x=x, y=y
        )
