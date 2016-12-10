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

    # Kind of interface
    "New GUI Interface"
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



testcase translate_project:
    "Generate Translations"

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
    type BACKSPACE
    type BACKSPACE
    type BACKSPACE
    type BACKSPACE
    type BACKSPACE
    type BACKSPACE

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
