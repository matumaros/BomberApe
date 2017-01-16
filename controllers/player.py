

from copy import deepcopy


CHANGES_TEMPLATE = {
    'move': {},
}


class Player:
    def __init__(self, uid, view=None):
        self.uid = uid
        self.entity = None
        self.view = view
        self.changes = deepcopy(CHANGES_TEMPLATE)

    def pos_to_coord(self, pos):
        return '{}|{}'.format(*pos)

    def update(self, changes):
        try:
            self.entity = changes['change_controller_entity'][self.uid]
        except KeyError:
            pass

        if self.view:
            spawns = changes.get('spawn_entities', {})
            for euid, entity in spawns.items():
                coord = self.pos_to_coord(entity.pos)
                self.view.board.spawn_entity(
                    coord, entity.uid, entity.type, entity.size
                )

            entities = changes.get('move_entities', {})
            for euid, pos in entities.items():
                coord = self.pos_to_coord(pos)
                self.view.board.move_entity(coord, euid)
                if euid == self.entity:
                    self.view.board.focused_coord = coord

            tiles = changes.get('updated_tiles', {})
            self.view.board.update_tiles(tiles)

        changes = self.changes
        self.changes = deepcopy(CHANGES_TEMPLATE)
        return changes

    def move(self, x=0, y=0):
        if x == y == 0:
            return
        self.changes['move'][self.entity] = (x, y)
