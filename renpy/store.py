# This is the Ren'Py store. It's the module in which the user code
# is executed.

# But please note that this will not be available in the body
# of user code, unless we re-import it.
import renpy

from renpy.python import RevertableList as __renpy__list__
list = __renpy__list__

from renpy.python import RevertableDict as __renpy__dict__
dict = __renpy__dict__

from renpy.python import RevertableObject as object

# Set up symbols.

config = renpy.config
Image = renpy.display.image.Image
Solid = renpy.display.image.Solid
Position = renpy.curry.curry(renpy.display.layout.Position)
Resize = renpy.curry.curry(renpy.display.layout.Resize)

# Note that this is really a RevertableObject.
# TODO: Move this someplace saner. Like perhaps to .exports. But
# be sure to change the base class after the move!

class Character(object):
    import renpy.config as config

    def __init__(self, name,
                 who_style='say_label', what_style='say_dialogue',
                 window_style='window_say', **properties):

        self.name = name
        self.who_style = who_style
        self.what_style = what_style
        self.window_style = window_style
        self.properties = properties

    def say(self, what):
        renpy.display_say(self.name, what,
                          who_style=self.who_style,
                          what_style=self.what_style,
                          **self.properties)
        

# Conveniently get rid of all the packages we had imported before.
import renpy.exports as renpy

