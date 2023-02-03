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

# This contains wrappers for the various Transform classes. It uses some
# of the classes in 00matrixcolor.rpy.

init -1400 python:


    class TransformMatrix(_BaseMatrix):
        """
        :undocumented:
        """

        function = None
        nargs = 0


        def __init__(self, *args):
            if len(args) != self.nargs:
                raise Exception("{} takes {} arguments, {} given.".format(type(self).__name__, self.nargs, len(args)))

            self.args = args


        def __call__(self, other, done):

            if type(other) is not type(self):
                return self.function(*self.args)
            else:
                args = tuple(a + (b - a) * done for a, b in zip(other.args, self.args))
                return self.function(*args)

        @staticmethod
        def _document(function):
            if not function:
                return ":undocumented:"

            rv = function.__doc__

            rv = rv.replace(":doc: matrix", ":doc: transform_matrix")
            rv = rv.replace("Returns", "A TransformMatrix that returns")

            return rv


    class OffsetMatrix(TransformMatrix, DictEquality):
        nargs = 3
        function = Matrix.offset
        __doc__ = TransformMatrix._document(Matrix.offset)

    class RotateMatrix(TransformMatrix, DictEquality):
        nargs = 3
        function = Matrix.rotate
        __doc__ = TransformMatrix._document(Matrix.rotate)

    class ScaleMatrix(TransformMatrix, DictEquality):
        nargs = 3
        function = Matrix.scale
        __doc__ = TransformMatrix._document(Matrix.scale)
