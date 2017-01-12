

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen as Base


class Screen(Base):
    keybindings = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actionbindings = {}

    def gain_focus(self):
        Window.bind(on_key_down=self.on_key_down)

    def lose_focus(self):
        Window.unbind(on_key_down=self.on_key_down)

    def on_key_down(self, keyboard, keycode, scancode, text, modifiers):
        try:
            action = self.keybindings[(keycode, tuple(modifiers))]
        except KeyError:
            print('key not bound:', (keycode, tuple(modifiers)))
            pass
        else:
            self.actionbindings[action]()
