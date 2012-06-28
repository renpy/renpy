# This is an early version of an interface for the updater. For now, we just
# assume that the user wants to update the prerelease channel, and the
# base tag.

init python:
    import os
    import time
    
    version_fn = os.path.join(config.basedir, "lib", "update-version.txt")
    update_allowed = os.path.exists(version_fn)

label update:
    
    python hide:
        
        try:
            info("Checking for update...", "")
            
            old_version = file(version_fn, "rb").read()                 
            updater = Updater(config.basedir, 'http://update.renpy.org/renpy/updates/prerelease', [ 'base' ])

            # Check the version.
            version, verbose_version = updater.check_version(old_version)
            
            if version is None:
                pauseinfo("Up To Date", "Your version of Ren'Py is up to date.")
                renpy.jump("top")


            if not yesno("Update Available", "Would you like to update to %s?" % verbose_version):
                renpy.jump("top")

            # If we've made it this far, the user has decided that he wants
            # to try an update.

            for what, amount, limit in updater.step():
                progress(what, limit, amount)

            f = file(version_fn, "wb")
            f.write(version)
            f.close()
            
            pauseinfo("Update complete.", "The update has finished. Ren'Py will now restart.")

            if sys.platform == "win32" and sys.argv[0].lower().endswith(".exe"):
                proc = subprocess.Popen([sys.argv[0], config.basedir])
            else:
                proc = subprocess.Popen([sys.executable, sys.argv[0], config.basedir])

            renpy.quit()
        

        except UpdateException, e:
            error('The update has failed, with the error message: %s' % e.args[0])

            

            
