cdef extern from "assimp/types.h":
    cdef enum aiReturn:
        aiReturn_SUCCESS
        aiReturn_FAILURE
        aiReturn_OUTOFMEMORYn

    cdef struct aiString:
        unsigned int length
        char[1024] data

cdef extern from "assimp/vector2.h":
    cdef struct aiVector2D:
        float x
        float y

cdef extern from "assimp/vector3.h":
    cdef struct aiVector3D:
        float x
        float y
        float z

cdef extern from "assimp/matrix4x4.h":
    cdef struct aiMatrix4x4:
        float a1, a2, a3, a4
        float b1, b2, b3, b4
        float c1, c2, c3, c4
        float d1, d2, d3, d4

cdef extern from "assimp/postprocess.h":
    cdef enum:
        aiProcess_CalcTangentSpace
        aiProcess_JoinIdenticalVertices
        aiProcess_MakeLeftHanded
        aiProcess_Triangulate
        aiProcess_RemoveComponent
        aiProcess_GenNormals
        aiProcess_GenSmoothNormals
        aiProcess_SplitLargeMeshes
        aiProcess_PreTransformVertices
        aiProcess_LimitBoneWeights
        aiProcess_ValidateDataStructure
        aiProcess_ImproveCacheLocality
        aiProcess_RemoveRedundantMaterials
        aiProcess_FixInfacingNormals
        aiProcess_SortByPType
        aiProcess_FindDegenerates
        aiProcess_FindInvalidData
        aiProcess_GenUVCoords
        aiProcess_TransformUVCoords
        aiProcess_FindInstances
        aiProcess_OptimizeMeshes
        aiProcess_OptimizeGraph
        aiProcess_FlipUVs
        aiProcess_FlipWindingOrder
        aiProcess_SplitByBoneCount
        aiProcess_Debone
        aiProcess_GlobalScale
        aiProcess_EmbedTextures
        aiProcess_ForceGenNormals
        aiProcess_DropNormals
        aiProcess_GenBoundingBoxes

        aiProcessPreset_TargetRealtime_Fast
        aiProcessPreset_TargetRealtime_Quality
        aiProcessPreset_TargetRealtime_MaxQuality

        aiProcess_ConvertToLeftHanded

cdef extern from "assimp/mesh.h":
    cdef enum aiPrimitiveType:
        aiPrimitiveType_POINT
        aiPrimitiveType_LINE
        aiPrimitiveType_TRIANGLE
        aiPrimitiveType_POLYGON


    cdef struct aiFace:
        unsigned int mNumIndices
        unsigned int *mIndices

    cdef struct aiMesh:
        unsigned int mPrimitiveTypes
        unsigned int mNumVertices
        unsigned int mNumFaces

        unsigned int mMaterialIndex

        aiVector3D *mVertices
        aiVector3D *mNormals
        aiVector3D *mTangents
        aiVector3D *mBitangents
        aiVector2D **mTextureCoords

        aiFace *mFaces

cdef extern from "assimp/material.h":

    cdef enum aiTextureType:
        aiTextureType_NONE
        aiTextureType_DIFFUSE
        aiTextureType_SPECULAR
        aiTextureType_AMBIENT
        aiTextureType_EMISSIVE
        aiTextureType_HEIGHT
        aiTextureType_NORMALS
        aiTextureType_SHININESS
        aiTextureType_OPACITY
        aiTextureType_DISPLACEMENT
        aiTextureType_LIGHTMAP
        aiTextureType_REFLECTION
        aiTextureType_BASE_COLOR
        aiTextureType_NORMAL_CAMERA
        aiTextureType_EMISSION_COLOR
        aiTextureType_METALNESS
        aiTextureType_DIFFUSE_ROUGHNESS
        aiTextureType_AMBIENT_OCCLUSION
        aiTextureType_UNKNOWN
        aiTextureType_SHEEN
        aiTextureType_CLEARCOAT
        aiTextureType_TRANSMISSION

    cdef struct aiMaterial:
        unsigned int GetTextureCount(aiTextureType type)
        aiReturn GetTexture(aiTextureType type, unsigned int index, aiString *path)

cdef extern from "assimp/texture.h":
    cdef struct aiTexture:
        unsigned int mWidth
        unsigned int mHeight
        char[8] achFormatHint
        void *pcData
        aiString mFilename

cdef extern from "assimp/scene.h":

    cdef struct aiNode:
        aiMatrix4x4 mTransformation
        aiNode *mParent
        unsigned int mNumChildren
        aiNode **mChildren
        unsigned int mNumMeshes
        unsigned int *mMeshes

    cdef struct aiScene:
        unsigned int mNumMeshes
        unsigned int mNumMaterials
        unsigned int mNumAnimations
        unsigned int mNumTextures
        unsigned int mNumLights
        unsigned int mNumCameras

        aiNode *mRootNode
        aiMesh **mMeshes
        aiTexture **mTextures
        aiMaterial **mMaterials

cdef extern from "assimp/IOSystem.hpp" namespace "Assimp":

    cdef cppclass IOSystem:
        pass

cdef extern from "assimp/Importer.hpp" namespace "Assimp":

    cdef cppclass Importer:
        Importer()
        const aiScene *ReadFile(const char* pFile, unsigned int pFlags)
        const aiScene *GetScene()
        void FreeScene()
        const char *GetErrorString()

        void SetIOHandler(IOSystem *ioHandler)
