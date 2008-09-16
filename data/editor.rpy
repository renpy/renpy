# This file contains logic for detecting an editor, and for selecting
# the default editor.

init:
    python hide:
        import os
        import sys

        if not config.editor:

            editor = config.renpy_base + "/jedit/jedit.jar"
            editor = renpy.shell_escape(editor)

            if sys.platform == 'win32':
                config.editor = 'javaw.exe -jar "' + editor + '" -reuseview "%(filename)s" +line:%(line)d "%(otherfiles)s"'
                config.editor_transient = 'javaw.exe -jar "' + editor + '" -newplainview "%(filename)s" +line:%(line)d "%(otherfiles)s"'
            else:
                config.editor = "java -jar '" + editor + "' -reuseview '%(filename)s'  +line:%(line)d '%(otherfiles)s'"
                config.editor_transient = "java -jar '" + editor + "' -newplainview '%(filename)s' +line:%(line)d '%(otherfiles)s'"
            
        if config.editor:
            os.environ['RENPY_EDITOR'] = config.editor
        if config.editor_transient:
            os.environ['RENPY_EDITOR_TRANSIENT'] = config.editor_transient
                
