#!/usr/bin/python

import sys
import re

keywords = [
    r'\bimage\b',
    r'\bscene\b',
    r'\bshow\b',
    r'\bhide\b',
    r'\binit\b',
    r'\$',
    r'\blabel\b',
    r'\bmenu\b',
    r'\bset\b',
    r'\bif\b',
    r'\bwhile\b',
    r'\bjump\b',
    r'\blabel\b',
    r'\bcall\b',
    r'\breturn\b',
    r'\bfrom\b',
    r'\belif\b',
    r'\belse\b',
    r'\bpass\b',
    ]

kwre = '|'.join(keywords)

def example(m):
    s = m.group(1)
    rv = ""
    pos = 0

    while pos < len(s):

        m = re.compile(r'(?s)"(([^"]|\\.)*)"').match(s, pos)
        if m:
            rv += '"<span class="string">%s</span>"' % m.group(1)
            pos = m.end()
            continue

        m = re.compile(r"(?s)'(([^']|\\.)*)'").match(s, pos)
        if m:
            rv += '\'<span class="string">%s</span>\'' % m.group(1)
            pos = m.end()
            continue

        m = re.compile(r"(?s)(#[^\n]+)").match(s, pos)
        if m:
            rv += '<span class="comment">%s</span>' % m.group(1)
            pos = m.end()
            continue


        m = re.compile(kwre).match(s, pos)
        if m:
            rv += '<span class="keyword">%s</span>' % m.group(0)
            pos = m.end()
            continue


        rv += s[pos]
        pos += 1
        

    return "<example>" + rv + "</example>"

def main():

    f = file(sys.argv[1])
    s = f.read()
    f.close()

    s = re.sub(r"(?s)<example>(.*?)</example>", example, s)

    print s

if __name__ == "__main__":
    main()
