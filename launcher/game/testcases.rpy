init python:
    TEST_PROJECTS = u"/tmp/renpy-moé"
    import shutil


testcase default:

    call new_project
    call translate_project
    call extract_dialogue

    "Delete Persistent"
    "Force Recompile"

    call build_project

    "quit"


testcase new_project:
    python:
        if os.path.exists(TEST_PROJECTS):
            shutil.rmtree(TEST_PROJECTS)

        os.mkdir(TEST_PROJECTS, 0o777)

        persistent.projects_directory = TEST_PROJECTS

    "refresh"
    "Create New Project"

    "Continue"

    # Name
    type "Test Project"
    "Continue"

    # Size
    "1280x720"
    "Continue"

    # Color Selection
    "Continue"


testcase choose_colors:
    "Change/Update GUI"
    "Choose new colors"
    "Continue"
    "Continue"

    "Change/Update GUI"
    "Regenerate the"
    "Continue"


testcase delete10:
    type BACKSPACE
    type BACKSPACE
    type BACKSPACE
    type BACKSPACE
    type BACKSPACE
    type BACKSPACE
    type BACKSPACE
    type BACKSPACE
    type BACKSPACE
    type BACKSPACE


testcase delete30:
    call delete10
    call delete10
    call delete10


testcase translate_project:
    "Generate Translations"

    call delete30

    type "piglatin"

    "Generate Translations"
    "Continue"

    "Generate Translations"
    "Extract String Translations"
    "Continue"

    "Generate Translations"
    "Merge String Translations"
    "Continue"

    "Generate Translations"
    "Update Default"


testcase build_project:
    "Build Distributions"
    "Build"


testcase extract_dialogue_common:
    "Extract Dialogue"
    "Strip text tags"
    "Escape quotes"
    "Extract all"

testcase extract_dialogue:
    call extract_dialogue_common
    "Tab-delimited"
    "Continue"
    "Continue"

    call extract_dialogue_common
    "Text Only"
    "Continue"
    "Continue"


testcase android:

    $ _test.timeout = 60.0
    $ _test.maximum_framerate = False

    "Tutorial"
    "Android"

    # Download and install RAPT.
    if "Yes":

        "Yes"
        "Proceed"

    "Install SDK"
    "Yes" until "Continue"

    # We have to create the key.
    if "Cancel":
        type "Test Key"
        "Continue"
        "Continue"

    # Configure the application.
    "Configure"

    $ _test.maximum_framerate = True

    call delete30
    type "Ren'Py Tutorial"
    "Continue"

    call delete30
    type "Ren'Py Tutorial"
    "Continue"

    call delete30
    type "org.renpy.tutorial"
    "Continue"

    call delete30
    type "1.2.3"
    "Continue"

    call delete30
    type "10203"
    "Continue"

    $ _test.maximum_framerate = False

    "In landscape"
    "Continue"

    "Neither"
    "Continue"

    "No."
    "Continue"

    "Android 4.0"
    "Continue"

    # Access the internet.
    "No"
    "Continue"

    # Build the package.
    "Build Package"
    "Continue"

    "quit"
