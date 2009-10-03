/*
 * FFplay : Simple Media Player based on the ffmpeg libraries
 * Copyright (c) 2003 Fabrice Bellard
 *
 * This file is part of FFmpeg.
 *
 * FFmpeg is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * FFmpeg is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with FFmpeg; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */

#include <pygame/pygame.h>
#include <math.h>
#include <limits.h>
#include <libavutil/avstring.h>
#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
// #include "libavdevice/avdevice.h"
#include <libswscale/swscale.h>
// #include "libavcodec/audioconvert.h"
// #include "libavcodec/opt.h"

// #include "cmdutils.h"

#include <SDL.h>
#include <SDL_thread.h>

#ifdef __MINGW32__
#undef main /* We don't want SDL to override our main() */
#endif

#undef exit

// #define DEBUG_SYNC

#define MAX_VIDEOQ_SIZE (5 * 256 * 1024)
#define MAX_AUDIOQ_SIZE (5 * 16 * 1024)
#define MAX_SUBTITLEQ_SIZE (5 * 16 * 1024)

/* SDL audio buffer size, in samples. Should be small to have precise
   A/V sync as SDL does not have hardware buffer fullness info. */
#define SDL_AUDIO_BUFFER_SIZE 2048

/* no AV sync correction is done if below the AV sync threshold */
#define AV_SYNC_THRESHOLD 0.01
/* no AV correction is done if too big error */
#define AV_NOSYNC_THRESHOLD 10.0

/* maximum audio speed change to get correct sync */
#define SAMPLE_CORRECTION_PERCENT_MAX 10

/* we use about AUDIO_DIFF_AVG_NB A-V differences to make the average */
#define AUDIO_DIFF_AVG_NB   20

/* NOTE: the size must be big enough to compensate the hardware audio buffersize size */
#define SAMPLE_ARRAY_SIZE (2*65536)

AVCodecContext *avctx_opts[CODEC_TYPE_NB];
AVFormatContext *avformat_opts;

static int sws_flags = 1;

typedef struct PacketQueue {
    AVPacketList *first_pkt, *last_pkt;
    int nb_packets;
    int size;
    int abort_request;
    int end_request;
    SDL_mutex *mutex;
    SDL_cond *cond;
} PacketQueue;

#define VIDEO_PICTURE_QUEUE_SIZE 1
#define SUBPICTURE_QUEUE_SIZE 4

typedef struct VideoPicture {
    double pts;                                  ///<presentation time stamp for this picture
    SDL_Overlay *bmp;
    int width, height; /* source height & width */
    int allocated;
} VideoPicture;

typedef struct SubPicture {
    double pts; /* presentation time stamp for this picture */
    AVSubtitle sub;
} SubPicture;

enum {
    AV_SYNC_AUDIO_MASTER, /* default choice */
    AV_SYNC_VIDEO_MASTER,
    AV_SYNC_EXTERNAL_CLOCK, /* synchronize to an external clock */
};

typedef struct VideoState {
    SDL_Thread *parse_tid;
    SDL_Thread *video_tid;
    AVInputFormat *iformat;
    int no_background;
    int abort_request;
    int paused;
    int last_paused;
    int seek_req;
    int seek_flags;
    int64_t seek_pos;
    AVFormatContext *ic;
    int dtg_active_format;

    int audio_stream;

    int av_sync_type;
    double external_clock; /* external clock base */
    int64_t external_clock_time;

    double audio_clock;
    double audio_diff_cum; /* used for AV difference average computation */
    double audio_diff_avg_coef;
    double audio_diff_threshold;
    int audio_diff_avg_count;
    AVStream *audio_st;
    PacketQueue audioq;
    int audio_hw_buf_size;
    /* samples output by the codec. we reserve more space for avsync
       compensation */

    uint8_t audio_buf1[(AVCODEC_MAX_AUDIO_FRAME_SIZE * 3) / 2] __attribute__ ((aligned (16))) ;
    uint8_t audio_buf2[(AVCODEC_MAX_AUDIO_FRAME_SIZE * 3) / 2] __attribute__ ((aligned (16))) ;

    uint8_t *audio_buf;
    unsigned int audio_buf_size; /* in bytes */
    int audio_buf_index; /* in bytes */
    AVPacket audio_pkt;
    uint8_t *audio_pkt_data;
    int audio_pkt_size;

    // AVAudioConvert *reformat_ctx;
    ReSampleContext *reformat_ctx;
    int resample_frac;
    
    int show_audio; /* if true, display audio samples */
    int16_t sample_array[SAMPLE_ARRAY_SIZE];
    int sample_array_index;
    int last_i_start;

    SDL_Thread *subtitle_tid;
    int subtitle_stream;
    int subtitle_stream_changed;
    AVStream *subtitle_st;
    PacketQueue subtitleq;
    SubPicture subpq[SUBPICTURE_QUEUE_SIZE];
    int subpq_size, subpq_rindex, subpq_windex;
    SDL_mutex *subpq_mutex;
    SDL_cond *subpq_cond;

    double frame_timer;
    double frame_last_pts;
    double frame_last_delay;
    double video_clock;                          ///<pts of last decoded frame / predicted pts of next decoded frame
    int video_stream;
    AVStream *video_st;
    PacketQueue videoq;
    double video_current_pts;                    ///<current displayed pts (different from video_clock if frame fifos are used)
    int64_t video_current_pts_time;              ///<time (av_gettime) at which we updated video_current_pts - used to have running video pts
    VideoPicture pictq[VIDEO_PICTURE_QUEUE_SIZE];
    int pictq_size, pictq_rindex, pictq_windex;
    SDL_mutex *pictq_mutex;
    SDL_cond *pictq_cond;

    
    // These are used to notify the parse thread when it's time to die.
    SDL_mutex *quit_mutex;
    SDL_cond *quit_cond;

    //    QETimer *video_timer;
    SDL_RWops *rwops;
    ByteIOContext *io_context;
    
    int width, height, xleft, ytop;

    int64_t audio_callback_time;

    char *filename;

    // Have we initialized fully?
    int started;

    // Have we finished decoding?
    int finished;

    // Do we need to have a picture allocated?
    int needs_alloc;

    // The audio duration.
    unsigned int audio_duration;

    // The amount of audio we've played, in samples.
    unsigned int audio_played;
    
} VideoState;

SDL_mutex *codec_mutex = NULL;

static int audio_write_get_buf_size(VideoState *is);

/* options specified by the user */
static int frame_width = 0;
static int frame_height = 0;
static enum PixelFormat frame_pix_fmt = PIX_FMT_NONE;
static int seek_by_bytes;
static int show_status;
static int av_sync_type = AV_SYNC_AUDIO_MASTER;
static int64_t start_time = AV_NOPTS_VALUE;
static int debug = 0;
static int debug_mv = 0;
static int thread_count = 1;
static int workaround_bugs = 1;
static int fast = 0;
static int genpts = 0;
static int lowres = 0;
static int idct = FF_IDCT_AUTO;
static enum AVDiscard skip_frame= AVDISCARD_DEFAULT;
static enum AVDiscard skip_idct= AVDISCARD_DEFAULT;
static enum AVDiscard skip_loop_filter= AVDISCARD_DEFAULT;
static int error_recognition = FF_ER_CAREFUL;
static int error_concealment = 3;
static int decoder_reorder_pts= 0;

static AVPacket flush_pkt;

#define FF_ALLOC_EVENT   (SDL_USEREVENT)
#define FF_REFRESH_EVENT (SDL_USEREVENT + 1)
// #define FF_QUIT_EVENT    (SDL_USEREVENT + 2)

// The rate that audio will be resampled to.
static int audio_sample_rate;

/* ByteIOContext <-> SDL_RWops mapping. */
static int rwops_read(void *opaque, uint8_t *buf, int buf_size) {
    SDL_RWops *rw = (SDL_RWops *) opaque;    

    int rv = rw->read(rw, buf, 1, buf_size);
    return rv;

}

static int rwops_write(void *opaque, uint8_t *buf, int buf_size) {
    /* SDL_RWops *rw = (SDL_RWops *) opaque; */
    /* return rw->write(rw, buf, 1, buf_size); */
    printf("Writing to an SDL_rwops is a really bad idea.\n");
    return -1;
}

static int64_t rwops_seek(void *opaque, int64_t offset, int whence) {
    SDL_RWops *rw = (SDL_RWops *) opaque;

    if (whence == 65536) {
        return -1;
    }

    int64_t rv = rw->seek(rw, (int) offset, whence);
    return rv;
}

#define RWOPS_BUFFER 65536

static ByteIOContext *rwops_open(SDL_RWops *rw) {

    unsigned char *buffer = av_malloc(RWOPS_BUFFER);
    ByteIOContext *rv = av_alloc_put_byte(
        buffer,
        RWOPS_BUFFER,
        0,
        rw,
        rwops_read,
        rwops_write,
        rwops_seek);

    return rv;    
}

static void rwops_close(SDL_RWops *rw) {
    rw->close(rw);
}


/* packet queue handling */
static void packet_queue_init(PacketQueue *q)
{
    memset(q, 0, sizeof(PacketQueue));
    q->mutex = SDL_CreateMutex();
    q->cond = SDL_CreateCond();
}

static void packet_queue_flush(PacketQueue *q)
{
    AVPacketList *pkt, *pkt1;

    SDL_LockMutex(q->mutex);
    for(pkt = q->first_pkt; pkt != NULL; pkt = pkt1) {
        pkt1 = pkt->next;
        av_free_packet(&pkt->pkt);
        av_freep(&pkt);
    }
    q->last_pkt = NULL;
    q->first_pkt = NULL;
    q->nb_packets = 0;
    q->size = 0;
    SDL_UnlockMutex(q->mutex);
}

static void packet_queue_end(PacketQueue *q)
{
    packet_queue_flush(q);
    SDL_DestroyMutex(q->mutex);
    SDL_DestroyCond(q->cond);
}

static int packet_queue_put(PacketQueue *q, AVPacket *pkt)
{
    AVPacketList *pkt1;

    /* duplicate the packet */
    if (pkt!=&flush_pkt && av_dup_packet(pkt) < 0)
        return -1;

    pkt1 = av_malloc(sizeof(AVPacketList));
    if (!pkt1)
        return -1;
    pkt1->pkt = *pkt;
    pkt1->next = NULL;


    SDL_LockMutex(q->mutex);

    if (!q->last_pkt)

        q->first_pkt = pkt1;
    else
        q->last_pkt->next = pkt1;
    q->last_pkt = pkt1;
    q->nb_packets++;
    q->size += pkt1->pkt.size + sizeof(*pkt1);
    /* XXX: should duplicate packet data in DV case */
    SDL_CondSignal(q->cond);

    SDL_UnlockMutex(q->mutex);
    return 0;
}

static void packet_queue_abort(PacketQueue *q)
{
    SDL_LockMutex(q->mutex);

    q->abort_request = 1;

    SDL_CondSignal(q->cond);

    SDL_UnlockMutex(q->mutex);
}

/* return < 0 if aborted, 0 if no packet and > 0 if packet.  */
static int packet_queue_get(PacketQueue *q, AVPacket *pkt, int block)
{
    AVPacketList *pkt1;
    int ret;

    SDL_LockMutex(q->mutex);

    for(;;) {
        if (q->abort_request) {
            ret = -1;
            break;
        }

        pkt1 = q->first_pkt;
        if (pkt1) {
            q->first_pkt = pkt1->next;
            if (!q->first_pkt)
                q->last_pkt = NULL;
            q->nb_packets--;
            q->size -= pkt1->pkt.size + sizeof(*pkt1);
            *pkt = pkt1->pkt;
            av_free(pkt1);
            ret = 1;
            break;
        } else if (!block) {
            ret = 0;
            break;
        } else if (q->end_request) {
            ret = -1;
            break;            
        } else {
            SDL_CondWait(q->cond, q->mutex);
        }
    }
    SDL_UnlockMutex(q->mutex);
    return ret;
}

static inline void fill_rectangle(SDL_Surface *screen,
                                  int x, int y, int w, int h, int color)
{
    SDL_Rect rect;
    rect.x = x;
    rect.y = y;
    rect.w = w;
    rect.h = h;
    SDL_FillRect(screen, &rect, color);
}




#define SCALEBITS 10
#define ONE_HALF  (1 << (SCALEBITS - 1))
#define FIX(x)    ((int) ((x) * (1<<SCALEBITS) + 0.5))

#define RGB_TO_Y_CCIR(r, g, b) \
((FIX(0.29900*219.0/255.0) * (r) + FIX(0.58700*219.0/255.0) * (g) + \
  FIX(0.11400*219.0/255.0) * (b) + (ONE_HALF + (16 << SCALEBITS))) >> SCALEBITS)

#define RGB_TO_U_CCIR(r1, g1, b1, shift)\
(((- FIX(0.16874*224.0/255.0) * r1 - FIX(0.33126*224.0/255.0) * g1 +         \
     FIX(0.50000*224.0/255.0) * b1 + (ONE_HALF << shift) - 1) >> (SCALEBITS + shift)) + 128)

#define RGB_TO_V_CCIR(r1, g1, b1, shift)\
(((FIX(0.50000*224.0/255.0) * r1 - FIX(0.41869*224.0/255.0) * g1 -           \
   FIX(0.08131*224.0/255.0) * b1 + (ONE_HALF << shift) - 1) >> (SCALEBITS + shift)) + 128)

#define ALPHA_BLEND(a, oldp, newp, s)\
((((oldp << s) * (255 - (a))) + (newp * (a))) / (255 << s))

#define RGBA_IN(r, g, b, a, s)\
{\
    unsigned int v = ((const uint32_t *)(s))[0];\
    a = (v >> 24) & 0xff;\
    r = (v >> 16) & 0xff;\
    g = (v >> 8) & 0xff;\
    b = v & 0xff;\
}

#define YUVA_IN(y, u, v, a, s, pal)\
{\
    unsigned int val = ((const uint32_t *)(pal))[*(const uint8_t*)(s)];\
    a = (val >> 24) & 0xff;\
    y = (val >> 16) & 0xff;\
    u = (val >> 8) & 0xff;\
    v = val & 0xff;\
}

#define YUVA_OUT(d, y, u, v, a)\
{\
    ((uint32_t *)(d))[0] = (a << 24) | (y << 16) | (u << 8) | v;\
}


#define BPP 1

static void blend_subrect(AVPicture *dst, const AVSubtitleRect *rect, int imgw, int imgh)
{
    int wrap, wrap3, width2, skip2;
    int y, u, v, a, u1, v1, a1, w, h;
    uint8_t *lum, *cb, *cr;
    const uint8_t *p;
    const uint32_t *pal;
    int dstx, dsty, dstw, dsth;

    dstw = av_clip(rect->w, 0, imgw);
    dsth = av_clip(rect->h, 0, imgh);
    dstx = av_clip(rect->x, 0, imgw - dstw);
    dsty = av_clip(rect->y, 0, imgh - dsth);
    lum = dst->data[0] + dsty * dst->linesize[0];
    cb = dst->data[1] + (dsty >> 1) * dst->linesize[1];
    cr = dst->data[2] + (dsty >> 1) * dst->linesize[2];

    width2 = ((dstw + 1) >> 1) + (dstx & ~dstw & 1);
    skip2 = dstx >> 1;
    wrap = dst->linesize[0];
    wrap3 = rect->pict.linesize[0];
    p = rect->pict.data[0];
    pal = (const uint32_t *)rect->pict.data[1];  /* Now in YCrCb! */

    if (dsty & 1) {
        lum += dstx;
        cb += skip2;
        cr += skip2;

        if (dstx & 1) {
            YUVA_IN(y, u, v, a, p, pal);
            lum[0] = ALPHA_BLEND(a, lum[0], y, 0);
            cb[0] = ALPHA_BLEND(a >> 2, cb[0], u, 0);
            cr[0] = ALPHA_BLEND(a >> 2, cr[0], v, 0);
            cb++;
            cr++;
            lum++;
            p += BPP;
        }
        for(w = dstw - (dstx & 1); w >= 2; w -= 2) {
            YUVA_IN(y, u, v, a, p, pal);
            u1 = u;
            v1 = v;
            a1 = a;
            lum[0] = ALPHA_BLEND(a, lum[0], y, 0);

            YUVA_IN(y, u, v, a, p + BPP, pal);
            u1 += u;
            v1 += v;
            a1 += a;
            lum[1] = ALPHA_BLEND(a, lum[1], y, 0);
            cb[0] = ALPHA_BLEND(a1 >> 2, cb[0], u1, 1);
            cr[0] = ALPHA_BLEND(a1 >> 2, cr[0], v1, 1);
            cb++;
            cr++;
            p += 2 * BPP;
            lum += 2;
        }
        if (w) {
            YUVA_IN(y, u, v, a, p, pal);
            lum[0] = ALPHA_BLEND(a, lum[0], y, 0);
            cb[0] = ALPHA_BLEND(a >> 2, cb[0], u, 0);
            cr[0] = ALPHA_BLEND(a >> 2, cr[0], v, 0);
            p++;
            lum++;
        }
        p += wrap3 - dstw * BPP;
        lum += wrap - dstw - dstx;
        cb += dst->linesize[1] - width2 - skip2;
        cr += dst->linesize[2] - width2 - skip2;
    }
    for(h = dsth - (dsty & 1); h >= 2; h -= 2) {
        lum += dstx;
        cb += skip2;
        cr += skip2;

        if (dstx & 1) {
            YUVA_IN(y, u, v, a, p, pal);
            u1 = u;
            v1 = v;
            a1 = a;
            lum[0] = ALPHA_BLEND(a, lum[0], y, 0);
            p += wrap3;
            lum += wrap;
            YUVA_IN(y, u, v, a, p, pal);
            u1 += u;
            v1 += v;
            a1 += a;
            lum[0] = ALPHA_BLEND(a, lum[0], y, 0);
            cb[0] = ALPHA_BLEND(a1 >> 2, cb[0], u1, 1);
            cr[0] = ALPHA_BLEND(a1 >> 2, cr[0], v1, 1);
            cb++;
            cr++;
            p += -wrap3 + BPP;
            lum += -wrap + 1;
        }
        for(w = dstw - (dstx & 1); w >= 2; w -= 2) {
            YUVA_IN(y, u, v, a, p, pal);
            u1 = u;
            v1 = v;
            a1 = a;
            lum[0] = ALPHA_BLEND(a, lum[0], y, 0);

            YUVA_IN(y, u, v, a, p + BPP, pal);
            u1 += u;
            v1 += v;
            a1 += a;
            lum[1] = ALPHA_BLEND(a, lum[1], y, 0);
            p += wrap3;
            lum += wrap;

            YUVA_IN(y, u, v, a, p, pal);
            u1 += u;
            v1 += v;
            a1 += a;
            lum[0] = ALPHA_BLEND(a, lum[0], y, 0);

            YUVA_IN(y, u, v, a, p + BPP, pal);
            u1 += u;
            v1 += v;
            a1 += a;
            lum[1] = ALPHA_BLEND(a, lum[1], y, 0);

            cb[0] = ALPHA_BLEND(a1 >> 2, cb[0], u1, 2);
            cr[0] = ALPHA_BLEND(a1 >> 2, cr[0], v1, 2);

            cb++;
            cr++;
            p += -wrap3 + 2 * BPP;
            lum += -wrap + 2;
        }
        if (w) {
            YUVA_IN(y, u, v, a, p, pal);
            u1 = u;
            v1 = v;
            a1 = a;
            lum[0] = ALPHA_BLEND(a, lum[0], y, 0);
            p += wrap3;
            lum += wrap;
            YUVA_IN(y, u, v, a, p, pal);
            u1 += u;
            v1 += v;
            a1 += a;
            lum[0] = ALPHA_BLEND(a, lum[0], y, 0);
            cb[0] = ALPHA_BLEND(a1 >> 2, cb[0], u1, 1);
            cr[0] = ALPHA_BLEND(a1 >> 2, cr[0], v1, 1);
            cb++;
            cr++;
            p += -wrap3 + BPP;
            lum += -wrap + 1;
        }
        p += wrap3 + (wrap3 - dstw * BPP);
        lum += wrap + (wrap - dstw - dstx);
        cb += dst->linesize[1] - width2 - skip2;
        cr += dst->linesize[2] - width2 - skip2;
    }
    /* handle odd height */
    if (h) {
        lum += dstx;
        cb += skip2;
        cr += skip2;

        if (dstx & 1) {
            YUVA_IN(y, u, v, a, p, pal);
            lum[0] = ALPHA_BLEND(a, lum[0], y, 0);
            cb[0] = ALPHA_BLEND(a >> 2, cb[0], u, 0);
            cr[0] = ALPHA_BLEND(a >> 2, cr[0], v, 0);
            cb++;
            cr++;
            lum++;
            p += BPP;
        }
        for(w = dstw - (dstx & 1); w >= 2; w -= 2) {
            YUVA_IN(y, u, v, a, p, pal);
            u1 = u;
            v1 = v;
            a1 = a;
            lum[0] = ALPHA_BLEND(a, lum[0], y, 0);

            YUVA_IN(y, u, v, a, p + BPP, pal);
            u1 += u;
            v1 += v;
            a1 += a;
            lum[1] = ALPHA_BLEND(a, lum[1], y, 0);
            cb[0] = ALPHA_BLEND(a1 >> 2, cb[0], u, 1);
            cr[0] = ALPHA_BLEND(a1 >> 2, cr[0], v, 1);
            cb++;
            cr++;
            p += 2 * BPP;
            lum += 2;
        }
        if (w) {
            YUVA_IN(y, u, v, a, p, pal);
            lum[0] = ALPHA_BLEND(a, lum[0], y, 0);
            cb[0] = ALPHA_BLEND(a >> 2, cb[0], u, 0);
            cr[0] = ALPHA_BLEND(a >> 2, cr[0], v, 0);
        }
    }
}

static void free_subpicture(SubPicture *sp)
{
    int i;

    for (i = 0; i < sp->sub.num_rects; i++)
    {
        av_freep(&sp->sub.rects[i]->pict.data[0]);
        av_freep(&sp->sub.rects[i]->pict.data[1]);
        av_freep(&sp->sub.rects[i]);
    }

    av_free(sp->sub.rects);

    memset(&sp->sub, 0, sizeof(AVSubtitle));
}

static void video_image_display(VideoState *is)
{
    VideoPicture *vp;
    SubPicture *sp;
    AVPicture pict;
    float aspect_ratio;
    int width, height, x, y;
    SDL_Rect rect;
    int i;

    vp = &is->pictq[is->pictq_rindex];
    if (vp->bmp) {
        /* XXX: use variable in the frame */
        if (is->video_st->sample_aspect_ratio.num)
            aspect_ratio = av_q2d(is->video_st->sample_aspect_ratio);
        else if (is->video_st->codec->sample_aspect_ratio.num)
            aspect_ratio = av_q2d(is->video_st->codec->sample_aspect_ratio);
        else
            aspect_ratio = 0;
        if (aspect_ratio <= 0.0)
            aspect_ratio = 1.0;
        aspect_ratio *= (float)is->video_st->codec->width / is->video_st->codec->height;
        /* if an active format is indicated, then it overrides the
           mpeg format */
#if 0
        if (is->video_st->codec->dtg_active_format != is->dtg_active_format) {
            is->dtg_active_format = is->video_st->codec->dtg_active_format;
            printf("dtg_active_format=%d\n", is->dtg_active_format);
        }
#endif
#if 0
        switch(is->video_st->codec->dtg_active_format) {
        case FF_DTG_AFD_SAME:
        default:
            /* nothing to do */
            break;
        case FF_DTG_AFD_4_3:
            aspect_ratio = 4.0 / 3.0;
            break;
        case FF_DTG_AFD_16_9:
            aspect_ratio = 16.0 / 9.0;
            break;
        case FF_DTG_AFD_14_9:
            aspect_ratio = 14.0 / 9.0;
            break;
        case FF_DTG_AFD_4_3_SP_14_9:
            aspect_ratio = 14.0 / 9.0;
            break;
        case FF_DTG_AFD_16_9_SP_14_9:
            aspect_ratio = 14.0 / 9.0;
            break;
        case FF_DTG_AFD_SP_4_3:
            aspect_ratio = 4.0 / 3.0;
            break;
        }
#endif

        if (is->subtitle_st)
        {
            if (is->subpq_size > 0)
            {
                sp = &is->subpq[is->subpq_rindex];

                if (vp->pts >= sp->pts + ((float) sp->sub.start_display_time / 1000))
                {
                    SDL_LockYUVOverlay (vp->bmp);

                    pict.data[0] = vp->bmp->pixels[0];
                    pict.data[1] = vp->bmp->pixels[2];
                    pict.data[2] = vp->bmp->pixels[1];

                    pict.linesize[0] = vp->bmp->pitches[0];
                    pict.linesize[1] = vp->bmp->pitches[2];
                    pict.linesize[2] = vp->bmp->pitches[1];

                    for (i = 0; i < sp->sub.num_rects; i++)
                        blend_subrect(&pict, sp->sub.rects[i],
                                      vp->bmp->w, vp->bmp->h);

                    SDL_UnlockYUVOverlay (vp->bmp);
                }
            }
        }


        /* XXX: we suppose the screen has a 1.0 pixel ratio */
        height = is->height;
        width = ((int)rint(height * aspect_ratio)) & ~1;
        if (width > is->width) {
            width = is->width;
            height = ((int)rint(width / aspect_ratio)) & ~1;
        }
        x = (is->width - width) / 2;
        y = (is->height - height) / 2;
        if (!is->no_background) {
            /* fill the background */
            //            fill_border(is, x, y, width, height, QERGB(0x00, 0x00, 0x00));
        } else {
            is->no_background = 0;
        }
        rect.x = is->xleft + x;
        rect.y = is->ytop  + y;
        rect.w = width;
        rect.h = height;
        SDL_DisplayYUVOverlay(vp->bmp, &rect);
    } else {
#if 0
        fill_rectangle(screen,
                       is->xleft, is->ytop, is->width, is->height,
                       QERGB(0x00, 0x00, 0x00));
#endif
    }
}

static inline int compute_mod(int a, int b)
{
    a = a % b;
    if (a >= 0)
        return a;
    else
        return a + b;
}


/* display the current picture, if any */
static void video_display(VideoState *is)
{
    if (is->video_st)
        video_image_display(is);
}

static Uint32 sdl_refresh_timer_cb(Uint32 interval, void *opaque)
{
    SDL_Event event;
    event.type = FF_REFRESH_EVENT;
    event.user.data1 = opaque;
    SDL_PushEvent(&event);
    return 0; /* 0 means stop timer */
}

/* schedule a video refresh in 'delay' ms */
static void schedule_refresh(VideoState *is, int delay)
{
    if (is->video_stream < 0) {
        return;
    }

    if(!delay) delay=1; //SDL seems to be buggy when the delay is 0
    SDL_AddTimer(delay, sdl_refresh_timer_cb, is);
}

/* get the current audio clock value */
static double get_audio_clock(VideoState *is)
{
    double pts;
    int hw_buf_size, bytes_per_sec;
    pts = is->audio_clock;
    hw_buf_size = audio_write_get_buf_size(is);
    bytes_per_sec = 0;
    if (is->audio_st) {
        bytes_per_sec = is->audio_st->codec->sample_rate *
            2 * is->audio_st->codec->channels;
    }
    if (bytes_per_sec)
        pts -= (double)hw_buf_size / bytes_per_sec;
    return pts;
}

/* get the current video clock value */
static double get_video_clock(VideoState *is)
{
    double delta;
    if (is->paused) {
        delta = 0;
    } else {
        delta = (av_gettime() - is->video_current_pts_time) / 1000000.0;
    }
    return is->video_current_pts + delta;
}

/* get the current external clock value */
static double get_external_clock(VideoState *is)
{
    int64_t ti;
    ti = av_gettime();
    return is->external_clock + ((ti - is->external_clock_time) * 1e-6);
}

/* get the current master clock value */
static double get_master_clock(VideoState *is)
{
    double val;

    if (is->av_sync_type == AV_SYNC_VIDEO_MASTER) {
        if (is->video_st)
            val = get_video_clock(is);
        else
            val = get_audio_clock(is);
    } else if (is->av_sync_type == AV_SYNC_AUDIO_MASTER) {
        if (is->audio_st)
            val = get_audio_clock(is);
        else
            val = get_video_clock(is);
    } else {
        val = get_external_clock(is);
    }
    return val;
}

/* /\* seek in the stream *\/ */
/* static void stream_seek(VideoState *is, int64_t pos, int rel) */
/* { */
/*     if (!is->seek_req) { */
/*         is->seek_pos = pos; */
/*         is->seek_flags = rel < 0 ? AVSEEK_FLAG_BACKWARD : 0; */
/*         if (seek_by_bytes) */
/*             is->seek_flags |= AVSEEK_FLAG_BYTE; */
/*         is->seek_req = 1; */
/*     } */
/* } */

/* /\* pause or resume the video *\/ */
/* static void stream_pause(VideoState *is) */
/* { */
/*     is->paused = !is->paused; */
/*     if (!is->paused) { */
/*         is->video_current_pts = get_video_clock(is); */
/*         is->frame_timer += (av_gettime() - is->video_current_pts_time) / 1000000.0; */
/*     } */
/* } */

static double compute_frame_delay(double frame_current_pts, VideoState *is)
{
    double actual_delay, delay, sync_threshold, ref_clock, diff;

    /* compute nominal delay */
    delay = frame_current_pts - is->frame_last_pts;
    if (delay <= 0 || delay >= 10.0) {
        /* if incorrect delay, use previous one */
        delay = is->frame_last_delay;
    } else {
        is->frame_last_delay = delay;
    }
    is->frame_last_pts = frame_current_pts;

    /* update delay to follow master synchronisation source */
    if (((is->av_sync_type == AV_SYNC_AUDIO_MASTER && is->audio_st) ||
         is->av_sync_type == AV_SYNC_EXTERNAL_CLOCK)) {
        /* if video is slave, we try to correct big delays by
           duplicating or deleting a frame */
        ref_clock = get_master_clock(is);
        diff = frame_current_pts - ref_clock;

        /* skip or repeat frame. We take into account the
           delay to compute the threshold. I still don't know
           if it is the best guess */
        sync_threshold = FFMAX(AV_SYNC_THRESHOLD, delay);
        if (fabs(diff) < AV_NOSYNC_THRESHOLD) {
            if (diff <= -sync_threshold)
                delay = 0;
            else if (diff >= sync_threshold)
                delay = 2 * delay;
        }
    }

    is->frame_timer += delay;
    /* compute the REAL delay (we need to do that to avoid
       long term errors */
    actual_delay = is->frame_timer - (av_gettime() / 1000000.0);
    if (actual_delay < 0.010) {
        /* XXX: should skip picture */
        actual_delay = 0.010;
    }

#if defined(DEBUG_SYNC)
    printf("video: delay=%0.3f actual_delay=%0.3f pts=%0.3f A-V=%f\n",
            delay, actual_delay, frame_current_pts, -diff);
#endif

    return actual_delay;
}

/* called to display each frame */
static void video_refresh_timer(void *opaque)
{
    VideoState *is = opaque;
    VideoPicture *vp;

    SubPicture *sp, *sp2;

    double delay;
    
    if (is->video_st) {
        if (is->pictq_size == 0) {
            /* if no picture, need to wait */
            schedule_refresh(is, 1);
        } else {
            /* dequeue the picture */
            vp = &is->pictq[is->pictq_rindex];

            /* update current video pts */
            is->video_current_pts = vp->pts;
            is->video_current_pts_time = av_gettime();

            delay = compute_frame_delay(vp->pts, is);

            /* launch timer for next picture */
            schedule_refresh(is, (int)(delay * 1000 + 0.5));

            /* if(is->subtitle_st) { */
            /*     if (is->subtitle_stream_changed) { */
            /*         SDL_LockMutex(is->subpq_mutex); */

            /*         while (is->subpq_size) { */
            /*             free_subpicture(&is->subpq[is->subpq_rindex]); */

            /*             /\* update queue size and signal for next picture *\/ */
            /*             if (++is->subpq_rindex == SUBPICTURE_QUEUE_SIZE) */
            /*                 is->subpq_rindex = 0; */

            /*             is->subpq_size--; */
            /*         } */
            /*         is->subtitle_stream_changed = 0; */

            /*         SDL_CondSignal(is->subpq_cond); */
            /*         SDL_UnlockMutex(is->subpq_mutex); */
            /*     } else { */
            /*         if (is->subpq_size > 0) { */
            /*             sp = &is->subpq[is->subpq_rindex]; */

            /*             if (is->subpq_size > 1) */
            /*                 sp2 = &is->subpq[(is->subpq_rindex + 1) % SUBPICTURE_QUEUE_SIZE]; */
            /*             else */
            /*                 sp2 = NULL; */

            /*             if ((is->video_current_pts > (sp->pts + ((float) sp->sub.end_display_time / 1000))) */
            /*                     || (sp2 && is->video_current_pts > (sp2->pts + ((float) sp2->sub.start_display_time / 1000)))) */
            /*             { */
            /*                 free_subpicture(sp); */

            /*                 /\* update queue size and signal for next picture *\/ */
            /*                 if (++is->subpq_rindex == SUBPICTURE_QUEUE_SIZE) */
            /*                     is->subpq_rindex = 0; */

            /*                 SDL_LockMutex(is->subpq_mutex); */
            /*                 is->subpq_size--; */
            /*                 SDL_CondSignal(is->subpq_cond); */
            /*                 SDL_UnlockMutex(is->subpq_mutex); */
            /*             } */
            /*         } */
            /*     } */
            /* } */

            /* display picture */
            if (delay > 0.010) {
                video_display(is);
            }
                
            /* update queue size and signal for next picture */
            if (++is->pictq_rindex == VIDEO_PICTURE_QUEUE_SIZE)
                is->pictq_rindex = 0;

            SDL_LockMutex(is->pictq_mutex);
            is->pictq_size--;
            SDL_CondSignal(is->pictq_cond);
            SDL_UnlockMutex(is->pictq_mutex);
        }
    } 

    if (show_status) {
        static int64_t last_time;
        int64_t cur_time;
        int aqsize, vqsize, sqsize;
        double av_diff;

        cur_time = av_gettime();
        if (!last_time || (cur_time - last_time) >= 500 * 1000) {
            aqsize = 0;
            vqsize = 0;
            sqsize = 0;
            if (is->audio_st)
                aqsize = is->audioq.size;
            if (is->video_st)
                vqsize = is->videoq.size;
            if (is->subtitle_st)
                sqsize = is->subtitleq.size;
            av_diff = 0;
            if (is->audio_st && is->video_st)
                av_diff = get_audio_clock(is) - get_video_clock(is);
            printf("%7.2f A-V:%7.3f aq=%5dKB vq=%5dKB sq=%5dB    \r",
                   get_master_clock(is), av_diff, aqsize / 1024, vqsize / 1024, sqsize);
            fflush(stdout);
            last_time = cur_time;
        }
    }
}

/* allocate a picture (needs to do that in main thread to avoid
   potential locking problems */
static void alloc_picture(void *opaque, PyObject *pysurf)
{
    VideoState *is = opaque;
    VideoPicture *vp;

    SDL_Surface *surf;

    if (!is->needs_alloc) {
        return;
    }

    is->needs_alloc = 0;
    
    surf = PySurface_AsSurface(pysurf);
    is->width = surf->w;
    is->height = surf->h;
    
    vp = &is->pictq[is->pictq_windex];

    if (vp->bmp)
        SDL_FreeYUVOverlay(vp->bmp);

#if 0
    /* XXX: use generic function */
    /* XXX: disable overlay if no hardware acceleration or if RGB format */
    switch(is->video_st->codec->pix_fmt) {
    case PIX_FMT_YUV420P:
    case PIX_FMT_YUV422P:
    case PIX_FMT_YUV444P:
    case PIX_FMT_YUYV422:
    case PIX_FMT_YUV410P:
    case PIX_FMT_YUV411P:
        is_yuv = 1;
        break;
    default:
        is_yuv = 0;
        break;
    }
#endif

    vp->bmp = SDL_CreateYUVOverlay(
        is->video_st->codec->width,
        is->video_st->codec->height,
        SDL_YV12_OVERLAY,
        surf);
    
    vp->width = is->video_st->codec->width;
    vp->height = is->video_st->codec->height;

    SDL_LockMutex(is->pictq_mutex);
    vp->allocated = 1;
    SDL_CondSignal(is->pictq_cond);
    SDL_UnlockMutex(is->pictq_mutex);
}

/**
 *
 * @param pts the dts of the pkt / pts of the frame and guessed if not known
 */
static int queue_picture(VideoState *is, AVFrame *src_frame, double pts)
{
    VideoPicture *vp;
    int dst_pix_fmt;
    AVPicture pict;
    static struct SwsContext *img_convert_ctx;

    /* wait until we have space to put a new picture */
    SDL_LockMutex(is->pictq_mutex);
    while (is->pictq_size >= VIDEO_PICTURE_QUEUE_SIZE &&
           !is->videoq.abort_request) {
        SDL_CondWait(is->pictq_cond, is->pictq_mutex);
    }
    SDL_UnlockMutex(is->pictq_mutex);

    if (is->videoq.abort_request)
        return -1;

    vp = &is->pictq[is->pictq_windex];

    /* alloc or resize hardware picture buffer */
    if (!vp->bmp ||
        vp->width != is->video_st->codec->width ||
        vp->height != is->video_st->codec->height) {
        SDL_Event event;

        vp->allocated = 0;

        is->needs_alloc = 1;

        /* the allocation must be done in the main thread to avoid
           locking problems */
        event.type = FF_ALLOC_EVENT;
        event.user.data1 = is;
        SDL_PushEvent(&event);

        
        /* wait until the picture is allocated */
        SDL_LockMutex(is->pictq_mutex);
        while (!vp->allocated && !is->videoq.abort_request) {
            SDL_CondWait(is->pictq_cond, is->pictq_mutex);
        }
        SDL_UnlockMutex(is->pictq_mutex);

        if (is->videoq.abort_request)
            return -1;
    }

    /* if the frame is not skipped, then display it */
    if (vp->bmp) {
        /* get a pointer on the bitmap */
        SDL_LockYUVOverlay (vp->bmp);

        dst_pix_fmt = PIX_FMT_YUV420P;
        pict.data[0] = vp->bmp->pixels[0];
        pict.data[1] = vp->bmp->pixels[2];
        pict.data[2] = vp->bmp->pixels[1];

        pict.linesize[0] = vp->bmp->pitches[0];
        pict.linesize[1] = vp->bmp->pitches[2];
        pict.linesize[2] = vp->bmp->pitches[1];
        // sws_flags = av_get_int(sws_opts, "sws_flags", NULL);
        img_convert_ctx = sws_getCachedContext(img_convert_ctx,
            is->video_st->codec->width, is->video_st->codec->height,
            is->video_st->codec->pix_fmt,
            is->video_st->codec->width, is->video_st->codec->height,
            dst_pix_fmt, sws_flags, NULL, NULL, NULL);
        if (img_convert_ctx == NULL) {
            fprintf(stderr, "Cannot initialize the conversion context\n");
        }
        sws_scale(img_convert_ctx, src_frame->data, src_frame->linesize,
                  0, is->video_st->codec->height, pict.data, pict.linesize);
        /* update the bitmap content */
        SDL_UnlockYUVOverlay(vp->bmp);

        vp->pts = pts;

        /* now we can update the picture count */
        if (++is->pictq_windex == VIDEO_PICTURE_QUEUE_SIZE)
            is->pictq_windex = 0;
        SDL_LockMutex(is->pictq_mutex);
        is->pictq_size++;
        SDL_UnlockMutex(is->pictq_mutex);
    }
    return 0;
}

/**
 * compute the exact PTS for the picture if it is omitted in the stream
 * @param pts1 the dts of the pkt / pts of the frame
 */
static int output_picture2(VideoState *is, AVFrame *src_frame, double pts1)
{
    double frame_delay, pts;

    pts = pts1;

    if (pts != 0) {
        /* update video clock with pts, if present */
        is->video_clock = pts;
    } else {
        pts = is->video_clock;
    }
    /* update video clock for next frame */
    frame_delay = av_q2d(is->video_st->codec->time_base);
    /* for MPEG2, the frame can be repeated, so we update the
       clock accordingly */
    frame_delay += src_frame->repeat_pict * (frame_delay * 0.5);
    is->video_clock += frame_delay;

#if defined(DEBUG_SYNC) && 0
    {
        int ftype;
        if (src_frame->pict_type == FF_B_TYPE)
            ftype = 'B';
        else if (src_frame->pict_type == FF_I_TYPE)
            ftype = 'I';
        else
            ftype = 'P';
        printf("frame_type=%c clock=%0.3f pts=%0.3f\n",
               ftype, pts, pts1);
    }
#endif
    return queue_picture(is, src_frame, pts);
}

static int video_thread(void *arg)
{
    VideoState *is = arg;
    AVPacket pkt1, *pkt = &pkt1;
    int len1, got_picture;
    AVFrame *frame= avcodec_alloc_frame();
    double pts;

    for(;;) {
        while (is->paused && !is->videoq.abort_request) {
            SDL_Delay(10);
        }
        if (packet_queue_get(&is->videoq, pkt, 1) < 0)
            break;

        if(pkt->data == flush_pkt.data){
            avcodec_flush_buffers(is->video_st->codec);
            continue;
        }

        /* NOTE: ipts is the PTS of the _first_ picture beginning in
           this packet, if any */
        is->video_st->codec->reordered_opaque= pkt->pts;
        len1 = avcodec_decode_video(is->video_st->codec,
                                    frame, &got_picture,
                                    pkt->data, pkt->size);

        if(   (decoder_reorder_pts || pkt->dts == AV_NOPTS_VALUE)
           && frame->reordered_opaque != AV_NOPTS_VALUE)
            pts= frame->reordered_opaque;
        else if(pkt->dts != AV_NOPTS_VALUE)
            pts= pkt->dts;
        else
            pts= 0;
        pts *= av_q2d(is->video_st->time_base);

//            if (len1 < 0)
//                break;
        if (got_picture) {
            if (output_picture2(is, frame, pts) < 0)
                goto the_end;
        }
        av_free_packet(pkt);
    }
 the_end:
    av_free(frame);
    return 0;
}

static int subtitle_thread(void *arg)
{
    VideoState *is = arg;
    SubPicture *sp;
    AVPacket pkt1, *pkt = &pkt1;
    int len1, got_subtitle;
    double pts;
    int i, j;
    int r, g, b, y, u, v, a;

    for(;;) {
        while (is->paused && !is->subtitleq.abort_request) {
            SDL_Delay(10);
        }
        if (packet_queue_get(&is->subtitleq, pkt, 1) < 0)
            break;

        if(pkt->data == flush_pkt.data){
            avcodec_flush_buffers(is->subtitle_st->codec);
            continue;
        }
        SDL_LockMutex(is->subpq_mutex);
        while (is->subpq_size >= SUBPICTURE_QUEUE_SIZE &&
               !is->subtitleq.abort_request) {
            SDL_CondWait(is->subpq_cond, is->subpq_mutex);
        }
        SDL_UnlockMutex(is->subpq_mutex);

        if (is->subtitleq.abort_request)
            goto the_end;

        sp = &is->subpq[is->subpq_windex];

       /* NOTE: ipts is the PTS of the _first_ picture beginning in
           this packet, if any */
        pts = 0;
        if (pkt->pts != AV_NOPTS_VALUE)
            pts = av_q2d(is->subtitle_st->time_base)*pkt->pts;

        len1 = avcodec_decode_subtitle(is->subtitle_st->codec,
                                    &sp->sub, &got_subtitle,
                                    pkt->data, pkt->size);
//            if (len1 < 0)
//                break;
        if (got_subtitle && sp->sub.format == 0) {
            sp->pts = pts;

            for (i = 0; i < sp->sub.num_rects; i++)
            {
                for (j = 0; j < sp->sub.rects[i]->nb_colors; j++)
                {
                    RGBA_IN(r, g, b, a, (uint32_t*)sp->sub.rects[i]->pict.data[1] + j);
                    y = RGB_TO_Y_CCIR(r, g, b);
                    u = RGB_TO_U_CCIR(r, g, b, 0);
                    v = RGB_TO_V_CCIR(r, g, b, 0);
                    YUVA_OUT((uint32_t*)sp->sub.rects[i]->pict.data[1] + j, y, u, v, a);
                }
            }

            /* now we can update the picture count */
            if (++is->subpq_windex == SUBPICTURE_QUEUE_SIZE)
                is->subpq_windex = 0;
            SDL_LockMutex(is->subpq_mutex);
            is->subpq_size++;
            SDL_UnlockMutex(is->subpq_mutex);
        }
        av_free_packet(pkt);
    }
 the_end:
    return 0;
}


/* return the new audio buffer size (samples can be added or deleted
   to get better sync if video or external master clock) */
static int synchronize_audio(VideoState *is, short *samples,
                             int samples_size1, double pts)
{
    int n, samples_size;
    double ref_clock;

    n = 2 * is->audio_st->codec->channels;
    samples_size = samples_size1;

    /* if not master, then we try to remove or add samples to correct the clock */
    if (((is->av_sync_type == AV_SYNC_VIDEO_MASTER && is->video_st) ||
         is->av_sync_type == AV_SYNC_EXTERNAL_CLOCK)) {
        double diff, avg_diff;
        int wanted_size, min_size, max_size, nb_samples;

        ref_clock = get_master_clock(is);
        diff = get_audio_clock(is) - ref_clock;

        if (diff < AV_NOSYNC_THRESHOLD) {
            is->audio_diff_cum = diff + is->audio_diff_avg_coef * is->audio_diff_cum;
            if (is->audio_diff_avg_count < AUDIO_DIFF_AVG_NB) {
                /* not enough measures to have a correct estimate */
                is->audio_diff_avg_count++;
            } else {
                /* estimate the A-V difference */
                avg_diff = is->audio_diff_cum * (1.0 - is->audio_diff_avg_coef);

                if (fabs(avg_diff) >= is->audio_diff_threshold) {
                    wanted_size = samples_size + ((int)(diff * is->audio_st->codec->sample_rate) * n);
                    nb_samples = samples_size / n;

                    min_size = ((nb_samples * (100 - SAMPLE_CORRECTION_PERCENT_MAX)) / 100) * n;
                    max_size = ((nb_samples * (100 + SAMPLE_CORRECTION_PERCENT_MAX)) / 100) * n;
                    if (wanted_size < min_size)
                        wanted_size = min_size;
                    else if (wanted_size > max_size)
                        wanted_size = max_size;

                    /* add or remove samples to correction the synchro */
                    if (wanted_size < samples_size) {
                        /* remove samples */
                        samples_size = wanted_size;
                    } else if (wanted_size > samples_size) {
                        uint8_t *samples_end, *q;
                        int nb;

                        /* add samples */
                        nb = (samples_size - wanted_size);
                        samples_end = (uint8_t *)samples + samples_size - n;
                        q = samples_end + n;
                        while (nb > 0) {
                            memcpy(q, samples_end, n);
                            q += n;
                            nb -= n;
                        }
                        samples_size = wanted_size;
                    }
                }
#if 0
                printf("diff=%f adiff=%f sample_diff=%d apts=%0.3f vpts=%0.3f %f\n",
                       diff, avg_diff, samples_size - samples_size1,
                       is->audio_clock, is->video_clock, is->audio_diff_threshold);
#endif
            }
        } else {
            /* too big difference : may be initial PTS errors, so
               reset A-V filter */
            is->audio_diff_avg_count = 0;
            is->audio_diff_cum = 0;
        }
    }

    return samples_size;
}

/* decode one audio frame and returns its uncompressed size */
static int audio_decode_frame(VideoState *is, double *pts_ptr)
{
    AVPacket *pkt = &is->audio_pkt;
    AVCodecContext *dec= is->audio_st->codec;
    int len1, data_size;
    double pts;

    for(;;) {
        /* NOTE: the audio packet can contain several frames */
        while (is->audio_pkt_size > 0) {
            data_size = sizeof(is->audio_buf1);
            len1 = avcodec_decode_audio2(dec,
                                        (int16_t *)is->audio_buf1, &data_size,
                                        is->audio_pkt_data, is->audio_pkt_size);
            if (len1 < 0) {
                /* if error, we skip the frame */
                is->audio_pkt_size = 0;
                break;
            }

            is->audio_pkt_data += len1;
            is->audio_pkt_size -= len1;
            if (data_size <= 0)
                continue;

            if (!is->reformat_ctx &&
                (dec->channels != 2 || dec->sample_fmt != SAMPLE_FMT_S16)) {

                is->reformat_ctx = av_audio_resample_init(
                    2,
                    dec->channels,
                    // audio_sample_rate,
                    dec->sample_rate,
                    dec->sample_rate,
                    SAMPLE_FMT_S16,
                    dec->sample_fmt,
                    1, 0, 0, 1.0);

                // Setting the last four parameters to 16, 0, 0, 1.0
                // gives better performance when the rate is less than
                // audio_sample_rate / 2, at the cost of some
                // performance. Probably not worth it - Tom.
            }

            // Moved by tom, from below next block. Is this right?
            

            if (is->reformat_ctx) {
                
                int len = data_size / (av_get_bits_per_sample_format(dec->sample_fmt) / 8);
                len /= dec->channels;

                len = audio_resample(is->reformat_ctx, (short *) is->audio_buf2, (short *) is->audio_buf1, len);

                data_size = len * 4;
                is->audio_buf = is->audio_buf2;                
            } else {
                is->audio_buf = is->audio_buf1;
            }

            if (dec->sample_rate != audio_sample_rate) {
                short *in;
                short *out;
                int outpos;
                int in_per_out;
                int inpos;

                int len = data_size / 4;
                
                if (is->audio_buf == is->audio_buf1) {
                    in = (short *) is->audio_buf1;
                    out = (short *) is->audio_buf2;
                } else {
                    in = (short *) is->audio_buf2;
                    out = (short *) is->audio_buf1;
                }

                // Pad the buffer a bit. We pad with the difference
                // between the last sample and the one before it,
                // which seems reasonable.
                in[2 * len] = 2 * in[2 * len - 2] - in[2 * len - 4];
                in[2 * len + 1] = 2 * in[2 * len - 1] - in[2 * len - 3];
                                
                // The number of bytes of input consumed per output
                // sample. Scaled by 1 << 14.                
                in_per_out = (dec->sample_rate << 14) / audio_sample_rate;

                len *= (1 << 14);

                // The positions in the input. Scaled by 1 << 14.
                inpos = is->resample_frac;

                // The position in the output. Unscaled.
                outpos = 0;

                // While we still have samples.
                while (inpos < len) {
                    short a;
                    short b;

                    // Compute position and fraction.
                    int pos = inpos >> 14;
                    int frac = inpos & ((1 << 14) - 1);

                    // Interpolate the two channels.
                    a = in[2 * pos];
                    b = in[2 * pos + 2];
                    out[2 * outpos] = a + (((b - a) * frac) >> 14);

                    a = in[2 * pos + 1];
                    b = in[2 * pos + 3];
                    out[2 * outpos + 1] = a + (((b - a) * frac) >> 14);

                    outpos++;
                    inpos += in_per_out;                    
                }

                // Store the fraction.
                is->resample_frac = inpos & ((1 << 14) - 1);

                data_size = outpos * 4;
                is->audio_buf = (uint8_t *) out;                
            }


            /* if no pts, then compute it */
            pts = is->audio_clock;
            *pts_ptr = pts;
            /* is->audio_clock += (double)data_size / */
            /*     (double)(n * dec->sample_rate); */
            is->audio_clock += data_size / (4.0 * audio_sample_rate);

#if defined(DEBUG_SYNC)
            {
                static double last_clock;
                printf("audio: delay=%0.3f clock=%0.3f pts=%0.3f\n",
                       is->audio_clock - last_clock,
                       is->audio_clock, pts);
                last_clock = is->audio_clock;
            }
#endif


            // Deal with a reduced duration, like in an ogg file.

            if (is->audio_duration) {
                int len = data_size / 4;
                int maxlen = is->audio_duration - is->audio_played;
                
                if (len > maxlen) {
                    len = maxlen;
                }

                is->audio_played += len;
                data_size = len * 4;
            }
                
            return data_size;
        }

        /* free the current packet */
        if (pkt->data)
            av_free_packet(pkt);

        if (is->paused || is->audioq.abort_request) {
            return -1;
        }

        /* read next packet */
        if (packet_queue_get(&is->audioq, pkt, 1) < 0)
            return -1;
        if(pkt->data == flush_pkt.data){
            avcodec_flush_buffers(dec);
            continue;
        }

        is->audio_pkt_data = pkt->data;
        is->audio_pkt_size = pkt->size;

        /* if update the audio clock with the pts */
        if (pkt->pts != AV_NOPTS_VALUE) {
            is->audio_clock = av_q2d(is->audio_st->time_base)*pkt->pts;
        }
    }
}

/* get the current audio output buffer size, in samples. With SDL, we
   cannot have a precise information */
static int audio_write_get_buf_size(VideoState *is)
{
    return is->audio_buf_size - is->audio_buf_index;
}


/* prepare a new audio buffer */
int ffpy_audio_decode(struct VideoState *is, Uint8 *stream, int len)
{
    int audio_size, len1;
    double pts;

    int rv = 0;

    // Check to see if we've finished decoding, or we haven't
    // started yet. We don't leave this loop until one of those
    // is true.
    while (1) {
        if (is->finished) {
            return 0;
        }

        if (is->started) {
            break;
        }
        
        SDL_Delay(10);
    }
    
    is->audio_callback_time = av_gettime();
    
    while (len > 0) {
        if (is->audio_buf_index >= is->audio_buf_size) {

            audio_size = audio_decode_frame(is, &pts);

            if (audio_size < 0) {
                
                /* Nothing left to decode, break. */
                break;

            } else {
 
                audio_size = synchronize_audio(is, (int16_t *)is->audio_buf, audio_size,
                                              pts);

                is->audio_buf_size = audio_size;
            }
            is->audio_buf_index = 0;
        }
        len1 = is->audio_buf_size - is->audio_buf_index;
        if (len1 > len)
            len1 = len;
        memcpy(stream, (uint8_t *)is->audio_buf + is->audio_buf_index, len1);
        len -= len1;
        stream += len1;
        is->audio_buf_index += len1;

        rv += len1;
    }
    
    return rv;
}

/* open a given stream. Return 0 if OK */
static int stream_component_open(VideoState *is, int stream_index)
{
    AVFormatContext *ic = is->ic;
    AVCodecContext *enc;
    AVCodec *codec;
    int err;
    
    if (stream_index < 0 || stream_index >= ic->nb_streams)
        return -1;
    enc = ic->streams[stream_index]->codec;
    
    /* prepare audio output */
    if (enc->codec_type == CODEC_TYPE_AUDIO) {
        if (enc->channels > 0) {
            enc->request_channels = FFMIN(2, enc->channels);
        } else {
            enc->request_channels = 2;
        }
    }

    codec = avcodec_find_decoder(enc->codec_id);
    enc->debug_mv = debug_mv;
    enc->debug = debug;
    enc->workaround_bugs = workaround_bugs;
    enc->lowres = lowres;
    if(lowres) enc->flags |= CODEC_FLAG_EMU_EDGE;
    enc->idct_algo= idct;
    if(fast) enc->flags2 |= CODEC_FLAG2_FAST;
    enc->skip_frame= skip_frame;
    enc->skip_idct= skip_idct;
    enc->skip_loop_filter= skip_loop_filter;
    enc->error_recognition= error_recognition;
    enc->error_concealment= error_concealment;

//    set_context_opts(enc, avctx_opts[enc->codec_type], 0);
    
    if (!codec) {
        return -1;
    }
        
    err = avcodec_open(enc, codec);
    
    if (err < 0) {
        return -1;
    }
    
    is->audio_hw_buf_size = 2048;
    
    if(thread_count>1)
        avcodec_thread_init(enc, thread_count);
    enc->thread_count= thread_count;
    ic->streams[stream_index]->discard = AVDISCARD_DEFAULT;
    switch(enc->codec_type) {
    case CODEC_TYPE_AUDIO:
        is->audio_stream = stream_index;
        is->audio_st = ic->streams[stream_index];
        is->audio_buf_size = 0;
        is->audio_buf_index = 0;

        /* init averaging filter */
        is->audio_diff_avg_coef = exp(log(0.01) / AUDIO_DIFF_AVG_NB);
        is->audio_diff_avg_count = 0;
        /* since we do not have a precise anough audio fifo fullness,
           we correct audio sync only if larger than this threshold */
        is->audio_diff_threshold = 2.0 * SDL_AUDIO_BUFFER_SIZE / enc->sample_rate;

        memset(&is->audio_pkt, 0, sizeof(is->audio_pkt));
        packet_queue_init(&is->audioq);
        SDL_PauseAudio(0);
        break;
    case CODEC_TYPE_VIDEO:
        is->video_stream = stream_index;
        is->video_st = ic->streams[stream_index];

        is->frame_last_delay = 40e-3;
        is->frame_timer = (double)av_gettime() / 1000000.0;
        is->video_current_pts_time = av_gettime();

        packet_queue_init(&is->videoq);
        is->video_tid = SDL_CreateThread(video_thread, is);
        break;
    case CODEC_TYPE_SUBTITLE:
        is->subtitle_stream = stream_index;
        is->subtitle_st = ic->streams[stream_index];
        packet_queue_init(&is->subtitleq);

        is->subtitle_tid = SDL_CreateThread(subtitle_thread, is);
        break;
    default:
        break;
    }
    return 0;
}

static void stream_component_close(VideoState *is, int stream_index)
{
    AVFormatContext *ic = is->ic;
    AVCodecContext *enc;

    if (stream_index < 0 || stream_index >= ic->nb_streams)
        return;
    enc = ic->streams[stream_index]->codec;

    switch(enc->codec_type) {
    case CODEC_TYPE_AUDIO:
        packet_queue_abort(&is->audioq);
        packet_queue_end(&is->audioq);
        if (is->reformat_ctx)
            audio_resample_close(is->reformat_ctx);
        break;
    case CODEC_TYPE_VIDEO:
        packet_queue_abort(&is->videoq);

        /* note: we also signal this mutex to make sure we deblock the
           video thread in all cases */
        SDL_LockMutex(is->pictq_mutex);
        SDL_CondSignal(is->pictq_cond);
        SDL_UnlockMutex(is->pictq_mutex);

        SDL_WaitThread(is->video_tid, NULL);

        packet_queue_end(&is->videoq);
        break;
    case CODEC_TYPE_SUBTITLE:
        packet_queue_abort(&is->subtitleq);

        /* note: we also signal this mutex to make sure we deblock the
           video thread in all cases */
        SDL_LockMutex(is->subpq_mutex);
        is->subtitle_stream_changed = 1;

        SDL_CondSignal(is->subpq_cond);
        SDL_UnlockMutex(is->subpq_mutex);

        SDL_WaitThread(is->subtitle_tid, NULL);

        packet_queue_end(&is->subtitleq);
        break;
    default:
        break;
    }

    ic->streams[stream_index]->discard = AVDISCARD_ALL;

    SDL_LockMutex(codec_mutex);
    avcodec_close(enc);
    SDL_UnlockMutex(codec_mutex);
    
    switch(enc->codec_type) {
    case CODEC_TYPE_AUDIO:
        is->audio_st = NULL;
        is->audio_stream = -1;
        break;
    case CODEC_TYPE_VIDEO:
        is->video_st = NULL;
        is->video_stream = -1;
        break;
    case CODEC_TYPE_SUBTITLE:
        is->subtitle_st = NULL;
        is->subtitle_stream = -1;
        break;
    default:
        break;
    }
}

static void dump_stream_info(const AVFormatContext *s)
{
    AVMetadataTag *tag = NULL;
    while ((tag=av_metadata_get(s->metadata,"",tag,AV_METADATA_IGNORE_SUFFIX)))
        fprintf(stderr, "%s: %s\n", tag->key, tag->value);
}

#define PROBE_BUF_MIN 2048
#define PROBE_BUF_MAX (1<<20)

/* this thread gets the stream from the disk or the network */
static int decode_thread(void *arg)
{
    VideoState *is = arg;
    AVFormatContext *ic;
    int err, i, ret, video_index, audio_index, subtitle_index;
    AVPacket pkt1, *pkt = &pkt1;
    AVFormatParameters params, *ap = &params;
    AVProbeData probe_data, *pd = &probe_data;
    int probe_size;
    AVInputFormat *fmt = NULL;
    ByteIOContext *pb;
    int signalled_start = 0;
    int codecs_locked = 0;
    
    // url_set_interrupt_cb(decode_interrupt_cb);
    
    /* TODO: Set somehow. */
    pd->filename = is->filename;
    pd->buf = NULL;
    pd->buf_size = 0;
    
    video_index = -1;
    audio_index = -1;
    subtitle_index = -1;
    is->video_stream = -1;
    is->audio_stream = -1;
    is->subtitle_stream = -1;

    memset(ap, 0, sizeof(*ap));

    ap->width = frame_width;
    ap->height= frame_height;
    ap->time_base= (AVRational){1, 25};
    ap->pix_fmt = frame_pix_fmt;

    pb = is->io_context = rwops_open(is->rwops);

    codecs_locked = 1;
    SDL_LockMutex(codec_mutex);

    if (!fmt) {
        for(probe_size= PROBE_BUF_MIN; probe_size<=PROBE_BUF_MAX && !fmt; probe_size<<=1){

            /* read probe data */
            pd->buf= av_realloc(pd->buf, probe_size + AVPROBE_PADDING_SIZE);
            pd->buf_size = get_buffer(pb, pd->buf, probe_size);
            memset(pd->buf+pd->buf_size, 0, AVPROBE_PADDING_SIZE);

            /* Seek back to start. */
            if (url_fseek(pb, 0, SEEK_SET) < 0) {
                fprintf(stderr, "Could not seek in file.\n");
                goto fail;
            }

            /* guess file format */
            fmt = av_probe_input_format(pd, 1);
        }
        av_freep(&pd->buf);
    }

    if (!fmt) {
        fprintf(stderr, "Couldn't guess file format.\n");
        goto fail;
    }
        
    // err = av_open_input_file(&ic, "test.mkv", is->iformat, 0, ap);

    err = av_open_input_stream(
        &ic,
        is->io_context,
        is->filename,
        fmt,
        ap);

    // printf("Format name: %s\n", fmt->name);
    
    is->ic = ic;

    if (err < 0) {
        fprintf(stderr, "stream open error: %d\n", err);
        // print_error(is->filename, err);
        ret = -1;
        goto fail;
    }

    if(genpts)
        ic->flags |= AVFMT_FLAG_GENPTS;

    err = av_find_stream_info(ic);

    if (err < 0) {
        fprintf(stderr, "could not find codec parameters\n");
        ret = -1;
        goto fail;
    }
    if(ic->pb)
        ic->pb->eof_reached= 0; //FIXME hack, ffplay maybe should not
                                //use url_feof() to test for the end
    
    /* if seeking requested, we execute it */
    if (start_time != AV_NOPTS_VALUE) {
        int64_t timestamp;

        timestamp = start_time;
        /* add the stream start time */
        if (ic->start_time != AV_NOPTS_VALUE)
            timestamp += ic->start_time;
        ret = av_seek_frame(ic, -1, timestamp, AVSEEK_FLAG_BACKWARD);
        if (ret < 0) {
            fprintf(stderr, "could not seek to position %0.3f\n",
                    (double)timestamp / AV_TIME_BASE);
        }
    }

    for(i = 0; i < ic->nb_streams; i++) {
        AVCodecContext *enc = ic->streams[i]->codec;
        ic->streams[i]->discard = AVDISCARD_ALL;

        switch(enc->codec_type) {
        case CODEC_TYPE_AUDIO:
            /* if (wanted_audio_stream-- >= 0 && !audio_disable) */
            /*     audio_index = i; */
            audio_index = i;
            break;
        case CODEC_TYPE_VIDEO:
            /* if (wanted_video_stream-- >= 0 && !video_disable) */
            video_index = i;
            break;
        case CODEC_TYPE_SUBTITLE:
            /* if (wanted_subtitle_stream-- >= 0 && !video_disable) */
            /*     subtitle_index = i; */
            break;
        default:
            break;
        }
    }

    
    if (show_status) {
        dump_format(ic, 0, is->filename, 0);
        dump_stream_info(ic);
    }

    if (audio_index < 0) {
        printf("%s does not have an audio stream.\n", is->filename);
        ret = -1;
        goto fail;
    }

    /* open the streams */
    if (audio_index >= 0) {
        stream_component_open(is, audio_index);
    }

    if (video_index >= 0) {
        stream_component_open(is, video_index);
        /* add the refresh timer to draw the picture */
        schedule_refresh(is, 40);
    } else {
        is->show_audio = 0;
    }
    
    if (subtitle_index >= 0) {
        stream_component_open(is, subtitle_index);
    }

    signalled_start = 1;
    
    if (is->video_stream < 0 && is->audio_stream < 0) {
        fprintf(stderr, "could not open codecs\n");
        ret = -1;
        goto fail;
    }

    is->started = 1;

    // Compute the number of samples we need to play back.
    {
        long long duration = ((long long) is->ic->duration) * audio_sample_rate;
        is->audio_duration = (unsigned int) (duration /  AV_TIME_BASE);

        if (show_status) {
            printf("Duration of '%s' is %d samples.\n", is->filename, is->audio_duration);
        }
    }

    
    SDL_UnlockMutex(codec_mutex);
    codecs_locked = 0;
    
    for(;;) {

        if (is->abort_request) {
            break;
        }
            
        /* if (is->paused != is->last_paused) { */
        /*     is->last_paused = is->paused; */
        /*     if (is->paused) */
        /*         av_read_pause(ic); */
        /*     else */
        /*         av_read_play(ic); */
        /* } */

        /* if (is->seek_req) { */
        /*     int stream_index= -1; */
        /*     int64_t seek_target= is->seek_pos; */

        /*     if     (is->   video_stream >= 0) stream_index= is->   video_stream; */
        /*     else if(is->   audio_stream >= 0) stream_index= is->   audio_stream; */
        /*     else if(is->subtitle_stream >= 0) stream_index= is->subtitle_stream; */

        /*     if(stream_index>=0){ */
        /*         seek_target= av_rescale_q(seek_target, AV_TIME_BASE_Q, ic->streams[stream_index]->time_base); */
        /*     } */

        /*     ret = av_seek_frame(is->ic, stream_index, seek_target, is->seek_flags); */
        /*     if (ret < 0) { */
        /*         fprintf(stderr, "%s: error while seeking\n", is->ic->filename); */
        /*     }else{ */
        /*         if (is->audio_stream >= 0) { */
        /*             packet_queue_flush(&is->audioq); */
        /*             packet_queue_put(&is->audioq, &flush_pkt); */
        /*         } */
        /*         if (is->subtitle_stream >= 0) { */
        /*             packet_queue_flush(&is->subtitleq); */
        /*             packet_queue_put(&is->subtitleq, &flush_pkt); */
        /*         } */
        /*         if (is->video_stream >= 0) { */
        /*             packet_queue_flush(&is->videoq); */
        /*             packet_queue_put(&is->videoq, &flush_pkt); */
        /*         } */
        /*     } */
        /*     is->seek_req = 0; */
        /* } */

        /* if the queue are full, no need to read more */
        if (is->audioq.size > MAX_AUDIOQ_SIZE ||
            is->videoq.size > MAX_VIDEOQ_SIZE ||
            is->subtitleq.size > MAX_SUBTITLEQ_SIZE) {
            
            /* wait 10 ms - or wait for quit notify.*/
            SDL_LockMutex(is->quit_mutex);
            SDL_CondWaitTimeout(is->quit_cond, is->quit_mutex, 10);
            SDL_UnlockMutex(is->quit_mutex);

            continue;
        }

        if(url_feof(ic->pb)) {
            goto eof;
        }

        ret = av_read_frame(ic, pkt);
        if (ret < 0) {
            // Treat errors like end of stream.
            goto eof;
        }

        if (pkt->stream_index == is->audio_stream) {
            packet_queue_put(&is->audioq, pkt);
        } else if (pkt->stream_index == is->video_stream) {
            packet_queue_put(&is->videoq, pkt);
        } else if (pkt->stream_index == is->subtitle_stream) {
            packet_queue_put(&is->subtitleq, pkt);
        } else {
            av_free_packet(pkt);
        }
    }

eof:
    
    /* Request the end of the audio queue when we have no more
       bytes to decode. */
    if (is->audio_st) {
        SDL_LockMutex(is->audioq.mutex);
        is->audioq.end_request = 1;
        SDL_CondSignal(is->audioq.cond);
        SDL_UnlockMutex(is->audioq.mutex);
    }

    /* wait until we're notified it's safe to abort. */
    SDL_LockMutex(is->quit_mutex);
    while (!is->abort_request) {
        SDL_CondWait(is->quit_cond, is->quit_mutex);
    }
    SDL_UnlockMutex(is->quit_mutex);

    ret = 0;

fail:

    is->finished = 1;

   if (codecs_locked) {
        SDL_UnlockMutex(codec_mutex);
        codecs_locked = 0;
    }
        
    /* close each stream */
    if (is->audio_stream >= 0)
        stream_component_close(is, is->audio_stream);
    if (is->video_stream >= 0)
        stream_component_close(is, is->video_stream);
    if (is->subtitle_stream >= 0)
        stream_component_close(is, is->subtitle_stream);

    if (is->ic) {
        av_close_input_stream(is->ic);
        is->ic = NULL; /* safety */
    }
        
    is->audio_stream = -1;
    is->video_stream = -1;
    is->subtitle_stream = -1;

    av_free(is->io_context->buffer);
    av_free(is->io_context);
    rwops_close(is->rwops);
    
    return 0;
}

VideoState *ffpy_stream_open(SDL_RWops *rwops, const char *filename)
{
    VideoState *is;

    is = av_mallocz(sizeof(VideoState));
    if (!is)
        return NULL;

    is->filename = strdup(filename);
    is->rwops = rwops;
    
    is->iformat = NULL;
    is->ytop = 0;
    is->xleft = 0;

    /* start video display */
    is->pictq_mutex = SDL_CreateMutex();
    is->pictq_cond = SDL_CreateCond();

    is->subpq_mutex = SDL_CreateMutex();
    is->subpq_cond = SDL_CreateCond();

    is->av_sync_type = av_sync_type;

    is->quit_mutex = SDL_CreateMutex();
    is->quit_cond = SDL_CreateCond();
    
    is->parse_tid = SDL_CreateThread(decode_thread, is);

    if (!is->parse_tid) {
        av_free(is);
        return NULL;
    }

    return is;
}

void ffpy_stream_close(VideoState *is)
{
    VideoPicture *vp;
    int i;

    is->abort_request = 1;
    SDL_LockMutex(is->quit_mutex);
    SDL_CondSignal(is->quit_cond);
    SDL_UnlockMutex(is->quit_mutex);
    SDL_WaitThread(is->parse_tid, NULL);

    /* free all pictures */
    for(i=0;i<VIDEO_PICTURE_QUEUE_SIZE; i++) {
        vp = &is->pictq[i];
        if (vp->bmp) {
            SDL_FreeYUVOverlay(vp->bmp);
            vp->bmp = NULL;
        }
    }
    
    SDL_DestroyMutex(is->pictq_mutex);
    SDL_DestroyCond(is->pictq_cond);
    SDL_DestroyMutex(is->subpq_mutex);
    SDL_DestroyCond(is->subpq_cond);
    SDL_DestroyMutex(is->quit_mutex);
    SDL_DestroyCond(is->quit_cond);
    
    free(is->filename);
    av_free(is);
}

void ffpy_alloc_event(VideoState *vs, PyObject *surface) {
    alloc_picture(vs, surface);
}

void ffpy_refresh_event(VideoState *vs) {
    video_refresh_timer(vs);
}

int ffpy_did_init = 0;

/* Called from the main */
void ffpy_init(int rate, int status) {

    if (ffpy_did_init) {
        return;
    }

    ffpy_did_init = 1;

    show_status = status;
    
    audio_sample_rate = rate;
    
    /* register all codecs, demux and protocols */
    avcodec_register_all();
    av_register_all();

    if (status) {
        av_log_set_level(AV_LOG_INFO);
    } else {
        av_log_set_level(AV_LOG_ERROR);
    }
        
    av_init_packet(&flush_pkt);
    flush_pkt.data = (unsigned char *) "FLUSH";

    if (!codec_mutex) {
        codec_mutex = SDL_CreateMutex();
    }
}


