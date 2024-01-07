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

label add_file:

    python hide:
        import os
        filename = ""
        while True:
            filename = interface.input(
                _("FILENAME"),
                _("Enter the name of the script file to create."),
                allow=interface.FILENAME_LETTERS,
                cancel=Jump("navigation"),
                default=filename,
            )
            filename = filename.strip()
            if not filename:
                interface.error(_("The file name may not be empty."), label=None)
                continue

            if "." in filename and not filename.endswith(".rpy"):
                interface.error(_("The filename must have the .rpy extension."), label=None)
                continue
            elif "." not in filename:
                filename += ".rpy"

            path = os.path.join(project.current.gamedir, filename)
            dir = os.path.dirname(path)

            if os.path.exists(path):
                interface.error(_("The file already exists."), label=None)
                continue

            break

        try:
            os.makedirs(dir)
        except Exception:
            pass

        contents = u"\uFEFF"
        contents += _("# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n")

        with open(path, "wb") as f:
            f.write(contents.encode("utf-8"))

    jump navigation_refresh
