
3D Camera motion
================

With some limitations, Ren'Py can simulate 3D camera motion. This will easily
let you achieve a parallax effect by placing sprites and assets on a 3D field.
Ren'Py applies transforms to each layers which are registered as 3D layer by
positions of a camera and 3D layers on a 3D field to simulate 3D camera motion.

If you use this feature, in the first, set additional layers to be
registered as 3D layer.

For example, Write a code like below in options.rpy and add 'background', 'middle', 'forward'  layers.::

        config.layers = ['master', 'background', 'middle', 'forward', 'transient', 'screens', 'overlay']

Second, register layers which participate to a 3D motion as 3d layers by :func:`register_3d_layer`::

        init python:
            register_3d_layer('background', 'middle', 'forward')

Then, a camera and layers can move. ::

         label start:
             # reset a camera and layers positions
             $ camera_reset()
             scene bg onlayer background
             show A onlayer middle
             show B onlayer forward
             # It takes 0 second to move layers
             $ layer_move("background", 2000)
             $ layer_move("middle", 1500)
             $ layer_move("forward", 1000)
             with dissolve
             'It takes 1 second to move a camera to (1800, 0, 0)'
             $ camera_move(1800, 0, 0, 0, 1)
             'It takes 5 seconds to move a camera to (0, 0, 1600)'
             $ camera_move(0, 0, 1600, 0, 5)
             'A camera moves to (0, 0, 0) at the moment'
             $ camera_move(0, 0, 0)
             'It takes 1 second to rotate a camera to 180 degrees'
             $ camera_move(0, 0, 0, 180, 1)
             'It takes 1 second to rotate a camera to -180 degrees and 0.5 second to move a camera to (-1800, 0, 500)'
             $ camera_moves( ( (0, 0, 0, 0, 1), (-1800, 0, 500, 0, 1.5) ) )
             'a camera shuttles between (-1800, 0, 500) and (0, 0, 0)'
             $ camera_moves( ( (0, 0, 0, 0, .5), (-1800, 0, 500, 0, 1) ), loop=True)

When :var:`config.developer` is True, pressing position_viewer (by default,
"shift+P"), will open Position Viewer. This allow you to adjustment a camera
,3D layers and images positions by bars and manual inputs and see the result at
the moment.

Notice that 3D camera motion has some limits.:

* 3D camera motion applies transforms to 3D layers, so the show layer statement or
  :func:`renpy.show_layer_at` to 3D layers can't be usable.

* z coordinates of 3D layers don't affect the stacking order of 3d layers.

* A camera and a layer can't move at the same time.

* By default, the scene, hide statements use master or the given layer
  only. If you use 3D layers preferentially, set Ren'py like below.::

        init -1 python hide:
            def hide(name, layer='master'):
                for l in _3d_layers:
                    if renpy.showing(name, l):
                        renpy.hide(name, l)
                        break
                else:
                    renpy.hide(name, layer)

            config.hide = hide

            def scene(layer='master'):

                renpy.scene(layer)
                for l in _3d_layers:
                    renpy.scene(l)

            config.scene = scene

Camera Functions
----------------

.. include:: inc/camera
