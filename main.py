#!/usr/bin/env python


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager


class BomberApe(App):
    view = ScreenManager()

    def build(self):
        return self.view


if __name__ == '__main__':
    from screens.game import Game
    from screens.editor import Editor
    from controllers.player import Player

    ba = BomberApe()
    player = Player()
    game = Game(player, name='game')
    editor = Editor(name='editor', map_path='content/maps/new.map')
    ba.view.add_widget(game)
    ba.view.add_widget(editor)
    game.start(map_path='content/maps/new.map')
    ba.run()
