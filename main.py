#!/usr/bin/env python


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager


class BomberApe(App):
    view = ScreenManager()

    def build(self):
        return self.view


if __name__ == '__main__':
    from screens.main_menu import MainMenu

    ba = BomberApe()
    main_menu = MainMenu(name='main_menu')
    ba.view.add_widget(main_menu)
    ba.run()
