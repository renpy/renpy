# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This file contains code to perform the OpenGL test. This is always
# run - even in software mode - so that the user experience remains
# consistent. (But it terminates early in sw-mode.)

init -1024 python:
    # The image that we fill the screen with in GL-test mode.
    config.gl_test_image = "black"

    class __GLTest(renpy.Displayable):
        """
         This counts the number of times it's been rendered, and
         the number of seconds it's been displayed, and uses them
         to make the decisions as to if OpenGL is working or not.
         """
        
        def __init__(self, frames, timeout):
            super(__GLTest, self).__init__()

            self.frames = frames
            self.timeout = timeout
            
        def render(self, width, height, st, at):
            self.frames -= 1

            if self.frames <= 0:
                renpy.timeout(0)

            renpy.redraw(self, 0)
                
            rv = renpy.Render(width, height)
            return rv
            
                
        def event(self, ev, x, y, st):
            st = st

            if self.frames <= 0:
                return True

            if st > self.timeout:
                return False

            renpy.timeout(self.timeout - st)

label _gl_test:

    # Show the test image.
    show expression config.gl_test_image
    
    python hide:

        # If GL is able to render FRAMES in DELAY seconds, we consider it to
        # be operational, and continue in GL mode. Otherwise, we rever to
        # software rendering mode.
        FRAMES = 4
        DELAY = .25
        
        import os

        if (not "RENPY_RENDERER" in os.environ) and (renpy.get_renderer_info()["renderer"] == "gl"):

            for i in range(0, 2):
            
                renpy.pause(0)

                renpy.transition(Dissolve(DELAY))            
                ui.add(__GLTest(FRAMES, DELAY))
                rv = ui.interact(suppress_overlay=True, suppress_underlay=False)

                if rv:
                    break
                
            else:
                config.gl_enable = False
                renpy.display_reset()
                       
    # Hide the test image.
    scene

    return
        
