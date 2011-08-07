# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This contains code to choose between OpenGL and Software rendering, when
# a system supports both.

init -1024:

    python:
        class _SetRenderer(Action):
            """
            Sets the preferred renderer to one of "auto", "angle", "gl", or 
            "sw". 
            """
            
            def __init__(self, renderer):
                self.renderer = renderer
                
            def __call__(self):
                _preferences.renderer = self.renderer
                renpy.restart_interaction()
                
            def get_selected(self):
                return _preferences.renderer == self.renderer

    # This is displayed to ask the user to choose the renderer he or she
    # wants to use. It takes no parameters, doesn't return anything, and 
    # is expected to call _SetRenderer actions and quit when done.
    #
    # This screen can be customized by the creator, provided the actions 
    # remain available.    
    screen _choose_renderer:

        frame:
            style_group ""
            
            xalign .5
            yalign .33
            xpadding 20
            ypadding 20
    
            xmaximum 400

            has vbox

            label _("Graphics Acceleration")

            null height 10
            
            textbutton _("Automatically Choose"):
                action _SetRenderer("auto")
                xfill True
                
            if renpy.renpy.windows:
                textbutton _("Prefer Angle/DirectX Renderer"):
                    action _SetRenderer("angle")
                    xfill True
                
            textbutton _("Prefer OpenGL Renderer"):
                action _SetRenderer("gl")
                xfill True

            textbutton _("Prefer Software Renderer"):
                action _SetRenderer("sw")
                xfill True

            null height 10

            text _("Changes will take effect the next time this program is run.") substitute True
 
            null height 10

            textbutton _(u"Quit"):
                action Quit(confirm=False)
                xfill True


    # This is displayed when a display performance problem occurs. 
    # 
    # `problem` is the kind of problem that is occuring. It can be:
    # - "sw" if the software renderer was selected.
    # - "slow" if the performance test failed.
    # - other things, added in the future.
    #
    # `url` is the url of a web page on renpy.org that will include
    # info on troubleshooting display problems.
    screen _performance_warning:
    
        frame:
            style_group ""
            
            xalign .5
            yalign .33

            xpadding 20
            ypadding 20

            xmaximum 400

            has vbox

            label _("Performance Warning")
            
            null height 10
            
            if problem == "sw":
                text _("This computer is using software rendering.")
            elif problem == "slow":
                text _("This computer is displaying graphics slowly.")
            else:
                text _("This computer has a problem displaying graphics: [problem].")                
                
            null height 10

            text _("The graphics drivers are not operating correctly. This may lead to slow or incorrect graphics display. {a=[url]}Learn how to fix graphics problems.{/a}") substitute True
            
            null height 10
            
            textbutton _("Continue, Show this warning again"): 
                action Return(True)
                xfill True
                
            textbutton _("Continue, Don't show warning again"):
                action Return(False)
                xfill True
            
            null height 10
        
            textbutton _("Quit"): 
                action Quit(confirm=False)
                xfill True


init -1024 python:
    # The image that we fill the screen with in GL-test mode.
    config.gl_test_image = "black"

    class __GLTest(renpy.Displayable):
        """
         This counts the number of times it's been rendered, and
         the number of seconds it's been displayed, and uses them
         to make the decisions as to if OpenGL is working or not.
         """
        
        def __init__(self, frames, fps, timeout):
            super(__GLTest, self).__init__()

            self.target = 1.0 * frames / fps
            self.frames = frames
            self.timeout = timeout

            self.times = [ ]
            self.success = False
            
            renpy.renpy.display.log.write("- Target is {0} frames in {1} seconds.".format(frames, self.target))
            
        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)

            if self.success:
                return rv

            self.times.append(st)

            renpy.redraw(self, 0)

            renpy.renpy.display.log.write("- Frame drawn at %f seconds." % st)
            
            if len(self.times) >= self.frames:
                frames_timing = self.times[-1] - self.times[-self.frames]

                renpy.renpy.display.log.write("- %f seconds to render %d frames.", frames_timing, self.frames)

                if frames_timing <= self.target:
                    self.success = True
                    renpy.timeout(0)

            return rv                    
                            
        def event(self, ev, x, y, st):

            if self.success:
                return True

            if st > self.timeout:
                return False

            renpy.timeout(self.timeout - st)
   
    config.performance_test = True
        
    def __gl_test():

        import os

        # If we've entered safe mode, display the renderer choice screen.
        # This screen will cause us to quit.

        if _restart:
            return

        if not config.gl_enable:
            return
    
        if renpy.display.interface.safe_mode:
            renpy.call_screen("_choose_renderer")

        if not config.performance_test:
            return

        _gl_performance_test()

    def _gl_performance_test():
    
        import os

        if not _preferences.performance_test and "RENPY_PERFORMANCE_TEST" not in os.environ:
            return

        renpy.renpy.display.log.write("Performance test:")
            
        # This will cause the screen to start displaying.
        ui.pausebehavior(0)
        ui.interact(suppress_underlay=True, suppress_overlay=True)

        # The problem we have.
        problem = None

        if config.renderer != "sw" and renpy.get_renderer_info()["renderer"] == "sw":
            problem = "sw"
        
        # The parameters of the performance test. If we do not hit FPS fps
        # over FRAMES frames before DELAY seconds are up, we fail. 
        FRAMES = 5
        FPS = 15
        DELAY = 1.5
        
        renpy.transition(Dissolve(DELAY), always=True, force=True)
        ui.add(__GLTest(FRAMES, FPS, DELAY))
        result = ui.interact(suppress_overlay=True, suppress_underlay=True)

        if not result:
            problem = "slow"
            
        if problem is None:
            return
    
        # Give the warning message to the user.            
        url = "http://www.renpy.org/display-problems?v=" + renpy.version()
        result = renpy.call_screen("_performance_warning", problem=problem, url=url)

        # Store the user's choice, and continue.        
        _preferences.performance_test = result
        return
        
            
label _gl_test:

    # Show the test image.
    scene
    show expression config.gl_test_image
    
    $ __gl_test()
                
    # Hide the test image.
    scene

    return

