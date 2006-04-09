init 1000:
    python hide:

        # This returns true if the script_version is <= the
        # script_version supplied. Give it the last script version
        # where an old version was used.
        def compat(x, y, z):
            return library.script_version and library.script_version <= (x, y, z)


        if compat(5, 4, 5):
            if config.with_callback:
                def compat_with_function(trans, paired, old=config.with_function):
                    old(trans)
                    return trans

                config.with_callback = trans
                
                
