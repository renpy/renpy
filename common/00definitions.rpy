# This file contains a number of definitions of standard
# locations and transitions. We've moved them into the common
# directory so that it's easy for an updated version of all of these
# definitions.

init -1110 python:

    # Positions ##############################################################

    # These are positions that can be used inside at clauses. We set
    # them up here so that they can be used throughout the program.
    left = Position(xalign=0.0)
    center = Position(xalign=0.5)
    truecenter = Position(xalign=0.5, yalign=0.5)
    right = Position(xalign=1.0)

    # Offscreen positions for use with the move transition. Images at
    # these positions are still shown (and consume
    # resources)... remember to hide the image after the transition.    
    offscreenleft = Position(xpos=0.0, xanchor=1.0)
    offscreenright = Position(xpos=1.0, xanchor=0.0)

    # Transitions ############################################################

    # Simple transitions.
    fade = Fade(.5, 0, .5) # Fade to black and back.
    dissolve = Dissolve(0.5)
    pixellate = Pixellate(1.0, 5)

    # Various uses of CropMove.    
    wiperight = CropMove(1.0, "wiperight")
    wipeleft = CropMove(1.0, "wipeleft")
    wipeup = CropMove(1.0, "wipeup")
    wipedown = CropMove(1.0, "wipedown")

    slideright = CropMove(1.0, "slideright")
    slideleft = CropMove(1.0, "slideleft")
    slideup = CropMove(1.0, "slideup")
    slidedown = CropMove(1.0, "slidedown")

    slideawayright = CropMove(1.0, "slideawayright")
    slideawayleft = CropMove(1.0, "slideawayleft")
    slideawayup = CropMove(1.0, "slideawayup")
    slideawaydown = CropMove(1.0, "slideawaydown")

    irisout = CropMove(1.0, "irisout")
    irisin = CropMove(1.0, "irisin")

    # This moves changed images to their new locations
    move = MoveTransition(0.5)

    moveinright = MoveTransition(0.5, enter_factory=MoveIn((1.0, None, 0.0, None)))
    moveinleft = MoveTransition(0.5, enter_factory=MoveIn((0.0, None, 1.0, None)))
    moveintop = MoveTransition(0.5, enter_factory=MoveIn((None, 0.0, None, 1.0)))
    moveinbottom = MoveTransition(0.5, enter_factory=MoveIn((None, 1.0, None, 0.0)))

    moveoutright = MoveTransition(0.5, leave_factory=MoveOut((1.0, None, 0.0, None)))
    moveoutleft = MoveTransition(0.5, leave_factory=MoveOut((0.0, None, 1.0, None)))
    moveouttop = MoveTransition(0.5, leave_factory=MoveOut((None, 0.0, None, 1.0)))
    moveoutbottom = MoveTransition(0.5, leave_factory=MoveOut((None, 1.0, None, 0.0)))

    zoomin = MoveTransition(0.5, enter_factory=ZoomInOut(0.01, 1.0))
    zoomout = MoveTransition(0.5, leave_factory=ZoomInOut(1.0, 0.01))
    zoominout = MoveTransition(0.5, enter_factory=ZoomInOut(0.01, 1.0), leave_factory=ZoomInOut(1.0, 0.01))
    
    # These shake the screen up and down for a quarter second.
    # The delay needs to be an integer multiple of the period.
    vpunch = Move((0, 10), (0, -10), .10, bounce=True, repeat=True, delay=.275)
    hpunch = Move((15, 0), (-15, 0), .10, bounce=True, repeat=True, delay=.275)

    # These use the ImageDissolve to do some nifty effects.
    blinds = ImageDissolve(im.Tile("blindstile.png"), 1.0, 8)
    squares = ImageDissolve(im.Tile("squarestile.png"), 1.0, 256)


init -1110:
    image black = Solid("#000")

init 1110 python:
    if not hasattr(store, 'narrator'):
        narrator = Character(None, kind=adv, what_style='say_thought')

    if not hasattr(store, 'name_only'):
        name_only = adv

    if not hasattr(store, 'centered'):
        centered = Character(None, what_style="centered_text", window_style="centered_window")
