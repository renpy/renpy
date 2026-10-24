import unittest
from unittest.mock import Mock, patch

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

import renpy
from renpy.display.render import Render


class TestRenderSubsurface(unittest.TestCase):
    """Tests for Render.subsurface handling of zero-sized intermediate renders."""

    def setUp(self) -> None:
        patcher = patch.object(renpy.display, "draw", Mock())
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_zero_width_non_clipping_render_retains_and_clips_child_surface(self) -> None:
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
        self.assertEqual((tx, ty), (10, 5))
        self.assertEqual(len(text_sub.children), 1)

        holder_sub, hx, hy, _, _ = text_sub.children[0]
        self.assertEqual((hx, hy), (60, 20))
        self.assertEqual(len(holder_sub.children), 1)

        icon_sub, ix, iy, _, _ = holder_sub.children[0]
        self.assertEqual((ix, iy), (0, 0))
        self.assertEqual(len(icon_sub.children), 1)

        leaf_surf, lx, ly, _, _ = icon_sub.children[0]
        self.assertEqual((lx, ly), (0, 0))
        self.assertEqual(leaf_surf.get_size(), (30, 25))

    def test_zero_width_non_clipping_render_supports_negative_child_offset_for_rtl(self) -> None:
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

        self.assertEqual((tx + hx + ix + lx, ty + hy + iy + ly), (65, 15))
        self.assertEqual(leaf_surf.get_size(), (25, 30))

    def test_zero_width_clipping_render_is_excluded(self) -> None:
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
        self.assertEqual(clipped.children, [])


if __name__ == "__main__":
    unittest.main()
