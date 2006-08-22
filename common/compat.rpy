init 1000:
    python hide:

        # This returns true if the script_version is <= the
        # script_version supplied. Give it the last script version
        # where an old version was used.
        def compat(x, y, z):
            return library.script_version and library.script_version <= (x, y, z)


        # Compat for changes to with-callback.
        if compat(5, 4, 5):
            if config.with_callback:
                def compat_with_function(trans, paired, old=config.with_function):
                    old(trans)
                    return trans

                config.with_callback = compat_with_function
                
        # Compat for changes to button look.
        if compat(5, 4, 5):            
            style.button.setdefault(xpos=0.5, xanchor=0.5)
            style.button.clear()
            style.button_text.clear()
            style.selected_button.clear()
            style.selected_button_text.clear()

        if not config.sound:
            library.has_sound = False
            library.has_music = False

        # Compat for SFont recoloring.
        if compat(5, 1, 1):
            config.recolor_sfonts = False


# Style compatibility.
init -999:
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

        style.selected_button = _SelectedCompat('button')
        style.selected_button_text = _SelectedCompat('button_text')
        style.gm_nav_selected_button = _SelectedCompat('gm_nav_button')
        style.gm_nav_selected_button_text = _SelectedCompat('gm_nav_button_text')
        style.prefs_selected_button = _SelectedCompat('prefs_button')
        style.prefs_selected_button_text = _SelectedCompat('prefs_button_text')
    

init 1000:

    python hide:
        
        for scs in _selected_compat:
            scs.apply()
