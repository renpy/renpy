Model-Based Rendering
=====================

While Ren'Py is primarily used with two dimensional rectangular images that
are common in visual novels, underneath the hood it has a model-based renderer
intended to to take advantage of features found in modern GPUs. This allows
for a number of visual effects that would not otherwise be possible.

As a warning, this is one of the most advanced features available in Ren'Py.
In many cases, it's not necessary to understand how model-based rendering
works behind the scenes - features like :tpref:`matrixcolor` and Live2D support
can be used without understanding how Model-Based rendering works, and more
such features will be added to the understanding. This documentation is
intended for very advanced creators, and for developers looking to add
to Ren'Py itself.

As of Ren'Py 7.4 (late 2020), Model-Based rendering needs to be enabled to
be used. This is done by setting config.gl2 to True, using::

    define config.gl2 = True

.. var:: config.gl2 = False

    If true, Ren'Py will default to using a model-based renderer.

As it's expected that model-based rendering will become the only renderer
in the near future, the rest of this documentation is written as if model-based
rendering is enabled all the time.

Model-Based Rendering is one of the most advanced features in Ren'Py, and
this documentation may be hard to understand without first looking at the
OpenGL, OpenGL ES, GLSL, and GLSL ES manual. What's more, since there are
portions of the models that are passed directly to your GPU drivers, which
may accept erroneous inputs, it's important to check on multiple kinds of
hardware.


Models, Renders, and Drawing Operations
---------------------------------------

The fundamental thing that Ren'Py draws to the screen is a Model. A model
consists of the following things:

* A Mesh of one or more triangles. A triangle consists of
  three vertices (corners), each of which contains a position in two or
  three-dimensional space, and may contain additional information, most
  commonly texture coordinates.

* Zero or more textures, with the precise number allowed being limited by the
  GPUs your game can run on. All GPUs should support at least three textures
  per model. A texture is a rectangle containing image data that's been loaded
  on the GPU, either directly or using a render-to-texture operation.

* A list of shader part names. Ren'Py uses these shader parts to created shaders,
  which are programs that are run on the GPU to render the model. Shader part
  names can be prefixed with a "-" to prevent that shader part from being used.

* Uniform values. A uniform is additional data that is the same throughout the
  model. For example, when a model represents a solid color, the color is a
  uniform.

* GL properties. GL properties are flags that further control how things
  are rendered, such as the minification/magnification modes and the
  color mask.

As Ren'Py usually draws more than one thing to the screen, it creates a
tree of :class:`Render` objects. These Render objects may have Models or
other Renders as children. (A Render object can also be turned into a Model.
as described below.) A Render contains:

* A list of children, including a 2-dimensional offset that is applied to
  each child.

* A :class:`Matrix` that describes how the children are transformed in
  three-dimensional space.

* Lists of shader part names, uniforms, and GL properties that are applied
  to the Models when being drawn.

* Flags that determine if the drawable-space clipping polygon should be
  updated.

Ren'Py draws the screen by performing a depth-first walk through the tree of
Renders, until a Model is encountered. During this walk, Ren'Py updates a
matrix transforming the location of the Model, a clipping polygon, and
lists of shader parts, uniforms, and gl properties. When a Model is encountered
as part of this walk, the appropriate shader program is activated on the GPU,
all information is transferred, and a drawing operation occurs.


Where Models are Created
------------------------

Ren'Py creates Models automatically as part of its normal operation.
The main reason to understand where models are created is that models
correspond to drawing operations, and hence are the units that shaders
are applied to.

Images and Image Manipulators
    These create a model with a mesh containing two triangles that cover
    the rectangle of the image. The mesh contains texture coordinates.
    The model uses the "renpy.texture" shader.

:func:`Solid`
    The Solid displayable creates a mesh containing two triangles, and no
    texture coordinates. The model uses the "renpy.solid" shader,
    with the color placed in the ``u_renpy_solid_color`` uniform.

:func:`Dissolve`, :func:`ImageDissolve`, :func:`AlphaDissolve`, :func:`Pixellate`, :func:`AlphaMask`, :func:`Flatten`
    Each of these transforms and displayables creates a Model with a mesh,
    shaders, and uniforms as is needed for its purposes.

Live2D
    Live2D displayables may created multiple Models when rendered, generally
    one Model for each layer.

:func:`Transform` and ATL
    A Transform creates a model if :tpref:`mesh` is true, or if :tpref:`blur`
    is being used. In this case, the children of the Transform are rendered
    to textures, with the mesh of the first texture being used for the mesh
    associated with the model.

    Not every transform creates a Model. Some transforms will simply add
    shaders and uniforms to a Render (such as transforms that use
    :tpref:`blur` or :tpref:`alpha`). Other transforms simply affect
    geometry.

:class:`Render`
    A Transform creates a model if its ``mesh`` attribute is True.
    is being used. In this case, the children of the Render are rendered
    to textures, with the mesh of the first texture being used for
    the mesh associated with the model.

It's expected that Ren'Py will add more ways of creating models in the
future.

Shader Program Generation
-------------------------

Ren'Py generates a shader program by first assembling a list of shader part
names. This list consists of "renpy.geometry", the list of shader parts
taken from Renders, and the list of shader parts found in the Model being
drawn.

The shader parts are then deduplicated. If a shader part begins with "-",
it is removed from the list, as is the rest of that part without the
leading "-". (So "-renpy.geometry" will cause itself and "renpy.geometry"
to be removed.)

Ren'Py then takes the list of shader parts, and retrieves lists of variables,
functions, vertex shade parts, and fragment shader parts. These are, in turn,
used to generate the source code for shaders, with the parts of the vertex and
fragement shaders being included in low-number to high-number priority order.

Ren'Py keeps a cache of all combinations of shader parts that have ever been
used in game/cache/shaders.txt, and loads them at startup. If major changes
in shader use occur, this file should be edited or deleted so it can be
re-created with valid data.


Creating a Custom Shader
-------------------------

New shader parts can be created by calling the renpy.register_shader
function and supplying portions of GLSL shaders.

Generally, shader parts should be of the form "namespace.part", such as
"mygame.recolor" or "mylibrary.warp". Names beginning with "renpy." or
"live2d." are reserved for Ren'Py, as are names beginning with _.

.. include:: inc/register_shader

Ren'Py supports only the following variable types:

* float (a Python float)
* vec2 (a tuple of 2 floats)
* vec3 (a tuple of 3 floats)
* vec4 (a tuple of 4 floats)
* mat4 (a :class:`Matrix`)
* sampler2D (supplied by Ren'Py)

Uniform variables should begin with u\_, attributes with a\_, and varying
variables with v\_. Names starting with u_renpy\_, a_renpy, and v_renpy
are reserved, as as the standard variables given below.

As a general sketch for priority levels, priority 100 sets up geometry,
priority 200 determines the initial fragment color (gl_FragColor), and
higher-numbered priorities can apply effects to alter that color.

Here's an example of a custom shader part that applies a gradient across
each model it is used to render::

    init python:

        renpy.register_shader("example.gradient", variables="""
            uniform vec4 u_gradient_left;
            uniform vec4 u_gradient_right;
            uniform vec2 u_model_size;
            varying float v_gradient_done;
        """, vertex_300="""
            v_gradient_done = a_position.x / u_model_size.x;
        """, fragment_300="""
            gl_FragColor *= mix(u_gradient_left, u_gradient_right, v_gradient_done);
        """)

The custom shader can then be applied using a transform::

    transform gradient:
        shader "example.gradient"
        u_gradient_left (1.0, 0.0, 0.0, 1.0)
        u_gradient_right (0.0, 0.0, 1.0, 1.0)

    show eileen happy at gradient

Transforms and Model-Based Rendering
------------------------------------

Model-Based rendering adds the following properties to ATL and :func:`Transform`:

.. transform-property:: mesh

    :type: None or True or tuple
    :default: None

    If not None, this Transform will be rendered as a model. This means:

    * A mesh will be created. If this is a 2-component tuple, it's taken
      as the number of points in the mesh, in the x and y directions. (Eacn
      dimension must be at least 2.) If True, the mesh is taken from the
      child.
    * The child of this transform will be rendered to a texture.
    * The renpy.texture shader will be added.

.. transform-property:: shader

    :type: None or str or list of str
    :default: None

    If not None, a shader part name or list of shader part names that will be
    applied to the  this Render (if a Model is created) or the Models reached
    through this Render.

In addition, uniforms that start with u\_ and not u_renpy are made available
as Transform properties. GL properties are made available as transform
properties starting with gl\_. For example, the color_mask property is made
available as gl_color_mask.


Uniforms and Attributes
-----------------------

The following uniforms are made available to all Models.

``vec2 u_model_size``
    The width and height of the model.

``vec2 u_lod_bias``
    The level of detail bias to apply to texture lookups.

``mat4 u_transform``
    The transform used project virtual pixels to the OpenGL viewport.

``float u_time``
    The time of the frame. The epoch is undefined, so it's best to treat
    this as a number that increases by one second a second. The time is
    modulo 86400, so it will reset to 0.0 once a day.

``vec4 u_random``
    Four random numbers between 0.0 and 1.0 that are (with incredibly high
    likelyhood) different from frame to frame.

``sampler2D tex0``, ``sampler2D tex1``, ``sampler2D tex2``
    If textures are available, the corresponding samplers are placed in
    this variable.

``vec2 res0``, ``vec2 res1``, ``vec2 res2``
    If textures are available, the size of the textures are placed in these
    variables. When the texture is loaded from disk, this is the size of the
    image file. After a render to texture, it's the number of drawable pixels
    the rendered texture covered.

The following attributes are available to all models:

``vec4 a_position``
    The position of the vertex being rendered.

If textures are available, so is the following attribute:

``vec2 a_tex_coord``
    The coordinate that this vertex projects to inside the textures.


GL Properties
-------------

GL properties change the global state of OpenGL, or the Model-Based renderer.

``color_masks``
    This is expecting to be a 4-tuple of booleans, corresponding to the four
    channels of a pixel (red, green, blue, and alpha). If a given channel is
    treu, the draw operation will write to that pixel. Otherwise, it will
    not.

Default Shader Parts
--------------------

.. include:: inc/shadersource



