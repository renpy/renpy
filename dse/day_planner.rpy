# This contains code for the new day planner. You probably
# don't want to change this file, but it might make sense to
# change many of the variables or styles defined here from
# other files.

init -100:

    python:

        # A window placed behind the day planner (empty).
        style.create('dp_window', 'window')
        style.dp_window.ypos = 120
        style.dp_window.yanchor = 'top'

        # The grid containing the three choices in the day planner.
        style.create('dp_grid', 'default')
        style.dp_grid.xfill = True
        
        # Windows containing the groups of choices in the day planner.
        style.create('dp_choice', 'default')
        style.dp_choice.xpos = 0.5
        style.dp_choice.xanchor = 'center'

        # Action buttons.
        style.create('dp_button', 'button')
        style.create('dp_selected_button', 'selected_button')
        style.create('dp_button_text', 'button_text')
        style.create('dp_selected_button_text', 'selected_button_text')

        style.create('dp_done_button', 'button')
        style.create('dp_done_button_text', 'button_text')

        style.dp_done_button.ypos = 0.95
        style.dp_done_button.yanchor = 'bottom'
        
        # Labels.
        style.create('dp_label', 'default')
        style.dp_label.xpos = 0.5
        style.dp_label.xanchor = 'center'

        # The amount of padding between the label and the action
        # in a choice.
        dp_padding = 12 

        # The amount of padding between the choices and done.
        dp_done_padding = 32

        # The title of the done button.
        dp_done_title = "Done Planning Day"

    python:

        # A list of the periods of the day that are present in the
        # day planner. This can be changed at runtime.
        dp_period_names = [ "Morning", "Afternoon", "Evening" ]

        # A list of variables that will take the selected choices
        # for each of the periods named above.
        dp_period_vars = [ "morning_act",
                           "afternoon_act",
                           "evening_act", ]

        # A map from the period names to a list of the activities
        # available for that period. This may be conputed before
        # each call to day_planner. Each entry is a tuple, where
        # the first element is the name shown to the user, and the
        # second is the name assigned to the variable for that
        # period.
        dp_period_acts = {        
            'Morning': [
            ( 'Attend Class', "class" ),
            ( 'Cut Class', "cut"),
            ],
            
            'Afternoon': [
            ( 'Study', "study" ),
            ( 'Hang Out', "hang" ),
            ],
            
            'Evening' : [
            ( 'Exercise', "exercise" ),
            ( 'Play Games', "play" ),
            ],
            }

        

# We assume that the various period variables have been assigned
# default values by this point.
label day_planner:

    call show_stats from _call_show_stats_1

    python hide:

        ui.window(style='dp_window')
        ui.vbox(dp_done_padding)

        ui.grid(len(dp_period_names), 1, xfill=True, style='dp_grid')

        for period, var in zip(dp_period_names, dp_period_vars):

            ui.window(style='dp_choice')
            ui.vbox()

            _label_factory(period, "dp")
            ui.null(height=dp_padding)

            for label, value in dp_period_acts[period]:

                def clicked(var=var, value=value):
                    setattr(store, var, value)
                    return True

                _button_factory(label, "dp",
                                selected = getattr(store, var) == value,
                                clicked=clicked)

            ui.close()

        ui.close()
            
        _button_factory(dp_done_title, "dp_done",
                        clicked = lambda : False )

        ui.close()

        
    if ui.interact():
        jump day_planner

    return 
