
from uuid import uuid4

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from controllers.player import Player
from controllers.server import Server
from screens.game import Game
from screens.editor import Editor


class MainMenu(Screen):
    Builder.load_file('screens/main_menu.kv')

    keybindings = {
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Window.bind(on_key_down=self.on_key_down)

        self.actionbindings = {
        }

    def init_game(self):
        if self.parent.has_screen('game'):
            screen = self.parent.get_screen('game')
            self.parent.remove_widget(screen)
        game = Game(name='game')
        self.parent.add_widget(game)
        server = Server()
        server.load_map('content/maps/new.map')
        player = Player(uuid4(), server)
        server.players = {
            player.uid: player,
        }
        euid = uuid4()
        server.spawn_entity('gorilla', euid, player.uid)
        game.start(player)
        self.parent.current = 'game'

    def init_editor(self):
        if self.parent.has_screen('editor'):
            screen = self.parent.get_screen('game')
            self.parent.remove_widget(screen)
        editor = Editor(name='editor', map_path='content/maps/new.map')
        self.parent.add_widget(editor)
        self.parent.current = 'editor'

    def on_key_down(self, keyboard, keycode, scancode, text, modifiers):
        try:
            action = self.keybindings[(keycode, tuple(modifiers))]
        except KeyError:
            print('key not bound:', (keycode, tuple(modifiers)))
            pass
        else:
            self.actionbindings[action]()
