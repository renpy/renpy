#ifndef RENPY_MACOS_VIDEO_H
#define RENPY_MACOS_VIDEO_H

#include <stdint.h>

#ifdef __APPLE__
#include <OpenGL/gltypes.h>
#else
typedef unsigned int GLuint;
#endif

/* Extracts the IOSurface and NV12 dimensions from an AV_PIX_FMT_VIDEOTOOLBOX
 * AVFrame. The AVFrame remains owned by the caller. */
int renpy_macos_video_frame_info(void *frame, void **iosurface, int *width, int *height, int *full_range, int *bt709);

/* Imports one IOSurface plane into the current legacy OpenGL texture. */
int renpy_macos_video_import_texture(void *context, GLuint texture, int width, int height, void *iosurface, int plane);

#endif
