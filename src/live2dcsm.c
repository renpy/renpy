#include "live2dcsm.h"
#include <SDL3/SDL.h>
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
    window.live2d_csm.ccall('csmUpdateModel', null, ['number'], [model]);
});

static EM_JS(void, live2dReadCanvasInfo, (void* model, void *outSizeInPixels, void* outOriginInPixels, void* outPixelsPerUnit), {
    window.live2d_csm.ccall("csmReadCanvasInfo", null, ["number", "number", "number", "number"], [model, outSizeInPixels, outOriginInPixels, outPixelsPerUnit]);
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

static EM_JS(void *, live2dMallocModelAndInitialize, (void *moc), {
    return window.live2d_csm.ccall('csmMallocModelAndInitialize', 'number', ['number'], [moc]);
});

static EM_JS(void *, live2dMalloc, (unsigned int size), {
    return window.live2d_csm.ccall('csmMalloc', 'number', ['number'], [size]);
});

static EM_JS(void, live2dFree, (void* moc), {
    window.live2d_csm.ccall('csmFree', null, ['number'], [moc]);
});


// Our utility functions.

// Copy data from the main heap to the Live2D WebAssembly heap.
static EM_JS(void, copyToLive2d, (const void *source, void *live2d_destination, unsigned int size), {
    const data = HEAPU8.subarray(source, source + size);
    window.live2d_csm.HEAPU8.set(data, live2d_destination);
});

static EM_JS(void, copyFromLive2d, (const void *live2d_source, void *destination, unsigned int size), {
    const data = window.live2d_csm.HEAPU8.subarray(live2d_source, live2d_source + size);
    HEAPU8.set(data, destination);
});


typedef struct MocProxy {
    // This is 0x42424242 if the Moc has been proxied.
    unsigned int flag;

    // The address of the Moc in live2d.
    void *live2d_moc_data;

    // The address of the Moc in live2d, if it's been revived.
    void *live2d_moc;

    // The address of the Moc in Ren'Py.
    void *renpy_moc_data;

    // The size of the Moc in bytes.
    unsigned int size;

} MocProxy;



typedef struct ModelProxy {

    // The MocProxy associated with this model.
    const MocProxy *moc_proxy;

    // The address of the model, in live2d.
    void *live2d_model;

    // The address of the copy of the model stored by Ren'Py.
    void *renpy_model;

    // The size of the model.
    unsigned int size;

    // The number of parameters
    int parameter_count;
    const char **renpy_parameter_ids;
    const csmParameterType *renpy_parameter_types;
    const float *renpy_parameter_minimum_values;
    const float *renpy_parameter_maximum_values;
    const float *renpy_parameter_default_values;
    void *live2d_parameter_values;
    float *renpy_parameter_values;
    const int *renpy_parameter_repeats;
    const int *renpy_parameter_key_counts;
    const float **renpy_parameter_key_values;
    int part_count;
    const char **renpy_part_ids;
    void *live2d_part_opacities;
    float *renpy_part_opacities;
    const int *renpy_part_parent_part_indices;
    int drawable_count;
    const char **renpy_drawable_ids;
    const csmFlags *renpy_drawable_constant_flags;
    void *live2d_drawable_dynamic_flags;
    csmFlags *renpy_drawable_dynamic_flags;
    const int *renpy_drawable_texture_indices;
    const int *renpy_drawable_draw_orders;
    const int *renpy_drawable_render_orders;
    const float *renpy_drawable_opacities;
    const int *renpy_drawable_mask_counts;
    const int **renpy_drawable_masks;
    const int *renpy_drawable_vertex_counts;
    const csmVector2 **renpy_drawable_vertex_positions;
    const csmVector2 **renpy_drawable_vertex_uvs;
    const int *renpy_drawable_index_counts;
    const unsigned short **renpy_drawable_indices;
    const csmVector4 *renpy_drawable_multiply_colors;
    const csmVector4 *renpy_drawable_screen_colors;
    const int *renpy_drawable_parent_part_indices;
} ModelProxy;


/**
 * Given a pointer to a Moc in memory, copyies the data over to the live2d heap if it
 * hasn't been already, copies some information into the allocated data, and returns
 * the pointer cast to the MocProxy structure.
 */
static MocProxy* toMocProxy(void *address, unsigned int size) {

    MocProxy *proxy = (MocProxy *) address;
    if (proxy->flag == 0x42424242) {
        return proxy;
    }

    void *wasm_moc = live2dMallocMoc(size);
    copyToLive2d(address, wasm_moc, size);

    proxy->flag = 0x42424242;
    proxy->live2d_moc_data = wasm_moc;
    proxy->live2d_moc = NULL;
    proxy->renpy_moc_data = address;
    proxy->size = size;

    return proxy;
}

static ModelProxy *toModelProxy(csmModel *address) {
    ModelProxy *proxy = (ModelProxy *) address;
    return proxy;
}

static void *pointerFromLive2d(ModelProxy *model, const void *address) {
    if (!address) {
        return NULL;
    }

    if (model->live2d_model <= address && address < model->live2d_model + model->size) {
        return address - model->live2d_model + model->renpy_model;
    }

    const MocProxy *moc = model->moc_proxy;

    if (moc->live2d_moc_data <= address && address < moc->live2d_moc_data + moc->size) {
        return address - moc->live2d_moc_data + moc->renpy_moc_data;
    }

    fprintf(stderr, "Error: Address %p is not in the model or moc memory.\n", address);
    return NULL;
}

static void **pointerListFromLive2d(ModelProxy *model, const void *address, unsigned int size) {
    if (!address || size == 0) {
        return NULL;
    }

    void **source = (void **) pointerFromLive2d(model, address);
    void **result = (void **) malloc(size * sizeof(void *));

    for (unsigned int i = 0; i < size; i++) {
        result[i] = pointerFromLive2d(model, source[i]);
    }

    return result;
};

// Our CSM function implementations.

static csmVersion csmGetVersion() {
    return live2dGetVersion();
}

static csmMocVersion csmGetLatestMocVersion() {
    return live2dGetLatestMocVersion();
}

static csmMocVersion csmGetMocVersion(const void* address, const unsigned int size) {
    MocProxy *proxy = toMocProxy((void *) address, size);

    return live2dGetMocVersion(proxy->live2d_moc, proxy->size);
}

static int csmHasMocConsistency(void* address, const unsigned int size) {
    MocProxy *proxy = toMocProxy(address, size);
    return live2dHasMocConsistency(proxy->live2d_moc_data, proxy->size);
}

static csmLogFunction csmGetLogFunction() {
    return NULL;
}

static void csmSetLogFunction(csmLogFunction handler) {
}

static csmMoc* csmReviveMocInPlace(void* address, const unsigned int size) {
    MocProxy *proxy = toMocProxy(address, size);

    if (proxy->live2d_moc) {
        return (csmMoc *) proxy;
    }

    proxy->live2d_moc = live2dReviveMocInPlace(proxy->live2d_moc_data, proxy->size);
    if (proxy->live2d_moc == NULL) {
        return NULL;
    }

    proxy->renpy_moc_data = malloc(proxy->size);
    copyFromLive2d(proxy->live2d_moc_data, proxy->renpy_moc_data, proxy->size);

    return (csmMoc *) proxy;
}

static unsigned int csmGetSizeofModel(const csmMoc* moc) {
    return sizeof(ModelProxy);
}

static csmModel* csmInitializeModelInPlace(const csmMoc* moc, void* address, const unsigned int size) {
    const MocProxy *moc_proxy = (const MocProxy *) moc;
    ModelProxy *proxy = (ModelProxy *) address;

    memset(proxy, 0, sizeof(ModelProxy));

    proxy->moc_proxy = moc_proxy;
    proxy->size = live2dGetSizeofModel(moc_proxy->live2d_moc);
    proxy->live2d_model = live2dMallocModelAndInitialize(moc_proxy->live2d_moc);
    proxy->renpy_model = malloc(proxy->size);
    copyFromLive2d(proxy->live2d_model, proxy->renpy_model, proxy->size);

    proxy->parameter_count = live2dGetParameterCount(proxy->live2d_model);
    proxy->renpy_parameter_ids = (const char **) pointerListFromLive2d(proxy, live2dGetParameterIds(proxy->live2d_model), proxy->parameter_count);
    proxy->renpy_parameter_types = (const csmParameterType *) pointerFromLive2d(proxy, live2dGetParameterTypes(proxy->live2d_model));
    proxy->renpy_parameter_minimum_values = (const float *) pointerFromLive2d(proxy, live2dGetParameterMinimumValues(proxy->live2d_model));
    proxy->renpy_parameter_maximum_values = (const float *) pointerFromLive2d(proxy, live2dGetParameterMaximumValues(proxy->live2d_model));
    proxy->renpy_parameter_default_values = (const float *) pointerFromLive2d(proxy, live2dGetParameterDefaultValues(proxy->live2d_model));
    proxy->live2d_parameter_values = live2dGetParameterValues(proxy->live2d_model);
    proxy->renpy_parameter_values = (float *) pointerFromLive2d(proxy, proxy->live2d_parameter_values);
    proxy->renpy_parameter_repeats = (const int *) pointerFromLive2d(proxy, live2dGetParameterRepeats(proxy->live2d_model));
    proxy->renpy_parameter_key_counts = (const int *) pointerFromLive2d(proxy, live2dGetParameterKeyCounts(proxy->live2d_model));
    proxy->renpy_parameter_key_values = (const float **) pointerListFromLive2d(proxy, live2dGetParameterKeyValues(proxy->live2d_model), proxy->parameter_count);
    proxy->part_count = live2dGetPartCount(proxy->live2d_model);
    proxy->renpy_part_ids = (const char **) pointerListFromLive2d(proxy, live2dGetPartIds(proxy->live2d_model), proxy->part_count);
    proxy->live2d_part_opacities = live2dGetPartOpacities(proxy->live2d_model);
    proxy->renpy_part_opacities = (float *) pointerFromLive2d(proxy, proxy->live2d_part_opacities);
    proxy->renpy_part_parent_part_indices = (const int *) pointerFromLive2d(proxy, live2dGetPartParentPartIndices(proxy->live2d_model));
    proxy->drawable_count = live2dGetDrawableCount(proxy->live2d_model);
    proxy->renpy_drawable_ids = (const char **) pointerListFromLive2d(proxy, live2dGetDrawableIds(proxy->live2d_model), proxy->drawable_count);
    proxy->renpy_drawable_constant_flags = (const csmFlags *) pointerFromLive2d(proxy, live2dGetDrawableConstantFlags(proxy->live2d_model));
    proxy->live2d_drawable_dynamic_flags = live2dGetDrawableDynamicFlags(proxy->live2d_model);
    proxy->renpy_drawable_dynamic_flags = (const csmFlags *) pointerFromLive2d(proxy, proxy->live2d_drawable_dynamic_flags);
    proxy->renpy_drawable_texture_indices = (const int *) pointerFromLive2d(proxy, live2dGetDrawableTextureIndices(proxy->live2d_model));
    proxy->renpy_drawable_draw_orders = (const int *) pointerFromLive2d(proxy, live2dGetDrawableDrawOrders(proxy->live2d_model));
    proxy->renpy_drawable_render_orders = (const int *) pointerFromLive2d(proxy, live2dGetDrawableRenderOrders(proxy->live2d_model));
    proxy->renpy_drawable_opacities = (const float *) pointerFromLive2d(proxy, live2dGetDrawableOpacities(proxy->live2d_model));
    proxy->renpy_drawable_mask_counts = (const int *) pointerFromLive2d(proxy, live2dGetDrawableMaskCounts(proxy->live2d_model));
    proxy->renpy_drawable_masks = (const int **) pointerListFromLive2d(proxy, live2dGetDrawableMasks(proxy->live2d_model), proxy->drawable_count);
    proxy->renpy_drawable_vertex_counts = (const int *) pointerFromLive2d(proxy, live2dGetDrawableVertexCounts(proxy->live2d_model));
    proxy->renpy_drawable_vertex_positions = (const csmVector2 **) pointerListFromLive2d(proxy, live2dGetDrawableVertexPositions(proxy->live2d_model), proxy->drawable_count);
    proxy->renpy_drawable_vertex_uvs = (const csmVector2 **) pointerListFromLive2d(proxy, live2dGetDrawableVertexUvs(proxy->live2d_model), proxy->drawable_count);
    proxy->renpy_drawable_index_counts = (const int *) pointerFromLive2d(proxy, live2dGetDrawableIndexCounts(proxy->live2d_model));
    proxy->renpy_drawable_indices = (const unsigned short **) pointerListFromLive2d(proxy, live2dGetDrawableIndices(proxy->live2d_model), proxy->drawable_count);
    proxy->renpy_drawable_multiply_colors = (const csmVector4 *) pointerFromLive2d(proxy, live2dGetDrawableMultiplyColors(proxy->live2d_model));
    proxy->renpy_drawable_screen_colors = (const csmVector4 *) pointerFromLive2d(proxy, live2dGetDrawableScreenColors(proxy->live2d_model));
    proxy->renpy_drawable_parent_part_indices = (const int *) pointerFromLive2d(proxy, live2dGetDrawableParentPartIndices(proxy->live2d_model));

    return (csmModel *) proxy;
}

static void csmUpdateModel(csmModel* model) {
    ModelProxy *proxy = toModelProxy(model);

    copyToLive2d(proxy->renpy_parameter_values, proxy->live2d_parameter_values, sizeof(float) * proxy->parameter_count);
    copyToLive2d(proxy->renpy_part_opacities, proxy->live2d_part_opacities, sizeof(float) * proxy->part_count);
    live2dUpdateModel(proxy->live2d_model);
    copyFromLive2d(proxy->live2d_model, proxy->renpy_model, proxy->size);
}

static void csmReadCanvasInfo(csmModel* model, csmVector2* outSizeInPixels, csmVector2* outOriginInPixels, float* outPixelsPerUnit) {
    float results[5];
    void *live2dResults = live2dMalloc(sizeof(float) * 5);

    live2dReadCanvasInfo(
        toModelProxy(model)->live2d_model,
        live2dResults,
        live2dResults + sizeof(float) * 2,
        live2dResults + sizeof(float) * 4
    );

    copyFromLive2d(live2dResults, results, sizeof(float) * 5);
    live2dFree(live2dResults);

    outSizeInPixels->x = results[0];
    outSizeInPixels->y = results[1];
    outOriginInPixels->x = results[2];
    outOriginInPixels->y = results[3];
    *outPixelsPerUnit = results[4];
}

static int csmGetParameterCount(csmModel* model) {\
    ModelProxy *proxy = toModelProxy(model);
    return proxy->parameter_count;
}

static const char** csmGetParameterIds(csmModel* model) {
    return toModelProxy(model)->renpy_parameter_ids;
}

static const csmParameterType* csmGetParameterTypes(csmModel* model) {
    return toModelProxy(model)->renpy_parameter_types;
}

static const float* csmGetParameterMinimumValues(csmModel* model) {
    return toModelProxy(model)->renpy_parameter_minimum_values;
}

static const float* csmGetParameterMaximumValues(csmModel* model) {
    return toModelProxy(model)->renpy_parameter_maximum_values;
}

static const float* csmGetParameterDefaultValues(csmModel* model) {
    return toModelProxy(model)->renpy_parameter_default_values;
}

static float* csmGetParameterValues(csmModel* model) {
    return toModelProxy(model)->renpy_parameter_values;
}

static const int* csmGetParameterRepeats(csmModel* model) {
    return toModelProxy(model)->renpy_parameter_repeats;
}

static const int* csmGetParameterKeyCounts(csmModel* model) {
    return toModelProxy(model)->renpy_parameter_key_counts;
}

static const float** csmGetParameterKeyValues(csmModel* model) {
    return toModelProxy(model)->renpy_parameter_key_values;
}

static int csmGetPartCount(csmModel* model) {
    return toModelProxy(model)->part_count;
}

static const char** csmGetPartIds(csmModel* model) {
    return toModelProxy(model)->renpy_part_ids;
}

static float* csmGetPartOpacities(csmModel* model) {
    return toModelProxy(model)->renpy_part_opacities;
}

static const int* csmGetPartParentPartIndices(csmModel* model) {
    return toModelProxy(model)->renpy_part_parent_part_indices;
}

static int csmGetDrawableCount(csmModel* model) {
    return toModelProxy(model)->drawable_count;
}

static const char** csmGetDrawableIds(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_ids;
}

static const csmFlags* csmGetDrawableConstantFlags(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_constant_flags;
}

static const csmFlags* csmGetDrawableDynamicFlags(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_dynamic_flags;
}

static const int* csmGetDrawableTextureIndices(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_texture_indices;
}

static const int* csmGetDrawableDrawOrders(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_draw_orders;
}

static const int* csmGetDrawableRenderOrders(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_render_orders;
}

static const float* csmGetDrawableOpacities(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_opacities;
}

static const int* csmGetDrawableMaskCounts(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_mask_counts;
}

static const int** csmGetDrawableMasks(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_masks;
}

static const int* csmGetDrawableVertexCounts(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_vertex_counts;
}

static const csmVector2** csmGetDrawableVertexPositions(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_vertex_positions;
}

static const csmVector2** csmGetDrawableVertexUvs(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_vertex_uvs;
}

static const int* csmGetDrawableIndexCounts(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_index_counts;
}

static const unsigned short** csmGetDrawableIndices(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_indices;
}

static const csmVector4* csmGetDrawableMultiplyColors(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_multiply_colors;
}

static const csmVector4* csmGetDrawableScreenColors(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_screen_colors;
}

static const int* csmGetDrawableParentPartIndices(csmModel* model) {
    return toModelProxy(model)->renpy_drawable_parent_part_indices;
}

static void csmResetDrawableDynamicFlags(csmModel* model) {
    ModelProxy *proxy = toModelProxy(model);
    live2dResetDrawableDynamicFlags((void *) proxy->live2d_model);
    copyFromLive2d(proxy->live2d_drawable_dynamic_flags, proxy->renpy_drawable_dynamic_flags, proxy->drawable_count * sizeof(csmFlags));
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
    MocProxy *proxy = toMocProxy((void *) moc, 0);

    live2dFree(proxy->live2d_moc_data);
    free(proxy->renpy_moc_data);
}

void deallocate_live2d_model(void *model) {

    ModelProxy *proxy = toModelProxy((csmModel *) model);

    live2dFree(proxy->live2d_model);
    free(proxy->renpy_model);

    free(proxy->renpy_parameter_ids);
    free(proxy->renpy_parameter_key_values);
    free(proxy->renpy_part_ids);
    free(proxy->renpy_drawable_ids);
    free(proxy->renpy_drawable_masks);
    free(proxy->renpy_drawable_vertex_positions);
    free(proxy->renpy_drawable_vertex_uvs);
    free(proxy->renpy_drawable_indices);
}

#endif
