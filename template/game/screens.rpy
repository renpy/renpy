# This file is in the public domain. Feel free to modify it as a basis
# for your own screens.

##############################################################################
# Say
#
# Screen that's used to display adv-mode dialogue.
# http://www.renpy.org/doc/html/screen_special.html#say

screen say:

    # Defaults for side_image and two_window
    default side_image = None
    default two_window = False

    # Decide if we want to use the one-window or two-window varaint.
    if not two_window:

        # The one window variant.        
        window:
            id "window"

            has vbox:
                style "say_vbox"

            if who:
                text who id "who"

            text what id "what"

    else:

        # The two window variant.
        vbox:
            style "say_two_window_vbox"

            if who:            
                window:
                    style "say_who_window"

                    text who:
                        id "who"
                        
            window:
                id "window"

                has vbox:
                    style "say_vbox"

                text what id "what"
                
    # If there's a side image, display it above the text.
    if side_image:
        add side_image



##############################################################################
# Choice
#
# Screen that's used to display in-game menus.
# http://www.renpy.org/doc/html/screen_special.html#choice

screen choice:

    window:
        id "window"

        vbox:
            id "menu"

            for caption, action, button_id, caption_id in items:
                
                if action:
                    button:
                        action action
                        id button_id
                        
                        text caption id caption_id

                else:
                    text caption id caption_id

init python:
    config.narrator_menu = True
    
    style.menu.box_spacing = 2
    style.menu_window.set_parent(style.default)
    style.menu_window.xalign = 0.5
    style.menu_window.yalign = 0.5
    style.menu_choice.set_parent(style.button_text)
    style.menu_choice.clear()
    style.menu_choice_button.set_parent(style.button)
    style.menu_choice_button.xminimum = int(config.screen_width * 0.75)
    style.menu_choice_button.xmaximum = int(config.screen_width * 0.75)


##############################################################################
# Input
#
# Screen that's used to display renpy.input()
# http://www.renpy.org/doc/html/screen_special.html#input

screen input:

    window:
        has vbox

        text prompt
        input id "input"

        
##############################################################################
# Nvl
#
# Screen used for nvl-mode dialogue and menus.
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl:

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        # Display dialogue.
        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10
                
                if who is not None:
                    text who id who_id

                text what id what_id

        # Display a menu, if given.
        if items:
            
            vbox:
                id "menu"

                for caption, action, button_id, caption_id in items:

                    if action:
                        button:
                            action action
                            id button_id

                            text caption id caption_id

                    else:
                        text caption id caption_id

                
        
##############################################################################
# Main Menu 
#
# Screen that's used to display the main menu, when Ren'Py first starts
# http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu:

    # This ensures that any other menu screen is replaced.
    tag menu

    # The background of the main menu.
    window:
        style "mm_root"

    # The main menu buttons.
    frame:
        style_group "mm"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Start Game") action Start()
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Help") action Help()
        textbutton _("Quit") action Quit(confirm=False)

init python:

    # Make all the main menu buttons be the same size.
    style.mm_button.size_group = "mm"


##############################################################################
# Navigation
#
# Screen that's included in other screens to display the game menu
# navigation and background.
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation:

    # The background of the game menu.
    window:
        style "gm_root"

    # The various buttons.
    frame:
        style_group "gm_nav"

        has vbox

        textbutton _("Return") action Return()
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Save Game") action ShowMenu("save")
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Main Menu") action MainMenu()
        textbutton _("Help") action Help()
        textbutton _("Quit") action Quit()

init python:
    style.gm_nav_button.size_group = "gm_nav"
    style.gm_nav_frame.xalign = .98
    style.gm_nav_frame.yalign = .98
    

##############################################################################
# Save, Load
#
# Screens that allow the user to save and load the game.
# http://www.renpy.org/doc/html/screen_special.html#save
# http://www.renpy.org/doc/html/screen_special.html#load

# Since saving and loading are so similar, we combine them into
# a single screen, file_picker. We then use the file_picker screen
# from simple load and save screens.
    
screen file_picker:

    frame:
        style "file_picker_frame"

        has vbox

        # The buttons at the top allow the user to pick a
        # page of files.
        hbox:
            style_group "file_picker_nav"
            
            textbutton _("Previous"):
                action FilePagePrevious()

            textbutton _("Auto"):
                action FilePage("auto")

            for i in range(1, 9):
                textbutton str(i):
                    action FilePage(i)
                    
            textbutton _("Next"):
                action FilePageNext()
                
        # Display a grid of file slots.
        grid 2 5:
            transpose True
            xfill True
            style_group "file_picker"
            
            # Display ten file slots, numbered 1 - 10.
            for i in range(1, 11):

                # Each file slot is a button.
                button:
                    action FileAction(i)
                    xfill True

                    has hbox

                    # Add the screenshot.
                    add FileScreenshot(i)
                    
                    # Format the description, and add it as text.
                    $ description = "% 2d. %s\n%s" % (i, FileTime(i, empty=_("Empty Slot.")), FileSaveName(i))
                    text description

                    key "save_delete" action FileDelete(i)
                    
                    
screen save:

    # This ensures that any other menu screen is replaced.
    tag menu

    use navigation
    use file_picker

screen load:

    # This ensures that any other menu screen is replaced.
    tag menu

    use navigation
    use file_picker

init python:
    style.file_picker_frame = Style(style.menu_frame)

    style.file_picker_nav_button = Style(style.small_button)
    style.file_picker_nav_button_text = Style(style.small_button_text)

    style.file_picker_button = Style(style.large_button)
    style.file_picker_text = Style(style.large_button_text)

    

##############################################################################
# Preferences
#
# Screen that allows the user to change the preferences.
# http://www.renpy.org/doc/html/screen_special.html#prefereces
    
screen preferences:

    tag menu

    # Include the navigation.
    use navigation

    # Put the navigation columns in a three-wide grid.
    grid 3 1:
        style_group "prefs"
        xfill True

        # The left column.
        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Display")
                textbutton _("Window") action Preference("display", "window")
                textbutton _("Fullscreen") action Preference("display", "fullscreen")

            frame:
                style_group "pref"
                has vbox

                label _("Transitions")
                textbutton _("All") action Preference("transitions", "all")
                textbutton _("None") action Preference("transitions", "none")

            frame:
                style_group "pref"
                has vbox

                label _("Text Speed")
                bar value Preference("text speed")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Joystick...") action ShowMenu("joystick_preferences")

        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Skip")
                textbutton _("Seen Messages") action Preference("skip", "seen")
                textbutton _("All Messages") action Preference("skip", "all")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Begin Skipping") action Skip()

            frame:
                style_group "pref"
                has vbox

                label _("After Choices")
                textbutton _("Stop Skipping") action Preference("after choices", "stop")
                textbutton _("Keep Skipping") action Preference("after choices", "skip")

            frame:
                style_group "pref"
                has vbox

                label _("Auto-Forward Time")
                bar value Preference("auto-forward time")

        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Music Volume")
                bar value Preference("music volume")

            frame:
                style_group "pref"
                has vbox

                label _("Sound Volume")
                bar value Preference("sound volume")

                if config.sample_sound:
                    textbutton "Test":
                        action Play("sound", config.sample_sound)
                        style "soundtest_button"

            frame:
                style_group "pref"
                has vbox

                label _("Voice Volume")
                bar value Preference("voice volume")

                if config.sample_voice:
                    textbutton "Test":
                        action Play("voice", config.sample_voice)
                        style "soundtest_button"

init python:
    style.pref_frame.xfill = True
    style.pref_frame.xmargin = 5
    style.pref_frame.top_margin = 5
    style.pref_vbox.xfill = True
    style.pref_button.size_group = "pref"
    style.pref_button.xalign = 1.0
    style.pref_slider.xmaximum = 192
    style.pref_slider.xalign = 1.0
    style.soundtest_button.xalign = 1.0


##############################################################################
# Yes/No Prompt
#
# Screen that asks the user a yes or no question.
# http://www.renpy.org/doc/html/screen_special.html#yesno-prompt
    
screen yesno_prompt:

    modal True

    window:
        style "gm_root"

    frame:
        style_group "yesno"

        has vbox

        label _(message)

        hbox:
            textbutton _("Yes") action yes_action
            textbutton _("No") action no_action


init python:
    
    style.yesno_frame.xfill = True
    style.yesno_frame.xmargin = .05
    style.yesno_frame.ypos = .1
    style.yesno_frame.yanchor = 0
    style.yesno_frame.ypadding = .05
    
    style.yesno_vbox.xalign = 0.5
    style.yesno_vbox.yalign = 0.5
    style.yesno_vbox.box_spacing = 30
    
    style.yesno_hbox.xalign = 0.5
    style.yesno_hbox.spacing = 100
    
    style.yesno_button.size_group = "yesno"

    style.yesno_label.xalign = 0.5
    style.yesno_label_text.text_align = 0.5
