# Copyright 2004-2016 Tom Rothamel <pytom@bishoujo.us>
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

screen about:
    $ import sys
    $ import pygame
    $ platform = sys.platform
    $ version = renpy.version()
    $ major = str(sys.version_info[0])
    $ minor = str(sys.version_info[1])
    $ micro = str(sys.version_info[2])
    $ release = str(sys.version_info[3])
    $ serial = str(sys.version_info[4])
    $ SDLmajor = str(pygame.get_sdl_version()[0])
    $ SDLminor = str(pygame.get_sdl_version()[1])
    $ SDLmicro = str(pygame.get_sdl_version()[2])
    $ driver = str(pygame.display.get_driver())
    $ info = pygame.display.Info()
    $ accel = str(info.hw)

    frame:
        style_group "l"
        style "l_root"

        window:
            xfill True

            has vbox xfill True

            add "images/logo.png" xalign 0.5

            null height 5

            text _("[version!q]") xalign 0.5 bold True

            null height 5

            text _("{b}{size=-1}{color=#e8c764}Python {/color}{/size}[major!q].[minor!q].[micro!q] {size=-5}[release!q] [serial!q] {color=#d86e6e}[platform!q]{/color}{/size}{/b}") xalign 0.5

            null height 5
            
            text _("{b}{size=-3}Display driver:  [driver!q]   HW accelerated? [accel!q]{/size}{/b}") xalign 0.5

            null height 5

            text _("{b}{size=-3}SDL version: [SDLmajor!q].[SDLminor!q].[SDLmicro!q]{/size}{/b}") xalign 0.5

            textbutton _("View license") action interface.OpenLicense() xalign 1.0

    textbutton _("Return") action Jump("front_page") style "l_left_button"

label about:
    call screen about
