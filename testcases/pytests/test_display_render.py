"""
Tests for Render.subsurface handling of zero-sized intermediate renders.
"""

import pytest

import renpy
from renpy.display.render import Render


@pytest.fixture(autouse=True)
def draw(mocker):
    """Replaces the display's draw object, so rendering doesn't touch a real graphics device."""

    return mocker.patch.object(renpy.display, "draw", mocker.Mock())


def visible_rects(render, xo=0, yo=0):
    """
    Returns the (x, y, width, height) of every surface blitted anywhere under a render, in the render's
    own coordinates, so tests can check where content is drawn without depending on how the render tree is
    nested.
    """

    rects = []
    for child, x, y, _focus, _main in render.children:
        if isinstance(child, Render):
            rects.extend(visible_rects(child, xo + x, yo + y))
        else:
            rects.append((xo + x, yo + y, *child.get_size()))
    return rects


@pytest.mark.parametrize(
    ("text_size", "holder_size", "icon_size", "text_pos", "holder_pos", "icon_pos", "expected"),
    [
        # An icon whose bottom edge extends past the 50 pixel high container, so it is clipped. It is drawn at
        # x = 10 + 60 = 70 and y = 5 + 20 = 25, and keeps only the 25 rows that are inside the container.
        ((100, 80), (0, 40), (30, 40), (10, 5), (60, 20), (0, 0), [(70, 25, 30, 25)]),
        # The right-to-left layout of CTCPauseHolder, where the icon has a negative offset in the holder. It is
        # drawn at x = 50 + 40 - 25 = 65 and y = 10 + 5 = 15, fully inside the container.
        ((100, 40), (0, 30), (25, 30), (50, 10), (40, 5), (-25, 0), [(65, 15, 25, 30)]),
    ],
    ids=["ltr-clipped", "rtl-negative-offset"],
)
def test_zero_width_non_clipping_render_retains_and_clips_child_surface(
    text_size, holder_size, icon_size, text_pos, holder_pos, icon_pos, expected
):
    """
    A zero-width non-clipping Render (such as CTCPauseHolder) inside a subsurfaced container retains its
    child surface, positions it relative to the container (including with a negative offset, as in RTL
    mode), and clips it to the container's subsurface bounds. The test checks where the surface ends up
    and how large it is, not how the intermediate renders are nested.
    """

    root = Render(200, 50)
    text_render = Render(*text_size)
    ctc_holder = Render(*holder_size)
    icon_render = Render(*icon_size)
    surf = renpy.display.pgrender.surface(icon_size, True)

    icon_render.blit(surf, (0, 0))
    ctc_holder.blit(icon_render, icon_pos)
    text_render.blit(ctc_holder, holder_pos)
    root.blit(text_render, text_pos)

    clipped = root.subsurface((0, 0, 200, 50), focus=True)
    assert visible_rects(clipped) == expected


def test_zero_width_clipping_render_is_excluded():
    """
    A zero-width Render with xclipping enabled clips its children to zero
    width and is excluded by subsurface.
    """

    root = Render(100, 50)
    holder = Render(0, 30)
    holder.xclipping = True
    surf = renpy.display.pgrender.surface((20, 30), True)
    holder.blit(surf, (0, 0))
    root.blit(holder, (10, 10))

    clipped = root.subsurface((0, 0, 100, 50), focus=True)
    assert clipped.children == []


def test_callable_receives_displayable_dimensions(mocker) -> None:
    """A callable focus mask is called with coordinates relative to the displayable and the full displayable size."""
    render = Render(120, 60)
    displayable = object()
    result = mocker.Mock(return_value=True)
    mask = mocker.Mock(return_value=result)
    render.add_focus(displayable, None, 0, 0, 120, 60, 10, 5, mask)

    assert render.focus_at_point(30, 20, None) == (displayable, None, None)
    mask.assert_called_once_with(20, 15)
    result.assert_called_once_with(20, 15, 110, 55)


@pytest.mark.parametrize("subpixel", [False, True], ids=["pixel", "subpixel"])
@pytest.mark.parametrize("point", [(-1, 2), (40, 2), (3, -1), (3, 20)], ids=["left", "right", "above", "below"])
def test_callable_mask_remains_focusable_after_nested_clipping(subpixel: bool, point: tuple[int, int], mocker) -> None:
    """
    After two nested clipping subsurfaces, a point inside the clip is focused and the mask is called with the
    translated coordinates, while a point outside either clip is not focused and the mask is not called again.
    """
    render = Render(120, 60)
    displayable = object()
    result = mocker.Mock(return_value=True)
    mask = mocker.Mock(return_value=result)
    render.add_focus(displayable, None, 0, 0, 120, 60, 0, 0, mask)

    clipped = render.subsurface((20, 10, 70, 30), focus=True, subpixel=subpixel)
    clipped = clipped.subsurface((5, 4, 40, 20), focus=True, subpixel=subpixel)

    assert clipped.focus_at_point(3, 2, None) == (displayable, None, None)
    mask.assert_called_once_with(28, 16)
    result.assert_called_once_with(28, 16, 120, 60)

    assert clipped.focus_at_point(*point, None) is None
    assert mask.call_count == 1
