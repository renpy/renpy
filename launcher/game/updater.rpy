init python:
    # This can be one of None, "available", "not-available", or "error".
    #
    # It must be None for a release.
    UPDATE_SIMULATE = None
    
    PUBLIC_KEY = "renpy_public.pem"
    
    UPDATE_URLS = [
        ("Release", "http://update.renpy.org/release/updates.json" ),
        ("Pre-Release", "http://update.renpy.org/prerelease/updates.json" ),
        ("Experimental", "http://update.renpy.org/experimental/updates.json" ),
        ]
    
    DLC_URL = "http://localhost/tmp/renpy-dist/updates.json"
    
    if persistent.update_url is None:
        persistent.update_url = UPDATE_URLS[0][1]
    
    def check_dlc(name):
        """
        Returns true if the named dlc package is present.
        """
        
        return name in updater.get_installed_packages()
        
    def add_dlc(name):
        """
        Adds the DLC package, if it doesn't already exist.
        
        Returns True if the DLC is installed, False otherwise.
        """
        
        if check_dlc(name):
            return True
            
        return renpy.invoke_in_new_context(updater.update, DLC_URL, add=[name], public_key=PUBLIC_KEY, simulate=UPDATE_SIMULATE, restart=False)

screen updater:
        
    frame:
        style "l_root"

        frame:
            style_group "l_info"
        
            has vbox

            if u.state == u.ERROR:
                text _("An error has occured:")
            elif u.state == u.CHECKING:
                text _("Checking for updates.")
            elif u.state == u.UPDATE_NOT_AVAILABLE:
                text _("Ren'Py is up to date.")
            elif u.state == u.UPDATE_AVAILABLE:
                text _("[u.version] is now available. Do you want to install it?")
            elif u.state == u.PREPARING:
                text _("Preparing to download the update.")
            elif u.state == u.DOWNLOADING:
                text _("Downloading the update.")
            elif u.state == u.UNPACKING:
                text _("Unpacking the update.")
            elif u.state == u.FINISHING:
                text _("Finishing up.")
            elif u.state == u.DONE:
                text _("The update has been installed. Ren'Py will now restart.")
            elif u.state == u.DONE_NO_RESTART:
                text _("The update has been installed.")
            elif u.state == u.CANCELLED:
                text _("The update was cancelled.")

            if u.message is not None:
                add SPACER
                text "[u.message!q]"

            if u.progress is not None:
                add SPACER
                
                frame:
                    style "l_progress_frame"
                    
                    bar:
                        range 1.0
                        value u.progress
                        style "l_progress_bar"

        label _("Ren'Py Update") style "l_info_label"

    if u.can_cancel:
        textbutton _("Cancel") action u.cancel style "l_left_button"
        
    if u.can_proceed:
        textbutton _("Proceed") action u.proceed style "l_right_button"

label update:
    
    python:
        updater.update(persistent.update_url, simulate=UPDATE_SIMULATE, public_key=PUBLIC_KEY)
    
    # This should never happen.
    jump front_page

