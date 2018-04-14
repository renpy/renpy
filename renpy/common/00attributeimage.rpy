init offset = -100

python early in _attribute:

    from store import Transform, ConditionSwitch, Fixed, Null
    from collections import OrderedDict

    ATL_PROPERTIES =[ i for i in renpy.atl.PROPERTIES ]

    def format_function(what, name, group, attribute, image, image_format, **kwargs):
        """
        This is called to format the information about an attribute
        or condtion into a displayable. This can be replaced by a
        creator, but the new function should ignore unknown kwargs.

        `what`
            A string giving a description of the thing being formatted,
            which is used to create better error messages.

        `name`
            The name of the attribute image.

        `group`
            The group of an attribute, None if not supplied or if it's
            part of a condition.

        `attribute`
            The attribute itself.

        `image`
            Either a displayable or string.

        `image_format`
            The image_format argument of the attribute image.

        If `image `is None, then `name`, `group` (if not None), and
        `attribute` are combined to create `imasge`. If `images` is
        a string, and `image_format` is not None, `image` is formatted
        into the string to get the final displayable.

        So if `name` is "eileen", `group` is "expression", and
        `attribute` is "happy", `image` would be set to
        "eileen expression happy". If `image_format` is "images/{image}.png",
        the final image Ren'Py finds is "images/eileen expression happy.png".
        But note that it would have found the same image without the format
        argument.
        """

        if image is None:

            if name is None:
                raise Exception("Can't find an image name to format {}.".format(what))

            if attribute is None:
                raise Exception("Can't find an attribute name to format {}.".format(what))

            parts = [ name ]

            if group is not None:
                parts.append(group)

            parts.append(attribute)

            image = " ".join(parts)

        if isinstance(image, basestring) and (image_format is not None):
            image = image_format.format(name=name, image=image)

        return image


    class Attribute(object):
        """
        This is used to represent a layer of an AttributeImage that is
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

        `at`
            A transform or list of transforms that are applied to the
            image.

        Other keyword arguments are interpreted as transform properties. If
        any are present, a transform is created that wraps the image. (For
        example, pos=(100, 200) can be used to offset the image by 100 pixels
        horizontally and 200 vertically.)

        If the `image` parameter is omitted or None, and the AttributeImage
        has been given the `image_format` parameter, the image_format is used
        to generate an image filename.
        """

        def __init__(self, group, attribute, image=None, default=False, at=[ ], **kwargs):

            self.raw_group = group
            self.group = group or attribute
            self.attribute = attribute
            self.image = image
            self.default = default

            if not isinstance(at, list):
                at = list(at)

            self.at = at

            self.transform_args = kwargs

        def apply_format(self, ai):

            self.image = ai.format(
                "Attribute ({!r}, {!r})".format(self.raw_group, self.attribute),
                group=self.raw_group,
                attribute=self.attribute,
                image=self.image,
                )

            self.image = renpy.displayable(self.image)

            for i in self.at:
                self.image = i(self.image)

            if self.transform_args:

                self.image = Transform(self.image, **self.transform_args)

        def get_displayable(self, attributes):

            if self.attribute in attributes:
                return self.image

            return None


    class RawAttribute(object):

        def __init__(self, name):
            self.name = name
            self.image = None
            self.properties = OrderedDict()

        def execute(self, group=None, properties=None):

            if properties is not None:
                properties = dict(properties)
            else:
                properties = dict()

            properties.update({ k : eval(v) for k, v in self.properties.items() })
            return [ Attribute(group, self.name, eval(self.image), **properties) ]


    class RawAttributeGroup(object):

        def __init__(self, group):

            self.group = group
            self.properties = OrderedDict()
            self.children = [ ]

        def execute(self):

            properties = { k : eval(v) for k, v in self.properties.items() }

            rv = [ ]

            for i in self.children:
                rv.extend(i.execute(group=self.group, properties=properties))

            return rv


    class Condition(object):
        """
        This is used to represent a layer of an AttributeImage that
        is controlled by a condition. When the condition is true,
        the layer is displayed. Otherwise, nothing is displayed.

        `condition`
            This should be a string giving a Python condition that determines
            if the layer is displayed.

        `image`
            The displayable that is shown when the condition is True.

        `at`
            A transform or list of transforms that are applied to the
            image.

        Other keyword arguments are interpreted as transform properties. If
        any are present, a transform is created that wraps the image. (For
        example, pos=(100, 200) can be used to offset the image by 100 pixels
        horizontally and 200 vertically.)
        """

        at = [ ]

        def __init__(self, condition, image, at=[ ], **kwargs):
            self.condition = condition
            self.image = image

            if not isinstance(at, list):
                at = list(at)

            self.at = at

            self.transform_args = kwargs

        def apply_format(self, ai):

            self.image = ai.format(
                "Condition ({})".format(self.condition),
                group=None,
                attribute=None,
                image=self.image,
                )

            self.image = renpy.displayable(self.image)

            if self.transform_args:
                self.image = Transform(self.image, **self.transform_args)

            for i in self.at:
                self.image = i(self.image)

        def get_displayable(self, attributes):
            return ConditionSwitch(
                self.condition, self.image,
                None, Null(),
            )


    class RawCondition(object):

        def __init__(self, condition):
            self.condition = condition
            self.image = None
            self.properties = OrderedDict()

        def execute(self):
            properties = { k : eval(v) for k, v in self.properties.items() }
            return [ Condition(self.condition, eval(self.image), **properties) ]


    class ConditionGroup(object):
        """
        Combines a list of conditions into a single ConditionSwitch.
        """

        def __init__(self, conditions):
            self.conditions = conditions

        def apply_format(self, ai):
            for i in self.conditions:
                i.apply_format(ai)

        def get_displayable(self, attributes):
            args = [ ]

            for i in self.conditions:
                args.append(i.condition)
                args.append(i.image)

            args.append(None)
            args.append(Null())

            return ConditionSwitch(*args)

    class RawConditionGroup(object):

        def __init__(self):
            self.conditions = [ ]

        def execute(self):

            l = [ ]
            for i in self.conditions:
                l.extend(i.execute())

            return [ ConditionGroup(l) ]


    class AttributeImage(object):
        """
        This is an image-like object that, when shown with the proper set of
        attributes, shows a displayable created by compositing together the
        displayables associated with those attribute.

        `attributes`
            This must be a list of Attribute objects. Each Attribute object
            reflects a displayable that may or may not be displayed as part
            of the image. The items in this list are in back-to-front order,
            with the first item further from the viewer and the last
            closest.

        `at`
            A transform or list of transforms that are applied to the displayable
            after it is parameterized.

        `name`
            The name of the attribute image. This is used as part of the names
            of image components.

        `image_format`
            When a given image is a string, and this is supplied, the image and
            the name are interpolated into `image_format` to make an image. For example,
            "sprites/{name}/{image}.png" will look for the image in a subdirectory
            of sprites.

        `format_function`
            A function that is used instead of `_attribute.format_function` to format
            the image information into a displayable.

        Additional keyword arguments are passed to a Fixed that is created to hold
        the layer. Unless explicitly overridden, xfit and yfit are set to true on
        the Fixed, which means it will shrink to the smallest size that fits all
        of the layer images it is showing.

        An AttributeImage is not a displayable, and can't be used in all the
        places a displayable can be used. This is because it requires an image
        name (generally including image attributes) to be provided. As such,
        it should either be displayed through a scene or show statement, or by
        an image name string used as a displayable.
        """

        def __init__(self, attributes, at=[], name=None, image_format=None, format_function=None, **kwargs):

            self.name = name
            self.image_format = image_format
            self.format_function = format_function

            self.attributes = [ ]
            self.layers = [ ]

            import collections
            self.attribute_to_groups = collections.defaultdict(set)
            self.group_to_attributes = collections.defaultdict(set)

            for i in attributes:
                self.add(i)

            if not isinstance(at, list):
                at = [ at ]

            self.at = at

            kwargs.setdefault("xfit", True)
            kwargs.setdefault("yfit", True)

            self.fixed_args = kwargs

        def format(self, what, attribute, group, image):

            ff = format_function

            if self.format_function is not None:
                ff = self.format_function

            return ff(
                what=what,
                name=self.name,
                attribute=attribute,
                group=group,
                image=image,
                image_format=self.image_format)

        def add(self, a):
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

            rv = set()

            for i in attributes:
                for g in self.attribute_to_groups[i]:
                    for j in self.group_to_attributes[g]:
                        if j != i:
                            rv.add(j)
            return rv

        def _duplicate(self, args):

            name = " ".join(args.name + tuple(args.args))

            attributes = set(args.args)
            banned = self.get_banned(attributes)

            for a in self.attributes:
                if a.default and (a.attribute not in banned):
                    attributes.add(a.attribute)

            rv = Fixed(**self.fixed_args)

            for i in self.layers:
                d = i.get_displayable(attributes)

                if d is not None:

                    if d._duplicatable:
                        d = d._duplicate(args)

                    rv.add(d)

            for i in self.at:
                rv = i(rv)

            return rv

        def _list_attributes(self, attributes):
            banned = self.get_banned(attributes)

            rv = [ ]
            seen = set()

            for a in self.attributes:
                if a.attribute in banned:
                    continue

                if a.attribute in seen:
                    continue

                seen.add(a.attribute)
                rv.add(a.attribute)

            return rv

        def _choose_attributes(self, tag, attributes, optional):

            attributes = set(attributes)
            banned = self.get_banned(attributes)

            both = attributes & banned

            if both:
                raise Exception("The attributes for {} conflict: {}".format(tag, " ".join(both)))


            if optional is not None:
                attributes |= (set(optional) - banned)

            rv = [ ]

            for a in self.attributes:
                if a.attribute in attributes:
                    rv.append(a.attribute)
                    attributes.remove(a.attribute)

            return tuple(rv)

    class RawAttributeImage(object):

        def __init__(self, name):
            self.name = name
            self.children = [ ]
            self.properties = OrderedDict()

        def execute(self):
            properties = { k : eval(v) for k, v in self.properties.items() }


            l = [ ]
            for i in self.children:
                l.extend(i.execute())

            renpy.image(
                self.name,
                AttributeImage(l, name=self.name, **properties),
            )

    def execute_attributeimage(rai):
        rai.execute()


    def parse_property(l, o, names):
        """
        Parses a property, returns True if one is found.
        """

        regex = "|".join(names)
        name = l.match(regex)

        if name is None:
            return False

        if name in o.properties:
            ll.error("Duplicate property " + name)

        expr = l.require(l.simple_expression)
        o.properties[name] = expr

        return True


    def parse_attribute(l, parent):

        name = l.require(l.image_name_component)

        a = RawAttribute(name)
        parent.children.append(a)

        def line(l):

            while True:

                if parse_property(l, a, [ "default", "at" ] + ATL_PROPERTIES):
                    continue

                image = l.simple_expression()
                if image is not None:

                    if a.image is not None:
                        l.error('An attribute can only have zero or one displayables, two found.')

                    a.image = image
                    continue

                break


        line(l)

        if not l.match(':'):
            l.expect_eol()
            l.expect_noblock('attribute')
            return


        l.expect_block('attribute')
        l.expect_eol()

        ll = l.subblock_lexer()

        while ll.advance():
            line(ll)
            ll.expect_eol()
            ll.expect_noblock('attribute')

        return


    def parse_group(l, parent):

        group = l.require(l.image_name_component)

        rv = RawAttributeGroup(group)
        parent.children.append(rv)

        l.require(':')
        l.expect_block("group")
        l.expect_eol()

        ll = l.subblock_lexer()

        while ll.advance():
            if ll.match("attribute"):
                parse_attribute(ll, rv)
                continue

            while parse_property(ll, rv, [ "at" ] + ATL_PROPERTIES):
                pass

            ll.expect_eol()
            ll.expect_noblock('group property')


    def parse_condition(l, need_expr):

        l.skip_whitespace()

        if need_expr:
            condition = l.delimited_python(':')
        else:
            condition = None

        l.require(':')

        l.expect_block('condition')
        l.expect_eol()

        ll = l.subblock_lexer()

        rv = RawCondition(condition)

        while ll.advance():


            while True:

                if parse_property(ll, rv, [ "at" ] + ATL_PROPERTIES):
                    continue

                image = ll.simple_expression()

                if image is not None:

                    if rv.image is not None:
                        ll.error('A condition can only have one displayable, two found.')

                    rv.image = image
                    continue

                break

            ll.expect_noblock("condition properties")
            ll.expect_eol()


        if rv.image is None:
            l.error("A condition must have a displayable.")

        return rv


    def parse_conditions(l, parent):

        cg = RawConditionGroup()

        cg.conditions.append(parse_condition(l, True))
        l.advance()

        while l.match('elif'):

            cg.conditions.append(parse_condition(l, True))
            l.advance()

        if l.match('else'):

            cg.conditions.append(parse_condition(l, False))
            l.advance()

        parent.children.append(cg)


    def parse_attributeimage(l):

        name = [ l.require(l.image_name_component) ]

        while True:
            part = l.image_name_component()

            if part is None:
                break

            name.append(part)

        l.require(':')
        l.expect_block("attributeimage")

        ll = l.subblock_lexer()
        ll.advance()

        name = " ".join(name)
        rv = RawAttributeImage(name)

        while not ll.eob:

            if ll.match('attribute'):

                parse_attribute(ll, rv)
                ll.advance()

            elif ll.match('group'):

                parse_group(ll, rv)
                ll.advance()

            elif ll.match('if'):

                parse_conditions(ll, rv)
                # Advances for us.

            else:

                while parse_property(ll, rv, [ "image_format", "format_function", "at" ] + ATL_PROPERTIES):
                    pass

                ll.expect_noblock('statement')
                ll.expect_eol()
                ll.advance()

        return rv


    renpy.register_statement("attributeimage", parse=parse_attributeimage, execute=execute_attributeimage, init=True, block=True)

    renpy.store.Attribute = Attribute
    renpy.store.AttributeImage = AttributeImage
    renpy.store.Condition = Condition
    renpy.store.ConditionGroup = ConditionGroup
