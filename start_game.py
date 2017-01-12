

from uuid import uuid4

from main import BomberApe
from screens.game import Game
from controllers.player import Player
from controllers.game import Game as Server

ba = BomberApe()
game = Game(name='game')
ba.view.add_widget(game)
# Example game setup
server = Server()
server.load_map('content/maps/new.map')
player = Player(uuid4(), server)
server.players = {
    player.uid: player,
}
euid = uuid4()
server.spawn_entity('gorilla', euid, player.uid)
game.start(player)
###
ba.run()
