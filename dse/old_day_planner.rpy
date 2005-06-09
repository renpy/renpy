# This file contains the old day planner, the one used in the
# Ren'Py demo.

# Used in the old day planner to show the date.
init:

    $ dp_date = "No Date Set"


# This is the old day planner, as found in the demo code,
# reimplemented to be compatible with the new day planner.
#
# This isn't as well tested as the real one, given above.
label old_day_planner:

    # This is None to indicate that nothing is being edited, or
    # a name, var tuple to give the period that is being edited.
    $ dp_editing = None
    
label old_day_planner_cycle:

    call show_stats
    
    python hide:

        # Period Selection Window.
        ui.window(xpos=0,
                  ypos=200,
                  xanchor='left',
                  yanchor='top',
                  xfill=False,
                  xminimum=300
                  )

        ui.vbox(xpos=0.5, xanchor='center')
        ui.text(dp_date, xpos=0.5, xanchor='center', textalign=0.5)
        ui.null(height=20)

        cannot_continue = False
        
        for name, var in zip(dp_period_names, dp_period_vars):

            def period_clicked(name=name, var=var):
                store.dp_editing = (name, var)
                return True

            value = getattr(store, var)
            valname = ""
                        
            for n, v in dp_period_acts[name]:
                if v == value:
                    valname = n


            if not valname:
                cannot_continue = True
                    
            face = name + ": " + valname


            

            _button_factory(face, "dp",
                            selected = dp_editing == (name, var),
                            clicked = period_clicked)
                            

        ui.null(height=20)

        if cannot_continue:            
            _button_factory("Continue", "dp")
        else:
            _button_factory("Continue", "dp", clicked=ui.returns(False))

        ui.null(height=20)
        ui.close()


        # Choice window.
        if dp_editing:

            name, var = dp_editing
            
            ui.window(xpos=300,
                      ypos=200,
                      xanchor='left',
                      yanchor='top',
                      xfill=False,
                      xminimum=500
                      )

            ui.vbox()

            _label_factory("What will you do in the %s?" %
                           name.lower(), "dp")
            ui.null(height=20)

            for label, value in dp_period_acts[name]:

                def clicked(var=var, value=value):
                    setattr(store, var, value)
                    store.dp_editing = None
                    return True
                    
                

                _button_factory(label, "dp",
                                selected = getattr(store, var) == value, 
                                clicked = clicked)

            ui.close()


    if ui.interact():
        jump old_day_planner_cycle

    return
