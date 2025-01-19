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

from assimp cimport (
    Importer, aiProcessPreset_TargetRealtime_Quality, aiProcess_ConvertToLeftHanded, aiProcess_FlipUVs, aiScene,
    aiMesh, aiMatrix4x4
)

cdef class Loader:

    cdef Importer importer
    cdef const aiScene *scene

    def load(self, filename: str) -> None:
        cdef const aiScene *scene

        filename_bytes = filename.encode()
        self.scene = self.importer.ReadFile(filename_bytes, aiProcessPreset_TargetRealtime_Quality | aiProcess_ConvertToLeftHanded | aiProcess_FlipUVs) # type: ignore

        if not self.scene:
            raise Exception("Error loading %s: %s" % (filename, self.importer.GetErrorString()))
