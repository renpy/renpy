# Copyright 2004-2016 Tom Rothamel <pytom@bishoujo.us>
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

import os
import codecs
import re
import math

class CodeGenerator(object):
    """
    This is used to generate and update the GUI code.
    """

    def __init__(self, parameters, template, overwrite):
        """
        Generates or updates gui.rpy.
        """

        self.p = parameters
        self.template = template
        self.overwrite = overwrite

        self.target = os.path.join(self.p.prefix, "gui.rpy")

    def load_template(self):

        if os.path.exists(self.target) and not self.overwrite:
            template = self.target
        else:
            template = self.template

        with codecs.open(template, "r", "utf-8") as f:
            self.lines = [ i.rstrip() for i in f ]

    def remove_scale(self):

        def scale(m):
            original = int(m.group(1))
            scaled = int(math.ceil(original * self.p.scale))
            return str(scaled)


        lines = [ ]

        for l in self.lines:
            l = re.sub(r'gui.scale\((.*?)\)', scale, l)
            lines.append(l)

        self.lines = lines

    def write_target(self):

        if os.path.exists(self.target):
            backup = 1

            while True:

                bfn = "{}.{}.bak".format(self.target, backup)

                if not os.path.exists(bfn):
                    break

                backup += 1

            os.rename(self.target, bfn)


        with codecs.open(self.target, "w", "utf-8") as f:
            for l in self.lines:
                f.write(l + "\r\n")


    def generate(self):
        self.load_template()
        self.remove_scale()
        self.write_target()
