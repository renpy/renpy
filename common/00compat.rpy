init -1210:
    python:

        # This is called when script_version is set, to immediately
        # run code in response to a script_version change.        
        def _set_script_version(version):

            if version is None:
                return

            if version <= (5, 6, 0):
                config.check_properties = False

            if version <= (6, 5, 0):
                layout.compat()
                
init 1210:
    python hide:

        # This returns true if the script_version is <= the
        # script_version supplied. Give it the last script version
        # where an old version was used.
        def compat(x, y, z):
            return config.script_version and config.script_version <= (x, y, z)

        # Compat for changes to with-callback.
        if compat(5, 4, 5):
            if config.with_callback:
                def compat_with_function(trans, paired, old=config.with_callback):
                    old(trans)
                    return trans

                config.with_callback = compat_with_function
                

        if not config.sound:
            config.has_sound = False
            config.has_music = False

        # Compat for SFont recoloring.
        if compat(5, 1, 1):
            config.recolor_sfonts = False

        if compat(5, 5, 4):
            config.implicit_with_none = False
            
        # Compat for changes to button look.
        if compat(5, 5, 4):            
            style.button.setdefault(xpos=0.5, xanchor=0.5)
            style.menu_button.clear()
            style.menu_button_text.clear()

        if compat(5, 6, 6):
            config.reject_midi = False

        if compat(6, 2, 0):
            config.reject_backslash = False

        if "Fullscreen" in config.translations:
            fs = config.translations["Fullscreen"]
            config.translations.setdefault("Fullscreen (4:3)", fs + " (4:3)")
            config.translations.setdefault("Fullscreen (16:9)", fs + " (16:9)")
            config.translations.setdefault("Fullscreen (16:10)", fs + " (16:10)")
            
            
# Style compatibility.
init -1080:
    python:

        _selected_compat = [ ]

        class _SelectedCompat(object):

            def __init__(self, target):
                self.__dict__["target"] = target
                self.__dict__["property_updates"] = [ ]

                _selected_compat.append(self)

            def __setattr__(self, k, v):
                
                self.property_updates.append((k, v))

            def apply(self):
                target = getattr(style, self.target)
                for k, v in self.property_updates:
                    setattr(target, "selected_" + k, v)

            def clear(self):
                self.__dict__["property_updates"] = [ ]


        style.selected_button = _SelectedCompat('button')
        style.selected_button_text = _SelectedCompat('button_text')
        style.gm_nav_selected_button = _SelectedCompat('gm_nav_button')
        style.gm_nav_selected_button_text = _SelectedCompat('gm_nav_button_text')
        style.prefs_selected_button = _SelectedCompat('prefs_button')
        style.prefs_selected_button_text = _SelectedCompat('prefs_button_text')
    

init 1080:

    python hide:

        for scs in _selected_compat:
            scs.apply()
