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
    # Camera functions

    # value of _3d_layers isn't included in rollback.
    # so I copy it many times.
    _3d_layers = {}
    _camera_x = 0
    _camera_y = 0
    _camera_z = 0
    _camera_r = 0
    _focal_length = 147.40
    _layer_z = 1848.9


    def register_3d_layer(*layers):
        """
         :doc: camera

         Register layers as 3D layers. 3D layers is applied transforms to by a
         camera motion. You can use this in game again and again.

         `layers`
              These should be the string or strings of a layer name.
         """
        global _3d_layers
        af_3d_layers = {}
        for layer in layers:
            af_3d_layers[layer] = _layer_z
        _3d_layers = af_3d_layers

    def camera_reset():
        """
         :doc: camera

         Reset a camera and 3D layers positions.
         """
        camera_move(0, 0, 0, 0)
        for layer in _3d_layers:
            layer_move(layer, _layer_z)

    def camera_move(x, y, z, rotate=0, duration=0, warper='linear', subpixel=True, loop=False):
        """
         :doc: camera

         Move the coordinate and rotate of a camera and apply transforms to all 3D layers.

         `x`
              the x coordinate of a camera
         `y`
              the y coordinate of a camera
         `z`
              the z coordinate of a camera
         `rotate`
              Defaul 0, the rotate of a camera
         `duration`
              Default 0, this is the second times taken to move a camera.
         `warper`
              Default 'linear', this should be string and the name of a warper
              registered with ATL.
         `subpixel`
              Default True, if True, causes things to be drawn on the screen
              using subpixel positioning
         `loop`
              Default False, if True, this motion repeats.
         """

        camera_moves(((x, y, z, rotate, duration), ), warper=warper, subpixel=subpixel, loop=loop)

    def layer_move(layer, z, duration=0, warper='linear', subpixel=True, loop=False):
        """
         :doc: camera

         Move the z coordinate of a layer and apply transforms to all 3D
         layers.

         `layer`
              the string of a layer name to be moved
         `z`
              the z coordinate of a layer
         `duration`
              Default 0, this is the second times taken to move a camera.
         `warper`
              Default 'linear', this should be string and the name of a warper
              registered with ATL.
         `subpixel`
              Default True, if True, causes things to be drawn on the screen
              using subpixel positioning
         `loop`
              Default False, if True, this motion repeats.
         """

        layer_moves(layer, ((z, duration), ), warper=warper, subpixel=subpixel, loop=loop)

    def camera_moves(check_points, warper='linear', loop=False, subpixel=True):
        """
         :doc: camera

         Move a camera through check points and apply transforms to all 3D
         layers.

         `check_points`
              tuples of x, y, z, rotate, duration
         `loop`
              Default False, if True, this sequence of motions repeats.
         `subpixel`
              Default True, if True, causes things to be drawn on the screen
              using subpixel positioning
         """
        global _camera_x, _camera_y, _camera_z, _camera_r

        af_3d_layers = {}
        for layer in _3d_layers:
            start_xanchor = _focal_length*_camera_x/(config.screen_width *_layer_z) + .5
            start_yanchor = _focal_length*_camera_y/(config.screen_height*_layer_z) + .5

            check_points2 = [(_camera_z, _camera_r, start_xanchor, start_yanchor, _3d_layers[layer], 0), ]
            for c in check_points:
                xanchor = _focal_length*c[0]/(config.screen_width *_layer_z) + .5
                yanchor = _focal_length*c[1]/(config.screen_height*_layer_z) + .5
                duration = float(c[4])
                check_points2.append((c[2], c[3], xanchor, yanchor, _3d_layers[layer], duration))

            renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(function=renpy.curry(_camera_trans)(check_points=check_points2, warper=warper, loop=loop, subpixel=subpixel, layer=layer))])

        _camera_x = check_points[-1][0]
        _camera_y = check_points[-1][1]
        _camera_z = check_points[-1][2]
        _camera_r = check_points[-1][3]

    def layer_moves(layer, check_points, warper='linear', loop=False, subpixel=True):
        """
         :doc: camera

         Move a layer through check points and apply transforms to the layers.

         `layer`
              the string of a layer name to be moved
         `check_points`
              tuples of z, duration
         `loop`
              Default False, if True, this sequence of motions repeats.
         `subpixel`
              Default True, if True, causes things to be drawn on the screen
              using subpixel positioning
         """
        global _3d_layers, _camera_x, _camera_y, _camera_z, _camera_r

        start_xanchor = _focal_length*_camera_x/(config.screen_width *_layer_z) + .5
        start_yanchor = _focal_length*_camera_y/(config.screen_height*_layer_z) + .5

        check_points2 = [(_camera_z, _camera_r, start_xanchor, start_yanchor, _3d_layers[layer], 0), ]
        af_3d_layers = _3d_layers.copy()
        for c in check_points:
            check_points2.append((_camera_z, _camera_r, start_xanchor, start_yanchor, c[0], float(c[1])))

        renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(function=renpy.curry(_camera_trans)(check_points=check_points2, warper=warper, loop=loop, subpixel=subpixel, layer=layer))])

        af_3d_layers[layer] = check_points[-1][0]
        _3d_layers = af_3d_layers

    def _camera_trans(tran, st, at, check_points, warper, loop, subpixel, layer):
        # check_points = (z, r, xanchor, yanchor, layer_z, duration)
        duration = check_points[-1][5]
        tran.xpos    = .5 
        tran.ypos    = .5
        if duration > 0:
            g = renpy.atl.warpers[warper](st/duration) 
            if loop:
                g = g % 1
            tran.subpixel = subpixel
            # tran.transform_anchor = True

            for i in xrange(1, len(check_points)):
                checkpoint_g = check_points[i][5]/duration
                pre_checkpoint_g = check_points[i-1][5]/duration
                if g <= checkpoint_g:
                    start = check_points[i-1]
                    goal = check_points[i]
                    ch_g = (g - pre_checkpoint_g) / (checkpoint_g - pre_checkpoint_g)

                    z = ch_g*(goal[0]-start[0])+start[0]
                    layer_z = ch_g*(goal[4]-start[4])+start[4]
                    distance = float(layer_z - z)
                    if distance == 0:
                        distance = .1

                    tran.xanchor = ch_g*(goal[2]-start[2]) + start[2]
                    tran.yanchor = ch_g*(goal[3]-start[3]) + start[3]
                    tran.rotate  = ch_g*(goal[1]  -  start[1]) + start[1]

                    if distance >= 0:
                        tran.alpha = 1
                        tran.zoom = _layer_z / distance
                    else:
                        tran.alpha = 0
                    return .005
        distance = float(check_points[-1][4] - check_points[-1][0])
        if distance == 0:
            distance = .1
        tran.xanchor = check_points[-1][2]
        tran.yanchor = check_points[-1][3]
        tran.zoom = _layer_z / distance
        tran.rotate = check_points[-1][1]
        if distance >= 0:
            tran.alpha = 1
        else:
            tran.alpha = 0
        return None
