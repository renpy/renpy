init python:
    def slparser_legacy_screen(**kwargs):
        renpy.ui.text("Legacy content")

    renpy.display.screen.define_screen("slparser_legacy_screen", slparser_legacy_screen)


screen slparser_legacy_root():
    use slparser_legacy_screen
    text "SL2 content"


screen slparser_legacy_nested():
    vbox:
        use slparser_legacy_screen
        text "SL2 content"


testsuite slparser:

    testcase legacy_screen_use:
        run Show("slparser_legacy_root")
        assert eval len(renpy.get_screen("slparser_legacy_root").child.children) == 2
        run Hide("slparser_legacy_root")

        run Show("slparser_legacy_nested")
        assert eval len(renpy.get_screen("slparser_legacy_nested").child.children[0].children) == 2
        run Hide("slparser_legacy_nested")

    testcase legacy_screen_show:
        run Show("slparser_legacy_screen")
        assert eval len(renpy.get_screen("slparser_legacy_screen").child.children) == 1
        run Hide("slparser_legacy_screen")
