# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

init -1600 python:

    ##########################################################################
    # TransformViewer
    class TransformViewer(object):
        def __init__(self):

            self.int_range = 1500
            self.float_range = 7.0
            # layer->tag->property->value
            self.state_org = {}
            # {property:(default, float)}, default is used when property can't be got.
            self.props_default = {
            "xpos":(0., False),
            "ypos":(0., False),
            "xanchor":(0., False),
            "yanchor":(0., False),
            "xzoom":(1., True),
            "yzoom":(1., True),
            "zoom":(1., True),
            "rotate":(0, False),
            "alpha":(1., True),
            "additive":(0., True),
            }

        def init(self):
            if not config.developer:
                return
            sle = renpy.game.context().scene_lists
            # back up for reset()
            for layer in config.layers:
                self.state_org[layer] = {}
                for tag in sle.layers[layer]:
                    d = sle.get_displayable_by_tag(layer, tag[0])
                    if isinstance(d, renpy.display.screen.ScreenDisplayable):
                        break
                    pos = renpy.get_placement(d)
                    state = getattr(d, "state", None)

                    self.state_org[layer][tag[0]] = {}
                    for p in ["xpos", "ypos", "xanchor", "yanchor"]:
                        self.state_org[layer][tag[0]][p] = getattr(pos, p, None)
                    for p in self.props_default:
                        if not self.state_org[layer][tag[0]].has_key(p):
                            self.state_org[layer][tag[0]][p] = getattr(state, p, None)

        def reset(self):
            for layer in config.layers:
                for tag, props in self.state_org[layer].iteritems():
                    if tag and props:
                        kwargs = props.copy()
                        for p in self.props_default:
                            if kwargs[p] is None and p != "rotate":
                                kwargs[p] = self.props_default[p][0]
                        renpy.show(tag, [Transform(**kwargs)], layer=layer)
            renpy.restart_interaction()

        def generate_changed(self, layer, tag, prop, int=False):
            def changed(v):
                kwargs = {}
                for p in self.props_default:
                    kwargs[p] = self.get_state(layer, tag, p, False)

                if int and not self.props_default[prop][1]:
                    kwargs[prop] = v - self.int_range
                else:
                    kwargs[prop] = v -self.float_range
                renpy.show(tag, [Transform(**kwargs)], layer=layer)
                renpy.restart_interaction()
            return changed

        def get_state(self, layer, tag, prop, default=True):
            sle = renpy.game.context().scene_lists

            if tag:
                d = sle.get_displayable_by_tag(layer, tag)
                pos = renpy.get_placement(d)
                state = getattr(pos, prop, None)
                if state is None:
                    state = getattr(getattr(d, "state", None), prop, None)
                # set default
                if state is None and default:
                    state = self.props_default[prop][0]
                if state and self.props_default[prop][1]:
                    state = float(state)
                return state
            return None

        def put_prop_clipboard(self, prop, value):
            try:
                from pygame import scrap, locals
                scrap.put(locals.SCRAP_TEXT, "%s %s" % (prop, value))
            except ImportError:
                renpy.notify(_("Can't open clipboard"))
            else:
                renpy.notify(__('Putted "%s %s" on clipboard') % (prop, value))

        def put_show_clipboard(self, tag, layer):
            string = "show %s onlayer %s" % (tag, layer)
            for k, v in self.props_default.iteritems():
                value = self.get_state(layer, tag, k)
                if value != v[0]:
                    if string.find(":") < 0:
                        string += ":\n    "
                    string += "%s %s " % (k, value)
            try:
                from pygame import scrap, locals
                scrap.put(locals.SCRAP_TEXT, string)
            except ImportError:
                renpy.notify(_("Can't open clipboard"))
            else:
                renpy.notify(__('Putted "%s" on clipboard') % string)

        def edit_value(self, function, int=False):
            v = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen")
            if v:
                try:
                    if int:
                        v = renpy.python.py_eval(v) + self.int_range
                    else:
                        v = renpy.python.py_eval(v) + self.float_range
                    function(v)
                except:
                    renpy.notify(_("Please type value"))
    _transform_viewer = TransformViewer()

    ##########################################################################
    # CameraViewer
    class CameraViewer(object):

        def __init__(self):
            self.range_camera_pos   = 6000
            self.range_rotate       = 360
            self.range_layer_z   = 10000

        def init(self):
            if not config.developer:
                return
            self._camera_x = _camera_x
            self._camera_y = _camera_y
            self._camera_z = _camera_z
            self._camera_rotate = _camera_rotate
            self._3d_layers = _3d_layers.copy()

        def camera_reset(self):
            camera_move(self._camera_x, self._camera_y, self._camera_z, self._camera_rotate)
            renpy.restart_interaction()

        def layer_reset(self):
            global _3d_layers
            for layer in _3d_layers:
                layer_move(layer, self._3d_layers[layer])
            renpy.restart_interaction()

        def x_changed(self, v):
            camera_move(v - self.range_camera_pos, _camera_y, _camera_z, _camera_rotate)
            renpy.restart_interaction()

        def y_changed(self, v):
            camera_move(_camera_x, v - self.range_camera_pos, _camera_z, _camera_rotate)
            renpy.restart_interaction()

        def z_changed(self, v):
            camera_move(_camera_x, _camera_y, v - self.range_camera_pos, _camera_rotate)
            renpy.restart_interaction()

        def r_changed(self, v):
            camera_move(_camera_x, _camera_y, _camera_z, v - self.range_rotate)
            renpy.restart_interaction()

        def generate_layer_z_changed(self, l):
            def layer_z_changed(v):
                layer_move(l, v)
                renpy.restart_interaction()
            return layer_z_changed

        def put_clipboard(self, camera_tab, layer=""):
            string = '$camera_move(%s, %s, %s, %s, duration=0)' % (_camera_x, _camera_y, _camera_z, _camera_rotate)
            if not camera_tab:
                string = '$layer_move("%s", %s, duration=0)' % (layer, _3d_layers[layer])
            try:
                from pygame import scrap, locals
                scrap.put(locals.SCRAP_TEXT, string)
            except:
                renpy.notify(_("Can't open clipboard"))
            else:
                renpy.notify(__("Putted '%s' on clipboard") % string)

        def edit_value(self, function, range):
            v = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen")
            if v:
                try:
                    function(renpy.python.py_eval(v) + range)
                except:
                    renpy.notify(_("Please type value"))
    _camera_viewer = CameraViewer()

    def _position_viewer():
        _transform_viewer.init()
        _camera_viewer.init()
        renpy.invoke_in_new_context(renpy.call_screen, "_position_viewer")
        _camera_viewer.layer_reset()
        _camera_viewer.camera_reset()

screen _position_viewer(tab="images", layer="master", tag=""):
    key "game_menu" action Return()
    zorder 10

    frame:
        xfill True
        style_group "position_viewer"
        has vbox

        hbox:
            xfill False
            textbutton _("Images") action [SelectedIf(tab == "images"), Show("_position_viewer", tab="images")]
            textbutton _("3D Layers") action [SelectedIf(tab == "3D"), Show("_position_viewer", tab="3D")]
            textbutton _("Camera") action [SelectedIf(tab == "camera"), Show("_position_viewer", tab="camera")]
        null height 10
        if tab == "images":
            hbox:
                xfill False
                label _("layers")
                for l in config.layers:
                    if l not in ["screens", "transient", "overlay"]:
                        textbutton "[l]" action [SelectedIf(l == layer), Show("_position_viewer", tab=tab, layer=l)]
            hbox:
                xfill False
                label _("images")
                for t in _transform_viewer.state_org[layer]:
                    textbutton "[t]" action [SelectedIf(t == tag), Show("_position_viewer", tab=tab, layer=layer, tag=t)]

            if tag:
                textbutton _("clip board") action Function(_transform_viewer.put_show_clipboard, tag, layer)
                for p in sorted(_transform_viewer.props_default.keys()):
                    $state = _transform_viewer.get_state(layer, tag, p)
                    if isinstance(state, int):
                        hbox:
                            $ f = _transform_viewer.generate_changed(layer, tag, p, True)
                            textbutton "[p]" action Function(_transform_viewer.put_prop_clipboard, p, state)
                            textbutton "[state]" action Function(_transform_viewer.edit_value, f, int)
                            bar adjustment ui.adjustment(range=_transform_viewer.int_range*2, value=state+_transform_viewer.int_range, page=1, changed=f) xalign 1.
                    elif isinstance(state, float):
                        hbox:
                            $ f = _transform_viewer.generate_changed(layer, tag, p)
                            textbutton "[p]" action Function(_transform_viewer.put_prop_clipboard, p, state)
                            textbutton "[state:>.4]" action Function(_transform_viewer.edit_value, f)
                            bar adjustment ui.adjustment(range=_transform_viewer.float_range*2, value=state+_transform_viewer.float_range, page=.05, changed=f) xalign 1.
        elif tab == "camera":
            textbutton _("clip board") action Function(_camera_viewer.put_clipboard, True)
            hbox:
                label "x"
                textbutton "[_camera_x]" action Function(_camera_viewer.edit_value, _camera_viewer.x_changed, _camera_viewer.range_camera_pos)
                bar adjustment ui.adjustment(range=_camera_viewer.range_camera_pos*2, value=_camera_x+_camera_viewer.range_camera_pos, page=1, changed=_camera_viewer.x_changed) xalign 1.
            hbox:
                label "y"
                textbutton "[_camera_y]" action Function(_camera_viewer.edit_value, _camera_viewer.y_changed, _camera_viewer.range_camera_pos)
                bar adjustment ui.adjustment(range=_camera_viewer.range_camera_pos*2, value=_camera_y+_camera_viewer.range_camera_pos, page=1, changed=_camera_viewer.y_changed) xalign 1.
            hbox:
                label "z"
                textbutton "[_camera_z]" action Function(_camera_viewer.edit_value, _camera_viewer.z_changed, _camera_viewer.range_camera_pos)
                bar adjustment ui.adjustment(range=_camera_viewer.range_camera_pos*2, value=_camera_z+_camera_viewer.range_camera_pos, page=1, changed=_camera_viewer.z_changed) xalign 1.
            hbox:
                label "rotate"
                textbutton "[_camera_rotate]" action Function(_camera_viewer.edit_value, _camera_viewer.r_changed, _camera_viewer.range_rotate)
                bar adjustment ui.adjustment(range=_camera_viewer.range_rotate*2, value=_camera_rotate+_camera_viewer.range_rotate, page=1, changed=_camera_viewer.r_changed) xalign 1.
        elif tab == "3D":
            for layer in sorted(_3d_layers.keys()):
                hbox:
                    textbutton "[layer]" action Function(_camera_viewer.put_clipboard, False, layer)
                    textbutton "{}".format(int(_3d_layers[layer])) action Function(_camera_viewer.edit_value, _camera_viewer.generate_layer_z_changed(layer), 0)
                    bar adjustment ui.adjustment(range=_camera_viewer.range_layer_z, value=_3d_layers[layer], page=1, changed=_camera_viewer.generate_layer_z_changed(layer)) xalign 1.
        hbox:
            xfill False
            xalign 1.
            if tab == "images":
                textbutton _("reset") action [_transform_viewer.reset, renpy.restart_interaction]
            elif tab == "camera":
                textbutton _("reset") action [_camera_viewer.camera_reset, renpy.restart_interaction]
            elif tab == "3D":
                textbutton _("reset") action [_camera_viewer.layer_reset, renpy.restart_interaction]
            textbutton _("close") action Return()

init -1600:
    style position_viewer_frame background "#0006"
    style position_viewer_button size_group "transform_viewer"
    style position_viewer_button_text xalign .5
    style position_viewer_label xminimum 100
    style position_viewer_vbox xfill True

screen _input_screen(message="type value", default=""):
    modal True
    zorder 100
    key "game_menu" action Return("")

    frame:
        style_group "input_screen"

        has vbox

        label message

        hbox:
            input default default

init -1600:
    style input_screen_frame xfill True ypos .1 xmargin .05 ymargin .05
    style input_screen_vbox xfill True spacing 30
    style input_screen_label xalign .5
    style input_screen_hbox  xalign .5
