#include "renpy_macos_video.h"

#ifdef __APPLE__

#include <CoreVideo/CoreVideo.h>
#include <OpenGL/CGLCurrent.h>
#include <OpenGL/CGLIOSurface.h>
#include <OpenGL/gl.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>

#include <libavutil/frame.h>
#include <libavutil/pixfmt.h>

static void renpy_video_debug(const char *format, ...) {
    va_list args;
    FILE *file;

    if (!getenv("RENPY_DEBUG_VIDEO")) {
        return;
    }

    file = fopen("/tmp/renpy-video-import.log", "a");
    if (!file) {
        return;
    }

    va_start(args, format);
    vfprintf(file, format, args);
    va_end(args);
    fclose(file);
}

int renpy_macos_video_frame_info(void *frame_ptr, void **iosurface, int *width, int *height, int *full_range, int *bt709) {
	AVFrame *frame = (AVFrame *) frame_ptr;
	CVPixelBufferRef pixel_buffer;
	IOSurfaceRef surface;
	OSType pixel_format;

    if (!frame || frame->format != AV_PIX_FMT_VIDEOTOOLBOX || !frame->data[3]) {
        renpy_video_debug("frame info invalid\\n");
        return -1;
    }

    pixel_buffer = (CVPixelBufferRef) frame->data[3];
    surface = CVPixelBufferGetIOSurface(pixel_buffer);
    if (!surface) {
        renpy_video_debug("frame has no IOSurface\\n");
        return -2;
    }

	pixel_format = CVPixelBufferGetPixelFormatType(pixel_buffer);
	if (pixel_format != kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange &&
		pixel_format != kCVPixelFormatType_420YpCbCr8BiPlanarFullRange) {
		renpy_video_debug("unsupported pixel format: %u\\n", (unsigned) pixel_format);
		return -3;
	}

    *iosurface = (void *) surface;
	*width = (int) CVPixelBufferGetWidth(pixel_buffer);
	*height = (int) CVPixelBufferGetHeight(pixel_buffer);
	*full_range = pixel_format == kCVPixelFormatType_420YpCbCr8BiPlanarFullRange;
	*bt709 = frame->colorspace == AVCOL_SPC_BT709;
	return 0;
}

int renpy_macos_video_import_texture(void *context_ptr, GLuint texture, int width, int height, void *iosurface_ptr, int plane) {
    CGLContextObj context = CGLGetCurrentContext();
    IOSurfaceRef surface = (IOSurfaceRef) iosurface_ptr;
    GLenum format = plane ? GL_LUMINANCE_ALPHA : GL_LUMINANCE;
    CGLError error;

    (void) context_ptr;

    if (!context || !surface || width <= 0 || height <= 0 || (plane != 0 && plane != 1)) {
        return -1;
    }

    glBindTexture(GL_TEXTURE_RECTANGLE_ARB, texture);
    glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

    error = CGLTexImageIOSurface2D(
        context,
        GL_TEXTURE_RECTANGLE_ARB,
        format,
        width,
        height,
        format,
        GL_UNSIGNED_BYTE,
        surface,
        (GLuint) plane);

    if (error != kCGLNoError) {
        renpy_video_debug("IOSurface import failed: plane=%d error=%d width=%d height=%d\\n", plane, (int) error, width, height);
    }

    return error == kCGLNoError ? 0 : (int) error;
}

#else

int renpy_macos_video_frame_info(void *frame, void **iosurface, int *width, int *height, int *full_range, int *bt709) {
	(void) frame;
	(void) iosurface;
	(void) width;
	(void) height;
	(void) full_range;
	(void) bt709;
    return -1;
}

int renpy_macos_video_import_texture(void *context, GLuint texture, int width, int height, void *iosurface, int plane) {
    (void) context;
    (void) texture;
    (void) width;
    (void) height;
    (void) iosurface;
    (void) plane;
    return -1;
}

#endif
