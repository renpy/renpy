#!/usr/bin/env python
#@PydevCodeAnalysisIgnore

import sys
import pylint.lint
import pylint.reporters.text
import linecache

class MyReporter(pylint.reporters.text.TextReporter):

    def add_message(self, msg_id, location, msg):
        if msg_id == "E1103" and "Instance of 'Style'" in msg:
            return

        if msg_id == "E1101" and "Instance of 'Style'" in msg:
            return

        if msg_id == "E1101" and "Instance of 'ModuleProxy'" in msg:
            return

        if msg_id == "E1101" and "Instance of 'ImageFont'" in msg:
            return

        if msg_id == "E1102" and "renpy.config" in msg:
            return
        
        fn, module, obj, line = location

        text = linecache.getline(fn, line)

        if msg_id.lower() in text.lower():
            return
        
        pylint.reporters.text.TextReporter.add_message(self, msg_id, location, msg)

pylint.lint.Run(sys.argv[1:], reporter=MyReporter())
