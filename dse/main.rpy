# This is the main program. This can be changed quite a bit to
# customize it for your program... But remember what you do, so you
# can integrate with a new version of DSE when it comes out.

# Declare black, so we can use it in the game,
init:
    image black = Solid((0, 0, 0, 255))

# This is the entry point into the game.
label start:

    # Required to initialize the event engine.
    call events_init from _call_events_init_1

    # Initialize the default values of some of the variables used in
    # the game.
    $ day = 0
    $ strength = 10
    $ intelligence = 10

    scene black


    # The script here is run before any event.

    "In case you're just tuning in, here's the story of my life to
     date."

    "I'm a guy in the second year of high school."

    "I'm not good at sports or school or even something as simple as
     remembering peoples names."

    "In short, I am your usual random loser guy."

    "And this is my story..."


    # We jump to day to start the first day.
    jump day


# This is the label that is jumped to at the start of a day.
label day:

    # Increment the day it is.
    $ day += 1

    # We may also want to compute the name for the day here, but
    # right now we don't bother.

    "It's day %(day)d."

    # Here, we want to set up some of the default values for the
    # day planner. In a more complicated game, we would probably
    # want to add and remove choices from the dp_ variables
    # (especially dp_period_acts) to reflect the choices the
    # user has available to him.

    $ morning_act = "class"
    $ afternoon_act = "hang"
    $ evening_act = "play"

    # Now, we call the day planner, which may set the act variables
    # to new values. 
    call day_planner from _call_day_planner_1


    # We process each of the three periods of the day, in turn.
label morning:

    # Tell the user what period it is.
    centered "Morning"

    # Set these variables to appropriate values, so they can be
    # picked up by the expression in the various events defined below. 
    $ period = "morning"
    $ act = morning_act

    # Execute the events for the morning.
    call events_run_period from _call_events_run_period_1

    # That's it for the morning, so we fall through to the
    # afternoon.

label afternoon:

    # It's possible that we will be skipping the afternoon, if one
    # of the events in the morning jumped to skip_next_period. If
    # so, we should skip the afternoon.
    if check_skip_period():
        jump evening

    # The rest of this is the same as for the morning.

    centered "Afternoon"

    $ period = "afternoon"
    $ act = afternoon_act

    call events_run_period from _call_events_run_period_2


label evening:
    
    # The evening is the same as the afternoon.
    if check_skip_period():
        jump night

    centered "Evening"

    $ period = "evening"
    $ act = evening_act

    call events_run_period from _call_events_run_period_3


label night:

    # This is now the end of the day, and not a period in which
    # events can be run. We put some boilerplate end-of-day text
    # in here.

    centered "Night"

    "It's getting late, so I decide to go to sleep."

    # We call events_end_day to let it know that the day is done.
    call events_end_day from _call_events_end_day_1

    # We force the statistics into the range 0-100.
    $ intelligence = max(intelligence, 0)
    $ intelligence = min(intelligence, 100)

    $ strength = max(strength, 0)
    $ strength = min(strength, 100)

    # And we jump back to day to start the next day. This goes
    # on forever, until an event ends the game.
    jump day
         

# This is the code, that is called from the day planner, to show
# the statistics to the user. It can actually show just about
# anything, so the statistics are really just a suggestion.

label show_stats:

    python hide:

        # Add in a line of dialogue asking the question that's on
        # everybody's mind.
        narrator("What should I do today?", interact=False)

        # This is a list of the statistics that we are showing to the
        # user.
        stats = [
            ('Strength', 100, strength ),
            ('Intelligence', 100, intelligence ),
            ]

        # This is the window that the stats are kept in, if any.
        ui.window(xpos=0,
                  ypos=0,
                  xanchor='left',
                  yanchor='top',
                  xfill=True,
                  yminimum=0)

        ui.vbox()

        ui.text('Day %d' % day)
        ui.null(height=20)

        for name, range, value in stats:

            ui.hbox()
            ui.text(name, minwidth=150)
            ui.bar(600, 20, range, value, ypos=0.5, yanchor=center)
            ui.close()

        ui.close()

    return

