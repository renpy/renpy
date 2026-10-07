init python:
    def test_particle__midpoint(a, b):
        return (a + b) / 2

    def test_particle__blossoms(d):
        if isinstance(d, renpy.display.particle.Particles):
            return [d]

        return [p for child in d.visit() for p in test_particle__blossoms(child)]

    def test_particle__check_menu(returning=False):
        d = renpy.get_displayable("test_particle__menu", "snow")
        blossoms = test_particle__blossoms(d)
        assert len(blossoms) == 4

        for blossom, count in zip(blossoms, (80, 120, 20, 15)):
            assert len(blossom.particles) == count
            assert all(0 < sprite.y < config.screen_height for sprite, p in blossom.particles)
            if returning:
                assert all(p.start > 0 for sprite, p in blossom.particles)


image test_particle__snow = Composite(
    (1920, 1080),
    (0, 0), SnowBlossom(Solid("#fff", xysize=(4, 4)), 80, 27, (80, 120), (250, 450),
        fast=True, animation=True, distribution=test_particle__midpoint),
    (0, 0), SnowBlossom(Solid("#fff", xysize=(5, 5)), 120, 12, (50, 100), (200, 300),
        fast=True, animation=True, distribution=test_particle__midpoint),
    (0, 0), SnowBlossom(Solid("#fff", xysize=(6, 6)), 20, 149,
        fast=True, animation=True, distribution=test_particle__midpoint),
    (0, 0), SnowBlossom(Solid("#fff", xysize=(7, 7)), 15, 122,
        fast=True, animation=True, distribution=test_particle__midpoint),
)


screen test_particle__menu():
    tag menu

    add "test_particle__snow" id "snow"
    textbutton "Next menu" action ShowMenu("test_particle__other_menu")


screen test_particle__other_menu():
    tag menu

    textbutton "Return to snow" action ShowMenu("test_particle__menu")


testsuite particle:
    after testcase:
        run ShowMenu("main_menu")

    testcase snowblossom_menu_return:
        description "GH-7356: Fast SnowBlossom fills a Composite again after returning to its menu."

        run ShowMenu("test_particle__menu")
        pause 0.1
        $ test_particle__check_menu()

        click "Next menu"
        assert screen "test_particle__other_menu"
        pause 0.1
        click "Return to snow"
        assert screen "test_particle__menu"
        pause 0.1
        $ test_particle__check_menu(returning=True)
