

from uuid import uuid4

from .server import Server


class Player:
    def __init__(self):
        self.uid = uuid4()
        self.server = Server()
        self.entity = None

    def start(self, map_path):
        self.server.start(map_path)

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
