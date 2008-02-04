# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

# This file contains code to report an error after the rest of Ren'Py
# has been de-initialized.

import pygame
import renpy
import textwrap

class ReportError(object):

    # In the init method, Ren'Py is functioning reasonably normally.
    def __init__(self):
        self.font = renpy.display.text.get_font(renpy.store.style.default.font, 14, False, False, False)
        self.flags = pygame.display.get_surface().get_flags()
        self.size = pygame.display.get_surface().get_size()
        
    # In the report method, Ren'Py may be in an ill-defined state.
    def report(self, error_type):
        msg = "Ren'Py has experienced " + error_type + ".\n"
        msg += "Left-click or space reloads, right-click or escape exits."

        screen = pygame.display.set_mode(self.size, self.flags, 32)
        screen.fill((0, 0, 0, 255))
            
        y = 2
        for l in msg.split('\n'):        
            surf = self.font.render(l, True, (255, 255, 255, 255), (0, 0, 0, 255))
            screen.blit(surf, (2, y))

            y += self.font.get_linesize()
            
        pygame.display.flip()

        while True:
            ev = pygame.event.wait()

            if ev.type == pygame.MOUSEBUTTONUP:

                if ev.button == 1:
                    return True
                else:
                    return False

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    return True
                elif ev.key == pygame.K_ESCAPE:
                    return False

            if ev.type == pygame.QUIT:
                return False
            
        
        
        
        
        
        
        
