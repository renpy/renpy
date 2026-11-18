# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Load-time analysis of how the drawables and offscreens of a Live2D model are
blended, including the blend modes and offscreens introduced in Cubism 5.3.

This is kept separate from the Cython model so that the structure of a model
can be computed (and tested) without a Live2D library or a GPU. A model is
described by a tree of containers. Container 0 is the model itself, and
container ``j + 1`` is offscreen ``j``. Members of a container are identified
by their index in the render order array - drawable ``i`` is member ``i``, and
offscreen ``j`` is member ``drawable_count + j``.
"""

from collections.abc import Sequence

COLOR_NORMAL = 0
COLOR_ADD_COMPATIBLE = 1
COLOR_MULTIPLY_COMPATIBLE = 2
COLOR_MAX = 17
"The largest color blend type that Ren'Py knows about (Color)."

ALPHA_OVER = 0
ALPHA_ATOP = 1
ALPHA_OUT = 2
ALPHA_CONJOINT_OVER = 3
ALPHA_DISJOINT_OVER = 4

KIND_NORMAL = 0
"Drawn with premultiplied alpha over, the same as Cubism 5.2 and earlier."

KIND_ADD_COMPATIBLE = 1
"Drawn with the Cubism 5.2 additive blend function."

KIND_MULTIPLY_COMPATIBLE = 2
"Drawn with the Cubism 5.2 multiplicative blend function."

KIND_ADVANCED = 3
"Requires the live2d.blend shader and a copy of what's been drawn beneath."


def decode_blend_mode(mode: int) -> tuple[int, int]:
    """
    Splits a Cubism blend mode into a (color, alpha) pair.

    Unknown color or alpha blend types are treated as Normal or Over, which
    matches the Cubism framework. The compatible color types ignore the
    alpha blend type, so Over is returned for them.
    """

    color = mode & 0xFF
    alpha = (mode >> 8) & 0xFF

    if color > COLOR_MAX:
        color = COLOR_NORMAL

    if alpha > ALPHA_DISJOINT_OVER:
        alpha = ALPHA_OVER

    if color == COLOR_ADD_COMPATIBLE or color == COLOR_MULTIPLY_COMPATIBLE:
        alpha = ALPHA_OVER

    return color, alpha


def classify_blend_mode(mode: int) -> int:
    """
    Returns the KIND_* constant that describes how a blend mode is drawn.
    """

    color, alpha = decode_blend_mode(mode)

    if color == COLOR_ADD_COMPATIBLE:
        return KIND_ADD_COMPATIBLE

    if color == COLOR_MULTIPLY_COMPATIBLE:
        return KIND_MULTIPLY_COMPATIBLE

    if color == COLOR_NORMAL and alpha == ALPHA_OVER:
        return KIND_NORMAL

    return KIND_ADVANCED


def flags_blend_mode(additive: bool, multiplicative: bool) -> int:
    """
    Returns the blend mode of a drawable with the given Cubism 5.2 blend
    flags, for use with a Cubism Core that doesn't report blend modes.
    """

    if additive:
        return COLOR_ADD_COMPATIBLE

    if multiplicative:
        return COLOR_MULTIPLY_COMPATIBLE

    return COLOR_NORMAL


def find_offscreen(part: int, part_parents: Sequence[int], part_offscreens: Sequence[int]) -> int:
    """
    Returns the index of the offscreen owned by `part` or its nearest
    ancestor, or -1 if there is no such offscreen. `part` may be -1.
    """

    seen = 0

    while part >= 0 and seen <= len(part_parents):
        offscreen = part_offscreens[part]

        if offscreen >= 0:
            return offscreen

        part = part_parents[part]
        seen += 1

    return -1


class BlendAnalysis:
    """
    The static structure used to render a model. A model without offscreens
    has a single container holding every drawable.
    """

    drawable_kinds: list[int]
    "The KIND_* constant for each drawable."

    drawable_colors: list[int]
    "The decoded color blend type of each drawable."

    drawable_alphas: list[int]
    "The decoded alpha blend type of each drawable."

    offscreen_kinds: list[int]
    "The KIND_* constant used to composite each offscreen."

    offscreen_colors: list[int]
    "The decoded color blend type of each offscreen."

    offscreen_alphas: list[int]
    "The decoded alpha blend type of each offscreen."

    offscreen_parents: list[int]
    "The container index (0 for the model, j + 1 for offscreen j) that each offscreen is drawn into."

    containers: list[list[int]]
    "For each container, the members drawn into it, in index order."

    can_flatten: list[bool]
    """
    For each offscreen, True if drawing its members directly into its parent
    gives the same result as compositing it, provided the offscreen has an
    opacity of 1, a white multiply color, and a black screen color.
    """

    def __init__(
        self,
        drawable_modes: Sequence[int],
        drawable_parts: Sequence[int],
        part_parents: Sequence[int],
        part_offscreens: Sequence[int],
        offscreen_modes: Sequence[int],
        offscreen_owners: Sequence[int],
        offscreen_mask_counts: Sequence[int],
    ):
        drawable_count = len(drawable_modes)
        offscreen_count = len(offscreen_modes)

        self.drawable_kinds = [classify_blend_mode(i) for i in drawable_modes]
        self.drawable_colors = [decode_blend_mode(i)[0] for i in drawable_modes]
        self.drawable_alphas = [decode_blend_mode(i)[1] for i in drawable_modes]

        self.offscreen_kinds = [classify_blend_mode(i) for i in offscreen_modes]
        self.offscreen_colors = [decode_blend_mode(i)[0] for i in offscreen_modes]
        self.offscreen_alphas = [decode_blend_mode(i)[1] for i in offscreen_modes]

        self.containers = [[] for _ in range(offscreen_count + 1)]
        self.offscreen_parents = []

        for i in range(drawable_count):
            container = find_offscreen(drawable_parts[i], part_parents, part_offscreens) + 1
            self.containers[container].append(i)

        for j in range(offscreen_count):
            owner = offscreen_owners[j]
            parent_part = part_parents[owner] if owner >= 0 else -1
            container = find_offscreen(parent_part, part_parents, part_offscreens) + 1

            if container == j + 1:
                container = 0

            self.offscreen_parents.append(container)
            self.containers[container].append(drawable_count + j)

        self.can_flatten = []

        for j in range(offscreen_count):
            flat = self.offscreen_kinds[j] == KIND_NORMAL and offscreen_mask_counts[j] == 0

            for m in self.containers[j + 1]:
                if m < drawable_count:
                    flat = flat and self.drawable_kinds[m] == KIND_NORMAL
                else:
                    flat = flat and self.offscreen_kinds[m - drawable_count] == KIND_NORMAL

            self.can_flatten.append(flat)
