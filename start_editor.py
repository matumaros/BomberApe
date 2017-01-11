

from main import BomberApe
from screens.editor import Editor


ba = BomberApe()
editor = Editor(name='editor', map_path='content/maps/new.map')
ba.view.add_widget(editor)
ba.run()
