# This is the code for the logo example.
init python:

    # This spins the logo, while at the same time zooming it and decreasing the
    # alpha.
    def logo_transform(t, st, at):

        # Repeat every 10 seconds.
        st = st % 7.0

        # The move takes 5 seconds.
        done = min(st / 5.0, 1.0)

        t.xpos = done
        t.xanchor = 1.0 - done
        t.ypos = .5
        t.yanchor = .5
        t.rotate = 360 * done
        t.alpha = 1.0 - done
        t.zoom = 1.0  + done

        return 0


# This is the code for the balls example. It's a bit complicated, but most of
# this is the code for ball movement and so on. Only a very little bit of this
# actually deals with Ren'Py.
init python:
    import math

    class Ball(object):
        def __init__(self, filename, x, y, function=None):

            self.transform = Transform(child=filename, xanchor=0.5, yanchor=0.5, rotate=0, function=function)
            self.x = x
            self.y = y

            MAX_SPEED = 150

            self.dx = renpy.random.uniform(-MAX_SPEED, MAX_SPEED)
            self.dy = renpy.random.uniform(-MAX_SPEED, MAX_SPEED)

            # Rotation speed.
            self.drotate = renpy.random.uniform(0, 180)

    # This is called
    def balls_collide(p1, p2):
        """
        Check to see if any of the balls are colliding. If they are,
        then handle the collision.
        """

        DOUBLE_RADIUS = 75

        x21 = p2.x - p1.x
        y21 = p2.y - p1.y

        d = math.hypot(x21, y21)

        # Return if too far.
        if d > DOUBLE_RADIUS:
            return

        vx21 = p2.dx - p1.dx
        vy21 = p2.dy - p1.dy

        # Return if not approaching.
        if (vx21 * x21 + vy21 * y21) > 0:
            return

        # Fix divide by zero.
        if x21 == 0:
            x21 = .00001

        # Compute the collision.
        a = y21 / x21
        dvx2 = -(vx21 + a * vy21) / (1 + a * a)

        p2.dx += dvx2
        p2.dy += a * dvx2

        p1.dx -= dvx2
        p2.dy -= a * dvx2

    # This is called by the first transform. It updates all of the
    # transforms.
    def balls_update(pilot, st, at):

        global last_time

        RADIUS = 75 / 2
        LEFT = RADIUS
        RIGHT = 800 - RADIUS
        TOP = RADIUS
        BOTTOM = 600 - RADIUS

        # The pilot is the first ball in our list, and he's the one
        # that gets last_time updated.
        if last_time is None:
            dt = 0
        else:
            dt = st - last_time

        last_time = st

        # Handle current collisions.
        for i in xrange(0, len(balls)):
            for j in xrange(i + 1, len(balls)):
                balls_collide(balls[i], balls[j])

        # Basic movement, and bouncing off the walls.
        for i in balls:

            i.x += i.dx * dt
            i.y += i.dy * dt

            if i.x < LEFT:
                i.x = LEFT
                i.dx = abs(i.dx)

            if i.x > RIGHT:
                i.x = RIGHT
                i.dx = -abs(i.dx)

            if i.y < TOP:
                i.y = TOP
                i.dy = abs(i.dy)

            if i.y > BOTTOM:
                i.y = BOTTOM
                i.dy = -abs(i.dy)


        # Update the transforms.
        for i in balls:

            # This is the code that deals with Ren'Py to update the
            # various transforms. Note that we use absolute coordinates
            # to position ourselves with subpixel accuracy.
            i.transform.xpos = absolute(i.x)
            i.transform.ypos = absolute(i.y)
            i.transform.rotate = (i.drotate * st) % 360.0

            i.transform.update()

        return 0

# These are used in the button example:
init python:
    def button_transform(t, st, at):
        t.rotate = (90 * st) % 360.0
        return 0

label demo_transform:

    e "The Transform function allows you to rotate, zoom, move, and adjust the alpha of a displayable."

    e "It does this under the control of a Python function, making it incredibly flexible at the cost of some complexity."

    hide eileen
    with dissolve

    show logo base at Transform(function=logo_transform)

    e "Here's a simple example, showing how we can change an image as it moves around the screen."

    e "A nice thing about Transform is that it's \"one price\"."

    e "If you use it to do a rotation, you can zoom or adjust alpha at no additional cost."

    hide logo base
    with dissolve

    python:

        last_time = None

        # Define a list of ball objects.
        balls = [
            Ball("eileen_orb.png", 200, 150, function=balls_update),
            Ball("lucy_orb.png", 400, 150),
            Ball("eileen_orb.png", 600, 150),

            Ball("lucy_orb.png", 200, 300),
            Ball("lucy_orb.png", 600, 300),

            Ball("eileen_orb.png", 200, 450),
            Ball("lucy_orb.png", 400, 450),
            Ball("eileen_orb.png", 600, 450),
            ]

        # Add each ball's transform to the screen.
        for i, b in enumerate(balls):
            renpy.show("ball%d" % i, what=b.transform)

    with dissolve

    e "As the python functions get more complicated, more advanced behavior is possible."

    e "This can include coordinating more than one Transform."

    python:
        for i, b in enumerate(balls):
            renpy.hide("ball%d" % i)


    with dissolve

    python hide:
        ui.transform(function=button_transform, xalign=0.5, yalign=0.5)
        ui.textbutton(_("A Working Button"), clicked=ui.returns(True))

    e "Finally, transforms can be applied to buttons, and work even while the button is zoomed."

    show eileen happy
    with dissolve

    e "With a little Python code, transforms let you do a lot of things."



    return
