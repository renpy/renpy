# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file contains code that helps Ren'Py run on an iRex iLiad.

import os
import renpy

address = os.environ.get("RENPY_ILIAD", None)

if address is not None:

    import socket
    import pygame
    import _renpy
    
    dm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dm_socket.connect((address, 50555))

    busy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    busy_socket.connect((address, 50071))

    pagebar_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pagebar_socket.connect((address, 50073))
    
    pygame_Surface = pygame.Surface
    pygame_display_set_mode = pygame.display.set_mode
    pygame_display_update = pygame.display.update
    pygame_display_get_surface = pygame.display.get_surface
    pygame_event_wait = pygame.event.wait
    
    window = None
    surface = None

    # Used for gamma correction, if it proves necessary.
    ramp = "".join(chr(i) for i in xrange(256))
    
    def set_mode(size, flags=0, depth=32):
        global window
        global surface

        window = pygame_display_set_mode(size, 0, 8)
        surface = pygame_Surface(size, 0, 32)

        # ccPbReset
        pagebar_socket.send("17,200")
        
        return surface
        
    pygame.display.set_mode = set_mode

    def get_surface():
        return surface

    pygame.display.get_surface = get_surface

    def update(rectangle=None):        
        _renpy.staticgray(surface, window, 44, 127, 84, 0, 8, ramp)
        pygame_display_update()
        dm_socket.send("!0,3,0")
        
    pygame.display.update = update

    def wait():
        busy_socket.send("0,0")
        return pygame_event_wait()

    pygame.event.wait = wait
    
    os.environ["SDL_VIDEO_X11_WMCLASS"] = "sh"

    def post_init():
    
        # Pagebar Right - short 281 (K_PAGEDOWN), long 282 (K_F1)
        # Pagebar Left - short 280 (K_PAGEUP), long 283 (K_F2)
        # Arrow Up - short 273 (K_UP), long 285 (K_F4)
        # Arrow Down - short 274 (K_DOWN), long 284 (K_F3)
        # Circle - short 13 (K_RETURN), long 287 (K_F6)
        # Updir - short 286 (K_F5), long 278 (K_HOME)

        renpy.config.keymap = dict(
            rollback = [ 'K_PAGEUP' ],
            screenshot = [ ],
            toggle_fullscreen = [ ],
            toggle_music = [ ],
            game_menu = [ 'K_HOME', 'K_F6' ],
            hide_windows = [ ],
            launch_editor = [ ],
            dump_styles = [ ],
            reload_game = [ ],
            inspector = [ ],
            developer = [ ],
            quit = [ 'K_F5' ],
            iconify = [ ],
            help = [ ],

            # Say.
            rollforward = [ ],
            dismiss = [ 'mousedown_1', 'K_RETURN', 'K_PAGEDOWN' ],

            # Pause.
            dismiss_hard_pause = [ ],

            # Focus.
            focus_left = [ ],
            focus_right = [ ],
            focus_up = [ 'K_UP', 'joy_up' ],
            focus_down = [ 'K_DOWN', 'joy_down' ],

            # Button.
            button_select = [ 'mouseup_1', 'K_RETURN' ],

            # Input.
            input_backspace = [ ],
            input_enter = [ 'K_RETURN' ],

            # Viewport.
            viewport_up = [ ],
            viewport_down = [ ],
            viewport_drag_start = [ 'mousedown_1' ],
            viewport_drag_end = [ 'mouseup_1' ],

            # These keys control skipping.
            skip = [ ],
            toggle_skip = [ ],
            fast_skip = [ ],

            # These control the bar.
            bar_activate = [ 'mousedown_1' ],
            bar_deactivate = [ 'mouseup_1' ],
            bar_decrease = [ ],
            bar_increase = [ ],
            )

        try:
            renpy.config.save_directory = None
            renpy.config.help = None
        except:
            pass
        
        try:
            renpy.config.has_sound = False
            renpy.config.has_voice = False
            renpy.config.has_music = False
        except:
            pass
        
    renpy.game.post_init.append(post_init)
