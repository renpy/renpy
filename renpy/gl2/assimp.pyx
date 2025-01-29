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

from assimpapi cimport (
    Importer, aiProcessPreset_TargetRealtime_Quality, aiProcess_ConvertToLeftHanded, aiProcess_FlipUVs, aiScene,
    aiMesh, aiMatrix4x4, aiPrimitiveType_TRIANGLE, aiFace, aiNode, aiTexture,
    aiTextureType,

    aiTextureType_NONE,
    aiTextureType_DIFFUSE,
    aiTextureType_SPECULAR,
    aiTextureType_AMBIENT,
    aiTextureType_EMISSIVE,
    aiTextureType_HEIGHT,
    aiTextureType_NORMALS,
    aiTextureType_SHININESS,
    aiTextureType_OPACITY,
    aiTextureType_DISPLACEMENT,
    aiTextureType_LIGHTMAP,
    aiTextureType_REFLECTION,
    aiTextureType_BASE_COLOR,
    aiTextureType_NORMAL_CAMERA,
    aiTextureType_EMISSION_COLOR,
    aiTextureType_METALNESS,
    aiTextureType_DIFFUSE_ROUGHNESS,
    aiTextureType_AMBIENT_OCCLUSION,
    aiTextureType_UNKNOWN,
    aiTextureType_SHEEN,
    aiTextureType_CLEARCOAT,
    aiTextureType_TRANSMISSION,


    aiString, aiMaterial
)

from typing import Callable, Iterable

import renpy

from renpy.display.displayable import Displayable
from renpy.display.matrix import Matrix
from renpy.display.render import IDENTITY, Render
from renpy.display.im import Data, unoptimized_texture, render_for_texture
from renpy.gl2.gl2mesh3 cimport Mesh3, Point3
from renpy.gl2.gl2model import GL2Model

# A map from texture types to the corresponding assimp constants.
TEXTURE_TYPES = {
    "none": aiTextureType_NONE,
    "diffuse": aiTextureType_DIFFUSE,
    "specular": aiTextureType_SPECULAR,
    "ambient": aiTextureType_AMBIENT,
    "emissive": aiTextureType_EMISSIVE,
    "height": aiTextureType_HEIGHT,
    "normals": aiTextureType_NORMALS,
    "shininess": aiTextureType_SHININESS,
    "opacity": aiTextureType_OPACITY,
    "displacement": aiTextureType_DISPLACEMENT,
    "lightmap": aiTextureType_LIGHTMAP,
    "reflection": aiTextureType_REFLECTION,
    "base_color": aiTextureType_BASE_COLOR,
    "normal_camera": aiTextureType_NORMAL_CAMERA,
    "emission_color": aiTextureType_EMISSION_COLOR,
    "metalness": aiTextureType_METALNESS,
    "diffuse_roughness": aiTextureType_DIFFUSE_ROUGHNESS,
    "ambient_occlusion": aiTextureType_AMBIENT_OCCLUSION,
    "unknown": aiTextureType_UNKNOWN,
    "sheen": aiTextureType_SHEEN,
    "clearcoat": aiTextureType_CLEARCOAT,
    "transmission": aiTextureType_TRANSMISSION,
}


class ModelData:
    """
    Represents the information about a model after it's been loaded.
    """

    embedded_textures: dict[str, Data]
    "The embedded textures in the model."

    mesh_renders : list[Render]
    "The renders that make up the model."

    def __init__(self):
        self.embedded_textures = { }
        self.mesh_renders = [ ]


cache : dict[str, ModelData] = { }
"Caches the models that have been loaded."


def get_renders():
    for i in cache.values():
        for j in i.mesh_renders:
            yield j

def free_memory():
    cache.clear()


class MeshInfo:
    """
    This stores information that's passed into the mesh callback.
    """

    _importer: "AssetImporter"
    "The importer that's loading the mesh."

    _material_index: int
    "The index of the material."

    mesh: Mesh3
    "The mesh that's being loaded."

    reverse_matrix: Matrix
    forward_matrix: Matrix

    def has_texture(self, texture_type: str) -> bool:
        """
        Returns True if the mesh has a texture of the given type.
        """

        if texture_type not in TEXTURE_TYPES:
            raise Exception(f"Unknown texture type {texture_type}.")

        return self._importer.get_texture(self._material_index, TEXTURE_TYPES[texture_type]) is not None


    def get_texture(self, texture_type: str) -> renpy.display.displayable.Displayable:
        """
        Returns the texture of the given type.
        """

        if texture_type not in TEXTURE_TYPES:
            raise Exception(f"Unknown texture type {texture_type}.")

        path = self._importer.get_texture(self._material_index, TEXTURE_TYPES[texture_type])

        if path is None:
            rv = renpy.display.im.Null()

        elif path.startswith("*"):
            rv = self._importer.model_data.embedded_textures[path]

        else:
            rv = renpy.easy.displayable(self._importer.dirname + "/" + path)

        return renpy.display.im.render_for_texture(unoptimized_texture(rv), 0, 0, 0, 0)

    def wrap_texture(self, d):
        """
        Wraps an image file so it can be used as a texture.
        """

        d = renpy.easy.displayable(d)
        return renpy.display.im.render_for_texture(unoptimized_texture(d), 0, 0, 0, 0)


MeshCallbackType = Callable[[MeshInfo], Render]


class MeshCallback:
    """
    A callback that's called for each mesh in the model.
    """

    textures: tuple[str]
    "The textures that the callback is interested in."

    shaders: tuple[str]
    "The shaders that the callback is interested in."

    def __init__(self, textures=( "diffuse", ), shaders=()):
        self.textures = textures
        self.shaders = shaders


    def __call__(self, mesh: MeshInfo) -> None:
        """
        Called for each mesh in the model.
        """

        rv = renpy.display.render.Render(0, 0)
        rv.mesh = mesh.mesh
        rv.reverse = mesh.reverse_matrix
        rv.forward = mesh.forward_matrix

        rv.add_property("texture_wrap", (renpy.uguu.GL_REPEAT, renpy.uguu.GL_REPEAT))

        for i in self.shaders:
            rv.add_shader(i)

        for i in self.textures:
            rv.blit(mesh.get_texture(i), (0, 0))

        return rv



cdef class Loader:

    cdef public str dirname
    "The directory that the asset was loaded from."

    cdef Importer importer
    "The importer used to load the models."

    cdef const aiScene *scene
    "The scene that has been loaded."

    cdef public object model_data
    "The ModelData object that is being filled in."

    cdef public object mesh_callback
    "The callback that is called for each mesh."

    def load(self, filename: str, mesh_callback) -> None:

        self.mesh_callback = mesh_callback
        self.dirname = filename.rpartition("/")[0]

        full_filename = renpy.config.gamedir + "/" + filename

        # Load the scene.
        filename_bytes = full_filename.encode()
        self.scene = self.importer.ReadFile(
            filename_bytes,
            aiProcessPreset_TargetRealtime_Quality | aiProcess_FlipUVs)

        if not self.scene:
            raise Exception("Error loading %s: %s" % (filename, self.importer.GetErrorString()))

        try:

            self.model_data = ModelData()
            cache[filename] = self.model_data

            self.load_textures()

            # Load the nodes.
            flip_y = Matrix((
                1.0, 0.0,
                0.0, -1.0))

            self.load_node(self.scene.mRootNode, flip_y)

        finally:
            self.model_data = None
            self.mesh_callback = None


    def load_textures(self) -> None:
        """
        Loads the textures from the scene.
        """

        cdef aiTexture *texture
        cdef char *texbytes

        for i in range(self.scene.mNumTextures):
            texture = self.scene.mTextures[i]

            key = f"*{i}"
            format = texture.achFormatHint.decode()

            if texture.mHeight == 0:
                texbytes = <char *>texture.pcData
                data = texbytes[:texture.mWidth]

                filename = key + "." + format

                self.model_data.embedded_textures[key] = unoptimized_texture(Data(data, filename))

            else:
                raise Exception(f"{format} textures are not (yet) supported.")

    def get_texture(self, material_index : int, texture_type : int) -> str|None:
        """
        Given a material index and a texture type, returns the path to the texture. This
        may also be *0 (etc) for embedded textures.
        """

        cdef aiString path
        cdef aiMaterial *material = self.scene.mMaterials[material_index]

        if material.GetTextureCount(texture_type) == 0:
            return None

        material.GetTexture(texture_type, 0, &path)

        return path.data[:path.length].decode()


    cdef load_node(self, aiNode *node, matrix : Matrix):
        cdef unsigned int i

        node_matrix = Matrix((
            node.mTransformation.a1, node.mTransformation.b1, node.mTransformation.c1, node.mTransformation.d1,
            node.mTransformation.a2, node.mTransformation.b2, node.mTransformation.c2, node.mTransformation.d2,
            node.mTransformation.a3, node.mTransformation.b3, node.mTransformation.c3, node.mTransformation.d3,
            node.mTransformation.a4, node.mTransformation.b4, node.mTransformation.c4, node.mTransformation.d4)
            )

        matrix = node_matrix * matrix

        for i in range(node.mNumMeshes):
            self.load_mesh(node.mMeshes[i], matrix)

        for i in range(node.mNumChildren):
            self.load_node(node.mChildren[i], matrix)


    def load_mesh(self, mesh_index: int, matrix: Matrix) -> Render:
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

        info = MeshInfo()
        info._importer = self
        info._material_index = mesh.mMaterialIndex
        info.mesh = m
        info.reverse_matrix = matrix
        info.forward_matrix = matrix.inverse()

        r = self.mesh_callback(info)

        if r is not None:
            self.model_data.mesh_renders.append(r)

loader = Loader()
"The loader used to load in imported models."

class AssimpModel(renpy.display.displayable.Displayable):
    """
    A displayable that displays a model.
    """

    filename: str
    "The filename of the model to display."

    def __init__(
        self,
        filename: str,
        callback: MeshCallbackType|None = None,
        textures: Iterable[str] = ("diffuse",),
        shader: str|tuple[str] = "renpy.texture"):

        super().__init__()

        if isinstance(shader, str):
            shaders = (shader, )
        else:
            shaders = shader

        if callback is None:
            callback = MeshCallback(textures=textures, shaders=shaders)

        self.filename = filename
        self.callback = callback

    def render(self, width, height, st, at):

        if self.filename not in cache:
            loader.load(self.filename, self.callback)

        model_data = cache[self.filename]

        rv = Render(0, 0)

        for cr in model_data.mesh_renders:
            rv.blit(cr, (0, 0), focus=False, main=False)

        rv.add_property("depth", True)

        return rv
