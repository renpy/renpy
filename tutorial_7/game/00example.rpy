

# This defines the example statement.
#
# The example statement takes:
# * An optional name for the example.
# * An optional hide flag.
# * An optional size/position flag, which can be either bottom or small.
#
# The statement defines an example with the name, or an anyonymous name if no
# name is given. When run, the example is displayed if the hide flag is not
# given. Bottom and small determine if the example is displayed at the bottom
# of the screen or at half height.

python early:


    # This maps from example name to the text of a fragment.
    examples = { }


    def read_example(name, fn, line):
        """
        This reads an example from an example statement, and places it into
        the examples dictionary.
        """

        if name in examples:
            return

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

        while l:

            if l.match(':'):
                break

            elif l.keyword('hide'):
                hide = True

            elif l.keyword('bottom'):
                bottom = True

            elif l.keyword('small'):
                small = True

            else:

                if name:
                    l.error('an example may have at most one name')

                name = l.require(l.name)

        l.expect_eol()

        if name is None:
            name = "example_{}_{}".format(l.filename, l.number)

        read_example(name, l.filename, l.number)
        return { "name" : name, "hide" : hide, "bottom" : bottom, "small" : small }

    def next_example(data, first):
        return first

    def execute_example(data):
        name = data.get("name", None)
        hide = data.get("hide", False)
        bottom = data.get("bottom", False)
        small = data.get("small", False)

        if hide:
            return

        if bottom:
            tf = example_bottom
        else:
            tf = example_transform

        renpy.show_screen("example", name, tf)

    renpy.register_statement("example", parse=parse_example, execute=execute_example, next=next_example, block="script")


# These determine the height of the examples.
define EXAMPLE_HEIGHT = 160

# These transforms control the placement of the example on the screen, and
#
transform example_transform:
    ypos 540 yanchor 1.0
    xalign 0.5

    on replace:
        crop (0, 0, 1280, EXAMPLE_HEIGHT)

    on show:
        crop (0, 0, 1280, 0)
        linear .5 crop (0, 0, 1280, EXAMPLE_HEIGHT)

    on hide:
        linear .5 crop (0, 0, 1280, 0)


transform example_bottom:
    ypos 720 yanchor 1.0
    xalign 0.5

    on replace:
        crop (0, 0, 1280, EXAMPLE_HEIGHT)

    on show:
        crop (0, 0, 1280, 0)
        linear .5 crop (0, 0, 1280, EXAMPLE_HEIGHT)

    on hide:
        linear .5 crop (0, 0, 1280, 0)

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

    def example_code(blocks, raw=False):

        if not isinstance(blocks, list):
            blocks = [ blocks ]


        # Collect the examples we use.
        lines1 = [ ]

        for i in blocks:
            if i not in examples:
                raise Exception("Unknown example %r." % i)
            lines1.extend(examples[i])
            lines1.append('')


        # Strip off doubled blank lines.
        last_blank = False
        lines = [ ]

        for i in lines1:

            if not i and last_blank:
                continue

            last_blank = not i

            if not raw:
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


screen example(blocks, transform_=example_transform):

    zorder 10

    default raw_code = example_code(blocks, raw=True)
    default code = example_code(blocks)

    window:
        style "empty"
        background "#fffc"
        left_padding 180
        xfill True
        yfill True
        ymaximum EXAMPLE_HEIGHT

        at transform_

        viewport:
            child_size (2000, 2000)
            ymaximum EXAMPLE_HEIGHT
            draggable True
            mousewheel True

            text code:
                size 16
                color "#000"

        textbutton _("Copy"):
            ypos 0
            xalign 1.0
            xoffset -5
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
