# Python wrapper for emscripten_* C functions

# Copyright (C) 2018, 2019, 2020  Sylvain Beucler

# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

# http://docs.cython.org/en/latest/src/tutorial/strings.html#auto-encoding-and-decoding
# Most of our strings are converted from/to JS through emscripten stringToUTF8/UTF8ToString
# cython: c_string_type=unicode, c_string_encoding=utf8
# Note: Py->C auto-UTF-8 (instead of .encode('UTF-8')) not supported for Py2
# Note: causes issues with Typed Memoryviews

cdef extern from "emscripten.h":
    ctypedef void (*em_callback_func)() noexcept
    ctypedef void (*em_arg_callback_func)(void*) noexcept
    ctypedef void (*em_async_wget_onload_func)(void*, void*, int) noexcept

    void emscripten_set_main_loop(em_callback_func func, int fps, int simulate_infinite_loop)
    void emscripten_set_main_loop_arg(em_arg_callback_func func, void *arg, int fps, int simulate_infinite_loop)
    void emscripten_cancel_main_loop()
    void emscripten_exit_with_live_runtime()

    void emscripten_run_script(const char *script)
    int emscripten_run_script_int(const char *script)
    char *emscripten_run_script_string(const char *script)

    void emscripten_async_wget_data(const char* url, void *arg, em_async_wget_onload_func onload, em_arg_callback_func onerror)
    void emscripten_async_call(em_arg_callback_func func, void *arg, int millis)

    void emscripten_sleep(unsigned int ms)
    void emscripten_wget(const char* url, const char* file)
    void emscripten_wget_data(const char* url, void** pbuffer, int* pnum, int *perror)

    enum:
        EM_LOG_CONSOLE
        EM_LOG_WARN
        EM_LOG_ERROR
        EM_LOG_C_STACK
        EM_LOG_JS_STACK
        EM_LOG_DEMANGLE
        EM_LOG_NO_PATHS
        EM_LOG_FUNC_PARAMS

    int emscripten_get_compiler_setting(const char *name)
    void emscripten_debugger()
    void emscripten_log(int flags, const char* format, ...)
    int emscripten_get_callstack(int flags, char *out, int maxbytes)

LOG_CONSOLE = EM_LOG_CONSOLE
LOG_WARN = EM_LOG_WARN
LOG_ERROR = EM_LOG_ERROR
LOG_C_STACK = EM_LOG_C_STACK
LOG_JS_STACK = EM_LOG_JS_STACK
LOG_DEMANGLE = EM_LOG_DEMANGLE
LOG_NO_PATHS = EM_LOG_NO_PATHS
LOG_FUNC_PARAMS = EM_LOG_FUNC_PARAMS


cdef extern from "emscripten/html5.h":
    int emscripten_webgl_enable_extension(int context, const char *extension);
    int emscripten_webgl_get_current_context();
    char *emscripten_webgl_get_supported_extensions();


# https://cython.readthedocs.io/en/latest/src/tutorial/memory_allocation.html
from libc.stdlib cimport malloc, free
from cpython.mem cimport PyMem_Malloc, PyMem_Free
# https://github.com/cython/cython/wiki/FAQ#what-is-the-difference-between-pyobject-and-object
from cpython.ref cimport PyObject, Py_XINCREF, Py_XDECREF

from cpython.buffer cimport PyBuffer_FillInfo

#cdef extern from "stdio.h":
#    int puts(const char *s);


# C callback - no memory management
# Take a single Python object and calls it
# Kept for documentation
cdef void callpyfunc(void *py_function):
    # not necessary as we're using a no-threading Python
    #PyEval_InitThreads()
    # Call Python function from C using (<object>)()
    f = <object>py_function
    f()


# C callbacks - memory management
cdef struct pycaller:
    PyObject* py_function
    PyObject* py_arg  # can be: set, None or NULL

cdef pycaller* pycaller_create(PyObject* py_function, PyObject* py_arg):
    cdef pycaller* c = <pycaller*> PyMem_Malloc(sizeof(pycaller))
    c.py_function = py_function
    c.py_arg = py_arg
    Py_XINCREF(c.py_function)
    if c.py_arg != NULL:
        Py_XINCREF(c.py_arg)
    return c

cdef void pycaller_free(pycaller *c):
    if c.py_arg != NULL:
        Py_XDECREF(c.py_arg)
    Py_XDECREF(c.py_function)
    PyMem_Free(c)

# Take a Python object and calls it ONCE on passed argument
# C callback for e.g. emscripten_async_call
cdef void pycaller_callback_once(void* p) noexcept:
    pycaller_callback_recurring(p)
    pycaller_free(<pycaller*>p)

# Take a Python object and calls it on passed argument
# C callback for e.g. emscripten_set_main_loop_arg
cdef void pycaller_callback_recurring(void* p) noexcept:
    cdef pycaller* c = <pycaller*>p
    py_function = <object>(c.py_function)
    if c.py_arg != NULL:
        py_arg = <object>(c.py_arg)
        py_function(py_arg)
    else:
        py_function()


cdef pycaller* main_loop = NULL

def set_main_loop_arg(py_function, py_arg, fps, simulate_infinite_loop):
    set_main_loop_arg_c(<PyObject*>py_function, <PyObject*>py_arg,
                        fps, simulate_infinite_loop)

def set_main_loop(py_function, fps, simulate_infinite_loop):
    set_main_loop_arg_c(<PyObject*>py_function, NULL,
                        fps, simulate_infinite_loop)

# handle py_arg == NULL != None
cdef set_main_loop_arg_c(PyObject* py_function, PyObject* py_arg,
                         fps, simulate_infinite_loop):
    global main_loop
    if main_loop == NULL:
        main_loop = pycaller_create(py_function, py_arg)
    else:
        pass  # invalid, let emscripten_set_main_loop_arg() abort
    emscripten_set_main_loop_arg(pycaller_callback_recurring, <void*>main_loop,
                                 fps, simulate_infinite_loop)

def cancel_main_loop():
    global main_loop
    emscripten_cancel_main_loop()
    if main_loop != NULL:
       pycaller_free(main_loop)
    main_loop = NULL

# import emscripten,sys
# emscripten.set_main_loop(lambda: sys.stdout.write("main_loop\n"), 2, 0)
# emscripten.cancel_main_loop()
# emscripten.set_main_loop(lambda: sys.stdout.write("main_loop\n"), -1, 1)
# emscripten.set_main_loop_arg(lambda a: sys.stdout.write(a), "main_loop_arg\n", 2, 0)

def async_call(py_function, py_arg, millis):
    cdef pycaller* c = pycaller_create(<PyObject*>py_function, <PyObject*>py_arg)
    emscripten_async_call(pycaller_callback_once, <void*>c, millis)

# emscripten.async_call(lambda a: sys.stdout.write(a), "async_call_arg\n", 1000)


def exit_with_live_runtime():
    emscripten_exit_with_live_runtime();


# Emterpreter-only
#def sleep_with_yield(ms):
#    emscripten_sleep_with_yield(ms)

def run_script(script):
    emscripten_run_script(script.encode('UTF-8'));

def run_script_int(script):
    return emscripten_run_script_int(script.encode('UTF-8'));

def run_script_string(script):
    return emscripten_run_script_string(script.encode('UTF-8'));


TRACE = False

trace_set = set()
old_trace_set = set()

def process_trace(trace):
    global trace_set
    global old_trace_set

    lines = trace.splitlines()
    lines.pop(0)

    for i in lines:
        i = i.strip()
        i = i.split(' ')[1]
        trace_set.add(i)

    if trace_set != old_trace_set:

        print("New sleep trace:", trace_set - old_trace_set)

        old_trace_set |= trace_set

        l = list(trace_set)
        l.sort()
        print("Full sleep trace:")

        for i in l:
            print(repr(i) + ",")


if TRACE:
    emscripten_run_script("""Error.stackTraceLimit = 1024;""")

def sleep(ms):

    if TRACE:
        emscripten_run_script("""inSleep = true;""")
        trace = emscripten_run_script_string(r"""stackTrace()""".encode('UTF-8'))
        process_trace(trace)

    emscripten_sleep(ms)

    if TRACE:
        emscripten_run_script("""inSleep = false;""")
        pass


# async_wget
# Requires a C function without parameter, while we need to set
# callpyfunc_arg as callback (so we can call a Python function)
# Perhaps doable if we maintain a list of Python callbacks indexed by 'file' (and ignore potential conflict)
# Or dynamically generate C callbacks in WebAssembly but I doubt that's simple.
# Or implement it with async_wget_data + write output file manually (implies an additional copy)
#def async_wget(url, file, onload, onerror):
#    pass

cdef class pycaller_async_wget:
    cdef onload
    cdef onerror
    cdef arg
    def __cinit__(self, onload, onerror, arg):
        self.onload = onload
        self.onerror = onerror
        self.arg = arg
    #def __dealloc__(self):
    #    print("dealloc")

cdef void pycaller_callback_async_wget_onload(void* p, void* buf, int size) noexcept:
    c = <pycaller_async_wget>p
    # https://cython.readthedocs.io/en/latest/src/tutorial/strings.html#passing-byte-strings
    py_buf = (<char*>buf)[:size]  # copy
    c.onload(c.arg, py_buf)
    Py_XDECREF(<PyObject*>p)
    # 'buf' freed right after by emscripten

cdef void pycaller_callback_async_wget_onerror(void* p) noexcept:
    c = <pycaller_async_wget>p
    if c.onerror is not None:
        c.onerror(c.arg)
    Py_XDECREF(<PyObject*>p)

def async_wget_data(url, arg, onload, onerror=None):
    cdef pycaller_async_wget c = pycaller_async_wget(onload, onerror, arg)
    cdef PyObject* p = <PyObject*>c
    Py_XINCREF(p)  # survive until callback
    emscripten_async_wget_data(url.encode('UTF-8'), p,
                               pycaller_callback_async_wget_onload,
                               pycaller_callback_async_wget_onerror)

# emscripten.async_wget_data('/', {'a':1}, lambda arg,buf: sys.stdout.write(repr(arg)+"\n"+repr(buf)+"\n"), lambda arg: sys.stdout.write(repr(arg)+"\nd/l error\n"))
# emscripten.async_wget_data('https://bank.confidential/', None, None, lambda arg: sys.stdout.write("d/l error\n"))
# emscripten.async_wget_data('https://bank.confidential/', None, None)


# requires -s RETAIN_COMPILER_SETTINGS=1 (otherwise Exception)
def get_compiler_setting(name):
    cdef void* amb = <void*>emscripten_get_compiler_setting(name.encode('UTF-8'))
    # can be int or char*, use heuristic
    # otherwise we could whitelist all known string parameters, if that's possible
    if <int>amb < 1000:
        return <int>amb
    else:
        return <char*>amb  # c_string_encoding
# emscripten.get_compiler_setting('EMULATE_FUNCTION_POINTER_CASTS')
#   1
# emscripten.get_compiler_setting('OPT_LEVEL')
#   3
# emscripten.get_compiler_setting('EMSCRIPTEN_VERSION')
#   u'1.39.0'
# emscripten.get_compiler_setting('non-existent')
#   u'invalid compiler setting: non-existent'
# emscripten.get_compiler_setting('EXPORTED_FUNCTIONS')
#   u'invalid compiler setting: EXPORTED_FUNCTIONS'  # :(

def debugger():
    emscripten_debugger()
# open the JavaScript console
# emscripten.debugger()

def log(flags, fmt, *args):
    # No variadic function support in Cython?
    # No va_arg variant for emscripten_log either.
    # Let's offer limited support
    cdef char* cstr
    cdef char* cformat
    pystrfmt = fmt.encode('UTF-8')
    cformat = pystrfmt
    if len(args) == 0:
        emscripten_log(flags, cformat)
    elif len(args) > 0:
        if len(args) == 1:
            arg = args[0]
            if type(arg) == int:
                emscripten_log(flags, cformat, <int>arg)
            elif type(arg) == float:
                emscripten_log(flags, cformat, <float>arg)
            elif type(arg) in (str, unicode):
                pystr = arg.encode('UTF-8')
                cstr = pystr
                emscripten_log(flags, cformat, cstr)
            else:
                pystr = ("emscripten.log: unsupported argument " + str(type(arg))).encode('UTF-8')
                cstr = pystr
                emscripten_log(flags, cstr)
        else:
            emscripten_log(flags, "emscripten.log: only up to 2 arguments are supported")
# import emscripten; emscripten.log(0, "hello %02d", 1)
# import emscripten; emscripten.log(emscripten.LOG_WARN|emscripten.LOG_CONSOLE|emscripten.LOG_C_STACK, "warning!")
# emscripten_log doesn't to properly support UTF-8
# import emscripten; emscripten.log(0, u"é")
# import emscripten; emscripten.log(0, "%s", u"é")

def get_callstack(flags):
    cdef int size = emscripten_get_callstack(flags, NULL, 0)
    # "subsequent calls will carry different line numbers, so it is
    # best to allocate a few bytes extra to be safe"
    size += 1024
    cdef char* buf = <char*>PyMem_Malloc(size)
    emscripten_get_callstack(flags, buf, size)
    cdef object ret = buf  # c_string_encoding
    PyMem_Free(buf)
    return ret
# from emscripten import *
# print(get_callstack(0))
# print(get_callstack(LOG_C_STACK|LOG_JS_STACK|LOG_DEMANGLE|LOG_NO_PATHS|LOG_FUNC_PARAMS))


# Pseudo-synchronous, requires ASYNCIFY
def wget(url, file):
    return emscripten_wget(url.encode('UTF-8'), file.encode('UTF-8'))
# emscripten.wget('/hello', '/hello'); open('/hello','rb').read()
# Notes:
# - FS error if file already exists
# - Download indicator showing up not going away
# - Download progress bar showing up not going away on error

# Wrap a malloc'd buffer with buffer interface and automatic free()
cdef class MallocBuffer:
    cdef char *buf
    cdef int size
    def __init__(self):
        raise Exception("MallocBuffer: constructor not available from Python")
    # constructor from non-Python parameters (__cinit__ don't accept them)
    @staticmethod
    cdef MallocBuffer from_string_and_size(char* buf, int size):
        cdef MallocBuffer ret = MallocBuffer.__new__(MallocBuffer)
        ret.buf = buf
        ret.size = size
        return ret
    def __dealloc__(self):
        free(self.buf)
    def __getbuffer__(self, Py_buffer *view, int flags):
        is_readonly = 0
        PyBuffer_FillInfo(view, self, <void*>self.buf, self.size, is_readonly, flags)
    def __releasebuffer__(self, Py_buffer *view):
        pass

# Pseudo-synchronous, requires ASYNCIFY
def wget_data(url):
    cdef char* buf
    cdef int num, error
    emscripten_wget_data(url.encode('utf-8'), <void**>&buf, &num, &error)
    if error != 0:
        return None
    pybuf = MallocBuffer.from_string_and_size(buf, num)
    return pybuf


# WebGL

def webgl_enable_extension(extension):
    """
    Tries to enable the given WebGL extension, and returns 1 if it was enabled, 0 otherwise.
    """

    return emscripten_webgl_enable_extension(emscripten_webgl_get_current_context(), extension.encode('UTF-8'))

def webgl_get_supported_extensions():
    """
    Returns a list of extensions that emscripten supports.
    """

    cdef char *extensions = emscripten_webgl_get_supported_extensions()
    rv = extensions.split(' ')
    free(extensions)

    return rv



# Non-API utility

def syncfs():
    emscripten_run_script(r"""
        FS.syncfs(false, function(err) {
            if (err) {
                console.trace(); console.log(err, err.message);
                Module.print("Warning: write error: " + err.message + "\n");
            }
        });
    """);
