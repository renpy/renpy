init python:
    TEST_PROJECTS = u"/tmp/renpy-moé"
    import shutil

testcase default:
    call new_project
    call build_project

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

testcase build_project:
    "Build Distributions"
    "Build"

