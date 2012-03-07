# Name: jEdit
# Version: 1
# Description: jEdit requires Java be installed on your computer.

import os
import os.path
import sys


if sys.platform == 'win32':
    editor = os.path.normpath(base + "/../jedit/jedit.exe")
    editor = renpy.shell_escape(editor)
    config.editor = '"' + editor + '" -reuseview "%(filename)s" +line:%(line)d "%(otherfiles)s"'
    config.editor_transient = '"' + editor + '" -newplainview "%(filename)s" +line:%(line)d "%(otherfiles)s"'
else:
    editor = os.path.normpath(base + "/../jedit/jedit.jar")
    editor = renpy.shell_escape(editor)
    config.editor = 'java -jar "' + editor + '" -reuseview "%(filename)s" +line:%(line)d "%(otherfiles)s"'
    config.editor_transient = 'java -jar "' + editor + '" -newplainview "%(filename)s" +line:%(line)d "%(otherfiles)s"'
