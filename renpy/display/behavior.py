# This contains various Displayables that handle events.


import renpy.display.core as core
import renpy.display.layout as layout
import renpy.display.text as text
import renpy.config as config
import renpy.game as game

import pygame
from pygame.constants import *

class Keymap(layout.Container):
    """
    This is a behavior that maps keys to functions that are called when
    the key is pressed. The keys are specified by giving the appropriate
    k_constant from pygame.constants, or the unicode for the key.
    """

    def __init__(self, **keymap):
        self.keymap = keymap

    def event(self, ev, x, y):

        if ev.type != KEYDOWN:
            return

        for key, action in self.keymap.iteritems():
            if key == ev.unicode or ev.key == getattr(pygame.constants, key, None):
                action()
                raise core.IgnoreEvent()

    def render(self, width, height, st, tt):
        return None

class SayBehavior(layout.Container):
    """
    This is a class that implements the say behavior,
    which is to return True (ending the interaction) if
    the user presses space or enter, or clicks the left
    mouse button.
    """

    def event(self, ev, x, y):
        if ev.type == MOUSEBUTTONDOWN:
            if ev.button == 1:
                return True

        if ev.type == KEYDOWN:
            if ev.key == K_RETURN:
                return True

            if ev.key == K_SPACE:
                return True

        return None

class Menu(layout.VBox):

    def __init__(self, menuitems):
        """
        @param menuitems: A list of menuitem tuples. The first element
        of each tuple is the string that should be displayed to the
        user. The second item is the value that should be returned if
        this item is selected, or None to indicate that this item is a
        caption.
        """

        super(Menu, self).__init__(full=False)

        self.selected = None
        self.results = [ ]

        for i, (caption, result) in enumerate(menuitems):
            self.add(text.Text(caption))

            if not self.selected and result is not None:
                self.selected = i

            self.results.append(result)

        self.update_colors()

    def update_colors(self):
        """
        This updates the colors of our children to reflect the
        one that has been selected by the user.
        """

        for i, (child, result) in enumerate(zip(self.children, self.results)):

            # Captions should stay the default text color.
            if result is None:
                continue

            # Actual choices change color if they are selected or not.
            if i == self.selected:
                child.color = config.menu_selected_color
            else:
                child.color = config.menu_unselected_color


    def event(self, ev, x, y):
        """
        Processes events.
        """

#        print ev
#        print x, y

        old_selected = self.selected

        # Change selection based on mouse position.
        if ev.type == MOUSEMOTION:
            target = self.child_at_point(x, y)
            if target is None:
                return None

            if self.results[target] is not None:
                self.selected = target

        # Make selection based on mouse click position.
        if ev.type == MOUSEBUTTONDOWN:
            target = self.child_at_point(x, y)
            if target is None:
                return None

            if self.results[target] is not None:
                return self.results[target]

        # Change selection based on keypress.
        if ev.type == KEYDOWN and ev.key == K_DOWN:

            selected = self.selected

            while selected < len(self.results) - 1:
                selected += 1
                if self.results[selected] is not None:
                    self.selected = selected
                    break

        # Change selection based on keypress.
        if ev.type == KEYDOWN and ev.key == K_UP:

            selected = self.selected

            while selected > 0:
                selected -= 1
                if self.results[selected] is not None:
                    self.selected = selected
                    break

        # Make selection based on keypress.
        if ev.type == KEYDOWN and ev.key == K_RETURN:
            return self.results[self.selected]
            
        # If the selected item changed, update the display.
        if self.selected != old_selected:

            self.children[self.selected].color = config.menu_selected_color
            self.children[old_selected].color = config.menu_unselected_color

            game.interface.redraw(0)

        return None
        

# class MenuBehavior(layout.Container):
    
