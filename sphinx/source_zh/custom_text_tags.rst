.. _custom-text-tags:

================
Custom Text Tags
================

Ren'Py has support for defining your own text tags. These text tags
can manipulate the text and text tags defined within, including adding
and removing text and other text tags.

Custom text tags are created by assigning a text tag function to an
entry in the config.custom_text_tags dictionary.

.. var:: config.custom_text_tags

    Maps text tag names to text tag functions.

A text tag function takes three arguments: The tag itself, the argument
for the tag, and a list of content tuples. For example, for the text::

    "{big=2}Hello, {b}World{/b}{/big}"

The tag will be "big", the argument will be the string "2", and the list
of content tuples will be::

    [
        (renpy.TEXT_TEXT, "Hello, "),
        (renpy.TEXT_TAG, "b"),
        (renpy.TEXT_TEXT, "World"),
        (renpy.TEXT_TAG, "/b"),
    ]

The text tag function should return a new list of content tuples, which
is used to replace the text tag and its contents.

Content tuples consist of two components. The first component is one of the
the constants in the following list. The second component varies based on
the first component, as describe below.

renpy.TEXT_TEXT

    The second component is text that is intended for display to the user.

renpy.TEXT_TAG

    The second component is the contents of a text tag, without the
    enclosing braces.

renpy.TEXT_DISPLAYABLE

    The second component is a displayable to be embedded into the text.

renpy.TEXT_PARAGRAPH

    This represents a break between paragraphs, and the second component
    is undefined (but must be present).

Caveats
-------

The dialogue text tags {p}, {w}, {nw}, and {fast} are processed before
custom text tags, and should either be not included inside a custom
text tag, or passed through unchanged.

Examples
--------

The example big text tag works like the {size} text tag, but applies a
multiplier to its argument. ::

    init python:

        def big_tag(tag, argument, contents):

            size = int(argument) * 20

            return [
                    (renpy.TEXT_TAG, u"size={}".format(size)),
                ] + contents + [
                    (renpy.TEXT_TAG, u"/size"),
                ]

        config.custom_text_tags["big"] = big_tag


    "This is {big=3}BIG!{/big}"

The example rot13 text tag applies the rot13 transform to text. Note that
rot26 - rot13 applied twice - is just normal text. ::

    init python:

        def rot13_tag(tag, argument, contents):
            rv = [ ]

            for kind, text in contents:

                if kind == renpy.TEXT_TEXT:
                    text = text.encode("rot13")

                rv.append((kind, text))

            return rv

        config.custom_text_tags["rot13"] = rot13_tag

    "Rot0. {rot13}Rot13. {rot13}Rot26. {/rot13}Rot13. {/rot13}Rot0."
