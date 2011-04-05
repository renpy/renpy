# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This contains code to choose between OpenGL and Software rendering, when
# a system supports both.

init -1024:
    screen _gl_test:
        frame:
            style_group ""
            
            xalign .5
            yalign .33

            xpadding 20
            ypadding 20

            has vbox

            label _(u"Graphics Acceleration")

            null height 10
            
            textbutton _(u"Automatically Choose"):
                size_group "gl"
                action SetField(persistent, "_gl_test", "auto")
            textbutton _(u"Prefer Software Renderer"):
                size_group "gl"
                action SetField(persistent, "_gl_test", "sw")
            textbutton _(u"Prefer OpenGL Renderer"):
                size_group "gl"
                action SetField(persistent, "_gl_test", "gl")

            null height 10

            textbutton _(u"Continue"):
                size_group "gl"
                action Return(True)

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
            
        def render(self, width, height, st, at):
            self.times.append(st)

            renpy.redraw(self, 0)

            renpy.renpy.display.log.write("Frame drawn at %f seconds." % st)
            
            if len(self.times) >= self.frames:
                frames_timing = self.times[-1] - self.times[-self.frames]

                renpy.renpy.display.log.write("It took %f seconds to render %d frames.", frames_timing, self.frames)

                if frames_timing <= self.target:
                    self.success = True
                    renpy.timeout(0)
                    
            rv = renpy.Render(width, height)
            return rv
                            
        def event(self, ev, x, y, st):

            if self.success:
                return True

            if st > self.timeout:
                return False

            renpy.timeout(self.timeout - st)


    def __gl_prefer_renderers(renderers):
        """
         Forces the current renderer to be renderer, one of gl or sw.
         """

        if renpy.display.prefer_renderers == renderers:
            return

        renpy.display.prefer_renderers = renderers        
        renpy.display_reset()
                    
    def __gl_prompt():
        """
         Decides if we want to prompt the user to enable OpenGL mode.
         If so, shows a screen that allows the user to alter the
         OpenGL setting.
         """

        if not renpy.display.interface.safe_mode:
            return 

        __gl_prefer_renderers("sw")
        
        renpy.call_screen("_gl_test")

        renpy.display.interface.safe_mode = False
        
    def __gl_test():
        """
         Makes the decision as to if we should use GL or SW mode.
         """

        import os
        if "RENPY_RENDERER" in os.environ:
            return

        # Our decision survives a restart.
        if _restart:
            return

        renpy.renpy.display.log.write("GL test mode: %s", persistent._gl_test)

        # If GL is disabled, don't bother.
        if not config.gl_enable:
            return
        
        __gl_prompt()

        if persistent._gl_test == "gl":
            __gl_prefer_renderers("gl,sw")
            return

        if persistent._gl_test == "sw":
            __gl_prefer_renderers("sw")
            return

        __gl_prefer_renderers("gl,sw")

        ui.pausebehavior(0)
        ui.interact(suppress_underlay=True, suppress_overlay=True)

        # If GL is able to render FRAMES frames at FPS fps in less
        # than DELAY seconds, we consider it to be operational, and
        # continue in GL mode. Otherwise, we rever to software
        # rendering mode.
        FRAMES = 5
        FPS = 15
        DELAY = 1
        
        renpy.transition(Dissolve(DELAY), always=True, force=True)
        ui.add(__GLTest(FRAMES, FPS, DELAY))
        result = ui.interact(suppress_overlay=True, suppress_underlay=True)

        if result:
            __gl_prefer_renderers("gl,sw")
        else:
            __gl_prefer_renderers("sw")

    # Init-time code:
    # Make a guess as to what modes we should be in.
    if persistent._gl_test is None:
        persistent._gl_test = "auto"

    if persistent._gl_test == "sw":
        renpy.display.prefer_renderers = "sw"
        
            
label _gl_test:

    # Show the test image.
    scene
    show expression config.gl_test_image
    
    $ __gl_test()
                
    # Hide the test image.
    scene

    return

