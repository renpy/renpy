# This is an early version of an interface for the updater. For now, we just
# assume that the user wants to update the prerelease channel, and the
# base tag.

init python:
    if persistent.last_update is None:
        persistent.last_update = "0"

label update:
    
    python hide:
        import time
        
        updater = Updater(config.basedir, 'http://update.renpy.org/update/prerelease', [ 'base' ])

        try:
            # Check the version.
            version, verbose_version = updater.check_version(persistent.last_update)
            
            if version is None:
                info("No Update Needed", "Your version of Ren'Py is up to date.")
                renpy.jump("top")


            if not yesno("Update Available", "Would you like to update to %s?" % verbose_version):
                renpy.jump("top")

            # If we've made it this far, the user has decided that he wants
            # to try an update.


            for what, amount, limit in updater.step():
                progress(what, limit, amount)

            persistent.last_update = version                
            info("Update complete.", "The update has finished. Ren'Py will now restart.")

            if sys.platform == "win32" and sys.argv[0].lower().endswith(".exe"):
                proc = subprocess.Popen([sys.argv[0], config.basedir])
            else:
                proc = subprocess.Popen([sys.executable, sys.argv[0], config.basedir])

            renpy.quit()
        

        except UpdateException, e:
            error('The update has failed, with the error message: %s' % e.args[0])

            

            
