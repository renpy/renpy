import renpy

python_object = object

"""renpy
init offset = -100

python early in layeredimage:
"""
# Do not participate in saves.
_constant = True

from typing import Container, Literal
from collections.abc import Iterable
from collections import defaultdict
from renpy.atl import RawBlock, parse_atl
from renpy.display.transform import ATLTransform
from store import Transform, ConditionSwitch, Fixed, Null, config, Text, eval, At

type Imageable = RawBlock | str | None

ATL_PROPERTIES = frozenset(renpy.atl.PROPERTIES)

# The properties for the Fixed wrapping the layeredimage
FIXED_PROPERTIES = frozenset(renpy.sl2.slproperties.position_property_names).union(
    renpy.sl2.slproperties.box_property_names
)

# The properties taken at the base level of the layeredimage
BASE_PROPERTIES = (
    ATL_PROPERTIES | FIXED_PROPERTIES | {"image_format", "format_function", "attribute_function", "offer_screen", "at"}
)
# The properties for all layers
LAYER_PROPERTIES = ATL_PROPERTIES | {"when", "if_all", "if_any", "if_not", "at"}
# The properties for the attribute layers
ATTRIBUTE_PROPERTIES = LAYER_PROPERTIES | {"variant", "default"}
# The properties for the group statement
GROUP_BLOCK_PROPERTIES = LAYER_PROPERTIES | {"auto"}
GROUP_INLINE_PROPERTIES = GROUP_BLOCK_PROPERTIES | {"prefix", "variant", "multiple"}
# The properties for the if/elif/else layers
CONDITION_PROPERTIES = LAYER_PROPERTIES
# The properties for the always layers
ALWAYS_PROPERTIES = LAYER_PROPERTIES


# This is the default value for predict_all given to conditions.
predict_all = None


def format_function(what, name, group, variant, attribute, image, image_format, **kwargs):
    """
    :doc: li_ff

    This is called to format the information about an attribute
    or condition into a displayable. This can be replaced by a
    creator, but the new function should ignore unknown kwargs.

    `what`
        A string giving a description of the thing being formatted,
        which is used to create better error messages.

    `name`
        The name of the layeredimage.

    `group`
        The group of an attribute, None if not supplied or if it's
        part of a condition.

    `variant`
        The variant argument to the group, or None if it is not
        supplied.

    `attribute`
        The attribute itself.

    `image`
        Either a displayable or string.

    `image_format`
        The image_format argument of the LayeredImage.

    If `image` is None, then `name`, `group` (if not None), `variant` (if not None),
    and `attribute` are combined with underscores to create `image`, which
    will then be a string.

    If `images` is a string, and `image_format` is not None, `image` is formatted
    into the string to get the final displayable.

    So if `name` is "eileen", `group` is "expression", and
    `attribute` is "happy", `image` would be set to "eileen_expression_happy".
    If `image_format` is "images/{image}.png",
    the final image Ren'Py finds is "images/eileen_expression_happy.png".
    But note that it would have found the same image without the format
    argument.
    """

    if image is None:
        if name is None:
            raise Exception("Can't find an image name to format {}.".format(what))

        if attribute is None:
            raise Exception("Can't find an attribute name to format {}.".format(what))

        parts = [name]

        if group is not None:
            parts.append(group)

        if variant is not None:
            parts.append(variant)

        parts.append(attribute)

        image = "_".join(parts)

    if isinstance(image, str) and (image_format is not None):
        image = image_format.format(name=name, image=image)

    return image


def resolve_image(img: Imageable):
    if img is None:
        return None
    if isinstance(img, RawBlock):
        return ATLTransform(img)
    else:
        return eval(img)


def resolve_at(at: RawBlock | Transform | Iterable[Transform]) -> tuple[Transform, ...]:
    """
    Turns an ATL RawBlock, or a Transform, or an iterable of Transforms,
    into a tuple of transforms.
    """
    if isinstance(at, RawBlock):
        return (ATLTransform(at),)
    return renpy.easy.to_tuple(at)


class When(python_object):
    """
    Represents a when expression.
    Abstract base class.
    """

    __slots__ = ()

    def __init__(self):
        raise Exception("When is an abstract base class.")

    def check(self, attributes: set[str]) -> bool:
        raise Exception  # implemented in subclasses

    @staticmethod
    def parse(l) -> "When":
        return WhenOr.parse(l)


class WhenOr(When):
    __slots__ = ("left", "right")

    def __init__(self, left, right, /):
        self.left = left
        self.right = right

    def check(self, attributes):
        return self.left.check(attributes) or self.right.check(attributes)

    @staticmethod
    def parse(l) -> When:
        rv = WhenAnd.parse(l)
        while l.keyword("or"):  # or l.match(r"\|"):
            rv = WhenOr(rv, WhenAnd.parse(l))
        return rv


class WhenAnd(When):
    __slots__ = ("left", "right")

    def __init__(self, left, right, /):
        self.left = left
        self.right = right

    def check(self, attributes):
        return self.left.check(attributes) and self.right.check(attributes)

    @staticmethod
    def parse(l) -> When:
        rv = WhenNot.parse(l)
        while l.keyword("and"):  # or l.match(r"&"):
            rv = WhenAnd(rv, WhenNot.parse(l))
        return rv


class WhenNot(When):
    __slots__ = ("when",)

    def __init__(self, when, /):
        self.when = when

    def check(self, attributes):
        return not self.when.check(attributes)

    @staticmethod
    def parse(l) -> When:
        if l.keyword("not"):  # or l.match(r"\!"):
            return WhenNot(WhenNot.parse(l))
        else:
            return WhenAttribute.parse(l)


class WhenAttribute(When):
    __slots__ = ("attribute",)

    def __init__(self, attribute, /):
        self.attribute = attribute

    def check(self, attributes):
        return self.attribute in attributes

    @staticmethod
    def parse(l) -> When:
        if l.match(r"\("):
            rv = WhenOr.parse(l)
            l.require(r"\)", "closing parenthesis")
            return rv
        else:
            name = l.require(l.image_name_component, "attribute name")
            return WhenAttribute(name)


class Layer(object):
    """
    Abstract base class for our layers.
    """

    group_args = {}

    def __init__(
        self, if_all=[], if_any=[], if_not=[], at=(), group_args={}, *, when: When | str | None = None, **kwargs
    ):
        self.at = resolve_at(at)

        if isinstance(when, str):
            when = When.parse(renpy.lexer.lex_string(when))
        self.when = when
        self.if_all = renpy.easy.to_list(if_all)
        self.if_any = renpy.easy.to_list(if_any)
        self.if_not = renpy.easy.to_list(if_not)

        self.group_args = group_args
        self.transform_args = kwargs

    def check(self, attributes):
        if self.when is not None:
            if not self.when.check(attributes):
                return False

        for i in self.if_all:
            if i not in attributes:
                return False

        if self.if_any:
            for i in self.if_any:
                if i in attributes:
                    break
            else:
                return False

        for i in self.if_not:
            if i in attributes:
                return False

        return True

    def wrap(self, d):
        """
        Wraps a displayable in the at list and transform arguments.
        """

        d = At(d, *self.at)

        if self.group_args or self.transform_args:
            d = Transform(d)

            for k, v in self.group_args.items():
                setattr(d, k, v)

            for k, v in self.transform_args.items():
                setattr(d, k, v)

        return d

    def apply_format(self, li: "LayeredImage", /):
        """
        Abstract method on Layer.
        Actuates the displayable for this layer, by passing infos to li's format function.
        """
        raise NotImplementedError

    def get_displayable(self, attributes):
        """
        Abstract method on Layer.
        Returns the displayable for this layer.
        """
        raise NotImplementedError


class Attribute(Layer):
    """
    :doc: li
    :name: Attribute

    This is used to represent a layer of an LayeredImage that is
    controlled by an attribute. A single attribute can control
    multiple layers, in which case all layers corresponding to
    that attribute will be displayed.

    `group`
        A string giving the group the attribute is part of. This
        may be None, in which case a group with the same name as
        the attribute is created.

    `attribute`
        A string giving the name of the attribute.

    `image`
        If not None, this should be a displayable that is displayed when
        this attribute is shown.

    `default`
        If True, and no other attribute for the group is selected,
        this attribute is.

    The following keyword arguments are also known:

    `at`
        A transform or list of transforms that are applied to the
        image.

    `when`
        A string containing a ``when`` expression, described in the :ref:`when` section.
        The displayable is only shown when the expression is satisfied by
        the pool of attributes currently applied to the layeredimage.

    `variant`
        A string giving the variant of the attribute. This is used
        as part of finding the displayable when `image` is None.

    Other keyword arguments are interpreted as transform properties. If
    any are present, a transform is created that wraps the image. (For
    example, pos=(100, 200) can be used to offset the image by 100 pixels
    horizontally and 200 vertically.)

    If the `image` parameter is omitted or None, and the LayeredImage
    has been given the `image_format` parameter, the image_format is used
    to generate an image filename.
    """

    def __init__(self, group, attribute, image=None, default=False, *, prefix=None, variant=None, **kwargs):
        super().__init__(**kwargs)

        self.group = group
        self.raw_attribute = attribute

        if prefix is not None:
            attribute = prefix + "_" + attribute

        self.attribute = attribute
        self.image = image
        self.default = default
        self.variant = variant

    def apply_format(self, li: "LayeredImage"):
        self.image = self.wrap(
            li.format(
                what=f"Attribute ({self.group!r}, {self.attribute!r})",
                group=self.group,
                variant=self.variant,
                attribute=self.raw_attribute,
                image=self.image,
            )
        )

    def get_displayable(self, attributes):
        if self.attribute not in attributes:
            return None

        if not self.check(attributes):
            return None

        return self.image


class Condition(Layer):
    """
    :doc: li
    :name: Condition

    When the condition is true, the layer is displayed. Otherwise, nothing
    is displayed.

    This is used to implement a single ``if``, ``elif`` **or** ``else``
    layeredimage statement (for ``else``, `condition` should be "True").
    Several Conditions can then be passed to a :class:`ConditionGroup` to
    emulate a full if/elif/else statement.

    `condition`
        This should be a string giving a Python condition that determines
        if the layer is displayed.

    `image`
        If not None, this should be a displayable that is displayed when
        the condition is true.

    `when`
        A string containing a ``when`` expression, described in the :ref:`when` section.
        The condition is only evaluated when the expression is satisfied by
        the pool of attributes currently applied to the layeredimage.

    `at`
        A transform or list of transforms that are applied to the image.

    Other keyword arguments are interpreted as transform properties. If any
    is present, a transform is created that wraps the image. (For example,
    pos=(100, 200) can be used to offset the image by 100 pixels
    horizontally and 200 vertically.)
    """

    at = []

    def __init__(self, condition, image, **kwargs):
        super().__init__(**kwargs)

        self.condition = condition
        self.image = image

    def apply_format(self, li: "LayeredImage"):
        self.image = self.wrap(
            li.format(
                what=f"Condition ({self.condition})",
                image=self.image,
            )
        )

    def get_displayable(self, attributes):
        if not self.check(attributes):
            return None

        return ConditionSwitch(
            self.condition,
            self.image,
            None,
            Null(),
            predict_all=predict_all,
        )


class ConditionGroup(Layer):
    """
    :doc: li
    :name: ConditionGroup

    Takes a list of :class:`Condition` to combine them into a single
    :func:`ConditionSwitch`.

    Implements the if/elif/else statement.
    """

    def __init__(self, conditions):
        super().__init__()

        self.conditions = conditions

    def apply_format(self, li: "LayeredImage"):
        for i in self.conditions:
            i.apply_format(li)

    def get_displayable(self, attributes):
        args = []

        for i in self.conditions:
            if not i.check(attributes):
                continue

            args.append(i.condition)
            args.append(i.image)

        args.append(None)
        args.append(Null())

        return ConditionSwitch(*args, predict_all=predict_all)


class Always(Layer):
    """
    :undocumented:
    :name: Always

    This is used for a displayable that is always shown.

    `image`
        The displayable to show.

    `default`
        If True, and no other attribute for the group is selected,
        this attribute is.

    `at`
        A transform or list of transforms that are applied to the
        image.

    `when`
        A string containing a ``when`` expression, described in the :ref:`when` section.
        The displayable is only shown when the expression is satisfied by
        the pool of attributes currently applied to the layeredimage.
    """

    def __init__(self, image, **kwargs):
        super().__init__(**kwargs)

        self.image = image

    def apply_format(self, li: "LayeredImage"):
        self.image = self.wrap(
            li.format(
                "Always",
                image=self.image,
            )
        )

    def get_displayable(self, attributes):
        if not self.check(attributes):
            return None

        return self.image


class LayeredImage(object):
    """
    :doc: li
    :name: LayeredImage

    This is an image-like object that, when shown with the proper set of
    attributes, shows a displayable created by compositing together the
    displayables associated with those attribute.

    `attributes`
        This must be a list of Attribute, Condition, ConditionGroup or
        :doc:`displayable <displayables>` objects. Each one
        reflects a displayable that may or may not be displayed as part
        of the image. The items in this list are in back-to-front order,
        with the first item further from the viewer and the last
        closest.
        Passing a displayable directly is the equivalent of the `always`
        layeredimage statement.

    `at`
        A transform or list of transforms that are applied to the displayable
        after it is parameterized.

    `name`
        The name of the layeredimage. This is used as part of the names
        of image components.

    `image_format`
        When a given image is a string, and this is supplied, the image name
        is interpolated into `image_format` to make an image file. For example,
        "sprites/eileen/{image}.png" will look for the image in a subdirectory
        of sprites. (This is not used by auto groups, which look for images and
        not image files.)

    `format_function`
        A function that is used instead of `layeredimage.format_function` to format
        the image information into a displayable.

    `attribute_function`
        If not None, a function that's called with a set of attributes supplied to
        the image, and returns the set of attributes used to select layers. This is
        called when determining the layers to display, after the attribute themselves
        have been chosen. It can be used to express complex dependencies between attributes
        or select attributes at random.

    `offer_screen`
        Sets whether or not the available area is taken into account as for how children
        are placed and how they are sized (when they have variable size). If False, the
        available area is considered, and if True it is not. If None, defaults to
        :var:`config.layeredimage_offer_screen`.

    Additional keyword arguments may contain transform properties. If
    any are present, a transform is created that wraps the result image.
    Remaining keyword arguments are passed to a Fixed that is created to hold
    the layer. Unless explicitly overridden, xfit and yfit are set to true on
    the Fixed, which means it will shrink to the smallest size that fits all
    of the layer images it is showing.

    A LayeredImage is not a displayable, and can't be used in all the
    places a displayable can be used. This is because it requires an image
    name (generally including image attributes) to be provided. As such,
    it should either be displayed through a scene or show statement, or by
    an image name string used as a displayable.
    """

    attribute_function = None
    transform_args = {}
    offer_screen = None

    def __init__(
        self,
        attributes,
        at=[],
        name=None,
        image_format=None,
        format_function=format_function,
        attribute_function=None,
        offer_screen=None,
        **kwargs,
    ):
        self.name = name
        self.image_format = image_format
        self.format_function = format_function
        self.attribute_function = attribute_function
        self.offer_screen = offer_screen

        self.attributes: list[Attribute] = []
        self.layers: list[Layer] = []

        self.attribute_to_groups: defaultdict[str, set[str]] = defaultdict(set)
        self.group_to_attributes: defaultdict[str, set[str]] = defaultdict(set)

        for i in attributes:
            self.add(i)

        self.at = resolve_at(at)

        kwargs.setdefault("xfit", True)
        kwargs.setdefault("yfit", True)

        self.fixed_args = {k: kwargs.pop(k) for k in FIXED_PROPERTIES.intersection(kwargs)}
        self.transform_args = kwargs

    def format(self, what, attribute=None, group=None, variant=None, image=None):
        ff = self.format_function or format_function
        return ff(
            what=what,
            name=self.name,
            group=group,
            variant=variant,
            attribute=attribute,
            image=image,
            image_format=self.image_format,
        )

    def add(self, a):
        """
        :doc: li

        `a`
            An Attribute, Condition, ConditionGroup or :doc:`displayable <displayables>`
            object.

        This method adds the provided layer to the list of layers of the layeredimage,
        as if it had been passed in the `attributes` argument to the constructor.
        """

        if not isinstance(a, Layer):
            a = Always(a)

        a.apply_format(self)
        self.layers.append(a)

        if isinstance(a, Attribute):
            self.attributes.append(a)

            if a.group is not None:
                self.attribute_to_groups[a.attribute].add(a.group)
                self.group_to_attributes[a.group].add(a.attribute)

    def get_banned(self, attributes):
        """
        Get the set of attributes that are incompatible with those
        in attributes.
        """
        banned = set()

        for a1 in attributes:
            for gn in self.attribute_to_groups[a1]:
                for a2 in self.group_to_attributes[gn]:
                    if a2 != a1:
                        banned.add(a2)

        return banned

    def _duplicate(self, args):
        attributes = set(args.args)
        unknown = set(args.args)
        banned = self.get_banned(attributes)

        for a in self.attributes:
            unknown.discard(a.attribute)

            if a.default and (a.attribute not in banned):
                attributes.add(a.attribute)

        if self.attribute_function:
            attributes = set(self.attribute_function(attributes))

            unknown = {i[1:] if i.startswith("-") else i for i in attributes}

            for a in self.attributes:
                unknown.discard(a.attribute)

                if a.variant:
                    unknown.discard(a.variant)

        rv = Fixed(**self.fixed_args)

        offer_screen = self.offer_screen
        if offer_screen is None:
            offer_screen = config.layeredimage_offer_screen
        if offer_screen:
            rv._offer_size = (config.screen_width, config.screen_height)

        for i in self.layers:
            d = i.get_displayable(attributes)

            if d is not None:
                if d._duplicatable:
                    d = d._duplicate(None)

                rv.add(d)

        if unknown and args.lint:
            args = args.copy()
            args.args = tuple(unknown)
            args.extraneous()

        if unknown and config.developer:
            message = [" ".join(args.name), "unknown attributes:", " ".join(sorted(unknown))]

            text = Text(
                "\n".join(message),
                size=16,
                xalign=0.5,
                yalign=0.5,
                textalign=0.5,
                color="#fff",
                outlines=[(1, "#0008", 0, 0)],
            )

            rv = Fixed(rv, text, fit_first=True)

        rv = At(rv, *self.at)

        if self.transform_args:
            rv = Transform(child=rv, **self.transform_args)

        return rv

    def _list_attributes(self, tag, attributes):
        banned = self.get_banned(attributes)

        group_attr_pairs: list[tuple[int, str]] = []

        seen = set()

        group_count = 0
        old_group = None

        for a in self.attributes:
            if a.group != old_group:
                old_group = a.group
                group_count += 1

            if a.attribute in banned:
                continue

            if a.attribute in seen:
                continue

            seen.add(a.attribute)
            group_attr_pairs.append((group_count, a.attribute))

        group_attr_pairs.sort()

        return [p[1] for p in group_attr_pairs]

    def _choose_attributes(self, tag, required, optional):
        rv = list(required)

        required = set(required)
        banned = self.get_banned(required)
        both = required & banned

        if both:
            raise Exception(f"The specified attributes for {tag} conflict: {', '.join(both)}")

        # The set of all available attributes.
        available_attributes = set(a.attribute for a in self.attributes)

        if optional is not None:
            optional = set(optional) & available_attributes
            rv.extend(optional - required - banned)

        # If there is an unknown attribute.
        if set(rv) - available_attributes:
            return None

        return tuple(rv)


def parse_property(
    l, final_properties: dict, expr_properties: dict, names: Container[str]
) -> Literal[0] | Literal[1] | Literal[2]:
    """
    Parses a property among the provided names and stores it inside the appropriate dict.
    Returns 0 if it didn't find any property,
    1 if it found a normal, inline property,
    and 2 if it found a block property.

    This function knows and decides which property is final and which is an expression.
    """

    check = l.checkpoint()

    name = l.word()

    if name is None:
        return 0

    if name not in names:
        l.revert(check)
        return 0

    if (name in final_properties) or (name in expr_properties):
        l.error(f"Duplicate property: {name}")

    if name in ("auto", "default", "multiple"):
        final_properties[name] = True
    elif name == "when":
        final_properties[name] = When.parse(l)
    elif name in ("if_all", "if_any", "if_not"):
        expr_properties[name] = l.require(l.simple_expression)
    elif name in ("variant", "prefix"):
        if (value := l.image_name_component()) is not None:
            final_properties[name] = value
        else:
            expr_properties[name] = l.require(l.simple_expression)
    elif name == "at":
        if l.keyword("transform"):
            l.require(":")
            l.expect_eol()
            l.expect_block("ATL")
            final_properties[name] = parse_atl(l.subblock_lexer())
            return 2
        else:
            expr_properties[name] = l.require(l.comma_expression)
    else:
        expr_properties[name] = l.require(l.simple_expression)

    return 1


def parse_displayable(l) -> Imageable:
    """
    Parses either "image:" opening an ATL block and returns a RawBlock,
    or a simple expression and returns an evaluable string,
    or None.
    """

    if l.keyword("image"):
        l.require(":")
        l.expect_eol()
        l.expect_block("ATL image")
        return parse_atl(l.subblock_lexer())
    else:
        return l.simple_expression()


class RawAttribute(renpy.object.Object):
    __version__ = 1

    def after_upgrade(self, version: int):
        if version < 1:
            self.expr_properties = self.properties  # type: ignore
            self.final_properties = {}

    def __init__(self, name):
        self.name = name
        self.image: Imageable = None
        self.final_properties = {}
        self.expr_properties = {}

    def execute(self, group_name=None, **group_properties):
        if "when" in self.final_properties:
            if "when" in group_properties:
                self.final_properties["when"] = WhenAnd(self.final_properties["when"], group_properties.pop("when"))

        group_args = {k: group_properties.pop(k) for k in ATL_PROPERTIES.intersection(group_properties)}

        properties = (
            group_properties  # the remaining ones, overridden by the following
            | self.final_properties
            | {k: eval(v) for k, v in self.expr_properties.items()}
        )

        return [Attribute(group_name, self.name, resolve_image(self.image), group_args=group_args, **properties)]


def parse_attribute(l):
    name = l.require(l.image_name_component)

    ra = RawAttribute(name)

    got_block = False

    def line(lex):
        nonlocal got_block

        while True:
            pp = parse_property(lex, ra.final_properties, ra.expr_properties, ATTRIBUTE_PROPERTIES)
            if pp:
                if pp == 2:
                    got_block = True
                    return
                continue

            if lex.match("null"):
                displayable = "Null()"
            else:
                displayable = parse_displayable(lex)

            if displayable is not None:
                if ra.image is not None:
                    lex.error(
                        f"An attribute can only have zero or one displayable, two found : {displayable} and {ra.image}."
                    )

                ra.image = displayable

                if isinstance(displayable, RawBlock):
                    got_block = True
                    return
                continue

            break

    line(l)

    if got_block:
        return ra
    elif not l.match(":"):
        l.expect_eol()
        l.expect_noblock("attribute")
        return ra

    l.expect_block("attribute")
    l.expect_eol()

    ll = l.subblock_lexer()

    while ll.advance():
        if ll.keyword("pass"):
            ll.expect_eol()
            ll.expect_noblock("pass")
            continue

        line(ll)
        if got_block:
            got_block = False
        else:
            ll.expect_eol()
            ll.expect_noblock("attribute")

    if (ra.image is not None) and ("variant" in ra.final_properties):
        l.error(f"Attribute {ra.name!r} cannot have a variant if it is provided a displayable.")

    return ra


class RawAttributeGroup(renpy.object.Object):
    __version__ = 1

    def after_upgrade(self, version: int):
        if version < 1:
            self.expr_properties = self.properties  # type: ignore
            self.final_properties = {}
            self.group_name = self.group  # type: ignore
            self.li_name = self.image_name  # type: ignore

    def __init__(self, li_name, group_name: str | None):
        self.li_name = li_name
        self.group_name = group_name
        self.children = []
        self.final_properties = {}
        self.expr_properties = {}

    def execute(self):
        properties = self.final_properties | {k: eval(v) for k, v in self.expr_properties.items()}

        auto = properties.pop("auto", False)
        variant = properties.get("variant", None)
        multiple = properties.pop("multiple", False)

        rv = []

        if multiple:
            group_name_for_attributes = None
        else:
            group_name_for_attributes = self.group_name

        for ra in self.children:
            rv.extend(ra.execute(group_name=group_name_for_attributes, **properties))

        if auto:
            seen = set(a.raw_attribute for a in rv)

            pattern = format_function(
                what="auto group attribute",
                name=self.li_name.replace(" ", "_"),
                group=self.group_name or None,
                variant=variant or None,
                attribute="",
                image=None,
                image_format=None,
            )

            for i in renpy.list_images():
                if i.startswith(pattern):
                    attr, *rest = i.removeprefix(pattern).split()
                    if (not rest) and (attr not in seen):
                        rv.append(Attribute(group_name_for_attributes, attr, renpy.displayable(i), **properties))

        return rv


def parse_group(l, li_name):
    if l.keyword("multiple"):
        # a multiple group can be anonymous,
        # though for compatibility, not all multiple groups are anonymous
        group_name = None
    else:
        group_name = l.require(l.image_name_component)

    rv = RawAttributeGroup(li_name, group_name)

    got_block = False

    while True:
        pp = parse_property(l, rv.final_properties, rv.expr_properties, GROUP_INLINE_PROPERTIES)
        if pp == 1:
            continue
        elif pp == 2:
            got_block = True
        break

    if not got_block:
        if l.match(":"):
            l.expect_eol()
            l.expect_block("group")

            ll = l.subblock_lexer()

            while ll.advance():
                got_block = False

                if ll.keyword("pass"):
                    ll.expect_eol()
                    ll.expect_noblock("pass")
                    continue

                if ll.keyword("attribute"):
                    raw_attribute = parse_attribute(ll)
                    rv.children.append(raw_attribute)
                    continue

                while True:
                    pp = parse_property(ll, rv.final_properties, rv.expr_properties, GROUP_BLOCK_PROPERTIES)
                    if pp == 1:
                        continue
                    elif pp == 2:
                        got_block = True
                    break

                if got_block:
                    got_block = False
                else:
                    ll.expect_eol()
                    ll.expect_noblock("group property")

        else:
            l.expect_eol()
            l.expect_noblock("group")

    # after the parsing, to avoid duplicate property errors
    if group_name is None:
        rv.final_properties["multiple"] = True

    if "variant" in rv.final_properties:
        for an in rv.children:
            if "variant" in an.final_properties:
                l.error(
                    f"Attribute {an.name!r} has a variant, it cannot be inside group {group_name!r} which also has a variant."
                )
    elif (group_name is None) and ("auto" in rv.final_properties):
        # tolerated for named multiple groups, for compatibility
        l.error(f"Group {group_name!r} cannot be multiple and auto at the same time.")

    return rv


class RawCondition(renpy.object.Object):
    __version__ = 1

    def after_upgrade(self, version: int):
        if version < 1:
            self.expr_properties = self.properties  # type: ignore
            self.final_properties = {}

    def __init__(self, condition):
        self.condition = condition
        self.image: Imageable = None
        self.final_properties = {}
        self.expr_properties = {}

    def execute(self):
        properties = self.final_properties | {k: eval(v) for k, v in self.expr_properties.items()}
        return [Condition(self.condition, resolve_image(self.image), **properties)]


def parse_condition(l, need_expr):
    l.skip_whitespace()

    if need_expr:
        # condition = l.require(l.comma_expression)
        condition = l.delimited_python(":")
    else:
        condition = None

    l.require(":")
    l.expect_block("if/elif/else")
    l.expect_eol()

    ll = l.subblock_lexer()

    rv = RawCondition(condition)

    while ll.advance():
        # not necessary : the if/elif/else blocks require a displayable,
        # so they can't be empty in the first place anyway
        # if ll.keyword("pass"):
        #     ll.expect_eol()
        #     ll.expect_noblock("pass")
        #     continue

        got_block = False

        while True:
            pp = parse_property(ll, rv.final_properties, rv.expr_properties, CONDITION_PROPERTIES)
            if pp:
                if pp == 2:
                    got_block = True
                    break
                continue

            displayable = parse_displayable(ll)
            if displayable is not None:
                if rv.image is not None:
                    ll.error(
                        f"An if, elif or else statement can only have one displayable, two found : {displayable} and {rv.image}."
                    )

                rv.image = displayable

                if isinstance(displayable, RawBlock):
                    got_block = True
                    break
                continue

            break

        if not got_block:
            ll.expect_noblock("if/elif/else properties")
            ll.expect_eol()

    if rv.image is None:
        l.error("An if, elif or else statement must have a displayable.")

    return rv


class RawConditionGroup(object):
    def __init__(self, conditions: list | tuple = ()):
        self.conditions = conditions

    def execute(self):
        l = []
        for i in self.conditions:
            l.extend(i.execute())

        return [ConditionGroup(l)]


def parse_conditions(l):
    conditions = []

    conditions.append(parse_condition(l, True))
    l.advance()

    while l.keyword("elif"):
        conditions.append(parse_condition(l, True))
        l.advance()

    if l.keyword("else"):
        conditions.append(parse_condition(l, False))
    else:
        l.unadvance()

    return RawConditionGroup(conditions)


class RawAlways(renpy.object.Object):
    __version__ = 1

    def after_upgrade(self, version: int):
        if version < 1:
            self.expr_properties = self.properties  # type: ignore
            self.final_properties = {}

    def __init__(self):
        self.image: Imageable = None
        self.final_properties = {}
        self.expr_properties = {}

    def execute(self):
        image = resolve_image(self.image)
        properties = self.final_properties | {k: eval(v) for k, v in self.expr_properties.items()}
        return [Always(image, **properties)]


def parse_always(l):
    a = RawAlways()

    got_block = False

    # parent.children.append(a)

    def line(lex):
        nonlocal got_block

        while True:
            pp = parse_property(lex, a.final_properties, a.expr_properties, ALWAYS_PROPERTIES)
            if pp:
                if pp == 2:
                    got_block = True
                    return
                continue

            displayable = parse_displayable(lex)

            if displayable is not None:
                if a.image is not None:
                    l.error(
                        f"The always statement can only have one displayable, two found : {displayable} and {a.image}."
                    )

                a.image = displayable

                if isinstance(displayable, RawBlock):
                    got_block = True
                    return
                continue

            break

    line(l)

    if got_block:
        return a
    if not l.match(":"):
        l.expect_eol()
        l.expect_noblock("always")
        return a

    l.expect_block("always")
    l.expect_eol()

    ll = l.subblock_lexer()

    while ll.advance():
        # since an always can have an inline child, it can have an empty block
        if ll.keyword("pass"):
            ll.expect_eol()
            ll.expect_noblock("pass")
            continue

        line(ll)
        if got_block:
            got_block = False
        else:
            ll.expect_eol()
            ll.expect_noblock("always")

    if a.image is None:
        l.error("The always statement must have a displayable.")

    return a


class RawLayeredImage(renpy.object.Object):
    __version__ = 1

    def after_upgrade(self, version: int):
        if version < 1:
            self.expr_properties = self.properties  # type: ignore
            self.final_properties = {}

    def __init__(self, name):
        self.name = name
        self.children: list[RawAlways | RawAttribute | RawAttributeGroup | RawConditionGroup] = []
        self.final_properties = {}
        self.expr_properties = {}

    def execute(self):
        properties = self.final_properties | {k: eval(v) for k, v in self.expr_properties.items()}

        l = []
        for i in self.children:
            l.extend(i.execute())

        renpy.image(
            self.name,
            LayeredImage(l, name=self.name.replace(" ", "_"), **properties),
        )


def execute_layeredimage(rai):
    rai.execute()


def parse_layeredimage(l):
    name = [l.require(l.image_name_component)]

    part = l.image_name_component()
    while part is not None:
        name.append(part)
        part = l.image_name_component()

    name = " ".join(name)

    l.require(":")
    l.expect_block("layeredimage")

    ll = l.subblock_lexer()
    ll.advance()

    rv = RawLayeredImage(name)

    while not ll.eob:
        if ll.keyword("attribute"):
            rv.children.append(parse_attribute(ll))

        elif ll.keyword("group"):
            rv.children.append(parse_group(ll, name))

        elif ll.keyword("if"):
            rv.children.append(parse_conditions(ll))

        elif ll.keyword("always"):
            rv.children.append(parse_always(ll))

        elif ll.keyword("pass"):
            ll.expect_eol()
            ll.expect_noblock("pass")

        else:
            pp = 1
            while pp == 1:
                pp = parse_property(ll, rv.final_properties, rv.expr_properties, BASE_PROPERTIES)

            if not pp:
                ll.expect_noblock("layeredimage property")
                ll.expect_eol()

        ll.advance()

    return rv


def lint_layeredimage(rli: RawLayeredImage) -> None:
    for c in rli.children:
        if isinstance(c, RawAttributeGroup):
            # named auto multiple groups have weird behavior
            if c.group_name and {"auto", "multiple"}.issubset(c.final_properties):
                renpy.error(
                    f"In Layeredimage {rli.name!r}, group {c.group_name!r} should not be named, auto and multiple at the same time."
                )

    if False:
        # Things that are obsolete but work, so are not reported:
        # - if_all, if_any and if_not, in any layer
        # - prefix and variant being in expr_properties (reporting this could really bloat the report)
        # - all named multiple groups
        # - non-auto multiple groups with a variant and a single attribute inside (use variant at the attribute level)
        for c in rli.children:
            if getattr(c, "if_any", None):
                renpy.error('if_any is obsolete, use "when" instead.')
            elif getattr(c, "if_all", None):
                renpy.error('if_all is obsolete, use "when" instead.')
            elif getattr(c, "if_not", None):
                renpy.error('if_not is obsolete, use "when" instead.')

            if {"prefix", "variant"}.intersection(getattr(c, "expr_properties", ())):
                renpy.error("prefix and variant should be passed unquoted.")

            if isinstance(c, RawAttributeGroup):
                named = c.group_name is not None
                multiple = (not named) or c.final_properties.get("multiple", False)
                if named and multiple:
                    renpy.error("Multiple groups should not have a name.")

                if (
                    multiple
                    and (not c.final_properties.get("auto", False))
                    and (("variant" in c.final_properties) or ("variant" in c.expr_properties))
                    and (len(c.children) == 1)
                ):
                    renpy.error("Use variant at the attribute level, rather than creating a multiple group.")


renpy.register_statement(
    "layeredimage",
    parse=parse_layeredimage,
    execute=execute_layeredimage,
    lint=lint_layeredimage,
    init=True,
    block=True,
)


class LayeredImageProxy(object):
    """
    :doc: li_proxy
    :name: LayeredImageProxy

    This is an image-like object that proxies attributes passed to it to
    another layered image.

    `name`
        A string giving the name of the layeredimage to proxy to.

    `transform`
        If given, a transform or list of transforms that are applied to the
        image after it has been proxied.
    """

    def __init__(self, name, transform=None):
        self.name = name

        if "[" not in self.name:
            if renpy.get_registered_image(name) is None:
                raise Exception("{!r} is not a registered image name.".format(self.name))

        if transform is None:
            self.transform = []

        else:
            self.transform = renpy.easy.to_list(transform)

    @property
    def image(self):
        name = self.name

        if "[" in name:
            name = renpy.substitute(name, translate=False)

        image = renpy.get_registered_image(name)

        if image is None:
            raise Exception("{!r} is not a registered image name, in LayeredImageProxy.".format(name))

        return image

    def _duplicate(self, args):
        rv = self.image._duplicate(args)

        for i in self.transform:
            rv = i(rv)

        return rv

    def filter_attributes(self, attributes):
        if attributes is None:
            return None

        name = self.name

        if "[" in name:
            name = renpy.substitute(name, translate=False)

        name = name.split()

        return tuple(i for i in attributes if i not in name[1:])

    def _choose_attributes(self, tag, attributes, optional):
        return self.filter_attributes(self.image._choose_attributes(tag, attributes, optional))

    def _list_attributes(self, tag, attributes):
        return self.filter_attributes(self.image._list_attributes(tag, attributes))


renpy.store.Attribute = Attribute
renpy.store.LayeredImage = LayeredImage
renpy.store.LayeredImageProxy = LayeredImageProxy
renpy.store.Condition = Condition
renpy.store.ConditionGroup = ConditionGroup
