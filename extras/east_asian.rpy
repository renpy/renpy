# This file contains code to do east asian word-wrapping. It's based
# on what I gathered from the information found at:
#
# http://lemmasoft.renai.us/forums/viewtopic.php?p=9282#9282
#
# It was then further enhanced with the information found at:
#
# http://zoonek.free.fr/LaTeX/Omega-Japanese/doc.html
#
# I'd expect it to do a decent job with Chinese and Japanese, but
# I have no idea how it does with Korean. If someone wants to clue
# me in, I'd be happy to hear more about it.

init:
    python hide:

        # These are characters for which line breaking is forbidden before them.
        # In our algorithm, they try to cling to the back of a word.
        not_before = ur'\!\"\%\)\,\-\.\:\;\?\]\}\u2010\u2019\u201d\u2030\u2032\u2033\u2103\u2212\u3001\u3002\u3005\u3009\u300b\u300d\u300f\u3011\u3015\u3017\u3041\u3043\u3045\u3047\u3049\u3063\u3083\u3085\u3087\u308e\u309b\u309c\u309d\u309e\u30a1\u30a3\u30a5\u30a7\u30a9\u30c3\u30e3\u30e5\u30e7\u30ee\u30f5\u30f6\u30fc\u30fd\u30fe\uff01\uff02\uff05\uff09\uff09\uff0c\uff0d\uff0e\uff1a\uff1b\uff1f\uff3d\uff5d\uff5d\uff61\uff63\uff9e\uff9f'


        # These are characters for which line breaking is forbidden after them.
        # In our algorithm, they try to cling to the front of a word.
        not_after = ur'\"\#\$\(\@\[\{\xa2\xa3\xa5\xa7\u2018\u201c\u266f\u3008\u300a\u300c\u300e\u3010\u3012\u3014\u3016\uff03\uff04\uff08\uff08\uff20\uff3b\uff5b\uff5b\uff62\uffe0\uffe1\uffe5'


        # These are ranges of characters that are treated as western. (And hence are always grouped
        # together as a word.
        western = ur'\'\w\u000a-\u0024f\uff10-\uff19\uff20-\uff2a\uff41-\uff5a'

        regexp = ur"""(?x)
          (?P<space>[ \u200b])
        | \{(?P<tag>[^{}]+)\}
        | (?P<untag>\{\{)
        | (?P<newline>\n)
        | (?P<word> [%(not_after)s]*
                    ([^ \n\{\u200b%(not_before)s%(not_after)s%(western)s]|[%(western)s]+)
                    [%(not_before)s]*
                      )
        """ % locals()

        import re

        store._cjk_regexp = re.compile(regexp)
        
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

            for m in store._cjk_regexp.finditer(s):

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
        
