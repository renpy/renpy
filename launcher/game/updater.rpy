init python:
    # This can be one of None, "available", "not-available", or "error".
    #
    # It must be None for a release.
    UPDATE_SIMULATE = None
    
    UPDATE_URLS = [
        ("Release", "http://update.renpy.org/release/update.json" ),
        ("Pre-Release", "http://update.renpy.org/prerelease/update.json" ),
        ("Experimental", "http://update.renpy.org/experimental/update.json" ),
        ]
    
    if persistent.update_url is None:
        persistent.update_url = UPDATE_URLS[0][1]
    
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
        updater.update(persistent.update_url, simulate=UPDATE_SIMULATE, public_key="renpy_public.pem")
    
    # This should never happen.
    jump front_page

