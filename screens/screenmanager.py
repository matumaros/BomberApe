

from kivy.uix.screenmanager import ScreenManager as Base


class ScreenManager(Base):
    def switch_to(self, name):
        if self.current:
            self.current_screen.lose_focus()
        self.current = name
        self.current_screen.gain_focus()
