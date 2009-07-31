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
    
    # A map from editor name to the file containing information about
    # that editor.
    editors = { }

    # A map from editor to the version of that editor.
    editor_versions = { }

    # A map from editor to a description of that editor.
    editor_descriptions = { }
    
    # Should we set up the editor? How about the transient editor?
    set_editor = "RENPY_EDITOR" not in os.environ
    set_editor_transient = "RENPY_EDITOR_TRANSIENT" not in os.environ

    if set_editor and not set_editor_transient:
        config.editor_transient = config.editor
        os.environ['RENPY_EDITOR_TRANSIENT'] = config.editor
        set_editor_transient = False

    def scan_editor(ef):
        """
         Scans a single editor file to get the meta-information. If it
         checks out, adds it to editors. Uses editor_versions as a cache
         so we only add the newest version of each editor.
         """

        info = { }
        
        f = file(ef, "r")
        for l in f:
            m = re.match("#\s*(\w+):\s*(.*?)\s*$", l)
            if not m:
                break

            info[m.group(1)] = m.group(2)

        f.close()
            
        try:
            name = info["Name"]
            version = int(info["Version"])
            description = info.get("Description", "")
        except:
            traceback.print_exc()
            print >>sys.stderr, ef
            

        if version > editor_versions.get(name, -1):
            editors[name] = ef
            editor_versions[name] = version
            editor_descriptions[name] = description
            
    
    def scan_editors():
        """
         Finds all *.editor.py files, and uses them to populate the list
         of editors.
         """

        editors.clear()
        editor_versions.clear()
        editor_descriptions.clear()
        
        for d in [ config.renpy_base, persistent.projects_directory ]:
            if d is None:
                continue
            
            for ef in glob.glob(d + "/*/*.editor.py"):
                scan_editor(ef)


    def setup_editor():
        """
         Sets the system up to respect the value containined in
         persistent.editor.
         """

        if not set_editor:
            return
        
        ef = None
        
        for i in [ persistent.editor, "jEdit", "None" ]:
            if i in editors:
                ef = editors[i]
                break
        else:
            return

        ctx = {
           "renpy" : renpy,
            "config" : config,
            "persistent" : persistent,
            "base" : os.path.dirname(ef),
            }
        
        execfile(ef, ctx, ctx)

        if set_editor:
            if config.editor:
                os.environ['RENPY_EDITOR'] = config.editor
            else:
                if 'RENPY_EDITOR' in os.environ:
                    del os.environ['RENPY_EDITOR']

        if set_editor_transient:
            if config.editor_transient:
                os.environ['RENPY_EDITOR_TRANSIENT'] = config.editor_transient
            else:
                if 'RENPY_EDITOR_TRANSIENT' in os.environ:
                    del os.environ['RENPY_EDITOR_TRANSIENT']

label editor:

    python hide:

        if not set_editor:
            error(_(u"The editor has been set from the RENPY_EDITOR environment variable, and cannot be changed."), "options")
        
        set_tooltip("")

        screen()
        ui.vbox()
        title(_(u"Choose Editor"))

        text(_(u"Please choose the editor that will be use to edit scripts and display errors. More editors can be downloaded from {a=http://www.renpy.org/wiki/renpy/Editors}the Ren'Py website{/a}."))

        ui.null(height=15)
        
        scrolled("options")

        ui.vbox()

        for i in sorted(editors, key=lambda a : a.lower()):
            button(i,
                   ui.returns(i),
                   editor_descriptions[i])

        ui.close() # Vbox
        ui.close() # Scrolled

        ui.close() # Vbox

        persistent.editor = interact()
        setup_editor()
        
    jump options
