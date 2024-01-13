# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

define gui.project_system_font = None
define gui.asian = False

# This is set in new_project before new_template_project is called,
# and provides the full path to the template project.
default gui_template_path = None

init -1 python:

    import gui7
    from gui7 import translate_define, translate_copy, translate_code

    import os

    from store import config

    def translate_font(language, font):
        """
        Selects the font file that is used when translating `language`.

        `font`
            Is the name of the font file used for both the launcher and
            the new GUI template. This should be a string giving the name
            of the font file.
        """

        def callback():
            gui.REGULAR_FONT = font
            gui.LIGHT_FONT = font
            gui.REGULAR_BOLD = True

            style._default.font = font
            style.default.font = font

            gui.system_font = font
            gui.project_system_font = font

        config.language_callbacks[language].append(callback)

        def s(s):
            return '"' + s + '"'

        gui7.translate_copy(language, "sdk-fonts/" + font, font)
        gui7.translate_define(language, "gui.text_font", s(font))
        gui7.translate_define(language, "gui.name_text_font", s(font))
        gui7.translate_define(language, "gui.interface_text_font", s(font))


    for fn in [ "gui.rpy", "options.rpy", "screens.rpy" ]:
        fn = os.path.join(config.renpy_base, "gui", "game", fn)
        if os.path.exists(fn):
            config.translate_files.append(fn)

    config.translate_comments = config.translate_files


    DARK_COLORS = [
        "#0099cc",
        "#99ccff",
        "#66cc00",
        "#cccc00",
        "#cc6600",
        # "#cc3300",

        "#0066cc",
        "#9933ff",
        "#00cc99",
        "#cc0066",
        "#cc0000",
    ]

    LIGHT_COLORS = [
        "#003366", # Dark Blue
        "#0099ff", # Light Blue
        "#336600", # Green
        "#000000", # Black
        "#cc6600", # Orange

        "#000066", # Darkest Blue
        "#660066", # Purple
        "#006666", # Dark Green
        "#cc0066", # Pinkish
        "#990000", # Red
    ]


    # LIGHT_COLORS = DARK_COLORS

    COLOR_OPTIONS = [
        (i, "#000000", False) for i in DARK_COLORS
    ] + [
        (i, "#ffffff", True) for i in LIGHT_COLORS
    ]


screen gui_swatches():

    grid 5 4:

        for accent, bg, light in COLOR_OPTIONS:

            frame:
                style "empty"
                xysize (85, 60)

                add Color(accent).replace_hsv_saturation(.25).replace_value(.5)

                if light:
                    add Color(bg).opacity(.9)
                else:
                    add Color(bg).opacity(.8)

                button:
                    style "empty"

                    if light:
                        selected_background "#000"
                    else:
                        selected_background "#fff"

                    xpadding 3
                    ypadding 3
                    xmargin 10
                    ymargin 10

                    action SetVariable("gui_color", (accent, bg, light))

                    idle_child Solid(accent)
                    hover_child Solid(Color(accent).tint(.6))

screen gui_demo(accent, boring, light, display):

    $ p = gui7.GuiParameters(
        "-",
        "-",
        1280,
        720,
        accent,
        boring,
        light,
        None,
        False,
        False,
        False,
        "-"
    )

    frame:
        style "empty"

        add p.menu_color

        if light:
            add Solid(p.boring_color.opacity(.9))
        else:
            add Solid(p.boring_color.opacity(.8))


        frame:
            style "empty"

            xpadding 10
            ypadding 10

            has vbox

            text _("Display"):
                style "empty"
                font (gui.system_font or "DejaVuSans.ttf")
                color p.accent_color
                size 24

            for i in [ _("Window"), _("Fullscreen"), _("Planetarium") ]:

                textbutton i:
                    action (None if i == "Planetarium" else SetScreenVariable("display", i))
                    style "empty"

                    text_style "empty"
                    text_font (gui.system_font or "DejaVuSans.ttf")
                    text_size 24

                    text_color p.idle_color
                    text_hover_color p.hover_color
                    text_selected_color p.selected_color
                    text_insensitive_color p.insensitive_color

                    xmargin 4
                    ymargin 4
                    left_padding 21

                    selected_background Solid(p.accent_color, xsize=5)

            null height 30

            text _("Text Speed"):
                style "empty"
                color p.accent_color
                size 24
                font (gui.system_font or "DejaVuSans.ttf")

            bar:
                value ScreenVariableValue("value", 1.0)
                style "empty"
                base_bar Solid(p.muted_color)
                hover_base_bar Solid(p.hover_muted_color)

                thumb Solid(p.accent_color, xsize=10)
                hover_thumb Solid(p.hover_color, xsize=10)

                ysize 30


screen choose_gui_color():

    default display = "Window"
    default value = 0.5

    frame:
        style_group "l"
        style "l_root"

        window:
            has vbox

            label _("Select Accent and Background Colors")

            frame:
                style "l_indent"

                has hbox:
                    yfill True

                frame:
                    style "l_default"
                    xsize 425

                    has vbox

                    text _("Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later.")

                    add SPACER

                    use gui_swatches()


                # Preview
                frame:
                    xsize 350

                    style "l_default"
                    background Frame(PATTERN, 0, 0, tile=True)
                    xpadding 5
                    ypadding 5

                    xfill True
                    yfill True
                    xmargin 20
                    bottom_margin 6

                    use gui_demo(gui_color[0], gui_color[1], gui_color[2], display)

    textbutton _("Return") action Jump("front_page") style "l_left_button"

    if gui_color:
        textbutton _("Continue") action Return(True) style "l_right_button"
        key "input_enter" action Return(True)


label change_gui:

    python:

        gui_new = False
        gui_replace_images = True
        gui_update_code = True
        gui_replace_code = False

        project.current.update_dump(True)
        gui_size = tuple(project.current.dump["size"])

        project_dir = project.current.path
        project_name = project.current.name

        mode = interface.choice(
            __("{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?") +
            __("{size=-4}\n\nThis will not overwrite gui/main_menu.png, gui/game_menu.png, and gui/window_icon.png, but will create files that do not exist.{/size}"),
            [
                ("change", _("Choose new colors, then regenerate image files.")),
                ("regenerate",  _("Regenerate the image files using the colors in gui.rpy.")),
            ],
            None,
            cancel=Jump("front_page"),
        )

    if mode == "change":
        jump gui_project_common
    else:
        jump gui_generate_images

label new_gui_project:

    python:
        gui_new = True
        gui_replace_images = True
        gui_replace_code = True
        gui_update_code = True


label gui_project_size:

    python:

        default_size = (1920, 1080)

        gui_size = interface.choice(
            _("What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of [default_size[0]]x[default_size[1]] is a reasonable compromise."),
            [
                ((1280, 720), "1280x720"),
                ((1920, 1080), "1920x1080"),
                ((2560, 1440), "2560x1440"),
                ((3840, 2160), "3840x2160"),
                ("custom", _("Custom. The GUI is optimized for a 16:9 aspect ratio.")),
            ],
            default_size,
            cancel=Jump("front_page"),
        )

        if gui_size == "custom":

            gui_width = ""
            while True:
                gui_width = interface.input(
                    _("WIDTH"),
                    _("Please enter the width of your game, in pixels."),
                    cancel=Jump("front_page"),
                    allow=interface.DIGITS_LETTERS,
                )

                try:
                    gui_width = int(gui_width)
                except Exception:
                    interface.error(_("The width must be a number."), label=None)
                    continue
                break

            gui_height = ""
            while True:
                gui_height = interface.input(
                    _("HEIGHT"),
                    _("Please enter the height of your game, in pixels."),
                    cancel=Jump("front_page"),
                    allow=interface.DIGITS_LETTERS,
                )

                try:
                    gui_height = int(gui_height)
                except Exception:
                    interface.error(_("The height must be a number."), label=None)
                    continue
                break

            gui_size = (gui_width, gui_height)


label gui_project_common:

    $ gui_color = (DARK_COLORS[0], "#000000", False)

    call screen choose_gui_color

    python hide:

        width, height = gui_size
        accent, boring, light = gui_color

        prefix = os.path.join(project_dir, "game")

        if not os.path.isdir(prefix) and not gui_new:
            interface.error("{} does not appear to be a Ren'Py game.".format(prefix))

        template = os.path.join(config.renpy_base, "gui", "game")

        if not os.path.isdir(template):
            interface.error("{} does not appear to be a Ren'Py game.".format(template))

        p = gui7.GuiParameters(
            prefix,
            template,
            width,
            height,
            accent,
            boring,
            light,
            _preferences.language,
            gui_replace_images,
            gui_replace_code,
            gui_update_code,
            project_name,
            )

        if gui_new:
            interface.processing(_("Creating the new project..."))
        else:
            interface.processing(_("Updating the project..."))

        with interface.error_handling(_("creating a new project")):
            gui7.generate_gui(p)

        # Activate the project.
        with interface.error_handling(_("activating the new project")):
            project.manager.scan()
            project.Select(project.manager.get(project_name))()

    if gui_new:

        call update_renpy_strings_common

        python hide:
            if gui.project_system_font:
                with open(os.path.join(project.current.gamedir, "tl/None/common.rpym"), "ab") as f:
                    f.write("define gui.system_font = {!r}\r\n".format(gui.project_system_font).encode("utf-8"))


label gui_generate_images:

    python:

        interface.processing(_("Updating the project..."))
        project.current.launch([ 'gui_images' ], env={ "RENPY_VARIANT" : "small phone" }, wait=True)
        project.current.launch([ 'gui_images' ], wait=True)

    jump front_page

label new_template_project:

    # Unused in new_template_project.
    $ gui_size = (1920, 1080)
    $ gui_color = (DARK_COLORS[0], "#000000", False)

    python hide:

        width, height = gui_size
        accent, boring, light = gui_color

        prefix = os.path.join(project_dir, "game")
        template = os.path.join(gui_template_path, "game")

        # Most of this isn't actually used.
        p = gui7.GuiParameters(
            prefix,
            template,
            width,
            height,
            accent,
            boring,
            light,
            _preferences.language,
            False,
            True,
            True,
            project_name,
            )

        interface.processing(_("Creating the new project..."))

        with interface.error_handling(_("creating a new project")):
            gui7.generate_minimal(p)

        # Activate the project.
        with interface.error_handling(_("activating the new project")):
            project.manager.scan()
            project.Select(project.manager.get(project_name))()

    call update_renpy_strings_common

    python hide:
        if gui.project_system_font:
            with open(os.path.join(project.current.gamedir, "tl/None/common.rpym"), "ab") as f:
                f.write("define gui.system_font = {!r}\r\n".format(gui.project_system_font).encode("utf-8"))

    jump front_page
