# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy

# Layer management.
layers = frozenset(renpy.config.layers)
sticky_layers = frozenset()


def init_layers():
    global layers, sticky_layers

    layers = frozenset(
        renpy.config.layers + renpy.config.detached_layers +
        renpy.config.top_layers + renpy.config.bottom_layers)
    sticky_layers = frozenset(
        renpy.config.sticky_layers + renpy.config.detached_layers)


class SceneListEntry(renpy.object.Object):
    """
    Represents a scene list entry. Since this was replacing a tuple,
    it should be treated as immutable after its initial creation.
    """

    def __init__(self, tag, zorder, show_time, animation_time, displayable, name):
        self.tag = tag
        self.zorder = zorder
        self.show_time = show_time
        self.animation_time = animation_time
        self.displayable = displayable
        self.name = name

    def __iter__(self):
        return iter((self.tag, self.zorder, self.show_time, self.animation_time, self.displayable))

    def __getitem__(self, index):
        return (self.tag, self.zorder, self.show_time, self.animation_time, self.displayable)[index]

    def __repr__(self):
        return "<SLE: %r %r %r>" % (self.tag, self.name, self.displayable)

    def copy(self):
        return SceneListEntry(
            self.tag,
            self.zorder,
            self.show_time,
            self.animation_time,
            self.displayable,
            self.name)

    def update_time(self, time):

        rv = self

        if self.show_time is None or self.animation_time is None:
            rv = self.copy()
            rv.show_time = rv.show_time or time
            rv.animation_time = rv.animation_time or time

        return rv


class SceneLists(renpy.object.Object):
    """
    This stores the current scene lists that are being used to display
    things to the user.
    """

    __version__ = 9

    def after_setstate(self):
        self.camera_list = getattr(self, "camera_list", { })
        self.camera_transform = getattr(self, "camera_transform", { })
        self.config_layer_transform = getattr(self, "config_layer_transform", { })

        for i in layers:
            if i not in self.layers:
                self.layers[i] = [ ]
                self.at_list[i] = { }
                self.layer_at_list[i] = (None, [ ])

            if i not in self.camera_list:
                self.camera_list[i] = (None, [ ])

            if i not in self.config_layer_transform:
                self.config_layer_transform[i] = [ ]

    def after_upgrade(self, version):

        if version < 1:

            self.at_list = { }
            self.layer_at_list = { }

            for i in layers:
                self.at_list[i] = { }
                self.layer_at_list[i] = (None, [ ])

        if version < 3:
            self.shown_window = False

        if version < 4:
            for k in self.layers:
                self.layers[k] = [ SceneListEntry(*(i + (None,))) for i in self.layers[k] ]

            self.additional_transient = [ ]

        if version < 5:
            self.drag_group = None

        if version < 6:
            self.shown = self.image_predict_info # type: ignore

        if version < 7:
            self.layer_transform = { }

        if version < 8:
            self.sticky_tags = { }

        if version < 9:
            self.additional_transient = [ (layer, tag, None) for layer, tag in self.additional_transient ] # type: ignore


    def __init__(self, oldsl, shown):

        super(SceneLists, self).__init__()

        # Has a window been shown as part of these scene lists?
        self.shown_window = False

        # A map from layer name -> list(SceneListEntry)
        self.layers = { }

        # A map from layer name -> tag -> at_list associated with that tag.
        self.at_list = { }

        # A map from layer to (start time, at_list), where the at list has
        # been applied to the layer as a whole.
        self.layer_at_list = { }

        # The camera list, which is similar to the layer at list but is not
        # cleared during the scene statement.
        self.camera_list = { }

        # The current shown images,
        self.shown = shown

        # A list of (layer, tag) pairs that are considered to be
        # transient.
        self.additional_transient = [ ]

        # Either None, or a DragGroup that's used as the default for
        # drags with names.
        self.drag_group = None

        # A map from a layer to the transform that applies to that
        # layer.
        self.layer_transform = { }

        # Same thing, but for the camera transform.
        self.camera_transform = { }

        # Same thing, but for config.layer_transforms.
        self.config_layer_transform = { }

        # A map from tag -> layer name, only for layers in config.sticky_layers.
        self.sticky_tags = { }

        if oldsl:

            for i in layers:

                try:
                    self.layers[i] = oldsl.layers[i][:]
                except KeyError:
                    self.layers[i] = [ ]

                if i in oldsl.at_list:
                    self.at_list[i] = oldsl.at_list[i].copy()
                    self.layer_at_list[i] = oldsl.layer_at_list[i]
                    self.camera_list[i] = oldsl.camera_list[i]
                else:
                    self.at_list[i] = { }
                    self.layer_at_list[i] = (None, [ ])
                    self.camera_list[i] = (None, [ ])

            for i in renpy.config.overlay_layers:
                self.clear(i)

            self.replace_transient(prefix=None)

            self.focused = None

            self.drag_group = oldsl.drag_group

            self.layer_transform.update(oldsl.layer_transform)
            self.camera_transform.update(oldsl.camera_transform)
            self.sticky_tags.update(oldsl.sticky_tags)

        else:
            for i in layers:
                self.layers[i] = [ ]
                self.at_list[i] = { }
                self.layer_at_list[i] = (None, [ ])
                self.camera_list[i] = (None, [ ])

            self.music = None
            self.focused = None

    def set_transient_prefix(self, layer, tag, prefix):
        """
        Sets the transient prefix for the given tag on the given layer. This
        can be used to have the "replaced" event delivered when the displayable
        is hidden, and not the "hide" event.
        """

        l = [ ]

        for ltp in self.additional_transient:
            if ltp[0] == layer and ltp[1] == tag:
                ltp = (ltp[0], ltp[1], prefix)

            l.append(ltp)

        self.additional_transient = l

    def replace_transient(self, prefix="hide"): # type: (str|None) -> None
        """
        Replaces the contents of the transient display list with
        a copy of the master display list. This is used after a
        scene is displayed to get rid of transitions and interface
        elements.

        `prefix`
            The prefix/event to use. Set this to None to prevent the hide
            from happening.
        """

        for i in renpy.config.transient_layers:
            self.clear(i, True)

        for layer, tag, p in self.additional_transient:
            self.remove(layer, tag, prefix=p if p is not None else prefix)

        self.additional_transient = [ ]

    def transient_is_empty(self):
        """
        This returns True if all transient layers are empty. This is
        used by the rollback code, as we can't start a new rollback
        if there is something in a transient layer (as things in the
        transient layer may contain objects that cannot be pickled,
        like lambdas.)
        """

        for i in renpy.config.transient_layers:
            if self.layers[i]:
                return False

        return True

    def transform_state(self, old_thing, new_thing, execution=False):
        """
        If the old thing is a transform, then move the state of that transform
        to the new thing.
        """

        if old_thing is None:
            return new_thing

        # Don't bother wrapping screens, as they can't be transformed.
        if isinstance(new_thing, renpy.display.screen.ScreenDisplayable):
            return new_thing

        if renpy.config.take_state_from_target:
            old_transform = old_thing._target()
        else:
            old_transform = old_thing

        if not isinstance(old_transform, renpy.display.motion.Transform):
            return new_thing

        if renpy.config.take_state_from_target:
            new_transform = new_thing._target()
        else:
            new_transform = new_thing

        if not isinstance(new_transform, renpy.display.motion.Transform):
            new_thing = new_transform = renpy.display.motion.Transform(child=new_thing)

        new_transform.take_state(old_transform)

        if execution:
            new_transform.take_execution_state(old_transform)

        return new_thing

    def find_index(self, layer, tag, zorder, behind):
        """
        This finds the spot in the named layer where we should insert the
        displayable. It returns two things: an index at which the new thing
        should be added, and an index at which the old thing should be hidden.
        (Note that the indexes are relative to the current state of the list,
        which may change on an add or remove.)
        """

        add_index = None
        remove_index = None

        for i, sle in enumerate(self.layers[layer]):

            if remove_index is None:
                if (sle.tag and sle.tag == tag) or sle.displayable == tag:
                    remove_index = i

                    if zorder is None:
                        zorder = sle.zorder

        if zorder is None:
            zorder = renpy.config.tag_zorder.get(tag, 0)

        for i, sle in enumerate(self.layers[layer]):

            if add_index is None:

                if sle.zorder == zorder:
                    if sle.tag and (sle.tag == tag or sle.tag in behind):
                        add_index = i

                elif sle.zorder > zorder:
                    add_index = i

        if add_index is None:
            add_index = len(self.layers[layer])

        return add_index, remove_index, zorder

    def add(self,
            layer,
            thing,
            key=None,
            zorder=0,
            behind=[ ],
            at_list=[ ],
            name=None,
            atl=None,
            default_transform=None,
            transient=False,
            keep_st=False):
        """
        Adds something to this scene list. Some of these names are quite a bit
        out of date.

        `thing` - The displayable to add.

        `key` - A string giving the tag associated with this thing.

        `zorder` - Where to place this thing in the zorder, an integer
        A greater value means closer to the user.

        `behind` - A list of tags to place the thing behind.

        `at_list` - The at_list associated with this
        displayable. Counterintuitively, this is not actually
        applied, but merely stored for future use.

        `name` - The full name of the image being displayed. This is used for
        image lookup.

        `atl` - If not None, an atl block applied to the thing. (This actually is
        applied here.)

        `default_transform` - The default transform that is used to initialized
        the values in the other transforms.

        `keep_st`
            If true, we preserve the shown time of a replaced displayable.
        """

        if not isinstance(thing, renpy.display.core.Displayable):
            raise Exception("Attempting to show something that isn't a displayable:" + repr(thing))

        if layer not in self.layers:
            raise Exception("Trying to add something to non-existent layer '%s'." % layer)

        if key:
            self.remove_hide_replaced(layer, key)
            self.at_list[layer][key] = at_list

            if layer in sticky_layers:
                self.sticky_tags[key] = layer

        if key and name:
            self.shown.predict_show(layer, (key,) + name[1:])

        if transient:
            self.additional_transient.append((layer, key, None))

        l = self.layers[layer]

        if atl:
            thing = renpy.display.motion.ATLTransform(atl, child=thing)

        add_index, remove_index, zorder = self.find_index(layer, key, zorder, behind)

        at = None
        st = None

        if remove_index is not None:
            sle = l[remove_index]
            old = sle.displayable

            at = sle.animation_time

            if keep_st:
                st = sle.show_time

            if not self.hide_or_replace(layer, remove_index, "replaced"):
                if add_index > remove_index:
                    add_index -= 1

            if (not atl and
                    not at_list and
                    renpy.config.keep_running_transform and
                    isinstance(old, renpy.display.motion.Transform)):

                thing = sle.displayable._change_transform_child(thing)

            else:

                thing = self.transform_state(old, thing)

            thing.set_transform_event("replace")

        else:

            if not isinstance(thing, renpy.display.motion.Transform):
                thing = self.transform_state(default_transform, thing)

            thing.set_transform_event("show")

        if add_index is not None:
            sle = SceneListEntry(key, zorder, st, at, thing, name)
            l.insert(add_index, sle)

        # By walking the tree of displayables we allow the displayables to
        # capture the current state. In older code, we allow this to to fail.
        # Errors might exist in older games, which are ignored when not in
        # developer mode.
        try:
            thing.visit_all(lambda d : None)
        except Exception:
            if renpy.config.developer:
                raise

    def hide_or_replace(self, layer, index, prefix):
        """
        Hides or replaces the scene list entry at the given
        index. `prefix` is a prefix that is used if the entry
        decides it doesn't want to be hidden quite yet.

        Returns True if the displayable is kept, False if it is removed.
        """

        if index is None:
            return False

        l = self.layers[layer]
        oldsle = l[index]

        now = renpy.display.core.get_time()

        st = oldsle.show_time or now
        at = oldsle.animation_time or now

        if renpy.config.fast_unhandled_event:
            if not oldsle.displayable._handles_event(prefix):
                prefix = None

        if (prefix is not None) and oldsle.tag:

            d = oldsle.displayable._in_current_store()._hide(now - st, now - at, prefix)

            # _hide can mutate the layers, so we need to recompute
            # index.
            index = l.index(oldsle)

            if d is not None:

                sle = SceneListEntry(
                    prefix + "$" + oldsle.tag,
                    oldsle.zorder,
                    st,
                    at,
                    d,
                    None)

                l[index] = sle

                return True

        l.pop(index)

        return False

    def get_all_displayables(self, current=False):
        """
        Gets all displayables reachable from this scene list.

        `current`
            If true, only returns displayables that are not in the process
            of being hidden.
        """

        rv = [ ]
        for l in self.layers.values():
            for sle in l:

                if current and sle.tag and ("$" in sle.tag):
                    continue

                rv.append(sle.displayable)

        return rv

    def remove_above(self, layer, thing):
        """
        Removes everything on the layer that is closer to the user
        than thing, which may be either a tag or a displayable. Thing must
        be displayed, or everything will be removed.
        """

        for i in range(len(self.layers[layer]) - 1, -1, -1):

            sle = self.layers[layer][i]

            if thing:
                if sle.tag == thing or sle.displayable == thing:
                    break

            if sle.tag and "$" in sle.tag:
                continue

            self.hide_or_replace(layer, i, "hide")

    def remove(self, layer, thing, prefix="hide"): # type: (str, str|tuple|renpy.display.core.Displayable, str|None) -> None
        """
        Thing is either a key or a displayable. This iterates through the
        named layer, searching for entries matching the thing.
        When they are found, they are removed from the displaylist.

        It's not an error to remove something that isn't in the layer in
        the first place.
        """

        if layer not in self.layers:
            raise Exception("Trying to remove something from non-existent layer '%s'." % layer)

        _add_index, remove_index, _zorder = self.find_index(layer, thing, 0, [ ])

        if remove_index is not None:
            tag = self.layers[layer][remove_index].tag

            if tag:
                self.shown.predict_hide(layer, (tag,))
                self.at_list[layer].pop(tag, None)

                if self.sticky_tags.get(tag, None) == layer:
                    del self.sticky_tags[tag]

            self.hide_or_replace(layer, remove_index, prefix)

    def clear(self, layer, hide=False):
        """
        Clears the named layer, making it empty.

        If hide is True, then objects are hidden. Otherwise, they are
        totally wiped out.
        """

        if layer not in self.layers:
            return

        if not hide:
            self.layers[layer][:] = [ ]

        else:

            # Have to iterate in reverse order, since otherwise
            # the indexes might change.
            for i in range(len(self.layers[layer]) - 1, -1, -1):
                self.hide_or_replace(layer, i, hide)

        self.at_list[layer].clear()
        self.sticky_tags = {k: v for k, v in self.sticky_tags.items() if v != layer}

        self.shown.predict_scene(layer)

        if renpy.config.scene_clears_layer_at_list:
            self.layer_at_list[layer] = (None, [ ])

    def set_layer_at_list(self, layer, at_list, reset=True, camera=False):

        if camera:
            self.camera_list[layer] = (None, list(at_list))
        else:
            self.layer_at_list[layer] = (None, list(at_list))

        if reset:
            self.layer_transform[layer] = None

    def set_times(self, time):
        """
        This finds entries with a time of None, and replaces that
        time with the given time.
        """

        for l, (t, ll) in list(self.camera_list.items()):
            self.camera_list[l] = (t or time, ll)

        for l, (t, ll) in list(self.layer_at_list.items()):
            self.layer_at_list[l] = (t or time, ll)

        for ll in self.layers.values():
            ll[:] = [ i.update_time(time) for i in ll ]

    def showing(self, layer, name):
        """
        Returns true if something with the prefix of the given name
        is found in the scene list.
        """

        return self.shown.showing(layer, name)

    def get_showing_tags(self, layer):
        return self.shown.get_showing_tags(layer)

    def get_sorted_tags(self, layer):
        rv = [ ]

        for sle in self.layers[layer]:
            if not sle.tag:
                continue

            if "$" in sle.tag:
                continue

            rv.append(sle.tag)

        return rv

    def make_layer(self, layer, properties):
        """
        Creates a Fixed with the given layer name and scene_list.
        """

        rv = renpy.display.layout.MultiBox(layout='fixed', focus=layer, **properties)
        rv.append_scene_list(self.layers[layer])
        rv.layer_name = layer
        rv._duplicatable = False
        rv._layer_at_list = self.layer_at_list[layer]
        rv._camera_list = self.camera_list[layer]

        return rv

    def transform_layer(self, layer, d, layer_at_list=None, camera_list=None):
        """
        When `d` is a layer created with make_layer, returns `d` with the
        various at_list transforms applied to it.
        """

        if layer_at_list is None:
            layer_at_list = self.layer_at_list[layer]
        if camera_list is None:
            camera_list = self.camera_list[layer]

        rv = d

        # Layer at list.

        time, at_list = layer_at_list

        old_transform = self.layer_transform.get(layer, None)
        new_transform = None

        if at_list:

            for a in at_list:

                if isinstance(a, renpy.display.motion.Transform):
                    rv = a(child=rv)
                else:
                    rv = a(rv)

                rv._unique()

                if isinstance(rv, renpy.display.motion.Transform):
                    new_transform = rv

            if (new_transform is not None) and (renpy.config.keep_show_layer_state):
                self.transform_state(old_transform, new_transform, execution=True)

            f = renpy.display.layout.MultiBox(layout='fixed')
            f.add(rv, time, time)
            f.layer_name = layer
            f.untransformed_layer = d

            rv = f

        self.layer_transform[layer] = new_transform

        # Camera list.

        time, at_list = camera_list

        old_transform = self.camera_transform.get(layer, None)
        new_transform = None

        if at_list:

            for a in at_list:

                if isinstance(a, renpy.display.motion.Transform):
                    rv = a(child=rv)
                else:
                    rv = a(rv)

                rv._unique()

                if isinstance(rv, renpy.display.motion.Transform):
                    new_transform = rv

            if (new_transform is not None):
                self.transform_state(old_transform, new_transform, execution=True)

            f = renpy.display.layout.MultiBox(layout='fixed')
            f.add(rv, time, time)
            f.layer_name = layer
            f.untransformed_layer = d

            rv = f

        self.camera_transform[layer] = new_transform

        # Handle config.layer_transforms.

        at_list = renpy.config.layer_transforms.get(layer, [ ])

        old_transform = self.config_layer_transform.get(layer, None)
        new_transform = None

        if at_list:

            for a in at_list:

                if isinstance(a, renpy.display.motion.Transform):
                    rv = a(child=rv)
                else:
                    rv = a(rv)

                rv._unique()

                if isinstance(rv, renpy.display.motion.Transform):
                    new_transform = rv

            if (new_transform is not None):
                self.transform_state(old_transform, new_transform, execution=True)

            f = renpy.display.layout.MultiBox(layout='fixed')
            f.add(rv, 0, 0)
            f.layer_name = layer
            f.untransformed_layer = d

            rv = f

        self.config_layer_transform[layer] = new_transform

        return rv

    def remove_hide_replaced(self, layer, tag):
        """
        Removes things that are hiding or replaced, that have the given
        tag.
        """

        hide_tag = "hide$" + tag
        replaced_tag = "replaced$" + tag

        layer_list = self.layers[layer]


        now = renpy.display.core.get_time()

        new_layer_list = [ ]

        for sle in layer_list:
            if (sle.tag == hide_tag) or (sle.tag == replaced_tag):
                d = sle.displayable._hide(now - sle.show_time, now - sle.animation_time, "cancel")

                if d is None:
                    continue

            new_layer_list.append(sle)

        layer_list[:] = new_layer_list

    def remove_hidden(self):
        """
        Goes through all of the layers, and removes things that are
        hidden and are no longer being kept alive by their hide
        methods.
        """

        now = renpy.display.core.get_time()

        for v in self.layers.values():
            newl = [ ]

            for sle in v:

                if sle.tag:

                    if sle.tag.startswith("hide$"):
                        d = sle.displayable._hide(now - sle.show_time, now - sle.animation_time, "hide")
                        if not d:
                            continue

                    elif sle.tag.startswith("replaced$"):
                        d = sle.displayable._hide(now - sle.show_time, now - sle.animation_time, "replaced")
                        if not d:
                            continue

                newl.append(sle)

            v[:] = newl

    def remove_all_hidden(self):
        """
        Removes everything hidden, even if it's not time yet. (Used when making a rollback copy).
        """

        for v in self.layers.values():
            newl = [ ]

            for sle in v:

                if sle.tag:

                    if "$" in sle.tag:
                        continue

                newl.append(sle)

            v[:] = newl

    def get_displayable_by_tag(self, layer, tag):
        """
        Returns the displayable on the layer with the given tag, or None
        if no such displayable exists. Note that this will usually return
        a Transform.
        """

        if layer not in self.layers:
            raise Exception("Unknown layer %r." % layer)

        for sle in self.layers[layer]:
            if sle.tag == tag:
                return sle.displayable

        return None

    def get_displayable_by_name(self, layer, name):
        """
        Returns the displayable on the layer with the given name, or None
        if no such displayable exists. Note that this will usually return
        a Transform.
        """

        if layer not in self.layers:
            raise Exception("Unknown layer %r." % layer)

        for sle in self.layers[layer]:
            if sle.name == name:
                return sle.displayable

        return None

    def get_image_bounds(self, layer, tag, width, height):
        """
        Implements renpy.get_image_bounds().
        """

        if layer not in self.layers:
            raise Exception("Unknown layer %r." % layer)

        for sle in self.layers[layer]:
            if sle.tag == tag:
                break
        else:
            return None

        now = renpy.display.core.get_time()

        if sle.show_time is not None:
            st = now - sle.show_time
        else:
            st = 0

        if sle.animation_time is not None:
            at = now - sle.animation_time
        else:
            at = 0

        surf = renpy.display.render.render_for_size(sle.displayable, width, height, st, at)

        sw = surf.width
        sh = surf.height

        x, y = renpy.display.displayable.place(width, height, sw, sh, sle.displayable.get_placement())

        return (x, y, sw, sh)

    def get_zorder_list(self, layer):
        """
        Returns a list of (tag, zorder) pairs.
        """

        rv = [ ]

        for sle in self.layers.get(layer, [ ]):

            if sle.tag is None:
                continue
            if "$" in sle.tag:
                continue

            rv.append((sle.tag, sle.zorder))

        return rv

    def change_zorder(self, layer, tag, zorder):
        """
        Changes the zorder for tag on layer.
        """

        sl = self.layers.get(layer, [ ])
        for sle in sl:

            if sle.tag == tag:
                sle.zorder = zorder

        sl.sort(key=lambda sle : sle.zorder)


def scene_lists(index=-1):
    """
    Returns either the current scenelists object, or the one for the
    context at the given index.
    """

    return renpy.game.context(index).scene_lists
