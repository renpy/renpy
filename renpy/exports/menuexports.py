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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy
from renpy.exports.commonexports import renpy_pure


def get_menu_args():
    """
    :doc: other

    Returns a tuple giving the arguments (as a tuple) and the keyword arguments
    (as a dict) passed to the current menu statement.
    """

    if renpy.exports.menu_args is None:
        return (), {}

    return renpy.exports.menu_args, renpy.exports.menu_kwargs


def menu(items, set_expr, args=None, kwargs=None, item_arguments=None):
    """
    :undocumented:

    Displays a menu, and returns to the user the value of the selected
    choice. Also handles conditions and the menuset.
    """

    args = args or ()
    kwargs = kwargs or {}

    nvl = kwargs.pop("nvl", False)

    if renpy.config.menu_arguments_callback is not None:
        args, kwargs = renpy.config.menu_arguments_callback(*args, **kwargs)

    if renpy.config.old_substitutions:

        def substitute(s):
            return s % renpy.exports.tag_quoting_dict

    else:

        def substitute(s):
            return s

    if item_arguments is None:
        item_arguments = [ ((), {}) ] * len(items)

    # Filter the list of items on the set_expr:
    if set_expr:
        set = renpy.python.py_eval(set_expr) # @ReservedAssignment

        new_items = [ ]
        new_item_arguments = [ ]

        for i, ia in zip(items, item_arguments):
            if i[0] not in set:
                new_items.append(i)
                new_item_arguments.append(ia)

        items = new_items
        item_arguments = new_item_arguments
    else:
        set = None # @ReservedAssignment

    # Filter the list of items to only include ones for which the
    # condition is true.

    if renpy.config.menu_actions:

        location = renpy.game.context().current

        new_items = [ ]

        for (label, condition, value), (item_args, item_kwargs) in zip(items, item_arguments):
            label = substitute(label)
            condition = renpy.python.py_eval(condition)

            if (not renpy.config.menu_include_disabled) and (not condition):
                continue

            if value is not None:
                new_items.append((label, renpy.ui.ChoiceReturn(label, value, location, sensitive=condition, args=item_args, kwargs=item_kwargs)))
            else:
                new_items.append((label, None))

    else:

        new_items = [ (substitute(label), value)
                      for label, condition, value in items
                      if renpy.python.py_eval(condition) ]

    # Check to see if there's at least one choice in set of items:
    choices = [ value for label, value in new_items if value is not None ]

    # If not, bail out.
    if not choices:
        return None

    old_menu_args = renpy.exports.menu_args
    old_menu_kwargs = renpy.exports.menu_kwargs

    # Show the menu.
    try:
        renpy.exports.menu_args = args
        renpy.exports.menu_kwargs = kwargs

        if nvl:
            rv = renpy.store.nvl_menu(new_items) # type: ignore
        else:
            rv = renpy.store.menu(new_items)

    finally:
        renpy.exports.menu_args = old_menu_args
        renpy.exports.menu_kwargs = old_menu_kwargs

    # If we have a set, fill it in with the label of the chosen item.
    if set is not None and rv is not None:
        for label, condition, value in items:
            if value == rv:
                try:
                    set.append(label)
                except AttributeError:
                    set.add(label)

    return rv


def choice_for_skipping():
    """
    :doc: other

    Tells Ren'Py that a choice is coming up soon. This currently has
    two effects:

    * If Ren'Py is skipping, and the Skip After Choices preferences is set
      to stop skipping, skipping is terminated.

    * An auto-save is triggered.
    """

    if renpy.config.skipping and not renpy.game.preferences.skip_after_choices: # type: ignore
        renpy.config.skipping = None

    if renpy.config.autosave_on_choice and not renpy.game.after_rollback:
        renpy.loadsave.force_autosave(True)


def predict_menu():
    """
    :undocumented:

    Predicts widgets that are used by the menu.
    """

    # This only makes sense for non-NVL menus. But when we have
    # NVL menus, they're likely to have already been predicted.
    #
    # An item lets us load imagebuttons as necessary.

    if not renpy.config.choice_screen_chosen:
        return

    items = [ ("Menu Prediction", True, False) ]

    renpy.exports.predict_screen(
        "choice",
        items=items,
        )


class MenuEntry(tuple):
    """
    The object passed into the choice screen.
    """


def display_menu(items,
                 window_style='menu_window',
                 interact=True,
                 with_none=None,
                 caption_style='menu_caption',
                 choice_style='menu_choice',
                 choice_chosen_style='menu_choice_chosen',
                 choice_button_style='menu_choice_button',
                 choice_chosen_button_style='menu_choice_chosen_button',
                 scope=(),
                 widget_properties=None,
                 screen="choice",
                 type="menu", # @ReservedAssignment
                 predict_only=False,
                 _layer=None,
                 _args=None,
                 _kwargs=None,
                 **kwargs):
    """
    :doc: se_menu
    :name: renpy.display_menu
    :args: (items, *, interact=True, screen="choice", type="menu", _layer=None, args=None, kwargs=None)

    This displays a menu to the user. `items` should be a list of 2-item tuples.
    In each tuple, the first item is a textual label, and the second item is
    the value to be returned if that item is selected. If the value is None,
    the first item is used as a menu caption.

    This function takes many optional arguments, of which only a few are documented.
    Except for `items`, all arguments should be given as keyword arguments.

    `interact`
        If false, the menu is displayed, but no interaction is performed.

    `screen`
        The name of the screen used to display the menu.

    `type`
        May be "menu" or "nvl". If "nvl", the menu is displayed in NVL mode.
        Otherwise, it is displayed in ADV mode.

    `_layer`
        The layer to display the menu on. If not given, defaults to :var:`config.choice_layer`
        for normal choice menus, and :var:`config.nvl_choice_layer` for NVL choice menus.

    `_args`
        If not None, this should be a tuple containing the positional :ref:`menu arguments <menu-arguments>`
        supplied to this menu.

    `_kwargs`
        If not None, this should be a dict containing the keyword :ref:`menu arguments <menu-arguments>`
        supplied to this menu.

    Note that most Ren'Py games do not use menu captions, but use narration
    instead. To display a menu using narration, write::

        $ narrator("Which direction would you like to go?", interact=False)
        $ result = renpy.display_menu([ ("East", "east"), ("West", "west") ])

    If you need to supply per-item arguments, use :class:`renpy.Choice` objects as the values. For example::

        renpy.display_menu([
            ("East", renpy.Choice("east", icon="right_arrow"),
            ("West", renpy.Choice("west", icon="left_arrow"),
            ])
    """

    if _args is not None or _kwargs is not None:
        menu_args = _args or ()
        menu_kwargs = _kwargs or {}

        if renpy.config.menu_arguments_callback is not None:
            menu_args, menu_kwargs = renpy.config.menu_arguments_callback(*menu_args, **menu_kwargs)

    else:
        menu_args, menu_kwargs = get_menu_args()

    screen = menu_kwargs.pop("screen", screen)
    with_none = menu_kwargs.pop("_with_none", with_none)
    mode = menu_kwargs.pop("_mode", type)
    layer = menu_kwargs.pop("_layer", _layer)

    if interact:
        renpy.exports.mode(mode)
        choice_for_skipping()

        if not predict_only:
            if renpy.config.choice_empty_window and (not renpy.game.context().scene_lists.shown_window):
                renpy.config.choice_empty_window("", interact=False)

    choices = [ ]

    for _, val in items:
        if isinstance(val, renpy.ui.ChoiceReturn):
            val = val.value

        if val is None:
            continue

        choices.append(val)

    # Roll forward.
    roll_forward = renpy.exports.roll_forward_info()

    if roll_forward not in choices:
        roll_forward = None

    # Auto choosing.
    if renpy.config.auto_choice_delay:

        renpy.ui.pausebehavior(renpy.config.auto_choice_delay,
                               renpy.exports.random.choice(choices))

    # The location
    location = renpy.game.context().current

    # change behavior for fixed rollback
    if renpy.exports.in_fixed_rollback() and renpy.config.fix_rollback_without_choice:
        renpy.ui.saybehavior()

    scope = dict(scope)

    scope.update(menu_kwargs) # type: ignore

    # Show the menu.
    if renpy.exports.has_screen(screen):

        item_actions = [ ]

        if widget_properties is None:
            props = { }
        else:
            props = widget_properties

        for (label, value) in items:

            if not label:
                value = None


            if isinstance(value, renpy.ui.Choice):
                action = renpy.ui.ChoiceReturn(label, value.value, location)
                chosen = action.get_chosen()
                item_args = value.args
                item_kwargs = value.kwargs

            elif isinstance(value, renpy.ui.ChoiceReturn):
                action = value
                chosen = action.get_chosen()
                item_args = action.args
                item_kwargs = action.kwargs

            elif value is not None:
                action = renpy.ui.ChoiceReturn(label, value, location)
                chosen = action.get_chosen()
                item_args = ()
                item_kwargs = { }

            else:
                action = None
                chosen = False
                item_args = ()
                item_kwargs = { }

            if renpy.config.choice_screen_chosen:
                me = MenuEntry((label, action, chosen))
            else:
                me = MenuEntry((label, action))

            me.caption = label # type: ignore
            me.action = action # type: ignore
            me.chosen = chosen # type: ignore
            me.args = item_args # type: ignore
            me.kwargs = item_kwargs # type: ignore

            item_actions.append(me)

        if layer is None:
            if type == "nvl":
                layer = renpy.config.nvl_choice_layer
            else:
                layer = renpy.config.choice_layer

        renpy.exports.show_screen(
            screen,
            items=item_actions,
            _widget_properties=props,
            _transient=True,
            _layer=layer,
            *menu_args,
            **scope)

    else:
        renpy.exports.shown_window()

        renpy.ui.window(style=window_style, focus="menu")
        renpy.ui.menu(items,
                      location=renpy.game.context().current,
                      focus="choices",
                      default=True,
                      caption_style=caption_style,
                      choice_style=choice_style,
                      choice_chosen_style=choice_chosen_style,
                      choice_button_style=choice_button_style,
                      choice_chosen_button_style=choice_chosen_button_style,
                      **kwargs)

    if renpy.config.menu_showed_window:
        renpy.exports.shown_window()

    log = renpy.exports.log

    # Log the chosen choice.
    for label, val in items:
        if val is not None:
            log("Choice: " + label)
        else:
            log(label)

    log("")

    if interact:

        rv = renpy.ui.interact(mouse='menu', type=type, roll_forward=roll_forward)

        for label, val in items:

            if isinstance(val, renpy.ui.ChoiceReturn):
                val = val.value

            if rv == val:
                log("Player chose: " + label)
                break
        else:
            log("No choice chosen.")

        log("")

        renpy.exports.checkpoint(rv)

        if with_none is None:
            with_none = renpy.config.implicit_with_none

        if with_none:
            renpy.game.interface.do_with(None, None)

        return rv

    return None
