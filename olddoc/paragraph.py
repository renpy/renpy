#!/usr/bin/python

import sys
import re

nopar = [
    "<pre",
    "<ul",
    "<li",
    "<example",
    "<ol",
    "<h",
    "<var",
    "</var",
    "<label",
    "<!--",
    "<func",
    "</func",
    "<label",
    "</label",
    ]

noclose = [
    "</pre",
    "</ul",
    "</li",
    "</example",
    "</ol",
    "</h",
    "</var",
    "<var",
    "<!--",
    "</func",
    "<func",
    "</label",
    "<label",
    ]



while True:

    # Read until # START NOPAR or EOF.
    for l in sys.stdin:
        if l.startswith("# START NOPAR"):
            break
        sys.stdout.write(l)
    else:
        break

    # Read until # END NOPAR.
    data = ""

    for l in sys.stdin:
        if l.startswith("# END NOPAR"):
            break

        data += l

    # Tokenize.
    tokens = list(re.split(r'(?s)(<[^>]+>)', data))
    moretokens = [ ]

    for i in tokens:
        moretokens.extend([j for j in re.split(r'(?s)(\s*\n\s*\n\s*)', i) if j])

    nt = [ moretokens[0] ]

    # Insert paragraphs as appropriate.
    i = 1
    while i < len(moretokens) - 1:

        prev = moretokens[i - 1]
        cur = moretokens[i]
        next = moretokens[i + 1]

        if cur == "<example>":

            nt.append(cur)
            while True:
                i += 1
                cur = moretokens[i]
                nt.append(cur)
                if cur == "</example>":
                    break

            i += 1
            continue

        if not re.search(r'\n\s*\n', cur):
            nt.append(cur)
            i += 1
            continue

        nt.append("\n")

        for j in noclose:
            if prev.startswith(j):
                break
        else:
            nt.append("</p>")

        for j in nopar:
            if next.startswith(j):
                break
        else:
            nt.append("<p>")

        nt.append("\n")

        i += 1

    nt.append(moretokens[-1])        
    nt.append("\n</p>\n")            

    print ''.join(nt)
