# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

# Other text-related things.

import renpy.text

from renpy.text.textsupport import TAG
import renpy.text.textsupport as textsupport


# A list of text tags, mapping from the text tag prefix to if it
# requires a closing tag.
text_tags = dict(
    image=False,
    p=False,
    w=False,
    fast=False,
    b=True,
    i=True,
    u=True,
    a=True,
    plain=True,
    font=True,
    color=True,
    size=True,
    nw=False,
    s=True,
    rt=True,
    rb=True,
    k=True,
    cps=True,
    space=False,
    vspace=False
    )

text_tags[""] = True


# This checks the text tags in a string to be sure they are all matched, and
# properly nested. It returns an error message, or None if the line is okay.
def check_text_tags(s):
    """
    :doc: lint

    Checks the text tags in s for correctness. Returns an error string if there is
    an error, or None if there is no error. 
    """

    tokens = textsupport.tokenize(unicode(s))

    tag_stack = [ ]

    for type, text in tokens: #@ReservedAssignment
        if type != TAG:
            continue

        if text[0] == "#":
            continue

        # Strip off arguments for tags.
        if text.find('=') != -1:
            text = text[:text.find('=')]

        # Closing tag.
        if text and text[0] == '/':
            if not tag_stack:
                return "Close text tag '%s' does not match an open text tag." % text

            if tag_stack[-1] != text[1:]:
                return "Close text tag '%s' does not match open text tag '%s'." % (text, tag_stack[-1])

            tag_stack.pop()
            continue

        if text not in text_tags:
            return "Text tag '%s' is not known." % text

        if text_tags[text]:
            tag_stack.append(text)

    if tag_stack:
        return "One or more text tags were left open at the end of the string: " + ", ".join([ "'" + i + "'" for i in tag_stack])

    return None


class ParameterizedText(object):
    """
    This can be used as an image. When used, this image is expected to
    have a single parameter, a string which is rendered as the image.
    """

    def __init__(self, style='default', **properties):
        self.style = style
        self.properties = properties

    def parameterize(self, name, parameters):

        if len(parameters) != 1:
            raise Exception("'%s' takes a single string parameter." %
                            ' '.join(name))

        param = parameters[0]
        string = renpy.python.py_eval(param)

        return renpy.text.text.Text(string, style=self.style, **self.properties)
