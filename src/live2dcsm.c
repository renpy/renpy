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

// Emscripten implementations with empty function bodies

csmVersion csmGetVersion() {
    return 0;
}

csmMocVersion csmGetLatestMocVersion() {
    return 0;
}

csmMocVersion csmGetMocVersion(const void* address, const unsigned int size) {
    return 0;
}

int csmHasMocConsistency(void* address, const unsigned int size) {
    return 0;
}

csmLogFunction csmGetLogFunction() {
    return NULL;
}

void csmSetLogFunction(csmLogFunction handler) {
}

csmMoc* csmReviveMocInPlace(void* address, const unsigned int size) {
    return NULL;
}

unsigned int csmGetSizeofModel(const csmMoc* moc) {
    return 0;
}

csmModel* csmInitializeModelInPlace(const csmMoc* moc, void* address, const unsigned int size) {
    return NULL;
}

void csmUpdateModel(csmModel* model) {
}

void csmReadCanvasInfo(const csmModel* model, csmVector2* outSizeInPixels, csmVector2* outOriginInPixels, float* outPixelsPerUnit) {
}

int csmGetParameterCount(const csmModel* model) {
    return 0;
}

const char** csmGetParameterIds(const csmModel* model) {
    return NULL;
}

const csmParameterType* csmGetParameterTypes(const csmModel* model) {
    return NULL;
}

const float* csmGetParameterMinimumValues(const csmModel* model) {
    return NULL;
}

const float* csmGetParameterMaximumValues(const csmModel* model) {
    return NULL;
}

const float* csmGetParameterDefaultValues(const csmModel* model) {
    return NULL;
}

float* csmGetParameterValues(csmModel* model) {
    return NULL;
}

const int* csmGetParameterRepeats(const csmModel* model) {
    return NULL;
}

const int* csmGetParameterKeyCounts(const csmModel* model) {
    return NULL;
}

const float** csmGetParameterKeyValues(const csmModel* model) {
    return NULL;
}

int csmGetPartCount(const csmModel* model) {
    return 0;
}

const char** csmGetPartIds(const csmModel* model) {
    return NULL;
}

float* csmGetPartOpacities(csmModel* model) {
    return NULL;
}

const int* csmGetPartParentPartIndices(const csmModel* model) {
    return NULL;
}

int csmGetDrawableCount(const csmModel* model) {
    return 0;
}

const char** csmGetDrawableIds(const csmModel* model) {
    return NULL;
}

const csmFlags* csmGetDrawableConstantFlags(const csmModel* model) {
    return NULL;
}

const csmFlags* csmGetDrawableDynamicFlags(const csmModel* model) {
    return NULL;
}

const int* csmGetDrawableTextureIndices(const csmModel* model) {
    return NULL;
}

const int* csmGetDrawableDrawOrders(const csmModel* model) {
    return NULL;
}

const int* csmGetDrawableRenderOrders(const csmModel* model) {
    return NULL;
}

const float* csmGetDrawableOpacities(const csmModel* model) {
    return NULL;
}

const int* csmGetDrawableMaskCounts(const csmModel* model) {
    return NULL;
}

const int** csmGetDrawableMasks(const csmModel* model) {
    return NULL;
}

const int* csmGetDrawableVertexCounts(const csmModel* model) {
    return NULL;
}

const csmVector2** csmGetDrawableVertexPositions(const csmModel* model) {
    return NULL;
}

const csmVector2** csmGetDrawableVertexUvs(const csmModel* model) {
    return NULL;
}

const int* csmGetDrawableIndexCounts(const csmModel* model) {
    return NULL;
}

const unsigned short** csmGetDrawableIndices(const csmModel* model) {
    return NULL;
}

const csmVector4* csmGetDrawableMultiplyColors(const csmModel* model) {
    return NULL;
}

const csmVector4* csmGetDrawableScreenColors(const csmModel* model) {
    return NULL;
}

const int* csmGetDrawableParentPartIndices(const csmModel* model) {
    return NULL;
}

void csmResetDrawableDynamicFlags(csmModel* model) {
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
