image model__texture = Solid("#fff")
default model__image = "model__texture"


screen model__dynamic_texture():
    tag menu

    default model = Model().texture(
        DynamicImage("[model__image]"),
        fit=True,
        texture_wrap=(renpy.uguu.GL_REPEAT, renpy.uguu.GL_CLAMP_TO_EDGE))

    add model:
        xysize (100, 100)
        align (0.5, 0.5)


testsuite model:
    after testcase:
        run ShowMenu("main_menu")

    testcase dynamic_texture_transition:
        description "GH-7430: Transitions can copy a Model with a DynamicImage texture."

        run ShowMenu("model__dynamic_texture")
        pause 0.1
        assert screen "model__dynamic_texture"
        $ renpy.transition(Dissolve(0.1))
        run ShowMenu("main_menu")
        pause 0.1
        assert screen "main_menu"
