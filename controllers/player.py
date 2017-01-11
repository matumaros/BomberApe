

class Player:
    def __init__(self, uid, server, view=None):
        self.uid = uid
        self.server = server
        self.entity = None
        self.view = view

    def start(self):
        self.server.start()

    def update(self, changes):
        try:
            self.entity = changes['change_controller_entity'][self.uid]
        except KeyError:
            pass
        if self.view:
            try:
                spawns = changes['spawn_entities']
            except KeyError:
                pass
            else:
                for euid, entity in spawns.items():
                    coord = '{}|{}'.format(*entity.pos)
                    self.view.board.spawn_entity(
                        coord, entity.uid, entity.skin, entity.size
                    )
            try:
                tiles = changes['updated_tiles']
            except KeyError:
                pass
            else:
                self.view.board.update_tiles(tiles)

    def move(self, x=0, y=0):
        if x == y == 0:
            return
        self.server.move_entity(
            issuer=self.uid,
            euid=self.entity,
            x=x, y=y
        )
