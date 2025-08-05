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

static EM_JS(csmVersion, live2dGetVersion, (), {
    return window.live2d_csm.ccall('csmGetVersion', 'number', [], []);
});

static EM_JS(csmMocVersion, live2dGetLatestMocVersion, (), {
    return window.live2d_csm.ccall('csmGetLatestMocVersion', 'number', [], []);
});

static EM_JS(csmMocVersion, live2dGetMocVersion, (const void* address, const unsigned int size), {
    return window.live2d_csm.ccall('csmGetMocVersion', 'number', ['number', 'number'], [address, size]);
});

static EM_JS(int, live2dHasMocConsistency, (void* address, const unsigned int size), {
    return reflect(window.live2d_csm.ccall('csmHasMocConsistency', 'number', ['number', 'number'], [address, size]));
});

static EM_JS(csmLogFunction, live2dGetLogFunction, (), {
    return NULL;
});

static EM_JS(void, live2dSetLogFunction, (csmLogFunction handler), {
    // pass
});

static EM_JS(void*, live2dReviveMocInPlace, (void* address, const unsigned int size), {
    return window.live2d_csm.ccall('csmReviveMocInPlace', 'number', ['number', 'number'], [address, size]);
});

static EM_JS(unsigned int, live2dGetSizeofModel, (void* moc), {
    return window.live2d_csm.ccall('csmGetSizeofModel', 'number', ['number'], [moc]);
});

static EM_JS(void*, live2dInitializeModelInPlace, (void* moc, void* address, const unsigned int size), {
    return window.live2d_csm.ccall('csmInitializeModelInPlace', 'number', ['number', 'number', 'number'], [moc, address, size]);
});

static EM_JS(void, live2dUpdateModel, (void* model), {
    window.live2d_csm.ccall('csmUpdateModel', 'void', ['number'], [model]);
});

static EM_JS(void, live2dReadCanvasInfo, (void* model, void *outSizeInPixels, void* outOriginInPixels, void* outPixelsPerUnit), {
    window.live2d_csm.ccall('csmReadCanvasInfo', 'void', ['number', 'number', 'number', 'number'], [model, outSizeInPixels, outOriginInPixels, outPixelsPerUnit]);
});

static EM_JS(int, live2dGetParameterCount, (void* model), {
    return window.live2d_csm.ccall('csmGetParameterCount', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetParameterIds, (void* model), {
    return window.live2d_csm.ccall('csmGetParameterIds', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetParameterTypes, (void* model), {
    return window.live2d_csm.ccall('csmGetParameterTypes', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetParameterMinimumValues, (void * model), {
    return window.live2d_csm.ccall('csmGetParameterMinimumValues', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetParameterMaximumValues, (void* model), {
    return window.live2d_csm.ccall('csmGetParameterMaximumValues', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetParameterDefaultValues, (void* model), {
    return window.live2d_csm.ccall('csmGetParameterDefaultValues', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetParameterValues, (csmModel* model), {
    return window.live2d_csm.ccall('csmGetParameterValues', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetParameterRepeats, (void* model), {
    return window.live2d_csm.ccall('csmGetParameterRepeats', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetParameterKeyCounts, (void* model), {
    return window.live2d_csm.ccall('csmGetParameterKeyCounts', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetParameterKeyValues, (void* model), {
    return window.live2d_csm.ccall('csmGetParameterKeyValues', 'number', ['number'], [model]);
});

static EM_JS(int, live2dGetPartCount, (void* model), {
    return window.live2d_csm.ccall('csmGetPartCount', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetPartIds, (void* model), {
    return window.live2d_csm.ccall('csmGetPartIds', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetPartOpacities, (csmModel* model), {
    return window.live2d_csm.ccall('csmGetPartOpacities', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetPartParentPartIndices, (void* model), {
    return window.live2d_csm.ccall('csmGetPartParentPartIndices', 'number', ['number'], [model]);
});

static EM_JS(int, live2dGetDrawableCount, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableCount', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableIds, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableIds', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableConstantFlags, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableConstantFlags', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableDynamicFlags, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableDynamicFlags', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableTextureIndices, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableTextureIndices', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableDrawOrders, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableDrawOrders', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableRenderOrders, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableRenderOrders', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableOpacities, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableOpacities', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableMaskCounts, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableMaskCounts', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableMasks, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableMasks', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableVertexCounts, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableVertexCounts', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableVertexPositions, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableVertexPositions', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableVertexUvs, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableVertexUvs', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableIndexCounts, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableIndexCounts', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableIndices, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableIndices', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableMultiplyColors, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableMultiplyColors', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableScreenColors, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableScreenColors', 'number', ['number'], [model]);
});

static EM_JS(void*, live2dGetDrawableParentPartIndices, (void* model), {
    return window.live2d_csm.ccall('csmGetDrawableParentPartIndices', 'number', ['number'], [model]);
});

static EM_JS(void, live2dResetDrawableDynamicFlags, (void* model), {
    window.live2d_csm.ccall('csmResetDrawableDynamicFlags', null, ['number'], [model]);
});

static EM_JS(void*, live2dMallocMoc, (unsigned int size), {
    return window.live2d_csm.ccall('csmMallocMoc', 'number', ['number'], [size]);
});

static EM_JS(void *, live2dMallocModel, (void *model), {
    return window.live2d_csm.ccall('csmMallocModelAndInitialize', 'number', ['number'], [model]);
});

static EM_JS(void, live2dFree, (void* moc), {
    window.live2d_csm.ccall('csmFree', null, ['number'], [moc]);
});


// Our utility functions.

// Copy data from the main heap to the Live2D WebAssembly heap.
static EM_JS(void, copyToLive2d, (void *source, void *wasm_destination, unsigned int size), {
    const source = HEAPU8.subarray(source, source + size);
    window.live2d_csm.HEAPU8.set(source, wasm_destination);
);

static EM_JS(void, copyFromLive2d, (void *wasm_source, void *destination, unsigned int size), {
    const source = window.live2d_csm.HEAPU8.subarray(wasm_source, wasm_source + size);
    HEAPU8.set(source, destination);
});


// Our CSM function implementations.

static csmVersion csmGetVersion() {
    return live2dGetVersion();
}

static csmMocVersion csmGetLatestMocVersion() {
    return live2dGetLatestMocVersion();
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

static void csmReadCanvasInfo(void* model, csmVector2* outSizeInPixels, csmVector2* outOriginInPixels, float* outPixelsPerUnit) {
}

static int csmGetParameterCount(void* model) {
    return 0;
}

static const char** csmGetParameterIds(void* model) {
    return NULL;
}

static const csmParameterType* csmGetParameterTypes(void* model) {
    return NULL;
}

static const float* csmGetParameterMinimumValues(void* model) {
    return NULL;
}

static const float* csmGetParameterMaximumValues(void* model) {
    return NULL;
}

static const float* csmGetParameterDefaultValues(void* model) {
    return NULL;
}

static float* csmGetParameterValues(csmModel* model) {
    return NULL;
}

static const int* csmGetParameterRepeats(void* model) {
    return NULL;
}

static const int* csmGetParameterKeyCounts(void* model) {
    return NULL;
}

static const float** csmGetParameterKeyValues(void* model) {
    return NULL;
}

static int csmGetPartCount(void* model) {
    return 0;
}

static const char** csmGetPartIds(void* model) {
    return NULL;
}

static float* csmGetPartOpacities(csmModel* model) {
    return NULL;
}

static const int* csmGetPartParentPartIndices(void* model) {
    return NULL;
}

static int csmGetDrawableCount(void* model) {
    return 0;
}

static const char** csmGetDrawableIds(void* model) {
    return NULL;
}

static const csmFlags* csmGetDrawableConstantFlags(void* model) {
    return NULL;
}

static const csmFlags* csmGetDrawableDynamicFlags(void* model) {
    return NULL;
}

static const int* csmGetDrawableTextureIndices(void* model) {
    return NULL;
}

static const int* csmGetDrawableDrawOrders(void* model) {
    return NULL;
}

static const int* csmGetDrawableRenderOrders(void* model) {
    return NULL;
}

static const float* csmGetDrawableOpacities(void* model) {
    return NULL;
}

static const int* csmGetDrawableMaskCounts(void* model) {
    return NULL;
}

static const int** csmGetDrawableMasks(void* model) {
    return NULL;
}

static const int* csmGetDrawableVertexCounts(void* model) {
    return NULL;
}

static const csmVector2** csmGetDrawableVertexPositions(void* model) {
    return NULL;
}

static const csmVector2** csmGetDrawableVertexUvs(void* model) {
    return NULL;
}

static const int* csmGetDrawableIndexCounts(void* model) {
    return NULL;
}

static const unsigned short** csmGetDrawableIndices(void* model) {
    return NULL;
}

static const csmVector4* csmGetDrawableMultiplyColors(void* model) {
    return NULL;
}

static const csmVector4* csmGetDrawableScreenColors(void* model) {
    return NULL;
}

static const int* csmGetDrawableParentPartIndices(void* model) {
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
