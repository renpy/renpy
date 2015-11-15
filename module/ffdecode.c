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

#include <math.h>
#include <limits.h>
#include <libavutil/avstring.h>
#include <libavutil/time.h>
#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libswscale/swscale.h>

#ifdef HAS_RESAMPLE
#include <libavutil/opt.h>
#include <libavresample/avresample.h>
#endif

#include <SDL.h>
#include <SDL_thread.h>

#include <pygame_sdl2/pygame_sdl2.h>

#ifdef __MINGW32__
#undef main /* We don't want SDL to override our main() */
#endif

#undef exit

#define MIN_AUDIOQ_SIZE (20 * 16 * 1024)
#define MIN_FRAMES 5

/* SDL audio buffer size, in samples. Should be small to have precise
   A/V sync as SDL does not have hardware buffer fullness info. */
#define SDL_AUDIO_BUFFER_SIZE 2048

/* NOTE: the size must be big enough to compensate the hardware audio buffersize size */
#define SAMPLE_ARRAY_SIZE (2*65536)

AVCodecContext *avctx_opts[AVMEDIA_TYPE_NB];
AVFormatContext *avformat_opts;

static int sws_flags = SWS_BILINEAR;

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

typedef struct VideoPicture {
    double pts;                                  ///<presentation time stamp for this picture
    SDL_Surface *surf;
    AVFrame *frame;
    int fmt;
    int width, height; /* source height & width */
    int allocated;
} VideoPicture;

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

    double audio_clock;
    AVStream *audio_st;
    PacketQueue audioq;
    int audio_hw_buf_size;
    /* samples output by the codec. we reserve more space for avsync
       compensation */

#ifndef HAS_RESAMPLE
    uint8_t audio_buf1[(AVCODEC_MAX_AUDIO_FRAME_SIZE * 3) / 2] __attribute__ ((aligned (16))) ;
    uint8_t audio_buf2[(AVCODEC_MAX_AUDIO_FRAME_SIZE * 3) / 2] __attribute__ ((aligned (16))) ;
#else
    uint8_t *audio_buf1;
#endif
    uint8_t *audio_buf;

    unsigned int audio_buf_size; /* in bytes */

    int audio_buf_index; /* in bytes */
    AVPacket audio_pkt;
    AVPacket audio_pkt_temp;

    // AVAudioConvert *reformat_ctx;
#ifndef HAS_RESAMPLE
    ReSampleContext *reformat_ctx;
#endif
    int resample_frac;

    int show_audio; /* if true, display audio samples */
    int16_t sample_array[SAMPLE_ARRAY_SIZE];
    int sample_array_index;
    int last_i_start;


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
    AVIOContext *io_context;

    int width, height, xleft, ytop;

    double audio_callback_time;

    char *filename;

    // Have we initialized fully?
    volatile int started;

    // Have we finished decoding?
    volatile int finished;

    // The audio duration.
    unsigned int audio_duration;

    // The amount of audio we've played, in samples.
    unsigned int audio_played;

    double start_time;

    // Should we force the display of the current video frame?
    int first_frame;

    // The PTS of the first frame.
    double first_frame_pts;

    // Is the is the first audio?
    int first_audio;

    // The PTS of the first audio.
    double first_audio_clock;

#ifdef HAS_RESAMPLE
    // The audio frame, and the audio resample context.
    enum AVSampleFormat sdl_sample_fmt;
    uint64_t sdl_channel_layout;
    int sdl_channels;
    int sdl_sample_rate;
    enum AVSampleFormat resample_sample_fmt;
    uint64_t resample_channel_layout;
    int resample_sample_rate;
    AVAudioResampleContext *avr;
    AVFrame *frame;
#endif

} VideoState;

SDL_mutex *codec_mutex = NULL;

static int audio_write_get_buf_size(VideoState *is);

int ffpy_needs_alloc = 0;
int ffpy_movie_width = 64;
int ffpy_movie_height = 64;

/* options specified by the user */
static int show_status;
static int64_t start_time = AV_NOPTS_VALUE;
static int debug = 0;
static int debug_mv = 0;
static int workaround_bugs = 1;
static int fast = 0;
static int genpts = 0;
static int idct = FF_IDCT_AUTO;
static enum AVDiscard skip_frame= AVDISCARD_DEFAULT;
static enum AVDiscard skip_idct= AVDISCARD_DEFAULT;
static enum AVDiscard skip_loop_filter= AVDISCARD_DEFAULT;
static int error_concealment = 3;
static int decoder_reorder_pts= 0;

static AVPacket flush_pkt;

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

    if (whence == AVSEEK_SIZE) {
    	return rw->size(rw);
    }

    // Ignore flags like AVSEEK_FORCE.
    whence &= (SEEK_SET | SEEK_CUR | SEEK_END);

    int64_t rv = rw->seek(rw, (int) offset, whence);
    return rv;
}

#define RWOPS_BUFFER 65536

static AVIOContext *rwops_open(SDL_RWops *rw) {

    unsigned char *buffer = av_malloc(RWOPS_BUFFER);
    AVIOContext *rv = avio_alloc_context(
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

static double get_time(void) {
	return av_gettime() * 1e-6;
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

static void video_image_display(VideoState *is)
{
    VideoPicture *vp;

    AVPicture pict;
    float aspect_ratio;
    int width, height, x, y;
    SDL_Rect rect;

    static struct SwsContext *img_convert_ctx;

    vp = &is->pictq[is->pictq_rindex];
    if (vp->surf) {
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

        img_convert_ctx = sws_getCachedContext(
            img_convert_ctx,
            is->video_st->codec->width,
            is->video_st->codec->height,
            is->video_st->codec->pix_fmt,
            rect.w,
            rect.h,
            vp->fmt, //dst_pix_fmt,
            sws_flags,
            NULL, NULL, NULL);

        if (img_convert_ctx != NULL) {

            pict.data[0] = &((uint8_t *)vp->surf->pixels)[rect.y * vp->surf->pitch + rect.x * 4];
            pict.linesize[0] = vp->surf->pitch;

            sws_scale(
                img_convert_ctx,
                (const uint8_t * const *) vp->frame->data,
                vp->frame->linesize,
                0,
                is->video_st->codec->height,
                pict.data,
                pict.linesize);
        }

    } else {
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

/* get the current audio clock value. If adjust is 1, also adjusts the
 * offset. */
static double get_audio_clock(VideoState *is, int adjust)
{
	double now;
    double pts;
    double altpts;
    double offset;
    int hw_buf_size, bytes_per_sec;
    pts = is->audio_clock - is->first_audio_clock;
    hw_buf_size = audio_write_get_buf_size(is);
    bytes_per_sec = 0;
    if (is->audio_st) {
        bytes_per_sec = is->audio_st->codec->sample_rate *
            2 * is->audio_st->codec->channels;
    }
    if (bytes_per_sec)
        pts -= (double)hw_buf_size / bytes_per_sec;

    now = get_time();

    if (is->audio_callback_time == 0) {
    	is->audio_callback_time = now;
    }

    if (is->start_time == 0) {
    	is->start_time = now;
    }

    pts += (now - is->audio_callback_time);
    altpts = now - is->start_time;
    offset = altpts - pts;

    if (fabs(offset) > .25) {
    	is->start_time = now - pts;
    	altpts = pts;
    }

    if (adjust) {
    	if (offset > 0) {
			is->start_time += .00025;
		} else {
			is->start_time -= .00025;
		}
    }

    return altpts;
}

/* called to display each frame */
static int video_refresh(void *opaque)
{
    VideoState *is = opaque;
    VideoPicture *vp;

    double delay;

    if (!is->video_st) {
    	return 0;
    }

    while (1) {

    	if (is->pictq_size == 0) {
    		return 0;
        }

		/* dequeue the picture */
		vp = &is->pictq[is->pictq_rindex];

		/* update current video pts */
		is->video_current_pts = vp->pts;
		is->video_current_pts_time = av_gettime();

		if (is->first_frame) {
			is->first_frame_pts = vp->pts;
		}

		delay = get_audio_clock(is, 0) - (vp->pts - is->first_frame_pts);

		/* The video is ahead of the audio. */
		if (delay < 0 && !is->first_frame) {
			return 0;
		}
		// Adjust the audio clock.
		get_audio_clock(is, 1);

		if (delay < .1 || is->first_frame) {
			video_display(is);
		}

		is->first_frame = 0;

		av_free(vp->frame);
		vp->frame = NULL;

		/* update queue size and signal for next picture */
		if (++is->pictq_rindex == VIDEO_PICTURE_QUEUE_SIZE)
			is->pictq_rindex = 0;

		SDL_LockMutex(is->pictq_mutex);
		is->pictq_size--;
		SDL_CondSignal(is->pictq_cond);
		SDL_UnlockMutex(is->pictq_mutex);

		return 1;
    }
}

/* allocate a picture (needs to do that in main thread to avoid
   potential locking problems */
static void alloc_picture(void *opaque, PyObject *pysurf)
{
    VideoState *is = opaque;
    VideoPicture *vp;
    SDL_Surface *surf;

    uint32_t pixel;
    uint8_t *bytes = (uint8_t *) &pixel;

    SDL_LockMutex(is->pictq_mutex);

    if (!ffpy_needs_alloc) {
    	SDL_UnlockMutex(is->pictq_mutex);
    	return;
    }

    if (! is->video_st) {
        SDL_UnlockMutex(is->pictq_mutex);
        return;
    }

    ffpy_needs_alloc = 0;

    surf = PySurface_AsSurface(pysurf);
    is->width = surf->w;
    is->height = surf->h;

    vp = &is->pictq[is->pictq_windex];
    vp->surf = surf;
    vp->width = is->video_st->codec->width;
    vp->height = is->video_st->codec->height;

    pixel = SDL_MapRGBA(surf->format, 1, 2, 3, 4);
    if (bytes[0] == 4 && bytes[1] == 1) {
        vp->fmt = PIX_FMT_ARGB;
    } else if (bytes[0] == 4 && bytes[1] == 3) {
        vp->fmt = PIX_FMT_ABGR;
    } else if (bytes[0] == 1) {
        vp->fmt = PIX_FMT_RGBA;
    } else {
        vp->fmt = PIX_FMT_BGRA;
    }

    pixel = SDL_MapRGBA(surf->format, 0, 0, 0, 255);
    SDL_FillRect(surf, NULL, pixel);

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

#if 0
    int dst_pix_fmt;
    AVPicture pict;
    static struct SwsContext *img_convert_ctx;
#endif

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
    if (!vp->surf ||
        vp->width != is->video_st->codec->width ||
        vp->height != is->video_st->codec->height) {

    	SDL_LockMutex(is->pictq_mutex);

        vp->allocated = 0;

        ffpy_movie_width = is->video_st->codec->width;
        ffpy_movie_height = is->video_st->codec->height;

        ffpy_needs_alloc = 1;

        /* wait until the picture is allocated */
        while (!vp->allocated && !is->videoq.abort_request) {
        	SDL_CondWait(is->pictq_cond, is->pictq_mutex);
        }
        SDL_UnlockMutex(is->pictq_mutex);

        if (is->videoq.abort_request)
            return -1;
    }

    vp->frame = src_frame;
    vp->pts = pts;

    /* now we can update the picture count */
    if (++is->pictq_windex == VIDEO_PICTURE_QUEUE_SIZE)
        is->pictq_windex = 0;
    SDL_LockMutex(is->pictq_mutex);
    is->pictq_size++;
    SDL_UnlockMutex(is->pictq_mutex);

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
    int got_picture;
    AVFrame *frame;
    double pts;

    for(;;) {
        frame = avcodec_alloc_frame();

        while (is->paused && !is->videoq.abort_request) {
            SDL_Delay(2);
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

        avcodec_decode_video2(is->video_st->codec,
								frame, &got_picture,
								pkt);

        if(   (decoder_reorder_pts || pkt->dts == AV_NOPTS_VALUE)
           && frame->reordered_opaque != AV_NOPTS_VALUE)
            pts= frame->reordered_opaque;
        else if(pkt->dts != AV_NOPTS_VALUE)
            pts= pkt->dts;
        else
            pts= 0;
        pts *= av_q2d(is->video_st->time_base);

        if (got_picture) {
            if (output_picture2(is, frame, pts) < 0)
                goto the_end;
        }

        av_free_packet(pkt);
    }
 the_end:
    return 0;
}

#ifdef HAS_RESAMPLE

/* decode one audio frame and returns its uncompressed size */
static int audio_decode_frame(VideoState *is, double *pts_ptr)
{
    AVPacket *pkt_temp = &is->audio_pkt_temp;
    AVPacket *pkt = &is->audio_pkt;
    AVCodecContext *dec = is->audio_st->codec;
    int n, len1, data_size, got_frame;
    double pts;
    int new_packet = 0;
    int flush_complete = 0;

    for (;;) {
        /* NOTE: the audio packet can contain several frames */
        while (pkt_temp->size > 0 || (!pkt_temp->data && new_packet)) {
            int resample_changed, audio_resample;

            if (!is->frame) {
                if (!(is->frame = avcodec_alloc_frame()))
                    return AVERROR(ENOMEM);
            } else
                avcodec_get_frame_defaults(is->frame);

            if (flush_complete)
                break;
            new_packet = 0;
            len1 = avcodec_decode_audio4(dec, is->frame, &got_frame, pkt_temp);
            if (len1 < 0) {
                /* if error, we skip the frame */
                pkt_temp->size = 0;
                break;
            }

            pkt_temp->data += len1;
            pkt_temp->size -= len1;

            if (!got_frame) {
                /* stop sending empty packets if the decoder is finished */
                if (!pkt_temp->data && dec->codec->capabilities & CODEC_CAP_DELAY)
                    flush_complete = 1;
                continue;
            }
            data_size = av_samples_get_buffer_size(NULL, dec->channels,
                                                   is->frame->nb_samples,
                                                   is->frame->format, 1);

            audio_resample = is->frame->format         != is->sdl_sample_fmt     ||
                             is->frame->channel_layout != is->sdl_channel_layout ||
                             is->frame->sample_rate    != is->sdl_sample_rate;

            resample_changed = is->frame->format         != is->resample_sample_fmt     ||
                               is->frame->channel_layout != is->resample_channel_layout ||
                               is->frame->sample_rate    != is->resample_sample_rate;

            if ((!is->avr && audio_resample) || resample_changed) {
                int ret;
                if (is->avr)
                    avresample_close(is->avr);
                else if (audio_resample) {
                    is->avr = avresample_alloc_context();
                    if (!is->avr) {
                        fprintf(stderr, "error allocating AVAudioResampleContext\n");
                        break;
                    }
                }
                if (audio_resample) {
                    av_opt_set_int(is->avr, "in_channel_layout",  is->frame->channel_layout, 0);
                    av_opt_set_int(is->avr, "in_sample_fmt",      is->frame->format,         0);
                    av_opt_set_int(is->avr, "in_sample_rate",     is->frame->sample_rate,    0);
                    av_opt_set_int(is->avr, "out_channel_layout", is->sdl_channel_layout,    0);
                    av_opt_set_int(is->avr, "out_sample_fmt",     is->sdl_sample_fmt,        0);
                    av_opt_set_int(is->avr, "out_sample_rate",    is->sdl_sample_rate,       0);

                    if ((ret = avresample_open(is->avr)) < 0) {
                        fprintf(stderr, "error initializing libavresample\n");
                        break;
                    }
                }
                is->resample_sample_fmt     = is->frame->format;
                is->resample_channel_layout = is->frame->channel_layout;
                is->resample_sample_rate    = is->frame->sample_rate;
            }

            if (audio_resample) {
                void *tmp_out;
                int out_samples, out_size, out_linesize;
                int osize      = av_get_bytes_per_sample(is->sdl_sample_fmt);
                int nb_samples = is->frame->nb_samples;

                int max_samples = 2 * (avresample_get_delay(is->avr) + nb_samples) * is->sdl_sample_rate / is->frame->sample_rate;


                out_size = av_samples_get_buffer_size(
                		&out_linesize,
                		is->sdl_channels,
                		max_samples,
                		is->sdl_sample_fmt, 0);

                tmp_out = av_realloc(is->audio_buf1, out_size);

                if (!tmp_out)
                    return AVERROR(ENOMEM);

                is->audio_buf1 = tmp_out;

                out_samples = avresample_convert(is->avr,
                                                 &is->audio_buf1,
                                                 out_linesize, max_samples,
                                                 is->frame->data,
                                                 is->frame->linesize[0],
                                                 is->frame->nb_samples);

                if (out_samples < 0) {
                    fprintf(stderr, "avresample_convert() failed\n");
                    break;
                }
                is->audio_buf = is->audio_buf1;
                data_size = out_samples * osize * is->sdl_channels;
            } else {
                is->audio_buf = is->frame->data[0];
            }

            /* if no pts, then compute it */
            pts = is->audio_clock;
            *pts_ptr = pts;
            n = is->sdl_channels * av_get_bytes_per_sample(is->sdl_sample_fmt);
            is->audio_clock += (double)data_size /
                (double)(n * is->sdl_sample_rate);

            // This is Ren'Py specific code, to deal with ogg files with
            // more data than their duration.
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
        memset(pkt_temp, 0, sizeof(*pkt_temp));

        if (is->paused || is->audioq.abort_request) {
            return -1;
        }

        /* read next packet */
        if ((new_packet = packet_queue_get(&is->audioq, pkt, 1)) < 0)
            return -1;

        if (pkt->data == flush_pkt.data) {
            avcodec_flush_buffers(dec);
            flush_complete = 0;
        }

        *pkt_temp = *pkt;

        /* if update the audio clock with the pts */
        if (pkt->pts != AV_NOPTS_VALUE) {
            is->audio_clock = av_q2d(is->audio_st->time_base)*pkt->pts;

            if (is->first_audio) {
            	is->first_audio_clock = is->audio_clock;
            	is->first_audio = 0;
            }
        }
    }
}

#else

/* decode one audio frame and returns its uncompressed size */
static int audio_decode_frame(VideoState *is, double *pts_ptr)
{
	AVPacket *pkt = &is->audio_pkt;
	AVPacket *pkt_temp = &is->audio_pkt_temp;
	AVCodecContext *dec= is->audio_st->codec;
    int len1, data_size;
    double pts;

    for(;;) {
        /* NOTE: the audio packet can contain several frames */
        while (pkt_temp->size > 0) {
            data_size = sizeof(is->audio_buf1);

            len1 = avcodec_decode_audio3(dec,
                                        (int16_t *)is->audio_buf1, &data_size,
                                        pkt_temp);

            if (len1 < 0) {
                /* if error, we skip the frame */
                pkt_temp->size = 0;
                break;
            }

            pkt_temp->data += len1;
            pkt_temp->size -= len1;

            if (data_size <= 0)
                continue;

            if (!is->reformat_ctx &&
                (dec->channels != 2 || dec->sample_fmt != AV_SAMPLE_FMT_S16)) {

                is->reformat_ctx = av_audio_resample_init(
                    2,
                    dec->channels,
                    // audio_sample_rate,
                    dec->sample_rate,
                    dec->sample_rate,
                    AV_SAMPLE_FMT_S16,
                    dec->sample_fmt,
                    1, 0, 0, 1.0);

                // Setting the last four parameters to 16, 0, 0, 1.0
                // gives better performance when the rate is less than
                // audio_sample_rate / 2, at the cost of some
                // performance. Probably not worth it - Tom.
            }

            // Moved by tom, from below next block. Is this right?


            if (is->reformat_ctx) {

                int len = data_size / av_get_bytes_per_sample(dec->sample_fmt);
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

        pkt_temp->data = pkt->data;
        pkt_temp->size = pkt->size;

        /* if update the audio clock with the pts */
        if (pkt->pts != AV_NOPTS_VALUE) {
            is->audio_clock = av_q2d(is->audio_st->time_base)*pkt->pts;
        }
    }
}

#endif


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

    is->audio_callback_time = get_time();

    while (len > 0) {
        if (is->audio_buf_index >= is->audio_buf_size) {

            audio_size = audio_decode_frame(is, &pts);

            if (audio_size < 0) {
                /* Nothing left to decode, break. */
                break;
            } else {
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
    if (enc->codec_type == AVMEDIA_TYPE_AUDIO) {
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
    enc->idct_algo= idct;
    if(fast) enc->flags2 |= CODEC_FLAG2_FAST;
    enc->skip_frame= skip_frame;
    enc->skip_idct= skip_idct;
    enc->skip_loop_filter= skip_loop_filter;
    enc->error_concealment= error_concealment;

//    set_context_opts(enc, avctx_opts[enc->codec_type], 0);

    if (!codec) {
        return -1;
    }

    err = avcodec_open2(enc, codec, NULL);

    if (err < 0) {
        return -1;
    }

    is->audio_hw_buf_size = 2048;

    ic->streams[stream_index]->discard = AVDISCARD_DEFAULT;
    switch(enc->codec_type) {
    case AVMEDIA_TYPE_AUDIO:
        is->audio_stream = stream_index;
        is->audio_st = ic->streams[stream_index];
        is->audio_buf_size = 0;
        is->audio_buf_index = 0;

#ifdef HAS_RESAMPLE
        if (!enc->channel_layout)
            enc->channel_layout = av_get_default_channel_layout(enc->channels);
        if (!enc->channel_layout) {
            fprintf(stderr, "%s: unable to guess channel layout\n", is->filename);
            return -1;
        }

        is->sdl_sample_rate = audio_sample_rate;
		is->sdl_channel_layout = AV_CH_LAYOUT_STEREO;
        is->sdl_channels = av_get_channel_layout_nb_channels(is->sdl_channel_layout);
        is->sdl_sample_fmt = AV_SAMPLE_FMT_S16;
#endif

        memset(&is->audio_pkt, 0, sizeof(is->audio_pkt));
        packet_queue_init(&is->audioq);
        break;
    case AVMEDIA_TYPE_VIDEO:
        is->video_stream = stream_index;
        is->video_st = ic->streams[stream_index];

        is->frame_last_delay = 40e-3;
        is->frame_timer = (double)av_gettime() / 1000000.0;
        is->video_current_pts_time = av_gettime();

        packet_queue_init(&is->videoq);
        is->video_tid = SDL_CreateThread(video_thread, "video_thread", is);
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
    case AVMEDIA_TYPE_AUDIO:
        packet_queue_abort(&is->audioq);
        packet_queue_end(&is->audioq);
#ifndef HAS_RESAMPLE
        if (is->reformat_ctx)
            audio_resample_close(is->reformat_ctx);
#endif
        break;
    case AVMEDIA_TYPE_VIDEO:
        packet_queue_abort(&is->videoq);

        /* note: we also signal this mutex to make sure we deblock the
           video thread in all cases */
        SDL_LockMutex(is->pictq_mutex);
        SDL_CondSignal(is->pictq_cond);
        SDL_UnlockMutex(is->pictq_mutex);

        SDL_WaitThread(is->video_tid, NULL);

        packet_queue_end(&is->videoq);
        break;
    default:
        break;
    }

    ic->streams[stream_index]->discard = AVDISCARD_ALL;

    SDL_LockMutex(codec_mutex);
    avcodec_close(enc);
    SDL_UnlockMutex(codec_mutex);

    switch(enc->codec_type) {
    case AVMEDIA_TYPE_AUDIO:
        is->audio_st = NULL;
        is->audio_stream = -1;
        break;
    case AVMEDIA_TYPE_VIDEO:
        is->video_st = NULL;
        is->video_stream = -1;
        break;
    default:
        break;
    }
}

#define PROBE_BUF_MIN 2048
#define PROBE_BUF_MAX (1<<20)

/* this thread gets the stream from the disk or the network */
static int decode_thread(void *arg)
{
    VideoState *is = arg;
    AVFormatContext *ic;
    int err, i, ret, video_index, audio_index;
    AVPacket pkt1, *pkt = &pkt1;
    int codecs_locked = 0;

    // url_set_interrupt_cb(decode_interrupt_cb);

    video_index = -1;
    audio_index = -1;
    is->video_stream = -1;
    is->audio_stream = -1;

    is->io_context = rwops_open(is->rwops);

    codecs_locked = 1;
    SDL_LockMutex(codec_mutex);

    ic = avformat_alloc_context();

    if (!ic) {
    	fprintf(stderr, "could not allocate context\n");
    	ret = -1;
    	goto fail;
    }

    ic->pb = is->io_context;

    err = avformat_open_input(
        &ic,
        is->filename,
        NULL,
        NULL);

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

    err = avformat_find_stream_info(ic, NULL);

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
        case AVMEDIA_TYPE_AUDIO:
            /* if (wanted_audio_stream-- >= 0 && !audio_disable) */
            /*     audio_index = i; */
            audio_index = i;
            break;
        case AVMEDIA_TYPE_VIDEO:
            /* if (wanted_video_stream-- >= 0 && !video_disable) */
            video_index = i;
            break;
        default:
            break;
        }
    }


    if (show_status) {
        av_dump_format(ic, 0, is->filename, 0);
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
    } else {
        is->show_audio = 0;
    }

    if (is->audio_stream < 0) {
    	printf("%s audio stream could not be opened.\n", is->filename);
    	ret = -1;
        goto fail;
    }

    // Compute the number of samples we need to play back.
    {
        long long duration = ((long long) is->ic->duration) * audio_sample_rate;
        is->audio_duration = (unsigned int) (duration /  AV_TIME_BASE);

        // Check that the duration is reasonable (between 0s and 3600s). If not,
        // reject it.
        if (is->audio_duration < 0 || is->audio_duration > 3600 * audio_sample_rate) {
        	is->audio_duration = 0;
        }

        if (show_status) {
            printf("Duration of '%s' is %d samples.\n", is->filename, is->audio_duration);
        }
    }


    SDL_UnlockMutex(codec_mutex);
    codecs_locked = 0;

    is->started = 1;

    for(;;) {

        if (is->abort_request) {
            break;
        }

        /* if the queue are full, no need to read more */
        if ((is->audioq.size > MIN_AUDIOQ_SIZE || is->audio_stream < 0) &&
        	(is->videoq.nb_packets > MIN_FRAMES || is->video_stream < 0)) {

        	/* wait 2 ms - or wait for quit notify.*/
            SDL_LockMutex(is->quit_mutex);
            SDL_CondWaitTimeout(is->quit_cond, is->quit_mutex, 2);
            SDL_UnlockMutex(is->quit_mutex);

            continue;
        }

        ret = av_read_frame(ic, pkt);
        if (ret < 0) {
        	// End of stream and other errors.
        	goto eof;
        }

        if (pkt->stream_index == is->audio_stream) {
            packet_queue_put(&is->audioq, pkt);
        } else if (pkt->stream_index == is->video_stream) {
            packet_queue_put(&is->videoq, pkt);
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
    if (is->ic) {
    	avformat_close_input(&(is->ic));
    	is->ic = NULL;
    }

    is->audio_stream = -1;
    is->video_stream = -1;

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

    is->quit_mutex = SDL_CreateMutex();
    is->quit_cond = SDL_CreateCond();

    is->parse_tid = SDL_CreateThread(decode_thread, "decode_thread", is);

    is->first_frame = 1;
    is->first_audio = 1;

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
    for(i=0; i<VIDEO_PICTURE_QUEUE_SIZE; i++) {
        vp = &is->pictq[i];
        if (vp->frame) {
            av_free(vp->frame);
        }
    }

    SDL_DestroyMutex(is->pictq_mutex);
    SDL_DestroyCond(is->pictq_cond);
    SDL_DestroyMutex(is->quit_mutex);
    SDL_DestroyCond(is->quit_cond);

    free(is->filename);
    av_free(is);
}

void ffpy_alloc_event(VideoState *vs, PyObject *surface) {
    alloc_picture(vs, surface);
}

int ffpy_refresh_event(VideoState *vs) {
    return video_refresh(vs);
}

int ffpy_did_init = 0;

/* Called from the main */
void ffpy_init(int rate, int status) {

    if (ffpy_did_init) {
        return;
    }

    ffpy_did_init = 1;

    import_pygame_sdl2();

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


