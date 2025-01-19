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


    cdef struct aiMesh:
        unsigned int mNumVertices
        unsigned int mNumFaces

        aiVector3D *mVertices
        aiVector3D *mNormals
        aiVector3D *mTangents
        aiVector3D *mBitangents

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

cdef extern from "assimp/Importer.hpp" namespace "Assimp":

    cdef cppclass Importer:
        Importer()
        const aiScene *ReadFile(const char* pFile, unsigned int pFlags)
        const aiScene *GetScene()
        const char *GetErrorString()
