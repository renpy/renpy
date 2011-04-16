# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains code to handle GUI-based error reporting. There are 
# two unrelated mechanisms here. 
#
# report_exception is used to report an exception that occurs when the GUI
# system is behaving reasonably.
#
# ReportError is used to report an exception that occurs when the GUI is not
# initialized, such as after a reload.

import renpy.display
import os

##############################################################################
# Initialized approach.

def call_exception_screen(**kwargs):
    renpy.exports.show_screen("_exception", _transient=True, **kwargs)
    return renpy.ui.interact(mouse="screen", type="screen", suppress_overlay=True, suppress_underlay=True)

def rollback_action():
    renpy.exports.rollback(force=True)
    
def init_display():
    """
    The minimum amount of code required to init the display.
    """

    if not renpy.game.interface:
        renpy.display.core.Interface()
        renpy.style.build_styles()
        renpy.loader.index_archives()
        renpy.display.im.cache.init()
    
    renpy.ui.reset()
    
def report_exception(short, full):
    """
    Reports an exception to the user. Returns True if the exception should
    be raised by the normal reporting mechanisms. Otherwise, should raise
    the appropriate exception.
    """

    if "RENPY_SIMPLE_EXCEPTIONS" in os.environ:
        return True
       
    if not renpy.exports.has_screen("_exception"):
        return True
    
    init_display()    
          
    if not renpy.game.context().init_phase:
        rollback_action = renpy.display.error.rollback_action
        reload_action = renpy.exports.curried_call_in_new_context("_save_reload_game")
    else:
        rollback_action = None
        reload_action = renpy.exports.utter_restart

    if renpy.game.context(-1).next_node is not None:
        ignore_action = renpy.ui.returns(False)
    else:
        ignore_action = None
     
    renpy.game.invoke_in_new_context(
        call_exception_screen, 
        short=short, full=full, 
        rollback_action=rollback_action,
        reload_action=reload_action,
        ignore_action=ignore_action,
        )

##############################################################################
# Non-initialized approach.

commandfile = "command.%d.txt" % os.getpid()

class ReportError(object):

    # In the init method, Ren'Py is functioning reasonably normally.
    def __init__(self):
        self.font = renpy.display.text.get_font(renpy.store.style.default.font, 14, False, False, False) #@UndefinedVariable
        # self.flags = pygame.display.get_surface().get_flags()
        # self.size = pygame.display.get_surface().get_size()

        self.size = (renpy.config.screen_width, renpy.config.screen_height)
        
    # In the report method, Ren'Py may be in an ill-defined state.
    def report(self, error_type):
        import os.path
        import pygame # W0404

        pygame.display.init()
        pygame.display.set_caption("Ren'Py Error - left-click reloads, right-click quits")
        
        msg = "Ren'Py has experienced " + error_type + ".\n"
        msg += "Left-click or space reloads, right-click or escape exits."

        screen = pygame.display.set_mode(self.size, 0, 32)
            
        pygame.time.set_timer(pygame.USEREVENT + 1, 50)

        while True:

            if commandfile and os.path.exists(commandfile):
                return True

            screen.fill((0, 0, 0, 255))
            
            y = 2
            for l in msg.split('\n'):        
                surf = self.font.render(l, True, (255, 255, 255, 255), (0, 0, 0, 255))
                screen.blit(surf, (2, y))

                y += self.font.get_linesize()
                        
            pygame.display.flip() # E1120

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
