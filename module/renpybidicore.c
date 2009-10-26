#include <Python.h>
#include <alloca.h>
#include <fribidi/fribidi.h>


PyObject *renpybidi_log2vis(PyObject *s, int *direction) {
    char *src;
    int size;
    FriBidiChar *srcuni;
    int unisize;
    FriBidiChar *dstuni;
    char *dst;
    

    
    int i;
    
    src = PyString_AsString(s);

    if (src == NULL) {
        return NULL;
    }

    size = PyString_Size(s);

    srcuni = (FriBidiChar *) alloca(size * 4);
    dstuni = (FriBidiChar *) alloca(size * 4);
    dst = (char *) alloca(size * 4);
    
    unisize = fribidi_charset_to_unicode(FRIBIDI_CHAR_SET_UTF8, src, size, srcuni);

    fribidi_log2vis(
        srcuni,
        unisize,
        direction,
        dstuni,
        NULL,
        NULL,
        NULL);

    fribidi_unicode_to_charset(FRIBIDI_CHAR_SET_UTF8, dstuni, unisize, dst);

    return PyString_FromString(dst);
}
