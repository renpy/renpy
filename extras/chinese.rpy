# This file contains code to do chinese word-wrapping. It's based
# on what I gathered from the information found at:
#
# http://lemmasoft.renai.us/forums/viewtopic.php?p=9282#9282

init:

    # You'll probably want to replace this with whatever you consider
    # to be punctuation. I've used unicode escapes for many of the
    # fullwidth characters, as I don't know how to type them otherwise.
    $ chinese_punctuation = u";,.?\uff1b\uff1a\uff0c\u3002\u3001\uff1f\uff01"

    python hide:
        
        def text_tokenizer(s, style):
            """
            This functions is used to tokenize text. It's called when laying
            out a Text widget, and is given the string that is the text of the
            widget, and the style associated with the widget.

            It's expected to yield some number of pairs. In each pair, the
            first element is the kind of token found, and the second element
            is the text corresponding to that token. The following token
            types are defined:

            "newline" -- A newline, which when encountered starts a new line.

            "word" -- A word of text. A line will never be broken inside of
            a word.

            "space" -- A space. Spaces are always placed on the current line,
            and will never be placed as the start of a line.

            "tag" -- A text tag. If encountered, the second element should be
            the name of the tag, without any enclosing braces.
            """

            regexp = r"""(?x)
              (?P<space>\ )
            | \{(?P<tag>[^{}]+)\}
            | (?P<untag>\{\{)
            | (?P<newline>\n)
            | (?P<word>[^ \n\{][%s]*)
            """ % chinese_punctuation

            import re

            for m in re.finditer(regexp, s):

                if m.group('space'):
                    yield 'space', m.group('space')
                elif m.group('word'):
                    yield 'word', m.group('word')
                elif m.group('tag'):
                    yield 'tag', m.group('tag')
                elif m.group('untag'):
                    yield 'word', '{'
                elif m.group('newline'):
                    yield 'newline', m.group('newline')

        config.text_tokenizer = text_tokenizer
        
