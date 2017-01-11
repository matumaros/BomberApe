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

    ba = BomberApe()
    game = Game(name='game')
    editor = Editor(name='editor', map_path='content/maps/new.map')
    ba.view.add_widget(game)
    ba.view.add_widget(editor)
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
