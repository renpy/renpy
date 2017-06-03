label screen_displayables:

    e "There are quite a few screen displayables. Here, I'll tell you about some of the most important ones."

label screen_displayables_menu:

    $ reset_examples()

    menu:

        e "What would you like to know about?"

        "Properties all displayable share.":
            call screen_displayable_properties

        "That's all for now.":
            return

    jump screen_displayables_menu



label screen_displayable_properties:

    "..."

    return


