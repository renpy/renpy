# This file contains code to automatically switch the game into
# fullscreen mode.

# Please note: Fullscreen mode is broken on some platforms (mostly
# virtual windows machines like vmware and virtual PC). So having
# this code automatically execute could make your game hard to use
# on those platforms.
#
# The way we work around this is to tell users of these platforms
# to press 'f' to toggle fullscreen mode. If the game's running in
# windowed mode, the problems don't seem to appear.
#
# You should probably put words to that effect in some sort of
# README file.

# The first time this code runs, the game switches into fullscreen.
# After that, it respects the user's preference. 

init:
    python:
        if not persistent.set_fullscreen:
            persistent.set_fullscreen = True
            _preferences.fullscreen = True
