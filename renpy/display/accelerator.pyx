#cython: profile=False
# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

import renpy
import math
from renpy.display.matrix cimport Matrix
from renpy.display.render cimport Render, Matrix2D, render
from renpy.display.core import absolute

from sdl2 cimport *
from pygame_sdl2 cimport *

import_pygame_sdl2()

################################################################################
# Surface copying
################################################################################


def nogil_copy(src, dest):
    """
    Does a gil-less blit of src to dest, with minimal locking.
    """

    cdef SDL_Surface *src_surf
    cdef SDL_Surface *dst_surf

    src_surf = PySurface_AsSurface(src)
    dest_surf = PySurface_AsSurface(dest)

    with nogil:
        SDL_SetSurfaceBlendMode(src_surf, SDL_BLENDMODE_NONE)
        SDL_UpperBlit(src_surf, NULL, dest_surf, NULL)



def get_poi(state):
    """
    For the given state, return the poi - the point that point_to looks at.
    """

    point_to = state.point_to

    if isinstance(point_to, tuple) and len(point_to) == 3:
        return point_to

    if isinstance(point_to, renpy.display.transform.Camera):

        if state.perspective:
            raise Exception("The point_to transform property for camera should not be True.")

        layer = point_to.layer
        sle = renpy.game.context().scene_lists

        d = sle.camera_transform.get(layer, None)

        if not isinstance(d, renpy.display.motion.Transform):
            return None

        perspective = d.perspective

        if perspective is True:
            perspective = renpy.config.perspective

        elif isinstance(perspective, (int, float)):
            perspective = (renpy.config.perspective[0], perspective, renpy.config.perspective[2])

        if not perspective:
            return None

        z11 = perspective[1]
        width = renpy.config.screen_width
        height = renpy.config.screen_height

        placement = (d.xpos, d.ypos, d.xanchor, d.yanchor, d.xoffset, d.yoffset, True)
        xplacement, yplacement = renpy.display.core.place(width, height, width, height, placement)

        return (xplacement + width / 2, yplacement + height / 2, d.zpos + z11)

    raise Exception("The point_to transform property should be None, a 3-tuple (x, y, z), or True.")


################################################################################
# Transform render function
################################################################################

cdef Matrix2D IDENTITY
IDENTITY = renpy.display.render.IDENTITY


# The distance to the 1:1 plan, in the current perspective.
z11 = 0.0

def relative(n, base, limit):
    """
    A utility function that converts a relative value to an absolute value,
    using the usual Ren'Py conventions (int and absolute are passed unchanged,
    while a float is interpreted as a fraction of the limit).
    """

    if isinstance(n, (int, absolute)):
        return n
    else:
        return min(int(n * base), limit)

cdef class RenderTransform:
    """
    This class is used to render Transforms.
    """

    cdef object transform
    cdef object state

    cdef object widtho
    cdef object heighto

    cdef object perspective

    cdef Render cr
    cdef Render mr

    cdef object width
    cdef object height

    cdef object xsize
    cdef object ysize

    cdef object xo
    cdef object yo

    cdef object clipping

    cdef Matrix reverse

    def __init__(self, transform): # type: (renpy.display.transform.Transform) -> None
        self.transform = transform
        self.state = transform.state

        # The original width and heigh given to the render.
        self.widtho = 0
        self.heighto = 0

        # The perspective.
        self.perspective = None

        # The child render.
        self.cr = None # type: renpy.display.render.Render|None

        # If self.make_mesh was called, mr is the render of the mesh that
        # it created.
        self.mr = None # type: renpy.display.render.Render|None

        # The width and height of the child render.
        self.width = 0
        self.height = 0

        # The xsize and ysize the displayable should be scaled to.
        self.xsize = None # type: float|None
        self.ysize = None # type: float|None

        # The x and y offsets the child render will be placed at.
        self.xo = 0
        self.yo = 0

        # If true, the child will be clipped.
        self.clipping = False

        # The reverse transform.
        self.reverse = None # type: renpy.display.render.Matrix|None

    cdef make_mesh(self, cr):
        """
        Creates a mesh from the given render.

        Handles the mesh, mesh_pad, and blur properties.
        """

        # The render we're going to return.
        mr = Render(cr.width, cr.height)

        mesh = self.state.mesh
        blur = self.state.blur
        mesh_pad = self.state.mesh_pad

        if self.state.mesh_pad:

            if len(mesh_pad) == 4:
                pad_left, pad_top, pad_right, pad_bottom = mesh_pad
            else:
                pad_right, pad_bottom = mesh_pad
                pad_left = 0
                pad_top = 0

            padded = Render(cr.width + pad_left + pad_right, cr.height + pad_top + pad_bottom)
            padded.blit(cr, (pad_left, pad_top))

            cr = padded

        mr.blit(cr, (0, 0))

        mr.operation = renpy.display.render.FLATTEN
        mr.add_shader("renpy.texture")

        if isinstance(mesh, tuple):
            mesh_width, mesh_height = mesh

            mr.mesh = renpy.gl2.gl2mesh2.Mesh2.texture_grid_mesh(
                mesh_width, mesh_height,
                0.0, 0.0, cr.width, cr.height,
                0.0, 0.0, 1.0, 1.0)
        else:
            mr.mesh = True

        if blur is not None:
            mr.add_shader("-renpy.texture")
            mr.add_shader("renpy.blur")
            mr.add_uniform("u_renpy_blur_log2", math.log(blur, 2))

        self.mr = mr
        return mr

    cdef tile_and_pan(self):
        """
        This handles the xtile, ytile, xpan, and ypan properties.
        """

        cr = self.cr

        cwidth = cr.width
        cheight = cr.height

        # Tile the child to make it bigger.

        xtile = self.state.xtile
        ytile = self.state.ytile

        xpan = self.state.xpan
        ypan = self.state.ypan

        # Tiling.
        if (xtile != 1) or (ytile != 1):
            tcr = renpy.display.render.Render(cwidth * xtile, cheight * ytile)

            for i in range(xtile):
                for j in range(ytile):
                    tcr.blit(cr, (i * cwidth, j * cheight))

            cr = tcr

        # Panning.
        if (xpan is not None) or (ypan is not None):

            if xpan is not None:
                xpan = (xpan % 360) / 360.0
                pan_x = cwidth * xpan
                pan_w = cwidth
            else:
                pan_x = 0
                pan_w = cr.width

            if ypan is not None:
                ypan = (ypan % 360) / 360.0
                pan_y = cheight * ypan
                pan_h = cheight
            else:
                pan_y = 0
                pan_h = cr.height

            tcr = renpy.display.render.Render(pan_w, pan_h)

            for xpano in [ 0, cwidth ] if (xpan is not None) else [ 0 ]:
                for ypano in [ 0, cheight ] if (ypan is not None) else [ 0 ]:
                    tcr.subpixel_blit(cr, (xpano - pan_x, ypano - pan_y))

            tcr.xclipping = True
            tcr.yclipping = True

            cr = tcr

        self.cr = cr

    cdef cropping(self):
        """
        Handles cropping, crop_relative, and corner1/corner2.
        """

        cr = self.cr
        width = self.width
        height = self.height

        xo = 0
        yo = 0
        clipping = False

        crop = self.state.crop

        crop_relative = self.state.crop_relative

        if crop_relative is None:
            crop_relative = renpy.config.crop_relative_default

        if crop is not None:

            if crop_relative:
                x, y, w, h = crop

                x = relative(x, width, width)
                y = relative(y, height, height)
                w = relative(w, width, width - x)
                h = relative(h, height, height - y)

                crop = (x, y, w, h)

        if (self.state.corner1 is not None) and (crop is None) and (self.state.corner2 is not None):
            x1, y1 = self.state.corner1
            x2, y2 = self.state.corner2

            if crop_relative:
                x1 = relative(x1, width, width)
                y1 = relative(y1, height, height)
                x2 = relative(x2, width, width)
                y2 = relative(y2, height, height)

            if x1 > x2:
                x3 = x1
                x1 = x2
                x2 = x3

            if y1 > y2:
                y3 = y1
                y1 = y2
                y2 = y3

            crop = (x1, y1, x2-x1, y2-y1)

        if crop is not None:

            negative_xo, negative_yo, width, height = crop

            if self.state.rotate is not None:
                clipcr = Render(width, height)
                clipcr.subpixel_blit(cr, (-negative_xo, -negative_yo))
                clipcr.xclipping = True
                clipcr.yclipping = True
                cr = clipcr
            else:
                self.xo = -negative_xo
                self.yo = -negative_yo
                self.clipping = True

        self.cr = cr
        self.width = width
        self.height = height

    cdef render_child(self, st, at):
        """
        Renders the child.

        Handles the xsize and ysize properties.
        """

        state = self.state

        # Render the child.
        child = self.transform.child

        if child is None:
            child = renpy.display.transform.get_null()

        xsize = state.xsize
        ysize = state.ysize

        if xsize is not None:
            if (type(xsize) is float) and renpy.config.relative_transform_size:
                xsize *= self.widtho
            self.widtho = xsize

        if ysize is not None:
            if (type(ysize) is float) and renpy.config.relative_transform_size:
                ysize *= self.heighto
            self.heighto = ysize

        self.cr = render(child, self.widtho, self.heighto, st - self.transform.child_st_base, at)
        self.xsize = xsize
        self.ysize = ysize

    cdef size_zoom_rotate(self):
        """
        Handles size, zoom, and fit properties. Handles the rotate property
        of non-camera displayables.
        """

        cdef double cw
        cdef double ch
        cdef double width
        cdef double height
        cdef double sina
        cdef double angle
        cdef double cosa
        cdef double nh
        cdef double nw
        cdef double px
        cdef double py
        cdef double rxdx
        cdef double rxdy
        cdef double rydx
        cdef double rydy
        cdef double x2
        cdef double x3
        cdef double x4
        cdef double xo
        cdef double y2
        cdef double y3
        cdef double y4
        cdef double yo
        cdef double xzoom
        cdef double yzoom
        cdef double zoom

        xo = self.xo
        yo = self.yo

        width = self.width
        height = self.height

        state = self.state

        xsize = self.xsize
        ysize = self.ysize

        fit = self.state.fit

        # The reverse matrix used by the zoom and rotate properties.
        # (This can probably become a Matrix at some point.)
        rxdx = 1
        rxdy = 0
        rydx = 0
        rydy = 1

        # Size.
        if (width != 0) and (height != 0):
            maxsize = state.maxsize
            mul = None

            if (maxsize is not None):
                maxsizex, maxsizey = maxsize
                mul = min(maxsizex / width, maxsizey / height)

            scale = []
            if xsize is not None:
                scale.append(xsize / width)
            if ysize is not None:
                scale.append(ysize / height)

            if fit and not scale:
                scale = [ self.widtho / width, self.heighto / height]

            if fit is None:
                fit = 'fill'

            if scale:
                if fit == 'scale-up':
                    mul = max(1, *scale)
                elif fit == 'scale-down':
                    mul = min(1, *scale)
                elif fit == 'contain':
                    mul = min(scale)
                elif fit == 'cover':
                    mul = max(scale)
                else:
                    if xsize is None:
                        xsize = width
                    if ysize is None:
                        ysize = height

            if mul is not None:
                xsize = mul * width
                ysize = mul * height

            if (xsize is not None) and (ysize is not None) and ((xsize, ysize) != (width, height)):
                nw = xsize
                nh = ysize

                xzoom = 1.0 * nw / width
                yzoom = 1.0 * nh / height

                rxdx = xzoom
                rydy = yzoom

                xo *= xzoom
                yo *= yzoom

                width = xsize
                height = ysize

        # zoom
        zoom = state.zoom
        xzoom = zoom * <double> state.xzoom
        yzoom = zoom * <double> state.yzoom

        if xzoom != 1:

            rxdx *= xzoom

            if xzoom < 0:
                width *= -xzoom
            else:
                width *= xzoom

            xo *= xzoom
            # origin corrections for flipping
            if xzoom < 0:
                xo += width

        if yzoom != 1:

            rydy *= yzoom

            if yzoom < 0:
                height *= -yzoom
            else:
                height *= yzoom

            yo *= yzoom
            # origin corrections for flipping
            if yzoom < 0:
                yo += height

        # Rotation.
        rotate = state.rotate
        if (rotate is not None) and (not self.perspective):

            cw = width
            ch = height

            angle = rotate * 3.1415926535897931 / 180

            cosa = math.cos(angle)
            sina = math.sin(angle)

            # reverse = Matrix2D(xdx, xdy, ydx, ydy) * reverse

            # We know that at this point, rxdy and rydx are both 0, so
            # we can simplify these formulae a bit.
            rxdy = rydy * -sina
            rydx = rxdx * sina
            rxdx *= cosa
            rydy *= cosa

            # first corner point (changes with flipping)
            px = cw / 2.0
            if xzoom < 0:
                px = -px
            py = ch / 2.0
            if yzoom < 0:
                py = -py

            if state.rotate_pad:
                width = height = math.hypot(cw, ch)

                xo = -px * cosa + py * sina
                yo = -px * sina - py * cosa

            else:
                xo = -px * cosa + py * sina
                yo = -px * sina - py * cosa

                x2 = -px * cosa - py * sina
                y2 = -px * sina + py * cosa

                x3 =  px * cosa - py * sina
                y3 =  px * sina + py * cosa

                x4 =  px * cosa + py * sina
                y4 =  px * sina - py * cosa

                width = max(xo, x2, x3, x4) - min(xo, x2, x3, x4)
                height = max(yo, y2, y3, y4) - min(yo, y2, y3, y4)

            xo += width / 2.0
            yo += height / 2.0

        self.height = height
        self.width = width
        self.yo = yo
        self.xo = xo

        # Default case - no transformation matrix.
        if rxdx == 1 and rxdy == 0 and rydx == 0 and rydy == 1:
            self.reverse = IDENTITY
        else:
            self.reverse = Matrix2D(rxdx, rxdy, rydx, rydy)

    cdef camera_matrix_operations(self):
        """
        Handles the poi, orientation, rotate, and zpos properties
        of cameras.
        """

        cdef Matrix m

        z11 = self.perspective[1]

        state = self.state

        width = self.width
        height = self.height

        if state.point_to is not None:
            poi = get_poi(state)
        else:
            poi = None

        orientation = state.orientation
        if orientation:
            xorientation, yorientation, zorientation = orientation

        xyz_rotate = False
        if state.xrotate or state.yrotate or state.zrotate:
            xyz_rotate = True
            xrotate = state.xrotate or 0
            yrotate = state.yrotate or 0
            zrotate = state.zrotate or 0

        placement = (state.xpos, state.ypos, state.xanchor, state.yanchor, state.xoffset, state.yoffset, True)
        xplacement, yplacement = renpy.display.core.place(width, height, width, height, placement)

        if poi:
            start_pos = (xplacement + width / 2, yplacement + height / 2, state.zpos + z11)
            a, b, c = ( float(e - s) for s, e in zip(start_pos, poi) )

            #cameras is rotated in z, y, x order.
            #It is because rotating stage in x, y, z order means rotating a camera in z, y, x order.
            #rotating around z axis isn't rotating around the center of the screen when rotating camera in x, y, z order.
            v_len = math.sqrt(a**2 + b**2 + c**2) # math.hypot is better in py3.8+
            if v_len == 0:
                xpoi = ypoi = zpoi = 0
            else:
                a /= v_len
                b /= v_len
                c /= v_len

                sin_ypoi = min(1., max(-a, -1.))
                ypoi = math.asin(sin_ypoi)
                if c == 0:
                    if abs(a) == 1:
                        xpoi = 0
                    else:
                        sin_xpoi = min(1., max(b / math.cos(ypoi), -1.))
                        xpoi = math.asin(sin_xpoi)
                else:
                    xpoi = math.atan(-b/c)

                if c > 0:
                    ypoi = math.pi - ypoi

                if xpoi != 0.0 and ypoi != 0.0:
                    if xpoi == math.pi / 2 or xpoi == - math.pi / 2:
                        if -math.sin(xpoi) * math.sin(ypoi) > 0.0:
                            zpoi = math.pi / 2
                        else:
                            zpoi = - math.pi / 2
                    else:
                        zpoi = math.atan(-(math.sin(xpoi) * math.sin(ypoi)) / math.cos(xpoi))
                else:
                    zpoi = 0

                xpoi = math.degrees(xpoi)
                ypoi = math.degrees(ypoi)
                zpoi = math.degrees(zpoi)

        if poi or orientation or xyz_rotate:
            m = Matrix.offset(-width / 2, -height / 2, -z11)

        if poi:
            m = Matrix.rotate(-xpoi, -ypoi, -zpoi) * m

        if orientation:
            m = Matrix.rotate(-xorientation, -yorientation, -zorientation) * m

        if xyz_rotate:
            m = Matrix.rotate(-xrotate, -yrotate, -zrotate) * m

        if poi or orientation or xyz_rotate:
            m = Matrix.offset(width / 2, height / 2, z11) * m

            self.reverse = m * self.reverse

        if xplacement or yplacement or state.zpos:
            self.reverse = Matrix.offset(-xplacement, -yplacement, -state.zpos) * self.reverse

        if state.rotate is not None:
            m = Matrix.offset(-width / 2, -height / 2, 0.0)
            m = Matrix.rotate(0, 0, -state.rotate) * m
            m = Matrix.offset(width / 2, height / 2, 0.0) * m

            self.reverse = m * self.reverse

    cdef matrix_operations(self):
        """
        Handles the poi, orientation, x/y/z/rotate, and zpos properties
        of non-cameras. (Rotate is handled above.)
        """

        cdef Matrix m

        state = self.state

        width = self.width
        height = self.height

        if state.point_to is not None:
            poi = get_poi(state)
        else:
            poi = None

        orientation = state.orientation
        if orientation:
            xorientation, yorientation, zorientation = orientation

        xyz_rotate = False
        if state.xrotate or state.yrotate or state.zrotate:
            xyz_rotate = True
            xrotate = state.xrotate or 0
            yrotate = state.yrotate or 0
            zrotate = state.zrotate or 0

        if poi or orientation or xyz_rotate:
            if state.matrixanchor is None:

                manchorx = width / 2.0
                manchory = height / 2.0

            else:
                manchorx, manchory = state.matrixanchor

                if type(manchorx) is float:
                    manchorx *= width
                if type(manchory) is float:
                    manchory *= height

            m = Matrix.offset(-manchorx, -manchory, 0.0)

        if poi:
            placement = self.transform.get_placement()
            xplacement, yplacement = renpy.display.core.place(self.widtho, self.heighto, width, height, placement)
            start_pos = (xplacement + manchorx, yplacement + manchory, state.zpos)

            a, b, c = ( float(e - s) for s, e in zip(start_pos, poi) )
            v_len = math.sqrt(a**2 + b**2 + c**2) # math.hypot is better in py3.8+
            if v_len == 0:
                xpoi = ypoi = 0
            else:
                a /= v_len
                b /= v_len
                c /= v_len

                sin_xpoi = min(1., max(-b, -1.))
                xpoi = math.asin(sin_xpoi)
                if c == 0:
                    if abs(b) == 1:
                        ypoi = 0
                    else:
                        sin_ypoi = min(1., max(a / math.cos(xpoi), -1.))
                        ypoi = math.asin(sin_ypoi)
                else:
                    ypoi = math.atan(a/c)

                if c < 0:
                    ypoi += math.pi

                xpoi = math.degrees(xpoi)
                ypoi = math.degrees(ypoi)

        if poi:
            m = Matrix.rotate(xpoi, ypoi, 0) * m
        if orientation:
            m = Matrix.rotate(xorientation, yorientation, zorientation) * m
        if xyz_rotate:
            m = Matrix.rotate(xrotate, yrotate, zrotate) * m

        if poi or orientation or xyz_rotate:
            m = Matrix.offset(manchorx, manchory, 0.0) * m

            self.reverse = m * self.reverse

        if state.zpos:
            self.reverse = Matrix.offset(0, 0, state.zpos) * self.reverse

    cdef matrix_transform(self):
        """
        Handles the matrixtransform and matrixanchor properties.
        """

        cdef Matrix m, mt

        state = self.state

        mt = state.matrixtransform

        if mt is not None:

            if callable(mt):
                mt = mt(None, 1.0)

            if not isinstance(mt, renpy.display.matrix.Matrix):
                raise Exception("matrixtransform requires a Matrix (got %r)" % (mt,))

            if state.matrixanchor is None:

                manchorx = self.width / 2.0
                manchory = self.height / 2.0

            else:
                manchorx, manchory = state.matrixanchor

                if type(manchorx) is float:
                    manchorx *= self.width
                if type(manchory) is float:
                    manchory *= self.height

            m = Matrix.offset(-manchorx, -manchory, 0.0)
            m = mt * m
            m = Matrix.offset(manchorx, manchory, 0.0) * m

            self.reverse = m * self.reverse

    cdef zzoom(self):
        """
        Handles the zzoom property.
        """

        cdef Matrix m

        state = self.state
        width = self.width
        height = self.height

        if state.zzoom and z11:
            zzoom = (z11 - state.zpos) / z11

            m = Matrix.offset(-width / 2, -height / 2, 0.0)
            m = Matrix.scale(zzoom, zzoom, 1) * m
            m = Matrix.offset(width / 2, height / 2, 0.0) * m

            self.reverse = m * self.reverse

    cdef final_render(self, rv):
        """
        Apply properties to the final render:

        * matrixcolor
        * nearest
        * blend
        * alpha
        * additive
        * shader
        * uniforms
        * gl properties
        """

        state = self.state

        # Matrixcolor.
        if state.matrixcolor:
            matrix = state.matrixcolor

            if callable(matrix):
                matrix = matrix(None, 1.0)

            if not isinstance(matrix, renpy.display.matrix.Matrix):
                raise Exception("matrixcolor requires a Matrix (not im.matrix, got %r)" % (matrix,))

            rv.add_shader("renpy.matrixcolor")
            rv.add_uniform("u_renpy_matrixcolor", matrix)

        # Nearest neighbor.
        rv.nearest = state.nearest

        if state.nearest:
            rv.add_property("texture_scaling", "nearest")

        if state.blend:
            rv.add_property("blend_func", renpy.config.gl_blend_func[state.blend])

        # Alpha.
        alpha = state.alpha

        if alpha < 0.0:
            alpha = 0.0
        elif alpha > 1.0:
            alpha = 1.0

        rv.alpha = alpha
        rv.over = 1.0 - state.additive

        if (rv.alpha != 1.0) or (rv.over != 1.0):
            rv.add_shader("renpy.alpha")
            rv.add_uniform("u_renpy_alpha", rv.alpha)
            rv.add_uniform("u_renpy_over", rv.over)

        # Shaders and uniforms.
        if state.shader is not None:

            if isinstance(state.shader, basestring):
                rv.add_shader(state.shader)
            else:
                for name in state.shader:
                    rv.add_shader(name)

        for name in renpy.display.transform.uniforms:
            value = getattr(state, name, None)

            if value is not None:
                rv.add_uniform(name, value)

        for name in renpy.display.transform.gl_properties:
            value = getattr(state, name, None)

            if value is not None:
                if self.mr:
                    self.mr.add_property(name[3:], value)
                else:
                    rv.add_property(name[3:], value)

    def render(self, widtho, heighto, st, at):

        global z11

        self.widtho = widtho
        self.heighto = heighto

        self.state.available_width = widtho
        self.state.available_height = heighto

        transform = self.transform
        state = self.state

        # Figure out the perspective.
        perspective = state.perspective

        if perspective is True:
            perspective = renpy.config.perspective
        elif perspective is False:
            perspective = None
        elif isinstance(perspective, (int, float)):
            perspective = (renpy.config.perspective[0], perspective, renpy.config.perspective[2])

        self.perspective = perspective

        # Set the z11 distance, so it can be used elsewhere.
        old_z11 = z11

        if perspective:
            z11 = perspective[1]

        # Actually render the child.
        self.render_child(st, at)

        # Reset the z11 distance.
        z11 = old_z11

        # Tiling and panning.
        self.tile_and_pan()

        mesh = state.mesh or (True if state.blur else None)

        if mesh and not perspective:
            self.cr = self.make_mesh(self.cr)

        # The width and height of the child.
        self.width = self.cr.width
        self.height = self.cr.height

        transform.child_size = self.width, self.height

        # Cropping.
        self.cropping()

        # Size, zoom, and rotate.
        self.size_zoom_rotate()

        # Other matrix transformations.
        if perspective:
            self.camera_matrix_operations()
        else:
            self.matrix_operations()

        self.matrix_transform()

        self.zzoom()

        # The final render. (Unless we mesh it.)
        rv = Render(self.width, self.height)

        # perspective
        if perspective:
            near, z_one_one, far = perspective
            self.reverse = Matrix.perspective(self.width, self.height, near, z_one_one, far) * self.reverse

        # Apply the matrices to the transform.
        transform.reverse = self.reverse

        if transform.reverse is not IDENTITY:
            rv.reverse = transform.reverse
            transform.forward = rv.forward = transform.reverse.inverse()
        else:
            transform.forward = IDENTITY

        pos = (self.xo, self.yo)

        if state.subpixel:
            rv.subpixel_blit(self.cr, pos)
        else:
            rv.blit(self.cr, pos)

        if mesh and perspective:
            rv = self.make_mesh(rv)

        self.final_render(rv)

        # Clipping.
        rv.xclipping = self.clipping
        rv.yclipping = self.clipping

        transform.offsets = [ pos ]
        transform.render_size = (self.width, self.height)

        return rv
