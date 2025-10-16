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


import functools
import threading

from typing import Iterable, Literal

from pygame_sdl2 cimport *
import_pygame_sdl2()

from assimpapi cimport (
    Importer,

    aiProcessPreset_TargetRealtime_Quality,
    aiProcess_FlipUVs,
    aiProcess_FlipWindingOrder,

    aiScene,
    aiMesh,
    aiMatrix4x4,
    aiFace,
    aiNode,
    IOSystem,

    aiPrimitiveType_TRIANGLE,
    aiPrimitiveType_LINE,
    aiPrimitiveType_POINT,

    aiTexture,
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

    aiPTI_Float,
    aiPTI_Double,
    aiPTI_Integer,
    aiPTI_Buffer,

    aiString,
    aiMaterial,
    aiGetMaterialFloatArray,
    aiGetMaterialIntegerArray,

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
    "u_tex_none": aiTextureType_NONE,
    "u_tex_diffuse": aiTextureType_DIFFUSE,
    "u_tex_specular": aiTextureType_SPECULAR,
    "u_tex_ambient": aiTextureType_AMBIENT,
    "u_tex_emissive": aiTextureType_EMISSIVE,
    "u_tex_height": aiTextureType_HEIGHT,
    "u_tex_normals": aiTextureType_NORMALS,
    "u_tex_shininess": aiTextureType_SHININESS,
    "u_tex_opacity": aiTextureType_OPACITY,
    "u_tex_displacement": aiTextureType_DISPLACEMENT,
    "u_tex_lightmap": aiTextureType_LIGHTMAP,
    "u_tex_reflection": aiTextureType_REFLECTION,
    "u_tex_base_color": aiTextureType_BASE_COLOR,
    "u_tex_normal_camera": aiTextureType_NORMAL_CAMERA,
    "u_tex_emission_color": aiTextureType_EMISSION_COLOR,
    "u_tex_metalness": aiTextureType_METALNESS,
    "u_tex_diffuse_roughness": aiTextureType_DIFFUSE_ROUGHNESS,
    "u_tex_ambient_occlusion": aiTextureType_AMBIENT_OCCLUSION,
    "u_tex_unknown": aiTextureType_UNKNOWN,
    "u_tex_sheen": aiTextureType_SHEEN,
    "u_tex_clearcoat": aiTextureType_CLEARCOAT,
    "u_tex_transmission": aiTextureType_TRANSMISSION,
}


def free_memory():
    cache.clear()


class MeshInfo:
    """
    This stores the information used to blit a texture.
    """

    mesh: Mesh3
    "The mesh that's being loaded."

    shaders: Iterable[str]
    """
    The shaders to use.
    """

    uniforms: dict[str, object]
    """
    A dictionary of uniforms that are set by the material.
    """

    texture_uniforms = dict[str, renpy.display.displayable.Displayable]
    """
    A dictionary of texture uniforms that are set by the material.
    """

    twosided: bool
    """
    True of the mesh is two-sided, and should be rendered with backface culling disabled.
    """

    def __init__(self, Loader loader, Mesh3 mesh, int material_index, textures: Iterable[str], shaders: Iterable[str]):

        self.mesh = mesh
        self.shaders = shaders

        self.uniforms = loader.get_material_uniforms(material_index)
        self.texture_uniforms = loader.get_texture_uniforms(material_index)
        self.twosided = loader.get_twosided(material_index)


class BlitInfo:
    """
    This stores the information used to blit a texture.
    """

    def __init__(self, reverse: Matrix, forward: Matrix, mesh_info: MeshInfo):
        """
        Initializes the BlitInfo.
        """

        self.reverse: Matrix = reverse
        self.forward: Matrix = forward
        self.mesh_info: MeshInfo = mesh_info

        if self.mesh_info is None:
            raise ValueError("MeshInfo cannot be None.")

class ModelData:
    """
    Represents the information about a model after it's been loaded.
    """

    filename: str
    "The filename of the model."

    embedded_textures: dict[str, Data]
    "The embedded textures in the model."

    blit_info: list[BlitInfo]
    "Information required to blit each mesh in the model."

    mesh_info: list[MeshInfo]
    "A list of MeshInfo objects used by the blit_info objects."

    def __init__(self):
        self.embedded_textures = { }
        self.blit_info = [ ]


    def report(self):
        """
        Prints a report of the model data.
        """

        def log(msg: str):
            """
            Prints a message to the log.
            """

            renpy.display.log.write("%s", msg)

        log("")
        log(f"GLTFModel {self.filename!r}")

        minx = miny = minz = float("inf")
        maxx = maxy = maxz = float("-inf")

        for bi in self.blit_info:
            for x, y, z, w in bi.mesh_info.mesh.get_points():

                x, y, z = bi.reverse.transform(x, y, z, components=3)

                minx = min(minx, x)
                miny = min(miny, y)
                minz = min(minz, z)

                maxx = max(maxx, x)
                maxy = max(maxy, y)
                maxz = max(maxz, z)

        log(f"  Bounding box (after zoom):")

        log(f"    X: {minx:.3f} to {maxx:.3f}")
        log(f"    Y: {miny:.3f} to {maxy:.3f}")
        log(f"    Z: {minz:.3f} to {maxz:.3f}")

        uniform_sets = [ ]

        min_values = { }
        max_values = { }

        types: dict[str, str] = {}

        def recursive_min(a, b):
            """
            Returns the minimum of a and b. If a and b are tuples, it returns a tuple of the minimums.
            """

            if isinstance(a, tuple) and isinstance(b, tuple):
                return tuple(recursive_min(x, y) for x, y in zip(a, b))
            else:
                return min(a, b)

        def recursive_max(a, b):
            """
            Returns the maximum of a and b. If a and b are tuples, it returns a tuple of the maximums.
            """
            if isinstance(a, tuple) and isinstance(b, tuple):
                return tuple(recursive_max(x, y) for x, y in zip(a, b))
            else:
                return max(a, b)


        def recursive_format(v):
            """
            Formats a value for display. If it's a tuple, it formats each element.
            """

            if v is None:
                return "N/A"

            if isinstance(v, tuple):
                return "(" + ", ".join(f"{x:.5g}" for x in v) + ")"
            else:
                return f"{v:.5g}"

        for i in self.mesh_info:
            uniform_sets.append(set(i.uniforms) | set(i.texture_uniforms))

            for k, v in i.uniforms.items():
                if k not in min_values:
                    min_values[k] = v
                    max_values[k] = v
                else:
                    min_values[k] = recursive_min(min_values[k], v)
                    max_values[k] = recursive_max(max_values[k], v)

                if isinstance(v, float):
                    types[k] = "float"
                elif isinstance(v, int):
                    types[k] = "int"
                elif isinstance(v, tuple):
                    types[k] = f"vec{len(v)}"
                else:
                    types[k] = "unknown"

            for k, v in i.texture_uniforms.items():
                types[k] = "sampler2D"


        any_uniforms = set.union(*uniform_sets)
        all_uniforms = set.intersection(*uniform_sets)
        all_uniforms.add("u_tex_diffuse")

        log("  Uniforms:")

        for u in sorted(any_uniforms):

            min_value = min_values.get(u, None)
            max_value = max_values.get(u, None)

            comments = [ ]

            if min_value is not None:
                comments.append(f"range {recursive_format(min_value)} to {recursive_format(max_value)}")

            if u not in all_uniforms:
                comments.append("not in all meshes")

            uniform_type = types.get(u, "unknown")

            comment = "; ".join(comments)
            if comment:
                comment = " // " + comment


            log(f"    uniform {uniform_type} {u};{comment}")


cache: dict[GLTFModel, ModelData] = { }
"Caches the models that have been loaded."

predicted: set[GLTFModel]|None = None
"The set of models that are predicted to be loaded."

new_predicted: set[GLTFModel] = set()
"The same, but before finish_predict() is called."

cdef class Loader:

    cdef public str dirname
    "The directory that the asset was loaded from."

    cdef Importer importer
    "The importer used to load the models."

    cdef const aiScene *scene
    "The scene that has been loaded."

    cdef public object model_data
    "The ModelData object that is being filled in."

    cdef public dict mesh_info
    "A dictionary mapping mesh indices to MeshInfo objects."

    cdef public bint tangents
    "True if tangents should be included in the mesh."

    cdef public object shaders
    "A shader or list of shaders to use."

    cdef public set uniforms
    "A list of the uniforms being set by materials."

    cdef public dict textures
    "A map from material and texture type to the texture displayable."

    cdef public object filename
    "The name of the file being loaded."


    def __cinit__(self):
        self.importer.SetIOHandler(new RenpyIOSystem())

    def load(
        self,
        model_data: ModelData,
        filename: str,
        shaders: Iterable[str|renpy.display.displayable.Displayable],
        tangents: bool,
        zoom: float,
        report: bool) -> None:

        if not renpy.loader.loadable(filename):
            raise FileNotFoundError(f"GLTFModel not loadable: {filename}")

        self.filename = filename

        self.shaders = shaders
        self.tangents = tangents
        self.uniforms = set()

        self.textures = { }

        self.dirname = filename.rpartition("/")[0]

        # Load the scene.
        filename_bytes = filename.encode()
        self.scene = self.importer.ReadFile(
            filename_bytes,
            aiProcessPreset_TargetRealtime_Quality | aiProcess_FlipUVs | aiProcess_FlipWindingOrder)

        if not self.scene:
            raise Exception("Error loading %s: %s" % (filename, self.importer.GetErrorString()))

        try:

            self.model_data = model_data
            self.mesh_info = { }

            self.load_textures()

            # The base matrix uses scale and rotate to move the model into the Ren'Py coordinate system,
            # and then scales it.
            m = Matrix.scale(-1, -1, -1) * Matrix.rotate(0, 180, 0) *  Matrix.scale(zoom, zoom, zoom)

            self.load_node(self.scene.mRootNode, m)

            self.model_data.filename = filename
            self.model_data.mesh_info = list(self.mesh_info.values())

            if report:
                self.model_data.report()

            return self.model_data

        finally:
            self.mesh_info = { }
            self.shaders = [ ]
            self.model_data = None
            self.uniforms = set()

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

    def get_texture(self, material_index : int, texture_type : int) -> Displayable|None:
        """
        Given a material index and a texture type, returns the path to the texture. This
        may also be *0 (etc) for embedded textures.
        """

        key = (material_index, texture_type)

        if key in self.textures:
            return self.textures[key]

        cdef aiString path_string
        cdef aiMaterial *material = self.scene.mMaterials[material_index]

        if material.GetTextureCount(texture_type) == 0:
            rv = None
        else:
            material.GetTexture(texture_type, 0, &path_string)
            path = path_string.data[:path_string.length].decode()

            if path.startswith("*"):
                d = loader.model_data.embedded_textures[path]

            else:
                d = renpy.easy.displayable(loader.dirname + "/" + path)

            rv = unoptimized_texture(d)

        self.textures[key] = rv

        return rv

    def get_texture_uniforms(self, material_index: int) -> dict[str, str]:
        """
        Given a material index, returns a dictionary of texture uniforms that
        should be set for the material.
        """

        uniforms = { }

        for uniform, texture_type in TEXTURE_TYPES.items():

            d = self.get_texture(material_index, texture_type)
            if d is not None:
                uniforms[uniform] = unoptimized_texture(d)

        return uniforms

    def get_material_uniforms(self, material_index: int):

        cdef float[4] values
        cdef int ivalue
        cdef unsigned int pmax

        cdef aiMaterial *material = self.scene.mMaterials[material_index]

        uniforms = { }

        for i in range(material.mNumProperties):
            pmax = 4

            prop = material.mProperties[i]

            key = prop.mKey.data[:prop.mKey.length].decode()

            prefix, _, suffix = key.partition(".")
            suffix = suffix.lower().replace(".", "_")

            if prop.mType != aiPTI_Float and prop.mType != aiPTI_Double and prop.mType != aiPTI_Integer and prop.mType != aiPTI_Buffer:
                continue

            if prefix == "$mat":
                name = f"u_material_{suffix}"
            elif prefix == "$clr":
                name = f"u_color_{suffix}"
            else:
                continue

            pmax = 4
            if aiGetMaterialFloatArray(material, prop.mKey.data, 0, 0, &values[0], &pmax):
                continue

            if pmax == 1:
                value = values[0]
            elif pmax == 2:
                value = (values[0], values[1])
            elif pmax == 3:
                value = (values[0], values[1], values[2])
            elif pmax == 4:
                value = (values[0], values[1], values[2], values[3])
            else:
                continue

            uniforms[name] = value

        return uniforms

    def get_twosided(self, material_index: int) -> bool:
        """
        Returns True if the material with the given index is two-sided.
        """

        cdef aiMaterial *material = self.scene.mMaterials[material_index]
        cdef int ivalue

        if aiGetMaterialIntegerArray(material, "$mat.twosided", 0, 0, &ivalue, NULL):
            return False

        return ivalue != 0


    cdef load_node(self, aiNode *node, matrix : Matrix):
        cdef unsigned int i

        node_matrix = Matrix((
            node.mTransformation.a1, node.mTransformation.a2, node.mTransformation.a3, node.mTransformation.a4,
            node.mTransformation.b1, node.mTransformation.b2, node.mTransformation.b3, node.mTransformation.b4,
            node.mTransformation.c1, node.mTransformation.c2, node.mTransformation.c3, node.mTransformation.c4,
            node.mTransformation.d1, node.mTransformation.d2, node.mTransformation.d3, node.mTransformation.d4,
            ))

        matrix = matrix * node_matrix

        for i in range(node.mNumMeshes):

            mesh_info = self.load_mesh(node.mMeshes[i])

            if mesh_info is None:
                continue

            self.model_data.blit_info.append(BlitInfo(
                matrix,
                matrix.inverse(),
                mesh_info))

        for i in range(node.mNumChildren):
            self.load_node(node.mChildren[i], matrix)


    def load_mesh(self, mesh_index: int) -> MeshInfo:
        """
        Loads the mesh with index `mesh_index` from the scene.
        """

        cached = self.mesh_info.get(mesh_index, None)
        if cached is not None:
            return cached

        if mesh_index < 0 or mesh_index >= self.scene.mNumMeshes:
            raise Exception("Invalid mesh index %d." % mesh_index)

        cdef aiMesh *mesh = self.scene.mMeshes[mesh_index]

        def log(msg: str):
            if renpy.config.developer:
                renpy.display.log.write("%s", msg)

        if mesh.mPrimitiveTypes == aiPrimitiveType_LINE:
            log(f"Warning: {self.filename!r}, mesh {mesh_index} is a line mesh, which is not supported. Skipping.")
            return

        if mesh.mPrimitiveTypes == aiPrimitiveType_POINT:
            log(f"Warning: {self.filename!r}, mesh {mesh_index} is a point mesh, which is not supported. Skipping.")
            return

        if mesh.mPrimitiveTypes != aiPrimitiveType_TRIANGLE:
            log(f"Warning: {self.filename!r}, mesh {mesh_index} is not a triangle mesh (type={mesh.mPrimitiveTypes}). Skipping.")
            return

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
            mesh.mMaterialIndex,
            self.textures,
            self.shaders)

        self.mesh_info[mesh_index] = info
        return info

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

    `shader`
        Either a string or tuple of strings, giving the name of the shader to use.

    `tangents`
        If True, tangents will be included in the mesh.

    `zoom`
        A zoom factor that will be applied to the model. Many models naturally use the range -1 to 1, and so this
        may need to be quite large to make the model visible.

    `report`
        If true, a report of the model will be printed to the log. This includes the uniforms that are used by
        the model.
    """

    filename: str
    "The filename of the model to display."

    shaders: Iterable[str]
    "The shaders to use."

    tangents: bool
    "True if tangents should be included in the mesh."

    zoom: float
    "The zoom level of the model."

    uniforms: dict[str, object]
    """
    A dictionary of uniforms that are set by the model.
    """

    texture_uniforms: dict[str, renpy.display.displayable.Displayable]
    """
    A dictionary of texture uniforms.
    """

    report: bool
    """
    Should a report of the model be printed to the log? This includes the uniforms that are used by the model.
    """

    def __init__(
        self,
        filename: str,
        shader: str|tuple[str] = tuple(),
        tangents: bool = False,
        zoom: float = 1.0,
        report: bool = False,
        **kwargs):

        super().__init__()

        if isinstance(shader, str):
            shaders = (shader, )
        else:
            shaders = shader

        if not shaders:
            raise ValueError("At least one shader must be specified for GLTFModel. Consider 'renpy.texture' to start with.")

        self.filename = filename
        self.shaders = shaders
        self.tangents = tangents
        self.zoom = zoom
        self.report = report

        self.uniforms = { }
        self.texture_uniforms = { }

        kwargs.setdefault("u_tex_diffuse", renpy.display.im.Null("#fff"))

        for k, v in kwargs.items():

            if k.startswith("u_tex_"):
                self.texture_uniforms[k] = renpy.display.im.unoptimized_texture(renpy.easy.displayable(v))
            elif k.startswith("u_"):
                self.uniforms[k] = v
            else:
                raise ValueError(f"Unknown keyword argument {k!r} for GLTFModel. Uniforms must start with 'u_'.")

        if report:
            self.load()
            self.report = False


    def load(self):
        """
        Loads the AssimpModel, including its meshes and textures.
        """

        model_data = cache.get(self)

        if model_data is None:

            with loader_lock:
                model_data = ModelData()

                loader.load(
                    model_data,
                    self.filename,
                    self.shaders,
                    self.tangents,
                    self.zoom,
                    self.report)

                cache[self] = model_data

            for i in cache[self].mesh_info:
                for d in i.texture_uniforms.values():
                    renpy.display.im.cache.preload_image(d)

        return model_data

    def render(self, width, height, st, at):

        new_predicted.add(self)

        model_data = self.load()

        rv = Render(0, 0)

        for k, v in self.uniforms.items():
            rv.add_uniform(k, v)

        for k, v in self.texture_uniforms.items():
            tr = renpy.display.im.render_for_texture(v, width, height, st, at)
            rv.add_uniform(k, tr)

        for bi in model_data.blit_info:
            mi = bi.mesh_info

            cr = Render(0, 0)
            cr.mesh = mi.mesh
            cr.reverse = bi.reverse
            cr.forward = bi.forward

            for i in mi.shaders:
                cr.add_shader(i)

            for k, v in mi.uniforms.items():
                cr.add_uniform(k, v)

            if mi.twosided:
                cr.add_property("cull_face", None)

            has_diffuse = False

            for k, i in mi.texture_uniforms.items():
                tr = renpy.display.im.render_for_texture(i, width, height, st, at)
                cr.add_uniform(k, tr)

                if k == "u_tex_diffuse":
                    cr.blit(tr, (0, 0))
                    has_diffuse = True

            if not has_diffuse:
                tr = renpy.display.im.render_for_texture(self.texture_uniforms.get("u_tex_diffuse", renpy.display.im.Null("#fff")), width, height, st, at)
                cr.blit(tr, (0, 0))

            rv.blit(cr, (0, 0))

        rv.add_property("depth", True)
        rv.add_property("texture_wrap", (renpy.uguu.GL_REPEAT, renpy.uguu.GL_REPEAT))
        rv.add_property("cull_face", "ccw")

        return rv

    def visit(self):
        if self in cache:
            return [ j for i in cache[self].mesh_info for j in i.texture_uniforms.values() ]
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
