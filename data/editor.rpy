# This file contains logic for detecting an editor, and for selecting
# the default editor.

init:
    python hide:
        import os.path
        import sys
        import platform
        

        if not config.editor:
             
            if sys.platform == 'win32':
                editor = config.renpy_base + "/editor/scite.exe"

                if os.path.exists(editor):
                    editor = renpy.shell_escape(editor)
                    config.editor = '"' + editor + '" "%(allfiles)s" "-open:%(filename)s" -goto:%(line)d'

            elif platform.mac_ver()[0]:
                config.editor = "open -t '%(allfiles)s'"

            else:
                editor = config.renpy_base + "/editor/scite"
            
                if os.path.exists(editor):
                    editor = renpy.shell_escape(editor)
                    config.editor = "'" + editor + "' '%(allfiles)s' '-open:%(filename)s' -goto:%(line)d"

            if config.editor:
                os.environ['RENPY_EDITOR'] = config.editor
                
