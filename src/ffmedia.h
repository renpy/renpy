/*
 * Shared declarations for Ren'Py's FFmpeg media backend.
 */

#ifndef RENPY_FFMEDIA_H
#define RENPY_FFMEDIA_H

#include <stdint.h>

typedef struct MediaState MediaState;

typedef struct RPSVideoStats {
    const char *state;
    const char *decoder_backend;
    const char *decoder_name;
    const char *codec_name;
    const char *input_pixel_format;
    const char *surface_backend;
    const char *output_pixel_format;
    const char *transfer_pixel_format;
    const char *hardware_status;
    int hardware_decode;
    int hardware_surface;
    int hardware_attempted;
    int hardware_available;
    int width;
    int height;
    int queue_depth;
    uint64_t decoded_frames;
    uint64_t converted_frames;
    uint64_t submitted_frames;
    uint64_t dropped_frames;
    uint64_t decode_time_ns;
    uint64_t hardware_transfer_frames;
    uint64_t hardware_transfer_time_ns;
    uint64_t hardware_transfer_failures;
    uint64_t color_convert_time_ns;
    uint64_t present_lateness_ns;
    uint64_t present_lateness_max_ns;
    double last_pts;
} RPSVideoStats;

void media_video_stats(MediaState *ms, RPSVideoStats *stats);

/* Returns a retained AVFrame-backed hardware surface, or NULL when the next
 * frame is not a VideoToolbox surface. The caller owns the returned frame. */
void *media_read_video_hardware(MediaState *ms);
void media_video_frame_free(void *frame);

#endif
