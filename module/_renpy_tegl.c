/* _renpy_tegl.c */

#define GL_GLEXT_PROTOTYPES

#include <Python.h>
#include <structmember.h>
#include <GL/glew.h>
#include <GL/glu.h>

static char ARGCOUNT[] = "wrong number of arguments";

static PyObject* teglClearIndex(PyObject* self, PyObject* obj) {
    double val;
    val = PyFloat_AsDouble(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glClearIndex(val);
    Py_RETURN_NONE;
}

static PyObject* teglClearColor(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glClearColor(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglClear(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glClear(val);
    Py_RETURN_NONE;
}

static PyObject* teglIndexMask(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glIndexMask(val);
    Py_RETURN_NONE;
}

static PyObject* teglColorMask(PyObject* self, PyObject* args) {
    int val0;
    int val1;
    int val2;
    int val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyObject_IsTrue(PyTuple_GET_ITEM(args,0));
    if (val0 == -1) return 0;
    val1 = PyObject_IsTrue(PyTuple_GET_ITEM(args,1));
    if (val1 == -1) return 0;
    val2 = PyObject_IsTrue(PyTuple_GET_ITEM(args,2));
    if (val2 == -1) return 0;
    val3 = PyObject_IsTrue(PyTuple_GET_ITEM(args,3));
    if (val3 == -1) return 0;
    glColorMask(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglAlphaFunc(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glAlphaFunc(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglBlendFunc(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glBlendFunc(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglLogicOp(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glLogicOp(val);
    Py_RETURN_NONE;
}

static PyObject* teglCullFace(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glCullFace(val);
    Py_RETURN_NONE;
}

static PyObject* teglFrontFace(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glFrontFace(val);
    Py_RETURN_NONE;
}

static PyObject* teglPointSize(PyObject* self, PyObject* obj) {
    double val;
    val = PyFloat_AsDouble(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glPointSize(val);
    Py_RETURN_NONE;
}

static PyObject* teglLineWidth(PyObject* self, PyObject* obj) {
    double val;
    val = PyFloat_AsDouble(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glLineWidth(val);
    Py_RETURN_NONE;
}

static PyObject* teglLineStipple(PyObject* self, PyObject* args) {
    long val0;
    unsigned long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glLineStipple(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglPolygonMode(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glPolygonMode(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglPolygonOffset(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glPolygonOffset(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglPolygonStipple(PyObject* self, PyObject* obj) {
    const void* val;
    Py_ssize_t buflen;
    if(PyObject_AsReadBuffer(obj,&val,&buflen) == -1)
        return 0;
    glPolygonStipple(val);
    Py_RETURN_NONE;
}

static PyObject* teglGetPolygonStipple(PyObject* self, PyObject* obj) {
    void* val;
    Py_ssize_t buflen;
    if(PyObject_AsWriteBuffer(obj,&val,&buflen) == -1)
        return 0;
    glGetPolygonStipple(val);
    Py_RETURN_NONE;
}

static PyObject* teglEdgeFlag(PyObject* self, PyObject* obj) {
    int val;
    val = PyObject_IsTrue(obj);
    if (val == -1) return 0;
    glEdgeFlag(val);
    Py_RETURN_NONE;
}

static PyObject* teglEdgeFlagv(PyObject* self, PyObject* obj) {
    GLboolean val[1];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyObject_IsTrue(q);
        fail = (t == -1);
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glEdgeFlagv(val);
    Py_RETURN_NONE;
}

static PyObject* teglScissor(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glScissor(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglClipPlane(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLdouble val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glClipPlane(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglGetClipPlane(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLdouble val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetClipPlane(val0,val1);
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val1[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglDrawBuffer(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glDrawBuffer(val);
    Py_RETURN_NONE;
}

static PyObject* teglReadBuffer(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glReadBuffer(val);
    Py_RETURN_NONE;
}

static PyObject* teglEnable(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glEnable(val);
    Py_RETURN_NONE;
}

static PyObject* teglDisable(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glDisable(val);
    Py_RETURN_NONE;
}

static PyObject* teglIsEnabled(PyObject* self, PyObject* obj) {
    unsigned long val;
    int r;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    r = glIsEnabled(val);
    return PyBool_FromLong(r);
}

static PyObject* teglEnableClientState(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glEnableClientState(val);
    Py_RETURN_NONE;
}

static PyObject* teglDisableClientState(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glDisableClientState(val);
    Py_RETURN_NONE;
}

static PyObject* teglGetBooleanv(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLboolean val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetBooleanv(val0,val1);
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyBool_FromLong(val1[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetDoublev(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLdouble val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetDoublev(val0,val1);
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val1[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetFloatv(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLfloat val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetFloatv(val0,val1);
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val1[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetIntegerv(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLint val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetIntegerv(val0,val1);
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val1[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglPushAttrib(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glPushAttrib(val);
    Py_RETURN_NONE;
}

static PyObject* teglPopAttrib(PyObject* self) {
    glPopAttrib();
    Py_RETURN_NONE;
}

static PyObject* teglPushClientAttrib(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glPushClientAttrib(val);
    Py_RETURN_NONE;
}

static PyObject* teglPopClientAttrib(PyObject* self) {
    glPopClientAttrib();
    Py_RETURN_NONE;
}

static PyObject* teglRenderMode(PyObject* self, PyObject* obj) {
    unsigned long val;
    long r;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    r = glRenderMode(val);

    return PyInt_FromLong(r);
}

static PyObject* teglGetError(PyObject* self) {
    unsigned long r;
    r = glGetError();
    return PyLong_FromUnsignedLong(r);
}

static PyObject* teglFinish(PyObject* self) {
    glFinish();
    Py_RETURN_NONE;
}

static PyObject* teglFlush(PyObject* self) {
    glFlush();
    Py_RETURN_NONE;
}

static PyObject* teglHint(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glHint(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglClearDepth(PyObject* self, PyObject* obj) {
    double val;
    val = PyFloat_AsDouble(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glClearDepth(val);
    Py_RETURN_NONE;
}

static PyObject* teglDepthFunc(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glDepthFunc(val);
    Py_RETURN_NONE;
}

static PyObject* teglDepthMask(PyObject* self, PyObject* obj) {
    int val;
    val = PyObject_IsTrue(obj);
    if (val == -1) return 0;
    glDepthMask(val);
    Py_RETURN_NONE;
}

static PyObject* teglDepthRange(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glDepthRange(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglClearAccum(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glClearAccum(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglAccum(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glAccum(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMatrixMode(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glMatrixMode(val);
    Py_RETURN_NONE;
}

static PyObject* teglOrtho(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    double val4;
    double val5;
    if (PyTuple_GET_SIZE(args) != 6) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    glOrtho(val0,val1,val2,val3,val4,val5);
    Py_RETURN_NONE;
}

static PyObject* teglFrustum(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    double val4;
    double val5;
    if (PyTuple_GET_SIZE(args) != 6) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    glFrustum(val0,val1,val2,val3,val4,val5);
    Py_RETURN_NONE;
}

static PyObject* teglViewport(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glViewport(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglPushMatrix(PyObject* self) {
    glPushMatrix();
    Py_RETURN_NONE;
}

static PyObject* teglPopMatrix(PyObject* self) {
    glPopMatrix();
    Py_RETURN_NONE;
}

static PyObject* teglLoadIdentity(PyObject* self) {
    glLoadIdentity();
    Py_RETURN_NONE;
}

static PyObject* teglLoadMatrixd(PyObject* self, PyObject* obj) {
    GLdouble val[16];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glLoadMatrixd(val);
    Py_RETURN_NONE;
}

static PyObject* teglLoadMatrixf(PyObject* self, PyObject* obj) {
    GLfloat val[16];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glLoadMatrixf(val);
    Py_RETURN_NONE;
}

static PyObject* teglMultMatrixd(PyObject* self, PyObject* obj) {
    GLdouble val[16];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glMultMatrixd(val);
    Py_RETURN_NONE;
}

static PyObject* teglMultMatrixf(PyObject* self, PyObject* obj) {
    GLfloat val[16];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glMultMatrixf(val);
    Py_RETURN_NONE;
}

static PyObject* teglRotated(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glRotated(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglRotatef(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glRotatef(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglScaled(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glScaled(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglScalef(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glScalef(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTranslated(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTranslated(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTranslatef(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTranslatef(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglIsList(PyObject* self, PyObject* obj) {
    unsigned long val;
    int r;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    r = glIsList(val);
    return PyBool_FromLong(r);
}

static PyObject* teglDeleteLists(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glDeleteLists(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglGenLists(PyObject* self, PyObject* obj) {
    long val;
    unsigned long r;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    r = glGenLists(val);
    return PyLong_FromUnsignedLong(r);
}

static PyObject* teglNewList(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glNewList(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglEndList(PyObject* self) {
    glEndList();
    Py_RETURN_NONE;
}

static PyObject* teglCallList(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glCallList(val);
    Py_RETURN_NONE;
}

static PyObject* teglCallLists(PyObject* self, PyObject* args) {
    long val0;
    unsigned long val1;
    const void* val2;
    Py_ssize_t buflen2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    glCallLists(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglListBase(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glListBase(val);
    Py_RETURN_NONE;
}

static PyObject* teglBegin(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glBegin(val);
    Py_RETURN_NONE;
}

static PyObject* teglEnd(PyObject* self) {
    glEnd();
    Py_RETURN_NONE;
}

static PyObject* teglVertex2d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glVertex2d(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglVertex2f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glVertex2f(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglVertex2i(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glVertex2i(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglVertex2s(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glVertex2s(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglVertex3d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glVertex3d(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglVertex3f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glVertex3f(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglVertex3i(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glVertex3i(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglVertex3s(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glVertex3s(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglVertex4d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glVertex4d(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglVertex4f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glVertex4f(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglVertex4i(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glVertex4i(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglVertex4s(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glVertex4s(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglVertex2dv(PyObject* self, PyObject* obj) {
    GLdouble val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glVertex2dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglVertex2fv(PyObject* self, PyObject* obj) {
    GLfloat val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glVertex2fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglVertex2iv(PyObject* self, PyObject* obj) {
    GLint val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glVertex2iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglVertex2sv(PyObject* self, PyObject* obj) {
    GLshort val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glVertex2sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglVertex3dv(PyObject* self, PyObject* obj) {
    GLdouble val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glVertex3dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglVertex3fv(PyObject* self, PyObject* obj) {
    GLfloat val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glVertex3fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglVertex3iv(PyObject* self, PyObject* obj) {
    GLint val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glVertex3iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglVertex3sv(PyObject* self, PyObject* obj) {
    GLshort val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glVertex3sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglVertex4dv(PyObject* self, PyObject* obj) {
    GLdouble val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glVertex4dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglVertex4fv(PyObject* self, PyObject* obj) {
    GLfloat val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glVertex4fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglVertex4iv(PyObject* self, PyObject* obj) {
    GLint val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glVertex4iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglVertex4sv(PyObject* self, PyObject* obj) {
    GLshort val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glVertex4sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglNormal3b(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glNormal3b(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglNormal3d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glNormal3d(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglNormal3f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glNormal3f(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglNormal3i(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glNormal3i(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglNormal3s(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glNormal3s(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglNormal3bv(PyObject* self, PyObject* obj) {
    GLbyte val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glNormal3bv(val);
    Py_RETURN_NONE;
}

static PyObject* teglNormal3dv(PyObject* self, PyObject* obj) {
    GLdouble val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glNormal3dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglNormal3fv(PyObject* self, PyObject* obj) {
    GLfloat val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glNormal3fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglNormal3iv(PyObject* self, PyObject* obj) {
    GLint val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glNormal3iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglNormal3sv(PyObject* self, PyObject* obj) {
    GLshort val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glNormal3sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglIndexd(PyObject* self, PyObject* obj) {
    double val;
    val = PyFloat_AsDouble(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glIndexd(val);
    Py_RETURN_NONE;
}

static PyObject* teglIndexf(PyObject* self, PyObject* obj) {
    double val;
    val = PyFloat_AsDouble(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glIndexf(val);
    Py_RETURN_NONE;
}

static PyObject* teglIndexi(PyObject* self, PyObject* obj) {
    long val;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glIndexi(val);
    Py_RETURN_NONE;
}

static PyObject* teglIndexs(PyObject* self, PyObject* obj) {
    long val;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glIndexs(val);
    Py_RETURN_NONE;
}

static PyObject* teglIndexub(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glIndexub(val);
    Py_RETURN_NONE;
}

static PyObject* teglIndexdv(PyObject* self, PyObject* obj) {
    GLdouble val[1];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glIndexdv(val);
    Py_RETURN_NONE;
}

static PyObject* teglIndexfv(PyObject* self, PyObject* obj) {
    GLfloat val[1];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glIndexfv(val);
    Py_RETURN_NONE;
}

static PyObject* teglIndexiv(PyObject* self, PyObject* obj) {
    GLint val[1];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glIndexiv(val);
    Py_RETURN_NONE;
}

static PyObject* teglIndexsv(PyObject* self, PyObject* obj) {
    GLshort val[1];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glIndexsv(val);
    Py_RETURN_NONE;
}

static PyObject* teglIndexubv(PyObject* self, PyObject* obj) {
    GLubyte val[1];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        unsigned long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsUnsignedLongMask(q);
        fail = (t == (unsigned long)(-1) && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glIndexubv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor3b(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glColor3b(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglColor3d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glColor3d(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglColor3f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glColor3f(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglColor3i(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glColor3i(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglColor3s(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glColor3s(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglColor3ub(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    unsigned long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glColor3ub(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglColor3ui(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    unsigned long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glColor3ui(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglColor3us(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    unsigned long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glColor3us(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglColor4b(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glColor4b(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglColor4d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glColor4d(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglColor4f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glColor4f(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglColor4i(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glColor4i(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglColor4s(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glColor4s(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglColor4ub(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    unsigned long val2;
    unsigned long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val3 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,3));
    if (val3 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glColor4ub(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglColor4ui(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    unsigned long val2;
    unsigned long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val3 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,3));
    if (val3 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glColor4ui(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglColor4us(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    unsigned long val2;
    unsigned long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val3 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,3));
    if (val3 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glColor4us(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglColor3bv(PyObject* self, PyObject* obj) {
    GLbyte val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor3bv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor3dv(PyObject* self, PyObject* obj) {
    GLdouble val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor3dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor3fv(PyObject* self, PyObject* obj) {
    GLfloat val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor3fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor3iv(PyObject* self, PyObject* obj) {
    GLint val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor3iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor3sv(PyObject* self, PyObject* obj) {
    GLshort val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor3sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor3ubv(PyObject* self, PyObject* obj) {
    GLubyte val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        unsigned long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsUnsignedLongMask(q);
        fail = (t == (unsigned long)(-1) && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor3ubv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor3uiv(PyObject* self, PyObject* obj) {
    GLuint val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        unsigned long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsUnsignedLongMask(q);
        fail = (t == (unsigned long)(-1) && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor3uiv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor3usv(PyObject* self, PyObject* obj) {
    GLushort val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        unsigned long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsUnsignedLongMask(q);
        fail = (t == (unsigned long)(-1) && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor3usv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor4bv(PyObject* self, PyObject* obj) {
    GLbyte val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor4bv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor4dv(PyObject* self, PyObject* obj) {
    GLdouble val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor4dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor4fv(PyObject* self, PyObject* obj) {
    GLfloat val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor4fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor4iv(PyObject* self, PyObject* obj) {
    GLint val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor4iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor4sv(PyObject* self, PyObject* obj) {
    GLshort val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor4sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor4ubv(PyObject* self, PyObject* obj) {
    GLubyte val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        unsigned long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsUnsignedLongMask(q);
        fail = (t == (unsigned long)(-1) && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor4ubv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor4uiv(PyObject* self, PyObject* obj) {
    GLuint val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        unsigned long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsUnsignedLongMask(q);
        fail = (t == (unsigned long)(-1) && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor4uiv(val);
    Py_RETURN_NONE;
}

static PyObject* teglColor4usv(PyObject* self, PyObject* obj) {
    GLushort val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        unsigned long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsUnsignedLongMask(q);
        fail = (t == (unsigned long)(-1) && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glColor4usv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord1d(PyObject* self, PyObject* obj) {
    double val;
    val = PyFloat_AsDouble(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glTexCoord1d(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord1f(PyObject* self, PyObject* obj) {
    double val;
    val = PyFloat_AsDouble(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glTexCoord1f(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord1i(PyObject* self, PyObject* obj) {
    long val;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glTexCoord1i(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord1s(PyObject* self, PyObject* obj) {
    long val;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glTexCoord1s(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord2d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glTexCoord2d(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord2f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glTexCoord2f(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord2i(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glTexCoord2i(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord2s(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glTexCoord2s(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord3d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTexCoord3d(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord3f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTexCoord3f(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord3i(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTexCoord3i(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord3s(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTexCoord3s(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord4d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glTexCoord4d(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord4f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glTexCoord4f(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord4i(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glTexCoord4i(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord4s(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glTexCoord4s(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord1dv(PyObject* self, PyObject* obj) {
    GLdouble val[1];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord1dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord1fv(PyObject* self, PyObject* obj) {
    GLfloat val[1];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord1fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord1iv(PyObject* self, PyObject* obj) {
    GLint val[1];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord1iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord1sv(PyObject* self, PyObject* obj) {
    GLshort val[1];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord1sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord2dv(PyObject* self, PyObject* obj) {
    GLdouble val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord2dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord2fv(PyObject* self, PyObject* obj) {
    GLfloat val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord2fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord2iv(PyObject* self, PyObject* obj) {
    GLint val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord2iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord2sv(PyObject* self, PyObject* obj) {
    GLshort val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord2sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord3dv(PyObject* self, PyObject* obj) {
    GLdouble val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord3dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord3fv(PyObject* self, PyObject* obj) {
    GLfloat val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord3fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord3iv(PyObject* self, PyObject* obj) {
    GLint val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord3iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord3sv(PyObject* self, PyObject* obj) {
    GLshort val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord3sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord4dv(PyObject* self, PyObject* obj) {
    GLdouble val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord4dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord4fv(PyObject* self, PyObject* obj) {
    GLfloat val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord4fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord4iv(PyObject* self, PyObject* obj) {
    GLint val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord4iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoord4sv(PyObject* self, PyObject* obj) {
    GLshort val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glTexCoord4sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos2d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glRasterPos2d(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos2f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glRasterPos2f(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos2i(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glRasterPos2i(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos2s(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glRasterPos2s(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos3d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glRasterPos3d(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos3f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glRasterPos3f(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos3i(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glRasterPos3i(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos3s(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glRasterPos3s(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos4d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glRasterPos4d(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos4f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glRasterPos4f(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos4i(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glRasterPos4i(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos4s(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glRasterPos4s(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos2dv(PyObject* self, PyObject* obj) {
    GLdouble val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glRasterPos2dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos2fv(PyObject* self, PyObject* obj) {
    GLfloat val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glRasterPos2fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos2iv(PyObject* self, PyObject* obj) {
    GLint val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glRasterPos2iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos2sv(PyObject* self, PyObject* obj) {
    GLshort val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glRasterPos2sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos3dv(PyObject* self, PyObject* obj) {
    GLdouble val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glRasterPos3dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos3fv(PyObject* self, PyObject* obj) {
    GLfloat val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glRasterPos3fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos3iv(PyObject* self, PyObject* obj) {
    GLint val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glRasterPos3iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos3sv(PyObject* self, PyObject* obj) {
    GLshort val[3];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glRasterPos3sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos4dv(PyObject* self, PyObject* obj) {
    GLdouble val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glRasterPos4dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos4fv(PyObject* self, PyObject* obj) {
    GLfloat val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glRasterPos4fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos4iv(PyObject* self, PyObject* obj) {
    GLint val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glRasterPos4iv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRasterPos4sv(PyObject* self, PyObject* obj) {
    GLshort val[4];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glRasterPos4sv(val);
    Py_RETURN_NONE;
}

static PyObject* teglRectd(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glRectd(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglRectf(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glRectf(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglRecti(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glRecti(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglRects(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glRects(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglRectdv(PyObject* self, PyObject* args) {
    GLdouble val0[2];
    GLdouble val1[2];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    p = PyTuple_GET_ITEM(args,0);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val0[j] = t;
    }
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glRectdv(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglRectfv(PyObject* self, PyObject* args) {
    GLfloat val0[2];
    GLfloat val1[2];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    p = PyTuple_GET_ITEM(args,0);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val0[j] = t;
    }
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glRectfv(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglRectiv(PyObject* self, PyObject* args) {
    GLint val0[2];
    GLint val1[2];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    p = PyTuple_GET_ITEM(args,0);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val0[j] = t;
    }
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glRectiv(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglRectsv(PyObject* self, PyObject* args) {
    GLshort val0[2];
    GLshort val1[2];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    p = PyTuple_GET_ITEM(args,0);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val0[j] = t;
    }
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glRectsv(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglVertexPointer(PyObject* self, PyObject* args) {
    long val0;
    unsigned long val1;
    long val2;
    const void* val3;
    Py_ssize_t buflen3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,3),&val3,&buflen3) == -1)
        return 0;
    glVertexPointer(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglNormalPointer(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    const void* val2;
    Py_ssize_t buflen2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    glNormalPointer(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglColorPointer(PyObject* self, PyObject* args) {
    long val0;
    unsigned long val1;
    long val2;
    const void* val3;
    Py_ssize_t buflen3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,3),&val3,&buflen3) == -1)
        return 0;
    glColorPointer(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglIndexPointer(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    const void* val2;
    Py_ssize_t buflen2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    glIndexPointer(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexCoordPointer(PyObject* self, PyObject* args) {
    long val0;
    unsigned long val1;
    long val2;
    const void* val3;
    Py_ssize_t buflen3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,3),&val3,&buflen3) == -1)
        return 0;
    glTexCoordPointer(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglEdgeFlagPointer(PyObject* self, PyObject* args) {
    long val0;
    const void* val1;
    Py_ssize_t buflen1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,1),&val1,&buflen1) == -1)
        return 0;
    glEdgeFlagPointer(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglArrayElement(PyObject* self, PyObject* obj) {
    long val;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glArrayElement(val);
    Py_RETURN_NONE;
}

static PyObject* teglDrawArrays(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glDrawArrays(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglDrawElements(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    unsigned long val2;
    const void* val3;
    Py_ssize_t buflen3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,3),&val3,&buflen3) == -1)
        return 0;
    glDrawElements(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglInterleavedArrays(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    const void* val2;
    Py_ssize_t buflen2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    glInterleavedArrays(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglShadeModel(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glShadeModel(val);
    Py_RETURN_NONE;
}

static PyObject* teglLightf(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glLightf(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglLighti(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glLighti(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglLightfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLfloat val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glLightfv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglLightiv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLint val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glLightiv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglGetLightfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLfloat val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetLightfv(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetLightiv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLint val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetLightiv(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglLightModelf(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glLightModelf(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglLightModeli(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glLightModeli(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglLightModelfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLfloat val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glLightModelfv(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglLightModeliv(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLint val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glLightModeliv(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMaterialf(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glMaterialf(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglMateriali(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glMateriali(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglMaterialfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLfloat val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glMaterialfv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglMaterialiv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLint val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glMaterialiv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglGetMaterialfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLfloat val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetMaterialfv(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetMaterialiv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLint val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetMaterialiv(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglColorMaterial(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glColorMaterial(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglPixelZoom(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glPixelZoom(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglPixelStoref(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glPixelStoref(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglPixelStorei(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glPixelStorei(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglPixelTransferf(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glPixelTransferf(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglPixelTransferi(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glPixelTransferi(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglPixelMapfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    const void* val2;
    Py_ssize_t buflen2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    glPixelMapfv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglPixelMapuiv(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    const void* val2;
    Py_ssize_t buflen2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    glPixelMapuiv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglPixelMapusv(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    const void* val2;
    Py_ssize_t buflen2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    glPixelMapusv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglGetPixelMapfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    void* val1;
    Py_ssize_t buflen1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,1),&val1,&buflen1) == -1)
        return 0;
    glGetPixelMapfv(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglGetPixelMapuiv(PyObject* self, PyObject* args) {
    unsigned long val0;
    void* val1;
    Py_ssize_t buflen1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,1),&val1,&buflen1) == -1)
        return 0;
    glGetPixelMapuiv(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglGetPixelMapusv(PyObject* self, PyObject* args) {
    unsigned long val0;
    void* val1;
    Py_ssize_t buflen1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,1),&val1,&buflen1) == -1)
        return 0;
    glGetPixelMapusv(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglBitmap(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    double val2;
    double val3;
    double val4;
    double val5;
    const void* val6;
    Py_ssize_t buflen6;
    if (PyTuple_GET_SIZE(args) != 7) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,6),&val6,&buflen6) == -1)
        return 0;
    glBitmap(val0,val1,val2,val3,val4,val5,val6);
    Py_RETURN_NONE;
}

static PyObject* teglReadPixels(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    unsigned long val4;
    unsigned long val5;
    void* val6;
    Py_ssize_t buflen6;
    if (PyTuple_GET_SIZE(args) != 7) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,4));
    if (val4 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val5 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,5));
    if (val5 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,6),&val6,&buflen6) == -1)
        return 0;
    glReadPixels(val0,val1,val2,val3,val4,val5,val6);
    Py_RETURN_NONE;
}

static PyObject* teglDrawPixels(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    unsigned long val2;
    unsigned long val3;
    const void* val4;
    Py_ssize_t buflen4;
    if (PyTuple_GET_SIZE(args) != 5) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val3 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,3));
    if (val3 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,4),&val4,&buflen4) == -1)
        return 0;
    glDrawPixels(val0,val1,val2,val3,val4);
    Py_RETURN_NONE;
}

static PyObject* teglCopyPixels(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    unsigned long val4;
    if (PyTuple_GET_SIZE(args) != 5) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,4));
    if (val4 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glCopyPixels(val0,val1,val2,val3,val4);
    Py_RETURN_NONE;
}

static PyObject* teglStencilFunc(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    unsigned long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glStencilFunc(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglStencilMask(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glStencilMask(val);
    Py_RETURN_NONE;
}

static PyObject* teglStencilOp(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    unsigned long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glStencilOp(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglClearStencil(PyObject* self, PyObject* obj) {
    long val;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glClearStencil(val);
    Py_RETURN_NONE;
}

static PyObject* teglTexGend(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTexGend(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexGenf(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTexGenf(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexGeni(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTexGeni(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexGendv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLdouble val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glTexGendv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexGenfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLfloat val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glTexGenfv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexGeniv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLint val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glTexGeniv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglGetTexGendv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLdouble val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetTexGendv(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetTexGenfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLfloat val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetTexGenfv(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetTexGeniv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLint val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetTexGeniv(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglTexEnvf(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTexEnvf(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexEnvi(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTexEnvi(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexEnvfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLfloat val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glTexEnvfv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexEnviv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLint val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glTexEnviv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglGetTexEnvfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLfloat val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetTexEnvfv(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetTexEnviv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLint val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetTexEnviv(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglTexParameterf(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTexParameterf(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexParameteri(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glTexParameteri(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexParameterfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLfloat val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glTexParameterfv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglTexParameteriv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLint val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glTexParameteriv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglGetTexParameterfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLfloat val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetTexParameterfv(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetTexParameteriv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLint val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetTexParameteriv(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetTexLevelParameterfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    unsigned long val2;
    GLfloat val3[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetTexLevelParameterfv(val0,val1,val2,val3);
    p = PyTuple_GET_ITEM(args,3);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val3[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetTexLevelParameteriv(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    unsigned long val2;
    GLint val3[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetTexLevelParameteriv(val0,val1,val2,val3);
    p = PyTuple_GET_ITEM(args,3);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val3[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglTexImage1D(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    long val4;
    unsigned long val5;
    unsigned long val6;
    const void* val7;
    Py_ssize_t buflen7;
    if (PyTuple_GET_SIZE(args) != 8) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,5));
    if (val5 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val6 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,6));
    if (val6 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,7),&val7,&buflen7) == -1)
        return 0;
    glTexImage1D(val0,val1,val2,val3,val4,val5,val6,val7);
    Py_RETURN_NONE;
}

static PyObject* teglTexImage2D(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    long val4;
    long val5;
    unsigned long val6;
    unsigned long val7;
    const void* val8;
    Py_ssize_t buflen8;
    if (PyTuple_GET_SIZE(args) != 9) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyInt_AsLong(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    val6 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,6));
    if (val6 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val7 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,7));
    if (val7 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,8),&val8,&buflen8) == -1)
        return 0;
    glTexImage2D(val0,val1,val2,val3,val4,val5,val6,val7,val8);
    Py_RETURN_NONE;
}

static PyObject* teglGetTexImage(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    unsigned long val2;
    unsigned long val3;
    void* val4;
    Py_ssize_t buflen4;
    if (PyTuple_GET_SIZE(args) != 5) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val3 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,3));
    if (val3 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,4),&val4,&buflen4) == -1)
        return 0;
    glGetTexImage(val0,val1,val2,val3,val4);
    Py_RETURN_NONE;
}

static PyObject* teglBindTexture(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glBindTexture(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglIsTexture(PyObject* self, PyObject* obj) {
    unsigned long val;
    int r;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    r = glIsTexture(val);
    return PyBool_FromLong(r);
}

static PyObject* teglTexSubImage1D(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    unsigned long val4;
    unsigned long val5;
    const void* val6;
    Py_ssize_t buflen6;
    if (PyTuple_GET_SIZE(args) != 7) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,4));
    if (val4 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val5 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,5));
    if (val5 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,6),&val6,&buflen6) == -1)
        return 0;
    glTexSubImage1D(val0,val1,val2,val3,val4,val5,val6);
    Py_RETURN_NONE;
}

static PyObject* teglTexSubImage2D(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    long val4;
    long val5;
    unsigned long val6;
    unsigned long val7;
    const void* val8;
    Py_ssize_t buflen8;
    if (PyTuple_GET_SIZE(args) != 9) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyInt_AsLong(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    val6 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,6));
    if (val6 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val7 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,7));
    if (val7 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,8),&val8,&buflen8) == -1)
        return 0;
    glTexSubImage2D(val0,val1,val2,val3,val4,val5,val6,val7,val8);
    Py_RETURN_NONE;
}

static PyObject* teglCopyTexImage1D(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    unsigned long val2;
    long val3;
    long val4;
    long val5;
    long val6;
    if (PyTuple_GET_SIZE(args) != 7) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyInt_AsLong(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    val6 = PyInt_AsLong(PyTuple_GET_ITEM(args,6));
    if (val6 == -1 && PyErr_Occurred()) return 0;
    glCopyTexImage1D(val0,val1,val2,val3,val4,val5,val6);
    Py_RETURN_NONE;
}

static PyObject* teglCopyTexImage2D(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    unsigned long val2;
    long val3;
    long val4;
    long val5;
    long val6;
    long val7;
    if (PyTuple_GET_SIZE(args) != 8) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,2));
    if (val2 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyInt_AsLong(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    val6 = PyInt_AsLong(PyTuple_GET_ITEM(args,6));
    if (val6 == -1 && PyErr_Occurred()) return 0;
    val7 = PyInt_AsLong(PyTuple_GET_ITEM(args,7));
    if (val7 == -1 && PyErr_Occurred()) return 0;
    glCopyTexImage2D(val0,val1,val2,val3,val4,val5,val6,val7);
    Py_RETURN_NONE;
}

static PyObject* teglCopyTexSubImage1D(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    long val4;
    long val5;
    if (PyTuple_GET_SIZE(args) != 6) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyInt_AsLong(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    glCopyTexSubImage1D(val0,val1,val2,val3,val4,val5);
    Py_RETURN_NONE;
}

static PyObject* teglCopyTexSubImage2D(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    long val4;
    long val5;
    long val6;
    long val7;
    if (PyTuple_GET_SIZE(args) != 8) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyInt_AsLong(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    val6 = PyInt_AsLong(PyTuple_GET_ITEM(args,6));
    if (val6 == -1 && PyErr_Occurred()) return 0;
    val7 = PyInt_AsLong(PyTuple_GET_ITEM(args,7));
    if (val7 == -1 && PyErr_Occurred()) return 0;
    glCopyTexSubImage2D(val0,val1,val2,val3,val4,val5,val6,val7);
    Py_RETURN_NONE;
}

static PyObject* teglGenTextures(PyObject* self, PyObject* args) {
    long val0;
    GLuint val1[96];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    glGenTextures(val0,val1);
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 96) n = 96;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyLong_FromUnsignedLong(val1[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglDeleteTextures(PyObject* self, PyObject* args) {
    long val0;
    GLuint val1[96];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 96) n = 96;
    for (j = 0; j < n; j++) {
        PyObject* q;
        unsigned long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsUnsignedLongMask(q);
        fail = (t == (unsigned long)(-1) && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glDeleteTextures(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglPrioritizeTextures(PyObject* self, PyObject* args) {
    long val0;
    GLuint val1[96];
    GLclampf val2[96];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 96) n = 96;
    for (j = 0; j < n; j++) {
        PyObject* q;
        unsigned long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsUnsignedLongMask(q);
        fail = (t == (unsigned long)(-1) && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 96) n = 96;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glPrioritizeTextures(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglAreTexturesResident(PyObject* self, PyObject* args) {
    long val0;
    GLuint val1[96];
    GLboolean val2[96];
    PyObject* p;
    Py_ssize_t j,n;
    int r;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 96) n = 96;
    for (j = 0; j < n; j++) {
        PyObject* q;
        unsigned long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsUnsignedLongMask(q);
        fail = (t == (unsigned long)(-1) && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    r = glAreTexturesResident(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 96) n = 96;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyBool_FromLong(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    return PyBool_FromLong(r);
}

static PyObject* teglMap1d(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    double val2;
    long val3;
    long val4;
    const void* val5;
    Py_ssize_t buflen5;
    if (PyTuple_GET_SIZE(args) != 6) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,5),&val5,&buflen5) == -1)
        return 0;
    glMap1d(val0,val1,val2,val3,val4,val5);
    Py_RETURN_NONE;
}

static PyObject* teglMap1f(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    double val2;
    long val3;
    long val4;
    const void* val5;
    Py_ssize_t buflen5;
    if (PyTuple_GET_SIZE(args) != 6) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,5),&val5,&buflen5) == -1)
        return 0;
    glMap1f(val0,val1,val2,val3,val4,val5);
    Py_RETURN_NONE;
}

static PyObject* teglMap2d(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    double val2;
    long val3;
    long val4;
    double val5;
    double val6;
    long val7;
    long val8;
    const void* val9;
    Py_ssize_t buflen9;
    if (PyTuple_GET_SIZE(args) != 10) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    val6 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,6));
    if (val6 == -1 && PyErr_Occurred()) return 0;
    val7 = PyInt_AsLong(PyTuple_GET_ITEM(args,7));
    if (val7 == -1 && PyErr_Occurred()) return 0;
    val8 = PyInt_AsLong(PyTuple_GET_ITEM(args,8));
    if (val8 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,9),&val9,&buflen9) == -1)
        return 0;
    glMap2d(val0,val1,val2,val3,val4,val5,val6,val7,val8,val9);
    Py_RETURN_NONE;
}

static PyObject* teglMap2f(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    double val2;
    long val3;
    long val4;
    double val5;
    double val6;
    long val7;
    long val8;
    const void* val9;
    Py_ssize_t buflen9;
    if (PyTuple_GET_SIZE(args) != 10) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    val6 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,6));
    if (val6 == -1 && PyErr_Occurred()) return 0;
    val7 = PyInt_AsLong(PyTuple_GET_ITEM(args,7));
    if (val7 == -1 && PyErr_Occurred()) return 0;
    val8 = PyInt_AsLong(PyTuple_GET_ITEM(args,8));
    if (val8 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,9),&val9,&buflen9) == -1)
        return 0;
    glMap2f(val0,val1,val2,val3,val4,val5,val6,val7,val8,val9);
    Py_RETURN_NONE;
}

static PyObject* teglGetMapdv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    void* val2;
    Py_ssize_t buflen2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    glGetMapdv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglGetMapfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    void* val2;
    Py_ssize_t buflen2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    glGetMapfv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglGetMapiv(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    void* val2;
    Py_ssize_t buflen2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    glGetMapiv(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglEvalCoord1d(PyObject* self, PyObject* obj) {
    double val;
    val = PyFloat_AsDouble(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glEvalCoord1d(val);
    Py_RETURN_NONE;
}

static PyObject* teglEvalCoord1f(PyObject* self, PyObject* obj) {
    double val;
    val = PyFloat_AsDouble(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glEvalCoord1f(val);
    Py_RETURN_NONE;
}

static PyObject* teglEvalCoord1dv(PyObject* self, PyObject* obj) {
    GLdouble val[1];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glEvalCoord1dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglEvalCoord1fv(PyObject* self, PyObject* obj) {
    GLfloat val[1];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glEvalCoord1fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglEvalCoord2d(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glEvalCoord2d(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglEvalCoord2f(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glEvalCoord2f(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglEvalCoord2dv(PyObject* self, PyObject* obj) {
    GLdouble val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glEvalCoord2dv(val);
    Py_RETURN_NONE;
}

static PyObject* teglEvalCoord2fv(PyObject* self, PyObject* obj) {
    GLfloat val[2];
    Py_ssize_t j,n;
    n = PySequence_Size(obj);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(obj,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val[j] = t;
    }
    glEvalCoord2fv(val);
    Py_RETURN_NONE;
}

static PyObject* teglMapGrid1d(PyObject* self, PyObject* args) {
    long val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glMapGrid1d(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglMapGrid1f(PyObject* self, PyObject* args) {
    long val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glMapGrid1f(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglMapGrid2d(PyObject* self, PyObject* args) {
    long val0;
    double val1;
    double val2;
    long val3;
    double val4;
    double val5;
    if (PyTuple_GET_SIZE(args) != 6) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    glMapGrid2d(val0,val1,val2,val3,val4,val5);
    Py_RETURN_NONE;
}

static PyObject* teglMapGrid2f(PyObject* self, PyObject* args) {
    long val0;
    double val1;
    double val2;
    long val3;
    double val4;
    double val5;
    if (PyTuple_GET_SIZE(args) != 6) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    glMapGrid2f(val0,val1,val2,val3,val4,val5);
    Py_RETURN_NONE;
}

static PyObject* teglEvalPoint1(PyObject* self, PyObject* obj) {
    long val;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glEvalPoint1(val);
    Py_RETURN_NONE;
}

static PyObject* teglEvalPoint2(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glEvalPoint2(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglEvalMesh1(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glEvalMesh1(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglEvalMesh2(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    long val4;
    if (PyTuple_GET_SIZE(args) != 5) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    glEvalMesh2(val0,val1,val2,val3,val4);
    Py_RETURN_NONE;
}

static PyObject* teglFogf(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glFogf(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglFogi(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glFogi(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglFogfv(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLfloat val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glFogfv(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglFogiv(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLint val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glFogiv(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglFeedbackBuffer(PyObject* self, PyObject* args) {
    long val0;
    unsigned long val1;
    void* val2;
    Py_ssize_t buflen2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    glFeedbackBuffer(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglPassThrough(PyObject* self, PyObject* obj) {
    double val;
    val = PyFloat_AsDouble(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glPassThrough(val);
    Py_RETURN_NONE;
}

static PyObject* teglSelectBuffer(PyObject* self, PyObject* args) {
    long val0;
    void* val1;
    Py_ssize_t buflen1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,1),&val1,&buflen1) == -1)
        return 0;
    glSelectBuffer(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglInitNames(PyObject* self) {
    glInitNames();
    Py_RETURN_NONE;
}

static PyObject* teglLoadName(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glLoadName(val);
    Py_RETURN_NONE;
}

static PyObject* teglPushName(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glPushName(val);
    Py_RETURN_NONE;
}

static PyObject* teglPopName(PyObject* self) {
    glPopName();
    Py_RETURN_NONE;
}

static PyObject* teglActiveTextureARB(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glActiveTextureARB(val);
    Py_RETURN_NONE;
}

static PyObject* teglClientActiveTextureARB(PyObject* self, PyObject* obj) {
    unsigned long val;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glClientActiveTextureARB(val);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord1dARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord1dARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord1dvARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLdouble val1[1];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord1dvARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord1fARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord1fARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord1fvARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLfloat val1[1];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord1fvARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord1iARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord1iARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord1ivARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLint val1[1];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord1ivARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord1sARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord1sARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord1svARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLshort val1[1];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord1svARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord2dARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord2dARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord2dvARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLdouble val1[2];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord2dvARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord2fARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord2fARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord2fvARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLfloat val1[2];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord2fvARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord2iARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord2iARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord2ivARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLint val1[2];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord2ivARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord2sARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord2sARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord2svARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLshort val1[2];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord2svARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord3dARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord3dARB(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord3dvARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLdouble val1[3];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord3dvARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord3fARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord3fARB(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord3fvARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLfloat val1[3];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord3fvARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord3iARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord3iARB(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord3ivARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLint val1[3];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord3ivARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord3sARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord3sARB(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord3svARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLshort val1[3];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord3svARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord4dARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    double val2;
    double val3;
    double val4;
    if (PyTuple_GET_SIZE(args) != 5) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord4dARB(val0,val1,val2,val3,val4);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord4dvARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLdouble val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord4dvARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord4fARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    double val1;
    double val2;
    double val3;
    double val4;
    if (PyTuple_GET_SIZE(args) != 5) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord4fARB(val0,val1,val2,val3,val4);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord4fvARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLfloat val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord4fvARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord4iARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    long val4;
    if (PyTuple_GET_SIZE(args) != 5) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord4iARB(val0,val1,val2,val3,val4);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord4ivARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLint val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord4ivARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord4sARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    long val4;
    if (PyTuple_GET_SIZE(args) != 5) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    glMultiTexCoord4sARB(val0,val1,val2,val3,val4);
    Py_RETURN_NONE;
}

static PyObject* teglMultiTexCoord4svARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    GLshort val1[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glMultiTexCoord4svARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglBindBufferARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glBindBufferARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglDeleteBuffersARB(PyObject* self, PyObject* args) {
    long val0;
    GLuint val1[1];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        unsigned long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsUnsignedLongMask(q);
        fail = (t == (unsigned long)(-1) && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val1[j] = t;
    }
    glDeleteBuffersARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglGenBuffersARB(PyObject* self, PyObject* args) {
    long val0;
    GLuint val1[1];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    glGenBuffersARB(val0,val1);
    p = PyTuple_GET_ITEM(args,1);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyLong_FromUnsignedLong(val1[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglIsBufferARB(PyObject* self, PyObject* obj) {
    unsigned long val;
    int r;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    r = glIsBufferARB(val);
    return PyBool_FromLong(r);
}

static PyObject* teglBufferDataARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    const void* val2;
    Py_ssize_t buflen2;
    unsigned long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    val3 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,3));
    if (val3 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glBufferDataARB(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglBufferSubDataARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    const void* val3;
    Py_ssize_t buflen3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,3),&val3,&buflen3) == -1)
        return 0;
    glBufferSubDataARB(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglGetBufferSubDataARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    void* val3;
    Py_ssize_t buflen3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,3),&val3,&buflen3) == -1)
        return 0;
    glGetBufferSubDataARB(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglMapBufferARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    void* r;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    r = glMapBufferARB(val0,val1);
    return PyCObject_FromVoidPtr(r,0);
}

static PyObject* teglUnmapBufferARB(PyObject* self, PyObject* obj) {
    unsigned long val;
    int r;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    r = glUnmapBufferARB(val);
    return PyBool_FromLong(r);
}

static PyObject* teglGetBufferParameterivARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    unsigned long val1;
    GLint val2[1];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetBufferParameterivARB(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglDeleteObjectARB(PyObject* self, PyObject* obj) {
    long val;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glDeleteObjectARB(val);
    Py_RETURN_NONE;
}

static PyObject* teglGetHandleARB(PyObject* self, PyObject* obj) {
    unsigned long val;
    long r;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    r = glGetHandleARB(val);

    return PyInt_FromLong(r);
}

static PyObject* teglDetachObjectARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glDetachObjectARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglCreateShaderObjectARB(PyObject* self, PyObject* obj) {
    unsigned long val;
    long r;
    val = PyInt_AsUnsignedLongMask(obj);
    if (val == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    r = glCreateShaderObjectARB(val);

    return PyInt_FromLong(r);
}

static PyObject* teglShaderSourceARB(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    const void* val2[1];
    Py_ssize_t buflen2;
    long val3[1];
    PyObject* p;
    Py_ssize_t n;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n != 1) {
        PyErr_SetString(
            PyExc_ValueError,
            "glShaderSourceARB currently supports only one string");
        return 0;
    }
    {
        PyObject* q;
        int fail;
        q = PySequence_GetItem(p,0);
        if (!q) return 0;
        fail = PyObject_AsReadBuffer(q,&val2[0],&buflen2) == -1;
        Py_DECREF(q);
        if (fail) return 0;
    }    
    p = PyTuple_GET_ITEM(args,3);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n != 1) {
        PyErr_SetString(
            PyExc_ValueError,
            "glShaderSourceARB currently supports only one string");
        return 0;
    }
    {
        PyObject* q;
        int fail;
        q = PySequence_GetItem(p,0);
        if (!q) return 0;
        val3[0] = PyInt_AsLong(p);
        fail = (val3[0] == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
    }    
    glShaderSourceARB(val0,val1,(const char**)val2,(const int*)val3);
    Py_RETURN_NONE;
}

static PyObject* teglCompileShaderARB(PyObject* self, PyObject* obj) {
    long val;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glCompileShaderARB(val);
    Py_RETURN_NONE;
}

static PyObject* teglCreateProgramObjectARB(PyObject* self) {
    long r;
    r = glCreateProgramObjectARB();

    return PyInt_FromLong(r);
}

static PyObject* teglAttachObjectARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glAttachObjectARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglLinkProgramARB(PyObject* self, PyObject* obj) {
    long val;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glLinkProgramARB(val);
    Py_RETURN_NONE;
}

static PyObject* teglUseProgramObjectARB(PyObject* self, PyObject* obj) {
    long val;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glUseProgramObjectARB(val);
    Py_RETURN_NONE;
}

static PyObject* teglValidateProgramARB(PyObject* self, PyObject* obj) {
    long val;
    val = PyInt_AsLong(obj);
    if (val == -1 && PyErr_Occurred()) return 0;
    glValidateProgramARB(val);
    Py_RETURN_NONE;
}

static PyObject* teglUniform1fARB(PyObject* self, PyObject* args) {
    long val0;
    double val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glUniform1fARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglUniform2fARB(PyObject* self, PyObject* args) {
    long val0;
    double val1;
    double val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glUniform2fARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglUniform3fARB(PyObject* self, PyObject* args) {
    long val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glUniform3fARB(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglUniform4fARB(PyObject* self, PyObject* args) {
    long val0;
    double val1;
    double val2;
    double val3;
    double val4;
    if (PyTuple_GET_SIZE(args) != 5) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    glUniform4fARB(val0,val1,val2,val3,val4);
    Py_RETURN_NONE;
}

static PyObject* teglUniform1iARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glUniform1iARB(val0,val1);
    Py_RETURN_NONE;
}

static PyObject* teglUniform2iARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    glUniform2iARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglUniform3iARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    glUniform3iARB(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglUniform4iARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    long val2;
    long val3;
    long val4;
    if (PyTuple_GET_SIZE(args) != 5) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    glUniform4iARB(val0,val1,val2,val3,val4);
    Py_RETURN_NONE;
}

static PyObject* teglUniform1fvARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLfloat val2[1];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glUniform1fvARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglUniform2fvARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLfloat val2[2];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glUniform2fvARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglUniform3fvARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLfloat val2[3];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glUniform3fvARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglUniform4fvARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLfloat val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glUniform4fvARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglUniform1ivARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLint val2[1];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glUniform1ivARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglUniform2ivARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLint val2[2];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 2) n = 2;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glUniform2ivARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglUniform3ivARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLint val2[3];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 3) n = 3;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glUniform3ivARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglUniform4ivARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLint val2[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val2[j] = t;
    }
    glUniform4ivARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglUniformMatrix2fvARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    int val2;
    GLfloat val3[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyObject_IsTrue(PyTuple_GET_ITEM(args,2));
    if (val2 == -1) return 0;
    p = PyTuple_GET_ITEM(args,3);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val3[j] = t;
    }
    glUniformMatrix2fvARB(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglUniformMatrix3fvARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    int val2;
    GLfloat val3[9];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyObject_IsTrue(PyTuple_GET_ITEM(args,2));
    if (val2 == -1) return 0;
    p = PyTuple_GET_ITEM(args,3);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 9) n = 9;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val3[j] = t;
    }
    glUniformMatrix3fvARB(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglUniformMatrix4fvARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    int val2;
    GLfloat val3[16];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyObject_IsTrue(PyTuple_GET_ITEM(args,2));
    if (val2 == -1) return 0;
    p = PyTuple_GET_ITEM(args,3);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val3[j] = t;
    }
    glUniformMatrix4fvARB(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* teglGetObjectParameterfvARB(PyObject* self, PyObject* args) {
    long val0;
    unsigned long val1;
    GLfloat val2[1];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetObjectParameterfvARB(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetObjectParameterivARB(PyObject* self, PyObject* args) {
    long val0;
    unsigned long val1;
    GLint val2[1];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    glGetObjectParameterivARB(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetInfoLogARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLsizei val2[1];
    void* val3;
    Py_ssize_t buflen3;
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,3),&val3,&buflen3) == -1)
        return 0;
    glGetInfoLogARB(val0,val1,val2,val3);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetAttachedObjectsARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLsizei val2[1];
    void* val3;
    Py_ssize_t buflen3;
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,3),&val3,&buflen3) == -1)
        return 0;
    glGetAttachedObjectsARB(val0,val1,val2,val3);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetUniformLocationARB(PyObject* self, PyObject* args) {
    long val0;
    const void* val1;
    Py_ssize_t buflen1;
    long r;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,1),&val1,&buflen1) == -1)
        return 0;
    r = glGetUniformLocationARB(val0,val1);

    return PyInt_FromLong(r);
}

static PyObject* teglGetActiveUniformARB(PyObject* self, PyObject* args) {
    long val0;
    unsigned long val1;
    long val2;
    GLsizei val3[1];
    GLint val4[1];
    GLenum val5[1];
    void* val6;
    Py_ssize_t buflen6;
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 7) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,6),&val6,&buflen6) == -1)
        return 0;
    glGetActiveUniformARB(val0,val1,val2,val3,val4,val5,val6);
    p = PyTuple_GET_ITEM(args,3);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val3[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    p = PyTuple_GET_ITEM(args,4);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val4[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    p = PyTuple_GET_ITEM(args,5);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyLong_FromUnsignedLong(val5[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetUniformfvARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLfloat val2[16];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glGetUniformfvARB(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetUniformivARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLint val2[16];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    glGetUniformivARB(val0,val1,val2);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetShaderSourceARB(PyObject* self, PyObject* args) {
    long val0;
    long val1;
    GLsizei val2[1];
    void* val3;
    Py_ssize_t buflen3;
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,3),&val3,&buflen3) == -1)
        return 0;
    glGetShaderSourceARB(val0,val1,val2,val3);
    p = PyTuple_GET_ITEM(args,2);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val2[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglBindAttribLocationARB(PyObject* self, PyObject* args) {
    long val0;
    unsigned long val1;
    const void* val2;
    Py_ssize_t buflen2;
    if (PyTuple_GET_SIZE(args) != 3) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,2),&val2,&buflen2) == -1)
        return 0;
    glBindAttribLocationARB(val0,val1,val2);
    Py_RETURN_NONE;
}

static PyObject* teglGetActiveAttribARB(PyObject* self, PyObject* args) {
    long val0;
    unsigned long val1;
    long val2;
    GLsizei val3[1];
    GLint val4[1];
    GLenum val5[1];
    void* val6;
    Py_ssize_t buflen6;
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 7) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,1));
    if (val1 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,6),&val6,&buflen6) == -1)
        return 0;
    glGetActiveAttribARB(val0,val1,val2,val3,val4,val5,val6);
    p = PyTuple_GET_ITEM(args,3);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val3[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    p = PyTuple_GET_ITEM(args,4);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyInt_FromLong(val4[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    p = PyTuple_GET_ITEM(args,5);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyLong_FromUnsignedLong(val5[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* teglGetAttribLocationARB(PyObject* self, PyObject* args) {
    long val0;
    const void* val1;
    Py_ssize_t buflen1;
    long r;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsLong(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,1),&val1,&buflen1) == -1)
        return 0;
    r = glGetAttribLocationARB(val0,val1);

    return PyInt_FromLong(r);
}

static PyObject* tegluBuild1DMipmapLevels(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    unsigned long val3;
    unsigned long val4;
    long val5;
    long val6;
    long val7;
    const void* val8;
    Py_ssize_t buflen8;
    if (PyTuple_GET_SIZE(args) != 9) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,3));
    if (val3 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val4 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,4));
    if (val4 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val5 = PyInt_AsLong(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    val6 = PyInt_AsLong(PyTuple_GET_ITEM(args,6));
    if (val6 == -1 && PyErr_Occurred()) return 0;
    val7 = PyInt_AsLong(PyTuple_GET_ITEM(args,7));
    if (val7 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,8),&val8,&buflen8) == -1)
        return 0;
    gluBuild1DMipmapLevels(val0,val1,val2,val3,val4,val5,val6,val7,val8);
    Py_RETURN_NONE;
}

static PyObject* tegluBuild1DMipmaps(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    unsigned long val3;
    unsigned long val4;
    const void* val5;
    Py_ssize_t buflen5;
    if (PyTuple_GET_SIZE(args) != 6) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,3));
    if (val3 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val4 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,4));
    if (val4 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,5),&val5,&buflen5) == -1)
        return 0;
    gluBuild1DMipmaps(val0,val1,val2,val3,val4,val5);
    Py_RETURN_NONE;
}

static PyObject* tegluBuild2DMipmapLevels(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    unsigned long val4;
    unsigned long val5;
    long val6;
    long val7;
    long val8;
    const void* val9;
    Py_ssize_t buflen9;
    if (PyTuple_GET_SIZE(args) != 10) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,4));
    if (val4 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val5 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,5));
    if (val5 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val6 = PyInt_AsLong(PyTuple_GET_ITEM(args,6));
    if (val6 == -1 && PyErr_Occurred()) return 0;
    val7 = PyInt_AsLong(PyTuple_GET_ITEM(args,7));
    if (val7 == -1 && PyErr_Occurred()) return 0;
    val8 = PyInt_AsLong(PyTuple_GET_ITEM(args,8));
    if (val8 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,9),&val9,&buflen9) == -1)
        return 0;
    gluBuild2DMipmapLevels(val0,val1,val2,val3,val4,val5,val6,val7,val8,val9);
    Py_RETURN_NONE;
}

static PyObject* tegluBuild2DMipmaps(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    unsigned long val4;
    unsigned long val5;
    const void* val6;
    Py_ssize_t buflen6;
    if (PyTuple_GET_SIZE(args) != 7) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,4));
    if (val4 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val5 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,5));
    if (val5 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,6),&val6,&buflen6) == -1)
        return 0;
    gluBuild2DMipmaps(val0,val1,val2,val3,val4,val5,val6);
    Py_RETURN_NONE;
}

static PyObject* tegluBuild3DMipmapLevels(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    long val4;
    unsigned long val5;
    unsigned long val6;
    long val7;
    long val8;
    long val9;
    const void* val10;
    Py_ssize_t buflen10;
    if (PyTuple_GET_SIZE(args) != 11) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,5));
    if (val5 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val6 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,6));
    if (val6 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val7 = PyInt_AsLong(PyTuple_GET_ITEM(args,7));
    if (val7 == -1 && PyErr_Occurred()) return 0;
    val8 = PyInt_AsLong(PyTuple_GET_ITEM(args,8));
    if (val8 == -1 && PyErr_Occurred()) return 0;
    val9 = PyInt_AsLong(PyTuple_GET_ITEM(args,9));
    if (val9 == -1 && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,10),&val10,&buflen10) == -1)
        return 0;
    gluBuild3DMipmapLevels(val0,val1,val2,val3,val4,val5,val6,val7,val8,val9,val10);
    Py_RETURN_NONE;
}

static PyObject* tegluBuild3DMipmaps(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    long val3;
    long val4;
    unsigned long val5;
    unsigned long val6;
    const void* val7;
    Py_ssize_t buflen7;
    if (PyTuple_GET_SIZE(args) != 8) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsLong(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyInt_AsLong(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,5));
    if (val5 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val6 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,6));
    if (val6 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,7),&val7,&buflen7) == -1)
        return 0;
    gluBuild3DMipmaps(val0,val1,val2,val3,val4,val5,val6,val7);
    Py_RETURN_NONE;
}

static PyObject* tegluCheckExtension(PyObject* self, PyObject* args) {
    const void* val0;
    Py_ssize_t buflen0;
    const void* val1;
    Py_ssize_t buflen1;
    int r;
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,0),&val0,&buflen0) == -1)
        return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,1),&val1,&buflen1) == -1)
        return 0;
    r = gluCheckExtension(val0,val1);
    return PyBool_FromLong(r);
}

static PyObject* tegluLookAt(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    double val4;
    double val5;
    double val6;
    double val7;
    double val8;
    if (PyTuple_GET_SIZE(args) != 9) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    val4 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,4));
    if (val4 == -1 && PyErr_Occurred()) return 0;
    val5 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    val6 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,6));
    if (val6 == -1 && PyErr_Occurred()) return 0;
    val7 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,7));
    if (val7 == -1 && PyErr_Occurred()) return 0;
    val8 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,8));
    if (val8 == -1 && PyErr_Occurred()) return 0;
    gluLookAt(val0,val1,val2,val3,val4,val5,val6,val7,val8);
    Py_RETURN_NONE;
}

static PyObject* tegluOrtho2D(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    gluOrtho2D(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* tegluPerspective(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    if (PyTuple_GET_SIZE(args) != 4) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    gluPerspective(val0,val1,val2,val3);
    Py_RETURN_NONE;
}

static PyObject* tegluPickMatrix(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    GLint val4[4];
    PyObject* p;
    Py_ssize_t j,n;
    if (PyTuple_GET_SIZE(args) != 5) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,4);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val4[j] = t;
    }
    gluPickMatrix(val0,val1,val2,val3,val4);
    Py_RETURN_NONE;
}

static PyObject* tegluProject(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    GLdouble val3[16];
    GLdouble val4[16];
    GLint val5[4];
    GLdouble val6[1];
    GLdouble val7[1];
    GLdouble val8[1];
    PyObject* p;
    Py_ssize_t j,n;
    long r;
    if (PyTuple_GET_SIZE(args) != 9) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,3);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val3[j] = t;
    }
    p = PyTuple_GET_ITEM(args,4);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val4[j] = t;
    }
    p = PyTuple_GET_ITEM(args,5);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val5[j] = t;
    }
    r = gluProject(val0,val1,val2,val3,val4,val5,val6,val7,val8);
    p = PyTuple_GET_ITEM(args,6);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val6[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    p = PyTuple_GET_ITEM(args,7);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val7[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    p = PyTuple_GET_ITEM(args,8);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val8[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }

    return PyInt_FromLong(r);
}

static PyObject* tegluScaleImage(PyObject* self, PyObject* args) {
    unsigned long val0;
    long val1;
    long val2;
    unsigned long val3;
    const void* val4;
    Py_ssize_t buflen4;
    long val5;
    long val6;
    unsigned long val7;
    void* val8;
    Py_ssize_t buflen8;
    if (PyTuple_GET_SIZE(args) != 9) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,0));
    if (val0 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    val1 = PyInt_AsLong(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyInt_AsLong(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,3));
    if (val3 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsReadBuffer(PyTuple_GET_ITEM(args,4),&val4,&buflen4) == -1)
        return 0;
    val5 = PyInt_AsLong(PyTuple_GET_ITEM(args,5));
    if (val5 == -1 && PyErr_Occurred()) return 0;
    val6 = PyInt_AsLong(PyTuple_GET_ITEM(args,6));
    if (val6 == -1 && PyErr_Occurred()) return 0;
    val7 = PyInt_AsUnsignedLongMask(PyTuple_GET_ITEM(args,7));
    if (val7 == (unsigned long)(-1) && PyErr_Occurred()) return 0;
    if(PyObject_AsWriteBuffer(PyTuple_GET_ITEM(args,8),&val8,&buflen8) == -1)
        return 0;
    gluScaleImage(val0,val1,val2,val3,val4,val5,val6,val7,val8);
    Py_RETURN_NONE;
}

static PyObject* tegluUnProject(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    GLdouble val3[16];
    GLdouble val4[16];
    GLint val5[4];
    GLdouble val6[1];
    GLdouble val7[1];
    GLdouble val8[1];
    PyObject* p;
    Py_ssize_t j,n;
    long r;
    if (PyTuple_GET_SIZE(args) != 9) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,3);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val3[j] = t;
    }
    p = PyTuple_GET_ITEM(args,4);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val4[j] = t;
    }
    p = PyTuple_GET_ITEM(args,5);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val5[j] = t;
    }
    r = gluUnProject(val0,val1,val2,val3,val4,val5,val6,val7,val8);
    p = PyTuple_GET_ITEM(args,6);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val6[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    p = PyTuple_GET_ITEM(args,7);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val7[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    p = PyTuple_GET_ITEM(args,8);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val8[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }

    return PyInt_FromLong(r);
}

static PyObject* tegluUnProject4(PyObject* self, PyObject* args) {
    double val0;
    double val1;
    double val2;
    double val3;
    GLdouble val4[16];
    GLdouble val5[16];
    GLint val6[4];
    double val7;
    double val8;
    GLdouble val9[1];
    GLdouble val10[1];
    GLdouble val11[1];
    GLdouble val12[1];
    PyObject* p;
    Py_ssize_t j,n;
    long r;
    if (PyTuple_GET_SIZE(args) != 13) {
        PyErr_SetString(PyExc_ValueError,ARGCOUNT);
        return 0;
    }
    val0 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,0));
    if (val0 == -1 && PyErr_Occurred()) return 0;
    val1 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,1));
    if (val1 == -1 && PyErr_Occurred()) return 0;
    val2 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,2));
    if (val2 == -1 && PyErr_Occurred()) return 0;
    val3 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,3));
    if (val3 == -1 && PyErr_Occurred()) return 0;
    p = PyTuple_GET_ITEM(args,4);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val4[j] = t;
    }
    p = PyTuple_GET_ITEM(args,5);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 16) n = 16;
    for (j = 0; j < n; j++) {
        PyObject* q;
        double t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyFloat_AsDouble(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val5[j] = t;
    }
    p = PyTuple_GET_ITEM(args,6);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 4) n = 4;
    for (j = 0; j < n; j++) {
        PyObject* q;
        long t;
        int fail;
        q = PySequence_GetItem(p,j);
        if (!q) return 0;
        t = PyInt_AsLong(q);
        fail = (t == -1 && PyErr_Occurred());
        Py_DECREF(q);
        if (fail) return 0;
        val6[j] = t;
    }
    val7 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,7));
    if (val7 == -1 && PyErr_Occurred()) return 0;
    val8 = PyFloat_AsDouble(PyTuple_GET_ITEM(args,8));
    if (val8 == -1 && PyErr_Occurred()) return 0;
    r = gluUnProject4(val0,val1,val2,val3,val4,val5,val6,val7,val8,val9,val10,val11,val12);
    p = PyTuple_GET_ITEM(args,9);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val9[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    p = PyTuple_GET_ITEM(args,10);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val10[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    p = PyTuple_GET_ITEM(args,11);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val11[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }
    p = PyTuple_GET_ITEM(args,12);
    n = PySequence_Size(p);
    if (n == -1) return 0;
    if (n > 1) n = 1;
    for (j = 0; j < n; j++) {
        PyObject* q;
        int status;
        q = PyFloat_FromDouble(val12[j]);
        if (!q) return 0;
        status = PySequence_SetItem(p,j,q);
        Py_DECREF(q);
        if (status == -1) return 0;
    }

    return PyInt_FromLong(r);
}


PyMethodDef module_methods[] = {
    { "ClearIndex", (PyCFunction)teglClearIndex, METH_O },
    { "ClearColor", (PyCFunction)teglClearColor, METH_VARARGS },
    { "Clear", (PyCFunction)teglClear, METH_O },
    { "IndexMask", (PyCFunction)teglIndexMask, METH_O },
    { "ColorMask", (PyCFunction)teglColorMask, METH_VARARGS },
    { "AlphaFunc", (PyCFunction)teglAlphaFunc, METH_VARARGS },
    { "BlendFunc", (PyCFunction)teglBlendFunc, METH_VARARGS },
    { "LogicOp", (PyCFunction)teglLogicOp, METH_O },
    { "CullFace", (PyCFunction)teglCullFace, METH_O },
    { "FrontFace", (PyCFunction)teglFrontFace, METH_O },
    { "PointSize", (PyCFunction)teglPointSize, METH_O },
    { "LineWidth", (PyCFunction)teglLineWidth, METH_O },
    { "LineStipple", (PyCFunction)teglLineStipple, METH_VARARGS },
    { "PolygonMode", (PyCFunction)teglPolygonMode, METH_VARARGS },
    { "PolygonOffset", (PyCFunction)teglPolygonOffset, METH_VARARGS },
    { "PolygonStipple", (PyCFunction)teglPolygonStipple, METH_O },
    { "GetPolygonStipple", (PyCFunction)teglGetPolygonStipple, METH_O },
    { "EdgeFlag", (PyCFunction)teglEdgeFlag, METH_O },
    { "EdgeFlagv", (PyCFunction)teglEdgeFlagv, METH_O },
    { "Scissor", (PyCFunction)teglScissor, METH_VARARGS },
    { "ClipPlane", (PyCFunction)teglClipPlane, METH_VARARGS },
    { "GetClipPlane", (PyCFunction)teglGetClipPlane, METH_VARARGS },
    { "DrawBuffer", (PyCFunction)teglDrawBuffer, METH_O },
    { "ReadBuffer", (PyCFunction)teglReadBuffer, METH_O },
    { "Enable", (PyCFunction)teglEnable, METH_O },
    { "Disable", (PyCFunction)teglDisable, METH_O },
    { "IsEnabled", (PyCFunction)teglIsEnabled, METH_O },
    { "EnableClientState", (PyCFunction)teglEnableClientState, METH_O },
    { "DisableClientState", (PyCFunction)teglDisableClientState, METH_O },
    { "GetBooleanv", (PyCFunction)teglGetBooleanv, METH_VARARGS },
    { "GetDoublev", (PyCFunction)teglGetDoublev, METH_VARARGS },
    { "GetFloatv", (PyCFunction)teglGetFloatv, METH_VARARGS },
    { "GetIntegerv", (PyCFunction)teglGetIntegerv, METH_VARARGS },
    { "PushAttrib", (PyCFunction)teglPushAttrib, METH_O },
    { "PopAttrib", (PyCFunction)teglPopAttrib, METH_NOARGS },
    { "PushClientAttrib", (PyCFunction)teglPushClientAttrib, METH_O },
    { "PopClientAttrib", (PyCFunction)teglPopClientAttrib, METH_NOARGS },
    { "RenderMode", (PyCFunction)teglRenderMode, METH_O },
    { "GetError", (PyCFunction)teglGetError, METH_NOARGS },
    { "Finish", (PyCFunction)teglFinish, METH_NOARGS },
    { "Flush", (PyCFunction)teglFlush, METH_NOARGS },
    { "Hint", (PyCFunction)teglHint, METH_VARARGS },
    { "ClearDepth", (PyCFunction)teglClearDepth, METH_O },
    { "DepthFunc", (PyCFunction)teglDepthFunc, METH_O },
    { "DepthMask", (PyCFunction)teglDepthMask, METH_O },
    { "DepthRange", (PyCFunction)teglDepthRange, METH_VARARGS },
    { "ClearAccum", (PyCFunction)teglClearAccum, METH_VARARGS },
    { "Accum", (PyCFunction)teglAccum, METH_VARARGS },
    { "MatrixMode", (PyCFunction)teglMatrixMode, METH_O },
    { "Ortho", (PyCFunction)teglOrtho, METH_VARARGS },
    { "Frustum", (PyCFunction)teglFrustum, METH_VARARGS },
    { "Viewport", (PyCFunction)teglViewport, METH_VARARGS },
    { "PushMatrix", (PyCFunction)teglPushMatrix, METH_NOARGS },
    { "PopMatrix", (PyCFunction)teglPopMatrix, METH_NOARGS },
    { "LoadIdentity", (PyCFunction)teglLoadIdentity, METH_NOARGS },
    { "LoadMatrixd", (PyCFunction)teglLoadMatrixd, METH_O },
    { "LoadMatrixf", (PyCFunction)teglLoadMatrixf, METH_O },
    { "MultMatrixd", (PyCFunction)teglMultMatrixd, METH_O },
    { "MultMatrixf", (PyCFunction)teglMultMatrixf, METH_O },
    { "Rotated", (PyCFunction)teglRotated, METH_VARARGS },
    { "Rotatef", (PyCFunction)teglRotatef, METH_VARARGS },
    { "Scaled", (PyCFunction)teglScaled, METH_VARARGS },
    { "Scalef", (PyCFunction)teglScalef, METH_VARARGS },
    { "Translated", (PyCFunction)teglTranslated, METH_VARARGS },
    { "Translatef", (PyCFunction)teglTranslatef, METH_VARARGS },
    { "IsList", (PyCFunction)teglIsList, METH_O },
    { "DeleteLists", (PyCFunction)teglDeleteLists, METH_VARARGS },
    { "GenLists", (PyCFunction)teglGenLists, METH_O },
    { "NewList", (PyCFunction)teglNewList, METH_VARARGS },
    { "EndList", (PyCFunction)teglEndList, METH_NOARGS },
    { "CallList", (PyCFunction)teglCallList, METH_O },
    { "CallLists", (PyCFunction)teglCallLists, METH_VARARGS },
    { "ListBase", (PyCFunction)teglListBase, METH_O },
    { "Begin", (PyCFunction)teglBegin, METH_O },
    { "End", (PyCFunction)teglEnd, METH_NOARGS },
    { "Vertex2d", (PyCFunction)teglVertex2d, METH_VARARGS },
    { "Vertex2f", (PyCFunction)teglVertex2f, METH_VARARGS },
    { "Vertex2i", (PyCFunction)teglVertex2i, METH_VARARGS },
    { "Vertex2s", (PyCFunction)teglVertex2s, METH_VARARGS },
    { "Vertex3d", (PyCFunction)teglVertex3d, METH_VARARGS },
    { "Vertex3f", (PyCFunction)teglVertex3f, METH_VARARGS },
    { "Vertex3i", (PyCFunction)teglVertex3i, METH_VARARGS },
    { "Vertex3s", (PyCFunction)teglVertex3s, METH_VARARGS },
    { "Vertex4d", (PyCFunction)teglVertex4d, METH_VARARGS },
    { "Vertex4f", (PyCFunction)teglVertex4f, METH_VARARGS },
    { "Vertex4i", (PyCFunction)teglVertex4i, METH_VARARGS },
    { "Vertex4s", (PyCFunction)teglVertex4s, METH_VARARGS },
    { "Vertex2dv", (PyCFunction)teglVertex2dv, METH_O },
    { "Vertex2fv", (PyCFunction)teglVertex2fv, METH_O },
    { "Vertex2iv", (PyCFunction)teglVertex2iv, METH_O },
    { "Vertex2sv", (PyCFunction)teglVertex2sv, METH_O },
    { "Vertex3dv", (PyCFunction)teglVertex3dv, METH_O },
    { "Vertex3fv", (PyCFunction)teglVertex3fv, METH_O },
    { "Vertex3iv", (PyCFunction)teglVertex3iv, METH_O },
    { "Vertex3sv", (PyCFunction)teglVertex3sv, METH_O },
    { "Vertex4dv", (PyCFunction)teglVertex4dv, METH_O },
    { "Vertex4fv", (PyCFunction)teglVertex4fv, METH_O },
    { "Vertex4iv", (PyCFunction)teglVertex4iv, METH_O },
    { "Vertex4sv", (PyCFunction)teglVertex4sv, METH_O },
    { "Normal3b", (PyCFunction)teglNormal3b, METH_VARARGS },
    { "Normal3d", (PyCFunction)teglNormal3d, METH_VARARGS },
    { "Normal3f", (PyCFunction)teglNormal3f, METH_VARARGS },
    { "Normal3i", (PyCFunction)teglNormal3i, METH_VARARGS },
    { "Normal3s", (PyCFunction)teglNormal3s, METH_VARARGS },
    { "Normal3bv", (PyCFunction)teglNormal3bv, METH_O },
    { "Normal3dv", (PyCFunction)teglNormal3dv, METH_O },
    { "Normal3fv", (PyCFunction)teglNormal3fv, METH_O },
    { "Normal3iv", (PyCFunction)teglNormal3iv, METH_O },
    { "Normal3sv", (PyCFunction)teglNormal3sv, METH_O },
    { "Indexd", (PyCFunction)teglIndexd, METH_O },
    { "Indexf", (PyCFunction)teglIndexf, METH_O },
    { "Indexi", (PyCFunction)teglIndexi, METH_O },
    { "Indexs", (PyCFunction)teglIndexs, METH_O },
    { "Indexub", (PyCFunction)teglIndexub, METH_O },
    { "Indexdv", (PyCFunction)teglIndexdv, METH_O },
    { "Indexfv", (PyCFunction)teglIndexfv, METH_O },
    { "Indexiv", (PyCFunction)teglIndexiv, METH_O },
    { "Indexsv", (PyCFunction)teglIndexsv, METH_O },
    { "Indexubv", (PyCFunction)teglIndexubv, METH_O },
    { "Color3b", (PyCFunction)teglColor3b, METH_VARARGS },
    { "Color3d", (PyCFunction)teglColor3d, METH_VARARGS },
    { "Color3f", (PyCFunction)teglColor3f, METH_VARARGS },
    { "Color3i", (PyCFunction)teglColor3i, METH_VARARGS },
    { "Color3s", (PyCFunction)teglColor3s, METH_VARARGS },
    { "Color3ub", (PyCFunction)teglColor3ub, METH_VARARGS },
    { "Color3ui", (PyCFunction)teglColor3ui, METH_VARARGS },
    { "Color3us", (PyCFunction)teglColor3us, METH_VARARGS },
    { "Color4b", (PyCFunction)teglColor4b, METH_VARARGS },
    { "Color4d", (PyCFunction)teglColor4d, METH_VARARGS },
    { "Color4f", (PyCFunction)teglColor4f, METH_VARARGS },
    { "Color4i", (PyCFunction)teglColor4i, METH_VARARGS },
    { "Color4s", (PyCFunction)teglColor4s, METH_VARARGS },
    { "Color4ub", (PyCFunction)teglColor4ub, METH_VARARGS },
    { "Color4ui", (PyCFunction)teglColor4ui, METH_VARARGS },
    { "Color4us", (PyCFunction)teglColor4us, METH_VARARGS },
    { "Color3bv", (PyCFunction)teglColor3bv, METH_O },
    { "Color3dv", (PyCFunction)teglColor3dv, METH_O },
    { "Color3fv", (PyCFunction)teglColor3fv, METH_O },
    { "Color3iv", (PyCFunction)teglColor3iv, METH_O },
    { "Color3sv", (PyCFunction)teglColor3sv, METH_O },
    { "Color3ubv", (PyCFunction)teglColor3ubv, METH_O },
    { "Color3uiv", (PyCFunction)teglColor3uiv, METH_O },
    { "Color3usv", (PyCFunction)teglColor3usv, METH_O },
    { "Color4bv", (PyCFunction)teglColor4bv, METH_O },
    { "Color4dv", (PyCFunction)teglColor4dv, METH_O },
    { "Color4fv", (PyCFunction)teglColor4fv, METH_O },
    { "Color4iv", (PyCFunction)teglColor4iv, METH_O },
    { "Color4sv", (PyCFunction)teglColor4sv, METH_O },
    { "Color4ubv", (PyCFunction)teglColor4ubv, METH_O },
    { "Color4uiv", (PyCFunction)teglColor4uiv, METH_O },
    { "Color4usv", (PyCFunction)teglColor4usv, METH_O },
    { "TexCoord1d", (PyCFunction)teglTexCoord1d, METH_O },
    { "TexCoord1f", (PyCFunction)teglTexCoord1f, METH_O },
    { "TexCoord1i", (PyCFunction)teglTexCoord1i, METH_O },
    { "TexCoord1s", (PyCFunction)teglTexCoord1s, METH_O },
    { "TexCoord2d", (PyCFunction)teglTexCoord2d, METH_VARARGS },
    { "TexCoord2f", (PyCFunction)teglTexCoord2f, METH_VARARGS },
    { "TexCoord2i", (PyCFunction)teglTexCoord2i, METH_VARARGS },
    { "TexCoord2s", (PyCFunction)teglTexCoord2s, METH_VARARGS },
    { "TexCoord3d", (PyCFunction)teglTexCoord3d, METH_VARARGS },
    { "TexCoord3f", (PyCFunction)teglTexCoord3f, METH_VARARGS },
    { "TexCoord3i", (PyCFunction)teglTexCoord3i, METH_VARARGS },
    { "TexCoord3s", (PyCFunction)teglTexCoord3s, METH_VARARGS },
    { "TexCoord4d", (PyCFunction)teglTexCoord4d, METH_VARARGS },
    { "TexCoord4f", (PyCFunction)teglTexCoord4f, METH_VARARGS },
    { "TexCoord4i", (PyCFunction)teglTexCoord4i, METH_VARARGS },
    { "TexCoord4s", (PyCFunction)teglTexCoord4s, METH_VARARGS },
    { "TexCoord1dv", (PyCFunction)teglTexCoord1dv, METH_O },
    { "TexCoord1fv", (PyCFunction)teglTexCoord1fv, METH_O },
    { "TexCoord1iv", (PyCFunction)teglTexCoord1iv, METH_O },
    { "TexCoord1sv", (PyCFunction)teglTexCoord1sv, METH_O },
    { "TexCoord2dv", (PyCFunction)teglTexCoord2dv, METH_O },
    { "TexCoord2fv", (PyCFunction)teglTexCoord2fv, METH_O },
    { "TexCoord2iv", (PyCFunction)teglTexCoord2iv, METH_O },
    { "TexCoord2sv", (PyCFunction)teglTexCoord2sv, METH_O },
    { "TexCoord3dv", (PyCFunction)teglTexCoord3dv, METH_O },
    { "TexCoord3fv", (PyCFunction)teglTexCoord3fv, METH_O },
    { "TexCoord3iv", (PyCFunction)teglTexCoord3iv, METH_O },
    { "TexCoord3sv", (PyCFunction)teglTexCoord3sv, METH_O },
    { "TexCoord4dv", (PyCFunction)teglTexCoord4dv, METH_O },
    { "TexCoord4fv", (PyCFunction)teglTexCoord4fv, METH_O },
    { "TexCoord4iv", (PyCFunction)teglTexCoord4iv, METH_O },
    { "TexCoord4sv", (PyCFunction)teglTexCoord4sv, METH_O },
    { "RasterPos2d", (PyCFunction)teglRasterPos2d, METH_VARARGS },
    { "RasterPos2f", (PyCFunction)teglRasterPos2f, METH_VARARGS },
    { "RasterPos2i", (PyCFunction)teglRasterPos2i, METH_VARARGS },
    { "RasterPos2s", (PyCFunction)teglRasterPos2s, METH_VARARGS },
    { "RasterPos3d", (PyCFunction)teglRasterPos3d, METH_VARARGS },
    { "RasterPos3f", (PyCFunction)teglRasterPos3f, METH_VARARGS },
    { "RasterPos3i", (PyCFunction)teglRasterPos3i, METH_VARARGS },
    { "RasterPos3s", (PyCFunction)teglRasterPos3s, METH_VARARGS },
    { "RasterPos4d", (PyCFunction)teglRasterPos4d, METH_VARARGS },
    { "RasterPos4f", (PyCFunction)teglRasterPos4f, METH_VARARGS },
    { "RasterPos4i", (PyCFunction)teglRasterPos4i, METH_VARARGS },
    { "RasterPos4s", (PyCFunction)teglRasterPos4s, METH_VARARGS },
    { "RasterPos2dv", (PyCFunction)teglRasterPos2dv, METH_O },
    { "RasterPos2fv", (PyCFunction)teglRasterPos2fv, METH_O },
    { "RasterPos2iv", (PyCFunction)teglRasterPos2iv, METH_O },
    { "RasterPos2sv", (PyCFunction)teglRasterPos2sv, METH_O },
    { "RasterPos3dv", (PyCFunction)teglRasterPos3dv, METH_O },
    { "RasterPos3fv", (PyCFunction)teglRasterPos3fv, METH_O },
    { "RasterPos3iv", (PyCFunction)teglRasterPos3iv, METH_O },
    { "RasterPos3sv", (PyCFunction)teglRasterPos3sv, METH_O },
    { "RasterPos4dv", (PyCFunction)teglRasterPos4dv, METH_O },
    { "RasterPos4fv", (PyCFunction)teglRasterPos4fv, METH_O },
    { "RasterPos4iv", (PyCFunction)teglRasterPos4iv, METH_O },
    { "RasterPos4sv", (PyCFunction)teglRasterPos4sv, METH_O },
    { "Rectd", (PyCFunction)teglRectd, METH_VARARGS },
    { "Rectf", (PyCFunction)teglRectf, METH_VARARGS },
    { "Recti", (PyCFunction)teglRecti, METH_VARARGS },
    { "Rects", (PyCFunction)teglRects, METH_VARARGS },
    { "Rectdv", (PyCFunction)teglRectdv, METH_VARARGS },
    { "Rectfv", (PyCFunction)teglRectfv, METH_VARARGS },
    { "Rectiv", (PyCFunction)teglRectiv, METH_VARARGS },
    { "Rectsv", (PyCFunction)teglRectsv, METH_VARARGS },
    { "VertexPointer", (PyCFunction)teglVertexPointer, METH_VARARGS },
    { "NormalPointer", (PyCFunction)teglNormalPointer, METH_VARARGS },
    { "ColorPointer", (PyCFunction)teglColorPointer, METH_VARARGS },
    { "IndexPointer", (PyCFunction)teglIndexPointer, METH_VARARGS },
    { "TexCoordPointer", (PyCFunction)teglTexCoordPointer, METH_VARARGS },
    { "EdgeFlagPointer", (PyCFunction)teglEdgeFlagPointer, METH_VARARGS },
    { "ArrayElement", (PyCFunction)teglArrayElement, METH_O },
    { "DrawArrays", (PyCFunction)teglDrawArrays, METH_VARARGS },
    { "DrawElements", (PyCFunction)teglDrawElements, METH_VARARGS },
    { "InterleavedArrays", (PyCFunction)teglInterleavedArrays, METH_VARARGS },
    { "ShadeModel", (PyCFunction)teglShadeModel, METH_O },
    { "Lightf", (PyCFunction)teglLightf, METH_VARARGS },
    { "Lighti", (PyCFunction)teglLighti, METH_VARARGS },
    { "Lightfv", (PyCFunction)teglLightfv, METH_VARARGS },
    { "Lightiv", (PyCFunction)teglLightiv, METH_VARARGS },
    { "GetLightfv", (PyCFunction)teglGetLightfv, METH_VARARGS },
    { "GetLightiv", (PyCFunction)teglGetLightiv, METH_VARARGS },
    { "LightModelf", (PyCFunction)teglLightModelf, METH_VARARGS },
    { "LightModeli", (PyCFunction)teglLightModeli, METH_VARARGS },
    { "LightModelfv", (PyCFunction)teglLightModelfv, METH_VARARGS },
    { "LightModeliv", (PyCFunction)teglLightModeliv, METH_VARARGS },
    { "Materialf", (PyCFunction)teglMaterialf, METH_VARARGS },
    { "Materiali", (PyCFunction)teglMateriali, METH_VARARGS },
    { "Materialfv", (PyCFunction)teglMaterialfv, METH_VARARGS },
    { "Materialiv", (PyCFunction)teglMaterialiv, METH_VARARGS },
    { "GetMaterialfv", (PyCFunction)teglGetMaterialfv, METH_VARARGS },
    { "GetMaterialiv", (PyCFunction)teglGetMaterialiv, METH_VARARGS },
    { "ColorMaterial", (PyCFunction)teglColorMaterial, METH_VARARGS },
    { "PixelZoom", (PyCFunction)teglPixelZoom, METH_VARARGS },
    { "PixelStoref", (PyCFunction)teglPixelStoref, METH_VARARGS },
    { "PixelStorei", (PyCFunction)teglPixelStorei, METH_VARARGS },
    { "PixelTransferf", (PyCFunction)teglPixelTransferf, METH_VARARGS },
    { "PixelTransferi", (PyCFunction)teglPixelTransferi, METH_VARARGS },
    { "PixelMapfv", (PyCFunction)teglPixelMapfv, METH_VARARGS },
    { "PixelMapuiv", (PyCFunction)teglPixelMapuiv, METH_VARARGS },
    { "PixelMapusv", (PyCFunction)teglPixelMapusv, METH_VARARGS },
    { "GetPixelMapfv", (PyCFunction)teglGetPixelMapfv, METH_VARARGS },
    { "GetPixelMapuiv", (PyCFunction)teglGetPixelMapuiv, METH_VARARGS },
    { "GetPixelMapusv", (PyCFunction)teglGetPixelMapusv, METH_VARARGS },
    { "Bitmap", (PyCFunction)teglBitmap, METH_VARARGS },
    { "ReadPixels", (PyCFunction)teglReadPixels, METH_VARARGS },
    { "DrawPixels", (PyCFunction)teglDrawPixels, METH_VARARGS },
    { "CopyPixels", (PyCFunction)teglCopyPixels, METH_VARARGS },
    { "StencilFunc", (PyCFunction)teglStencilFunc, METH_VARARGS },
    { "StencilMask", (PyCFunction)teglStencilMask, METH_O },
    { "StencilOp", (PyCFunction)teglStencilOp, METH_VARARGS },
    { "ClearStencil", (PyCFunction)teglClearStencil, METH_O },
    { "TexGend", (PyCFunction)teglTexGend, METH_VARARGS },
    { "TexGenf", (PyCFunction)teglTexGenf, METH_VARARGS },
    { "TexGeni", (PyCFunction)teglTexGeni, METH_VARARGS },
    { "TexGendv", (PyCFunction)teglTexGendv, METH_VARARGS },
    { "TexGenfv", (PyCFunction)teglTexGenfv, METH_VARARGS },
    { "TexGeniv", (PyCFunction)teglTexGeniv, METH_VARARGS },
    { "GetTexGendv", (PyCFunction)teglGetTexGendv, METH_VARARGS },
    { "GetTexGenfv", (PyCFunction)teglGetTexGenfv, METH_VARARGS },
    { "GetTexGeniv", (PyCFunction)teglGetTexGeniv, METH_VARARGS },
    { "TexEnvf", (PyCFunction)teglTexEnvf, METH_VARARGS },
    { "TexEnvi", (PyCFunction)teglTexEnvi, METH_VARARGS },
    { "TexEnvfv", (PyCFunction)teglTexEnvfv, METH_VARARGS },
    { "TexEnviv", (PyCFunction)teglTexEnviv, METH_VARARGS },
    { "GetTexEnvfv", (PyCFunction)teglGetTexEnvfv, METH_VARARGS },
    { "GetTexEnviv", (PyCFunction)teglGetTexEnviv, METH_VARARGS },
    { "TexParameterf", (PyCFunction)teglTexParameterf, METH_VARARGS },
    { "TexParameteri", (PyCFunction)teglTexParameteri, METH_VARARGS },
    { "TexParameterfv", (PyCFunction)teglTexParameterfv, METH_VARARGS },
    { "TexParameteriv", (PyCFunction)teglTexParameteriv, METH_VARARGS },
    { "GetTexParameterfv", (PyCFunction)teglGetTexParameterfv, METH_VARARGS },
    { "GetTexParameteriv", (PyCFunction)teglGetTexParameteriv, METH_VARARGS },
    { "GetTexLevelParameterfv", (PyCFunction)teglGetTexLevelParameterfv, METH_VARARGS },
    { "GetTexLevelParameteriv", (PyCFunction)teglGetTexLevelParameteriv, METH_VARARGS },
    { "TexImage1D", (PyCFunction)teglTexImage1D, METH_VARARGS },
    { "TexImage2D", (PyCFunction)teglTexImage2D, METH_VARARGS },
    { "GetTexImage", (PyCFunction)teglGetTexImage, METH_VARARGS },
    { "BindTexture", (PyCFunction)teglBindTexture, METH_VARARGS },
    { "IsTexture", (PyCFunction)teglIsTexture, METH_O },
    { "TexSubImage1D", (PyCFunction)teglTexSubImage1D, METH_VARARGS },
    { "TexSubImage2D", (PyCFunction)teglTexSubImage2D, METH_VARARGS },
    { "CopyTexImage1D", (PyCFunction)teglCopyTexImage1D, METH_VARARGS },
    { "CopyTexImage2D", (PyCFunction)teglCopyTexImage2D, METH_VARARGS },
    { "CopyTexSubImage1D", (PyCFunction)teglCopyTexSubImage1D, METH_VARARGS },
    { "CopyTexSubImage2D", (PyCFunction)teglCopyTexSubImage2D, METH_VARARGS },
    { "GenTextures", (PyCFunction)teglGenTextures, METH_VARARGS },
    { "DeleteTextures", (PyCFunction)teglDeleteTextures, METH_VARARGS },
    { "PrioritizeTextures", (PyCFunction)teglPrioritizeTextures, METH_VARARGS },
    { "AreTexturesResident", (PyCFunction)teglAreTexturesResident, METH_VARARGS },
    { "Map1d", (PyCFunction)teglMap1d, METH_VARARGS },
    { "Map1f", (PyCFunction)teglMap1f, METH_VARARGS },
    { "Map2d", (PyCFunction)teglMap2d, METH_VARARGS },
    { "Map2f", (PyCFunction)teglMap2f, METH_VARARGS },
    { "GetMapdv", (PyCFunction)teglGetMapdv, METH_VARARGS },
    { "GetMapfv", (PyCFunction)teglGetMapfv, METH_VARARGS },
    { "GetMapiv", (PyCFunction)teglGetMapiv, METH_VARARGS },
    { "EvalCoord1d", (PyCFunction)teglEvalCoord1d, METH_O },
    { "EvalCoord1f", (PyCFunction)teglEvalCoord1f, METH_O },
    { "EvalCoord1dv", (PyCFunction)teglEvalCoord1dv, METH_O },
    { "EvalCoord1fv", (PyCFunction)teglEvalCoord1fv, METH_O },
    { "EvalCoord2d", (PyCFunction)teglEvalCoord2d, METH_VARARGS },
    { "EvalCoord2f", (PyCFunction)teglEvalCoord2f, METH_VARARGS },
    { "EvalCoord2dv", (PyCFunction)teglEvalCoord2dv, METH_O },
    { "EvalCoord2fv", (PyCFunction)teglEvalCoord2fv, METH_O },
    { "MapGrid1d", (PyCFunction)teglMapGrid1d, METH_VARARGS },
    { "MapGrid1f", (PyCFunction)teglMapGrid1f, METH_VARARGS },
    { "MapGrid2d", (PyCFunction)teglMapGrid2d, METH_VARARGS },
    { "MapGrid2f", (PyCFunction)teglMapGrid2f, METH_VARARGS },
    { "EvalPoint1", (PyCFunction)teglEvalPoint1, METH_O },
    { "EvalPoint2", (PyCFunction)teglEvalPoint2, METH_VARARGS },
    { "EvalMesh1", (PyCFunction)teglEvalMesh1, METH_VARARGS },
    { "EvalMesh2", (PyCFunction)teglEvalMesh2, METH_VARARGS },
    { "Fogf", (PyCFunction)teglFogf, METH_VARARGS },
    { "Fogi", (PyCFunction)teglFogi, METH_VARARGS },
    { "Fogfv", (PyCFunction)teglFogfv, METH_VARARGS },
    { "Fogiv", (PyCFunction)teglFogiv, METH_VARARGS },
    { "FeedbackBuffer", (PyCFunction)teglFeedbackBuffer, METH_VARARGS },
    { "PassThrough", (PyCFunction)teglPassThrough, METH_O },
    { "SelectBuffer", (PyCFunction)teglSelectBuffer, METH_VARARGS },
    { "InitNames", (PyCFunction)teglInitNames, METH_NOARGS },
    { "LoadName", (PyCFunction)teglLoadName, METH_O },
    { "PushName", (PyCFunction)teglPushName, METH_O },
    { "PopName", (PyCFunction)teglPopName, METH_NOARGS },
    { "ActiveTextureARB", (PyCFunction)teglActiveTextureARB, METH_O },
    { "ClientActiveTextureARB", (PyCFunction)teglClientActiveTextureARB, METH_O },
    { "MultiTexCoord1dARB", (PyCFunction)teglMultiTexCoord1dARB, METH_VARARGS },
    { "MultiTexCoord1dvARB", (PyCFunction)teglMultiTexCoord1dvARB, METH_VARARGS },
    { "MultiTexCoord1fARB", (PyCFunction)teglMultiTexCoord1fARB, METH_VARARGS },
    { "MultiTexCoord1fvARB", (PyCFunction)teglMultiTexCoord1fvARB, METH_VARARGS },
    { "MultiTexCoord1iARB", (PyCFunction)teglMultiTexCoord1iARB, METH_VARARGS },
    { "MultiTexCoord1ivARB", (PyCFunction)teglMultiTexCoord1ivARB, METH_VARARGS },
    { "MultiTexCoord1sARB", (PyCFunction)teglMultiTexCoord1sARB, METH_VARARGS },
    { "MultiTexCoord1svARB", (PyCFunction)teglMultiTexCoord1svARB, METH_VARARGS },
    { "MultiTexCoord2dARB", (PyCFunction)teglMultiTexCoord2dARB, METH_VARARGS },
    { "MultiTexCoord2dvARB", (PyCFunction)teglMultiTexCoord2dvARB, METH_VARARGS },
    { "MultiTexCoord2fARB", (PyCFunction)teglMultiTexCoord2fARB, METH_VARARGS },
    { "MultiTexCoord2fvARB", (PyCFunction)teglMultiTexCoord2fvARB, METH_VARARGS },
    { "MultiTexCoord2iARB", (PyCFunction)teglMultiTexCoord2iARB, METH_VARARGS },
    { "MultiTexCoord2ivARB", (PyCFunction)teglMultiTexCoord2ivARB, METH_VARARGS },
    { "MultiTexCoord2sARB", (PyCFunction)teglMultiTexCoord2sARB, METH_VARARGS },
    { "MultiTexCoord2svARB", (PyCFunction)teglMultiTexCoord2svARB, METH_VARARGS },
    { "MultiTexCoord3dARB", (PyCFunction)teglMultiTexCoord3dARB, METH_VARARGS },
    { "MultiTexCoord3dvARB", (PyCFunction)teglMultiTexCoord3dvARB, METH_VARARGS },
    { "MultiTexCoord3fARB", (PyCFunction)teglMultiTexCoord3fARB, METH_VARARGS },
    { "MultiTexCoord3fvARB", (PyCFunction)teglMultiTexCoord3fvARB, METH_VARARGS },
    { "MultiTexCoord3iARB", (PyCFunction)teglMultiTexCoord3iARB, METH_VARARGS },
    { "MultiTexCoord3ivARB", (PyCFunction)teglMultiTexCoord3ivARB, METH_VARARGS },
    { "MultiTexCoord3sARB", (PyCFunction)teglMultiTexCoord3sARB, METH_VARARGS },
    { "MultiTexCoord3svARB", (PyCFunction)teglMultiTexCoord3svARB, METH_VARARGS },
    { "MultiTexCoord4dARB", (PyCFunction)teglMultiTexCoord4dARB, METH_VARARGS },
    { "MultiTexCoord4dvARB", (PyCFunction)teglMultiTexCoord4dvARB, METH_VARARGS },
    { "MultiTexCoord4fARB", (PyCFunction)teglMultiTexCoord4fARB, METH_VARARGS },
    { "MultiTexCoord4fvARB", (PyCFunction)teglMultiTexCoord4fvARB, METH_VARARGS },
    { "MultiTexCoord4iARB", (PyCFunction)teglMultiTexCoord4iARB, METH_VARARGS },
    { "MultiTexCoord4ivARB", (PyCFunction)teglMultiTexCoord4ivARB, METH_VARARGS },
    { "MultiTexCoord4sARB", (PyCFunction)teglMultiTexCoord4sARB, METH_VARARGS },
    { "MultiTexCoord4svARB", (PyCFunction)teglMultiTexCoord4svARB, METH_VARARGS },
    { "BindBufferARB", (PyCFunction)teglBindBufferARB, METH_VARARGS },
    { "DeleteBuffersARB", (PyCFunction)teglDeleteBuffersARB, METH_VARARGS },
    { "GenBuffersARB", (PyCFunction)teglGenBuffersARB, METH_VARARGS },
    { "IsBufferARB", (PyCFunction)teglIsBufferARB, METH_O },
    { "BufferDataARB", (PyCFunction)teglBufferDataARB, METH_VARARGS },
    { "BufferSubDataARB", (PyCFunction)teglBufferSubDataARB, METH_VARARGS },
    { "GetBufferSubDataARB", (PyCFunction)teglGetBufferSubDataARB, METH_VARARGS },
    { "MapBufferARB", (PyCFunction)teglMapBufferARB, METH_VARARGS },
    { "UnmapBufferARB", (PyCFunction)teglUnmapBufferARB, METH_O },
    { "GetBufferParameterivARB", (PyCFunction)teglGetBufferParameterivARB, METH_VARARGS },
    { "DeleteObjectARB", (PyCFunction)teglDeleteObjectARB, METH_O },
    { "GetHandleARB", (PyCFunction)teglGetHandleARB, METH_O },
    { "DetachObjectARB", (PyCFunction)teglDetachObjectARB, METH_VARARGS },
    { "CreateShaderObjectARB", (PyCFunction)teglCreateShaderObjectARB, METH_O },
    { "ShaderSourceARB", (PyCFunction)teglShaderSourceARB, METH_VARARGS },
    { "CompileShaderARB", (PyCFunction)teglCompileShaderARB, METH_O },
    { "CreateProgramObjectARB", (PyCFunction)teglCreateProgramObjectARB, METH_NOARGS },
    { "AttachObjectARB", (PyCFunction)teglAttachObjectARB, METH_VARARGS },
    { "LinkProgramARB", (PyCFunction)teglLinkProgramARB, METH_O },
    { "UseProgramObjectARB", (PyCFunction)teglUseProgramObjectARB, METH_O },
    { "ValidateProgramARB", (PyCFunction)teglValidateProgramARB, METH_O },
    { "Uniform1fARB", (PyCFunction)teglUniform1fARB, METH_VARARGS },
    { "Uniform2fARB", (PyCFunction)teglUniform2fARB, METH_VARARGS },
    { "Uniform3fARB", (PyCFunction)teglUniform3fARB, METH_VARARGS },
    { "Uniform4fARB", (PyCFunction)teglUniform4fARB, METH_VARARGS },
    { "Uniform1iARB", (PyCFunction)teglUniform1iARB, METH_VARARGS },
    { "Uniform2iARB", (PyCFunction)teglUniform2iARB, METH_VARARGS },
    { "Uniform3iARB", (PyCFunction)teglUniform3iARB, METH_VARARGS },
    { "Uniform4iARB", (PyCFunction)teglUniform4iARB, METH_VARARGS },
    { "Uniform1fvARB", (PyCFunction)teglUniform1fvARB, METH_VARARGS },
    { "Uniform2fvARB", (PyCFunction)teglUniform2fvARB, METH_VARARGS },
    { "Uniform3fvARB", (PyCFunction)teglUniform3fvARB, METH_VARARGS },
    { "Uniform4fvARB", (PyCFunction)teglUniform4fvARB, METH_VARARGS },
    { "Uniform1ivARB", (PyCFunction)teglUniform1ivARB, METH_VARARGS },
    { "Uniform2ivARB", (PyCFunction)teglUniform2ivARB, METH_VARARGS },
    { "Uniform3ivARB", (PyCFunction)teglUniform3ivARB, METH_VARARGS },
    { "Uniform4ivARB", (PyCFunction)teglUniform4ivARB, METH_VARARGS },
    { "UniformMatrix2fvARB", (PyCFunction)teglUniformMatrix2fvARB, METH_VARARGS },
    { "UniformMatrix3fvARB", (PyCFunction)teglUniformMatrix3fvARB, METH_VARARGS },
    { "UniformMatrix4fvARB", (PyCFunction)teglUniformMatrix4fvARB, METH_VARARGS },
    { "GetObjectParameterfvARB", (PyCFunction)teglGetObjectParameterfvARB, METH_VARARGS },
    { "GetObjectParameterivARB", (PyCFunction)teglGetObjectParameterivARB, METH_VARARGS },
    { "GetInfoLogARB", (PyCFunction)teglGetInfoLogARB, METH_VARARGS },
    { "GetAttachedObjectsARB", (PyCFunction)teglGetAttachedObjectsARB, METH_VARARGS },
    { "GetUniformLocationARB", (PyCFunction)teglGetUniformLocationARB, METH_VARARGS },
    { "GetActiveUniformARB", (PyCFunction)teglGetActiveUniformARB, METH_VARARGS },
    { "GetUniformfvARB", (PyCFunction)teglGetUniformfvARB, METH_VARARGS },
    { "GetUniformivARB", (PyCFunction)teglGetUniformivARB, METH_VARARGS },
    { "GetShaderSourceARB", (PyCFunction)teglGetShaderSourceARB, METH_VARARGS },
    { "BindAttribLocationARB", (PyCFunction)teglBindAttribLocationARB, METH_VARARGS },
    { "GetActiveAttribARB", (PyCFunction)teglGetActiveAttribARB, METH_VARARGS },
    { "GetAttribLocationARB", (PyCFunction)teglGetAttribLocationARB, METH_VARARGS },
    { "Build1DMipmapLevels", (PyCFunction)tegluBuild1DMipmapLevels, METH_VARARGS },
    { "Build1DMipmaps", (PyCFunction)tegluBuild1DMipmaps, METH_VARARGS },
    { "Build2DMipmapLevels", (PyCFunction)tegluBuild2DMipmapLevels, METH_VARARGS },
    { "Build2DMipmaps", (PyCFunction)tegluBuild2DMipmaps, METH_VARARGS },
    { "Build3DMipmapLevels", (PyCFunction)tegluBuild3DMipmapLevels, METH_VARARGS },
    { "Build3DMipmaps", (PyCFunction)tegluBuild3DMipmaps, METH_VARARGS },
    { "CheckExtension", (PyCFunction)tegluCheckExtension, METH_VARARGS },
    { "LookAt", (PyCFunction)tegluLookAt, METH_VARARGS },
    { "Ortho2D", (PyCFunction)tegluOrtho2D, METH_VARARGS },
    { "Perspective", (PyCFunction)tegluPerspective, METH_VARARGS },
    { "PickMatrix", (PyCFunction)tegluPickMatrix, METH_VARARGS },
    { "Project", (PyCFunction)tegluProject, METH_VARARGS },
    { "ScaleImage", (PyCFunction)tegluScaleImage, METH_VARARGS },
    { "UnProject", (PyCFunction)tegluUnProject, METH_VARARGS },
    { "UnProject4", (PyCFunction)tegluUnProject4, METH_VARARGS },
    { 0 }   /* Sentinel */
};

PyMODINIT_FUNC init_renpy_tegl(void) {
    GLenum err;
    PyObject* mod = Py_InitModule("_renpy_tegl", module_methods);

    PyModule_AddIntConstant(mod,"FALSE",GL_FALSE);
    PyModule_AddIntConstant(mod,"TRUE",GL_TRUE);
    PyModule_AddIntConstant(mod,"BYTE",GL_BYTE);
    PyModule_AddIntConstant(mod,"UNSIGNED_BYTE",GL_UNSIGNED_BYTE);
    PyModule_AddIntConstant(mod,"SHORT",GL_SHORT);
    PyModule_AddIntConstant(mod,"UNSIGNED_SHORT",GL_UNSIGNED_SHORT);
    PyModule_AddIntConstant(mod,"INT",GL_INT);
    PyModule_AddIntConstant(mod,"UNSIGNED_INT",GL_UNSIGNED_INT);
    PyModule_AddIntConstant(mod,"FLOAT",GL_FLOAT);
    PyModule_AddIntConstant(mod,"_2_BYTES",GL_2_BYTES);
    PyModule_AddIntConstant(mod,"_3_BYTES",GL_3_BYTES);
    PyModule_AddIntConstant(mod,"_4_BYTES",GL_4_BYTES);
    PyModule_AddIntConstant(mod,"DOUBLE",GL_DOUBLE);
    PyModule_AddIntConstant(mod,"POINTS",GL_POINTS);
    PyModule_AddIntConstant(mod,"LINES",GL_LINES);
    PyModule_AddIntConstant(mod,"LINE_LOOP",GL_LINE_LOOP);
    PyModule_AddIntConstant(mod,"LINE_STRIP",GL_LINE_STRIP);
    PyModule_AddIntConstant(mod,"TRIANGLES",GL_TRIANGLES);
    PyModule_AddIntConstant(mod,"TRIANGLE_STRIP",GL_TRIANGLE_STRIP);
    PyModule_AddIntConstant(mod,"TRIANGLE_FAN",GL_TRIANGLE_FAN);
    PyModule_AddIntConstant(mod,"QUADS",GL_QUADS);
    PyModule_AddIntConstant(mod,"QUAD_STRIP",GL_QUAD_STRIP);
    PyModule_AddIntConstant(mod,"POLYGON",GL_POLYGON);
    PyModule_AddIntConstant(mod,"VERTEX_ARRAY",GL_VERTEX_ARRAY);
    PyModule_AddIntConstant(mod,"NORMAL_ARRAY",GL_NORMAL_ARRAY);
    PyModule_AddIntConstant(mod,"COLOR_ARRAY",GL_COLOR_ARRAY);
    PyModule_AddIntConstant(mod,"INDEX_ARRAY",GL_INDEX_ARRAY);
    PyModule_AddIntConstant(mod,"TEXTURE_COORD_ARRAY",GL_TEXTURE_COORD_ARRAY);
    PyModule_AddIntConstant(mod,"EDGE_FLAG_ARRAY",GL_EDGE_FLAG_ARRAY);
    PyModule_AddIntConstant(mod,"VERTEX_ARRAY_SIZE",GL_VERTEX_ARRAY_SIZE);
    PyModule_AddIntConstant(mod,"VERTEX_ARRAY_TYPE",GL_VERTEX_ARRAY_TYPE);
    PyModule_AddIntConstant(mod,"VERTEX_ARRAY_STRIDE",GL_VERTEX_ARRAY_STRIDE);
    PyModule_AddIntConstant(mod,"NORMAL_ARRAY_TYPE",GL_NORMAL_ARRAY_TYPE);
    PyModule_AddIntConstant(mod,"NORMAL_ARRAY_STRIDE",GL_NORMAL_ARRAY_STRIDE);
    PyModule_AddIntConstant(mod,"COLOR_ARRAY_SIZE",GL_COLOR_ARRAY_SIZE);
    PyModule_AddIntConstant(mod,"COLOR_ARRAY_TYPE",GL_COLOR_ARRAY_TYPE);
    PyModule_AddIntConstant(mod,"COLOR_ARRAY_STRIDE",GL_COLOR_ARRAY_STRIDE);
    PyModule_AddIntConstant(mod,"INDEX_ARRAY_TYPE",GL_INDEX_ARRAY_TYPE);
    PyModule_AddIntConstant(mod,"INDEX_ARRAY_STRIDE",GL_INDEX_ARRAY_STRIDE);
    PyModule_AddIntConstant(mod,"TEXTURE_COORD_ARRAY_SIZE",GL_TEXTURE_COORD_ARRAY_SIZE);
    PyModule_AddIntConstant(mod,"TEXTURE_COORD_ARRAY_TYPE",GL_TEXTURE_COORD_ARRAY_TYPE);
    PyModule_AddIntConstant(mod,"TEXTURE_COORD_ARRAY_STRIDE",GL_TEXTURE_COORD_ARRAY_STRIDE);
    PyModule_AddIntConstant(mod,"EDGE_FLAG_ARRAY_STRIDE",GL_EDGE_FLAG_ARRAY_STRIDE);
    PyModule_AddIntConstant(mod,"VERTEX_ARRAY_POINTER",GL_VERTEX_ARRAY_POINTER);
    PyModule_AddIntConstant(mod,"NORMAL_ARRAY_POINTER",GL_NORMAL_ARRAY_POINTER);
    PyModule_AddIntConstant(mod,"COLOR_ARRAY_POINTER",GL_COLOR_ARRAY_POINTER);
    PyModule_AddIntConstant(mod,"INDEX_ARRAY_POINTER",GL_INDEX_ARRAY_POINTER);
    PyModule_AddIntConstant(mod,"TEXTURE_COORD_ARRAY_POINTER",GL_TEXTURE_COORD_ARRAY_POINTER);
    PyModule_AddIntConstant(mod,"EDGE_FLAG_ARRAY_POINTER",GL_EDGE_FLAG_ARRAY_POINTER);
    PyModule_AddIntConstant(mod,"V2F",GL_V2F);
    PyModule_AddIntConstant(mod,"V3F",GL_V3F);
    PyModule_AddIntConstant(mod,"C4UB_V2F",GL_C4UB_V2F);
    PyModule_AddIntConstant(mod,"C4UB_V3F",GL_C4UB_V3F);
    PyModule_AddIntConstant(mod,"C3F_V3F",GL_C3F_V3F);
    PyModule_AddIntConstant(mod,"N3F_V3F",GL_N3F_V3F);
    PyModule_AddIntConstant(mod,"C4F_N3F_V3F",GL_C4F_N3F_V3F);
    PyModule_AddIntConstant(mod,"T2F_V3F",GL_T2F_V3F);
    PyModule_AddIntConstant(mod,"T4F_V4F",GL_T4F_V4F);
    PyModule_AddIntConstant(mod,"T2F_C4UB_V3F",GL_T2F_C4UB_V3F);
    PyModule_AddIntConstant(mod,"T2F_C3F_V3F",GL_T2F_C3F_V3F);
    PyModule_AddIntConstant(mod,"T2F_N3F_V3F",GL_T2F_N3F_V3F);
    PyModule_AddIntConstant(mod,"T2F_C4F_N3F_V3F",GL_T2F_C4F_N3F_V3F);
    PyModule_AddIntConstant(mod,"T4F_C4F_N3F_V4F",GL_T4F_C4F_N3F_V4F);
    PyModule_AddIntConstant(mod,"MATRIX_MODE",GL_MATRIX_MODE);
    PyModule_AddIntConstant(mod,"MODELVIEW",GL_MODELVIEW);
    PyModule_AddIntConstant(mod,"PROJECTION",GL_PROJECTION);
    PyModule_AddIntConstant(mod,"TEXTURE",GL_TEXTURE);
    PyModule_AddIntConstant(mod,"POINT_SMOOTH",GL_POINT_SMOOTH);
    PyModule_AddIntConstant(mod,"POINT_SIZE",GL_POINT_SIZE);
    PyModule_AddIntConstant(mod,"POINT_SIZE_GRANULARITY",GL_POINT_SIZE_GRANULARITY);
    PyModule_AddIntConstant(mod,"POINT_SIZE_RANGE",GL_POINT_SIZE_RANGE);
    PyModule_AddIntConstant(mod,"LINE_SMOOTH",GL_LINE_SMOOTH);
    PyModule_AddIntConstant(mod,"LINE_STIPPLE",GL_LINE_STIPPLE);
    PyModule_AddIntConstant(mod,"LINE_STIPPLE_PATTERN",GL_LINE_STIPPLE_PATTERN);
    PyModule_AddIntConstant(mod,"LINE_STIPPLE_REPEAT",GL_LINE_STIPPLE_REPEAT);
    PyModule_AddIntConstant(mod,"LINE_WIDTH",GL_LINE_WIDTH);
    PyModule_AddIntConstant(mod,"LINE_WIDTH_GRANULARITY",GL_LINE_WIDTH_GRANULARITY);
    PyModule_AddIntConstant(mod,"LINE_WIDTH_RANGE",GL_LINE_WIDTH_RANGE);
    PyModule_AddIntConstant(mod,"POINT",GL_POINT);
    PyModule_AddIntConstant(mod,"LINE",GL_LINE);
    PyModule_AddIntConstant(mod,"FILL",GL_FILL);
    PyModule_AddIntConstant(mod,"CW",GL_CW);
    PyModule_AddIntConstant(mod,"CCW",GL_CCW);
    PyModule_AddIntConstant(mod,"FRONT",GL_FRONT);
    PyModule_AddIntConstant(mod,"BACK",GL_BACK);
    PyModule_AddIntConstant(mod,"POLYGON_MODE",GL_POLYGON_MODE);
    PyModule_AddIntConstant(mod,"POLYGON_SMOOTH",GL_POLYGON_SMOOTH);
    PyModule_AddIntConstant(mod,"POLYGON_STIPPLE",GL_POLYGON_STIPPLE);
    PyModule_AddIntConstant(mod,"EDGE_FLAG",GL_EDGE_FLAG);
    PyModule_AddIntConstant(mod,"CULL_FACE",GL_CULL_FACE);
    PyModule_AddIntConstant(mod,"CULL_FACE_MODE",GL_CULL_FACE_MODE);
    PyModule_AddIntConstant(mod,"FRONT_FACE",GL_FRONT_FACE);
    PyModule_AddIntConstant(mod,"POLYGON_OFFSET_FACTOR",GL_POLYGON_OFFSET_FACTOR);
    PyModule_AddIntConstant(mod,"POLYGON_OFFSET_UNITS",GL_POLYGON_OFFSET_UNITS);
    PyModule_AddIntConstant(mod,"POLYGON_OFFSET_POINT",GL_POLYGON_OFFSET_POINT);
    PyModule_AddIntConstant(mod,"POLYGON_OFFSET_LINE",GL_POLYGON_OFFSET_LINE);
    PyModule_AddIntConstant(mod,"POLYGON_OFFSET_FILL",GL_POLYGON_OFFSET_FILL);
    PyModule_AddIntConstant(mod,"COMPILE",GL_COMPILE);
    PyModule_AddIntConstant(mod,"COMPILE_AND_EXECUTE",GL_COMPILE_AND_EXECUTE);
    PyModule_AddIntConstant(mod,"LIST_BASE",GL_LIST_BASE);
    PyModule_AddIntConstant(mod,"LIST_INDEX",GL_LIST_INDEX);
    PyModule_AddIntConstant(mod,"LIST_MODE",GL_LIST_MODE);
    PyModule_AddIntConstant(mod,"NEVER",GL_NEVER);
    PyModule_AddIntConstant(mod,"LESS",GL_LESS);
    PyModule_AddIntConstant(mod,"EQUAL",GL_EQUAL);
    PyModule_AddIntConstant(mod,"LEQUAL",GL_LEQUAL);
    PyModule_AddIntConstant(mod,"GREATER",GL_GREATER);
    PyModule_AddIntConstant(mod,"NOTEQUAL",GL_NOTEQUAL);
    PyModule_AddIntConstant(mod,"GEQUAL",GL_GEQUAL);
    PyModule_AddIntConstant(mod,"ALWAYS",GL_ALWAYS);
    PyModule_AddIntConstant(mod,"DEPTH_TEST",GL_DEPTH_TEST);
    PyModule_AddIntConstant(mod,"DEPTH_BITS",GL_DEPTH_BITS);
    PyModule_AddIntConstant(mod,"DEPTH_CLEAR_VALUE",GL_DEPTH_CLEAR_VALUE);
    PyModule_AddIntConstant(mod,"DEPTH_FUNC",GL_DEPTH_FUNC);
    PyModule_AddIntConstant(mod,"DEPTH_RANGE",GL_DEPTH_RANGE);
    PyModule_AddIntConstant(mod,"DEPTH_WRITEMASK",GL_DEPTH_WRITEMASK);
    PyModule_AddIntConstant(mod,"DEPTH_COMPONENT",GL_DEPTH_COMPONENT);
    PyModule_AddIntConstant(mod,"LIGHTING",GL_LIGHTING);
    PyModule_AddIntConstant(mod,"LIGHT0",GL_LIGHT0);
    PyModule_AddIntConstant(mod,"LIGHT1",GL_LIGHT1);
    PyModule_AddIntConstant(mod,"LIGHT2",GL_LIGHT2);
    PyModule_AddIntConstant(mod,"LIGHT3",GL_LIGHT3);
    PyModule_AddIntConstant(mod,"LIGHT4",GL_LIGHT4);
    PyModule_AddIntConstant(mod,"LIGHT5",GL_LIGHT5);
    PyModule_AddIntConstant(mod,"LIGHT6",GL_LIGHT6);
    PyModule_AddIntConstant(mod,"LIGHT7",GL_LIGHT7);
    PyModule_AddIntConstant(mod,"SPOT_EXPONENT",GL_SPOT_EXPONENT);
    PyModule_AddIntConstant(mod,"SPOT_CUTOFF",GL_SPOT_CUTOFF);
    PyModule_AddIntConstant(mod,"CONSTANT_ATTENUATION",GL_CONSTANT_ATTENUATION);
    PyModule_AddIntConstant(mod,"LINEAR_ATTENUATION",GL_LINEAR_ATTENUATION);
    PyModule_AddIntConstant(mod,"QUADRATIC_ATTENUATION",GL_QUADRATIC_ATTENUATION);
    PyModule_AddIntConstant(mod,"AMBIENT",GL_AMBIENT);
    PyModule_AddIntConstant(mod,"DIFFUSE",GL_DIFFUSE);
    PyModule_AddIntConstant(mod,"SPECULAR",GL_SPECULAR);
    PyModule_AddIntConstant(mod,"SHININESS",GL_SHININESS);
    PyModule_AddIntConstant(mod,"EMISSION",GL_EMISSION);
    PyModule_AddIntConstant(mod,"POSITION",GL_POSITION);
    PyModule_AddIntConstant(mod,"SPOT_DIRECTION",GL_SPOT_DIRECTION);
    PyModule_AddIntConstant(mod,"AMBIENT_AND_DIFFUSE",GL_AMBIENT_AND_DIFFUSE);
    PyModule_AddIntConstant(mod,"COLOR_INDEXES",GL_COLOR_INDEXES);
    PyModule_AddIntConstant(mod,"LIGHT_MODEL_TWO_SIDE",GL_LIGHT_MODEL_TWO_SIDE);
    PyModule_AddIntConstant(mod,"LIGHT_MODEL_LOCAL_VIEWER",GL_LIGHT_MODEL_LOCAL_VIEWER);
    PyModule_AddIntConstant(mod,"LIGHT_MODEL_AMBIENT",GL_LIGHT_MODEL_AMBIENT);
    PyModule_AddIntConstant(mod,"FRONT_AND_BACK",GL_FRONT_AND_BACK);
    PyModule_AddIntConstant(mod,"SHADE_MODEL",GL_SHADE_MODEL);
    PyModule_AddIntConstant(mod,"FLAT",GL_FLAT);
    PyModule_AddIntConstant(mod,"SMOOTH",GL_SMOOTH);
    PyModule_AddIntConstant(mod,"COLOR_MATERIAL",GL_COLOR_MATERIAL);
    PyModule_AddIntConstant(mod,"COLOR_MATERIAL_FACE",GL_COLOR_MATERIAL_FACE);
    PyModule_AddIntConstant(mod,"COLOR_MATERIAL_PARAMETER",GL_COLOR_MATERIAL_PARAMETER);
    PyModule_AddIntConstant(mod,"NORMALIZE",GL_NORMALIZE);
    PyModule_AddIntConstant(mod,"CLIP_PLANE0",GL_CLIP_PLANE0);
    PyModule_AddIntConstant(mod,"CLIP_PLANE1",GL_CLIP_PLANE1);
    PyModule_AddIntConstant(mod,"CLIP_PLANE2",GL_CLIP_PLANE2);
    PyModule_AddIntConstant(mod,"CLIP_PLANE3",GL_CLIP_PLANE3);
    PyModule_AddIntConstant(mod,"CLIP_PLANE4",GL_CLIP_PLANE4);
    PyModule_AddIntConstant(mod,"CLIP_PLANE5",GL_CLIP_PLANE5);
    PyModule_AddIntConstant(mod,"ACCUM_RED_BITS",GL_ACCUM_RED_BITS);
    PyModule_AddIntConstant(mod,"ACCUM_GREEN_BITS",GL_ACCUM_GREEN_BITS);
    PyModule_AddIntConstant(mod,"ACCUM_BLUE_BITS",GL_ACCUM_BLUE_BITS);
    PyModule_AddIntConstant(mod,"ACCUM_ALPHA_BITS",GL_ACCUM_ALPHA_BITS);
    PyModule_AddIntConstant(mod,"ACCUM_CLEAR_VALUE",GL_ACCUM_CLEAR_VALUE);
    PyModule_AddIntConstant(mod,"ACCUM",GL_ACCUM);
    PyModule_AddIntConstant(mod,"ADD",GL_ADD);
    PyModule_AddIntConstant(mod,"LOAD",GL_LOAD);
    PyModule_AddIntConstant(mod,"MULT",GL_MULT);
    PyModule_AddIntConstant(mod,"RETURN",GL_RETURN);
    PyModule_AddIntConstant(mod,"ALPHA_TEST",GL_ALPHA_TEST);
    PyModule_AddIntConstant(mod,"ALPHA_TEST_REF",GL_ALPHA_TEST_REF);
    PyModule_AddIntConstant(mod,"ALPHA_TEST_FUNC",GL_ALPHA_TEST_FUNC);
    PyModule_AddIntConstant(mod,"BLEND",GL_BLEND);
    PyModule_AddIntConstant(mod,"BLEND_SRC",GL_BLEND_SRC);
    PyModule_AddIntConstant(mod,"BLEND_DST",GL_BLEND_DST);
    PyModule_AddIntConstant(mod,"ZERO",GL_ZERO);
    PyModule_AddIntConstant(mod,"ONE",GL_ONE);
    PyModule_AddIntConstant(mod,"SRC_COLOR",GL_SRC_COLOR);
    PyModule_AddIntConstant(mod,"ONE_MINUS_SRC_COLOR",GL_ONE_MINUS_SRC_COLOR);
    PyModule_AddIntConstant(mod,"SRC_ALPHA",GL_SRC_ALPHA);
    PyModule_AddIntConstant(mod,"ONE_MINUS_SRC_ALPHA",GL_ONE_MINUS_SRC_ALPHA);
    PyModule_AddIntConstant(mod,"DST_ALPHA",GL_DST_ALPHA);
    PyModule_AddIntConstant(mod,"ONE_MINUS_DST_ALPHA",GL_ONE_MINUS_DST_ALPHA);
    PyModule_AddIntConstant(mod,"DST_COLOR",GL_DST_COLOR);
    PyModule_AddIntConstant(mod,"ONE_MINUS_DST_COLOR",GL_ONE_MINUS_DST_COLOR);
    PyModule_AddIntConstant(mod,"SRC_ALPHA_SATURATE",GL_SRC_ALPHA_SATURATE);
    PyModule_AddIntConstant(mod,"FEEDBACK",GL_FEEDBACK);
    PyModule_AddIntConstant(mod,"RENDER",GL_RENDER);
    PyModule_AddIntConstant(mod,"SELECT",GL_SELECT);
    PyModule_AddIntConstant(mod,"_2D",GL_2D);
    PyModule_AddIntConstant(mod,"_3D",GL_3D);
    PyModule_AddIntConstant(mod,"_3D_COLOR",GL_3D_COLOR);
    PyModule_AddIntConstant(mod,"_3D_COLOR_TEXTURE",GL_3D_COLOR_TEXTURE);
    PyModule_AddIntConstant(mod,"_4D_COLOR_TEXTURE",GL_4D_COLOR_TEXTURE);
    PyModule_AddIntConstant(mod,"POINT_TOKEN",GL_POINT_TOKEN);
    PyModule_AddIntConstant(mod,"LINE_TOKEN",GL_LINE_TOKEN);
    PyModule_AddIntConstant(mod,"LINE_RESET_TOKEN",GL_LINE_RESET_TOKEN);
    PyModule_AddIntConstant(mod,"POLYGON_TOKEN",GL_POLYGON_TOKEN);
    PyModule_AddIntConstant(mod,"BITMAP_TOKEN",GL_BITMAP_TOKEN);
    PyModule_AddIntConstant(mod,"DRAW_PIXEL_TOKEN",GL_DRAW_PIXEL_TOKEN);
    PyModule_AddIntConstant(mod,"COPY_PIXEL_TOKEN",GL_COPY_PIXEL_TOKEN);
    PyModule_AddIntConstant(mod,"PASS_THROUGH_TOKEN",GL_PASS_THROUGH_TOKEN);
    PyModule_AddIntConstant(mod,"FEEDBACK_BUFFER_POINTER",GL_FEEDBACK_BUFFER_POINTER);
    PyModule_AddIntConstant(mod,"FEEDBACK_BUFFER_SIZE",GL_FEEDBACK_BUFFER_SIZE);
    PyModule_AddIntConstant(mod,"FEEDBACK_BUFFER_TYPE",GL_FEEDBACK_BUFFER_TYPE);
    PyModule_AddIntConstant(mod,"SELECTION_BUFFER_POINTER",GL_SELECTION_BUFFER_POINTER);
    PyModule_AddIntConstant(mod,"SELECTION_BUFFER_SIZE",GL_SELECTION_BUFFER_SIZE);
    PyModule_AddIntConstant(mod,"FOG",GL_FOG);
    PyModule_AddIntConstant(mod,"FOG_MODE",GL_FOG_MODE);
    PyModule_AddIntConstant(mod,"FOG_DENSITY",GL_FOG_DENSITY);
    PyModule_AddIntConstant(mod,"FOG_COLOR",GL_FOG_COLOR);
    PyModule_AddIntConstant(mod,"FOG_INDEX",GL_FOG_INDEX);
    PyModule_AddIntConstant(mod,"FOG_START",GL_FOG_START);
    PyModule_AddIntConstant(mod,"FOG_END",GL_FOG_END);
    PyModule_AddIntConstant(mod,"LINEAR",GL_LINEAR);
    PyModule_AddIntConstant(mod,"EXP",GL_EXP);
    PyModule_AddIntConstant(mod,"EXP2",GL_EXP2);
    PyModule_AddIntConstant(mod,"LOGIC_OP",GL_LOGIC_OP);
    PyModule_AddIntConstant(mod,"INDEX_LOGIC_OP",GL_INDEX_LOGIC_OP);
    PyModule_AddIntConstant(mod,"COLOR_LOGIC_OP",GL_COLOR_LOGIC_OP);
    PyModule_AddIntConstant(mod,"LOGIC_OP_MODE",GL_LOGIC_OP_MODE);
    PyModule_AddIntConstant(mod,"CLEAR",GL_CLEAR);
    PyModule_AddIntConstant(mod,"SET",GL_SET);
    PyModule_AddIntConstant(mod,"COPY",GL_COPY);
    PyModule_AddIntConstant(mod,"COPY_INVERTED",GL_COPY_INVERTED);
    PyModule_AddIntConstant(mod,"NOOP",GL_NOOP);
    PyModule_AddIntConstant(mod,"INVERT",GL_INVERT);
    PyModule_AddIntConstant(mod,"AND",GL_AND);
    PyModule_AddIntConstant(mod,"NAND",GL_NAND);
    PyModule_AddIntConstant(mod,"OR",GL_OR);
    PyModule_AddIntConstant(mod,"NOR",GL_NOR);
    PyModule_AddIntConstant(mod,"XOR",GL_XOR);
    PyModule_AddIntConstant(mod,"EQUIV",GL_EQUIV);
    PyModule_AddIntConstant(mod,"AND_REVERSE",GL_AND_REVERSE);
    PyModule_AddIntConstant(mod,"AND_INVERTED",GL_AND_INVERTED);
    PyModule_AddIntConstant(mod,"OR_REVERSE",GL_OR_REVERSE);
    PyModule_AddIntConstant(mod,"OR_INVERTED",GL_OR_INVERTED);
    PyModule_AddIntConstant(mod,"STENCIL_BITS",GL_STENCIL_BITS);
    PyModule_AddIntConstant(mod,"STENCIL_TEST",GL_STENCIL_TEST);
    PyModule_AddIntConstant(mod,"STENCIL_CLEAR_VALUE",GL_STENCIL_CLEAR_VALUE);
    PyModule_AddIntConstant(mod,"STENCIL_FUNC",GL_STENCIL_FUNC);
    PyModule_AddIntConstant(mod,"STENCIL_VALUE_MASK",GL_STENCIL_VALUE_MASK);
    PyModule_AddIntConstant(mod,"STENCIL_FAIL",GL_STENCIL_FAIL);
    PyModule_AddIntConstant(mod,"STENCIL_PASS_DEPTH_FAIL",GL_STENCIL_PASS_DEPTH_FAIL);
    PyModule_AddIntConstant(mod,"STENCIL_PASS_DEPTH_PASS",GL_STENCIL_PASS_DEPTH_PASS);
    PyModule_AddIntConstant(mod,"STENCIL_REF",GL_STENCIL_REF);
    PyModule_AddIntConstant(mod,"STENCIL_WRITEMASK",GL_STENCIL_WRITEMASK);
    PyModule_AddIntConstant(mod,"STENCIL_INDEX",GL_STENCIL_INDEX);
    PyModule_AddIntConstant(mod,"KEEP",GL_KEEP);
    PyModule_AddIntConstant(mod,"REPLACE",GL_REPLACE);
    PyModule_AddIntConstant(mod,"INCR",GL_INCR);
    PyModule_AddIntConstant(mod,"DECR",GL_DECR);
    PyModule_AddIntConstant(mod,"NONE",GL_NONE);
    PyModule_AddIntConstant(mod,"LEFT",GL_LEFT);
    PyModule_AddIntConstant(mod,"RIGHT",GL_RIGHT);
    PyModule_AddIntConstant(mod,"FRONT_LEFT",GL_FRONT_LEFT);
    PyModule_AddIntConstant(mod,"FRONT_RIGHT",GL_FRONT_RIGHT);
    PyModule_AddIntConstant(mod,"BACK_LEFT",GL_BACK_LEFT);
    PyModule_AddIntConstant(mod,"BACK_RIGHT",GL_BACK_RIGHT);
    PyModule_AddIntConstant(mod,"AUX0",GL_AUX0);
    PyModule_AddIntConstant(mod,"AUX1",GL_AUX1);
    PyModule_AddIntConstant(mod,"AUX2",GL_AUX2);
    PyModule_AddIntConstant(mod,"AUX3",GL_AUX3);
    PyModule_AddIntConstant(mod,"COLOR_INDEX",GL_COLOR_INDEX);
    PyModule_AddIntConstant(mod,"RED",GL_RED);
    PyModule_AddIntConstant(mod,"GREEN",GL_GREEN);
    PyModule_AddIntConstant(mod,"BLUE",GL_BLUE);
    PyModule_AddIntConstant(mod,"ALPHA",GL_ALPHA);
    PyModule_AddIntConstant(mod,"LUMINANCE",GL_LUMINANCE);
    PyModule_AddIntConstant(mod,"LUMINANCE_ALPHA",GL_LUMINANCE_ALPHA);
    PyModule_AddIntConstant(mod,"ALPHA_BITS",GL_ALPHA_BITS);
    PyModule_AddIntConstant(mod,"RED_BITS",GL_RED_BITS);
    PyModule_AddIntConstant(mod,"GREEN_BITS",GL_GREEN_BITS);
    PyModule_AddIntConstant(mod,"BLUE_BITS",GL_BLUE_BITS);
    PyModule_AddIntConstant(mod,"INDEX_BITS",GL_INDEX_BITS);
    PyModule_AddIntConstant(mod,"SUBPIXEL_BITS",GL_SUBPIXEL_BITS);
    PyModule_AddIntConstant(mod,"AUX_BUFFERS",GL_AUX_BUFFERS);
    PyModule_AddIntConstant(mod,"READ_BUFFER",GL_READ_BUFFER);
    PyModule_AddIntConstant(mod,"DRAW_BUFFER",GL_DRAW_BUFFER);
    PyModule_AddIntConstant(mod,"DOUBLEBUFFER",GL_DOUBLEBUFFER);
    PyModule_AddIntConstant(mod,"STEREO",GL_STEREO);
    PyModule_AddIntConstant(mod,"BITMAP",GL_BITMAP);
    PyModule_AddIntConstant(mod,"COLOR",GL_COLOR);
    PyModule_AddIntConstant(mod,"DEPTH",GL_DEPTH);
    PyModule_AddIntConstant(mod,"STENCIL",GL_STENCIL);
    PyModule_AddIntConstant(mod,"DITHER",GL_DITHER);
    PyModule_AddIntConstant(mod,"RGB",GL_RGB);
    PyModule_AddIntConstant(mod,"RGBA",GL_RGBA);
    PyModule_AddIntConstant(mod,"MAX_LIST_NESTING",GL_MAX_LIST_NESTING);
    PyModule_AddIntConstant(mod,"MAX_EVAL_ORDER",GL_MAX_EVAL_ORDER);
    PyModule_AddIntConstant(mod,"MAX_LIGHTS",GL_MAX_LIGHTS);
    PyModule_AddIntConstant(mod,"MAX_CLIP_PLANES",GL_MAX_CLIP_PLANES);
    PyModule_AddIntConstant(mod,"MAX_TEXTURE_SIZE",GL_MAX_TEXTURE_SIZE);
    PyModule_AddIntConstant(mod,"MAX_PIXEL_MAP_TABLE",GL_MAX_PIXEL_MAP_TABLE);
    PyModule_AddIntConstant(mod,"MAX_ATTRIB_STACK_DEPTH",GL_MAX_ATTRIB_STACK_DEPTH);
    PyModule_AddIntConstant(mod,"MAX_MODELVIEW_STACK_DEPTH",GL_MAX_MODELVIEW_STACK_DEPTH);
    PyModule_AddIntConstant(mod,"MAX_NAME_STACK_DEPTH",GL_MAX_NAME_STACK_DEPTH);
    PyModule_AddIntConstant(mod,"MAX_PROJECTION_STACK_DEPTH",GL_MAX_PROJECTION_STACK_DEPTH);
    PyModule_AddIntConstant(mod,"MAX_TEXTURE_STACK_DEPTH",GL_MAX_TEXTURE_STACK_DEPTH);
    PyModule_AddIntConstant(mod,"MAX_VIEWPORT_DIMS",GL_MAX_VIEWPORT_DIMS);
    PyModule_AddIntConstant(mod,"MAX_CLIENT_ATTRIB_STACK_DEPTH",GL_MAX_CLIENT_ATTRIB_STACK_DEPTH);
    PyModule_AddIntConstant(mod,"ATTRIB_STACK_DEPTH",GL_ATTRIB_STACK_DEPTH);
    PyModule_AddIntConstant(mod,"CLIENT_ATTRIB_STACK_DEPTH",GL_CLIENT_ATTRIB_STACK_DEPTH);
    PyModule_AddIntConstant(mod,"COLOR_CLEAR_VALUE",GL_COLOR_CLEAR_VALUE);
    PyModule_AddIntConstant(mod,"COLOR_WRITEMASK",GL_COLOR_WRITEMASK);
    PyModule_AddIntConstant(mod,"CURRENT_INDEX",GL_CURRENT_INDEX);
    PyModule_AddIntConstant(mod,"CURRENT_COLOR",GL_CURRENT_COLOR);
    PyModule_AddIntConstant(mod,"CURRENT_NORMAL",GL_CURRENT_NORMAL);
    PyModule_AddIntConstant(mod,"CURRENT_RASTER_COLOR",GL_CURRENT_RASTER_COLOR);
    PyModule_AddIntConstant(mod,"CURRENT_RASTER_DISTANCE",GL_CURRENT_RASTER_DISTANCE);
    PyModule_AddIntConstant(mod,"CURRENT_RASTER_INDEX",GL_CURRENT_RASTER_INDEX);
    PyModule_AddIntConstant(mod,"CURRENT_RASTER_POSITION",GL_CURRENT_RASTER_POSITION);
    PyModule_AddIntConstant(mod,"CURRENT_RASTER_TEXTURE_COORDS",GL_CURRENT_RASTER_TEXTURE_COORDS);
    PyModule_AddIntConstant(mod,"CURRENT_RASTER_POSITION_VALID",GL_CURRENT_RASTER_POSITION_VALID);
    PyModule_AddIntConstant(mod,"CURRENT_TEXTURE_COORDS",GL_CURRENT_TEXTURE_COORDS);
    PyModule_AddIntConstant(mod,"INDEX_CLEAR_VALUE",GL_INDEX_CLEAR_VALUE);
    PyModule_AddIntConstant(mod,"INDEX_MODE",GL_INDEX_MODE);
    PyModule_AddIntConstant(mod,"INDEX_WRITEMASK",GL_INDEX_WRITEMASK);
    PyModule_AddIntConstant(mod,"MODELVIEW_MATRIX",GL_MODELVIEW_MATRIX);
    PyModule_AddIntConstant(mod,"MODELVIEW_STACK_DEPTH",GL_MODELVIEW_STACK_DEPTH);
    PyModule_AddIntConstant(mod,"NAME_STACK_DEPTH",GL_NAME_STACK_DEPTH);
    PyModule_AddIntConstant(mod,"PROJECTION_MATRIX",GL_PROJECTION_MATRIX);
    PyModule_AddIntConstant(mod,"PROJECTION_STACK_DEPTH",GL_PROJECTION_STACK_DEPTH);
    PyModule_AddIntConstant(mod,"RENDER_MODE",GL_RENDER_MODE);
    PyModule_AddIntConstant(mod,"RGBA_MODE",GL_RGBA_MODE);
    PyModule_AddIntConstant(mod,"TEXTURE_MATRIX",GL_TEXTURE_MATRIX);
    PyModule_AddIntConstant(mod,"TEXTURE_STACK_DEPTH",GL_TEXTURE_STACK_DEPTH);
    PyModule_AddIntConstant(mod,"VIEWPORT",GL_VIEWPORT);
    PyModule_AddIntConstant(mod,"AUTO_NORMAL",GL_AUTO_NORMAL);
    PyModule_AddIntConstant(mod,"MAP1_COLOR_4",GL_MAP1_COLOR_4);
    PyModule_AddIntConstant(mod,"MAP1_INDEX",GL_MAP1_INDEX);
    PyModule_AddIntConstant(mod,"MAP1_NORMAL",GL_MAP1_NORMAL);
    PyModule_AddIntConstant(mod,"MAP1_TEXTURE_COORD_1",GL_MAP1_TEXTURE_COORD_1);
    PyModule_AddIntConstant(mod,"MAP1_TEXTURE_COORD_2",GL_MAP1_TEXTURE_COORD_2);
    PyModule_AddIntConstant(mod,"MAP1_TEXTURE_COORD_3",GL_MAP1_TEXTURE_COORD_3);
    PyModule_AddIntConstant(mod,"MAP1_TEXTURE_COORD_4",GL_MAP1_TEXTURE_COORD_4);
    PyModule_AddIntConstant(mod,"MAP1_VERTEX_3",GL_MAP1_VERTEX_3);
    PyModule_AddIntConstant(mod,"MAP1_VERTEX_4",GL_MAP1_VERTEX_4);
    PyModule_AddIntConstant(mod,"MAP2_COLOR_4",GL_MAP2_COLOR_4);
    PyModule_AddIntConstant(mod,"MAP2_INDEX",GL_MAP2_INDEX);
    PyModule_AddIntConstant(mod,"MAP2_NORMAL",GL_MAP2_NORMAL);
    PyModule_AddIntConstant(mod,"MAP2_TEXTURE_COORD_1",GL_MAP2_TEXTURE_COORD_1);
    PyModule_AddIntConstant(mod,"MAP2_TEXTURE_COORD_2",GL_MAP2_TEXTURE_COORD_2);
    PyModule_AddIntConstant(mod,"MAP2_TEXTURE_COORD_3",GL_MAP2_TEXTURE_COORD_3);
    PyModule_AddIntConstant(mod,"MAP2_TEXTURE_COORD_4",GL_MAP2_TEXTURE_COORD_4);
    PyModule_AddIntConstant(mod,"MAP2_VERTEX_3",GL_MAP2_VERTEX_3);
    PyModule_AddIntConstant(mod,"MAP2_VERTEX_4",GL_MAP2_VERTEX_4);
    PyModule_AddIntConstant(mod,"MAP1_GRID_DOMAIN",GL_MAP1_GRID_DOMAIN);
    PyModule_AddIntConstant(mod,"MAP1_GRID_SEGMENTS",GL_MAP1_GRID_SEGMENTS);
    PyModule_AddIntConstant(mod,"MAP2_GRID_DOMAIN",GL_MAP2_GRID_DOMAIN);
    PyModule_AddIntConstant(mod,"MAP2_GRID_SEGMENTS",GL_MAP2_GRID_SEGMENTS);
    PyModule_AddIntConstant(mod,"COEFF",GL_COEFF);
    PyModule_AddIntConstant(mod,"ORDER",GL_ORDER);
    PyModule_AddIntConstant(mod,"DOMAIN",GL_DOMAIN);
    PyModule_AddIntConstant(mod,"PERSPECTIVE_CORRECTION_HINT",GL_PERSPECTIVE_CORRECTION_HINT);
    PyModule_AddIntConstant(mod,"POINT_SMOOTH_HINT",GL_POINT_SMOOTH_HINT);
    PyModule_AddIntConstant(mod,"LINE_SMOOTH_HINT",GL_LINE_SMOOTH_HINT);
    PyModule_AddIntConstant(mod,"POLYGON_SMOOTH_HINT",GL_POLYGON_SMOOTH_HINT);
    PyModule_AddIntConstant(mod,"FOG_HINT",GL_FOG_HINT);
    PyModule_AddIntConstant(mod,"DONT_CARE",GL_DONT_CARE);
    PyModule_AddIntConstant(mod,"FASTEST",GL_FASTEST);
    PyModule_AddIntConstant(mod,"NICEST",GL_NICEST);
    PyModule_AddIntConstant(mod,"SCISSOR_BOX",GL_SCISSOR_BOX);
    PyModule_AddIntConstant(mod,"SCISSOR_TEST",GL_SCISSOR_TEST);
    PyModule_AddIntConstant(mod,"MAP_COLOR",GL_MAP_COLOR);
    PyModule_AddIntConstant(mod,"MAP_STENCIL",GL_MAP_STENCIL);
    PyModule_AddIntConstant(mod,"INDEX_SHIFT",GL_INDEX_SHIFT);
    PyModule_AddIntConstant(mod,"INDEX_OFFSET",GL_INDEX_OFFSET);
    PyModule_AddIntConstant(mod,"RED_SCALE",GL_RED_SCALE);
    PyModule_AddIntConstant(mod,"RED_BIAS",GL_RED_BIAS);
    PyModule_AddIntConstant(mod,"GREEN_SCALE",GL_GREEN_SCALE);
    PyModule_AddIntConstant(mod,"GREEN_BIAS",GL_GREEN_BIAS);
    PyModule_AddIntConstant(mod,"BLUE_SCALE",GL_BLUE_SCALE);
    PyModule_AddIntConstant(mod,"BLUE_BIAS",GL_BLUE_BIAS);
    PyModule_AddIntConstant(mod,"ALPHA_SCALE",GL_ALPHA_SCALE);
    PyModule_AddIntConstant(mod,"ALPHA_BIAS",GL_ALPHA_BIAS);
    PyModule_AddIntConstant(mod,"DEPTH_SCALE",GL_DEPTH_SCALE);
    PyModule_AddIntConstant(mod,"DEPTH_BIAS",GL_DEPTH_BIAS);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_S_TO_S_SIZE",GL_PIXEL_MAP_S_TO_S_SIZE);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_I_TO_I_SIZE",GL_PIXEL_MAP_I_TO_I_SIZE);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_I_TO_R_SIZE",GL_PIXEL_MAP_I_TO_R_SIZE);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_I_TO_G_SIZE",GL_PIXEL_MAP_I_TO_G_SIZE);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_I_TO_B_SIZE",GL_PIXEL_MAP_I_TO_B_SIZE);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_I_TO_A_SIZE",GL_PIXEL_MAP_I_TO_A_SIZE);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_R_TO_R_SIZE",GL_PIXEL_MAP_R_TO_R_SIZE);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_G_TO_G_SIZE",GL_PIXEL_MAP_G_TO_G_SIZE);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_B_TO_B_SIZE",GL_PIXEL_MAP_B_TO_B_SIZE);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_A_TO_A_SIZE",GL_PIXEL_MAP_A_TO_A_SIZE);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_S_TO_S",GL_PIXEL_MAP_S_TO_S);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_I_TO_I",GL_PIXEL_MAP_I_TO_I);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_I_TO_R",GL_PIXEL_MAP_I_TO_R);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_I_TO_G",GL_PIXEL_MAP_I_TO_G);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_I_TO_B",GL_PIXEL_MAP_I_TO_B);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_I_TO_A",GL_PIXEL_MAP_I_TO_A);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_R_TO_R",GL_PIXEL_MAP_R_TO_R);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_G_TO_G",GL_PIXEL_MAP_G_TO_G);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_B_TO_B",GL_PIXEL_MAP_B_TO_B);
    PyModule_AddIntConstant(mod,"PIXEL_MAP_A_TO_A",GL_PIXEL_MAP_A_TO_A);
    PyModule_AddIntConstant(mod,"PACK_ALIGNMENT",GL_PACK_ALIGNMENT);
    PyModule_AddIntConstant(mod,"PACK_LSB_FIRST",GL_PACK_LSB_FIRST);
    PyModule_AddIntConstant(mod,"PACK_ROW_LENGTH",GL_PACK_ROW_LENGTH);
    PyModule_AddIntConstant(mod,"PACK_SKIP_PIXELS",GL_PACK_SKIP_PIXELS);
    PyModule_AddIntConstant(mod,"PACK_SKIP_ROWS",GL_PACK_SKIP_ROWS);
    PyModule_AddIntConstant(mod,"PACK_SWAP_BYTES",GL_PACK_SWAP_BYTES);
    PyModule_AddIntConstant(mod,"UNPACK_ALIGNMENT",GL_UNPACK_ALIGNMENT);
    PyModule_AddIntConstant(mod,"UNPACK_LSB_FIRST",GL_UNPACK_LSB_FIRST);
    PyModule_AddIntConstant(mod,"UNPACK_ROW_LENGTH",GL_UNPACK_ROW_LENGTH);
    PyModule_AddIntConstant(mod,"UNPACK_SKIP_PIXELS",GL_UNPACK_SKIP_PIXELS);
    PyModule_AddIntConstant(mod,"UNPACK_SKIP_ROWS",GL_UNPACK_SKIP_ROWS);
    PyModule_AddIntConstant(mod,"UNPACK_SWAP_BYTES",GL_UNPACK_SWAP_BYTES);
    PyModule_AddIntConstant(mod,"ZOOM_X",GL_ZOOM_X);
    PyModule_AddIntConstant(mod,"ZOOM_Y",GL_ZOOM_Y);
    PyModule_AddIntConstant(mod,"TEXTURE_ENV",GL_TEXTURE_ENV);
    PyModule_AddIntConstant(mod,"TEXTURE_ENV_MODE",GL_TEXTURE_ENV_MODE);
    PyModule_AddIntConstant(mod,"TEXTURE_1D",GL_TEXTURE_1D);
    PyModule_AddIntConstant(mod,"TEXTURE_2D",GL_TEXTURE_2D);
    PyModule_AddIntConstant(mod,"TEXTURE_WRAP_S",GL_TEXTURE_WRAP_S);
    PyModule_AddIntConstant(mod,"TEXTURE_WRAP_T",GL_TEXTURE_WRAP_T);
    PyModule_AddIntConstant(mod,"TEXTURE_MAG_FILTER",GL_TEXTURE_MAG_FILTER);
    PyModule_AddIntConstant(mod,"TEXTURE_MIN_FILTER",GL_TEXTURE_MIN_FILTER);
    PyModule_AddIntConstant(mod,"TEXTURE_ENV_COLOR",GL_TEXTURE_ENV_COLOR);
    PyModule_AddIntConstant(mod,"TEXTURE_GEN_S",GL_TEXTURE_GEN_S);
    PyModule_AddIntConstant(mod,"TEXTURE_GEN_T",GL_TEXTURE_GEN_T);
    PyModule_AddIntConstant(mod,"TEXTURE_GEN_MODE",GL_TEXTURE_GEN_MODE);
    PyModule_AddIntConstant(mod,"TEXTURE_BORDER_COLOR",GL_TEXTURE_BORDER_COLOR);
    PyModule_AddIntConstant(mod,"TEXTURE_WIDTH",GL_TEXTURE_WIDTH);
    PyModule_AddIntConstant(mod,"TEXTURE_HEIGHT",GL_TEXTURE_HEIGHT);
    PyModule_AddIntConstant(mod,"TEXTURE_BORDER",GL_TEXTURE_BORDER);
    PyModule_AddIntConstant(mod,"TEXTURE_COMPONENTS",GL_TEXTURE_COMPONENTS);
    PyModule_AddIntConstant(mod,"TEXTURE_RED_SIZE",GL_TEXTURE_RED_SIZE);
    PyModule_AddIntConstant(mod,"TEXTURE_GREEN_SIZE",GL_TEXTURE_GREEN_SIZE);
    PyModule_AddIntConstant(mod,"TEXTURE_BLUE_SIZE",GL_TEXTURE_BLUE_SIZE);
    PyModule_AddIntConstant(mod,"TEXTURE_ALPHA_SIZE",GL_TEXTURE_ALPHA_SIZE);
    PyModule_AddIntConstant(mod,"TEXTURE_LUMINANCE_SIZE",GL_TEXTURE_LUMINANCE_SIZE);
    PyModule_AddIntConstant(mod,"TEXTURE_INTENSITY_SIZE",GL_TEXTURE_INTENSITY_SIZE);
    PyModule_AddIntConstant(mod,"NEAREST_MIPMAP_NEAREST",GL_NEAREST_MIPMAP_NEAREST);
    PyModule_AddIntConstant(mod,"NEAREST_MIPMAP_LINEAR",GL_NEAREST_MIPMAP_LINEAR);
    PyModule_AddIntConstant(mod,"LINEAR_MIPMAP_NEAREST",GL_LINEAR_MIPMAP_NEAREST);
    PyModule_AddIntConstant(mod,"LINEAR_MIPMAP_LINEAR",GL_LINEAR_MIPMAP_LINEAR);
    PyModule_AddIntConstant(mod,"OBJECT_LINEAR",GL_OBJECT_LINEAR);
    PyModule_AddIntConstant(mod,"OBJECT_PLANE",GL_OBJECT_PLANE);
    PyModule_AddIntConstant(mod,"EYE_LINEAR",GL_EYE_LINEAR);
    PyModule_AddIntConstant(mod,"EYE_PLANE",GL_EYE_PLANE);
    PyModule_AddIntConstant(mod,"SPHERE_MAP",GL_SPHERE_MAP);
    PyModule_AddIntConstant(mod,"DECAL",GL_DECAL);
    PyModule_AddIntConstant(mod,"MODULATE",GL_MODULATE);
    PyModule_AddIntConstant(mod,"NEAREST",GL_NEAREST);
    PyModule_AddIntConstant(mod,"REPEAT",GL_REPEAT);
    PyModule_AddIntConstant(mod,"CLAMP",GL_CLAMP);
    PyModule_AddIntConstant(mod,"S",GL_S);
    PyModule_AddIntConstant(mod,"T",GL_T);
    PyModule_AddIntConstant(mod,"R",GL_R);
    PyModule_AddIntConstant(mod,"Q",GL_Q);
    PyModule_AddIntConstant(mod,"TEXTURE_GEN_R",GL_TEXTURE_GEN_R);
    PyModule_AddIntConstant(mod,"TEXTURE_GEN_Q",GL_TEXTURE_GEN_Q);
    PyModule_AddIntConstant(mod,"VENDOR",GL_VENDOR);
    PyModule_AddIntConstant(mod,"RENDERER",GL_RENDERER);
    PyModule_AddIntConstant(mod,"VERSION",GL_VERSION);
    PyModule_AddIntConstant(mod,"EXTENSIONS",GL_EXTENSIONS);
    PyModule_AddIntConstant(mod,"NO_ERROR",GL_NO_ERROR);
    PyModule_AddIntConstant(mod,"INVALID_ENUM",GL_INVALID_ENUM);
    PyModule_AddIntConstant(mod,"INVALID_VALUE",GL_INVALID_VALUE);
    PyModule_AddIntConstant(mod,"INVALID_OPERATION",GL_INVALID_OPERATION);
    PyModule_AddIntConstant(mod,"STACK_OVERFLOW",GL_STACK_OVERFLOW);
    PyModule_AddIntConstant(mod,"STACK_UNDERFLOW",GL_STACK_UNDERFLOW);
    PyModule_AddIntConstant(mod,"OUT_OF_MEMORY",GL_OUT_OF_MEMORY);
    PyModule_AddIntConstant(mod,"CURRENT_BIT",GL_CURRENT_BIT);
    PyModule_AddIntConstant(mod,"POINT_BIT",GL_POINT_BIT);
    PyModule_AddIntConstant(mod,"LINE_BIT",GL_LINE_BIT);
    PyModule_AddIntConstant(mod,"POLYGON_BIT",GL_POLYGON_BIT);
    PyModule_AddIntConstant(mod,"POLYGON_STIPPLE_BIT",GL_POLYGON_STIPPLE_BIT);
    PyModule_AddIntConstant(mod,"PIXEL_MODE_BIT",GL_PIXEL_MODE_BIT);
    PyModule_AddIntConstant(mod,"LIGHTING_BIT",GL_LIGHTING_BIT);
    PyModule_AddIntConstant(mod,"FOG_BIT",GL_FOG_BIT);
    PyModule_AddIntConstant(mod,"DEPTH_BUFFER_BIT",GL_DEPTH_BUFFER_BIT);
    PyModule_AddIntConstant(mod,"ACCUM_BUFFER_BIT",GL_ACCUM_BUFFER_BIT);
    PyModule_AddIntConstant(mod,"STENCIL_BUFFER_BIT",GL_STENCIL_BUFFER_BIT);
    PyModule_AddIntConstant(mod,"VIEWPORT_BIT",GL_VIEWPORT_BIT);
    PyModule_AddIntConstant(mod,"TRANSFORM_BIT",GL_TRANSFORM_BIT);
    PyModule_AddIntConstant(mod,"ENABLE_BIT",GL_ENABLE_BIT);
    PyModule_AddIntConstant(mod,"COLOR_BUFFER_BIT",GL_COLOR_BUFFER_BIT);
    PyModule_AddIntConstant(mod,"HINT_BIT",GL_HINT_BIT);
    PyModule_AddIntConstant(mod,"EVAL_BIT",GL_EVAL_BIT);
    PyModule_AddIntConstant(mod,"LIST_BIT",GL_LIST_BIT);
    PyModule_AddIntConstant(mod,"TEXTURE_BIT",GL_TEXTURE_BIT);
    PyModule_AddIntConstant(mod,"SCISSOR_BIT",GL_SCISSOR_BIT);
    PyModule_AddIntConstant(mod,"ALL_ATTRIB_BITS",GL_ALL_ATTRIB_BITS);
    PyModule_AddIntConstant(mod,"PROXY_TEXTURE_1D",GL_PROXY_TEXTURE_1D);
    PyModule_AddIntConstant(mod,"PROXY_TEXTURE_2D",GL_PROXY_TEXTURE_2D);
    PyModule_AddIntConstant(mod,"TEXTURE_PRIORITY",GL_TEXTURE_PRIORITY);
    PyModule_AddIntConstant(mod,"TEXTURE_RESIDENT",GL_TEXTURE_RESIDENT);
    PyModule_AddIntConstant(mod,"TEXTURE_BINDING_1D",GL_TEXTURE_BINDING_1D);
    PyModule_AddIntConstant(mod,"TEXTURE_BINDING_2D",GL_TEXTURE_BINDING_2D);
    PyModule_AddIntConstant(mod,"TEXTURE_INTERNAL_FORMAT",GL_TEXTURE_INTERNAL_FORMAT);
    PyModule_AddIntConstant(mod,"ALPHA4",GL_ALPHA4);
    PyModule_AddIntConstant(mod,"ALPHA8",GL_ALPHA8);
    PyModule_AddIntConstant(mod,"ALPHA12",GL_ALPHA12);
    PyModule_AddIntConstant(mod,"ALPHA16",GL_ALPHA16);
    PyModule_AddIntConstant(mod,"LUMINANCE4",GL_LUMINANCE4);
    PyModule_AddIntConstant(mod,"LUMINANCE8",GL_LUMINANCE8);
    PyModule_AddIntConstant(mod,"LUMINANCE12",GL_LUMINANCE12);
    PyModule_AddIntConstant(mod,"LUMINANCE16",GL_LUMINANCE16);
    PyModule_AddIntConstant(mod,"LUMINANCE4_ALPHA4",GL_LUMINANCE4_ALPHA4);
    PyModule_AddIntConstant(mod,"LUMINANCE6_ALPHA2",GL_LUMINANCE6_ALPHA2);
    PyModule_AddIntConstant(mod,"LUMINANCE8_ALPHA8",GL_LUMINANCE8_ALPHA8);
    PyModule_AddIntConstant(mod,"LUMINANCE12_ALPHA4",GL_LUMINANCE12_ALPHA4);
    PyModule_AddIntConstant(mod,"LUMINANCE12_ALPHA12",GL_LUMINANCE12_ALPHA12);
    PyModule_AddIntConstant(mod,"LUMINANCE16_ALPHA16",GL_LUMINANCE16_ALPHA16);
    PyModule_AddIntConstant(mod,"INTENSITY",GL_INTENSITY);
    PyModule_AddIntConstant(mod,"INTENSITY4",GL_INTENSITY4);
    PyModule_AddIntConstant(mod,"INTENSITY8",GL_INTENSITY8);
    PyModule_AddIntConstant(mod,"INTENSITY12",GL_INTENSITY12);
    PyModule_AddIntConstant(mod,"INTENSITY16",GL_INTENSITY16);
    PyModule_AddIntConstant(mod,"R3_G3_B2",GL_R3_G3_B2);
    PyModule_AddIntConstant(mod,"RGB4",GL_RGB4);
    PyModule_AddIntConstant(mod,"RGB5",GL_RGB5);
    PyModule_AddIntConstant(mod,"RGB8",GL_RGB8);
    PyModule_AddIntConstant(mod,"RGB10",GL_RGB10);
    PyModule_AddIntConstant(mod,"RGB12",GL_RGB12);
    PyModule_AddIntConstant(mod,"RGB16",GL_RGB16);
    PyModule_AddIntConstant(mod,"RGBA2",GL_RGBA2);
    PyModule_AddIntConstant(mod,"RGBA4",GL_RGBA4);
    PyModule_AddIntConstant(mod,"RGB5_A1",GL_RGB5_A1);
    PyModule_AddIntConstant(mod,"RGBA8",GL_RGBA8);
    PyModule_AddIntConstant(mod,"RGB10_A2",GL_RGB10_A2);
    PyModule_AddIntConstant(mod,"RGBA12",GL_RGBA12);
    PyModule_AddIntConstant(mod,"RGBA16",GL_RGBA16);
    PyModule_AddIntConstant(mod,"CLIENT_PIXEL_STORE_BIT",GL_CLIENT_PIXEL_STORE_BIT);
    PyModule_AddIntConstant(mod,"CLIENT_VERTEX_ARRAY_BIT",GL_CLIENT_VERTEX_ARRAY_BIT);
    PyModule_AddIntConstant(mod,"CLIENT_ALL_ATTRIB_BITS",GL_CLIENT_ALL_ATTRIB_BITS);
    PyModule_AddIntConstant(mod,"TEXTURE0_ARB",GL_TEXTURE0_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE1_ARB",GL_TEXTURE1_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE2_ARB",GL_TEXTURE2_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE3_ARB",GL_TEXTURE3_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE4_ARB",GL_TEXTURE4_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE5_ARB",GL_TEXTURE5_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE6_ARB",GL_TEXTURE6_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE7_ARB",GL_TEXTURE7_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE8_ARB",GL_TEXTURE8_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE9_ARB",GL_TEXTURE9_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE10_ARB",GL_TEXTURE10_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE11_ARB",GL_TEXTURE11_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE12_ARB",GL_TEXTURE12_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE13_ARB",GL_TEXTURE13_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE14_ARB",GL_TEXTURE14_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE15_ARB",GL_TEXTURE15_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE16_ARB",GL_TEXTURE16_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE17_ARB",GL_TEXTURE17_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE18_ARB",GL_TEXTURE18_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE19_ARB",GL_TEXTURE19_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE20_ARB",GL_TEXTURE20_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE21_ARB",GL_TEXTURE21_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE22_ARB",GL_TEXTURE22_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE23_ARB",GL_TEXTURE23_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE24_ARB",GL_TEXTURE24_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE25_ARB",GL_TEXTURE25_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE26_ARB",GL_TEXTURE26_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE27_ARB",GL_TEXTURE27_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE28_ARB",GL_TEXTURE28_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE29_ARB",GL_TEXTURE29_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE30_ARB",GL_TEXTURE30_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE31_ARB",GL_TEXTURE31_ARB);
    PyModule_AddIntConstant(mod,"ACTIVE_TEXTURE_ARB",GL_ACTIVE_TEXTURE_ARB);
    PyModule_AddIntConstant(mod,"CLIENT_ACTIVE_TEXTURE_ARB",GL_CLIENT_ACTIVE_TEXTURE_ARB);
    PyModule_AddIntConstant(mod,"MAX_TEXTURE_UNITS_ARB",GL_MAX_TEXTURE_UNITS_ARB);
    PyModule_AddIntConstant(mod,"COMBINE_ARB",GL_COMBINE_ARB);
    PyModule_AddIntConstant(mod,"COMBINE_RGB_ARB",GL_COMBINE_RGB_ARB);
    PyModule_AddIntConstant(mod,"COMBINE_ALPHA_ARB",GL_COMBINE_ALPHA_ARB);
    PyModule_AddIntConstant(mod,"SOURCE0_RGB_ARB",GL_SOURCE0_RGB_ARB);
    PyModule_AddIntConstant(mod,"SOURCE1_RGB_ARB",GL_SOURCE1_RGB_ARB);
    PyModule_AddIntConstant(mod,"SOURCE2_RGB_ARB",GL_SOURCE2_RGB_ARB);
    PyModule_AddIntConstant(mod,"SOURCE0_ALPHA_ARB",GL_SOURCE0_ALPHA_ARB);
    PyModule_AddIntConstant(mod,"SOURCE1_ALPHA_ARB",GL_SOURCE1_ALPHA_ARB);
    PyModule_AddIntConstant(mod,"SOURCE2_ALPHA_ARB",GL_SOURCE2_ALPHA_ARB);
    PyModule_AddIntConstant(mod,"OPERAND0_RGB_ARB",GL_OPERAND0_RGB_ARB);
    PyModule_AddIntConstant(mod,"OPERAND1_RGB_ARB",GL_OPERAND1_RGB_ARB);
    PyModule_AddIntConstant(mod,"OPERAND2_RGB_ARB",GL_OPERAND2_RGB_ARB);
    PyModule_AddIntConstant(mod,"OPERAND0_ALPHA_ARB",GL_OPERAND0_ALPHA_ARB);
    PyModule_AddIntConstant(mod,"OPERAND1_ALPHA_ARB",GL_OPERAND1_ALPHA_ARB);
    PyModule_AddIntConstant(mod,"OPERAND2_ALPHA_ARB",GL_OPERAND2_ALPHA_ARB);
    PyModule_AddIntConstant(mod,"RGB_SCALE_ARB",GL_RGB_SCALE_ARB);
    PyModule_AddIntConstant(mod,"ADD_SIGNED_ARB",GL_ADD_SIGNED_ARB);
    PyModule_AddIntConstant(mod,"INTERPOLATE_ARB",GL_INTERPOLATE_ARB);
    PyModule_AddIntConstant(mod,"SUBTRACT_ARB",GL_SUBTRACT_ARB);
    PyModule_AddIntConstant(mod,"CONSTANT_ARB",GL_CONSTANT_ARB);
    PyModule_AddIntConstant(mod,"PRIMARY_COLOR_ARB",GL_PRIMARY_COLOR_ARB);
    PyModule_AddIntConstant(mod,"PREVIOUS_ARB",GL_PREVIOUS_ARB);
    PyModule_AddIntConstant(mod,"BUFFER_SIZE_ARB",GL_BUFFER_SIZE_ARB);
    PyModule_AddIntConstant(mod,"BUFFER_USAGE_ARB",GL_BUFFER_USAGE_ARB);
    PyModule_AddIntConstant(mod,"ARRAY_BUFFER_ARB",GL_ARRAY_BUFFER_ARB);
    PyModule_AddIntConstant(mod,"ELEMENT_ARRAY_BUFFER_ARB",GL_ELEMENT_ARRAY_BUFFER_ARB);
    PyModule_AddIntConstant(mod,"ARRAY_BUFFER_BINDING_ARB",GL_ARRAY_BUFFER_BINDING_ARB);
    PyModule_AddIntConstant(mod,"ELEMENT_ARRAY_BUFFER_BINDING_ARB",GL_ELEMENT_ARRAY_BUFFER_BINDING_ARB);
    PyModule_AddIntConstant(mod,"VERTEX_ARRAY_BUFFER_BINDING_ARB",GL_VERTEX_ARRAY_BUFFER_BINDING_ARB);
    PyModule_AddIntConstant(mod,"NORMAL_ARRAY_BUFFER_BINDING_ARB",GL_NORMAL_ARRAY_BUFFER_BINDING_ARB);
    PyModule_AddIntConstant(mod,"COLOR_ARRAY_BUFFER_BINDING_ARB",GL_COLOR_ARRAY_BUFFER_BINDING_ARB);
    PyModule_AddIntConstant(mod,"INDEX_ARRAY_BUFFER_BINDING_ARB",GL_INDEX_ARRAY_BUFFER_BINDING_ARB);
    PyModule_AddIntConstant(mod,"TEXTURE_COORD_ARRAY_BUFFER_BINDING_ARB",GL_TEXTURE_COORD_ARRAY_BUFFER_BINDING_ARB);
    PyModule_AddIntConstant(mod,"EDGE_FLAG_ARRAY_BUFFER_BINDING_ARB",GL_EDGE_FLAG_ARRAY_BUFFER_BINDING_ARB);
    PyModule_AddIntConstant(mod,"SECONDARY_COLOR_ARRAY_BUFFER_BINDING_ARB",GL_SECONDARY_COLOR_ARRAY_BUFFER_BINDING_ARB);
    PyModule_AddIntConstant(mod,"FOG_COORDINATE_ARRAY_BUFFER_BINDING_ARB",GL_FOG_COORDINATE_ARRAY_BUFFER_BINDING_ARB);
    PyModule_AddIntConstant(mod,"WEIGHT_ARRAY_BUFFER_BINDING_ARB",GL_WEIGHT_ARRAY_BUFFER_BINDING_ARB);
    PyModule_AddIntConstant(mod,"VERTEX_ATTRIB_ARRAY_BUFFER_BINDING_ARB",GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING_ARB);
    PyModule_AddIntConstant(mod,"READ_ONLY_ARB",GL_READ_ONLY_ARB);
    PyModule_AddIntConstant(mod,"WRITE_ONLY_ARB",GL_WRITE_ONLY_ARB);
    PyModule_AddIntConstant(mod,"READ_WRITE_ARB",GL_READ_WRITE_ARB);
    PyModule_AddIntConstant(mod,"BUFFER_ACCESS_ARB",GL_BUFFER_ACCESS_ARB);
    PyModule_AddIntConstant(mod,"BUFFER_MAPPED_ARB",GL_BUFFER_MAPPED_ARB);
    PyModule_AddIntConstant(mod,"BUFFER_MAP_POINTER_ARB",GL_BUFFER_MAP_POINTER_ARB);
    PyModule_AddIntConstant(mod,"STREAM_DRAW_ARB",GL_STREAM_DRAW_ARB);
    PyModule_AddIntConstant(mod,"STREAM_READ_ARB",GL_STREAM_READ_ARB);
    PyModule_AddIntConstant(mod,"STREAM_COPY_ARB",GL_STREAM_COPY_ARB);
    PyModule_AddIntConstant(mod,"STATIC_DRAW_ARB",GL_STATIC_DRAW_ARB);
    PyModule_AddIntConstant(mod,"STATIC_READ_ARB",GL_STATIC_READ_ARB);
    PyModule_AddIntConstant(mod,"STATIC_COPY_ARB",GL_STATIC_COPY_ARB);
    PyModule_AddIntConstant(mod,"DYNAMIC_DRAW_ARB",GL_DYNAMIC_DRAW_ARB);
    PyModule_AddIntConstant(mod,"DYNAMIC_READ_ARB",GL_DYNAMIC_READ_ARB);
    PyModule_AddIntConstant(mod,"DYNAMIC_COPY_ARB",GL_DYNAMIC_COPY_ARB);
    PyModule_AddIntConstant(mod,"PROGRAM_OBJECT_ARB",GL_PROGRAM_OBJECT_ARB);
    PyModule_AddIntConstant(mod,"SHADER_OBJECT_ARB",GL_SHADER_OBJECT_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_TYPE_ARB",GL_OBJECT_TYPE_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_SUBTYPE_ARB",GL_OBJECT_SUBTYPE_ARB);
    PyModule_AddIntConstant(mod,"FLOAT_VEC2_ARB",GL_FLOAT_VEC2_ARB);
    PyModule_AddIntConstant(mod,"FLOAT_VEC3_ARB",GL_FLOAT_VEC3_ARB);
    PyModule_AddIntConstant(mod,"FLOAT_VEC4_ARB",GL_FLOAT_VEC4_ARB);
    PyModule_AddIntConstant(mod,"INT_VEC2_ARB",GL_INT_VEC2_ARB);
    PyModule_AddIntConstant(mod,"INT_VEC3_ARB",GL_INT_VEC3_ARB);
    PyModule_AddIntConstant(mod,"INT_VEC4_ARB",GL_INT_VEC4_ARB);
    PyModule_AddIntConstant(mod,"BOOL_ARB",GL_BOOL_ARB);
    PyModule_AddIntConstant(mod,"BOOL_VEC2_ARB",GL_BOOL_VEC2_ARB);
    PyModule_AddIntConstant(mod,"BOOL_VEC3_ARB",GL_BOOL_VEC3_ARB);
    PyModule_AddIntConstant(mod,"BOOL_VEC4_ARB",GL_BOOL_VEC4_ARB);
    PyModule_AddIntConstant(mod,"FLOAT_MAT2_ARB",GL_FLOAT_MAT2_ARB);
    PyModule_AddIntConstant(mod,"FLOAT_MAT3_ARB",GL_FLOAT_MAT3_ARB);
    PyModule_AddIntConstant(mod,"FLOAT_MAT4_ARB",GL_FLOAT_MAT4_ARB);
    PyModule_AddIntConstant(mod,"SAMPLER_1D_ARB",GL_SAMPLER_1D_ARB);
    PyModule_AddIntConstant(mod,"SAMPLER_2D_ARB",GL_SAMPLER_2D_ARB);
    PyModule_AddIntConstant(mod,"SAMPLER_3D_ARB",GL_SAMPLER_3D_ARB);
    PyModule_AddIntConstant(mod,"SAMPLER_CUBE_ARB",GL_SAMPLER_CUBE_ARB);
    PyModule_AddIntConstant(mod,"SAMPLER_1D_SHADOW_ARB",GL_SAMPLER_1D_SHADOW_ARB);
    PyModule_AddIntConstant(mod,"SAMPLER_2D_SHADOW_ARB",GL_SAMPLER_2D_SHADOW_ARB);
    PyModule_AddIntConstant(mod,"SAMPLER_2D_RECT_ARB",GL_SAMPLER_2D_RECT_ARB);
    PyModule_AddIntConstant(mod,"SAMPLER_2D_RECT_SHADOW_ARB",GL_SAMPLER_2D_RECT_SHADOW_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_DELETE_STATUS_ARB",GL_OBJECT_DELETE_STATUS_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_COMPILE_STATUS_ARB",GL_OBJECT_COMPILE_STATUS_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_LINK_STATUS_ARB",GL_OBJECT_LINK_STATUS_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_VALIDATE_STATUS_ARB",GL_OBJECT_VALIDATE_STATUS_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_INFO_LOG_LENGTH_ARB",GL_OBJECT_INFO_LOG_LENGTH_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_ATTACHED_OBJECTS_ARB",GL_OBJECT_ATTACHED_OBJECTS_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_ACTIVE_UNIFORMS_ARB",GL_OBJECT_ACTIVE_UNIFORMS_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_ACTIVE_UNIFORM_MAX_LENGTH_ARB",GL_OBJECT_ACTIVE_UNIFORM_MAX_LENGTH_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_SHADER_SOURCE_LENGTH_ARB",GL_OBJECT_SHADER_SOURCE_LENGTH_ARB);
    PyModule_AddIntConstant(mod,"VERTEX_SHADER_ARB",GL_VERTEX_SHADER_ARB);
    PyModule_AddIntConstant(mod,"MAX_VERTEX_UNIFORM_COMPONENTS_ARB",GL_MAX_VERTEX_UNIFORM_COMPONENTS_ARB);
    PyModule_AddIntConstant(mod,"MAX_VARYING_FLOATS_ARB",GL_MAX_VARYING_FLOATS_ARB);
    PyModule_AddIntConstant(mod,"MAX_VERTEX_TEXTURE_IMAGE_UNITS_ARB",GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS_ARB);
    PyModule_AddIntConstant(mod,"MAX_COMBINED_TEXTURE_IMAGE_UNITS_ARB",GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_ACTIVE_ATTRIBUTES_ARB",GL_OBJECT_ACTIVE_ATTRIBUTES_ARB);
    PyModule_AddIntConstant(mod,"OBJECT_ACTIVE_ATTRIBUTE_MAX_LENGTH_ARB",GL_OBJECT_ACTIVE_ATTRIBUTE_MAX_LENGTH_ARB);
    PyModule_AddIntConstant(mod,"FRAGMENT_SHADER_ARB",GL_FRAGMENT_SHADER_ARB);
    PyModule_AddIntConstant(mod,"MAX_FRAGMENT_UNIFORM_COMPONENTS_ARB",GL_MAX_FRAGMENT_UNIFORM_COMPONENTS_ARB);
    PyModule_AddIntConstant(mod,"FRAGMENT_SHADER_DERIVATIVE_HINT_ARB",GL_FRAGMENT_SHADER_DERIVATIVE_HINT_ARB);
    PyModule_AddIntConstant(mod,"SHADING_LANGUAGE_VERSION_ARB",GL_SHADING_LANGUAGE_VERSION_ARB);
    PyModule_AddIntConstant(mod,"TRUE",GLU_TRUE);
    PyModule_AddIntConstant(mod,"FALSE",GLU_FALSE);
    PyModule_AddIntConstant(mod,"INVALID_ENUM",GLU_INVALID_ENUM);
    PyModule_AddIntConstant(mod,"INVALID_VALUE",GLU_INVALID_VALUE);
    PyModule_AddIntConstant(mod,"OUT_OF_MEMORY",GLU_OUT_OF_MEMORY);
    PyModule_AddIntConstant(mod,"INCOMPATIBLE_GL_VERSION",GLU_INCOMPATIBLE_GL_VERSION);
    PyModule_AddIntConstant(mod,"INVALID_OPERATION",GLU_INVALID_OPERATION);
    PyModule_AddIntConstant(mod,"VERSION",GLU_VERSION);
    PyModule_AddIntConstant(mod,"EXTENSIONS",GLU_EXTENSIONS);
    PyModule_AddIntConstant(mod,"INVALID_ENUM",GLU_INVALID_ENUM);
    PyModule_AddIntConstant(mod,"INVALID_VALUE",GLU_INVALID_VALUE);
    PyModule_AddIntConstant(mod,"OUT_OF_MEMORY",GLU_OUT_OF_MEMORY);
    PyModule_AddIntConstant(mod,"INCOMPATIBLE_GL_VERSION",GLU_INCOMPATIBLE_GL_VERSION);
    PyModule_AddIntConstant(mod,"INVALID_OPERATION",GLU_INVALID_OPERATION);
}
