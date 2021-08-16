python early:

    # This maps from example name to the text of a fragment.
    examples = { }

    # The size of the example - large or small.
    example_size = "small"

    # The location of the example - top or bottom.
    example_location = "top"

    # The screen in the last example.
    example_screen = None

    # A transition used with examples
    example_transition = None

    def reset_example():
        """
        Called to reset the example code to the defaults.
        """

        global example_size
        global example_location
        global example_screen

        example_size = "small"
        example_location = "top"
        example_screen = None

    def show_example_screen(name):
        global example_screen
        example_screen = name
        renpy.show_screen(name)

    def hide_example_screen():
        global example_screen

        if example_screen is not None:
            renpy.hide_screen(example_screen)

        example_screen = None


    # Keywords that, at the start of an example block, cause it to be
    # outdented
    OUTDENT_KEYWORDS = { "define", "default", "image", "screen", "init", "transform", "label", "style" }


    # This defines the example statement.
    #
    # The example statement takes:
    # * An optional name for the example.
    # * An optional hide flag.
    # * Optional size flags, large or small.
    # * Optional position flags, top or bottom.
    #
    # The statement defines an example with the name, or an anyonymous name if no
    # name is given. When run, the example is displayed if the hide flag is not
    # given.


    def read_example(name, fn, line, outdent):
        """
        This reads an example from an example statement, and places it into
        the examples dictionary.
        """

        fn = fn.replace("game/", "")

        with renpy.notl_file(fn) as f:
            data = f.read()

        rawlines = [ i.rstrip() for i in data.split("\n") ]

        lines = [ ]

        base_indent = 0

        while True:

            if line >= len(rawlines):
                raise Exception("Example open at end of {}.".format(fn))

            l = rawlines[line]
            line += 1

            if not l:
                lines.append(l)
                continue

            indent = len(l) - len(l.lstrip())

            if base_indent == 0:
                base_indent = indent
                lines.append(l[4:])
            elif indent >= base_indent:
                lines.append(l[4:])
            else:
                break

        # Determine if the line should be indented.
        if outdent == "auto":

            for i in lines:
                l = i.strip().split()
                if not l:
                    continue

                if l[0] in OUTDENT_KEYWORDS:
                    outdent = True
                else:
                    outdent = False

                break

        # Strip indentation.
        if outdent:
            lines = [ i[base_indent - 4:] for i in lines ]

        if name in examples:
            examples[name].append('')
            examples[name].extend(lines)
        else:
            examples[name] = lines

    def parse_example(l):
        """
        This parses the example statement.
        """

        # The name of the example. A string, or None if we don't know yet.
        name = None

        # Hide, bottom, and small flags.
        hide = False
        bottom = False
        small = False
        top = False
        large = False
        outdent = "auto"
        show_screen = True
        hide_screen = True
        showtrans = False

        while True:

            if l.match(':'):
                break

            elif l.keyword('hide'):
                hide = True

            elif l.keyword('bottom'):
                bottom = True

            elif l.keyword('small'):
                small = True

            elif l.keyword('top'):
                top = True

            elif l.keyword('large'):
                large = True

            elif l.keyword('outdent'):
                outdent = True

            elif l.keyword('nooutindent'):
                outdent = False

            elif l.keyword("noshow"):
                show_screen = False

            elif l.keyword("nohide"):
                hide_screen = False

            elif l.keyword("showtrans"):
                showtrans = True

            else:

                if name:
                    l.error('an example may have at most one name')

                name = l.require(l.name)

        l.expect_eol()

        if name is None:
            name = "example_{}_{}".format(l.filename, l.number)

        ll = l.subblock_lexer()
        ll.advance()

        if ll.keyword('screen'):
            screen_name = ll.name()
        else:
            screen_name = None

        return {
            "name" : name,
            "names" : [ name ],
            "hide" : hide,
            "bottom" : bottom,
            "small" : small,
            "filename" : l.filename,
            "number" : l.number,
            "top" : top,
            "large" : large,
            "outdent" : outdent,
            "screen_name" : screen_name,
            "show_screen" : show_screen,
            "hide_screen" : hide_screen,
            "showtrans" : showtrans,
            }

    def next_example(data, first):
        return first

    def execute_example(data):
        names = data.get("names", [ ])
        hide = data.get("hide", False)
        bottom = data.get("bottom", False)
        small = data.get("small", False)
        top = data.get("top", False)
        large = data.get("large", False)
        showtrans = data.get("showtrans", False)

        global example_location
        global example_size


        if bottom:
            example_location = "bottom"
        elif top:
            example_location = "top"

        if small:
            example_size = "small"
        elif large:
            example_size = "large"

        if not hide:
            renpy.show_screen("example", names, example_size == "small", example_location == "bottom", showtrans=showtrans)

        screen_name = data.get("screen_name", None)

        if screen_name is not None:
            if data.get("hide_screen", True):
                hide_example_screen()

            if data.get("show_screen", True):
                show_example_screen(screen_name)
                renpy.with_statement(example_transition)

    def execute_init_example(data):
        read_example(data["name"], data["filename"], data["number"], data.get("outdent", "auto"))

    renpy.register_statement("example", parse=parse_example, execute=execute_example, execute_init=execute_init_example, next=next_example, block="script")


    # The show example statement.

    def parse_show_example(l):

        names = [ ]

        bottom = False
        small = False
        top = False
        large = False
        showtrans = False

        while not l.eol():

            if l.keyword('bottom'):
                bottom = True

            elif l.keyword('small'):
                small = True

            elif l.keyword('top'):
                top = True

            elif l.keyword('large'):
                large = True

            elif l.keyword('showtrans'):
                showtrans = True

            else:

                names.append(l.require(l.name))

        return {
            "names" : names,
            "hide" : False,
            "bottom" : bottom,
            "small" : small,
            "top" : top,
            "large" : large,
            "showtrans" : showtrans,
            }

    renpy.register_statement("show example", parse=parse_show_example, execute=execute_example)


    # The hide example statement.

    def parse_hide_example(l):

        hide_screen = True

        while not l.eol():
            if l.keyword('nohide'):
                hide_screen = False
            else:
                break

        l.expect_eol()

        return {
            "hide_screen" : hide_screen,
        }

    def execute_hide_example(data):
        renpy.hide_screen("example")

        if example_screen and data.get("hide_screen", True) and renpy.get_screen(example_screen):
            hide_example_screen()
            renpy.with_statement(example_transition)

    renpy.register_statement("hide example", parse=parse_hide_example, execute=execute_hide_example)


# A preference that controls if translations are shown.
define persistent.show_translation_marker = False

init python:

    dialogue_map = { }

    for i in renpy.known_languages():
        dialogue_map[i] = renpy.translation.dialogue.create_dialogue_map(i)


    import re
    import keywords

    KEYWORDS = set(keywords.keywords)
    PROPERTIES = set(keywords.properties)

    regex = r"(?P<word>\b(\$|[_a-zA-Z0-9]+)\b)" + \
        r"|(?P<string>\"([^\"]|\\.)*(?<!\\)\")" + \
        r"|(?P<comment>#.*)"

    regex = re.compile(regex)

    def quote(s):
        s = s.replace("{", "{{")
        s = s.replace("[", "[[")

        return s

    def translate(m):
        if m.group("string"):
            s = eval(m.group(0))

            if __(s) != s:
                s = __(s)
            elif _preferences.language:

                dm = dialogue_map[_preferences.language]

                if s in dm:
                    s = dm[s]

            quote = m.group(0)[0]
            s = s.replace("\\", "\\\\")
            s = s.replace(quote, "\\" + quote)
            s = s.replace("\n", "\\n")
            s = quote + s + quote

            return s

        return m.group(0)

    def colorize(m):
        if m.group("string"):
            return "{color=#060}" + m.group(0) + "{/color}"

        word = m.group("word")
        if word:
            if word in KEYWORDS:
                return "{color=#840}" + m.group(0) + "{/color}"
            elif word in PROPERTIES:
                return "{color=#048}" + m.group(0) + "{/color}"
            else:
                return m.group(0)

        if m.group("comment"):
            return "{color=#600}" + m.group(0) + "{/color}"

        return m.group(0)

    def clean_example(lines):
        rv = list(lines)

        while rv and not rv[0]:
            rv.pop(0)

        while rv and not rv[-1]:
            rv.pop(-1)

        return rv

    def example_code(blocks, raw=False, showtrans=False):

        if not isinstance(blocks, list):
            blocks = [ blocks ]


        # Collect the examples we use.
        lines1 = [ ]

        for i in blocks:
            if i not in examples:
                lines1.append('Example {} not found.'.format(i))
            else:
                lines1.extend(clean_example(examples[i]))

            lines1.append('')


        # Strip off doubled blank lines.
        last_blank = False
        lines = [ ]

        for i in lines1:

            if not i and last_blank:
                continue

            last_blank = not i

            if not raw:
                i = regex.sub(translate, i)

                if not (persistent.show_translation_marker or showtrans):
                    i = re.sub(r'__?\((".*?")\)', r'\1', i)
                    i = re.sub(r"__?\(('.*?')\)", r'\1', i)
                    i = i.replace("!t]", "]")

                i = quote(i)
                i = regex.sub(colorize, i)

            lines.append(i)

        while not lines[-1]:
            lines.pop()

        # Join them into a single string.
        return "\n".join(lines) + "\n "

    class CopyCode(Action):
        def __init__(self, s):
            self.s = s

        def __call__(self):
            import pygame.scrap
            pygame.scrap.put(pygame.SCRAP_TEXT, self.s.encode("utf-8"))
            renpy.notify(_("Copied the example to the clipboard."))

    example_transition = dissolve

    import os
    SHOW_EXAMPLES = ("RENPY_LESS_EXAMPLES" not in os.environ)


transform example_transform(height, ypos):
    ypos ypos
    yanchor 1.0
    xalign 0.5

    on replace:
        crop (0, 0, 1280, height)

    on show:
        crop (0, 0, 1280, 0)
        linear .5 crop (0, 0, 1280, height)

    on hide:
        linear .5 crop (0, 0, 1280, 0)


screen example(blocks, small=False, bottom=False, showtrans=False):

    zorder 10

    default raw_code = example_code(blocks, raw=True, showtrans=showtrans)
    default code = example_code(blocks, showtrans=showtrans)

    if small:
        $ height = 80
    else:
        $ height = 160

    if bottom:
        $ ypos = 720
    else:
        $ ypos = 540


    if SHOW_EXAMPLES:

        frame:
            style "empty"
            background "#fffc"
            foreground Solid("#aaac", xsize=1, xpos=178)

            xfill True
            yfill True
            ymaximum height

            at example_transform(height, ypos)

            viewport:
                side_xmaximum 1098
                side_xpos 180
                child_size (2000, 2000)
                ymaximum height
                draggable True
                mousewheel True
                scrollbars "vertical"

                vscrollbar_xsize 5
                vscrollbar_base_bar "#aaac"
                vscrollbar_unscrollable "hide"

                text code:
                    alt ""
                    size 16
                    color "#000"

            textbutton _("copy"):
                style "empty"
                text_style "quick_button_text"
                text_text_align 0.5
                text_minwidth 180

                text_size 16

                action CopyCode(raw_code)




init python hide:

    import os.path
    import re

    # A list of files we will be scanning.
    files = [ ]

    for i in os.listdir(config.gamedir):
        if i.endswith(".rpy"):
            files.append(os.path.join(config.gamedir, i))

    for fn in files:

        f = file(fn, "r")

        open_examples = set()

        for l in f:

            l = l.decode("utf-8")
            l = l.rstrip()

            m = re.match("\s*#begin (\w+)", l)
            if m:
                example = m.group(1)

                if example in examples:
                    raise Exception("Example %r is defined in two places.", example)

                open_examples.add(example)
                examples[example] = [ ]

                continue

            m = re.match("\s*#end (\w+)", l)
            if m:
                example = m.group(1)

                if example not in open_examples:
                    raise Exception("Example %r is not open.", example)

                open_examples.remove(example)
                continue

            for i in open_examples:
                examples[i].append(l)

        if open_examples:
            raise Exception("Examples %r remain open at the end of %r" % (open_examples, fn))

        f.close()



init python:

    def lint_stats_callback():
        print("The game contains {} examples.".format(len(examples)))

    config.lint_stats_callbacks.append(lint_stats_callback)

    import base64

image _finaleimage = im.Data(base64.b64decode("""
    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
    """), "finale.png")


image _finale:
    "_finaleimage"
    yalign 0.3
    xanchor 1.0 xpos 0.0
    pause 90.0
    easein 1.5 xanchor 0.0 xpos .25
    pause 3.0
    easeout 1.5 xanchor 1.0 xpos 0.0
    repeat
