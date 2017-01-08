#!/usr/bin/env python


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager


class BomberApe(App):
    view = ScreenManager()

    def build(self):
        return self.view


if __name__ == '__main__':
    from screens.game import Game

    ba = BomberApe()
    game = Game()
    ba.view.add_widget(game)
    ba.run()
