
# This file imports the extensions API into the default store, and makes it
# also contains the strings used by the extensions API, so the Ren'Py translation
# framework can find them.

init python:
    import installer

init python hide:
    _("Downloading [extension.download_file].")
    _("Could not download [extension.download_file] from [extension.download_url]:\n{b}[extension.download_error]")
    _("The downloaded file [extension.download_file] from [extension.download_url] is not correct.")
