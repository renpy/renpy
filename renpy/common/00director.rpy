# Copyright 2017 Tom Rothamel <pytom@bishoujo.us>

# Permission to use, copy, modify, and/or distribute this software for
# non-commerical purposes is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# For the purpose of this license, when using this software to develop a
# another software program, this program is being used commerically if
# payment is required to distribute that program, to use that program, or
# to access any feature in that program, or if the program presents
# advertising to its user.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

# TODO:
#
# - Allow the creator to specify a list of tags they are interested in,
#   disabling the auto-detection.

init offset = -1101

default persistent._director_bottom = False

init python in director:
    from store import Action, config
    import store

    # A set of tags that will not be show to the user.
    tag_blacklist = { "black", "text", "vtext", "side" }

    # A set of tags that should only be used with the scene statement.
    scene_tags = { "bg" }

    # The set of tags that should only be used with the show statement.
    show_tags = set()

    # Should we try to filter out tags that have other tags as their
    # prefix (as are used alot in layerimages)?
    blacklist_prefixed_tags = True

    # A list of transforms to use.
    transforms = [ "left", "center", "right" ]

    # A list of transitions to use.
    transitions = [ "dissolve", "pixellate" ]

    # A list of audio channels we know about.
    audio_channels = [ "music", "sound", "audio" ]

    # The name of the voice channel.
    voice_channel = "voice"

    # A list of audio patterns to use for channels that do not have a
    # more specific list of patterns already defined.
    audio_patterns = [ "*.opus", "*.ogg", "*.mp3" ]

    # A map from channel name to the audio patterns to use for that channel.
    audio_channel_patterns = { }

    # A map from channel name to the audio files available on that channel.
    audio_files = { }

    # The spacing between a non-display line and a display line, or vice
    # versa.
    spacing = 1

    # The spacing between two display lines.
    director_spacing = 0

    # The spacing between two non-display lines.
    other_spacing = 0

    # The maximum height of viewports containing scrolling information.
    viewport_height = 280

    # Is the director enabled? Used by the tutorial to protect itself.
    enable = True

    state = renpy.session.get("director", None)

    # A list of statements we find too uninteresting to present to the
    # creator.
    UNINTERESTING_NODES = (
        renpy.ast.Translate,
        renpy.ast.EndTranslate,
    )

    # Nodes that are only interesting when on a line by itself.
    ALONE_NODES = (
        renpy.ast.Label,
        renpy.ast.Pass,
    )

    def audio_code_to_filename(channel, fn):
        return fn

    def audio_filename_to_code(channel, fn):
        return fn

    def audio_filename_to_display(channel, fn):
        return fn

    def is_play(n):
        return isinstance(n, renpy.ast.UserStatement) and n.get_name().startswith("play ")

    def is_queue(n):
        return isinstance(n, renpy.ast.UserStatement) and n.get_name().startswith("queue ")

    def is_stop(n):
        return isinstance(n, renpy.ast.UserStatement) and n.get_name().startswith("stop ")

    def is_voice(n):
        return isinstance(n, renpy.ast.UserStatement) and (n.get_name() == "voice")


    def is_interesting(n):

        if isinstance(n, (
            renpy.ast.Show,
            renpy.ast.Hide,
            renpy.ast.Scene,
            renpy.ast.With,
        )):

            return True

        if is_play(n) or is_queue(n) or is_stop(n) or is_voice(n):
            return True

        return False


    # Initialize the state object if it doesn't exist.
    if state is None:

        state = store.NoRollback()

        # Is the directory currently active.
        state.active = False

        # Should the director screen be shown.
        state.show_director = False

        # The list of lines we've seen recently.
        state.lines = [ ]

        # The mode we're in.
        state.mode = "lines"

        # The filename and linenumber of the line we're editing,
        state.filename = ""
        state.linenumber = 0

        # What tags are currently showing?
        state.showing = set()

        # What kind of statement is this?
        state.kind = None
        state.original_kind = None

        # The tag we're updating.
        state.tag = ""
        state.original_tag = ""

        # The attributes of the image we're updating.
        state.attributes = [ ]
        state.original_attributes = [ ]

        # The transforms applied to the image.
        state.transforms = [ ]
        state.original_transforms = [ ]

        # A list of image tags the current image is behind.
        state.behind = [ ]
        state.original_behind = [ ]

        # The transition in a with statement.
        state.transition = None
        state.original_transition = None

        # The audio channel.
        state.channel = None
        state.original_channel = None

        # The audio file.
        state.audio = None
        state.original_audio = None

        # NOTE: Remember to add new states to the Cancel function.

        # Has the new line been added to ast.
        state.added_statement = None

        # Are we changing the script? (Does the node needed to be removed?)
        state.change = False

        # The position of the first line.
        state.old_pos = None

        renpy.session["director"] = state

    def interact_base():
        """
        This is called by interact to update our data structures.
        """

        if renpy.game.interface.trans_pause:
            return False

        show_director = False

        # Update the line log.
        lines = renpy.get_line_log()
        renpy.clear_line_log()

        if lines:
            pos = (lines[0].filename, lines[0].line)
            if pos != state.old_pos:
                state.old_pos = pos
                renpy.hide_screen("director")

        # Update state.line to the current line.
        state.line = renpy.get_filename_line()

        # State.lines is the list of lines we've just seen, along with
        # the actions used to edit those lines.
        for lle in lines[-30:]:
            if isinstance(lle.node, renpy.ast.Say):
                state.lines = [ ]
                break

        for lle in lines[-30:]:

            filename = lle.filename
            line = lle.line
            node = lle.node

            if isinstance(node, UNINTERESTING_NODES):
                continue

            if isinstance(node, ALONE_NODES):
                if [ i for i in renpy.scriptedit.nodes_on_line(filename, line) if not isinstance(i, ALONE_NODES) ]:
                    continue

            if filename.startswith("renpy/"):
                show_director = False
                continue
            else:
                show_director = True

            text = renpy.scriptedit.get_line_text(filename, line)

            if text is None:
                text = ""

            text = text.strip()

            short_fn = filename.rpartition('/')[2]
            pos = "{}:{:04d}".format(short_fn, line)

            if lle.abnormal:
                add_action = None
            else:
                add_action = AddStatement(lle)

            if is_interesting(node):
                change_action = ChangeStatement(lle, node)
            else:
                change_action = None

            state.lines.append((
                pos,
                text,
                add_action,
                change_action,
            ))

        return show_director


    def interact():
        """
        This is called once per interaction, to update the list of lines
        being displayed, and also to show or hide the director as appropriate.
        """

        show_director = interact_base()

        # Show the director screen.
        if show_director and state.show_director and (renpy.context_nesting_level() == 0):
            if not renpy.get_screen("director"):
                renpy.show_screen("director")
        else:
            if renpy.get_screen("director"):
                renpy.hide_screen("director")

    def line_log_callback(lle):
        """
        This annotates a line log entry with more information.
        """
        lle.showing = set(renpy.get_showing_tags())


    def init():
        """
        This is called once at game start, to reconfigured Ren'Py to
        support the ID.
        """

        config.clear_lines = False
        config.line_log = True
        config.line_log_callbacks = [ line_log_callback ]

        config.start_interact_callbacks.append(interact)

    if state.active:
        init()

    def command():
        """
        This can be used to invoke the ID from the command line.
        """

        if not state.active:
            state.active = True
            init()

        return True

    renpy.arguments.register_command("director", command)


    def get_scene_show_hide_statement():


        if state.kind == "scene" and state.tag is None:
            return "scene"

        if state.tag is None:
            return None

        if state.kind == "hide":

            attributes = state.attributes

        else:

            if state.change and (state.attributes == state.original_attributes):
                attributes = state.attributes
            else:

                attributes = get_image_attributes()

                if attributes is None:
                    return None

        rv = [ state.kind ]

        rv.append(state.tag)
        rv.extend(attributes)

        rv = " ".join(rv)

        if state.transforms:
            rv += " at " + ", ".join(state.transforms)

        if state.behind:
            rv += " behind " + ",".join(state.behind)

        return rv

    def quote_audio():
        """
        Returns the quoted audio filename.
        """

        if state.audio is None:
            return None

        if state.channel is not None:
            audio = audio_filename_to_code(state.channel, state.audio)
        else:
            audio = state.audio

        return "'" + audio.replace("\\", "\\\\").replace("'", "\\'") + "'"


    def get_play_queue_statement():
        if state.channel is None:
            return None

        if state.audio is None:
            return None

        return "{} {} {}".format(state.kind, state.channel, quote_audio())

    def get_stop_statement():
        if state.channel is None:
            return None

        return "{} {}".format(state.kind, state.channel)

    def get_voice_statement():
        if state.audio is None:
            return None

        return "voice {}".format(quote_audio())

    def get_statement():
        """
        If a statement is defined enough to implement, returns the text
        that can be added to the AST. Otherwise, returns None.
        """

        if state.kind is None:
            rv = None

        elif state.kind == "with":
            rv = "with {}".format(state.transition)

        elif state.kind in ("play", "queue"):
            rv = get_play_queue_statement()

        elif state.kind == "stop":
            rv = get_stop_statement()

        elif state.kind == "voice":
            rv = get_voice_statement()

        else:
            rv = get_scene_show_hide_statement()

        return rv

    def update_ast(force=False):
        """
        Updates the abstract syntax tree to match the current state, forcing
        a rollback if something significant has changed. This always forces
        an interaction restart.
        """

        statement = get_statement()

        if (state.added_statement == statement) and (not force):
            renpy.restart_interaction()
            return

        linenumber = state.linenumber

        if statement:
            renpy.scriptedit.add_to_ast_before(statement, state.filename, linenumber)
            linenumber += 1

        if state.added_statement is not None:
            renpy.scriptedit.remove_from_ast(state.filename, linenumber)

        state.added_statement = statement

        renpy.rollback(checkpoints=0, force=True, greedy=True)

    def dump_script():
        for i in range(0, 100):
            key = ('game/script.rpy', i)
            if key in renpy.scriptedit.lines:
                print(key, renpy.scriptedit.lines[key].text)

    def pick_tag():
        """
        If there is only one valid tag, choose it and move to attribute mode.
        """

        tags = get_tags()

        if state.mode != "tag":
            return

        if len(tags) != 1:
            return

        state.tag = tags[0]

        if state.kind == "hide":
            return

        state.mode = "attributes"


    def find_statement(filename, line, delta, limit=10):
        """
        Tries to find a statement near `line`. If it can't find it on `line`
        itself, it searches forward (if `delta`) is positive or back (if `delta`)
        is negative.

        Returns the line number and nodes for the statement, or (None, None) if the
        statement is not found after searching `limit` lines.
        """

        for _i in range(limit):

            nodes = renpy.scriptedit.nodes_on_line(filename, line)
            if nodes:
                return line, nodes

            line += delta

        return None, None

    def needs_space(filename, line):
        """
        Returns True if there should be a space between (filename, line-1) and
        (filename, line).
        """


        previous, previous_nodes = find_statement(filename, line-1, -1)

        if previous is None:
            return None

        next, next_nodes = find_statement(filename, line, 1)

        if next is None:
            return None


        def display(nodes):
            for n in nodes:
                if is_interesting(n):
                    return True

            return False

        previous_display = display(previous_nodes)
        next_display = display(next_nodes)

        if previous_display ^ next_display:
            return spacing
        elif previous_display:
            return director_spacing
        else:
            return other_spacing

    def is_spacing(filename, line):

        line = renpy.scriptedit.get_full_text(filename, line)

        if line is None:
            return False

        return not line.strip()


    def adjust_spacing_before(filename, line):
        """
        Adjusts the spacing between (filename, line) and the line before it.
        """

        line, _ = find_statement(filename, line, 1)

        if line is None:
            return

        space = needs_space(filename, line)

        if space is None:
            return

        previous, _ = find_statement(filename, line - 1, -1)

        blanks = [ ]

        for i in range(previous + 1, line):
            if not is_spacing(filename, i):
                break

            blanks.append(i)

        delta_space = space - len(blanks)

        if delta_space > 0:
            for _ in range(delta_space):
                renpy.scriptedit.adjust_ast_linenumbers(filename, previous + 1, 1)
                renpy.scriptedit.insert_line_before('', filename, previous + 1)

        elif delta_space < 0:
            blanks.reverse()
            blanks = blanks[space:]

            for i in blanks:
                renpy.scriptedit.adjust_ast_linenumbers(filename, i, -1)
                renpy.scriptedit.remove_line(filename, i)


    def add_spacing(filename, line):
        adjust_spacing_before(filename, line + 1)
        adjust_spacing_before(filename, line)

    def remove_spacing(filename, line):
        adjust_spacing_before(filename, line)


    # Screen support functions #################################################

    def get_tags():
        """
        Returns a list of tags that are valid for the current statement kind.
        """

        if state.kind == "scene":
            rv = [ i for i in renpy.get_available_image_tags() if not i.startswith("_") if i not in tag_blacklist if i in scene_tags ]
        elif state.kind == "show":
            if show_tags:
                rv = [ i for i in renpy.get_available_image_tags() if not i.startswith("_") if i not in tag_blacklist if i in show_tags ]
            else:
                rv = [ i for i in renpy.get_available_image_tags() if not i.startswith("_") if i not in tag_blacklist if i not in scene_tags ]
        elif state.kind == "hide":
            rv = [ i for i in renpy.get_available_image_tags() if i in state.showing if not i.startswith("_") if i not in tag_blacklist if i not in scene_tags ]
        else:
            rv = [ ]

        rv.sort(key=component_key)
        return rv

    def get_attributes():
        """
        Returns a list of attributes that are valid for the current tag.
        """

        if not state.tag:
            return [ ]

        return renpy.get_ordered_image_attributes(state.tag, [ ], component_key)

    def get_transforms():
        """
        Returns a list of transforms that are valid for the current tag.
        """

        return transforms

    def get_image_attributes():
        """
        Returns the list of attributes in the current image, or None if
        no image is known.
        """

        if state.tag is None:
            return None

        return renpy.check_image_attributes(state.tag, state.attributes)

    def get_ordered_attributes():
        """
        Returns the list of attributes in the order they appear in the
        current image (if known), or in the order they were selected
        otherwise.
        """

        attrs = get_image_attributes()

        if attrs is not None:
            return attrs

        return state.attributes

    def get_behind_tags(exclude=None):
        """
        Get a list of tags the current tag can be placed behind.
        """

        rv = [ ]

        for t in state.showing:
            if t in scene_tags:
                continue

            if t == exclude:
                continue

            rv.append(t)

        return rv

    # Actions ##################################################################

    class Start(Action):
        """
        This action starts the director and displays the lines screen.
        """

        def __call__(self):

            if not state.show_director:

                if store._menu:
                    return None

                if not config.developer:
                    return None

                if not enable:
                    renpy.notify(_("The interactive director is not enabled here."))
                    return None

            if state.show_director:
                return None

            state.show_director = True
            state.mode = "lines"

            if state.active:

                renpy.show_screen("director")
                renpy.restart_interaction()

                return

            # renpy.session["compile"] = True
            renpy.session["_greedy_rollback"] = True

            state.active = True

            store._reload_game()

        def get_sensitive(self):
            return (not state.active) or (not state.show_director)

    class Stop(Action):
        """
        This hides the director interface.
        """

        def __call__(self):
            state.show_director = False

            if renpy.get_screen("director"):
                renpy.hide_screen("director")

            renpy.restart_interaction()


    class AddStatement(Action):
        """
        An action that adds a new statement before `filename`:`linenumber`.
        """

        def __init__(self, lle):
            self.lle = lle

            self.sensitive = renpy.scriptedit.can_add_before(self.lle.filename, self.lle.line)

        def get_sensitive(self):
            return self.sensitive

        def __call__(self):

            state.filename = self.lle.filename
            state.linenumber = self.lle.line
            state.showing = self.lle.showing

            state.kind = None
            state.mode = "kind"

            state.tag = None
            state.original_tag = None

            state.attributes = [ ]
            state.original_attributes = [ ]

            state.transforms = [ ]
            state.original_transforms = [ ]

            state.transition = None
            state.original_transition = None

            state.behind = [ ]
            state.original_behind = [ ]

            state.channel = None
            state.original_channel = None

            state.audio = None
            state.original_audio = None

            state.added_statement = None
            state.change = False

            update_ast()


    def is_scene_show_hide_editable(node):
        """
        Return true if a Scene, Show, or Hide ATL node is editable, or
        False otherwise.
        """

        if not node.imspec:
            return True

        if node.imspec[1]: # expression
            return False

        if node.imspec[2]: # tag
            return False

        if node.imspec[4]: # layer
            return False

        if node.imspec[5]: # zorder
            return False

        if getattr(node, "atl", None):
            return False

        return True


    class ChangeStatement(Action):
        """
        An action that changes the statement at `filename`:`linenumber`.

        `node`
            Should be the AST node corresponding to that statement.
        """

        def __init__(self, lle, node):
            self.lle = lle

            self.tag = None
            self.attributes = [ ]
            self.transforms = [ ]
            self.transition = None
            self.behind = [ ]

            self.channel = None
            self.audio = None

            self.sensitive = True

            def audio(n):

                self.sensitive = False

                name = n.parsed[0]
                p = n.parsed[1]

                self.kind = name[0]
                self.channel = p["channel"] or name[1]

                if "file" in p:
                    try:
                        self.audio = eval(p["file"])
                    except:
                        return

                    self.audio = audio_code_to_filename(self.channel, self.audio)
                else:
                    self.audio = None

                if p.get("loop", None):
                    return

                fadeout = p.get("fadeout", None)

                if (fadeout is not None) and (fadeout != "None"):
                    return

                if p.get("if_changed", False):
                    return

                if p.get("fadein", "0") != "0":
                    return

                self.sensitive = True


            if isinstance(node, renpy.ast.Show):
                self.kind = "show"

                self.tag = node.imspec[0][0]
                self.attributes = list(node.imspec[0][1:])
                self.transforms = list(node.imspec[3])
                self.behind = list(node.imspec[6])

                self.sensitive = is_scene_show_hide_editable(node)

            elif isinstance(node, renpy.ast.Scene):
                self.kind = "scene"

                # The scene statement does not need to show an image.
                if node.imspec is not None:

                    self.tag = node.imspec[0][0]
                    self.attributes = list(node.imspec[0][1:])
                    self.transforms = list(node.imspec[3])
                    self.behind = list(node.imspec[6])

                else:

                    self.tag = None
                    self.attributes = [ ]
                    self.transforms = [ ]
                    self.behind = [ ]

                self.sensitive = is_scene_show_hide_editable(node)

            elif isinstance(node, renpy.ast.Hide):
                self.kind = "hide"

                self.tag = node.imspec[0][0]
                self.attributes = list(node.imspec[0][1:])
                self.transforms = list(node.imspec[3])

                self.sensitive = is_scene_show_hide_editable(node)

            elif isinstance(node, renpy.ast.With):
                self.kind = "with"
                self.transition = node.expr

            elif is_play(node) or is_queue(node) or is_stop(node):
                audio(node)

            elif is_voice(node):
                p = node.parsed[1]

                self.kind = "voice"
                self.sensitive = False
                self.channel = voice_channel

                try:
                    self.audio = eval(p)
                except:
                    return

                self.audio = audio_code_to_filename(self.channel, self.audio)
                self.sensitive = True

        def get_sensitive(self):
            return self.sensitive

        def __call__(self):
            state.filename = self.lle.filename
            state.linenumber = self.lle.line
            state.showing = self.lle.showing

            state.kind = self.kind
            state.original_kind = self.kind

            if self.kind == "with":
                state.mode = "with"
            elif self.kind == "hide":
                state.mode = "tag"
            elif self.kind == "play" or self.kind == "queue":
                state.mode = "audio"
            elif self.kind == "stop":
                state.mode = "channel"
            elif self.kind == "voice":
                state.mode = "audio"
            else:
                if self.tag is None:
                    state.mode = "tag"
                else:
                    state.mode = "attributes"

            state.tag = self.tag
            state.original_tag = self.tag

            state.attributes = self.attributes
            state.original_attributes = list(self.attributes)

            state.transforms = list(self.transforms)
            state.original_transforms = list(self.transforms)

            state.transition = self.transition
            state.original_transition = self.transition

            state.behind = self.behind
            state.original_behind = list(self.behind)

            state.channel = self.channel
            state.original_channel = self.channel

            state.audio = self.audio
            state.original_audio = self.audio

            state.added_statement = True
            state.change = True

            update_ast()


    class SetKind(Action):

        def __init__(self, kind):
            self.kind = kind

        def __call__(self):

            if self.kind != state.kind:
                state.kind = self.kind
                state.tag = None
                state.attributes = [ ]

            if self.kind in ("scene", "show", "hide"):
                state.mode = "tag"
                pick_tag()

            if self.kind == "with":
                state.mode = "with"

            if self.kind in ("play", "queue", "stop"):
                state.mode = "channel"

            if self.kind == "voice":
                state.channel = "voice"
                state.mode = "audio"

            update_ast()


    class SetTag(Action):
        """
        An action that sets the image tag.
        """

        def __init__(self, tag):
            self.tag = tag

        def __call__(self):

            if state.tag != self.tag:

                state.tag = self.tag
                state.attributes = [ ]

            if state.kind != "hide":
                state.mode = "attributes"

            update_ast()

        def get_selected(self):
            return self.tag == state.tag


    class ToggleAttribute(Action):
        """
        This action toggles on and off an attribute. If an attribute being
        toggled on conflicts with other attributes, those attributes are
        removed.

        Then the AST is updated.
        """

        def __init__(self, attribute):
            self.attribute = attribute

        def __call__(self):
            if self.attribute in state.attributes:
                state.attributes.remove(self.attribute)
            else:

                state.attributes.append(self.attribute)

                compatible = set()

                for i in renpy.get_ordered_image_attributes(state.tag, [ self.attribute ]):
                    compatible.add(i)

                state.attributes = [ i for i in state.attributes if i in compatible ]

            update_ast()

        def get_selected(self):
            return self.attribute in state.attributes


    class SetList(Action):
        """
        When clicked once, sets l to [ v ]. When clicked again, sets l to [ ]
        """

        def __init__(self, l, v):
            self.l = l
            self.v = v

        def __call__(self):
            if self.v in self.l:
                self.l.remove(self.v)
            else:
                self.l[:] = [ self.v ]

            update_ast()

        def get_selected(self):
            return self.v in self.l


    class ToggleList(Action):
        """
        Toggles the presence or absence of v in l, appending it to the end
        of the list when necessary.
        """

        def __init__(self, l, v):
            self.l = l
            self.v = v

        def __call__(self):
            if self.v in self.l:
                self.l.remove(self.v)
            else:
                self.l.append(self.v)

            update_ast()

        def get_selected(self):
            return self.v in self.l


    class SetTransition(Action):
        """
        This sets the transition used by a with statement.
        """

        def __init__(self, transition):
            self.transition = transition

        def __call__(self):
            state.transition = self.transition

            update_ast()

        def get_selected(self):
            return self.transition == state.transition


    class SetChannel(Action):
        """
        This sets the channel used by an audio statement.
        """

        def __init__(self, channel):
            self.channel = channel

        def __call__(self):
            if state.kind != "stop":
                state.mode = "audio"

            state.channel = self.channel

            update_ast()

        def get_selected(self):
            return self.channel == state.channel


    class SetAudio(Action):
        """
        This sets the audio file played by a statement.
        """

        def __init__(self, filename):
            self.filename = filename

        def __call__(self):
            state.audio = self.filename

            update_ast()

        def get_selected(self):
            return state.audio == self.filename


    class Commit(Action):
        """
        Commits the current statement to the .rpy files.
        """

        def __call__(self):
            statement = get_statement()

            if statement:
                renpy.scriptedit.insert_line_before(statement, state.filename, state.linenumber)

            if state.change:
                if statement:
                    renpy.scriptedit.remove_line(state.filename, state.linenumber + 1)
                else:
                    renpy.scriptedit.remove_line(state.filename, state.linenumber)

            if not state.change and statement:
                add_spacing(state.filename, state.linenumber)

            if state.change and not statement:
                remove_spacing(state.filename, state.linenumber)

            state.mode = "lines"
            renpy.clear_line_log()
            renpy.rollback(checkpoints=0, force=True, greedy=True)

        def get_sensitive(self):
            return get_statement()

    class Reset(Action):
        """
        This action resets the AST to what it was when we started adjusting the
        statement.
        """

        def __call__(self):

            state.kind = state.original_kind
            state.tag = state.original_tag
            state.attributes = state.original_attributes
            state.transforms = state.original_transforms

            if state.kind is None:
                state.mode = "kind"
            elif state.tag is None:
                state.mode = "tag"

            update_ast()

    class Cancel(Action):
        """
        This action cancels the operation, resetting the AST and returning to
        the lines screen.
        """

        def __call__(self):

            state.kind = state.original_kind
            state.tag = state.original_tag
            state.attributes = state.original_attributes
            state.transforms = state.original_transforms

            state.transition = state.original_transition

            state.channel = state.original_channel
            state.audio = state.original_audio

            state.mode = "lines"

            update_ast()

    class Remove(Action):
        """
        This action removes the current line from the AST and the script.
        """

        def __call__(self):

            state.kind = None
            state.tag = None
            state.mode = "lines"

            try:
                update_ast(force=True)
            finally:
                if state.change:
                    renpy.scriptedit.remove_line(state.filename, state.linenumber)


    # Displayables #############################################################

    class SemiModal(renpy.Displayable):
        """
        This wraps a displayable, and ignores
        """

        def __init__(self, child):
            renpy.Displayable.__init__(self)

            self.child = child
            self.w = 0
            self.h = 0

        def per_interact(self):
            renpy.display.render.redraw(self, 0)

        def render(self, width, height, st, at):

            if renpy.get_screen("confirm"):
                return renpy.Render(0, 0)

            surf = renpy.render(self.child, width, height, st, at)
            w, h = surf.get_size()

            self.w = w
            self.h = h

            rv = renpy.Render(w, h)
            rv.blit(surf, (0, 0))

            return rv

        def event(self, ev, x, y, st):

            if renpy.get_screen("confirm"):
                return

            rv = self.child.event(ev, x, y, st)
            if rv is not None:
                return rv

            if ev.type == renpy.display.core.TIMEEVENT:
                return None

            if state.mode != "lines":

                if renpy.map_event(ev, "rollback") or renpy.map_event(ev, "rollforward"):
                    raise renpy.IgnoreEvent()

                raise renpy.display.layout.IgnoreLayers()

            if (0 <= x < self.w) and (0 <= y < self.h):
                raise renpy.display.layout.IgnoreLayers()

            return None

        def get_placement(self):
            return self.child.get_placement()

        def visit(self):
            return [ self.child ]

    # Sort #####################################################################

    import re

    def component_key(s):
        """
        Sorts l in a way that groups numbers together and treats them as
        numbers (so c10 comes after c9, not c1.)
        """
        rv = [ ]

        for i, v in enumerate(re.split(r'(\d+)', s.lower())):
            if not v:
                continue

            if i & 1:
                v = int(v)

            rv.append(v)

        return tuple(rv)

init 2202 python hide in director:

    if state.active:

        for name, file, _line in renpy.dump.transforms:
            if file.startswith("renpy/common/"):
                continue

            if file == "game/screens.rpy":
                continue

            transforms.append(name)
            transforms.sort(key=component_key)

        import fnmatch

        for c in audio_channels + [ voice_channel ]:

            patterns = audio_channel_patterns.get(c, audio_patterns)

            if c not in audio_files:
                audio_files[c] = [ ]

            for fn in renpy.list_files():

                for p in patterns:
                    if fnmatch.fnmatch(fn, p):
                        break
                else:
                    continue

                audio_files[c].append(fn)

            audio_files[c].sort()

    if blacklist_prefixed_tags:

        available = set()

        for i in sorted(renpy.get_available_image_tags()):

            blacklist = False

            prefix = i

            while prefix:
                prefix, _, _  = prefix.rpartition("_")
                if prefix in available:
                    blacklist = True

            if i in scene_tags:
                blacklist = False
            if i in show_tags:
                blacklist = False

            if blacklist:
                tag_blacklist.add(i)
            else:
                available.add(i)



# Styles and screens ###########################################################

style director_frame is _frame:
    xfill True
    yfill False
    ypadding 0

style director_top_frame is director_frame:
    background "#d0d0d0d0"
    yalign 0.0

style director_bottom_frame is director_frame:
    background "#d0d0d0f0"
    yalign 1.0


style director_text is _text:
    size 18

style director_label

style director_label_text is director_text:
    bold True

style director_button is empty

style director_button_text is director_text:
    color "#405060"
    hover_color "#048"
    insensitive_color "#00000020"
    selected_color "#0099cc"

style director_edit_button is director_button:
    xsize 18

style director_edit_button_text is director_button_text:
    font "DejaVuSans.ttf"
    xalign 0.5

style director_action_button is director_button

style director_action_button_text is director_button_text:
    size 26

style director_icon_action_button is director_action_button:
    xpadding 10

style director_icon_action_button_text is director_action_button_text:
    font "DejaVuSans.ttf"

style director_statement_text is director_text:
    size 20

style director_statement_button is director_button

style director_statement_button_text is director_button_text:
    size 20

style director_vscrollbar is _vscrollbar

screen director_move_button():

    if persistent._director_bottom:

        textbutton _("⬆"):
            style "director_icon_action_button"
            action SetField(persistent, "_director_bottom", False)
            xalign 1.0
    else:

        textbutton _("⬇"):
            style "director_icon_action_button"
            action SetField(persistent, "_director_bottom", True)
            xalign 1.0

screen director_lines(state):

    frame:
        style "empty"
        background Solid("#fff8", xsize=20, xpos=gui._scale(300))

        has vbox:
            xfill True

        viewport:
            scrollbars "vertical"
            ymaximum director.viewport_height
            mousewheel True
            yinitial 1.0
            viewport_yfill False

            has vbox:
                xfill True

            for line_pos, line_text, add_action, change_action in state.lines:

                fixed:
                    yfit True
                    textbutton "+":
                        xpos gui._scale(300)
                        action add_action
                        style "director_edit_button"
                        alt ("add before " + line_text)

                fixed:
                    yfit True

                    text "[line_pos]":
                        xpos (gui._scale(300) - 10)
                        xalign 1.0
                        text_align 1.0
                        style "director_text"

                    if change_action:
                        textbutton "✎":
                            action change_action
                            xpos gui._scale(300)
                            style "director_edit_button"
                            alt ("change " + line_text)

                    frame:
                        style "empty"
                        left_padding (gui._scale(300) + 30)

                        text "[line_text!q]" style "director_text"

        null height 14

        fixed:
            yfit True

            hbox:
                xpos (gui._scale(300) + 30)

                textbutton _("Done"):
                    action director.Stop()
                    style "director_action_button"

            use director_move_button()



screen director_statement(state):

    $ kind = state.kind or __("(statement)")
    $ tag = state.tag or __("(tag)")
    $ attributes =  " ".join(director.get_ordered_attributes()) or __("(attributes)")
    $ transforms = ", ".join(state.transforms) or __("(transform)")
    $ behind = ", ".join(state.behind) or __("(tag)")
    $ behind_tags = director.get_behind_tags(state.tag)

    hbox:
        style_prefix "director_statement"

        textbutton "[kind] " action SetField(state, "mode", "kind")
        textbutton "[tag] " action SetField(state, "mode", "tag")

        if state.attributes or state.kind in { "scene", "show"}:
            textbutton "[attributes] " action SetField(state, "mode", "attributes")

        if state.transforms or state.kind in { "scene", "show"}:
            text "at "
            textbutton "[transforms] " action SetField(state, "mode", "transform")

        if behind_tags and (state.kind in { "show" }):
            text "behind "
            textbutton "[behind]" action SetField(state, "mode", "behind")

    null height 14

screen director_with_statement(state):

    $ transition = state.transition or __("(transition)")

    hbox:
        style_prefix "director_statement"

        text "with "
        textbutton "[transition]" action SetField(state, "mode", "with")

    null height 14

screen director_audio_statement(state):

    $ channel = state.channel or __("(channel)")
    $ audio = director.quote_audio() or __("(filename)")

    hbox:
        style_prefix "director_statement"

        textbutton "[state.kind] " action SetField(state, "mode", "kind")

        if state.kind != "voice":
            textbutton "[channel] " action SetField(state, "mode", "channel")

        if state.kind != "stop":
            textbutton "[audio!q]" action SetField(state, "mode", "audio")

    null height 14

screen director_footer(state):

    null height 14

    fixed:

        yfit True

        hbox:
            style_prefix "director_action"

            spacing 26

            if state.change:
                textbutton _("Change") action director.Commit()
            else:
                textbutton _("Add") action director.Commit()


            textbutton _("Cancel") action director.Cancel()

            if state.change:
                textbutton _("Remove") action director.Remove()

        use director_move_button()


# Formats the choices.
screen director_choices(title):

    text title size 20

    frame:
        style "empty"
        left_margin 10

        viewport:
            scrollbars "vertical"
            ymaximum director.viewport_height
            mousewheel True
            yinitial 0.0
            viewport_yfill False

            hbox:
                box_wrap True
                spacing 20

                transclude


screen director_kind(state):

    vbox:
        xfill True

        use director_statement(state)

        use director_choices(_("Statement:")):

            textbutton "scene" action director.SetKind("scene")
            textbutton "show" action director.SetKind("show")
            textbutton "hide" action director.SetKind("hide")
            textbutton "with" action director.SetKind("with")
            textbutton "play" action director.SetKind("play")
            textbutton "queue" action director.SetKind("queue")
            textbutton "stop" action director.SetKind("stop")
            textbutton "voice" action director.SetKind("voice")

        use director_footer(state)


screen director_tag(state):

    vbox:
        xfill True

        use director_statement(state)

        use director_choices(_("Tag:")):

            for t in director.get_tags():
                textbutton "[t]":
                    action director.SetTag(t)

        use director_footer(state)


screen director_attributes(state):

    vbox:
        xfill True

        use director_statement(state)

        use director_choices(_("Attributes:")):

            for t in director.get_attributes():
                textbutton "[t]":
                    action director.ToggleAttribute(t)
                    style "director_button"
                    ypadding 0

        use director_footer(state)


screen director_transform(state):

    vbox:
        xfill True

        use director_statement(state)

        use director_choices(_("Transforms:")):

            for t in director.get_transforms():
                textbutton "[t]":
                    action director.SetList(state.transforms, t)
                    alternate director.ToggleList(state.transforms, t)
                    style "director_button"
                    ypadding 0

        use director_footer(state)


screen director_behind(state):

    vbox:
        xfill True

        use director_statement(state)

        use director_choices(_("Behind:")):

            for t in director.get_behind_tags(state.tag):
                textbutton "[t]":
                    action director.SetList(state.behind, t)
                    alternate director.ToggleList(state.behind, t)
                    style "director_button"
                    ypadding 0

        use director_footer(state)


screen director_with(state):

    vbox:
        xfill True

        use director_with_statement(state)

        use director_choices(_("Transition:")):

            for t in director.transitions:
                textbutton "[t]":
                    action director.SetTransition(t)
                    style "director_button"
                    ypadding 0

        use director_footer(state)


screen director_channel(state):

    vbox:
        xfill True

        use director_audio_statement(state)

        use director_choices(_("Channel:")):

            for c in director.audio_channels:
                textbutton "[c]":
                    action director.SetChannel(c)
                    style "director_button"
                    ypadding 0

        use director_footer(state)


screen director_audio(state):

    vbox:
        xfill True

        use director_audio_statement(state)

        use director_choices(_("Audio Filename:")):

            for fn in director.audio_files.get(state.channel, [ ]):
                $ elided_fn = director.audio_filename_to_display(state.channel, fn)

                textbutton "[elided_fn]":
                    action director.SetAudio(fn)
                    style "director_button"
                    ypadding 0

        use director_footer(state)



screen director():
    zorder 1400

    $ state = director.state

    if renpy.loadable("id/" + state.mode + ".png"):
        add ("id/" + state.mode + ".png")

    frame:
        style_prefix "director"

        style ("director_bottom_frame" if persistent._director_bottom else "director_top_frame")

        xpadding ( 0 if state.mode == "lines" else gui._scale(20) )

        at director.SemiModal

        has fixed:
            fit_first True

        if state.mode == "lines":
            use director_lines(state)
        elif state.mode == "kind":
            use director_kind(state)
        elif state.mode == "tag":
            use director_tag(state)
        elif state.mode == "attributes":
            use director_attributes(state)
        elif state.mode == "transform":
            use director_transform(state)
        elif state.mode == "behind":
            use director_behind(state)
        elif state.mode == "with":
            use director_with(state)
        elif state.mode == "channel":
            use director_channel(state)
        elif state.mode == "audio":
            use director_audio(state)

    if state.mode == "lines":
        key "director" action director.Stop()
