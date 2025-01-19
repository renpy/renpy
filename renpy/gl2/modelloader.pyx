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
    aiMesh, aiMatrix4x4, aiPrimitiveType_TRIANGLE, aiFace
)

from renpy.gl2.gl2mesh3 cimport Mesh3, Point3
from renpy.gl2.gl2model import GL2Model

import renpy


cdef class Loader:

    cdef Importer importer
    cdef const aiScene *scene

    def load(self, filename: str) -> None:
        cdef const aiScene *scene

        filename_bytes = filename.encode()
        self.scene = self.importer.ReadFile(
            filename_bytes,
            aiProcessPreset_TargetRealtime_Quality |
            aiProcess_ConvertToLeftHanded |
            aiProcess_FlipUVs)

        if not self.scene:
            raise Exception("Error loading %s: %s" % (filename, self.importer.GetErrorString()))


    def load_mesh(self, mesh_index: int, shaders : tuple[str]) -> GL2Model:
        """
        Loads the mesh with index `mesh_index` from the scene.
        """

        if mesh_index < 0 or mesh_index >= self.scene.mNumMeshes:
            raise Exception("Invalid mesh index %d." % mesh_index)

        cdef aiMesh *mesh = self.scene.mMeshes[mesh_index]

        if mesh.mPrimitiveTypes != aiPrimitiveType_TRIANGLE:
            raise Exception("Mesh %d is not a triangle mesh." % mesh_index)

        layout = renpy.gl2.gl2mesh.MODEL_N_LAYOUT
        cdef int stride = layout.stride

        cdef Mesh3 m = Mesh3(renpy.gl2.gl2mesh.MODEL_N_LAYOUT, mesh.mNumVertices, mesh.mNumFaces)
        m.points = mesh.mNumVertices
        m.triangles = mesh.mNumFaces

        cdef Point3 *point = m.point
        cdef float *attribute = m.attribute

        cdef unsigned int i

        for i in range(mesh.mNumVertices):
            point[i].x = mesh.mVertices[i].x
            point[i].y = mesh.mVertices[i].y
            point[i].z = mesh.mVertices[i].z

            miny = min(miny, point[i].y)
            maxy = max(maxy, point[i].y)

            # a_tex_coord
            if mesh.mTextureCoords[0]:
                attribute[0] = mesh.mTextureCoords[0][i].x
                attribute[1] = mesh.mTextureCoords[0][i].y

            # a_normal
            if mesh.mNormals:
                attribute[2] = mesh.mNormals[i].x
                attribute[3] = mesh.mNormals[i].y
                attribute[4] = mesh.mNormals[i].z

            attribute += stride

        cdef unsigned int *triangle = m.triangle

        for i in range(mesh.mNumFaces):
            triangle[0] = mesh.mFaces[i].mIndices[0]
            triangle[1] = mesh.mFaces[i].mIndices[1]
            triangle[2] = mesh.mFaces[i].mIndices[2]

            triangle += 3

        return GL2Model((0, 0), m, shaders, {}, { "depth" : True })
