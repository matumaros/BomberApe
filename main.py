#!/usr/bin/env python


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager


class BomberApe(App):
    view = ScreenManager()

    def build(self):
        return self.view


if __name__ == '__main__':
    from uuid import uuid4

    from screens.game import Game
    from screens.editor import Editor
    from controllers.player import Player
    from controllers.server import Server
    from controllers.entities.player import Player as PlayerEntity

    ba = BomberApe()
    game = Game(name='game')
    editor = Editor(name='editor', map_path='content/maps/new.map')
    ba.view.add_widget(game)
    ba.view.add_widget(editor)
    # Example game setup
    server = Server()
    player = Player(uuid4(), server)
    server.players = {
        player.uid: player,
    }
    euid = uuid4()
    server.entities = {
        euid: PlayerEntity(euid, player.uid, (0, 0)),
    }
    server.map_path = 'content/maps/new.map'
    game.start(player)
    ###
    ba.run()
