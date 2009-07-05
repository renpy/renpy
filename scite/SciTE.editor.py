# Name: SciTE
# Version: 1
# Description: The SciTE editor, for Windows and Linux.

import os.path
import sys

if sys.platform == 'win32':
    editor = base + "/scite.exe"
else:
    editor = base + "/scite"

editor = os.path.normpath(editor)
editor = renpy.shell_escape(editor)

config.editor = '"' + editor + '" "%(allfiles)s" -goto:%(line)d'
config.editor_transient = config.editor +' -revert:'
