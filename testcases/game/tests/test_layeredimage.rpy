layeredimage test_unknown_attribute:

    attribute happy:
        image:
            pass

    always:
        "eileen_happy.png"


label layeredimage_unknown_attribute_without_developer:
    $ config.developer = False
    $ config.report_extraneous_attributes = False
    $ config.raise_image_exceptions = False

    show test_unknown_attribute happy typo_attribute
    "Layeredimage displayed without developer mode."
    return


label layeredimage_unknown_attribute_with_developer:
    $ config.developer = True
    $ config.report_extraneous_attributes = True
    $ config.raise_image_exceptions = False

    show test_unknown_attribute happy typo_attribute
    "Layeredimage displayed with developer mode."
    return


label layeredimage_unknown_attribute_error:
    $ config.developer = True
    $ config.report_extraneous_attributes = True
    $ config.raise_image_exceptions = True
    show test_unknown_attribute happy typo_attribute
    "Layeredimage not displayed."
    return


init python:
    def layeredimage_has_error_displayable():
        displayable = renpy.game.context().scene_lists.get_displayable_by_tag("master", "test_unknown_attribute")
        children = []
        displayable.visit_all(children.append)

        return any(isinstance(child, renpy.text.text.Text) for child in children)


testsuite layeredimage:
    setup:
        $ _test.old_config = (config.developer, config.report_extraneous_attributes, config.raise_image_exceptions)
        $ layeredimage_old_developer = config.developer
        $ layeredimage_old_report_extraneous_attributes = config.report_extraneous_attributes
        $ layeredimage_old_raise_image_exceptions = config.raise_image_exceptions

    teardown:
        $ config.developer, config.report_extraneous_attributes, config.raise_image_exceptions = _test.old_config
        $ del _test.old_config

    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase unknown_attribute_without_developer:
        run Start("layeredimage_unknown_attribute_without_developer")
        advance until "Layeredimage displayed without developer mode."
        assert eval not layeredimage_has_error_displayable()

    testcase unknown_attribute_with_developer:
        run Start("layeredimage_unknown_attribute_with_developer")
        advance until "Layeredimage displayed with developer mode."
        assert eval layeredimage_has_error_displayable()

    testcase unknown_attribute_raises:
        xfail True
        run Start("layeredimage_unknown_attribute_error")
        advance
