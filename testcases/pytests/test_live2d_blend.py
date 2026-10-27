"""
Tests for the load-time analysis of Live2D Cubism 5.3 blend modes and
offscreens. The expected values come from the csmColorBlendType and
csmAlphaBlendType values in Live2DCubismCore.h, where a blend mode stores the
color type in its low byte and the alpha type in the next byte.
"""

from renpy.gl2.live2dblend import (
    ALPHA_ATOP,
    ALPHA_OUT,
    ALPHA_OVER,
    COLOR_ADD_COMPATIBLE,
    COLOR_MULTIPLY_COMPATIBLE,
    COLOR_NORMAL,
    KIND_ADD_COMPATIBLE,
    KIND_ADVANCED,
    KIND_MULTIPLY_COMPATIBLE,
    KIND_NORMAL,
    BlendAnalysis,
    classify_blend_mode,
    decode_blend_mode,
    find_offscreen,
    flags_blend_mode,
)

MULTIPLY = 6
HARD_LIGHT = 14
COLOR = 17


def mode(color: int, alpha: int) -> int:
    """
    Encodes a blend mode the way Cubism Core does.
    """

    return color | (alpha << 8)


def analyze_blend(drawable_modes, drawable_parts, offscreen_modes=(), offscreen_owners=(), mask_counts=None):
    """
    Analyzes a model with these parts:

    0 - the root part.
    1 - a child of 0, owning offscreen 0.
    2 - a child of 1, with no offscreen.
    3 - a child of 2, owning offscreen 1.
    """

    part_parents = [-1, 0, 1, 2]
    part_offscreens = [-1, 0, -1, 1]

    if mask_counts is None:
        mask_counts = [0] * len(offscreen_modes)

    return BlendAnalysis(
        drawable_modes,
        drawable_parts,
        part_parents,
        part_offscreens,
        offscreen_modes,
        offscreen_owners,
        mask_counts,
    )


def test_splits_color_and_alpha():
    """Decoding a blend mode returns its color type and alpha type, taken from the two bytes of the mode."""

    assert decode_blend_mode(mode(HARD_LIGHT, ALPHA_ATOP)) == (HARD_LIGHT, ALPHA_ATOP)
    assert decode_blend_mode(mode(COLOR, ALPHA_OUT)) == (COLOR, ALPHA_OUT)


def test_compatible_modes_ignore_alpha():
    """
    The framework draws compatible modes with the 5.2 blend functions,
    whatever the alpha type is.
    """

    assert decode_blend_mode(mode(COLOR_ADD_COMPATIBLE, ALPHA_OUT)) == (COLOR_ADD_COMPATIBLE, ALPHA_OVER)
    assert decode_blend_mode(mode(COLOR_MULTIPLY_COMPATIBLE, ALPHA_ATOP)) == (COLOR_MULTIPLY_COMPATIBLE, ALPHA_OVER)


def test_unknown_types_fall_back_to_normal_over():
    """
    An unrecognized color type decodes as normal color, and an unrecognized alpha type decodes as
    alpha over. Known types that are not compatible keep their values.
    """

    assert decode_blend_mode(mode(COLOR + 1, ALPHA_ATOP)) == (COLOR_NORMAL, ALPHA_ATOP)
    assert decode_blend_mode(mode(MULTIPLY, 5)) == (MULTIPLY, ALPHA_OVER)


def test_kinds():
    """Each blend mode is classified into the drawing path it needs: normal, add-compatible, multiply-compatible, or advanced."""

    assert classify_blend_mode(mode(COLOR_NORMAL, ALPHA_OVER)) == KIND_NORMAL
    assert classify_blend_mode(mode(COLOR_ADD_COMPATIBLE, ALPHA_ATOP)) == KIND_ADD_COMPATIBLE
    assert classify_blend_mode(mode(COLOR_MULTIPLY_COMPATIBLE, ALPHA_OVER)) == KIND_MULTIPLY_COMPATIBLE
    assert classify_blend_mode(mode(MULTIPLY, ALPHA_OVER)) == KIND_ADVANCED


def test_normal_with_other_alpha_is_advanced():
    """
    Normal color blending with a non-over alpha type depends on what's
    beneath, so it can't use the fixed-function path.
    """

    assert classify_blend_mode(mode(COLOR_NORMAL, ALPHA_OUT)) == KIND_ADVANCED


def test_nearest_ancestor():
    """
    find_offscreen walks up the part hierarchy and returns the nearest ancestor's offscreen, or -1 when
    no ancestor owns one. Part -1 means no part and always gives -1.
    """

    part_parents = [-1, 0, 1]
    part_offscreens = [0, -1, -1]

    assert find_offscreen(2, part_parents, part_offscreens) == 0
    assert find_offscreen(-1, part_parents, part_offscreens) == -1


def test_part_cycle_terminates():
    """
    A malformed part hierarchy whose parents form a cycle, with no offscreen, must not loop forever. The
    walk stops and returns -1.
    """

    assert find_offscreen(0, [1, 0], [-1, -1]) == -1


def test_model_without_offscreens_is_one_container():
    """
    Without offscreens, every drawable is drawn into the model, whatever
    its parent part and blend mode.
    """

    analysis = BlendAnalysis(
        [mode(COLOR_NORMAL, ALPHA_OVER), mode(COLOR_ADD_COMPATIBLE, ALPHA_OVER), mode(MULTIPLY, ALPHA_OVER)],
        [0, 2, -1],
        [-1, 0, 1],
        [-1, -1, -1],
        [],
        [],
        [],
    )

    assert analysis.containers == [[0, 1, 2]]
    assert analysis.offscreen_parents == []
    assert analysis.can_flatten == []
    assert analysis.drawable_kinds == [KIND_NORMAL, KIND_ADD_COMPATIBLE, KIND_ADVANCED]


def test_flags_analysis_matches_compatible_modes():
    """
    With a Cubism Core that predates blend modes, the analysis is built
    from the Cubism 5.2 blend flags, and must classify drawables the same
    way the compatible blend modes reported by a newer Core are.
    """

    modes = [flags_blend_mode(False, False), flags_blend_mode(True, False), flags_blend_mode(False, True)]

    analysis = BlendAnalysis(modes, [-1, -1, -1], [], [], [], [], [])

    assert analysis.containers == [[0, 1, 2]]
    assert analysis.drawable_kinds == [KIND_NORMAL, KIND_ADD_COMPATIBLE, KIND_MULTIPLY_COMPATIBLE]


def test_nested_offscreens():
    """
    Drawables go into the offscreen of their nearest ancestor part, and an
    offscreen goes into the offscreen of its owner's ancestors, not its own.
    Members are numbered with drawables first, then offscreens.
    """

    normal = mode(COLOR_NORMAL, ALPHA_OVER)

    analysis = analyze_blend(
        [normal, normal, normal, normal],
        [0, 2, 3, -1],
        [normal, normal],
        [1, 3],
    )

    assert analysis.offscreen_parents == [0, 1]
    assert analysis.containers == [[0, 3, 4], [1, 5], [2]]


def test_flatten_requires_normal_members():
    """
    An offscreen can be flattened into its parent only when every member drawn into it uses normal
    color blending with alpha over. An advanced or additive member prevents flattening.
    """

    normal = mode(COLOR_NORMAL, ALPHA_OVER)

    all_normal = analyze_blend([normal], [2], [normal], [1])
    assert all_normal.can_flatten == [True]

    advanced_member = analyze_blend([mode(MULTIPLY, ALPHA_ATOP)], [2], [normal], [1])
    assert advanced_member.can_flatten == [False]

    add_member = analyze_blend([mode(COLOR_ADD_COMPATIBLE, ALPHA_OVER)], [2], [normal], [1])
    assert add_member.can_flatten == [False]


def test_flatten_requires_normal_offscreen_without_masks():
    """
    An offscreen can be flattened only when it composites normally and has no masks. An advanced blend
    mode on the offscreen or a mask on it prevents flattening, even when all its members are normal.
    """

    normal = mode(COLOR_NORMAL, ALPHA_OVER)

    advanced = analyze_blend([normal], [2], [mode(HARD_LIGHT, ALPHA_OVER)], [1])
    assert advanced.can_flatten == [False]

    masked = analyze_blend([normal], [2], [normal], [1], mask_counts=[1])
    assert masked.can_flatten == [False]


def test_flatten_depends_on_nested_offscreen_composite_only():
    """
    A nested offscreen is drawn in isolation, so an offscreen containing
    it can be flattened when the nested one composites normally, even if
    the nested offscreen's own members don't.
    """

    normal = mode(COLOR_NORMAL, ALPHA_OVER)

    nested_normal = analyze_blend([mode(MULTIPLY, ALPHA_OVER)], [3], [normal, normal], [1, 3])
    assert nested_normal.can_flatten == [True, False]

    nested_advanced = analyze_blend([normal], [3], [normal, mode(MULTIPLY, ALPHA_OVER)], [1, 3])
    assert nested_advanced.can_flatten == [False, False]
