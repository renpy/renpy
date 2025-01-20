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
    aiMesh, aiMatrix4x4, aiPrimitiveType_TRIANGLE, aiFace, aiNode
)

import renpy

from renpy.display.displayable import Displayable
from renpy.display.matrix import Matrix
from renpy.display.render import IDENTITY, Render
from renpy.gl2.gl2mesh3 cimport Mesh3, Point3
from renpy.gl2.gl2model import GL2Model



class ModelData:
    """
    Represents the information about a model after it's been loaded.
    """

    mesh_renders : list[Render]
    "The renders that make up the model."

    def __init__(self):
        self.mesh_renders = [ ]


cache : dict[str, ModelData] = { }
"Caches the models that have been loaded."

cdef class Loader:

    cdef Importer importer
    cdef const aiScene *scene

    def load(self, filename: str) -> None:
        cdef const aiScene *scene

        filename_bytes = filename.encode()
        self.scene = self.importer.ReadFile(
            filename_bytes,
            aiProcessPreset_TargetRealtime_Quality)

        if not self.scene:
            raise Exception("Error loading %s: %s" % (filename, self.importer.GetErrorString()))

        model_data = ModelData()

        flip_y = Matrix((
            1.0, 0.0,
            0.0, -1.0))

        self.load_node(model_data, self.scene.mRootNode, flip_y)

        cache[filename] = model_data

    cdef load_node(self, model_data: ModelData, aiNode *node, matrix : Matrix):
        cdef unsigned int i

        matrix = Matrix((
            node.mTransformation.a1, node.mTransformation.a2, node.mTransformation.a3, node.mTransformation.a4,
            node.mTransformation.b1, node.mTransformation.b2, node.mTransformation.b3, node.mTransformation.b4,
            node.mTransformation.c1, node.mTransformation.c2, node.mTransformation.c3, node.mTransformation.c4,
            node.mTransformation.d1, node.mTransformation.d2, node.mTransformation.d3, node.mTransformation.d4)
            ) * matrix

        for i in range(node.mNumMeshes):
            self.load_mesh(model_data, node.mMeshes[i], matrix)

        for i in range(node.mNumChildren):
            self.load_node(model_data, node.mChildren[i], matrix)

    def load_mesh(self, model_data: ModelData, mesh_index: int, matrix: Matrix) -> Render:
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

        r = Render(0, 0)
        r.mesh = m
        r.reverse = matrix
        r.forward = matrix.inverse()

        model_data.mesh_renders.append(r)

loader = Loader()
"The loader used to load in imported models."


class ModelDisplayable(renpy.display.displayable.Displayable):
    """
    A displayable that displays a model.
    """

    filename: str
    "The filename of the model to display."

    shaders: tuple[str]
    "The shaders to use to display the model."

    def __init__(self, filename: str, shaders: tuple[str]):
        super().__init__()

        self.filename = filename
        self.shaders = shaders

    def render(self, width, height, st, at):

        if self.filename not in cache:
            loader.load(self.filename)

        model_data = cache[self.filename]

        rv = Render(0, 0)

        for cr in model_data.mesh_renders:
            rv.blit(cr, (0, 0), focus=False, main=False)

        for i in self.shaders:
            rv.add_shader(i)

        rv.add_property("depth", True)

        return rv
