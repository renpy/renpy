#!/usr/bin/python
import hotshot, hotshot.stats
import sys
import renpy

prof = hotshot.Profile("renpy.prof")
prof.runcall(renpy.main.main, sys.argv[1])
# prof.run(file("run_game.py").read())
prof.close()


print "Profiling in progress..."

stats = hotshot.stats.load("renpy.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(40)

             
