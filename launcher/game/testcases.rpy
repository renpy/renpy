testsuite all:
    after:
        exit

testcase dark_theme:
    python hide:
        renpy.watch("renpy.is_in_test()")
        renpy.watch("waitch")
        renpy.watch("whether")
        waitch = 5
    click "preferences"
    click "theme"
    click "dEfAuLt theme"
    click "theme"
    click "dark the"
    click "return"
    # exit
    # click "quit"


init python:
    import shutil
    import tempfile


testsuite default:
    before:
        python:
            persistent.old_projects_directory = persistent.projects_directory

            if persistent.temp_projects_directory:
                if os.path.exists(persistent.temp_projects_directory):
                    shutil.rmtree(persistent.temp_projects_directory)

                os.mkdir(persistent.temp_projects_directory, 0o777)
            else:
                persistent.temp_projects_directory = tempfile.mkdtemp(prefix="renpy-test-")

            persistent.projects_directory = persistent.temp_projects_directory

    before_each:
        $ _test.timeout = 5.0

    after:
        python:
            persistent.projects_directory = persistent.old_projects_directory
            if os.path.exists(persistent.temp_projects_directory):
                shutil.rmtree(persistent.temp_projects_directory)

            persistent.temp_projects_directory = None


    testcase new_project:
        click "refresh"
        click "Create New Project"

        click "Continue"

        # Name
        type "Test Project"
        click "Continue"

        # Size
        click "1280x720"
        click "Continue"

        # Color Selection
        click "Continue"


    testcase translate_project:
        click "Generate Translations"

        keysym "K_BACKSPACE" repeat 30

        type "piglatin"

        click "Generate Translations"
        click "Continue"

        click "Generate Translations"
        click "Extract String Translations"
        click "Continue"

        click "Generate Translations"
        click "Merge String Translations"
        click "Continue"

        click "Generate Translations"
        click "Update Default"


    testsuite extract_dialogue:
        before_each:
            click "Extract Dialogue"
            click "Strip text tags"
            click "Escape quotes"
            click "Extract all"

        testcase tab_delimited:
            click "Tab-delimited"
            click "Continue"
            click "Continue"

        testcase text_only:
            click "Text Only"
            click "Continue"
            click "Continue"


    testcase recompile:
        click "Delete Persistent"
        click "Force Recompile"


    testcase build_project:
        $ _test.timeout = 60.0
        click "Build Distributions"
        click "Build"
        pause until "Return"
        click "Return"


    testcase choose_colors:
        click "Change/Update GUI"
        click "Choose new colors"
        click "Continue"
        click "Continue"

        click "Change/Update GUI"
        click "Regenerate the"
        click "Continue"


testcase android(skip=True):

    $ _test.timeout = 60.0
    $ _test.maximum_framerate = False

    click "Tutorial"
    pause 0.5
    click "Android"

    # Download and install RAPT.
    if "Yes":

        click "Yes"
        click "Proceed"

    click "Install SDK"
    click "Yes" until "Continue"

    # We have to create the key.
    if "Cancel":
        type "Test Key"
        click "Continue"
        click "Continue"

    # Configure the application.
    click "Configure"

    $ _test.maximum_framerate = True

    keysym "K_BACKSPACE" repeat 30
    type "Ren'Py Tutorial"
    click "Continue"

    keysym "K_BACKSPACE" repeat 30
    type "Ren'Py Tutorial"
    click "Continue"

    keysym "K_BACKSPACE" repeat 30
    type "org.renpy.tutorial"
    click "Continue"

    keysym "K_BACKSPACE" repeat 30
    type "1.2.3"
    click "Continue"

    keysym "K_BACKSPACE" repeat 30
    type "10203"
    click "Continue"

    $ _test.maximum_framerate = False

    click "In landscape"
    click "Continue"

    click "Neither"
    click "Continue"

    click "No."
    click "Continue"

    click "Android 4.0"
    click "Continue"

    # Access the internet.
    click "No"
    click "Continue"

    # Build the package.
    click "Build Package"
    click "Continue"
