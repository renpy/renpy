#!/usr/bin/env python

# This program adds froms to every unqualified call found in the game
# directory. It's not perfect, but it's better than nothing.

import sys
import renpy.tools.add_from as add_from

def main():

    if len(sys.argv) != 3:
        print "Usage: %s <game directory> <common directory>" % sys.argv[0]
        return


    add_from.add_from(sys.argv[1], sys.argv[2])
        


if __name__ == "__main__":
    main()
