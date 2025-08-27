#ifndef PYTHON_THREADS
#define PYTHON_THREADS

#ifdef __EMSCRIPTEN__

static inline void init_python_threads(void) { }

#else

#include "Python.h"

static inline void init_python_threads(void) { PyEval_InitThreads(); }

#endif

#endif
