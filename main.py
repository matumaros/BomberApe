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

    ba = BomberApe()
    game = Game(name='game')
    editor = Editor(name='editor')
    editor.board.update_tiles({(1, 1): 'grass', (1, 0): 'stone_wall'})
    ba.view.add_widget(editor)
    ba.view.add_widget(game)
    ba.run()
