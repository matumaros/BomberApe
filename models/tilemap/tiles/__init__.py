

from .tile import Tile
from .ground import Ground
from .wall import Wall
from .bridge import Bridge
from .crate import Crate
from .ice import Ice
from .water import Water


TILES = {
    'base': Tile,
    'ground': Ground,
    'wall': Wall,
    'bridge': Bridge,
    'crate': Crate,
    'ice': Ice,
    'water': Water,
}
