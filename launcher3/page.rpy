# Management of "pages" - major modes of the launcher. This handles defining
# pages, changing the current page, and showing / hinding the page.

init -10 python in page:
    
    from store import renpy, Action, MoveTransition, MoveIn, MoveOut, Dissolve, persistent

    # The name of an overlay page that is open instead of the currently
    # selected page.
    current_overlay = None

    # The name of the currently selected page that's currently showing.
    current = None
    
    # The secondary navigation screen that's currently showing.
    secondary = None
    
    # A list of screens, in left-to-right navigation order. (That is, if 
    # we navigate from screen A to screen B, and screen B is later in the
    # navigation order, we move screen A out on the left, and B in from
    # the right. Otherwise, we move in the opposite direction.
    screens = [ ]
    
    # A map from screen name to the secondary navigation that should be
    # shown when that screen is shown.
    screen_secondary = { }

    # Transitions.
    right_to_left = MoveTransition(
        0.25, 
        enter_factory=MoveIn((1.0, None, 0.0, None)), 
        leave_factory=MoveOut((0.0, None, 1.0, None)))
    
    left_to_right = MoveTransition(
        0.25, 
        enter_factory=MoveIn((0.0, None, 1.0, None)), 
        leave_factory=MoveOut((1.0, None, 0.0, None)))
    
    def define(screen, secondary):
        """
        Defines a page we can navigate to. `Screen` is the screen corresponding
        to that page, while secondary is the secondary navigation page to show
        when that screen is navigated to.
        """
        
        screens.append(screen)
        screen_secondary[screen] = "secnav_" + secondary
        
    def open(screen):
        """
        Changes the page that we're showing.
        """
    
        global current
        global current_overlay
        global secondary

        if current_overlay is not None:
            renpy.hide_screen(current_overlay)
            renpy.show_screen(current)
            current_overlay = None

        if current == screen:
            return
            
        renpy.restart_interaction()
            
        if current is not None:
        
            current_idx = screens.index(current)
            new_idx = screens.index(screen)
                        
            if new_idx > current_idx:
                trans = right_to_left
            else:
                trans = left_to_right
        
            # TODO: Fix the above transitions.
            trans = Dissolve(.25, alpha=True)
        
            if persistent.launcher_uses_transitions:
                renpy.transition(trans, layer="screens")
    
            renpy.hide_screen(current)
            
        renpy.show_screen(screen)
        current = screen
        
        new_secondary = screen_secondary[screen]
        
        if secondary == new_secondary:
            return
            
        if secondary is not None:
            renpy.hide_screen(secondary)
            
        renpy.show_screen(new_secondary)
        secondary = new_secondary
            
    def overlay(screen, **kwargs):
        """
        Shows an overlay page.
        """
        
        global current_overlay
        
        if current_overlay is not None:
            renpy.hide_screen(current_overlay)
        else:
            renpy.hide_screen(current)

        renpy.show_screen(screen, **kwargs)
        current_overlay = screen

    def hide_overlay():
        """
        Hides the overlay page.
        """

        global current_overlay
        
        if current_overlay is not None:
            renpy.hide_screen(current_overlay)
            renpy.show_screen(current)
            current_overlay = None
            
        return
        
    class Primary(Action):
        """
        An action that causes the user to be navigated to the named page.
        This should be used in the top navigation bar. 
        """
        
        def __init__(self, page):
            self.screen = page
            self.secondary = screen_secondary[self.screen]
        
        def __call__(self):
            open(self.screen)
            
        def get_selected(self):
            return secondary == self.secondary

            
    class Secondary(Action):
        """
        An action that causes the user to be navigated to the named page. 
        This should be used in the secondary navigation bar.
        """
   
        def __init__(self, page):
            self.screen = page
            
        def __call__(self):
            open(self.screen)
            
        def get_selected(self):
            return current == self.screen

    def error(message):
        """
        Displays an error message to the user, and then returns to main
        loop.
        """
        
        overlay("error", message=message)

    def warning(message):
        """
        Displays a warning message that the user can dismiss.
        """
        
        overlay("warning", message=message)
        ui.interact()
        
    if persistent.launcher_uses_transitions is None:
        persistent.launcher_uses_transitions = True

# The top navigation screen.
screen topnav:
    zorder 100

    frame:
        style_group "topnav"

        has hbox
        
        textbutton "Ren'Py" action page.Primary("projects")
        textbutton "Navigate" action page.Primary("files")
        
    textbutton "Launch":
        style_group ""
        style "_button"
        text_font "DejaVuSans-ExtraLight.ttf"
        text_size 25
        text_kerning -1.5

        xalign 1.0
        top_margin 2

        action project.Launch()

# The error handling screen.
screen error:

    frame:
        style "page"
        style_group ""

        label "Error"
        text "[message]" 
        
        textbutton "Ok" action Jump("main")

# The warning screen.
screen warning:

    frame:
        style "page"
        style_group ""
    
        label "Warning"
        text "[message]"
        
        textbutton "Ok" action Return(True)


init python:
    page.define("projects", "renpy")
    page.define("settings", "renpy")
    page.define("files", "navigate")
            
            