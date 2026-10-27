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


def test_zero_width_non_clipping_render_retains_and_clips_child_surface():
    """
    A zero-width non-clipping Render (such as CTCPauseHolder) inside a
    subsurfaced container retains its child surface and clips it to the
    container's subsurface bounds.
    """

    root = Render(200, 50)
    text_render = Render(100, 80)
    ctc_holder = Render(0, 40)
    icon_render = Render(30, 40)
    surf = renpy.display.pgrender.surface((30, 40), True)

    icon_render.blit(surf, (0, 0))
    ctc_holder.blit(icon_render, (0, 0))
    text_render.blit(ctc_holder, (60, 20))
    root.blit(text_render, (10, 5))

    clipped = root.subsurface((0, 0, 200, 50), focus=True)

    # The icon is at x = 10 + 60 = 70 (width 30, completely within 200)
    # and y = 5 + 20 = 25 (height 40, clipped to 50 - 25 = 25).
    text_sub, tx, ty, _, _ = clipped.children[0]
    assert (tx, ty) == (10, 5)
    assert len(text_sub.children) == 1

    holder_sub, hx, hy, _, _ = text_sub.children[0]
    assert (hx, hy) == (60, 20)
    assert len(holder_sub.children) == 1

    icon_sub, ix, iy, _, _ = holder_sub.children[0]
    assert (ix, iy) == (0, 0)
    assert len(icon_sub.children) == 1

    leaf_surf, lx, ly, _, _ = icon_sub.children[0]
    assert (lx, ly) == (0, 0)
    assert leaf_surf.get_size() == (30, 25)


def test_zero_width_non_clipping_render_supports_negative_child_offset_for_rtl():
    """
    A zero-width non-clipping Render with a negatively offset child (such
    as CTCPauseHolder in RTL mode) retains and positions the child relative
    to the enclosing subsurface bounds.
    """

    root = Render(200, 50)
    text_render = Render(100, 40)
    ctc_holder = Render(0, 30)
    icon_render = Render(25, 30)
    surf = renpy.display.pgrender.surface((25, 30), True)

    icon_render.blit(surf, (0, 0))
    ctc_holder.blit(icon_render, (-25, 0))
    text_render.blit(ctc_holder, (40, 5))
    root.blit(text_render, (50, 10))

    clipped = root.subsurface((0, 0, 200, 50), focus=True)

    text_sub, tx, ty, _, _ = clipped.children[0]
    holder_sub, hx, hy, _, _ = text_sub.children[0]
    icon_sub, ix, iy, _, _ = holder_sub.children[0]
    leaf_surf, lx, ly, _, _ = icon_sub.children[0]

    assert (tx + hx + ix + lx, ty + hy + iy + ly) == (65, 15)
    assert leaf_surf.get_size() == (25, 30)


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
