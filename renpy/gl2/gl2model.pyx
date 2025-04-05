# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

from renpy.display.render import IDENTITY
from renpy.display.matrix import Matrix
from renpy.gl2.gl2polygon cimport Polygon
from renpy.gl2.gl2texture cimport GLTexture

from libc.math cimport ceil

cdef class GL2Model:
    """
    A model can be placed as a leaf of the tree of Renders, and contains
    everything needed to be draw to the screen.
    """

    def __init__(GL2Model self, size, mesh, shaders, uniforms=None, properties=None):
        self.width = size[0]
        self.height = size[1]
        self.mesh = mesh
        self.shaders = shaders
        self.uniforms = uniforms
        self.properties = properties
        self.cached_texture = None

        self.forward = IDENTITY
        self.reverse = IDENTITY

        self.tex0 = None
        self.tex1 = None
        self.tex2 = None
        self.tex3 = None

    def __repr__(GL2Model self):
        rv = "<{} {}x{} {} {}".format(type(self).__name__, self.width, self.height, self.shaders, self.uniforms)

        if self.forward is not IDENTITY:
            rv += "\n    forward (to mesh):\n    " + repr(self.forward).replace("\n", "\n    ")
            rv += "\n    reverse (to screen):\n    " + repr(self.reverse).replace("\n", "\n    ")

        rv += "\n    " + repr(self.mesh).replace("\n", "\n    ")
        rv += ">"

        return rv

    def load(self):
        """
        Loads the textures associated with this model.
        """

        if self.tex0 is not None:
            self.tex0.load()

        if self.tex1 is not None:
            self.tex1.load()

        if self.tex2 is not None:
            self.tex2.load()

        if self.tex3 is not None:
            self.tex3.load()

        if self.uniforms:
            for i in self.uniforms.values():
                if isinstance(i, GLTexture):
                    i.load()

    def get_size(self):
        """
        Returns the size of this GL2Model.
        """

        return (self.width, self.height)

    cpdef GL2Model copy(GL2Model self):
        """
        Creates an identical copy of the current model.
        """

        cdef GL2Model rv = GL2Model((self.width, self.height), self.mesh, self.shaders, self.uniforms, self.properties)
        rv.forward = self.forward
        rv.reverse = self.reverse

        rv.tex0 = self.tex0
        rv.tex1 = self.tex1
        rv.tex2 = self.tex2
        rv.tex3 = self.tex3

        return rv

    cpdef subsurface(GL2Model self, rect):
        """
        Given a rectangle `rect`, returns a GL2Model that only contains the
        portion of the model inside the rectangle.
        """

        cdef float x, y, w, h

        x, y, w, h = rect

        cdef GL2Model rv = self.copy()

        rv.width = <int> ceil(w)
        rv.height = <int> ceil(h)

        rv.reverse = rv.reverse * Matrix.coffset(-x, -y, 0)
        rv.forward = Matrix.coffset(x, y, 0) * rv.forward

        cdef Polygon p = Polygon.rectangle(0, 0, w, h)
        p.multiply_matrix_inplace(rv.forward)

        rv.mesh = rv.mesh.crop(p)

        return rv

    cpdef scale(GL2Model self, float factor):
        """
        Creates a new model that is this model scaled by a constant factor.
        """

        cdef float reciprocal_factor

        cdef GL2Model rv = self.copy()

        rv.width = <int> ceil(rv.width * factor)
        rv.height = <int> ceil(rv.height * factor)

        rv.reverse = rv.reverse * Matrix.scale(factor, factor, factor)

        if factor <= 0.0:
            # Map everything onto the (0, 0, 0) point for the zero-
            # scale case.
            rv.forward =  Matrix.cscale(0, 0, 0) * rv.forward
        else:
            reciprocal_factor = 1.0 / factor
            rv.forward = Matrix.cscale(reciprocal_factor, reciprocal_factor, reciprocal_factor) * rv.forward

        return rv

    cpdef void set_texture(self, int i, GL2Model texture):
        """
        Sets the i'th texture of this model to be `texture`.
        """

        if i == 0:
            self.tex0 = texture
        elif i == 1:
            self.tex1 = texture
        elif i == 2:
            self.tex2 = texture
        elif i == 3:
            self.tex3 = texture
        else:
            if self.uniforms is None:
                self.uniforms = {}

            self.uniforms["tex%d" % i] = texture
            self.uniforms["res%d" % i] = (texture.texture_width, texture.texture_height)

    cpdef GL2Model get_texture(self, int i):
        """
        Returns the i'th texture of this model.
        """

        if i == 0:
            return self.tex0
        elif i == 1:
            return self.tex1
        elif i == 2:
            return self.tex2
        elif i == 3:
            return self.tex3
        else:
            if self.uniforms is None:
                return None

            return self.uniforms.get("tex%d" % i, None)
