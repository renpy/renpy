init python:

    def check_dists_license():
        """
        Checks that every archive built for the current project contains
        renpy/LICENSE.txt, and that it matches sphinx/source/license.rst.
        Returns True if so, and raises an exception otherwise.
        """

        import tarfile
        import zipfile

        with open(os.path.join(config.renpy_base, "sphinx", "source", "license.rst"), "rb") as f:
            license = f.read()

        p = project.current
        destination = os.path.join(p.parent_path, p.dump["build"]["destination"])

        archives = [ i for i in os.listdir(destination) if i.endswith((".zip", ".tar.bz2")) ]

        if not archives:
            raise Exception("No archives were built in {}.".format(destination))

        for fn in archives:
            path = os.path.join(destination, fn)

            if fn.endswith(".zip"):
                with zipfile.ZipFile(path) as zf:
                    names = [ i for i in zf.namelist() if i.endswith("/renpy/LICENSE.txt") ]
                    contents = [ zf.read(i) for i in names ]
            else:
                with tarfile.open(path) as tf:
                    names = [ i for i in tf.getnames() if i.endswith("/renpy/LICENSE.txt") ]
                    contents = [ tf.extractfile(i).read() for i in names ]

            if not contents:
                raise Exception("{} does not contain renpy/LICENSE.txt.".format(fn))

            for name, data in zip(names, contents):
                if data != license:
                    raise Exception("{} in {} does not match license.rst.".format(name, fn))

        return True

    def check_package_failures():
        """
        Checks that failures while packaging reach the code that started the build.
        Returns True if so, and raises an exception otherwise.
        """

        import shutil
        import tempfile

        class FailingPackage(object):
            def close(self, progress=None):
                raise Exception("This failure is expected by the test.")

        distribute.ParallelPackage(FailingPackage(), None, "failing").close()

        try:
            distribute.wait_parallel_threads()
        except Exception as e:
            if "failing" not in str(e):
                raise
        else:
            raise Exception("A failure in a package thread was ignored.")

        tempdir = tempfile.mkdtemp(prefix="renpy-test-")

        try:
            # Zip has nothing to do, so it fails.
            package = distribute.ExternalZipPackage(os.path.join(tempdir, "empty.zip"))

            try:
                package.close()
            except Exception:
                pass
            else:
                raise Exception("A failure of zip was ignored.")

        finally:
            shutil.rmtree(tempdir)

        return True


testsuite global:
    setup:
        # On a tree that has never run the launcher, it starts by asking for a language.
        pause until (screen "choose_language" or id "pref_btn")

        if screen "choose_language":
            click "Start using Ren'Py"

    teardown:
        exit

testcase change_language:
    parameter lang = [
        "arabic", "danish", "finnish", "french", "german",
        "greek", "indonesian", "italian", "japanese", "korean",
        "malay", "persian", "piglatin", "polish", "portuguese",
        "russian", "schinese", "spanish", "tchinese", "turkish",
        "ukrainian", "vietnamese", "None"]

    click id "pref_btn"
    click id "pref_general_btn"
    click id f"pref_change_language_btn_{lang}"

    click "Options" raw
    click "Theme" raw
    click "Install Libraries" raw
    click "Actions" raw
    click "Lint" raw
    click "Return" raw

    # click id "pref_options_btn"
    # click id "pref_theme_btn"
    # click id "pref_install_btn"
    # click id "pref_actions_btn"
    # click id "pref_lint_btn"
    # click id "return_btn"

testcase themes:
    click id "pref_btn"

    click id "pref_theme_btn"
    click id "pref_theme_dark_btn"
    click id "pref_theme_btn"
    click id "pref_theme_default_btn"
    # click id "pref_theme_btn"
    # click id "pref_theme_dark_btn"

    click id "return_btn"


testsuite default:
    setup:
        python:
            import shutil
            import tempfile

            persistent.old_projects_directory = persistent.projects_directory

            if persistent.temp_projects_directory:
                if os.path.exists(persistent.temp_projects_directory):
                    shutil.rmtree(persistent.temp_projects_directory)

                os.mkdir(persistent.temp_projects_directory, 0o777)
            else:
                persistent.temp_projects_directory = tempfile.mkdtemp(prefix="renpy-test-")

            persistent.projects_directory = persistent.temp_projects_directory

    before testcase:
        $ _test.timeout = 5.0

    teardown:
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
        before testcase:
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

        assert eval check_dists_license()


    testcase package_failures:
        assert eval check_package_failures()


    testcase choose_colors:
        click "Change/Update GUI"
        click "Choose new colors"
        click "Continue"
        click "Continue"

        click "Change/Update GUI"
        click "Regenerate the"
        click "Continue"


testcase android:
    enabled False

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
