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


import threading

from typing import Iterable

from pygame_sdl2 cimport *
import_pygame_sdl2()

from assimpapi cimport (
    Importer, aiProcessPreset_TargetRealtime_Quality, aiProcess_ConvertToLeftHanded, aiProcess_FlipUVs, aiScene,
    aiMesh, aiMatrix4x4, aiPrimitiveType_TRIANGLE, aiFace, aiNode, aiTexture,
    aiTextureType, IOSystem,

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

cdef extern from "assimpio.h":
    cdef cppclass RenpyIOSystem(IOSystem):
        RenpyIOSystem()
        pass


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

    mesh_info: dict[str, MeshInfo]
    "Information required to blit each mesh in the model."

    def __init__(self):
        self.embedded_textures = { }
        self.mesh_info = [ ]


    def duplicate(self):
        """
        Duplicates the model data.
        """

        rv = ModelData()
        rv.embedded_textures = self.embedded_textures.copy()
        rv.mesh_info = [ mi.duplicate() for mi in self.mesh_info ]

        return rv


cache: dict[AssimpModel, ModelData] = { }
"Caches the models that have been loaded."

predicted: set[AssimpModel]|None = None
"The set of models that are predicted to be loaded."

new_predicted: set[AssimpModel] = set()
"The same, but before finish_predict() is called."


def free_memory():
    cache.clear()


class MeshInfo:
    """
    This stores the information used to blit a texture.
    """

    mesh: Mesh3
    "The mesh that's being loaded."

    reverse_matrix: Matrix
    forward_matrix: Matrix

    textures: list
    """
    A list of displaybles to render and blit as textures.
    """

    shaders: Iterable[str]
    """
    The shaders to use.
    """

    def __init__(self, Loader loader, Mesh3 mesh, reverse_matrix: Matrix, forward_matrix: Matrix,  int material_index, textures: Iterable[str], shaders: Iterable[str]):

        self.mesh = mesh
        self.reverse_matrix = reverse_matrix
        self.forward_matrix = forward_matrix

        self.textures = [ ]

        for t in textures:

            if isinstance(t, str) and t in TEXTURE_TYPES:

                path = loader.get_texture(material_index, TEXTURE_TYPES[t])

                if path is None:
                    d = renpy.display.im.Null()

                elif path.startswith("*"):
                    d = loader.model_data.embedded_textures[path]

                else:
                    d = renpy.easy.displayable(loader.dirname + "/" + path)

            else:

                d = t

            self.textures.append(unoptimized_texture(d))

        self.shaders = shaders

    def duplicate(self):
        """
        Duplicates the mesh info.
        """

        rv = MeshInfo.__new__(MeshInfo)
        rv.mesh = self.mesh
        rv.reverse_matrix = self.reverse_matrix
        rv.forward_matrix = self.forward_matrix
        rv.shaders = self.shaders

        rv.textures = [ ]

        for d in self.textures:
            if d._duplicatable:
                rv.textures.append(d._duplicate())
            else:
                rv.textures.append(d)

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

    cdef public bint tangents
    "True if tangents should be included in the mesh."

    cdef public object textures
    "A list of names of shaders to use."

    cdef public object shaders
    "A shader or list of shaders to use."

    def __cinit__(self):
        self.importer.SetIOHandler(new RenpyIOSystem())

    def load(
        self,
        model_data: ModelData,
        filename: str,
        textures: Iterable[str],
        shaders: Iterable[str|renpy.display.displayable.Displayable],
        tangents: bool,
        zoom: float,
        flip_x: bool,
        flip_y: bool,
        flip_z: bool,
        flip_uv: bool,) -> None:

        self.shaders = shaders
        self.textures = textures
        self.tangents = tangents

        self.dirname = filename.rpartition("/")[0]

        # Load the scene.
        filename_bytes = filename.encode()
        self.scene = self.importer.ReadFile(
            filename_bytes,
            aiProcessPreset_TargetRealtime_Quality | (aiProcess_FlipUVs if flip_uv else 0))

        if not self.scene:
            raise Exception("Error loading %s: %s" % (filename, self.importer.GetErrorString()))

        try:

            self.model_data = model_data

            self.load_textures()

            xdx = -1.0 if flip_x else 1.0
            ydy = -1.0 if flip_y else 1.0
            zdz = -1.0 if flip_z else 1.0

            # Load the nodes.
            m = Matrix.scale(xdx, ydy, zdz) * Matrix.scale(zoom, zoom, zoom)

            self.load_node(self.scene.mRootNode, m)

            return self.model_data

        finally:
            self.shaders = [ ]
            self.textures = [ ]
            self.model_data = None

            self.importer.FreeScene()


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

        if self.tangents:
            layout = renpy.gl2.gl2mesh.MODEL_NT_LAYOUT
        else:
            layout = renpy.gl2.gl2mesh.MODEL_N_LAYOUT
        cdef int stride = layout.stride

        cdef Mesh3 m = Mesh3(layout, mesh.mNumVertices, mesh.mNumFaces)
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

            if self.tangents:
                # a_tangent
                if mesh.mTangents:
                    attribute[5] = mesh.mTangents[i].x
                    attribute[6] = mesh.mTangents[i].y
                    attribute[7] = mesh.mTangents[i].z

                # a_bitangent
                if mesh.mBitangents:
                    attribute[8] = mesh.mBitangents[i].x
                    attribute[9] = mesh.mBitangents[i].y
                    attribute[10] = mesh.mBitangents[i].z

            attribute += stride

        cdef unsigned int *triangle = m.triangle

        for i in range(mesh.mNumFaces):
            triangle[0] = mesh.mFaces[i].mIndices[0]
            triangle[1] = mesh.mFaces[i].mIndices[1]
            triangle[2] = mesh.mFaces[i].mIndices[2]

            triangle += 3

        info = MeshInfo(
            self,
            m,
            matrix,
            matrix.inverse(),
            mesh.mMaterialIndex,
            self.textures,
            self.shaders)

        self.model_data.mesh_info.append(info)

loader = Loader()
"The loader used to load in imported models."

loader_lock = threading.Lock()
"The lock used to protect the loader."

class GLTFModel(renpy.display.displayable.Displayable):
    """
    :doc: assimp

    A displayable that loads a 3D Model in the GLTF format. This format is supported by many 3D tools. Ren'Py
    uses the `Open Asset Importer (assimp) library <https://github.com/assimp/assimp>`_ to load GLTF models.

    For the purposes of Ren'Py's 2D layout system, a GLTFModel has zero width and height. By default, the model
    is loaded at the size found in the file that contains it. If required, the `zoom` may be used to scale it.

    When multiple models are in use, the ``gl_depth True`` property should be supplied to the camera, so that
    depth testing is enabled. Ren'Py does not currently perform any culling of the model, so it's
    important to use models simple enough to be completely rendered.

    `filename`
        The filename of the model to display.

    `textures`
        A list of textures to load. These textures will be loaded into texture slots - the first will be tex0, the
        second tex1, and so on.

        The list may contain one of the following strings, giving the type of texture to load:

        * "none"
        * "diffuse"
        * "specular"
        * "ambient"
        * "emissive"
        * "height"
        * "normals"
        * "shininess"
        * "opacity"
        * "displacement"
        * "lightmap"
        * "reflection"
        * "base_color"
        * "normal_camera"
        * "emission_color"
        * "metalness"
        * "diffuse_roughness"
        * "ambient_occlusion"
        * "unknown"
        * "sheen"
        * "clearcoat"
        * "transmission"

        These correspond to the various textures defined by assimp. In many cases, you'll have multiple types packed
        into a single texture - like having a textuure that has metallic on the blue channel, roughness on the green,
        and ambient occlusion on the red. In that case, you'll want to pick one texture type to load, and use the
        texture shader to extract the channels you want.

        The textures list may also contain displayables, which will be used as textures directly.

    `shader`
        Either a string or tuple of strings, giving the name of the shader to use.

    `tangents`
        If True, tangents will be included in the mesh.

    `zoom`
        A zoom factor that will be applied to the model. Many models naturally use the range -1 to 1, and so this
        may need to be quite large to make the model visible.

    `flip_x`
        If True, the model will be flipped along the x axis.

    `flip_y`
        If True, the model will be flipped along the y axis. This defaults to True, to map models to Ren'Py's
        coordinate system.

    `flip_z`
        If True, the model will be flipped along the z axis.

    `flip_uv`
        If True, the UV coordinates will be flipped vertically. This defaults to True, to map texture coordinates
        to how Ren'Py expects them.
    """

    filename: str
    "The filename of the model to display."

    textures: Iterable[str]
    "The textures to load."

    shaders: Iterable[str]
    "The shaders to use."

    tangents: bool
    "True if tangents should be included in the mesh."

    zoom: float
    "The zoom level of the model."

    flip_y: bool
    "True if the model should be flipped along the y axis."

    flip_z: bool
    "True if the model should be flipped along the z axis."

    flip_uv: bool
    "True if the UV coordinates should be flipped vertically."


    def __init__(
        self,
        filename: str,
        textures: Iterable = ("diffuse",),
        shader: str|tuple[str] = "renpy.texture",
        tangents: bool = False,
        zoom: float = 1.0,
        flip_x: bool = False,
        flip_y: bool = True,
        flip_z: bool = False,
        flip_uv: bool = True):

        super().__init__()

        if isinstance(shader, str):
            shaders = (shader, )
        else:
            shaders = shader

        self.filename = filename
        self.shaders = shaders
        self.tangents = tangents
        self.zoom = zoom

        self.flip_x = flip_x
        self.flip_y = flip_y
        self.flip_z = flip_z
        self.flip_uv = flip_uv

        self.textures = [ ]

        for i in textures:
            if i not in TEXTURE_TYPES:
                i = renpy.easy.displayable(i)

            self.textures.append(i)

        self._duplicatable = any(getattr(i, "_duplicatable", False) for i in self.textures)

    def load(self):
        """
        Loads the AssimpModel, including its meshes and textures.
        """

        model_data = cache.get(self)

        if model_data is None:

            with loader_lock:
                model_data = cache[self] = ModelData()

                try:

                    loader.load(
                        model_data,
                        self.filename,
                        self.textures,
                        self.shaders,
                        self.tangents,
                        self.zoom,
                        self.flip_x,
                        self.flip_y,
                        self.flip_z,
                        self.flip_uv)

                except Exception as e:
                    del cache[self]
                    raise

            for d in (j for i in cache[self].mesh_info for j in i.textures if j):
                renpy.display.im.cache.preload_image(d)

        return model_data

    def render(self, width, height, st, at):

        new_predicted.add(self)

        model_data = self.load()

        rv = Render(0, 0)

        for mi in model_data.mesh_info:
            cr = Render(0, 0)
            cr.mesh = mi.mesh
            cr.reverse = mi.reverse_matrix
            cr.forward = mi.forward_matrix

            for i in mi.shaders:
                cr.add_shader(i)

            for i in mi.textures:
                cr.blit(renpy.display.im.render_for_texture(i, width, height, st, at), (0, 0))

            rv.blit(cr, (0, 0))

        rv.add_property("depth", True)
        rv.add_property("texture_wrap", (renpy.uguu.GL_REPEAT, renpy.uguu.GL_REPEAT))

        return rv

    def visit(self):
        if self in cache:
            return [ j for i in cache[self].mesh_info for j in i.textures ]
        else:
            return [ ]

    def predict_one(self):
        new_predicted.add(self)

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self is other


def finish_predict():
    """
    Called to finish the prediction process.
    """

    global predicted
    global new_predicted

    if new_predicted != predicted:
        predicted = new_predicted
        new_predicted = set()

        renpy.display.im.cache.start_prediction()


def preload():
    """
    Called to preload predicted models.
    """

    if predicted is None:
        return

    for i in set(cache.keys()) - predicted:
        del cache[i]

    for i in predicted:
        i.load()


cdef public int assimp_loadable(const char *filename) nogil:
    """
    Returns 1 if filename is loadable, 0 otherwise.
    """

    with gil:
        fn = filename.decode()

        if renpy.loader.loadable(filename):
            return 1
        else:
            return 0


cdef public SDL_RWops *assimp_load(const char *filename) nogil:
    """
    Loads the model from the given filename.
    """

    cdef SDL_RWops *rv = NULL

    with gil:

        fn = filename.decode()

        try:
            f = renpy.loader.load(fn)
            rv = RWopsFromPython(f)
        except Exception as e:
            pass

    return rv
