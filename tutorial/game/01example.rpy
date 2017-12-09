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
