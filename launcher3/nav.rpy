init -10 python in nav:
    
    from store import renpy, Action
    
    # The screen that's currently showing.
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
    
    def page(screen, secondary):
        """
        Defines a page we can navigate to. `Screen` is the screen corresponding
        to that page, while secondary is the secondary navigation page to show
        when that screen is navigated to.
        """
        
        screens.append(screen)
        screen_secondary[screen] = "secnav_" + secondary
        
    def show_page(screen):
        global current
        global secondary
        
        if current == screen:
            return
            
        renpy.restart_interaction()
            
        # TODO: Set up the appropriate transition.
            
        if current is not None:
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
            
        
    class TopPage(Action):
        """
        An action that causes the user to be navigated to the named page.
        This should be used in the top navigation bar. 
        """
        
        def __init__(self, page):
            self.screen = page
            self.secondary = screen_secondary[self.screen]
        
        def __call__(self):
            show_page(self.screen)
            
        def get_selected(self):
            return secondary == self.secondary

            
    class SecPage(Action):
        """
        An action that causes the user to be navigated to the named page. 
        This should be used in the secondary navigation bar.
        """
   
        def __init__(self, page):
            self.screen = page
            
        def __call__(self):
            show_page(self.screen)
            
        def get_selected(self):
            return current == self.screen
