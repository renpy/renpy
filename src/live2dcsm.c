#include "live2dcsm.h"
#include <SDL2/SDL.h>
#include <stdio.h>
#include <string.h>

#ifndef __EMSCRIPTEN__

// All other platforms use SDL_LoadObject and SDL_LoadFunction to load the CSM from the live2d libraries.

void *load_live2d_object(const char *sofile) {
    void *handle = SDL_LoadObject(sofile);
    return handle;
}

void *load_live2d_function(void *obj, const char *name) {
    void *func = SDL_LoadFunction(obj, name);
    return func;
}

void deallocate_live2d_moc(void *moc) {

}

void deallocate_live2d_model(void *model) {

}


#else

#include <emscripten.h>

typedef struct csmMoc csmMoc;
typedef struct csmModel csmModel;
typedef unsigned int csmVersion;
typedef unsigned int csmMocVersion;

typedef unsigned int csmParameterType;
typedef unsigned char csmFlags;

typedef struct csmVector2 {
    float x;
    float y;
} csmVector2;

typedef struct csmVector4 {
    float x;
    float y;
    float z;
    float w;
} csmVector4;

typedef void (*csmLogFunction)(const char* message);

// Wrappers to call the CSM functions in JavaScript using EM_JS.

static EM_JS(csmVersion, wasmGetVersion, (), {
    return window.live2d_csm.ccall('csmGetVersion', 'number', [], []);
});

static EM_JS(csmMocVersion, wasmGetLatestMocVersion, (), {
    return window.live2d_csm.ccall('csmGetLatestMocVersion', 'number', [], []);
});

static EM_JS(csmMocVersion, wasmGetMocVersion, (const void* address, const unsigned int size), {
    return 0;
});

static EM_JS(int, wasmHasMocConsistency, (void* address, const unsigned int size), {
    return 0;
});

static EM_JS(csmLogFunction, wasmGetLogFunction, (), {
    return 0;
});

static EM_JS(void, wasmSetLogFunction, (csmLogFunction handler), {
});

static EM_JS(csmMoc*, wasmReviveMocInPlace, (void* address, const unsigned int size), {
    return 0;
});

static EM_JS(unsigned int, wasmGetSizeofModel, (const csmMoc* moc), {
    return 0;
});

static EM_JS(csmModel*, wasmInitializeModelInPlace, (const csmMoc* moc, void* address, const unsigned int size), {
    return 0;
});

static EM_JS(void, wasmUpdateModel, (csmModel* model), {
});

static EM_JS(void, wasmReadCanvasInfo, (const csmModel* model, csmVector2* outSizeInPixels, csmVector2* outOriginInPixels, float* outPixelsPerUnit), {
});

static EM_JS(int, wasmGetParameterCount, (const csmModel* model), {
    return 0;
});

static EM_JS(const char**, wasmGetParameterIds, (const csmModel* model), {
    return 0;
});

static EM_JS(const csmParameterType*, wasmGetParameterTypes, (const csmModel* model), {
    return 0;
});

static EM_JS(const float*, wasmGetParameterMinimumValues, (const csmModel* model), {
    return 0;
});

static EM_JS(const float*, wasmGetParameterMaximumValues, (const csmModel* model), {
    return 0;
});

static EM_JS(const float*, wasmGetParameterDefaultValues, (const csmModel* model), {
    return 0;
});

static EM_JS(float*, wasmGetParameterValues, (csmModel* model), {
    return 0;
});

static EM_JS(const int*, wasmGetParameterRepeats, (const csmModel* model), {
    return 0;
});

static EM_JS(const int*, wasmGetParameterKeyCounts, (const csmModel* model), {
    return 0;
});

static EM_JS(const float**, wasmGetParameterKeyValues, (const csmModel* model), {
    return 0;
});

static EM_JS(int, wasmGetPartCount, (const csmModel* model), {
    return 0;
});

static EM_JS(const char**, wasmGetPartIds, (const csmModel* model), {
    return 0;
});

static EM_JS(float*, wasmGetPartOpacities, (csmModel* model), {
    return 0;
});

static EM_JS(const int*, wasmGetPartParentPartIndices, (const csmModel* model), {
    return 0;
});

static EM_JS(int, wasmGetDrawableCount, (const csmModel* model), {
    return 0;
});

static EM_JS(const char**, wasmGetDrawableIds, (const csmModel* model), {
    return 0;
});

static EM_JS(const csmFlags*, wasmGetDrawableConstantFlags, (const csmModel* model), {
    return 0;
});

static EM_JS(const csmFlags*, wasmGetDrawableDynamicFlags, (const csmModel* model), {
    return 0;
});

static EM_JS(const int*, wasmGetDrawableTextureIndices, (const csmModel* model), {
    return 0;
});

static EM_JS(const int*, wasmGetDrawableDrawOrders, (const csmModel* model), {
    return 0;
});

static EM_JS(const int*, wasmGetDrawableRenderOrders, (const csmModel* model), {
    return 0;
});

static EM_JS(const float*, wasmGetDrawableOpacities, (const csmModel* model), {
    return 0;
});

static EM_JS(const int*, wasmGetDrawableMaskCounts, (const csmModel* model), {
    return 0;
});

static EM_JS(const int**, wasmGetDrawableMasks, (const csmModel* model), {
    return 0;
});

static EM_JS(const int*, wasmGetDrawableVertexCounts, (const csmModel* model), {
    return 0;
});

static EM_JS(const csmVector2**, wasmGetDrawableVertexPositions, (const csmModel* model), {
    return 0;
});

static EM_JS(const csmVector2**, wasmGetDrawableVertexUvs, (const csmModel* model), {
    return 0;
});

static EM_JS(const int*, wasmGetDrawableIndexCounts, (const csmModel* model), {
    return 0;
});

static EM_JS(const unsigned short**, wasmGetDrawableIndices, (const csmModel* model), {
    return 0;
});

static EM_JS(const csmVector4*, wasmGetDrawableMultiplyColors, (const csmModel* model), {
    return 0;
});

static EM_JS(const csmVector4*, wasmGetDrawableScreenColors, (const csmModel* model), {
    return 0;
});

static EM_JS(const int*, wasmGetDrawableParentPartIndices, (const csmModel* model), {
    return 0;
});

static EM_JS(void, wasmResetDrawableDynamicFlags, (csmModel* model), {
});


// Our CSM function implementations.

static csmVersion csmGetVersion() {
    return wasmGetVersion();
}

static csmMocVersion csmGetLatestMocVersion() {
    return wasmGetLatestMocVersion();
}

static csmMocVersion csmGetMocVersion(const void* address, const unsigned int size) {
    return 0;
}

static int csmHasMocConsistency(void* address, const unsigned int size) {
    return 0;
}

static csmLogFunction csmGetLogFunction() {
    return NULL;
}

static void csmSetLogFunction(csmLogFunction handler) {
}

static csmMoc* csmReviveMocInPlace(void* address, const unsigned int size) {
    return NULL;
}

static unsigned int csmGetSizeofModel(const csmMoc* moc) {
    return 0;
}

static csmModel* csmInitializeModelInPlace(const csmMoc* moc, void* address, const unsigned int size) {
    return NULL;
}

static void csmUpdateModel(csmModel* model) {
}

static void csmReadCanvasInfo(const csmModel* model, csmVector2* outSizeInPixels, csmVector2* outOriginInPixels, float* outPixelsPerUnit) {
}

static int csmGetParameterCount(const csmModel* model) {
    return 0;
}

static const char** csmGetParameterIds(const csmModel* model) {
    return NULL;
}

static const csmParameterType* csmGetParameterTypes(const csmModel* model) {
    return NULL;
}

static const float* csmGetParameterMinimumValues(const csmModel* model) {
    return NULL;
}

static const float* csmGetParameterMaximumValues(const csmModel* model) {
    return NULL;
}

static const float* csmGetParameterDefaultValues(const csmModel* model) {
    return NULL;
}

static float* csmGetParameterValues(csmModel* model) {
    return NULL;
}

static const int* csmGetParameterRepeats(const csmModel* model) {
    return NULL;
}

static const int* csmGetParameterKeyCounts(const csmModel* model) {
    return NULL;
}

static const float** csmGetParameterKeyValues(const csmModel* model) {
    return NULL;
}

static int csmGetPartCount(const csmModel* model) {
    return 0;
}

static const char** csmGetPartIds(const csmModel* model) {
    return NULL;
}

static float* csmGetPartOpacities(csmModel* model) {
    return NULL;
}

static const int* csmGetPartParentPartIndices(const csmModel* model) {
    return NULL;
}

static int csmGetDrawableCount(const csmModel* model) {
    return 0;
}

static const char** csmGetDrawableIds(const csmModel* model) {
    return NULL;
}

static const csmFlags* csmGetDrawableConstantFlags(const csmModel* model) {
    return NULL;
}

static const csmFlags* csmGetDrawableDynamicFlags(const csmModel* model) {
    return NULL;
}

static const int* csmGetDrawableTextureIndices(const csmModel* model) {
    return NULL;
}

static const int* csmGetDrawableDrawOrders(const csmModel* model) {
    return NULL;
}

static const int* csmGetDrawableRenderOrders(const csmModel* model) {
    return NULL;
}

static const float* csmGetDrawableOpacities(const csmModel* model) {
    return NULL;
}

static const int* csmGetDrawableMaskCounts(const csmModel* model) {
    return NULL;
}

static const int** csmGetDrawableMasks(const csmModel* model) {
    return NULL;
}

static const int* csmGetDrawableVertexCounts(const csmModel* model) {
    return NULL;
}

static const csmVector2** csmGetDrawableVertexPositions(const csmModel* model) {
    return NULL;
}

static const csmVector2** csmGetDrawableVertexUvs(const csmModel* model) {
    return NULL;
}

static const int* csmGetDrawableIndexCounts(const csmModel* model) {
    return NULL;
}

static const unsigned short** csmGetDrawableIndices(const csmModel* model) {
    return NULL;
}

static const csmVector4* csmGetDrawableMultiplyColors(const csmModel* model) {
    return NULL;
}

static const csmVector4* csmGetDrawableScreenColors(const csmModel* model) {
    return NULL;
}

static const int* csmGetDrawableParentPartIndices(const csmModel* model) {
    return NULL;
}

static void csmResetDrawableDynamicFlags(csmModel* model) {
}

struct NameToPointer {
    const char* name;
    void* pointer;
};

static struct NameToPointer nameToPointer[] = {
    {"csmGetVersion", (void*) csmGetVersion},
    {"csmGetLatestMocVersion", (void*) csmGetLatestMocVersion},
    {"csmGetMocVersion", (void*) csmGetMocVersion},
    {"csmHasMocConsistency", (void*) csmHasMocConsistency},
    {"csmGetLogFunction", (void*) csmGetLogFunction},
    {"csmSetLogFunction", (void*) csmSetLogFunction},
    {"csmReviveMocInPlace", (void*) csmReviveMocInPlace},
    {"csmGetSizeofModel", (void*) csmGetSizeofModel},
    {"csmInitializeModelInPlace", (void*) csmInitializeModelInPlace},
    {"csmUpdateModel", (void*) csmUpdateModel},
    {"csmReadCanvasInfo", (void*) csmReadCanvasInfo},
    {"csmGetParameterCount", (void*) csmGetParameterCount},
    {"csmGetParameterIds", (void*) csmGetParameterIds},
    {"csmGetParameterTypes", (void*) csmGetParameterTypes},
    {"csmGetParameterMinimumValues", (void*) csmGetParameterMinimumValues},
    {"csmGetParameterMaximumValues", (void*) csmGetParameterMaximumValues},
    {"csmGetParameterDefaultValues", (void*) csmGetParameterDefaultValues},
    {"csmGetParameterValues", (void*) csmGetParameterValues},
    {"csmGetParameterRepeats", (void*) csmGetParameterRepeats},
    {"csmGetParameterKeyCounts", (void*) csmGetParameterKeyCounts},
    {"csmGetParameterKeyValues", (void*) csmGetParameterKeyValues},
    {"csmGetPartCount", (void*) csmGetPartCount},
    {"csmGetPartIds", (void*) csmGetPartIds},
    {"csmGetPartOpacities", (void*) csmGetPartOpacities},
    {"csmGetPartParentPartIndices", (void*) csmGetPartParentPartIndices},
    {"csmGetDrawableCount", (void*) csmGetDrawableCount},
    {"csmGetDrawableIds", (void*) csmGetDrawableIds},
    {"csmGetDrawableConstantFlags", (void*) csmGetDrawableConstantFlags},
    {"csmGetDrawableDynamicFlags", (void*) csmGetDrawableDynamicFlags},
    {"csmGetDrawableTextureIndices", (void*) csmGetDrawableTextureIndices},
    {"csmGetDrawableDrawOrders", (void*) csmGetDrawableDrawOrders},
    {"csmGetDrawableRenderOrders", (void*) csmGetDrawableRenderOrders},
    {"csmGetDrawableOpacities", (void*) csmGetDrawableOpacities},
    {"csmGetDrawableMaskCounts", (void*) csmGetDrawableMaskCounts},
    {"csmGetDrawableMasks", (void*) csmGetDrawableMasks},
    {"csmGetDrawableVertexCounts", (void*) csmGetDrawableVertexCounts},
    {"csmGetDrawableVertexPositions", (void*) csmGetDrawableVertexPositions},
    {"csmGetDrawableVertexUvs", (void*) csmGetDrawableVertexUvs},
    {"csmGetDrawableIndexCounts", (void*) csmGetDrawableIndexCounts},
    {"csmGetDrawableIndices", (void*) csmGetDrawableIndices},
    {"csmGetDrawableMultiplyColors", (void*) csmGetDrawableMultiplyColors},
    {"csmGetDrawableScreenColors", (void*) csmGetDrawableScreenColors},
    {"csmGetDrawableParentPartIndices", (void*) csmGetDrawableParentPartIndices},
    {"csmResetDrawableDynamicFlags", (void*) csmResetDrawableDynamicFlags},
    {NULL, NULL}
};

void *load_live2d_object(const char *sofile) {
    return (void *) 1;
}

void *load_live2d_function(void *obj, const char *name) {
    if (obj != (void *) 1) {
        return NULL;
    }

    for (int i = 0; nameToPointer[i].name != NULL; i++) {
        if (strcmp(nameToPointer[i].name, name) == 0) {
            return nameToPointer[i].pointer;
        }
    }

    fprintf(stderr, "live2dcsm: Could not find live2d function '%s'.\n", name);
    return NULL;
}

void deallocate_live2d_moc(void *moc) {

}

void deallocate_live2d_model(void *model) {

}

#endif
