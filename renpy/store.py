# This is the Ren'Py store. It's the module in which the user code
# is executed.

# Import in curry.
from renpy.curry import curry

# Import packages.
import renpy.config
import renpy.display.image
import renpy.display.layout
import renpy.display.behavior

from renpy.python import RevertableList as __renpy__list__
list = __renpy__list__

from renpy.python import RevertableDict as __renpy__dict__
dict = __renpy__dict__

from renpy.python import RevertableObject as object

# Set up symbols.

config = renpy.config
Image = renpy.display.image.Image
Solid = renpy.display.image.Solid
Position = curry(renpy.display.layout.Position)
Resize = curry(renpy.display.layout.Resize)

# TODO: Change the base class when we start implementing rollback.
class Character(object):
    import renpy.config as config

    def __init__(self, name, color=None):
        self.name = name
        self.color = color or config.text_color

    def say(self, what):
        renpy.display_say(self.name, what, color=self.color)
        

# Conveniently get rid of all the packages we had imported before.
import renpy.exports as renpy

