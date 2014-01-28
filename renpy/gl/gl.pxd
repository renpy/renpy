# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

cdef extern from "glcompat.h":
    ctypedef unsigned int    GLenum
    ctypedef unsigned char   GLboolean
    ctypedef unsigned int    GLbitfield
    ctypedef void            GLvoid
    ctypedef signed char     GLbyte
    ctypedef short           GLshort
    ctypedef int             GLint
    ctypedef unsigned char   GLubyte
    ctypedef unsigned short  GLushort
    ctypedef unsigned int    GLuint
    ctypedef int             GLsizei
    ctypedef float           GLfloat
    ctypedef float           GLclampf
    ctypedef double          GLdouble
    ctypedef double          GLclampd
    ctypedef long int        GLsizeiptrARB
    ctypedef long int        GLintptrARB
    ctypedef unsigned int    GLhandleARB
    ctypedef unsigned int    GLhandle
    ctypedef char            GLchar
    ctypedef char            GLcharARB
    void glClearIndex(GLfloat)
    void glClearColor(GLclampf, GLclampf, GLclampf, GLclampf)
    void glClear(GLbitfield)
    void glIndexMask(GLuint)
    void glColorMask(GLboolean, GLboolean, GLboolean, GLboolean)
    void glAlphaFunc(GLenum, GLclampf)
    void glBlendFunc(GLenum, GLenum)
    void glLogicOp(GLenum)
    void glCullFace(GLenum)
    void glFrontFace(GLenum)
    void glPointSize(GLfloat)
    void glLineWidth(GLfloat)
    void glLineStipple(GLint, GLushort)
    void glPolygonMode(GLenum, GLenum)
    void glPolygonOffset(GLfloat, GLfloat)
    void glPolygonStipple(GLubyte *)
    void glGetPolygonStipple(GLubyte *)
    void glEdgeFlag(GLboolean)
    void glEdgeFlagv(GLboolean *)
    void glScissor(GLint, GLint, GLsizei, GLsizei)
    void glClipPlane(GLenum, GLdouble *)
    void glGetClipPlane(GLenum, GLdouble *)
    void glDrawBuffer(GLenum)
    void glReadBuffer(GLenum)
    void glEnable(GLenum)
    void glDisable(GLenum)
    GLboolean glIsEnabled(GLenum)
    void glEnableClientState(GLenum)
    void glDisableClientState(GLenum)
    void glGetBooleanv(GLenum, GLboolean *)
    void glGetDoublev(GLenum, GLdouble *)
    void glGetFloatv(GLenum, GLfloat *)
    void glGetIntegerv(GLenum, GLint *)
    void glPushAttrib(GLbitfield)
    void glPopAttrib()
    void glPushClientAttrib(GLbitfield)
    void glPopClientAttrib()
    GLint glRenderMode(GLenum)
    GLenum glGetError()
    GLchar * glGetString(GLenum)
    void glFinish()
    void glFlush()
    void glHint(GLenum, GLenum)
    void glClearDepth(GLclampd)
    void glDepthFunc(GLenum)
    void glDepthMask(GLboolean)
    void glDepthRange(GLclampd, GLclampd)
    void glClearAccum(GLfloat, GLfloat, GLfloat, GLfloat)
    void glAccum(GLenum, GLfloat)
    void glMatrixMode(GLenum)
    void glOrtho(GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble)
    void glFrustum(GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble)
    void glViewport(GLint, GLint, GLsizei, GLsizei)
    void glPushMatrix()
    void glPopMatrix()
    void glLoadIdentity()
    void glLoadMatrixd(GLdouble *)
    void glLoadMatrixf(GLfloat *)
    void glMultMatrixd(GLdouble *)
    void glMultMatrixf(GLfloat *)
    void glRotated(GLdouble, GLdouble, GLdouble, GLdouble)
    void glRotatef(GLfloat, GLfloat, GLfloat, GLfloat)
    void glScaled(GLdouble, GLdouble, GLdouble)
    void glScalef(GLfloat, GLfloat, GLfloat)
    void glTranslated(GLdouble, GLdouble, GLdouble)
    void glTranslatef(GLfloat, GLfloat, GLfloat)
    GLboolean glIsList(GLuint)
    void glDeleteLists(GLuint, GLsizei)
    GLuint glGenLists(GLsizei)
    void glNewList(GLuint, GLenum)
    void glEndList()
    void glCallList(GLuint)
    void glCallLists(GLsizei, GLenum, GLubyte *)
    void glListBase(GLuint)
    void glBegin(GLenum)
    void glEnd()
    void glVertex2d(GLdouble, GLdouble)
    void glVertex2f(GLfloat, GLfloat)
    void glVertex2i(GLint, GLint)
    void glVertex2s(GLshort, GLshort)
    void glVertex3d(GLdouble, GLdouble, GLdouble)
    void glVertex3f(GLfloat, GLfloat, GLfloat)
    void glVertex3i(GLint, GLint, GLint)
    void glVertex3s(GLshort, GLshort, GLshort)
    void glVertex4d(GLdouble, GLdouble, GLdouble, GLdouble)
    void glVertex4f(GLfloat, GLfloat, GLfloat, GLfloat)
    void glVertex4i(GLint, GLint, GLint, GLint)
    void glVertex4s(GLshort, GLshort, GLshort, GLshort)
    void glVertex2dv(GLdouble *)
    void glVertex2fv(GLfloat *)
    void glVertex2iv(GLint *)
    void glVertex2sv(GLshort *)
    void glVertex3dv(GLdouble *)
    void glVertex3fv(GLfloat *)
    void glVertex3iv(GLint *)
    void glVertex3sv(GLshort *)
    void glVertex4dv(GLdouble *)
    void glVertex4fv(GLfloat *)
    void glVertex4iv(GLint *)
    void glVertex4sv(GLshort *)
    void glNormal3b(GLbyte, GLbyte, GLbyte)
    void glNormal3d(GLdouble, GLdouble, GLdouble)
    void glNormal3f(GLfloat, GLfloat, GLfloat)
    void glNormal3i(GLint, GLint, GLint)
    void glNormal3s(GLshort, GLshort, GLshort)
    void glNormal3bv(GLbyte *)
    void glNormal3dv(GLdouble *)
    void glNormal3fv(GLfloat *)
    void glNormal3iv(GLint *)
    void glNormal3sv(GLshort *)
    void glIndexd(GLdouble)
    void glIndexf(GLfloat)
    void glIndexi(GLint)
    void glIndexs(GLshort)
    void glIndexub(GLubyte)
    void glIndexdv(GLdouble *)
    void glIndexfv(GLfloat *)
    void glIndexiv(GLint *)
    void glIndexsv(GLshort *)
    void glIndexubv(GLubyte *)
    void glColor3b(GLbyte, GLbyte, GLbyte)
    void glColor3d(GLdouble, GLdouble, GLdouble)
    void glColor3f(GLfloat, GLfloat, GLfloat)
    void glColor3i(GLint, GLint, GLint)
    void glColor3s(GLshort, GLshort, GLshort)
    void glColor3ub(GLubyte, GLubyte, GLubyte)
    void glColor3ui(GLuint, GLuint, GLuint)
    void glColor3us(GLushort, GLushort, GLushort)
    void glColor4b(GLbyte, GLbyte, GLbyte, GLbyte)
    void glColor4d(GLdouble, GLdouble, GLdouble, GLdouble)
    void glColor4f(GLfloat, GLfloat, GLfloat, GLfloat)
    void glColor4i(GLint, GLint, GLint, GLint)
    void glColor4s(GLshort, GLshort, GLshort, GLshort)
    void glColor4ub(GLubyte, GLubyte, GLubyte, GLubyte)
    void glColor4ui(GLuint, GLuint, GLuint, GLuint)
    void glColor4us(GLushort, GLushort, GLushort, GLushort)
    void glColor3bv(GLbyte *)
    void glColor3dv(GLdouble *)
    void glColor3fv(GLfloat *)
    void glColor3iv(GLint *)
    void glColor3sv(GLshort *)
    void glColor3ubv(GLubyte *)
    void glColor3uiv(GLuint *)
    void glColor3usv(GLushort *)
    void glColor4bv(GLbyte *)
    void glColor4dv(GLdouble *)
    void glColor4fv(GLfloat *)
    void glColor4iv(GLint *)
    void glColor4sv(GLshort *)
    void glColor4ubv(GLubyte *)
    void glColor4uiv(GLuint *)
    void glColor4usv(GLushort *)
    void glTexCoord1d(GLdouble)
    void glTexCoord1f(GLfloat)
    void glTexCoord1i(GLint)
    void glTexCoord1s(GLshort)
    void glTexCoord2d(GLdouble, GLdouble)
    void glTexCoord2f(GLfloat, GLfloat)
    void glTexCoord2i(GLint, GLint)
    void glTexCoord2s(GLshort, GLshort)
    void glTexCoord3d(GLdouble, GLdouble, GLdouble)
    void glTexCoord3f(GLfloat, GLfloat, GLfloat)
    void glTexCoord3i(GLint, GLint, GLint)
    void glTexCoord3s(GLshort, GLshort, GLshort)
    void glTexCoord4d(GLdouble, GLdouble, GLdouble, GLdouble)
    void glTexCoord4f(GLfloat, GLfloat, GLfloat, GLfloat)
    void glTexCoord4i(GLint, GLint, GLint, GLint)
    void glTexCoord4s(GLshort, GLshort, GLshort, GLshort)
    void glTexCoord1dv(GLdouble *)
    void glTexCoord1fv(GLfloat *)
    void glTexCoord1iv(GLint *)
    void glTexCoord1sv(GLshort *)
    void glTexCoord2dv(GLdouble *)
    void glTexCoord2fv(GLfloat *)
    void glTexCoord2iv(GLint *)
    void glTexCoord2sv(GLshort *)
    void glTexCoord3dv(GLdouble *)
    void glTexCoord3fv(GLfloat *)
    void glTexCoord3iv(GLint *)
    void glTexCoord3sv(GLshort *)
    void glTexCoord4dv(GLdouble *)
    void glTexCoord4fv(GLfloat *)
    void glTexCoord4iv(GLint *)
    void glTexCoord4sv(GLshort *)
    void glRasterPos2d(GLdouble, GLdouble)
    void glRasterPos2f(GLfloat, GLfloat)
    void glRasterPos2i(GLint, GLint)
    void glRasterPos2s(GLshort, GLshort)
    void glRasterPos3d(GLdouble, GLdouble, GLdouble)
    void glRasterPos3f(GLfloat, GLfloat, GLfloat)
    void glRasterPos3i(GLint, GLint, GLint)
    void glRasterPos3s(GLshort, GLshort, GLshort)
    void glRasterPos4d(GLdouble, GLdouble, GLdouble, GLdouble)
    void glRasterPos4f(GLfloat, GLfloat, GLfloat, GLfloat)
    void glRasterPos4i(GLint, GLint, GLint, GLint)
    void glRasterPos4s(GLshort, GLshort, GLshort, GLshort)
    void glRasterPos2dv(GLdouble *)
    void glRasterPos2fv(GLfloat *)
    void glRasterPos2iv(GLint *)
    void glRasterPos2sv(GLshort *)
    void glRasterPos3dv(GLdouble *)
    void glRasterPos3fv(GLfloat *)
    void glRasterPos3iv(GLint *)
    void glRasterPos3sv(GLshort *)
    void glRasterPos4dv(GLdouble *)
    void glRasterPos4fv(GLfloat *)
    void glRasterPos4iv(GLint *)
    void glRasterPos4sv(GLshort *)
    void glRectd(GLdouble, GLdouble, GLdouble, GLdouble)
    void glRectf(GLfloat, GLfloat, GLfloat, GLfloat)
    void glRecti(GLint, GLint, GLint, GLint)
    void glRects(GLshort, GLshort, GLshort, GLshort)
    void glRectdv(GLdouble *, GLdouble *)
    void glRectfv(GLfloat *, GLfloat *)
    void glRectiv(GLint *, GLint *)
    void glRectsv(GLshort *, GLshort *)
    void glVertexPointer(GLint, GLenum, GLsizei, GLubyte *)
    void glNormalPointer(GLenum, GLsizei, GLubyte *)
    void glColorPointer(GLint, GLenum, GLsizei, GLubyte *)
    void glIndexPointer(GLenum, GLsizei, GLubyte *)
    void glTexCoordPointer(GLint, GLenum, GLsizei, GLubyte *)
    void glEdgeFlagPointer(GLsizei, GLubyte *)
    void glArrayElement(GLint)
    void glDrawArrays(GLenum, GLint, GLsizei)
    void glDrawElements(GLenum, GLsizei, GLenum, GLubyte *)
    void glInterleavedArrays(GLenum, GLsizei, GLubyte *)
    void glShadeModel(GLenum)
    void glLightf(GLenum, GLenum, GLfloat)
    void glLighti(GLenum, GLenum, GLint)
    void glLightfv(GLenum, GLenum, GLfloat *)
    void glLightiv(GLenum, GLenum, GLint *)
    void glGetLightfv(GLenum, GLenum, GLfloat *)
    void glGetLightiv(GLenum, GLenum, GLint *)
    void glLightModelf(GLenum, GLfloat)
    void glLightModeli(GLenum, GLint)
    void glLightModelfv(GLenum, GLfloat *)
    void glLightModeliv(GLenum, GLint *)
    void glMaterialf(GLenum, GLenum, GLfloat)
    void glMateriali(GLenum, GLenum, GLint)
    void glMaterialfv(GLenum, GLenum, GLfloat *)
    void glMaterialiv(GLenum, GLenum, GLint *)
    void glGetMaterialfv(GLenum, GLenum, GLfloat *)
    void glGetMaterialiv(GLenum, GLenum, GLint *)
    void glColorMaterial(GLenum, GLenum)
    void glPixelZoom(GLfloat, GLfloat)
    void glPixelStoref(GLenum, GLfloat)
    void glPixelStorei(GLenum, GLint)
    void glPixelTransferf(GLenum, GLfloat)
    void glPixelTransferi(GLenum, GLint)
    void glPixelMapfv(GLenum, GLsizei, GLubyte *)
    void glPixelMapuiv(GLenum, GLsizei, GLubyte *)
    void glPixelMapusv(GLenum, GLsizei, GLubyte *)
    void glGetPixelMapfv(GLenum, GLubyte *)
    void glGetPixelMapuiv(GLenum, GLubyte *)
    void glGetPixelMapusv(GLenum, GLubyte *)
    void glBitmap(GLsizei, GLsizei, GLfloat, GLfloat, GLfloat, GLfloat, GLubyte *)
    void glReadPixels(GLint, GLint, GLsizei, GLsizei, GLenum, GLenum, GLubyte *)
    void glDrawPixels(GLsizei, GLsizei, GLenum, GLenum, GLubyte *)
    void glCopyPixels(GLint, GLint, GLsizei, GLsizei, GLenum)
    void glStencilFunc(GLenum, GLint, GLuint)
    void glStencilMask(GLuint)
    void glStencilOp(GLenum, GLenum, GLenum)
    void glClearStencil(GLint)
    void glTexGend(GLenum, GLenum, GLdouble)
    void glTexGenf(GLenum, GLenum, GLfloat)
    void glTexGeni(GLenum, GLenum, GLint)
    void glTexGendv(GLenum, GLenum, GLdouble *)
    void glTexGenfv(GLenum, GLenum, GLfloat *)
    void glTexGeniv(GLenum, GLenum, GLint *)
    void glGetTexGendv(GLenum, GLenum, GLdouble *)
    void glGetTexGenfv(GLenum, GLenum, GLfloat *)
    void glGetTexGeniv(GLenum, GLenum, GLint *)
    void glTexEnvf(GLenum, GLenum, GLfloat)
    void glTexEnvi(GLenum, GLenum, GLint)
    void glTexEnvfv(GLenum, GLenum, GLfloat *)
    void glTexEnviv(GLenum, GLenum, GLint *)
    void glGetTexEnvfv(GLenum, GLenum, GLfloat *)
    void glGetTexEnviv(GLenum, GLenum, GLint *)
    void glTexParameterf(GLenum, GLenum, GLfloat)
    void glTexParameteri(GLenum, GLenum, GLint)
    void glTexParameterfv(GLenum, GLenum, GLfloat *)
    void glTexParameteriv(GLenum, GLenum, GLint *)
    void glGetTexParameterfv(GLenum, GLenum, GLfloat *)
    void glGetTexParameteriv(GLenum, GLenum, GLint *)
    void glGetTexLevelParameterfv(GLenum, GLint, GLenum, GLfloat *)
    void glGetTexLevelParameteriv(GLenum, GLint, GLenum, GLint *)
    void glTexImage1D(GLenum, GLint, GLint, GLsizei, GLint, GLenum, GLenum, GLubyte *)
    void glTexImage2D(GLenum, GLint, GLint, GLsizei, GLsizei, GLint, GLenum, GLenum, GLubyte *)
    void glGetTexImage(GLenum, GLint, GLenum, GLenum, GLubyte *)
    void glBindTexture(GLenum, GLuint)
    GLboolean glIsTexture(GLuint)
    void glTexSubImage1D(GLenum, GLint, GLint, GLsizei, GLenum, GLenum, GLubyte *)
    void glTexSubImage2D(GLenum, GLint, GLint, GLint, GLsizei, GLsizei, GLenum, GLenum, GLubyte *)
    void glCopyTexImage1D(GLenum, GLint, GLenum, GLint, GLint, GLsizei, GLint)
    void glCopyTexImage2D(GLenum, GLint, GLenum, GLint, GLint, GLsizei, GLsizei, GLint)
    void glCopyTexSubImage1D(GLenum, GLint, GLint, GLint, GLint, GLsizei)
    void glCopyTexSubImage2D(GLenum, GLint, GLint, GLint, GLint, GLint, GLsizei, GLsizei)
    void glGenTextures(GLsizei, GLuint *)
    void glDeleteTextures(GLsizei, GLuint *)
    void glPrioritizeTextures(GLsizei, GLuint *, GLclampf *)
    GLboolean glAreTexturesResident(GLsizei, GLuint *, GLboolean *)
    void glMap1d(GLenum, GLdouble, GLdouble, GLint, GLint, GLubyte *)
    void glMap1f(GLenum, GLfloat, GLfloat, GLint, GLint, GLubyte *)
    void glMap2d(GLenum, GLdouble, GLdouble, GLint, GLint, GLdouble, GLdouble, GLint, GLint, GLubyte *)
    void glMap2f(GLenum, GLfloat, GLfloat, GLint, GLint, GLfloat, GLfloat, GLint, GLint, GLubyte *)
    void glGetMapdv(GLenum, GLenum, GLubyte *)
    void glGetMapfv(GLenum, GLenum, GLubyte *)
    void glGetMapiv(GLenum, GLenum, GLubyte *)
    void glEvalCoord1d(GLdouble)
    void glEvalCoord1f(GLfloat)
    void glEvalCoord1dv(GLdouble *)
    void glEvalCoord1fv(GLfloat *)
    void glEvalCoord2d(GLdouble, GLdouble)
    void glEvalCoord2f(GLfloat, GLfloat)
    void glEvalCoord2dv(GLdouble *)
    void glEvalCoord2fv(GLfloat *)
    void glMapGrid1d(GLint, GLdouble, GLdouble)
    void glMapGrid1f(GLint, GLfloat, GLfloat)
    void glMapGrid2d(GLint, GLdouble, GLdouble, GLint, GLdouble, GLdouble)
    void glMapGrid2f(GLint, GLfloat, GLfloat, GLint, GLfloat, GLfloat)
    void glEvalPoint1(GLint)
    void glEvalPoint2(GLint, GLint)
    void glEvalMesh1(GLenum, GLint, GLint)
    void glEvalMesh2(GLenum, GLint, GLint, GLint, GLint)
    void glFogf(GLenum, GLfloat)
    void glFogi(GLenum, GLint)
    void glFogfv(GLenum, GLfloat *)
    void glFogiv(GLenum, GLint *)
    void glFeedbackBuffer(GLsizei, GLenum, GLubyte *)
    void glPassThrough(GLfloat)
    void glSelectBuffer(GLsizei, GLubyte *)
    void glInitNames()
    void glLoadName(GLuint)
    void glPushName(GLuint)
    void glPopName()
    void glDrawRangeElements(GLenum, GLuint, GLuint, GLsizei, GLenum, GLubyte *)
    void glTexImage3D(GLenum, GLint, GLint, GLsizei, GLsizei, GLsizei, GLint, GLenum, GLenum, GLubyte *)
    void glTexSubImage3D(GLenum, GLint, GLint, GLint, GLint, GLsizei, GLsizei, GLsizei, GLenum, GLenum, GLubyte *)
    void glCopyTexSubImage3D(GLenum, GLint, GLint, GLint, GLint, GLint, GLint, GLsizei, GLsizei)
    void glActiveTexture(GLenum)
    void glClientActiveTexture(GLenum)
    void glCompressedTexImage1D(GLenum, GLint, GLenum, GLsizei, GLint, GLsizei, GLubyte *)
    void glCompressedTexImage2D(GLenum, GLint, GLenum, GLsizei, GLsizei, GLint, GLsizei, GLubyte *)
    void glCompressedTexImage3D(GLenum, GLint, GLenum, GLsizei, GLsizei, GLsizei, GLint, GLsizei, GLubyte *)
    void glCompressedTexSubImage1D(GLenum, GLint, GLint, GLsizei, GLenum, GLsizei, GLubyte *)
    void glCompressedTexSubImage2D(GLenum, GLint, GLint, GLint, GLsizei, GLsizei, GLenum, GLsizei, GLubyte *)
    void glCompressedTexSubImage3D(GLenum, GLint, GLint, GLint, GLint, GLsizei, GLsizei, GLsizei, GLenum, GLsizei, GLubyte *)
    void glGetCompressedTexImage(GLenum, GLint, GLubyte *)
    void glMultiTexCoord1d(GLenum, GLdouble)
    void glMultiTexCoord1dv(GLenum, GLdouble *)
    void glMultiTexCoord1f(GLenum, GLfloat)
    void glMultiTexCoord1fv(GLenum, GLfloat *)
    void glMultiTexCoord1i(GLenum, GLint)
    void glMultiTexCoord1iv(GLenum, GLint *)
    void glMultiTexCoord1s(GLenum, GLshort)
    void glMultiTexCoord1sv(GLenum, GLshort *)
    void glMultiTexCoord2d(GLenum, GLdouble, GLdouble)
    void glMultiTexCoord2dv(GLenum, GLdouble *)
    void glMultiTexCoord2f(GLenum, GLfloat, GLfloat)
    void glMultiTexCoord2fv(GLenum, GLfloat *)
    void glMultiTexCoord2i(GLenum, GLint, GLint)
    void glMultiTexCoord2iv(GLenum, GLint *)
    void glMultiTexCoord2s(GLenum, GLshort, GLshort)
    void glMultiTexCoord2sv(GLenum, GLshort *)
    void glMultiTexCoord3d(GLenum, GLdouble, GLdouble, GLdouble)
    void glMultiTexCoord3dv(GLenum, GLdouble *)
    void glMultiTexCoord3f(GLenum, GLfloat, GLfloat, GLfloat)
    void glMultiTexCoord3fv(GLenum, GLfloat *)
    void glMultiTexCoord3i(GLenum, GLint, GLint, GLint)
    void glMultiTexCoord3iv(GLenum, GLint *)
    void glMultiTexCoord3s(GLenum, GLshort, GLshort, GLshort)
    void glMultiTexCoord3sv(GLenum, GLshort *)
    void glMultiTexCoord4d(GLenum, GLdouble, GLdouble, GLdouble, GLdouble)
    void glMultiTexCoord4dv(GLenum, GLdouble *)
    void glMultiTexCoord4f(GLenum, GLfloat, GLfloat, GLfloat, GLfloat)
    void glMultiTexCoord4fv(GLenum, GLfloat *)
    void glMultiTexCoord4i(GLenum, GLint, GLint, GLint, GLint)
    void glMultiTexCoord4iv(GLenum, GLint *)
    void glMultiTexCoord4s(GLenum, GLshort, GLshort, GLshort, GLshort)
    void glMultiTexCoord4sv(GLenum, GLshort *)
    void glLoadTransposeMatrixd(GLdouble *)
    void glLoadTransposeMatrixf(GLfloat *)
    void glMultTransposeMatrixd(GLdouble *)
    void glMultTransposeMatrixf(GLfloat *)
    void glSampleCoverage(GLclampf, GLboolean)
    void glActiveTextureARB(GLenum)
    void glClientActiveTextureARB(GLenum)
    void glMultiTexCoord1dARB(GLenum, GLdouble)
    void glMultiTexCoord1dvARB(GLenum, GLdouble *)
    void glMultiTexCoord1fARB(GLenum, GLfloat)
    void glMultiTexCoord1fvARB(GLenum, GLfloat *)
    void glMultiTexCoord1iARB(GLenum, GLint)
    void glMultiTexCoord1ivARB(GLenum, GLint *)
    void glMultiTexCoord1sARB(GLenum, GLshort)
    void glMultiTexCoord1svARB(GLenum, GLshort *)
    void glMultiTexCoord2dARB(GLenum, GLdouble, GLdouble)
    void glMultiTexCoord2dvARB(GLenum, GLdouble *)
    void glMultiTexCoord2fARB(GLenum, GLfloat, GLfloat)
    void glMultiTexCoord2fvARB(GLenum, GLfloat *)
    void glMultiTexCoord2iARB(GLenum, GLint, GLint)
    void glMultiTexCoord2ivARB(GLenum, GLint *)
    void glMultiTexCoord2sARB(GLenum, GLshort, GLshort)
    void glMultiTexCoord2svARB(GLenum, GLshort *)
    void glMultiTexCoord3dARB(GLenum, GLdouble, GLdouble, GLdouble)
    void glMultiTexCoord3dvARB(GLenum, GLdouble *)
    void glMultiTexCoord3fARB(GLenum, GLfloat, GLfloat, GLfloat)
    void glMultiTexCoord3fvARB(GLenum, GLfloat *)
    void glMultiTexCoord3iARB(GLenum, GLint, GLint, GLint)
    void glMultiTexCoord3ivARB(GLenum, GLint *)
    void glMultiTexCoord3sARB(GLenum, GLshort, GLshort, GLshort)
    void glMultiTexCoord3svARB(GLenum, GLshort *)
    void glMultiTexCoord4dARB(GLenum, GLdouble, GLdouble, GLdouble, GLdouble)
    void glMultiTexCoord4dvARB(GLenum, GLdouble *)
    void glMultiTexCoord4fARB(GLenum, GLfloat, GLfloat, GLfloat, GLfloat)
    void glMultiTexCoord4fvARB(GLenum, GLfloat *)
    void glMultiTexCoord4iARB(GLenum, GLint, GLint, GLint, GLint)
    void glMultiTexCoord4ivARB(GLenum, GLint *)
    void glMultiTexCoord4sARB(GLenum, GLshort, GLshort, GLshort, GLshort)
    void glMultiTexCoord4svARB(GLenum, GLshort *)
    void glVertexAttrib1dARB(GLuint, GLdouble)
    void glVertexAttrib1dvARB(GLuint, GLdouble *)
    void glVertexAttrib1fARB(GLuint, GLfloat)
    void glVertexAttrib1fvARB(GLuint, GLfloat *)
    void glVertexAttrib1sARB(GLuint, GLshort)
    void glVertexAttrib1svARB(GLuint, GLshort *)
    void glVertexAttrib2dARB(GLuint, GLdouble, GLdouble)
    void glVertexAttrib2dvARB(GLuint, GLdouble *)
    void glVertexAttrib2fARB(GLuint, GLfloat, GLfloat)
    void glVertexAttrib2fvARB(GLuint, GLfloat *)
    void glVertexAttrib2sARB(GLuint, GLshort, GLshort)
    void glVertexAttrib2svARB(GLuint, GLshort *)
    void glVertexAttrib3dARB(GLuint, GLdouble, GLdouble, GLdouble)
    void glVertexAttrib3dvARB(GLuint, GLdouble *)
    void glVertexAttrib3fARB(GLuint, GLfloat, GLfloat, GLfloat)
    void glVertexAttrib3fvARB(GLuint, GLfloat *)
    void glVertexAttrib3sARB(GLuint, GLshort, GLshort, GLshort)
    void glVertexAttrib3svARB(GLuint, GLshort *)
    void glVertexAttrib4NbvARB(GLuint, GLbyte *)
    void glVertexAttrib4NivARB(GLuint, GLint *)
    void glVertexAttrib4NsvARB(GLuint, GLshort *)
    void glVertexAttrib4NubARB(GLuint, GLubyte, GLubyte, GLubyte, GLubyte)
    void glVertexAttrib4NubvARB(GLuint, GLubyte *)
    void glVertexAttrib4NuivARB(GLuint, GLuint *)
    void glVertexAttrib4NusvARB(GLuint, GLushort *)
    void glVertexAttrib4bvARB(GLuint, GLbyte *)
    void glVertexAttrib4dARB(GLuint, GLdouble, GLdouble, GLdouble, GLdouble)
    void glVertexAttrib4dvARB(GLuint, GLdouble *)
    void glVertexAttrib4fARB(GLuint, GLfloat, GLfloat, GLfloat, GLfloat)
    void glVertexAttrib4fvARB(GLuint, GLfloat *)
    void glVertexAttrib4ivARB(GLuint, GLint *)
    void glVertexAttrib4sARB(GLuint, GLshort, GLshort, GLshort, GLshort)
    void glVertexAttrib4svARB(GLuint, GLshort *)
    void glVertexAttrib4ubvARB(GLuint, GLubyte *)
    void glVertexAttrib4uivARB(GLuint, GLuint *)
    void glVertexAttrib4usvARB(GLuint, GLushort *)
    void glVertexAttribPointerARB(GLuint, GLint, GLenum, GLboolean, GLsizei, GLubyte *)
    void glEnableVertexAttribArrayARB(GLuint)
    void glDisableVertexAttribArrayARB(GLuint)
    void glProgramStringARB(GLenum, GLenum, GLsizei, GLubyte *)
    void glBindProgramARB(GLenum, GLuint)
    void glDeleteProgramsARB(GLsizei, GLuint *)
    void glGenProgramsARB(GLsizei, GLuint *)
    void glProgramEnvParameter4dARB(GLenum, GLuint, GLdouble, GLdouble, GLdouble, GLdouble)
    void glProgramEnvParameter4dvARB(GLenum, GLuint, GLdouble *)
    void glProgramEnvParameter4fARB(GLenum, GLuint, GLfloat, GLfloat, GLfloat, GLfloat)
    void glProgramEnvParameter4fvARB(GLenum, GLuint, GLfloat *)
    void glProgramLocalParameter4dARB(GLenum, GLuint, GLdouble, GLdouble, GLdouble, GLdouble)
    void glProgramLocalParameter4dvARB(GLenum, GLuint, GLdouble *)
    void glProgramLocalParameter4fARB(GLenum, GLuint, GLfloat, GLfloat, GLfloat, GLfloat)
    void glProgramLocalParameter4fvARB(GLenum, GLuint, GLfloat *)
    void glGetProgramEnvParameterdvARB(GLenum, GLuint, GLdouble *)
    void glGetProgramEnvParameterfvARB(GLenum, GLuint, GLfloat *)
    void glGetProgramLocalParameterdvARB(GLenum, GLuint, GLdouble *)
    void glGetProgramLocalParameterfvARB(GLenum, GLuint, GLfloat *)
    void glGetProgramivARB(GLenum, GLenum, GLint *)
    void glGetProgramStringARB(GLenum, GLenum, GLchar *)
    void glGetVertexAttribdvARB(GLuint, GLenum, GLdouble *)
    void glGetVertexAttribfvARB(GLuint, GLenum, GLfloat *)
    void glGetVertexAttribivARB(GLuint, GLenum, GLint *)
    GLboolean glIsProgramARB(GLuint)
    void glBindBufferARB(GLenum, GLuint)
    GLboolean glIsBufferARB(GLuint)
    void glBufferDataARB(GLenum, GLsizeiptrARB, GLubyte *, GLenum)
    void glBufferSubDataARB(GLenum, GLintptrARB, GLsizeiptrARB, GLubyte *)
    void glGetBufferSubDataARB(GLenum, GLintptrARB, GLsizeiptrARB, GLubyte *)
    GLvoid * glMapBufferARB(GLenum, GLenum)
    GLboolean glUnmapBufferARB(GLenum)
    void glGetBufferParameterivARB(GLenum, GLenum, GLint *)
    void glDeleteObjectARB(GLhandleARB)
    GLhandleARB glGetHandleARB(GLenum)
    void glDetachObjectARB(GLhandleARB, GLhandleARB)
    GLhandleARB glCreateShaderObjectARB(GLenum)
    void glShaderSourceARB(GLhandleARB, GLsizei, GLchar * *, GLint *)
    void glCompileShaderARB(GLhandleARB)
    GLhandleARB glCreateProgramObjectARB()
    void glAttachObjectARB(GLhandleARB, GLhandleARB)
    void glLinkProgramARB(GLhandleARB)
    void glUseProgramObjectARB(GLhandleARB)
    void glValidateProgramARB(GLhandleARB)
    void glUniform1fARB(GLint, GLfloat)
    void glUniform2fARB(GLint, GLfloat, GLfloat)
    void glUniform3fARB(GLint, GLfloat, GLfloat, GLfloat)
    void glUniform4fARB(GLint, GLfloat, GLfloat, GLfloat, GLfloat)
    void glUniform1iARB(GLint, GLint)
    void glUniform2iARB(GLint, GLint, GLint)
    void glUniform3iARB(GLint, GLint, GLint, GLint)
    void glUniform4iARB(GLint, GLint, GLint, GLint, GLint)
    void glUniform1fvARB(GLint, GLsizei, GLfloat *)
    void glUniform2fvARB(GLint, GLsizei, GLfloat *)
    void glUniform3fvARB(GLint, GLsizei, GLfloat *)
    void glUniform4fvARB(GLint, GLsizei, GLfloat *)
    void glUniform1ivARB(GLint, GLsizei, GLint *)
    void glUniform2ivARB(GLint, GLsizei, GLint *)
    void glUniform3ivARB(GLint, GLsizei, GLint *)
    void glUniform4ivARB(GLint, GLsizei, GLint *)
    void glUniformMatrix2fvARB(GLint, GLsizei, GLboolean, GLfloat *)
    void glUniformMatrix3fvARB(GLint, GLsizei, GLboolean, GLfloat *)
    void glUniformMatrix4fvARB(GLint, GLsizei, GLboolean, GLfloat *)
    void glGetObjectParameterfvARB(GLhandleARB, GLenum, GLfloat *)
    void glGetObjectParameterivARB(GLhandleARB, GLenum, GLint *)
    void glGetInfoLogARB(GLhandleARB, GLsizei, GLsizei *, GLchar *)
    void glGetAttachedObjectsARB(GLhandleARB, GLsizei, GLsizei *, GLubyte *)
    GLint glGetUniformLocationARB(GLhandleARB, GLchar *)
    void glGetActiveUniformARB(GLhandleARB, GLuint, GLsizei, GLsizei *, GLint *, GLenum *, GLchar *)
    void glGetUniformfvARB(GLhandleARB, GLint, GLfloat *)
    void glGetUniformivARB(GLhandleARB, GLint, GLint *)
    void glGetShaderSourceARB(GLhandleARB, GLsizei, GLsizei *, GLchar *)
    void glBindAttribLocationARB(GLhandleARB, GLuint, GLchar *)
    void glGetActiveAttribARB(GLhandleARB, GLuint, GLsizei, GLsizei *, GLint *, GLenum *, GLchar *)
    GLint glGetAttribLocationARB(GLhandleARB, GLchar *)
    void glGetProgramiv(GLuint, GLenum, GLint *)
    void glGetShaderiv(GLuint, GLenum, GLint *)
    void glDeleteProgram(GLuint)
    void glDeleteShader(GLuint)
    void glGetProgramInfoLog(GLhandleARB, GLsizei, GLsizei *, GLchar *)
    void glGetShaderInfoLog(GLhandleARB, GLsizei, GLsizei *, GLchar *)
    GLboolean glIsRenderbufferEXT(GLuint)
    void glBindRenderbufferEXT(GLenum, GLuint)
    void glDeleteRenderbuffersEXT(GLsizei, GLuint *)
    void glGenRenderbuffersEXT(GLsizei, GLuint *)
    void glRenderbufferStorageEXT(GLenum, GLenum, GLsizei, GLsizei)
    void glGetRenderbufferParameterivEXT(GLenum, GLenum, GLint *)
    GLboolean glIsFramebufferEXT(GLuint)
    void glBindFramebufferEXT(GLenum, GLuint)
    void glDeleteFramebuffersEXT(GLsizei, GLuint *)
    void glGenFramebuffersEXT(GLsizei, GLuint *)
    GLenum glCheckFramebufferStatusEXT(GLenum)
    void glFramebufferTexture1DEXT(GLenum, GLenum, GLenum, GLuint, GLint)
    void glFramebufferTexture2DEXT(GLenum, GLenum, GLenum, GLuint, GLint)
    void glFramebufferTexture3DEXT(GLenum, GLenum, GLenum, GLuint, GLint, GLint)
    void glFramebufferRenderbufferEXT(GLenum, GLenum, GLenum, GLuint)
    void glGetFramebufferAttachmentParameterivEXT(GLenum, GLenum, GLenum, GLint *)
    void glGenerateMipmapEXT(GLenum)

    enum:
        GL_2D
        GL_2_BYTES
        GL_3D
        GL_3D_COLOR
        GL_3D_COLOR_TEXTURE
        GL_3_BYTES
        GL_4D_COLOR_TEXTURE
        GL_4_BYTES
        GL_ACCUM
        GL_ACCUM_ALPHA_BITS
        GL_ACCUM_BLUE_BITS
        GL_ACCUM_BUFFER_BIT
        GL_ACCUM_CLEAR_VALUE
        GL_ACCUM_GREEN_BITS
        GL_ACCUM_RED_BITS
        GL_ACTIVE_TEXTURE
        GL_ACTIVE_TEXTURE_ARB
        GL_ADD
        GL_ADD_SIGNED
        GL_ADD_SIGNED_ARB
        GL_ALIASED_LINE_WIDTH_RANGE
        GL_ALIASED_POINT_SIZE_RANGE
        GL_ALL_ATTRIB_BITS
        GL_ALPHA
        GL_ALPHA12
        GL_ALPHA16
        GL_ALPHA4
        GL_ALPHA8
        GL_ALPHA_BIAS
        GL_ALPHA_BITS
        GL_ALPHA_SCALE
        GL_ALPHA_TEST
        GL_ALPHA_TEST_FUNC
        GL_ALPHA_TEST_REF
        GL_ALWAYS
        GL_AMBIENT
        GL_AMBIENT_AND_DIFFUSE
        GL_AND
        GL_AND_INVERTED
        GL_AND_REVERSE
        GL_ARRAY_BUFFER_ARB
        GL_ARRAY_BUFFER_BINDING_ARB
        GL_ATTRIB_STACK_DEPTH
        GL_AUTO_NORMAL
        GL_AUX0
        GL_AUX1
        GL_AUX2
        GL_AUX3
        GL_AUX_BUFFERS
        GL_BACK
        GL_BACK_LEFT
        GL_BACK_RIGHT
        GL_BGR
        GL_BGRA
        GL_BGRA
        GL_BITMAP
        GL_BITMAP_TOKEN
        GL_BLEND
        GL_BLEND_DST
        GL_BLEND_SRC
        GL_BLUE
        GL_BLUE_BIAS
        GL_BLUE_BITS
        GL_BLUE_SCALE
        GL_BOOL_ARB
        GL_BOOL_VEC2_ARB
        GL_BOOL_VEC3_ARB
        GL_BOOL_VEC4_ARB
        GL_BUFFER_ACCESS_ARB
        GL_BUFFER_MAPPED_ARB
        GL_BUFFER_MAP_POINTER_ARB
        GL_BUFFER_SIZE_ARB
        GL_BUFFER_USAGE_ARB
        GL_BYTE
        GL_C3F_V3F
        GL_C4F_N3F_V3F
        GL_C4UB_V2F
        GL_C4UB_V3F
        GL_CCW
        GL_CLAMP
        GL_CLAMP_TO_BORDER
        GL_CLAMP_TO_EDGE
        GL_CLEAR
        GL_CLIENT_ACTIVE_TEXTURE
        GL_CLIENT_ACTIVE_TEXTURE_ARB
        GL_CLIENT_ALL_ATTRIB_BITS
        GL_CLIENT_ATTRIB_STACK_DEPTH
        GL_CLIENT_PIXEL_STORE_BIT
        GL_CLIENT_VERTEX_ARRAY_BIT
        GL_CLIP_PLANE0
        GL_CLIP_PLANE1
        GL_CLIP_PLANE2
        GL_CLIP_PLANE3
        GL_CLIP_PLANE4
        GL_CLIP_PLANE5
        GL_COEFF
        GL_COLOR
        GL_COLOR_ARRAY
        GL_COLOR_ARRAY_BUFFER_BINDING_ARB
        GL_COLOR_ARRAY_POINTER
        GL_COLOR_ARRAY_SIZE
        GL_COLOR_ARRAY_STRIDE
        GL_COLOR_ARRAY_TYPE
        GL_COLOR_ATTACHMENT0_EXT
        GL_COLOR_ATTACHMENT10_EXT
        GL_COLOR_ATTACHMENT11_EXT
        GL_COLOR_ATTACHMENT12_EXT
        GL_COLOR_ATTACHMENT13_EXT
        GL_COLOR_ATTACHMENT14_EXT
        GL_COLOR_ATTACHMENT15_EXT
        GL_COLOR_ATTACHMENT1_EXT
        GL_COLOR_ATTACHMENT2_EXT
        GL_COLOR_ATTACHMENT3_EXT
        GL_COLOR_ATTACHMENT4_EXT
        GL_COLOR_ATTACHMENT5_EXT
        GL_COLOR_ATTACHMENT6_EXT
        GL_COLOR_ATTACHMENT7_EXT
        GL_COLOR_ATTACHMENT8_EXT
        GL_COLOR_ATTACHMENT9_EXT
        GL_COLOR_BUFFER_BIT
        GL_COLOR_CLEAR_VALUE
        GL_COLOR_INDEX
        GL_COLOR_INDEXES
        GL_COLOR_LOGIC_OP
        GL_COLOR_MATERIAL
        GL_COLOR_MATERIAL_FACE
        GL_COLOR_MATERIAL_PARAMETER
        GL_COLOR_SUM_ARB
        GL_COLOR_WRITEMASK
        GL_COMBINE
        GL_COMBINE_ALPHA
        GL_COMBINE_ALPHA_ARB
        GL_COMBINE_ARB
        GL_COMBINE_RGB
        GL_COMBINE_RGB_ARB
        GL_COMPILE
        GL_COMPILE_AND_EXECUTE
        GL_COMPRESSED_ALPHA
        GL_COMPRESSED_INTENSITY
        GL_COMPRESSED_LUMINANCE
        GL_COMPRESSED_LUMINANCE_ALPHA
        GL_COMPRESSED_RGB
        GL_COMPRESSED_RGBA
        GL_COMPRESSED_TEXTURE_FORMATS
        GL_CONSTANT
        GL_CONSTANT_ARB
        GL_CONSTANT_ATTENUATION
        GL_COPY
        GL_COPY_INVERTED
        GL_COPY_PIXEL_TOKEN
        GL_CULL_FACE
        GL_CULL_FACE_MODE
        GL_CURRENT_BIT
        GL_CURRENT_COLOR
        GL_CURRENT_INDEX
        GL_CURRENT_MATRIX_ARB
        GL_CURRENT_MATRIX_STACK_DEPTH_ARB
        GL_CURRENT_NORMAL
        GL_CURRENT_RASTER_COLOR
        GL_CURRENT_RASTER_DISTANCE
        GL_CURRENT_RASTER_INDEX
        GL_CURRENT_RASTER_POSITION
        GL_CURRENT_RASTER_POSITION_VALID
        GL_CURRENT_RASTER_TEXTURE_COORDS
        GL_CURRENT_TEXTURE_COORDS
        GL_CURRENT_VERTEX_ATTRIB_ARB
        GL_CW
        GL_DECAL
        GL_DECR
        GL_DEPTH
        GL_DEPTH_ATTACHMENT_EXT
        GL_DEPTH_BIAS
        GL_DEPTH_BITS
        GL_DEPTH_BUFFER_BIT
        GL_DEPTH_CLEAR_VALUE
        GL_DEPTH_COMPONENT
        GL_DEPTH_FUNC
        GL_DEPTH_RANGE
        GL_DEPTH_SCALE
        GL_DEPTH_TEST
        GL_DEPTH_WRITEMASK
        GL_DIFFUSE
        GL_DITHER
        GL_DOMAIN
        GL_DONT_CARE
        GL_DOT3_RGB
        GL_DOT3_RGBA
        GL_DOUBLE
        GL_DOUBLEBUFFER
        GL_DRAW_BUFFER
        GL_DRAW_PIXEL_TOKEN
        GL_DST_ALPHA
        GL_DST_COLOR
        GL_DYNAMIC_COPY_ARB
        GL_DYNAMIC_DRAW_ARB
        GL_DYNAMIC_READ_ARB
        GL_EDGE_FLAG
        GL_EDGE_FLAG_ARRAY
        GL_EDGE_FLAG_ARRAY_BUFFER_BINDING_ARB
        GL_EDGE_FLAG_ARRAY_POINTER
        GL_EDGE_FLAG_ARRAY_STRIDE
        GL_ELEMENT_ARRAY_BUFFER_ARB
        GL_ELEMENT_ARRAY_BUFFER_BINDING_ARB
        GL_EMISSION
        GL_ENABLE_BIT
        GL_EQUAL
        GL_EQUIV
        GL_EVAL_BIT
        GL_EXP
        GL_EXP2
        GL_EXTENSIONS
        GL_EYE_LINEAR
        GL_EYE_PLANE
        GL_FALSE
        GL_FASTEST
        GL_FEEDBACK
        GL_FEEDBACK_BUFFER_POINTER
        GL_FEEDBACK_BUFFER_SIZE
        GL_FEEDBACK_BUFFER_TYPE
        GL_FILL
        GL_FLAT
        GL_FLOAT
        GL_FLOAT_MAT2_ARB
        GL_FLOAT_MAT3_ARB
        GL_FLOAT_MAT4_ARB
        GL_FLOAT_VEC2_ARB
        GL_FLOAT_VEC3_ARB
        GL_FLOAT_VEC4_ARB
        GL_FOG
        GL_FOG_BIT
        GL_FOG_COLOR
        GL_FOG_COORDINATE_ARRAY_BUFFER_BINDING_ARB
        GL_FOG_DENSITY
        GL_FOG_END
        GL_FOG_HINT
        GL_FOG_INDEX
        GL_FOG_MODE
        GL_FOG_START
        GL_FRAGMENT_PROGRAM_ARB
        GL_FRAGMENT_SHADER_ARB
        GL_FRAGMENT_SHADER_DERIVATIVE_HINT_ARB
        GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME_EXT
        GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE_EXT
        GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_3D_ZOFFSET_EXT
        GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_CUBE_MAP_FACE_EXT
        GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL_EXT
        GL_FRAMEBUFFER_BINDING_EXT
        GL_FRAMEBUFFER_COMPLETE_EXT
        GL_FRAMEBUFFER_EXT
        GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT_EXT
        GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS_EXT
        GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER_EXT
        GL_FRAMEBUFFER_INCOMPLETE_FORMATS_EXT
        GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT_EXT
        GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER_EXT
        GL_FRAMEBUFFER_UNSUPPORTED_EXT
        GL_FRONT
        GL_FRONT_AND_BACK
        GL_FRONT_FACE
        GL_FRONT_LEFT
        GL_FRONT_RIGHT
        GL_GEQUAL
        GL_GREATER
        GL_GREEN
        GL_GREEN_BIAS
        GL_GREEN_BITS
        GL_GREEN_SCALE
        GL_HINT_BIT
        GL_INCR
        GL_INDEX_ARRAY
        GL_INDEX_ARRAY_BUFFER_BINDING_ARB
        GL_INDEX_ARRAY_POINTER
        GL_INDEX_ARRAY_STRIDE
        GL_INDEX_ARRAY_TYPE
        GL_INDEX_BITS
        GL_INDEX_CLEAR_VALUE
        GL_INDEX_LOGIC_OP
        GL_INDEX_MODE
        GL_INDEX_OFFSET
        GL_INDEX_SHIFT
        GL_INDEX_WRITEMASK
        GL_INFO_LOG_LENGTH
        GL_INT
        GL_INTENSITY
        GL_INTENSITY12
        GL_INTENSITY16
        GL_INTENSITY4
        GL_INTENSITY8
        GL_INTERPOLATE
        GL_INTERPOLATE_ARB
        GL_INT_VEC2_ARB
        GL_INT_VEC3_ARB
        GL_INT_VEC4_ARB
        GL_INVALID_ENUM
        GL_INVALID_OPERATION
        GL_INVALID_VALUE
        GL_INVERT
        GL_KEEP
        GL_LEFT
        GL_LEQUAL
        GL_LESS
        GL_LIGHT0
        GL_LIGHT1
        GL_LIGHT2
        GL_LIGHT3
        GL_LIGHT4
        GL_LIGHT5
        GL_LIGHT6
        GL_LIGHT7
        GL_LIGHTING
        GL_LIGHTING_BIT
        GL_LIGHT_MODEL_AMBIENT
        GL_LIGHT_MODEL_COLOR_CONTROL
        GL_LIGHT_MODEL_LOCAL_VIEWER
        GL_LIGHT_MODEL_TWO_SIDE
        GL_LINE
        GL_LINEAR
        GL_LINEAR_ATTENUATION
        GL_LINEAR_MIPMAP_LINEAR
        GL_LINEAR_MIPMAP_NEAREST
        GL_LINES
        GL_LINE_BIT
        GL_LINE_LOOP
        GL_LINE_RESET_TOKEN
        GL_LINE_SMOOTH
        GL_LINE_SMOOTH_HINT
        GL_LINE_STIPPLE
        GL_LINE_STIPPLE_PATTERN
        GL_LINE_STIPPLE_REPEAT
        GL_LINE_STRIP
        GL_LINE_TOKEN
        GL_LINE_WIDTH
        GL_LINE_WIDTH_GRANULARITY
        GL_LINE_WIDTH_RANGE
        GL_LIST_BASE
        GL_LIST_BIT
        GL_LIST_INDEX
        GL_LIST_MODE
        GL_LOAD
        GL_LOGIC_OP
        GL_LOGIC_OP_MODE
        GL_LUMINANCE
        GL_LUMINANCE12
        GL_LUMINANCE12_ALPHA12
        GL_LUMINANCE12_ALPHA4
        GL_LUMINANCE16
        GL_LUMINANCE16_ALPHA16
        GL_LUMINANCE4
        GL_LUMINANCE4_ALPHA4
        GL_LUMINANCE6_ALPHA2
        GL_LUMINANCE8
        GL_LUMINANCE8_ALPHA8
        GL_LUMINANCE_ALPHA
        GL_MAP1_COLOR_4
        GL_MAP1_GRID_DOMAIN
        GL_MAP1_GRID_SEGMENTS
        GL_MAP1_INDEX
        GL_MAP1_NORMAL
        GL_MAP1_TEXTURE_COORD_1
        GL_MAP1_TEXTURE_COORD_2
        GL_MAP1_TEXTURE_COORD_3
        GL_MAP1_TEXTURE_COORD_4
        GL_MAP1_VERTEX_3
        GL_MAP1_VERTEX_4
        GL_MAP2_COLOR_4
        GL_MAP2_GRID_DOMAIN
        GL_MAP2_GRID_SEGMENTS
        GL_MAP2_INDEX
        GL_MAP2_NORMAL
        GL_MAP2_TEXTURE_COORD_1
        GL_MAP2_TEXTURE_COORD_2
        GL_MAP2_TEXTURE_COORD_3
        GL_MAP2_TEXTURE_COORD_4
        GL_MAP2_VERTEX_3
        GL_MAP2_VERTEX_4
        GL_MAP_COLOR
        GL_MAP_STENCIL
        GL_MATRIX0_ARB
        GL_MATRIX10_ARB
        GL_MATRIX11_ARB
        GL_MATRIX12_ARB
        GL_MATRIX13_ARB
        GL_MATRIX14_ARB
        GL_MATRIX15_ARB
        GL_MATRIX16_ARB
        GL_MATRIX17_ARB
        GL_MATRIX18_ARB
        GL_MATRIX19_ARB
        GL_MATRIX1_ARB
        GL_MATRIX20_ARB
        GL_MATRIX21_ARB
        GL_MATRIX22_ARB
        GL_MATRIX23_ARB
        GL_MATRIX24_ARB
        GL_MATRIX25_ARB
        GL_MATRIX26_ARB
        GL_MATRIX27_ARB
        GL_MATRIX28_ARB
        GL_MATRIX29_ARB
        GL_MATRIX2_ARB
        GL_MATRIX30_ARB
        GL_MATRIX31_ARB
        GL_MATRIX3_ARB
        GL_MATRIX4_ARB
        GL_MATRIX5_ARB
        GL_MATRIX6_ARB
        GL_MATRIX7_ARB
        GL_MATRIX8_ARB
        GL_MATRIX9_ARB
        GL_MATRIX_MODE
        GL_MAX_3D_TEXTURE_SIZE
        GL_MAX_ATTRIB_STACK_DEPTH
        GL_MAX_CLIENT_ATTRIB_STACK_DEPTH
        GL_MAX_CLIP_PLANES
        GL_MAX_COLOR_ATTACHMENTS_EXT
        GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS_ARB
        GL_MAX_CUBE_MAP_TEXTURE_SIZE
        GL_MAX_ELEMENTS_INDICES
        GL_MAX_ELEMENTS_VERTICES
        GL_MAX_EVAL_ORDER
        GL_MAX_FRAGMENT_UNIFORM_COMPONENTS_ARB
        GL_MAX_LIGHTS
        GL_MAX_LIST_NESTING
        GL_MAX_MODELVIEW_STACK_DEPTH
        GL_MAX_NAME_STACK_DEPTH
        GL_MAX_PIXEL_MAP_TABLE
        GL_MAX_PROGRAM_ADDRESS_REGISTERS_ARB
        GL_MAX_PROGRAM_ALU_INSTRUCTIONS_ARB
        GL_MAX_PROGRAM_ATTRIBS_ARB
        GL_MAX_PROGRAM_ENV_PARAMETERS_ARB
        GL_MAX_PROGRAM_INSTRUCTIONS_ARB
        GL_MAX_PROGRAM_LOCAL_PARAMETERS_ARB
        GL_MAX_PROGRAM_MATRICES_ARB
        GL_MAX_PROGRAM_MATRIX_STACK_DEPTH_ARB
        GL_MAX_PROGRAM_NATIVE_ADDRESS_REGISTERS_ARB
        GL_MAX_PROGRAM_NATIVE_ALU_INSTRUCTIONS_ARB
        GL_MAX_PROGRAM_NATIVE_ATTRIBS_ARB
        GL_MAX_PROGRAM_NATIVE_INSTRUCTIONS_ARB
        GL_MAX_PROGRAM_NATIVE_PARAMETERS_ARB
        GL_MAX_PROGRAM_NATIVE_TEMPORARIES_ARB
        GL_MAX_PROGRAM_NATIVE_TEX_INDIRECTIONS_ARB
        GL_MAX_PROGRAM_NATIVE_TEX_INSTRUCTIONS_ARB
        GL_MAX_PROGRAM_PARAMETERS_ARB
        GL_MAX_PROGRAM_TEMPORARIES_ARB
        GL_MAX_PROGRAM_TEX_INDIRECTIONS_ARB
        GL_MAX_PROGRAM_TEX_INSTRUCTIONS_ARB
        GL_MAX_PROJECTION_STACK_DEPTH
        GL_MAX_RENDERBUFFER_SIZE_EXT
        GL_MAX_TEXTURE_COORDS_ARB
        GL_MAX_TEXTURE_IMAGE_UNITS_ARB
        GL_MAX_TEXTURE_SIZE
        GL_MAX_TEXTURE_STACK_DEPTH
        GL_MAX_TEXTURE_UNITS
        GL_MAX_TEXTURE_UNITS_ARB
        GL_MAX_VARYING_FLOATS_ARB
        GL_MAX_VERTEX_ATTRIBS_ARB
        GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS_ARB
        GL_MAX_VERTEX_UNIFORM_COMPONENTS_ARB
        GL_MAX_VIEWPORT_DIMS
        GL_MODELVIEW
        GL_MODELVIEW_MATRIX
        GL_MODELVIEW_STACK_DEPTH
        GL_MODULATE
        GL_MULT
        GL_MULTISAMPLE
        GL_MULTISAMPLE_BIT
        GL_N3F_V3F
        GL_NAME_STACK_DEPTH
        GL_NAND
        GL_NEAREST
        GL_NEAREST_MIPMAP_LINEAR
        GL_NEAREST_MIPMAP_NEAREST
        GL_NEVER
        GL_NICEST
        GL_NONE
        GL_NOOP
        GL_NOR
        GL_NORMALIZE
        GL_NORMAL_ARRAY
        GL_NORMAL_ARRAY_BUFFER_BINDING_ARB
        GL_NORMAL_ARRAY_POINTER
        GL_NORMAL_ARRAY_STRIDE
        GL_NORMAL_ARRAY_TYPE
        GL_NORMAL_MAP
        GL_NOTEQUAL
        GL_NO_ERROR
        GL_NUM_COMPRESSED_TEXTURE_FORMATS
        GL_OBJECT_ACTIVE_ATTRIBUTES_ARB
        GL_OBJECT_ACTIVE_ATTRIBUTE_MAX_LENGTH_ARB
        GL_OBJECT_ACTIVE_UNIFORMS_ARB
        GL_OBJECT_ACTIVE_UNIFORM_MAX_LENGTH_ARB
        GL_OBJECT_ATTACHED_OBJECTS_ARB
        GL_OBJECT_COMPILE_STATUS_ARB
        GL_OBJECT_DELETE_STATUS_ARB
        GL_OBJECT_INFO_LOG_LENGTH_ARB
        GL_OBJECT_LINEAR
        GL_OBJECT_LINK_STATUS_ARB
        GL_OBJECT_PLANE
        GL_OBJECT_SHADER_SOURCE_LENGTH_ARB
        GL_OBJECT_SUBTYPE_ARB
        GL_OBJECT_TYPE_ARB
        GL_OBJECT_VALIDATE_STATUS_ARB
        GL_ONE
        GL_ONE_MINUS_DST_ALPHA
        GL_ONE_MINUS_DST_COLOR
        GL_ONE_MINUS_SRC_ALPHA
        GL_ONE_MINUS_SRC_COLOR
        GL_OPERAND0_ALPHA
        GL_OPERAND0_ALPHA_ARB
        GL_OPERAND0_RGB
        GL_OPERAND0_RGB_ARB
        GL_OPERAND1_ALPHA
        GL_OPERAND1_ALPHA_ARB
        GL_OPERAND1_RGB
        GL_OPERAND1_RGB_ARB
        GL_OPERAND2_ALPHA
        GL_OPERAND2_ALPHA_ARB
        GL_OPERAND2_RGB
        GL_OPERAND2_RGB_ARB
        GL_OR
        GL_ORDER
        GL_OR_INVERTED
        GL_OR_REVERSE
        GL_OUT_OF_MEMORY
        GL_PACK_ALIGNMENT
        GL_PACK_IMAGE_HEIGHT
        GL_PACK_LSB_FIRST
        GL_PACK_ROW_LENGTH
        GL_PACK_SKIP_IMAGES
        GL_PACK_SKIP_PIXELS
        GL_PACK_SKIP_ROWS
        GL_PACK_SWAP_BYTES
        GL_PASS_THROUGH_TOKEN
        GL_PERSPECTIVE_CORRECTION_HINT
        GL_PIXEL_MAP_A_TO_A
        GL_PIXEL_MAP_A_TO_A_SIZE
        GL_PIXEL_MAP_B_TO_B
        GL_PIXEL_MAP_B_TO_B_SIZE
        GL_PIXEL_MAP_G_TO_G
        GL_PIXEL_MAP_G_TO_G_SIZE
        GL_PIXEL_MAP_I_TO_A
        GL_PIXEL_MAP_I_TO_A_SIZE
        GL_PIXEL_MAP_I_TO_B
        GL_PIXEL_MAP_I_TO_B_SIZE
        GL_PIXEL_MAP_I_TO_G
        GL_PIXEL_MAP_I_TO_G_SIZE
        GL_PIXEL_MAP_I_TO_I
        GL_PIXEL_MAP_I_TO_I_SIZE
        GL_PIXEL_MAP_I_TO_R
        GL_PIXEL_MAP_I_TO_R_SIZE
        GL_PIXEL_MAP_R_TO_R
        GL_PIXEL_MAP_R_TO_R_SIZE
        GL_PIXEL_MAP_S_TO_S
        GL_PIXEL_MAP_S_TO_S_SIZE
        GL_PIXEL_MODE_BIT
        GL_POINT
        GL_POINTS
        GL_POINT_BIT
        GL_POINT_SIZE
        GL_POINT_SIZE_GRANULARITY
        GL_POINT_SIZE_RANGE
        GL_POINT_SMOOTH
        GL_POINT_SMOOTH_HINT
        GL_POINT_TOKEN
        GL_POLYGON
        GL_POLYGON_BIT
        GL_POLYGON_MODE
        GL_POLYGON_OFFSET_FACTOR
        GL_POLYGON_OFFSET_FILL
        GL_POLYGON_OFFSET_LINE
        GL_POLYGON_OFFSET_POINT
        GL_POLYGON_OFFSET_UNITS
        GL_POLYGON_SMOOTH
        GL_POLYGON_SMOOTH_HINT
        GL_POLYGON_STIPPLE
        GL_POLYGON_STIPPLE_BIT
        GL_POLYGON_TOKEN
        GL_POSITION
        GL_PREVIOUS
        GL_PREVIOUS_ARB
        GL_PRIMARY_COLOR
        GL_PRIMARY_COLOR_ARB
        GL_PROGRAM_ADDRESS_REGISTERS_ARB
        GL_PROGRAM_ALU_INSTRUCTIONS_ARB
        GL_PROGRAM_ATTRIBS_ARB
        GL_PROGRAM_BINDING_ARB
        GL_PROGRAM_ERROR_POSITION_ARB
        GL_PROGRAM_ERROR_STRING_ARB
        GL_PROGRAM_FORMAT_ARB
        GL_PROGRAM_FORMAT_ASCII_ARB
        GL_PROGRAM_INSTRUCTIONS_ARB
        GL_PROGRAM_LENGTH_ARB
        GL_PROGRAM_NATIVE_ADDRESS_REGISTERS_ARB
        GL_PROGRAM_NATIVE_ALU_INSTRUCTIONS_ARB
        GL_PROGRAM_NATIVE_ATTRIBS_ARB
        GL_PROGRAM_NATIVE_INSTRUCTIONS_ARB
        GL_PROGRAM_NATIVE_PARAMETERS_ARB
        GL_PROGRAM_NATIVE_TEMPORARIES_ARB
        GL_PROGRAM_NATIVE_TEX_INDIRECTIONS_ARB
        GL_PROGRAM_NATIVE_TEX_INSTRUCTIONS_ARB
        GL_PROGRAM_OBJECT_ARB
        GL_PROGRAM_PARAMETERS_ARB
        GL_PROGRAM_STRING_ARB
        GL_PROGRAM_TEMPORARIES_ARB
        GL_PROGRAM_TEX_INDIRECTIONS_ARB
        GL_PROGRAM_TEX_INSTRUCTIONS_ARB
        GL_PROGRAM_UNDER_NATIVE_LIMITS_ARB
        GL_PROJECTION
        GL_PROJECTION_MATRIX
        GL_PROJECTION_STACK_DEPTH
        GL_PROXY_TEXTURE_1D
        GL_PROXY_TEXTURE_2D
        GL_PROXY_TEXTURE_3D
        GL_PROXY_TEXTURE_CUBE_MAP
        GL_Q
        GL_QUADRATIC_ATTENUATION
        GL_QUADS
        GL_QUAD_STRIP
        GL_R
        GL_R3_G3_B2
        GL_READ_BUFFER
        GL_READ_ONLY_ARB
        GL_READ_WRITE_ARB
        GL_RED
        GL_RED_BIAS
        GL_RED_BITS
        GL_RED_SCALE
        GL_REFLECTION_MAP
        GL_RENDER
        GL_RENDERBUFFER_ALPHA_SIZE_EXT
        GL_RENDERBUFFER_BINDING_EXT
        GL_RENDERBUFFER_BLUE_SIZE_EXT
        GL_RENDERBUFFER_DEPTH_SIZE_EXT
        GL_RENDERBUFFER_EXT
        GL_RENDERBUFFER_GREEN_SIZE_EXT
        GL_RENDERBUFFER_HEIGHT_EXT
        GL_RENDERBUFFER_INTERNAL_FORMAT_EXT
        GL_RENDERBUFFER_RED_SIZE_EXT
        GL_RENDERBUFFER_STENCIL_SIZE_EXT
        GL_RENDERBUFFER_WIDTH_EXT
        GL_RENDERER
        GL_RENDER_MODE
        GL_REPEAT
        GL_REPLACE
        GL_RESCALE_NORMAL
        GL_RETURN
        GL_RGB
        GL_RGB10
        GL_RGB10_A2
        GL_RGB12
        GL_RGB16
        GL_RGB4
        GL_RGB5
        GL_RGB5_A1
        GL_RGB8
        GL_RGBA
        GL_RGBA12
        GL_RGBA16
        GL_RGBA2
        GL_RGBA4
        GL_RGBA8
        GL_RGBA_MODE
        GL_RGB_SCALE
        GL_RGB_SCALE_ARB
        GL_RIGHT
        GL_S
        GL_SAMPLER_1D_ARB
        GL_SAMPLER_1D_SHADOW_ARB
        GL_SAMPLER_2D_ARB
        GL_SAMPLER_2D_RECT_ARB
        GL_SAMPLER_2D_RECT_SHADOW_ARB
        GL_SAMPLER_2D_SHADOW_ARB
        GL_SAMPLER_3D_ARB
        GL_SAMPLER_CUBE_ARB
        GL_SAMPLES
        GL_SAMPLE_ALPHA_TO_COVERAGE
        GL_SAMPLE_ALPHA_TO_ONE
        GL_SAMPLE_BUFFERS
        GL_SAMPLE_COVERAGE
        GL_SAMPLE_COVERAGE_INVERT
        GL_SAMPLE_COVERAGE_VALUE
        GL_SCISSOR_BIT
        GL_SCISSOR_BOX
        GL_SCISSOR_TEST
        GL_SECONDARY_COLOR_ARRAY_BUFFER_BINDING_ARB
        GL_SELECT
        GL_SELECTION_BUFFER_POINTER
        GL_SELECTION_BUFFER_SIZE
        GL_SEPARATE_SPECULAR_COLOR
        GL_SET
        GL_SHADER_OBJECT_ARB
        GL_SHADE_MODEL
        GL_SHADING_LANGUAGE_VERSION_ARB
        GL_SHININESS
        GL_SHORT
        GL_SINGLE_COLOR
        GL_SMOOTH
        GL_SMOOTH_LINE_WIDTH_GRANULARITY
        GL_SMOOTH_LINE_WIDTH_RANGE
        GL_SMOOTH_POINT_SIZE_GRANULARITY
        GL_SMOOTH_POINT_SIZE_RANGE
        GL_SOURCE0_ALPHA
        GL_SOURCE0_ALPHA_ARB
        GL_SOURCE0_RGB
        GL_SOURCE0_RGB_ARB
        GL_SOURCE1_ALPHA
        GL_SOURCE1_ALPHA_ARB
        GL_SOURCE1_RGB
        GL_SOURCE1_RGB_ARB
        GL_SOURCE2_ALPHA
        GL_SOURCE2_ALPHA_ARB
        GL_SOURCE2_RGB
        GL_SOURCE2_RGB_ARB
        GL_SPECULAR
        GL_SPHERE_MAP
        GL_SPOT_CUTOFF
        GL_SPOT_DIRECTION
        GL_SPOT_EXPONENT
        GL_SRC_ALPHA
        GL_SRC_ALPHA_SATURATE
        GL_SRC_COLOR
        GL_STACK_OVERFLOW
        GL_STACK_UNDERFLOW
        GL_STATIC_COPY_ARB
        GL_STATIC_DRAW_ARB
        GL_STATIC_READ_ARB
        GL_STENCIL
        GL_STENCIL_ATTACHMENT_EXT
        GL_STENCIL_BITS
        GL_STENCIL_BUFFER_BIT
        GL_STENCIL_CLEAR_VALUE
        GL_STENCIL_FAIL
        GL_STENCIL_FUNC
        GL_STENCIL_INDEX
        GL_STENCIL_INDEX16_EXT
        GL_STENCIL_INDEX1_EXT
        GL_STENCIL_INDEX4_EXT
        GL_STENCIL_INDEX8_EXT
        GL_STENCIL_PASS_DEPTH_FAIL
        GL_STENCIL_PASS_DEPTH_PASS
        GL_STENCIL_REF
        GL_STENCIL_TEST
        GL_STENCIL_VALUE_MASK
        GL_STENCIL_WRITEMASK
        GL_STEREO
        GL_STREAM_COPY_ARB
        GL_STREAM_DRAW_ARB
        GL_STREAM_READ_ARB
        GL_SUBPIXEL_BITS
        GL_SUBTRACT
        GL_SUBTRACT_ARB
        GL_T
        GL_T2F_C3F_V3F
        GL_T2F_C4F_N3F_V3F
        GL_T2F_C4UB_V3F
        GL_T2F_N3F_V3F
        GL_T2F_V3F
        GL_T4F_C4F_N3F_V4F
        GL_T4F_V4F
        GL_TEXTURE
        GL_TEXTURE0
        GL_TEXTURE0_ARB
        GL_TEXTURE1
        GL_TEXTURE10
        GL_TEXTURE10_ARB
        GL_TEXTURE11
        GL_TEXTURE11_ARB
        GL_TEXTURE12
        GL_TEXTURE12_ARB
        GL_TEXTURE13
        GL_TEXTURE13_ARB
        GL_TEXTURE14
        GL_TEXTURE14_ARB
        GL_TEXTURE15
        GL_TEXTURE15_ARB
        GL_TEXTURE16
        GL_TEXTURE16_ARB
        GL_TEXTURE17
        GL_TEXTURE17_ARB
        GL_TEXTURE18
        GL_TEXTURE18_ARB
        GL_TEXTURE19
        GL_TEXTURE19_ARB
        GL_TEXTURE1_ARB
        GL_TEXTURE2
        GL_TEXTURE20
        GL_TEXTURE20_ARB
        GL_TEXTURE21
        GL_TEXTURE21_ARB
        GL_TEXTURE22
        GL_TEXTURE22_ARB
        GL_TEXTURE23
        GL_TEXTURE23_ARB
        GL_TEXTURE24
        GL_TEXTURE24_ARB
        GL_TEXTURE25
        GL_TEXTURE25_ARB
        GL_TEXTURE26
        GL_TEXTURE26_ARB
        GL_TEXTURE27
        GL_TEXTURE27_ARB
        GL_TEXTURE28
        GL_TEXTURE28_ARB
        GL_TEXTURE29
        GL_TEXTURE29_ARB
        GL_TEXTURE2_ARB
        GL_TEXTURE3
        GL_TEXTURE30
        GL_TEXTURE30_ARB
        GL_TEXTURE31
        GL_TEXTURE31_ARB
        GL_TEXTURE3_ARB
        GL_TEXTURE4
        GL_TEXTURE4_ARB
        GL_TEXTURE5
        GL_TEXTURE5_ARB
        GL_TEXTURE6
        GL_TEXTURE6_ARB
        GL_TEXTURE7
        GL_TEXTURE7_ARB
        GL_TEXTURE8
        GL_TEXTURE8_ARB
        GL_TEXTURE9
        GL_TEXTURE9_ARB
        GL_TEXTURE_1D
        GL_TEXTURE_2D
        GL_TEXTURE_3D
        GL_TEXTURE_ALPHA_SIZE
        GL_TEXTURE_BASE_LEVEL
        GL_TEXTURE_BINDING_1D
        GL_TEXTURE_BINDING_2D
        GL_TEXTURE_BINDING_3D
        GL_TEXTURE_BINDING_CUBE_MAP
        GL_TEXTURE_BIT
        GL_TEXTURE_BLUE_SIZE
        GL_TEXTURE_BORDER
        GL_TEXTURE_BORDER_COLOR
        GL_TEXTURE_COMPONENTS
        GL_TEXTURE_COMPRESSED
        GL_TEXTURE_COMPRESSED_IMAGE_SIZE
        GL_TEXTURE_COMPRESSION_HINT
        GL_TEXTURE_COORD_ARRAY
        GL_TEXTURE_COORD_ARRAY_BUFFER_BINDING_ARB
        GL_TEXTURE_COORD_ARRAY_POINTER
        GL_TEXTURE_COORD_ARRAY_SIZE
        GL_TEXTURE_COORD_ARRAY_STRIDE
        GL_TEXTURE_COORD_ARRAY_TYPE
        GL_TEXTURE_CUBE_MAP
        GL_TEXTURE_CUBE_MAP_NEGATIVE_X
        GL_TEXTURE_CUBE_MAP_NEGATIVE_Y
        GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
        GL_TEXTURE_CUBE_MAP_POSITIVE_X
        GL_TEXTURE_CUBE_MAP_POSITIVE_Y
        GL_TEXTURE_CUBE_MAP_POSITIVE_Z
        GL_TEXTURE_DEPTH
        GL_TEXTURE_ENV
        GL_TEXTURE_ENV_COLOR
        GL_TEXTURE_ENV_MODE
        GL_TEXTURE_GEN_MODE
        GL_TEXTURE_GEN_Q
        GL_TEXTURE_GEN_R
        GL_TEXTURE_GEN_S
        GL_TEXTURE_GEN_T
        GL_TEXTURE_GREEN_SIZE
        GL_TEXTURE_HEIGHT
        GL_TEXTURE_INTENSITY_SIZE
        GL_TEXTURE_INTERNAL_FORMAT
        GL_TEXTURE_LUMINANCE_SIZE
        GL_TEXTURE_MAG_FILTER
        GL_TEXTURE_MATRIX
        GL_TEXTURE_MAX_LEVEL
        GL_TEXTURE_MAX_LOD
        GL_TEXTURE_MIN_FILTER
        GL_TEXTURE_MIN_LOD
        GL_TEXTURE_PRIORITY
        GL_TEXTURE_RED_SIZE
        GL_TEXTURE_RESIDENT
        GL_TEXTURE_STACK_DEPTH
        GL_TEXTURE_WIDTH
        GL_TEXTURE_WRAP_R
        GL_TEXTURE_WRAP_S
        GL_TEXTURE_WRAP_T
        GL_TRANSFORM_BIT
        GL_TRANSPOSE_COLOR_MATRIX
        GL_TRANSPOSE_CURRENT_MATRIX_ARB
        GL_TRANSPOSE_MODELVIEW_MATRIX
        GL_TRANSPOSE_PROJECTION_MATRIX
        GL_TRANSPOSE_TEXTURE_MATRIX
        GL_TRIANGLES
        GL_TRIANGLE_FAN
        GL_TRIANGLE_STRIP
        GL_TRUE
        GL_UNPACK_ALIGNMENT
        GL_UNPACK_IMAGE_HEIGHT
        GL_UNPACK_LSB_FIRST
        GL_UNPACK_ROW_LENGTH
        GL_UNPACK_SKIP_IMAGES
        GL_UNPACK_SKIP_PIXELS
        GL_UNPACK_SKIP_ROWS
        GL_UNPACK_SWAP_BYTES
        GL_UNSIGNED_BYTE
        GL_UNSIGNED_BYTE_2_3_3_REV
        GL_UNSIGNED_BYTE_3_3_2
        GL_UNSIGNED_INT
        GL_UNSIGNED_INT_10_10_10_2
        GL_UNSIGNED_INT_2_10_10_10_REV
        GL_UNSIGNED_INT_8_8_8_8
        GL_UNSIGNED_INT_8_8_8_8_REV
        GL_UNSIGNED_SHORT
        GL_UNSIGNED_SHORT_1_5_5_5_REV
        GL_UNSIGNED_SHORT_4_4_4_4
        GL_UNSIGNED_SHORT_4_4_4_4_REV
        GL_UNSIGNED_SHORT_5_5_5_1
        GL_UNSIGNED_SHORT_5_6_5
        GL_UNSIGNED_SHORT_5_6_5_REV
        GL_V2F
        GL_V3F
        GL_VENDOR
        GL_VERSION
        GL_VERTEX_ARRAY
        GL_VERTEX_ARRAY_BUFFER_BINDING_ARB
        GL_VERTEX_ARRAY_POINTER
        GL_VERTEX_ARRAY_SIZE
        GL_VERTEX_ARRAY_STRIDE
        GL_VERTEX_ARRAY_TYPE
        GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING_ARB
        GL_VERTEX_ATTRIB_ARRAY_ENABLED_ARB
        GL_VERTEX_ATTRIB_ARRAY_NORMALIZED_ARB
        GL_VERTEX_ATTRIB_ARRAY_POINTER_ARB
        GL_VERTEX_ATTRIB_ARRAY_SIZE_ARB
        GL_VERTEX_ATTRIB_ARRAY_STRIDE_ARB
        GL_VERTEX_ATTRIB_ARRAY_TYPE_ARB
        GL_VERTEX_PROGRAM_ARB
        GL_VERTEX_PROGRAM_POINT_SIZE_ARB
        GL_VERTEX_PROGRAM_TWO_SIDE_ARB
        GL_VERTEX_SHADER_ARB
        GL_VIEWPORT
        GL_VIEWPORT_BIT
        GL_WEIGHT_ARRAY_BUFFER_BINDING_ARB
        GL_WRITE_ONLY_ARB
        GL_XOR
        GL_ZERO
        GL_ZOOM_X
        GL_ZOOM_Y
        RENPY_THIRD_TEXTURE


cdef inline gl_check(where):
    cdef GLenum error
    error = glGetError()
    if error:
        import renpy
        renpy.display.log.write("GL error 0x%X at %s", error, where)
