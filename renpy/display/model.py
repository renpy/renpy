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

import renpy


class Texture(object):

    texture_wrap = None

    def __init__(self, displayable, focus, main, fit, texture_wrap):

        displayable = renpy.easy.displayable(displayable)

        if displayable._duplicatable:
            displayable = displayable._duplicate(None)
            displayable._unique()

        displayable = renpy.display.im.unoptimized_texture(displayable)

        self.displayable = displayable
        self.focus = focus
        self.main = main
        self.fit = fit
        self.texture_wrap = texture_wrap

    def _in_current_store(self):

        d = self.displayable._in_current_store()

        if d is self.displayable:
            return self

        return Texture(d, self.focus, self.main, self.fit)


class Model(renpy.display.displayable.Displayable):
    """
    :doc: model_displayable class

    This is a displayable that causes Ren'Py to create a 2D or 3D model
    for use with the model-based renderer, that will be drawn in a single
    operation with the shaders given here, or selected by an enclosing
    Transform or Displayable.

    `size`
        If not None, this should be a width, height tuple, that's used to
        give the size of the Model. If not given, the model is the size
        of the area provided to it. The fit parameter to a texture takes
        precedence.

    If no mesh method is called, a mesh that sets a_position and a_tex_coord
    to match the way Ren'Py loads textures is created if at least one texture
    is supplied. Otherwise, a mesh that only sets a_position is used.

    All methods on this calls return the displayable the method is called
    on, making it possible to chain calls.
    """

    def __init__(self, size=None, **properties):
        super(Model, self).__init__(**properties)

        self.size = size
        self.textures = [ ]

        self._mesh = True

        self.shaders = [ ]
        self.uniforms = { }
        self.properties = { }

    def grid_mesh(self, width, height):
        """
        :doc: model_displayable method

        Creates a mesh that consists of a width x height grid of evenly
        spaced points, connecting each point to the closest points
        vertically and horizontally, and dividing each rectangle in
        the grid so created into triangles.

        `width`, `height`
            The number of points in the horizontal vertical directions,
            a integer that is at least 2.

        """

        if (width < 2) or (height < 2):
            raise Exception("The width and height of a grid_mesh must be >= 2.")

        self._mesh = ("grid", width, height)
        return self

    def texture(self, displayable, focus=False, main=False, fit=False, texture_wrap=None):
        """
        :doc: model_displayable method

        Add a texture to this model, by rendering the given displayable.
        The first texture added will be ``tex0``, the second ``tex1``, a
        and so on.

        `focus`
            If true, focus events are passed to the displayable. It's
            assumed that coordinate relative to the model map 1:1 with
            coordinates relative to the displayable.

        `main`
            If true, this is marked as a main child of this displayable,
            which allows it to be inspected using the displayable
            inspector.

        `fit`
            If true, the Model is given the size of the displayable.
            This may only be true for one texture.

        `texture_wrap`
            If not None, this is the :ref:`gl_texture wrap GL property <gl-properties>` that will be applied
            to this texture.
        """

        self.textures.append(Texture(displayable, focus, main, fit, texture_wrap))
        return self

    def child(self, displayable, fit=False):
        """
        :doc: model_displayable method

        This is the same as the texture method, except that the `focus`
        and `main` parameters are set to true.
        """

        self.texture(displayable, focus=True, main=True, fit=fit)
        return self

    def shader(self, shader):
        """
        :doc: model_displayable method

        Adds a shader to this model.

        `shader`
            A string given the name of a shader to use with this model.
        """

        self.shaders.append(shader)
        return self

    def uniform(self, name, value):
        """
        :doc: model_displayable method

        Sets the value of a uniform that is passed to the shaders.

        `name`
            A string giving the name of the uniform to set, including the
            "u\\_" prefix.

        `value`
            The value of the uniform. Either a float, a 2, 3, or 4 element
            tuple of floats, or a Matrix.
        """

        self.uniforms[name] = value
        return self

    def property(self, name, value):
        """
        :doc: model_displayable method

        Sets the value of a gl property.

        `name`
            A string giving the name of the GL property, including the "gl\\_"
            prefix.

        `value`
            The value of the gl property.

        """

        self.properties[name] = value
        return self

    ############################################################################

    def _handles_event(self, event):
        for i in self.textures:
            if i.displayable._handles_event(event):
                return True

        return False

    def set_style_prefix(self, prefix, root):
        super(Model, self).set_style_prefix(prefix, root)

        for i in self.textures:
            i.displayable.set_style_prefix(prefix, False)

    def _in_current_store(self):

        textures = [ ]

        changed = False

        for old in self.textures:
            new = old._in_current_store()
            changed |= (old is not new)
            textures.append(new)

        if not changed:
            return self

        rv = self._copy()
        rv.textures = textures

        return rv

    def visit(self):
        return [ i.displayable for i in self.textures ]

    def render(self, width, height, st, at):

        if not renpy.display.render.models:
            raise Exception("The Model displayable may only be used when model-based rendering is active.")

        if self.size is not None:
            width, height = self.size

        renders = [ renpy.display.im.render_for_texture(i.displayable, width, height, st, at) for i in self.textures ]

        for cr, t in zip(renders, self.textures):
            if t.fit:
                width, height = cr.get_size()

        rv = renpy.display.render.Render(width, height)

        for i, (cr, t) in enumerate(zip(renders, self.textures)):
            rv.blit(cr, (0, 0), focus=t.focus, main=t.main)

            if t.texture_wrap is not None:
                rv.add_property("texture_wrap_tex{}".format(i), t.texture_wrap)

        if self._mesh is None:

            if self.textures:
                rv.mesh = renpy.gl2.gl2mesh2.Mesh2.texture_rectangle(
                    0.0, 0.0, width, height,
                    0.0, 0.0, 1.0, 1.0,
                    )
            else:

                rv.mesh = renpy.gl2.gl2mesh2.Mesh2.rectangle(
                    0.0, 0.0, width, height,
                    )

        elif isinstance(self._mesh, tuple):

            if self._mesh[0] == "grid":
                _, mesh_width, mesh_height = self._mesh

                rv.mesh = renpy.gl2.gl2mesh2.Mesh2.texture_grid_mesh(
                    mesh_width, mesh_height,
                    0.0, 0.0, width, height,
                    0.0, 0.0, 1.0, 1.0)

        else:
            rv.mesh = self._mesh

        for i in self.shaders:
            rv.add_shader(i)

        for k, v in self.uniforms.items():
            rv.add_uniform(k, v)

        for k, v in self.properties.items():
            rv.add_property(k, v)

        return rv
