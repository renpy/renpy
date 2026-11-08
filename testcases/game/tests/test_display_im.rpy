screen test_image_cache__uncached():
    tag menu

    add im.Null(color="#fff", cache=False, optimize_bounds=False):
        zoom 100
        align (0.5, 0.5)

    textbutton "Return" action ShowMenu("main_menu")


testsuite image_cache:
    after testcase:
        run ShowMenu("main_menu")

    testcase uncached_image:
        description "GH-7429: An uncached image can be rendered on screen."

        run ShowMenu("test_image_cache__uncached")
        pause 0.1
        assert screen "test_image_cache__uncached"
        click "Return"
        assert screen "main_menu"
