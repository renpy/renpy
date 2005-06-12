# This file ensures that renpy packages will be imported in the right
# order.

# Some version numbers and things.
version = "Ren'Py 4.8.8"
script_version = 8007
savegame_suffix = "-8.4.save"


# Can be first, because has no dependencies, and may be imported
# directly.
import renpy.game

# Should probably be early, as we will add it as a base to serialized things.
import renpy.object # ?

import renpy.ast
import renpy.curry
import renpy.execution
import renpy.loader
import renpy.loadsave
import renpy.parser
import renpy.python # object
import renpy.script
import renpy.style

import renpy.display
import renpy.display.presplash
import renpy.display.module
import renpy.display.render # Most display stuff depends on this.
import renpy.display.core # object
import renpy.display.audio
import renpy.display.text # core
import renpy.display.layout # core
import renpy.display.behavior # layout
import renpy.display.transition # core
import renpy.display.im
import renpy.display.image # core, behavior, im
import renpy.display.video
import renpy.display.focus
import renpy.display.anim

import renpy.ui
import renpy.lint

import renpy.exports
import renpy.config # depends on lots.
import renpy.store  # depends on everything.
import renpy.main
