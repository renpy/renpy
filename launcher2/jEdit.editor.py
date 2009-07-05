# Name: jEdit
# Version: 1
# Description: jEdit requires Java be installed on your computer.

import os
import os.path
import sys

editor = os.path.normpath(base + "/../jedit/jedit.jar")
editor = renpy.shell_escape(editor)

if sys.platform == 'win32':
    config.editor = 'javaw.exe -jar "' + editor + '" -reuseview "%(filename)s" +line:%(line)d "%(otherfiles)s"'
    config.editor_transient = 'javaw.exe -jar "' + editor + '" -newplainview "%(filename)s" +line:%(line)d "%(otherfiles)s"'
else:
    config.editor = 'java -jar "' + editor + '" -reuseview "%(filename)s" +line:%(line)d "%(otherfiles)s"'
    config.editor_transient = 'java -jar "' + editor + '" -newplainview "%(filename)s" +line:%(line)d "%(otherfiles)s"'
