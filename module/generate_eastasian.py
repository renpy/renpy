#!/usr/bin/env python
# Code to generate the eastasian unicode table as a pxi.

import unicodedata

classes = [ "F", "H", "W", "N", "Na", "A" ]

class_map = { }

for i, c in enumerate(classes):
    class_map[c] = i
    print "cdef char EA_{} = {}".format(c, i)
    
data = ""
    
for code in range(0, 0xffff):
    c = unichr(code)
    ea = unicodedata.east_asian_width(c)
    v = class_map[ea]
    
    data += "\\x{:02x}".format(v)
    
print "cdef char *eastasian_width = \"{}\"".format(data)

