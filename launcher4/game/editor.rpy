# Editor Support.
#
# This contains code for scanning for editors, and for allowing the user to
# select an editor.

init python in editor:

    from store import Action, renpy, config, persistent
    import store.project as project

    import glob
    import re
    import traceback
    import os
    import os.path
    
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
        
    def scan_all():
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

    def setup():
        """
        Sets up the editor contained in system.editor.
        """

        if not set_editor:
            return
        
        for i in [ persistent.editor, "Editra", "None" ]:

            if i in editors:
                persistent.editor = i
                ei = editors[i]
                os.environ["RENPY_EDIT_PY"] = renpy.fsencode(os.path.abspath(ei.filename))
                renpy.editor.init()
                return

        os.environ.discard("RENPY_EDIT_PY") 
        renpy.editor.init()

    scan_all()
    setup()

    
    class Edit(Action):
        def __init__(self, filename, line=None, check=False):
            """
            An action that opens the given line of the given file in a
            text editor. 
            
            `filename`
                The filename to open.
                
            `line`
                The line in the file to jump to.
                
            `check`
                If true, we will check to see if the file exists, and gray
                out the box if it does not.
            """
            
            self.filename = filename
            self.line = line
            self.check = check
    
        def get_sensitive(self):
            if not self.check:
                return True
                
            fn = project.current.unelide_filename(self.filename)
            return os.path.exists(fn)
    
        def __call__(self):
            
            if not self.get_sensitive():
                return
            
            fn = project.current.unelide_filename(self.filename)
            e = renpy.editor.editor
            
            e.begin()
            e.open(fn, line=self.line)
            e.end()
            
    class EditAll(Action):
        """
        Opens all scripts that are part of the current project in a web browser.
        """
        
        def __init__(self):
            return
            
        def __call__(self):
            scripts = project.current.script_files()            
            scripts.sort(key=lambda fn : fn.lower())

            for fn in [ "game/screens.rpy", "game/options.rpy", "game/script.rpy" ]:
                if fn in scripts:
                    scripts.remove(fn)
                    scripts.insert(0, fn)
                    
            e = renpy.editor.editor
            e.begin()
            
            for fn in scripts:
                fn = project.current.unelide_filename(fn)
                e.open(fn)
                
            e.end()
            
    class Select(Action):
        """
        Selects the text editor to use.
        """
        
        def __init__(self, name):
            self.name = name
            
        def __call__(self):
            persistent.editor = self.name
            setup()
            renpy.restart_interaction()
            
        def get_selected(self):
            return persistent.editor == self.name
            
            
    def editor_action_list():
        """
        Gets a list of (editor name, select action) tuples, one for each
        editor we know of.
        """
        
        rv = [ ]
        
        for i in sorted(editors, key=lambda a : a.lower()):
            rv.append((i, Select(i)))
                
        return rv
