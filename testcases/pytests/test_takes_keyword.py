import functools

import pytest

from renpy.object import _takes_keyword, takes_keyword


def positional_or_keyword(layer, tag=None):
    """
    A function with an ordinary parameter named tag.
    """


def keyword_only(layer, *, tag=None):
    """
    A function with a keyword-only parameter named tag.
    """


def var_keyword(layer, **kwargs):
    """
    A function that accepts any keyword through **kwargs.
    """


def positional_only(layer, tag, /):
    """
    A function whose tag parameter can't be passed by keyword.
    """


def layer_only(layer="master"):
    """
    A function with no tag parameter and no **kwargs.
    """


def var_positional(*args):
    """
    A function that accepts only positional arguments.
    """


@pytest.mark.parametrize(
    ("function", "expected"),
    [
        (positional_or_keyword, True),
        (keyword_only, True),
        (var_keyword, True),
        (positional_only, False),
        (layer_only, False),
        (var_positional, False),
        (lambda layer: None, False),
        (functools.partial(positional_or_keyword, "master"), True),
    ],
)
def test_takes_keyword(function, expected):
    """
    Checks each kind of parameter that can or can't receive the tag keyword.
    """

    assert takes_keyword(function, "tag") is expected


def test_method_takes_keyword():
    """
    A bound method is judged by its signature without self.
    """

    class C:
        def method(self, tag=None):
            pass

    assert takes_keyword(C().method, "tag")
    assert not takes_keyword(C().method, "self")


def test_unknown_signature_is_false():
    """
    A callable whose signature can't be determined (the builtin max has none) is treated as not taking it.
    """

    assert not takes_keyword(max, "tag")


def test_unhashable_callable():
    """
    An unhashable callable can't be used as a cache key, but still gets an answer.
    """

    class Unhashable:
        def __eq__(self, other):
            """
            Defining __eq__ without __hash__ makes instances unhashable.
            """

            return self is other

        def __call__(self, layer, tag=None):
            pass

    assert takes_keyword(Unhashable(), "tag")


def test_cache_is_limited_to_fifty_entries():
    """
    The cache holds 50 entries, so the 51st distinct callable evicts the first.
    """

    _takes_keyword.cache_clear()

    functions = [lambda layer, tag=None: None for _ in range(51)]

    for f in functions:
        takes_keyword(f, "tag")

    info = _takes_keyword.cache_info()

    assert info.maxsize == 50
    assert info.currsize == 50
