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

# This code implements the ability to "warp" to a given location in
# the Ren'Py source code, given the filename and line number of the
# location.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *


import renpy
import operator

warp_spec = None
warping = False


def reconstruct(nodes):
    """
    Reconstructs state along a warp path without executing game logic.
    """

    global warping

    ctx = renpy.game.context()
    fields = (
        "current",
        "next_node",
        "say_attributes",
        "temporary_attributes",
        "translate_identifier",
        "alternate_translate_identifier",
        "translated",
        "deferred_translate_identifier",
    )
    old_context = {name: getattr(ctx, name) for name in fields}
    old_warping = warping
    old_skipping = renpy.config.skipping

    warping = True
    renpy.config.skipping = "fast"

    try:
        remaining = set(nodes)
        replaced = set()
        for node in nodes:
            remaining.discard(node)
            if node in replaced:
                continue

            if isinstance(node, renpy.ast.Translate):
                source = translation_nodes(node.next)
                # Do not replay the target early when it is inside a block.
                if set(source).issubset(remaining):
                    replay_node(node)
                    if ctx.next_node is not node.next:
                        replay_translation(ctx.next_node)
                        replaced.update(source)
                    continue

            replay_node(node)
            if isinstance(node, renpy.ast.Translate):
                # A partial source block has no unambiguous translated prefix.
                ctx.translated = False
    finally:
        for name, value in old_context.items():
            setattr(ctx, name, value)
        renpy.config.skipping = old_skipping
        warping = old_warping


def replay_node(node):
    ctx = renpy.game.context()
    ctx.current = node.name
    ctx.next_node = node.next

    last_say_fields = (
        "_last_say_who",
        "_last_say_what",
        "_last_say_args",
        "_last_say_kwargs",
        "_last_raw_what",
        "_side_image_attributes",
        "_side_image_attributes_reset",
    )
    missing = object()
    old_say = {name: getattr(renpy.store, name, missing) for name in last_say_fields}
    old_multiple = renpy.character.multiple_count
    old_attributes = ctx.say_attributes, ctx.temporary_attributes
    old_deferred = ctx.deferred_translate_identifier
    old_translation = ctx.translate_identifier, ctx.alternate_translate_identifier, ctx.translated
    old_retained = None

    try:
        if isinstance(node, renpy.ast.Say):
            old_retained = set(renpy.exports.get_showing_tags(renpy.store.bubble.retain_layer))

        if node.can_warp():
            node.execute()

            # TranslateSay.execute can redirect without executing the say.
            if isinstance(node, renpy.ast.TranslateSay) and ctx.next_node is not node.next:
                translated = ctx.next_node
                if isinstance(translated, renpy.ast.TranslateSay):
                    replay_node(translated)
                else:
                    replay_translation(translated)

        elif isinstance(node, (renpy.ast.Translate, renpy.ast.EndTranslate)):
            node.execute()
        else:
            clear_retain_for_node(node)

    except renpy.game.CONTROL_EXCEPTIONS:
        raise
    except Exception:
        ctx.translate_identifier, ctx.alternate_translate_identifier, ctx.translated = old_translation
        for name, value in old_say.items():
            if value is missing:
                if hasattr(renpy.store, name):
                    delattr(renpy.store, name)
            else:
                setattr(renpy.store, name, value)
        renpy.character.multiple_count = old_multiple
        if old_retained is not None:
            layer = renpy.store.bubble.retain_layer
            for tag in renpy.exports.get_showing_tags(layer):
                if tag.startswith("_retain_") and tag not in old_retained:
                    renpy.exports.hide_screen(tag, layer=layer, immediately=True)
        renpy.exports.write_log(
            "While warping, ignoring statement at %s:%s:",
            getattr(node, "filename", "<unknown>"),
            getattr(node, "linenumber", 0),
        )
        renpy.display.log.exception()
    finally:
        ctx.say_attributes, ctx.temporary_attributes = old_attributes
        ctx.deferred_translate_identifier = old_deferred
        renpy.config.skipping = "fast"


def translation_nodes(node):
    nodes = []
    seen = set()
    while node is not None and node not in seen:
        seen.add(node)
        nodes.append(node)
        if isinstance(node, (renpy.ast.EndTranslate, renpy.ast.TranslateSay)):
            break
        node = node.next
    return nodes


def replay_translation(node):
    for translated in translation_nodes(node):
        replay_node(translated)


def clear_retain_for_node(node):
    # Menus and screens remain skipped, but still delimit retained dialogue.
    bubble = renpy.store.bubble
    if bubble.statement_callback not in renpy.config.statement_callbacks:
        return

    if isinstance(node, renpy.ast.Menu):
        name = "menu"
        if node.arguments is not None and node.arguments.evaluate()[1].get("nvl") is True:
            name = "menu-nvl"
        if node.has_caption or renpy.config.choice_empty_window:
            name += "-with-caption"
    elif isinstance(node, renpy.ast.UserStatement):
        name = node.get_name()
    else:
        info = node.diff_info()
        name = getattr(info[0], "__name__", "").lower()

    bubble.statement_callback(name)


def warp():
    """
    Given a filename and line number, this attempts to warp the user
    to that filename and line number.
    """

    global warp_spec

    spec = warp_spec
    warp_spec = None

    if spec is None:
        return None

    if ":" not in spec:
        raise Exception("No : found in warp location.")

    filename, line = spec.split(":", 1)
    line = int(line)

    if not renpy.config.developer:
        raise Exception("Can't warp, developer mode disabled.")

    if not filename.startswith("game/"):
        filename = "game/" + filename

    # First, compute for each statement reachable from a scene statement,
    # one statement that reaches that statement.

    prev = {}

    seenset = set(renpy.game.script.namemap.values())

    # This is called to indicate that next can be executed following node.
    def add(node, next):
        if next is None:
            return

        if next not in prev:
            prev[next] = node
            return

        # Try to figure out which node to use.

        old = prev[next]

        def prefer(fn):
            if fn(node, old):
                return node

            if fn(old, node):
                return old

            return None

        n = None
        n = n or prefer(lambda a, b: (a.filename == next.filename) and (b.filename != next.filename))
        n = n or prefer(lambda a, b: (a.linenumber <= next.linenumber) and (b.linenumber > next.linenumber))
        n = n or prefer(lambda a, b: a.linenumber >= b.linenumber)
        n = n or node

        prev[next] = n

    for n in seenset:
        if isinstance(n, renpy.ast.Translate) and n.language:
            continue

        if isinstance(n, renpy.ast.Menu):
            for i in n.items:
                if i[2] is not None:
                    add(n, i[2][0])

        if isinstance(n, renpy.ast.Jump):
            if not n.expression and n.target in renpy.game.script.namemap:
                add(n, renpy.game.script.namemap[n.target])
                continue

        if isinstance(n, renpy.ast.While):
            add(n, n.block[0])

        if isinstance(n, renpy.ast.If):
            seen_true = False

            for condition, block in n.entries:
                add(n, block[0])

                if condition == "True":
                    seen_true = True

            if seen_true:
                continue

        if isinstance(n, renpy.ast.UserStatement):
            add(n, n.get_next())
        elif getattr(n, "next", None) is not None:
            add(n, n.next)

    # Now, attempt to find a statement preceding the line that the
    # user wants to warp to.

    candidates = [(n.linenumber, n) for n in seenset if n.filename == filename and n.linenumber <= line]

    # We didn't find any candidate statements, so give up the warp.
    if not candidates:
        raise Exception("Could not find a statement to warp to. ({})".format(spec))

    # Sort the list of candidates, so they're ordered by linenumber.
    candidates.sort(key=operator.itemgetter(0))

    # Pick the candidate immediately before (or on) the line.
    node = candidates[-1][1]

    # Now, determine a list of nodes to run while getting to this node.
    run = []
    n = node

    while True:
        n = prev.pop(n, None)
        if n:
            run.append(n)
        else:
            break

    run.reverse()

    run = run[-renpy.config.warp_limit :]

    reconstruct(run)

    # Now, return the name of the place where we will warp to. This
    # becomes the new starting point of the game.

    renpy.config.skipping = None
    renpy.game.after_rollback = True

    renpy.exports.block_rollback()

    renpy.game.context().goto_label(node.name)
    renpy.game.context().come_from(node.name, "_after_warp")
    raise renpy.execution.RestartContext()
