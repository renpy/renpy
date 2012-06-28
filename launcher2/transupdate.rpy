# This file contains code for updating translations. Basically, it will
# search for a non-default file in launcher, and if that file exists, it
# will append missing translations to it.

init python:
    import os
    import os.path
    import traceback
    import codecs
    
    def update_translations():

        # Find the first file in the launcher directory that was
        # not distributed with Ren'Py.
        for fn in sorted(os.listdir(config.gamedir)):
            if not fn.endswith(".rpy"):
                continue

            if fn in LAUNCHER_RPYS:
                continue

            break

        else:
            return

        # Find untranslated strings.
        new_translations = [ ]

        for t in TRANSLATION_STRINGS:
            if t not in config.translations:
                new_translations.append(t)

        if not new_translations:
            return


        # Add a block to the file with the untranslated strings.
        f = codecs.open(os.path.join(config.gamedir, fn), "a", "utf-8")
        
        print >>f
        print >>f, "# New translations for", renpy.version()
        print >>f, "init -1 python hide:"
        print >>f, "    config.translations.update({"
        
        for t in new_translations:

            print >>f
            print >>f, "    %r" % t
            print >>f, "    : %r," % t

        print >>f
        print >>f, "    })"
            
        f.close()
    
init 100 python hide:

    try:
        update_translations()
    except:
        traceback.print_exc()
