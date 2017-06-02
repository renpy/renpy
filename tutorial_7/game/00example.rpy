python early:

    # This maps from example name to the text of a fragment.
    examples = { }

    # The size of the example - large or small.
    example_size = "small"

    # The location of the example - top or bottom.
    example_location = "top"

    def reset_example():
        """
        Called to reset the example code to the defaults.
        """

        global example_size
        global example_location

        example_size = "small"
        example_location = "top"


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

    def read_example(name, fn, line):
        """
        This reads an example from an example statement, and places it into
        the examples dictionary.
        """

        fn = fn.replace("game/", "")

        with renpy.file(fn) as f:
            data = f.read()

        lines = [ i.rstrip() for i in data.split("\n") ]

        rv = [ ]

        base_indent = 0

        while True:
            l = lines[line]
            line += 1

            if not l:
                rv.append(l)
                continue

            indent = len(l) - len(l.lstrip())

            if base_indent == 0:
                base_indent = indent
                rv.append(l[4:])
            elif indent >= base_indent:
                rv.append(l[4:])
            else:
                break

        if name in examples:
            examples[name].append('')
            examples[name].extend(rv)
        else:
            examples[name] = rv

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

            else:

                if name:
                    l.error('an example may have at most one name')

                name = l.require(l.name)

        l.expect_eol()

        if name is None:
            name = "example_{}_{}".format(l.filename, l.number)

        return { "name" : name, "names" : [ name ], "hide" : hide, "bottom" : bottom, "small" : small, "filename" : l.filename, "number" : l.number, "top" : top, "large" : large }

    def next_example(data, first):
        return first

    def execute_example(data):
        names = data.get("names", [ ])
        hide = data.get("hide", False)
        bottom = data.get("bottom", False)
        small = data.get("small", False)
        top = data.get("top", False)
        large = data.get("large", False)

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

        if hide:
            return

        renpy.show_screen("example", names, example_size == "small", example_location == "bottom")

    def execute_init_example(data):
        read_example(data["name"], data["filename"], data["number"])

    renpy.register_statement("example", parse=parse_example, execute=execute_example, execute_init=execute_init_example, next=next_example, block="script")



    # The show example statement.

    def parse_show_example(l):

        names = [ ]


        bottom = False
        small = False
        top = False
        large = False

        while not l.eol():

            if l.keyword('bottom'):
                bottom = True

            elif l.keyword('small'):
                small = True

            elif l.keyword('top'):
                top = True

            elif l.keyword('large'):
                large = True

            else:

                names.append(l.require(l.name))

        return { "names" : names, "hide" : False, "bottom" : bottom, "small" : small, "top" : top, "large" : large }

    renpy.register_statement("show example", parse=parse_show_example, execute=execute_example)


    # The hide example statement.

    def parse_hide_example(l):

        l.expect_eol()

        return { }

    def execute_hide_example(data):
        renpy.hide_screen("example")

    renpy.register_statement("hide example", parse=parse_hide_example, execute=execute_hide_example)



init python:

    import re
    import keywords

    KEYWORDS = set(keywords.keywords)
    PROPERTIES = set(keywords.properties)

    KEYWORDS = [ re.escape(i) for i in keywords.keywords ]
    PROPERTIES = [ re.escape(i) for i in keywords.properties ]
    KWREGEX = r"|".join(KEYWORDS)
    PRREGEX = r"|".join(PROPERTIES)

    regex = r"(?P<word>\b(\$|\w+)\b)" + \
        r"|(?P<string>\"([^\"]|\\.)*\")" + \
        r"|(?P<comment>#.*)"
    regex = re.compile(regex)

    def quote(s):
        s = s.replace("{", "{{")
        s = s.replace("[", "[[")

        return s

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

    def example_code(blocks, raw=False):

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


screen example(blocks, small=False, bottom=False):

    zorder 10

    default raw_code = example_code(blocks, raw=True)
    default code = example_code(blocks)

    if small:
        $ height = 80
    else:
        $ height = 160

    if bottom:
        $ ypos = 720
    else:
        $ ypos = 540


    window:
        style "empty"
        background "#fffc"
        foreground Solid("#aaac", xsize=1, xpos=178)
        left_padding 180
        right_padding 2

        xfill True
        yfill True
        ymaximum height

        at example_transform(height, ypos)

        viewport:
            child_size (2000, 2000)
            ymaximum height
            draggable True
            mousewheel True
            scrollbars "vertical"

            vscrollbar_xsize 5
            vscrollbar_base_bar "#aaac"
            vscrollbar_unscrollable "hide"

            text code:
                size 16
                color "#000"

        textbutton _("Copy"):
            ypos 0
            xalign 0.0

            xpos 0
            xanchor 0.5
            xoffset -90
            yoffset -8
            text_size 14

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
