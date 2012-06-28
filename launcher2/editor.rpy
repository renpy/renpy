# This file contains logic for selecting an editor.

init python:

    import glob
    import re
    import traceback
    import os
    import os.path
    
    
    # The default name for the editor.
    if persistent.editor is None:
        persistent.editor = "jEdit"
    
    # Should we set up the editor?
    set_editor = "RENPY_EDIT_PY" not in os.environ

    # A map from editor name to EditorInfo object.
    editors = { }
 
    class EditorInfo(object):
        def __init__(self, filename):
            # The path to the editor info file.
            self.filename = filename
            
            # The name of the editor.
            self.name = os.path.basename(filename)[:-len(".edit.py")]
            
            # The time the editor file was last modified. We use this
            # to decide if we should update the editors mat when we 
            # have multiple versions of an editor in contention.
            self.mtime = os.path.getmtime(filename)
    

    def scan_editor(filename):
        """
        Inserts an editor into editors if there isn't a newer
        editor there already.
        """

        ei = EditorInfo(filename)
         
        if ei.name in editors:
           if editors[ei.name].mtime >= ei.mtime:
               return
                
        editors[ei.name] = ei
        
    def scan_editors():
        """
        Finds all *.edit.py files, and uses them to populate the list
        of editors.
        """

        editors.clear()
        
        for d in [ config.renpy_base, persistent.projects_directory ]:
            if d is None:
                continue
            
            for filename in glob.glob(d + "/*/*.edit.py"):
                scan_editor(filename)


    def setup_editor():
        """
         Sets the system up to respect the value containined in
         persistent.editor.
         """

        if not set_editor:
            return
        
        ei = None
        
        for i in [ persistent.editor, "jEdit", "None" ]:
            if i in editors:
                ei = editors[i]
                break
        else:
            return

        os.environ["RENPY_EDIT_PY"] = renpy.fsencode(os.path.abspath(ei.filename))
        renpy.editor.init()

label editor:

    python hide:

        if not set_editor:
            error(_(u"The editor has been set from the RENPY_EDIT_PY environment variable, and cannot be changed."), "options")
        
        set_tooltip("")

        screen()
        ui.vbox()
        title(_(u"Choose Editor"))

        text(_(u"Please choose the editor that will be use to edit scripts and display errors. More editors can be downloaded from {a=http://www.renpy.org/wiki/renpy/Editors}the Ren'Py website{/a}."))

        ui.null(height=15)
        
        scrolled("options")

        ui.vbox()

        for i in sorted(editors, key=lambda a : a.lower()):
            button(i, ui.returns(i))

        ui.close() # Vbox
        ui.close() # Scrolled

        ui.close() # Vbox

        persistent.editor = interact()
        setup_editor()
        
    jump options
