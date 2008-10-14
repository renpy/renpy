
# This file contains logic for detecting an editor, and for selecting
# the default editor.

init:
    python hide:
        import os.path
        import sys
        import platform
        

        if not config.editor:
             
            if platform.mac_ver()[0]:
                config.editor = "open -t '%(allfiles)s'"

            else:
                
                if sys.platform == 'win32':
                    editor = config.renpy_base + "/editor/scite.exe"
                else:
                    editor = config.renpy_base + "/editor/scite"
                
                if os.path.exists(editor):
                    editor = renpy.shell_escape(editor)
                    config.editor = '"' + editor + '" "%(allfiles)s" "-open:%(filename)s" -goto:%(line)d'
                    config.editor_transient = config.editor+' -revert:'

            if config.editor:
                os.environ['RENPY_EDITOR'] = config.editor
            if config.editor_transient:
                os.environ['RENPY_EDITOR_TRANSIENT'] = config.editor_transient
                
