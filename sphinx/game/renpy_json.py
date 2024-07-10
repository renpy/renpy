import argparse
import os
import re
import json

SPHINX = os.path.abspath(os.path.dirname(__file__) + "/..")

DEPRECATED = [
    "ui."
    "im."
]

NOT_DEPRECATED = [
    "ui.interact",
    "ui.adjustment",
    "im.Data",
]

class LineIterator:

    def __init__(self, filename):
        self.lines = [ ]

        self.add_lines(0, filename)

        self.skip_next = False

    def add_lines(self, indent, filename):
        """
        Breaks a file up into (indent, line) pairs. This handles includes
        and blank lines.
        """

        filename = SPHINX + "/source/" + filename

        last_indent = 0

        with open(filename, 'r') as f:

            for l in f:
                l = l.rstrip()
                line = l.lstrip(' ')

                if not line:
                    self.lines.append((last_indent, ''))
                    continue

                new_indent = indent + len(l) - len(line)

                if line.startswith('.. include::'):
                    self.add_lines(new_indent, line.split(None, 2)[2])
                    continue

                self.lines.append((new_indent, line))

                last_indent = new_indent

    def next(self):
        """
        Updates the line iterator to refer to the next line. Returns True if there is a next line, or
        false if this is the last line in the file.
        """

        if self.skip_next:
            self.skip_next = False
            return True

        if self.lines:
            self.indent, self.line = self.lines.pop(0)
            return True
        else:
            return False

    def skip(self):
        """
        Skips the next call to .next().
        """

        self.skip_next = True


def early_substitutions(s):
    """
    Substitutions that are performed on a line before it's checked to see if
    it contains code.
    """

    s = s.replace(".. warning::", "**Warning:**")
    s = s.replace(".. note::", "**Note:**")
    s = s.replace(".. seealso::", "See also:")
    s = s.replace(".. attribute::", "attribute")

    return s


def rst_to_markdown(s):
    """
    Converts a reStructuredText string to a Markdown string.
    """

    # Replaces :kind:`code` with `code`.
    s = re.sub(r':\w+:`(.*?)\s*(<.*?>)?`', r'\1', s)

    return s

class Documentation:

    def __init__(self):
        self.renpy = { }
        self.config = { }
        self.internal = { }

        for i in os.listdir(SPHINX + "/source"):
            if i.endswith(".rst"):
                basename = i[:-4]
                li = LineIterator(i)
                self.parse_file(basename, li)

    def parse_file(self, basename, li):
        """
        Parses a file and updates the documentation with the contents.

        `basename`
            The basename of the file, without the extension. This isn't currently used, but
            passed around in case we want to link to Sphinx documentation.

        `li`
            A LineIterator object that provides the lines of the file.
        """

        while li.next():


            m = re.match(r'..\s*(\w+)::\s*([\.\w]+)(.*)', li.line)

            if m and m.group(1) in { "function", "class", "var" }:
                self.parse_name(basename, m.group(1), m.group(2), m.group(3), li)


    def parse_name(self, basename, kind, name, rest, li):
        """
        Parses a name declaration.

        `basename`
            The basename of the file, without the extension.

        `kind`
            The kind of the declaration. This is one of "function", "class", or "var".

        `name`
            The name of the declaration.

        `rest`
            The rest of the declaration line.
        """

        indent = None

        body = ""

        while li.next():

            if indent is None:
                if not li.line:
                    continue
                indent = li.indent

            if li.indent < indent:
                li.skip()
                break

            # Look for :: starting a code block.
            line = li.line

            line = early_substitutions(line)

            if line.endswith("::"):
                line = line[:-2]
                code = True
            else:
                code = False

            line = rst_to_markdown(line)
            body += line + "\n"

            # Handle the code block.
            if code:

                body += "\n"
                body += "```\n"

                # Skip blank lines.
                while li.next():
                    if li.line:
                        li.skip()
                        break

                code_indent = li.indent

                while li.next():
                    if li.indent < code_indent:
                        li.skip()
                        break

                    body += " " * (li.indent - code_indent) + li.line + "\n"

                body += "```\n"
                body += "\n"

        self.output(basename, kind, name, rest, body)

    def output(self, basename, kind, name, rest, body):
        """
        Outputs a declaration to the appropriate dictionary.

        `basename`
            The basename of the file, without the extension.

        `kind`
            The kind of the declaration. This is one of "function", "class", or "var".

        `name`
            The name of the declaration.

        `rest`
            The rest of the declaration line.

        `body`
            The body of the declaration.
        """

        accessKind = kind

        origin = "renpy"

        for i in DEPRECATED:
            if name.startswith(i):
                origin = "deprecated"

        for i in NOT_DEPRECATED:
            if name == "i":
                origin = "renpy"

        entry = [
            origin,
            kind,
            rest.strip(),
            "",
            accessKind,
            body
        ]

        if basename == 'config':
            self.config[name] = entry
        else:
            self.renpy[name] = entry

def main():

    d = Documentation()

    def sort(d):
        return { k: d[k] for k in sorted(d) }

    renpy_json = {
        "config": sort(d.config),
        "renpy": sort(d.renpy),
        "internal": sort(d.internal),
    }

    with open(SPHINX + "/renpy.json", "w") as f:
        json.dump(renpy_json, f, indent=2)


if __name__ == '__main__':
    main()
