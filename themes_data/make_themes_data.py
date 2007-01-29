#!/usr/bin/python

import re
import sys
import pprint

sys.stdout.write("init 1 python:\n")
sys.stdout.write("    theme_data = ")

themes = { }

for fn in sys.argv[1:]:
    theme = fn.replace(".rpy", "")
    theme = theme.replace("_", " ").title()

    colors = { }
    
    f = file(fn)
    for l in f:
        l = l.strip()
        m = re.match(r'(\w+)\s*=\s*["\'](.*?)["\']', l)
        if m:
            colors[m.group(1)] = m.group(2)

        if "theme.roundrect" in l:
            colors["theme"] = "roundrect"
            
    f.close()
    themes[theme] = colors

pprint.pprint(themes, indent=1)
    
sys.stdout.write("\n")
