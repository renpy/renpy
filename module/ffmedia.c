#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libswresample/swresample.h>
#include <libavutil/time.h>
#include <libavutil/pixfmt.h>
#include <libswscale/swscale.h>

#include <SDL.h>
#include <SDL_thread.h>

#include <stdlib.h>

#ifndef _WIN32
#define USE_POSIX_MEMALIGN
#endif

/* Should a mono channel be split into two equal stero channels (true) or
 * should the energy be split onto two stereo channels with 1/2 the energy
 * (false).
 */
static int audio_equal_mono = 1;

/* The weight of stereo channels when audio_equal_mono is true. */
static double stereo_matrix[] = { 1.0, 1.0 };

/* The output audio sample rate. */
static int audio_sample_rate = 44100;

static int audio_sample_increase = 44100 / 5;
static int audio_target_samples = 44100 * 2;

const int CHANNELS = 2;
const int BPC = 2; // Bytes per channel.
const int BPS = 4; // Bytes per sample.

const int FRAMES = 3;

// The alignment of each row of pixels.
const int ROW_ALIGNMENT = 16;

// The number of pixels on each side. This has to be greater that 0 (since
// Ren'Py needs some padding), FRAME_PADDING * BPS has to be a multiple of
// 16 (alignment issues on ARM NEON), and has to match the crop in the
// read_video function of renpysound.pyx.
const int FRAME_PADDING = ROW_ALIGNMENT / 4;

const int SPEED = 1;

// How many seconds early can frames be delivered?
static const double frame_early_delivery = .005;

static SDL_Surface *rgb_surface = NULL;
static SDL_Surface *rgba_surface = NULL;

// http://dranger.com/ffmpeg/

/*******************************************************************************
 * SDL_RWops <-> AVIOContext
 */

static int rwops_read(void *opaque, uint8_t *buf, int buf_size) {
    SDL_RWops *rw = (SDL_RWops *) opaque;

    int rv = rw->read(rw, buf, 1, buf_size);
    return rv;

}

static int rwops_write(void *opaque, uint8_t *buf, int buf_size) {
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
	if (buffer == NULL) {
		return NULL;
	}
    AVIOContext *rv = avio_alloc_context(
        buffer,
        RWOPS_BUFFER,
        0,
        rw,
        rwops_read,
        rwops_write,
        rwops_seek);
    if (rv == NULL) {
    	av_free(buffer);
    	return NULL;
    }

    return rv;
}

static void rwops_close(SDL_RWops *rw) {
	rw->close(rw);
}

static double current_time = 0;

typedef struct PacketQueueEntry {
	AVPacket *pkt;
	struct PacketQueueEntry *next;
} PacketQueueEntry;

typedef struct PacketQueue {
	PacketQueueEntry *first;
	PacketQueueEntry *last;
} PacketQueue;

typedef struct FrameQueue {
	AVFrame *first;
	AVFrame *last;
} FrameQueue;


typedef struct SurfaceQueueEntry {
	struct SurfaceQueueEntry *next;

	SDL_Surface *surf;

	/* The pts, converted to seconds. */
	double pts;

	/* The format. This is not refcounted, but it's kept alive by being
	 * the format of one of the sampel surfaces.
	 */
	SDL_PixelFormat *format;

	/* As with SDL_Surface. */
	int w, h, pitch;
	void *pixels;

} SurfaceQueueEntry;

typedef struct MediaState {

    /* The next entry in a list of MediaStates */
    struct MediaState *next;

    /* The thread associated with decoding this media. */
    SDL_Thread *thread;

	/* The condition and lock. */
	SDL_cond* cond;
	SDL_mutex* lock;

	SDL_RWops *rwops;
	char *filename;

	/*
	 * True if we this stream should have video.
	 */
	int want_video;

	/* This becomes true once the decode thread has finished initializing
	 * and the readers and writers can do their thing.
	 */
	int ready; // Lock.

	/* This is set to true when data has been read, in order to ask the
	 * decode thread to produce more data.
	 */
	int needs_decode; // Lock.

	/*
	 * This is set to true when data has been read, in order to ask the
	 * decode thread to shut down and deallocate all resources.
	 */
	int quit; // Lock

	/* The number of seconds to skip at the start. */
	double skip;

	/* These become true when the audio and video finish. */
	int audio_finished;
	int video_finished;

	/* Indexes of video and audio streams. */
	int video_stream;
	int audio_stream;

	/* The main context. */
	AVFormatContext *ctx;

	/* Contexts for decoding audio and video streams. */
	AVCodecContext *video_context;
	AVCodecContext *audio_context;

	/* Queues of packets going to the audio and video streams. */
	PacketQueue video_packet_queue;
	PacketQueue audio_packet_queue;

	/* The total duration of the video. Only used for information purposes. */
	double total_duration;

	/* Audio Stuff ***********************************************************/

	/* The queue of converted audio frames. */
	FrameQueue audio_queue; // Lock

	/* The size of the audio queue, and the target size in seconds. */
	int audio_queue_samples;
	int audio_queue_target_samples;

	/* A frame used for decoding. */
	AVFrame *audio_decode_frame;

	/* The audio frame being read from, and the index into the audio frame. */
	AVFrame *audio_out_frame; // Lock
	int audio_out_index; // Lock

	SwrContext *swr;

	/* The duration of the audio stream, in samples.
	 * -1 means to play until we run out of data.
	 */
	int audio_duration;

	/* The number of samples that have been read so far. */
	int audio_read_samples; // Lock

	/* A frame that video is decoded into. */
	AVFrame *video_decode_frame;

	/* Video Stuff ***********************************************************/

	/* Software rescaling context. */
	struct SwsContext *sws;

	/* A queue of decoded video frames. */
	SurfaceQueueEntry *surface_queue; // Lock
	int surface_queue_size; // Lock

	/* The offset between a pts timestamp and realtime. */
	double video_pts_offset;

	/* The wall time the last video frame was read. */
	double video_read_time;

	/* Are frame drops allowed? */
	int frame_drops;

	/* The time the pause happened, or 0 if we're not paused. */
	double pause_time;

	/* The offset between now and the time of the current frame, at least for video. */
	double time_offset;

} MediaState;

static AVFrame *dequeue_frame(FrameQueue *fq);
static void free_packet_queue(PacketQueue *pq);
static SurfaceQueueEntry *dequeue_surface(SurfaceQueueEntry **queue);


/* A queue of MediaState objects that are awaiting deallocation.*/
static MediaState *deallocate_queue = NULL;

/* A mutex that discards deallocate_queue. */
SDL_mutex *deallocate_mutex = NULL;

/* Deallocates a single MediaState. */
static void deallocate(MediaState *ms) {

    while (1) {
		SurfaceQueueEntry *sqe = dequeue_surface(&ms->surface_queue);

		if (! sqe) {
			break;
		}

		if (sqe->pixels) {
#ifndef USE_POSIX_MEMALIGN
			SDL_free(sqe->pixels);
#else
			free(sqe->pixels);
#endif
		}
		av_free(sqe);
	}

	if (ms->sws) {
		sws_freeContext(ms->sws);
	}

	if (ms->video_decode_frame) {
		av_frame_free(&ms->video_decode_frame);
	}

	/* Destroy audio stuff. */
	if (ms->swr) {
		swr_free(&ms->swr);
	}

	if (ms->audio_decode_frame) {
		av_frame_free(&ms->audio_decode_frame);
	}

	if (ms->audio_out_frame) {
		av_frame_free(&ms->audio_out_frame);
	}

	while (1) {
		AVFrame *f = dequeue_frame(&ms->audio_queue);

		if (!f) {
			break;
		}

		av_frame_free(&f);
	}

	/* Destroy/Close core stuff. */
	free_packet_queue(&ms->audio_packet_queue);
	free_packet_queue(&ms->video_packet_queue);

	if (ms->video_context) {
		avcodec_free_context(&ms->video_context);
	}
	if (ms->audio_context) {
		avcodec_free_context(&ms->audio_context);
	}

	if (ms->ctx) {

		if (ms->ctx->pb) {
			if (ms->ctx->pb->buffer) {
				av_freep(&ms->ctx->pb->buffer);
			}
			av_freep(&ms->ctx->pb);
		}

		avformat_close_input(&ms->ctx);
		avformat_free_context(ms->ctx);
	}

	/* Destroy alloc stuff. */
	if (ms->cond) {
		SDL_DestroyCond(ms->cond);
	}
	if (ms->lock) {
		SDL_DestroyMutex(ms->lock);
	}

	if (ms->rwops) {
		rwops_close(ms->rwops);
	}

	if (ms->filename) {
		av_free(ms->filename);
	}

	/* Add this MediaState to a queue to have its thread ended, and the MediaState
	 * deactivated.
	 */
	SDL_LockMutex(deallocate_mutex);
    ms->next = deallocate_queue;
    deallocate_queue = ms;
    SDL_UnlockMutex(deallocate_mutex);

}

/* Perform the portion of deallocation that's been deferred to the main thread. */
static void deallocate_deferred() {

    SDL_LockMutex(deallocate_mutex);

    while (deallocate_queue) {
        MediaState *ms = deallocate_queue;
        deallocate_queue = ms->next;

        if (ms->thread) {
            SDL_WaitThread(ms->thread, NULL);
        }

        av_free(ms);
    }

    SDL_UnlockMutex(deallocate_mutex);
}

/* Frame queue ***************************************************************/

static void enqueue_frame(FrameQueue *fq, AVFrame *frame) {
	frame->opaque = NULL;

	if (fq->first) {
		fq->last->opaque = frame;
		fq->last = frame;
	} else {
		fq->first = fq->last = frame;
	}
}

static AVFrame *dequeue_frame(FrameQueue *fq) {
	if (!fq->first) {
		return NULL;
	}

	AVFrame *rv = fq->first;
	fq->first = (AVFrame *) rv->opaque;

	if (!fq->first) {
		fq->last = NULL;
	}

	return rv;
}


/* Packet queue **************************************************************/

static void enqueue_packet(PacketQueue *pq, AVPacket *pkt) {
	PacketQueueEntry *pqe = av_malloc(sizeof(PacketQueueEntry));
	if (pqe == NULL) {
		av_packet_free(&pkt);
		return;
	}

	pqe->pkt = pkt;
	pqe->next = NULL;

	if (!pq->first) {
		pq->first = pq->last = pqe;
	} else {
		pq->last->next = pqe;
		pq->last = pqe;
	}
}

static AVPacket *first_packet(PacketQueue *pq) {
	if (pq->first) {
		return pq->first->pkt;
	} else {
		return NULL;
	}
}

static void dequeue_packet(PacketQueue *pq) {
	if (! pq->first) {
		return;
	}

	PacketQueueEntry *pqe = pq->first;
	pq->first = pqe->next;

	if (!pq->first) {
		pq->last = NULL;
	}

	av_packet_free(&pqe->pkt);
	av_free(pqe);
}

static int count_packet_queue(PacketQueue *pq) {
    PacketQueueEntry *pqe = pq->first;

	int rv = 0;

	while (pqe) {
		rv += 1;
		pqe = pqe->next;
	}

	return rv;
}

static void free_packet_queue(PacketQueue *pq) {
	while(first_packet(pq)) {
		dequeue_packet(pq);
	}
}


/**
 * Reads a packet from one of the queues, filling the other queue if
 * necessary. Returns the packet, or NULL if end of file has been reached.
 */
static AVPacket *read_packet(MediaState *ms, PacketQueue *pq) {

	AVPacket *pkt;
	AVPacket *rv;

	while (1) {

		rv = first_packet(pq);
		if (rv) {
			return rv;
		}

		pkt = av_packet_alloc();

		if (!pkt) {
			return NULL;
		}

		if (av_read_frame(ms->ctx, pkt)) {
			return NULL;
		}

		if (pkt->stream_index == ms->video_stream && ! ms->video_finished) {
			enqueue_packet(&ms->video_packet_queue, pkt);
		} else if (pkt->stream_index == ms->audio_stream && ! ms->audio_finished) {
			enqueue_packet(&ms->audio_packet_queue, pkt);
		} else {
			av_packet_free(&pkt);
		}
	}
}


/* Surface queue *************************************************************/

static void enqueue_surface(SurfaceQueueEntry **queue, SurfaceQueueEntry *sqe) {
	while (*queue) {
		queue = &(*queue)->next;
	}

	*queue = sqe;
}


static SurfaceQueueEntry *dequeue_surface(SurfaceQueueEntry **queue) {
	SurfaceQueueEntry *rv = *queue;

	if (rv) {
		*queue = rv->next;
	}

	return rv;
}


#if 0
static void check_surface_queue(MediaState *ms) {

	SurfaceQueueEntry **queue = &ms->surface_queue;

	int count = 0;

	while (*queue) {
		count += 1;
		queue = &(*queue)->next;
	}

	if (count != ms->surface_queue_size) {
		abort();
	}

}
#endif

/* Find decoder context ******************************************************/


static AVCodecContext *find_context(AVFormatContext *ctx, int index) {

    AVDictionary *opts = NULL;

	if (index == -1) {
		return NULL;
	}

	AVCodec *codec = NULL;
	AVCodecContext *codec_ctx = NULL;

	codec_ctx = avcodec_alloc_context3(NULL);

	if (codec_ctx == NULL) {
		return NULL;
	}

	if (avcodec_parameters_to_context(codec_ctx, ctx->streams[index]->codecpar) < 0) {
		goto fail;
	}

	codec_ctx->pkt_timebase = ctx->streams[index]->time_base;

    codec = avcodec_find_decoder(codec_ctx->codec_id);

    if (codec == NULL) {
        goto fail;
    }

    codec_ctx->codec_id = codec->id;

    av_dict_set(&opts, "threads", "auto", 0);
    av_dict_set(&opts, "refcounted_frames", "0", 0);

	if (avcodec_open2(codec_ctx, codec, &opts)) {
		goto fail;
	}

	return codec_ctx;

fail:

    av_dict_free(&opts);

	avcodec_free_context(&codec_ctx);
	return NULL;
}


/* Audio decoding *************************************************************/

static void decode_audio(MediaState *ms) {
	int ret;
	AVPacket *pkt;
	AVFrame *converted_frame;

	if (!ms->audio_context) {
		ms->audio_finished = 1;
		return;
	}

	if (ms->audio_decode_frame == NULL) {
		ms->audio_decode_frame = av_frame_alloc();
	}

	if (ms->audio_decode_frame == NULL) {
		ms->audio_finished = 1;
		return;
	}

	double timebase = av_q2d(ms->ctx->streams[ms->audio_stream]->time_base);

	if (ms->audio_queue_target_samples < audio_target_samples) {
	    ms->audio_queue_target_samples += audio_sample_increase;
	}

	while (ms->audio_queue_samples < ms->audio_queue_target_samples) {

		/** Read a packet, and send it to the decoder. */
		pkt = read_packet(ms, &ms->audio_packet_queue);
		ret = avcodec_send_packet(ms->audio_context, pkt);

		if (ret == 0) {
			dequeue_packet(&ms->audio_packet_queue);
		} else if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) {
			// pass
		} else {
			ms->audio_finished = 1;
			return;
		}

		while (1) {

			ret = avcodec_receive_frame(ms->audio_context, ms->audio_decode_frame);

			// More input is needed.
			if (ret == AVERROR(EAGAIN)) {
				break;
			}

			if (ret < 0) {
				ms->audio_finished = 1;
				return;
			}

            converted_frame = av_frame_alloc();

			if (converted_frame == NULL) {
				ms->audio_finished = 1;
				return;
			}

            converted_frame->sample_rate = audio_sample_rate;
            converted_frame->channel_layout = AV_CH_LAYOUT_STEREO;
            converted_frame->format = AV_SAMPLE_FMT_S16;

			if (!ms->audio_decode_frame->channel_layout) {
				ms->audio_decode_frame->channel_layout = av_get_default_channel_layout(ms->audio_decode_frame->channels);

				if (audio_equal_mono && (ms->audio_decode_frame->channels == 1)) {
				    swr_alloc_set_opts(
                        ms->swr,
                        converted_frame->channel_layout,
                        converted_frame->format,
                        converted_frame->sample_rate,
                        ms->audio_decode_frame->channel_layout,
                        ms->audio_decode_frame->format,
                        ms->audio_decode_frame->sample_rate,
                        0,
                        NULL);

				    swr_set_matrix(ms->swr, stereo_matrix, 1);
				}
			}

			if(swr_convert_frame(ms->swr, converted_frame, ms->audio_decode_frame)) {
				av_frame_free(&converted_frame);
				continue;
			}

			double start = ms->audio_decode_frame->best_effort_timestamp * timebase;
			double end = start + 1.0 * converted_frame->nb_samples / audio_sample_rate;

			SDL_LockMutex(ms->lock);

			if (start >= ms->skip) {

				// Normal case, queue the frame.
				ms->audio_queue_samples += converted_frame->nb_samples;
				enqueue_frame(&ms->audio_queue, converted_frame);

			} else if (end < ms->skip) {
				// Totally before, drop the frame.
				av_frame_free(&converted_frame);

			} else {
				// The frame straddles skip, so we queue the (necessarily single)
				// frame and set the index into the frame.
				ms->audio_out_frame = converted_frame;
				ms->audio_out_index = BPS * (int) ((ms->skip - start) * audio_sample_rate);

			}

			SDL_UnlockMutex(ms->lock);
		}

	}

	return;

}


/* Video decoding *************************************************************/

static enum AVPixelFormat get_pixel_format(SDL_Surface *surf) {
    uint32_t pixel;
    uint8_t *bytes = (uint8_t *) &pixel;

	pixel = SDL_MapRGBA(surf->format, 1, 2, 3, 4);

	enum AVPixelFormat fmt;

    if ((bytes[0] == 4 || bytes[0] == 0) && bytes[1] == 1) {
        fmt = AV_PIX_FMT_ARGB;
    } else if ((bytes[0] == 4  || bytes[0] == 0) && bytes[1] == 3) {
        fmt = AV_PIX_FMT_ABGR;
    } else if (bytes[0] == 1) {
        fmt = AV_PIX_FMT_RGBA;
    } else {
        fmt = AV_PIX_FMT_BGRA;
    }

    return fmt;
}


static SurfaceQueueEntry *decode_video_frame(MediaState *ms) {
	int ret;

	while (1) {

		AVPacket *pkt = read_packet(ms, &ms->video_packet_queue);
		ret = avcodec_send_packet(ms->video_context, pkt);


		if (ret == 0) {
			dequeue_packet(&ms->video_packet_queue);
		} else if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) {
			// pass
		} else {
			ms->video_finished = 1;
			return NULL;
		}

		ret = avcodec_receive_frame(ms->video_context, ms->video_decode_frame);

		// More input is needed.
		if (ret == AVERROR(EAGAIN)) {
			continue;
		}

		if (ret < 0) {
			ms->video_finished = 1;
			return NULL;
		}

		break;
	}

	double pts = ms->video_decode_frame->best_effort_timestamp * av_q2d(ms->ctx->streams[ms->video_stream]->time_base);

	if (pts < ms->skip) {
		return NULL;
	}

	// If we're behind on decoding the frame, drop it.
	if (ms->video_pts_offset && (ms->video_pts_offset + pts < ms->video_read_time)) {

		// If we're 5s behind, give up on video for the time being, so we don't
		// blow out memory.
		if (ms->video_pts_offset + pts < ms->video_read_time - 5.0) {
			ms->video_finished = 1;
		}

		if (ms->frame_drops) {
		    return NULL;
		}
	}

	SDL_Surface *sample = rgba_surface;

	if (ms->sws == NULL) {
		ms->sws = sws_getContext(
			ms->video_decode_frame->width,
			ms->video_decode_frame->height,
			ms->video_decode_frame->format,

			ms->video_decode_frame->width,
			ms->video_decode_frame->height,
			get_pixel_format(sample),

			SWS_POINT | SWS_FULL_CHR_H_INP | SWS_FULL_CHR_H_INT,

			NULL,
			NULL,
			NULL
			);


		if (!ms->sws) {
			ms->video_finished = 1;
			return NULL;
		}

		sws_setColorspaceDetails(ms->sws,
			sws_getCoefficients(SWS_CS_DEFAULT), 0,
			sws_getCoefficients(SWS_CS_DEFAULT), 0,
			0, 1 << 16, 1 << 16);
	}

	SurfaceQueueEntry *rv = av_malloc(sizeof(SurfaceQueueEntry));
	if (rv == NULL) {
		ms->video_finished = 1;
		return NULL;
	}
	rv->w = ms->video_decode_frame->width + FRAME_PADDING * 2;
	rv->h = ms->video_decode_frame->height + FRAME_PADDING * 2;

	rv->pitch = rv->w * sample->format->BytesPerPixel;

	if (rv->pitch % ROW_ALIGNMENT) {
	    rv->pitch += ROW_ALIGNMENT - (rv->pitch % ROW_ALIGNMENT);
	}

#ifndef USE_POSIX_MEMALIGN
    rv->pixels = SDL_calloc(rv->pitch * rv->h, 1);
#else
	if (posix_memalign(&rv->pixels, ROW_ALIGNMENT, rv->pitch * rv->h)) {
		av_free(rv);
		return NULL;
	}
    memset(rv->pixels, 0, rv->pitch * rv->h);
#endif

	rv->format = sample->format;
	rv->next = NULL;
	rv->pts = pts;

	uint8_t *surf_pixels = (uint8_t *) rv->pixels;
	uint8_t *surf_data[] = { &surf_pixels[FRAME_PADDING * rv->pitch + FRAME_PADDING * sample->format->BytesPerPixel] };
	int surf_linesize[] = { rv->pitch };

	sws_scale(
		ms->sws,

		(const uint8_t * const *) ms->video_decode_frame->data,
		ms->video_decode_frame->linesize,

		0,
		ms->video_decode_frame->height,

		surf_data,
		surf_linesize
		);

	return rv;
}


static void decode_video(MediaState *ms) {
	if (!ms->video_context) {
		ms->video_finished = 1;
		return;
	}

	if (!ms->video_decode_frame) {
		ms->video_decode_frame = av_frame_alloc();
	}

	if (!ms->video_decode_frame) {
		ms->video_finished = 1;
		return;
	}

	SDL_LockMutex(ms->lock);

	if (!ms->video_finished && (ms->surface_queue_size < FRAMES)) {

		SDL_UnlockMutex(ms->lock);

		SurfaceQueueEntry *sqe = decode_video_frame(ms);

		SDL_LockMutex(ms->lock);

		if (sqe) {
			enqueue_surface(&ms->surface_queue, sqe);
			ms->surface_queue_size += 1;
		}
	}

	if (!ms->video_finished && (ms->surface_queue_size < FRAMES)) {
		ms->needs_decode = 1;
	}

	SDL_UnlockMutex(ms->lock);
}


static int decode_sync_start(void *arg);
void media_read_sync(struct MediaState *ms);
void media_read_sync_finish(struct MediaState *ms);


/**
 * Returns 1 if there is a video frame ready on this channel, or 0 otherwise.
 */
int media_video_ready(struct MediaState *ms) {

	int consumed = 0;
	int rv = 0;

	if (ms->video_stream == -1) {
		return 1;
	}

	SDL_LockMutex(ms->lock);

	if (!ms->ready) {
		goto done;
	}

	if (ms->pause_time > 0) {
	    goto done;
	}

	double offset_time = current_time - ms->time_offset;

	/*
	 * If we have an obsolete frame, drop it.
	 */
	if (ms->video_pts_offset) {
		while (ms->surface_queue) {

			/* The PTS is greater that the last frame read, so we're good. */
			if (ms->surface_queue->pts + ms->video_pts_offset >= ms->video_read_time) {
				break;
			}

			/* Otherwise, drop it without display. */
			SurfaceQueueEntry *sqe = dequeue_surface(&ms->surface_queue);
			ms->surface_queue_size -= 1;

			if (sqe->pixels) {
#ifndef USE_POSIX_MEMALIGN
				SDL_free(sqe->pixels);
#else
				free(sqe->pixels);
#endif
			}
			av_free(sqe);

			consumed = 1;
		}
	}


	/*
	 * Otherwise, check to see if we have a frame with a PTS that has passed.
	 */

	if (ms->surface_queue) {
		if (ms->video_pts_offset) {
			if (ms->surface_queue->pts + ms->video_pts_offset <= offset_time + frame_early_delivery) {
				rv = 1;
			}
		} else {
			rv = 1;
		}
	}

done:

	/* Only signal if we've consumed something. */
	if (consumed) {
		ms->needs_decode = 1;
		SDL_CondBroadcast(ms->cond);
	}

	SDL_UnlockMutex(ms->lock);

	return rv;
}


SDL_Surface *media_read_video(MediaState *ms) {

	SDL_Surface *rv = NULL;
	SurfaceQueueEntry *sqe = NULL;

	if (ms->video_stream == -1) {
		return NULL;
	}

	double offset_time = current_time - ms->time_offset;

	SDL_LockMutex(ms->lock);

#ifndef __EMSCRIPTEN__
	while (!ms->ready) {
	    SDL_CondWait(ms->cond, ms->lock);
	}
#endif

	if (ms->pause_time > 0) {
	    goto done;
	}

	if (!ms->surface_queue_size) {
		goto done;
	}

	if (ms->video_pts_offset == 0.0) {
		ms->video_pts_offset = offset_time - ms->surface_queue->pts;
	}

	if (ms->surface_queue->pts + ms->video_pts_offset <= offset_time + frame_early_delivery) {
		sqe = dequeue_surface(&ms->surface_queue);
		ms->surface_queue_size -= 1;

	}

done:

    /* Only signal if we've consumed something. */
	if (sqe) {
		ms->needs_decode = 1;
		ms->video_read_time = offset_time;
		SDL_CondBroadcast(ms->cond);
	}

	SDL_UnlockMutex(ms->lock);

	if (sqe) {
		rv = SDL_CreateRGBSurfaceFrom(
			sqe->pixels,
			sqe->w,
			sqe->h,
			sqe->format->BitsPerPixel,
			sqe->pitch,
			sqe->format->Rmask,
			sqe->format->Gmask,
			sqe->format->Bmask,
			sqe->format->Amask
		);

		/* Force SDL to take over management of pixels. */
		rv->flags &= ~SDL_PREALLOC;
		av_free(sqe);
	}

	return rv;
}


static int decode_thread(void *arg) {
	MediaState *ms = (MediaState *) arg;

	int err;

	AVFormatContext *ctx = avformat_alloc_context();
	if (ctx == NULL) {
		goto finish;
	}
	ms->ctx = ctx;

	AVIOContext *io_context = rwops_open(ms->rwops);
	if (io_context == NULL) {
		goto finish;
	}
	ctx->pb = io_context;

	err = avformat_open_input(&ctx, ms->filename, NULL, NULL);
	if (err) {
		avformat_free_context(ctx);
		ms->ctx = NULL;
		goto finish;
	}

	err = avformat_find_stream_info(ctx, NULL);
	if (err) {
		goto finish;
	}


	ms->video_stream = -1;
	ms->audio_stream = -1;

	for (unsigned int i = 0; i < ctx->nb_streams; i++) {
		if (ctx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO) {
			if (ms->want_video && ms->video_stream == -1) {
				ms->video_stream = i;
			}
		}

		if (ctx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_AUDIO) {
			if (ms->audio_stream == -1) {
				ms->audio_stream = i;
			}
		}
	}

	ms->video_context = find_context(ctx, ms->video_stream);
	ms->audio_context = find_context(ctx, ms->audio_stream);

	ms->swr = swr_alloc();
	if (ms->swr == NULL) {
		goto finish;
	}

	// Compute the number of samples we need to play back.
	if (ms->audio_duration < 0) {
		if (av_fmt_ctx_get_duration_estimation_method(ctx) != AVFMT_DURATION_FROM_BITRATE) {

			long long duration = ((long long) ctx->duration) * audio_sample_rate;
			ms->audio_duration = (unsigned int) (duration /  AV_TIME_BASE);

			ms->total_duration = 1.0 * ctx->duration / AV_TIME_BASE;

			// Check that the duration is reasonable (between 0s and 3600s). If not,
			// reject it.
			if (ms->audio_duration < 0 || ms->audio_duration > 3600 * audio_sample_rate) {
				ms->audio_duration = -1;
			}

			ms->audio_duration -= (unsigned int) (ms->skip * audio_sample_rate);


		} else {
			ms->audio_duration = -1;
		}
	}

	if (ms->skip != 0.0) {
		av_seek_frame(ctx, -1, (int64_t) (ms->skip * AV_TIME_BASE), AVSEEK_FLAG_BACKWARD);
	}

	while (!ms->quit) {

		if (! ms->audio_finished) {
			decode_audio(ms);
		}

		if (! ms->video_finished) {
			decode_video(ms);
		}

		SDL_LockMutex(ms->lock);

		if (!ms->ready) {
			ms->ready = 1;
			SDL_CondBroadcast(ms->cond);
		}

		if (!(ms->needs_decode || ms->quit)) {
			SDL_CondWait(ms->cond, ms->lock);
		}

		ms->needs_decode = 0;

		SDL_UnlockMutex(ms->lock);
	}


finish:
	/* Data used by the decoder should be freed here, while data shared with
	 * the readers should be freed in media_close.
	 */

	SDL_LockMutex(ms->lock);

	/* Ensures that every stream becomes ready. */
	if (!ms->ready) {
		ms->ready = 1;
		SDL_CondBroadcast(ms->cond);
	}

	while (!ms->quit) {
		SDL_CondWait(ms->cond, ms->lock);
	}

	SDL_UnlockMutex(ms->lock);

	deallocate(ms);

	return 0;
}


void media_read_sync_finish(struct MediaState *ms) {
	// copy/paste from end of decode_thread

	/* Data used by the decoder should be freed here, while data shared with
	 * the readers should be freed in media_close.
	 */

	SDL_LockMutex(ms->lock);

	/* Ensures that every stream becomes ready. */
	if (!ms->ready) {
		ms->ready = 1;
		SDL_CondBroadcast(ms->cond);
	}

	while (!ms->quit) {
		/* SDL_CondWait(ms->cond, ms->lock); */
	}

	SDL_UnlockMutex(ms->lock);

	deallocate(ms);
}


static int decode_sync_start(void *arg) {
    // copy/paste from start of decode_thread
	MediaState *ms = (MediaState *) arg;

	int err;

	AVFormatContext *ctx = avformat_alloc_context();
	if (ctx == NULL) {
		media_read_sync_finish(ms);
	}
	ms->ctx = ctx;

	AVIOContext *io_context = rwops_open(ms->rwops);
	if (io_context == NULL) {
		media_read_sync_finish(ms);
	}
	ctx->pb = io_context;

	err = avformat_open_input(&ctx, ms->filename, NULL, NULL);
	if (err) {
		avformat_free_context(ctx);
		ms->ctx = NULL;
		media_read_sync_finish(ms);
	}

	err = avformat_find_stream_info(ctx, NULL);
	if (err) {
		media_read_sync_finish(ms);
	}


	ms->video_stream = -1;
	ms->audio_stream = -1;

	for (unsigned int i = 0; i < ctx->nb_streams; i++) {
		if (ctx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO) {
			if (ms->want_video && ms->video_stream == -1) {
				ms->video_stream = i;
			}
		}

		if (ctx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_AUDIO) {
			if (ms->audio_stream == -1) {
				ms->audio_stream = i;
			}
		}
	}

	ms->video_context = find_context(ctx, ms->video_stream);
	ms->audio_context = find_context(ctx, ms->audio_stream);

	ms->swr = swr_alloc();
	if (ms->swr == NULL) {
		media_read_sync_finish(ms);
	}

	// Compute the number of samples we need to play back.
	if (ms->audio_duration < 0) {
		if (av_fmt_ctx_get_duration_estimation_method(ctx) != AVFMT_DURATION_FROM_BITRATE) {

			long long duration = ((long long) ctx->duration) * audio_sample_rate;
			ms->audio_duration = (unsigned int) (duration /  AV_TIME_BASE);

			ms->total_duration = 1.0 * ctx->duration / AV_TIME_BASE;

			// Check that the duration is reasonable (between 0s and 3600s). If not,
			// reject it.
			if (ms->audio_duration < 0 || ms->audio_duration > 3600 * audio_sample_rate) {
				ms->audio_duration = -1;
			}

			ms->audio_duration -= (unsigned int) (ms->skip * audio_sample_rate);


		} else {
			ms->audio_duration = -1;
		}
	}

	if (ms->skip != 0.0) {
		av_seek_frame(ctx, -1, (int64_t) (ms->skip * AV_TIME_BASE), AVSEEK_FLAG_BACKWARD);
	}

	// [snip!]

	return 0;
}


void media_read_sync(struct MediaState *ms) {
	// copy/paste from middle of decode_thread
	// printf("---* media_read_sync %p\n", ms);

	//while (!ms->quit) {
	if (!ms->quit) {
		// printf("     audio_finished: %d, video_finished: %d\n", ms->audio_finished, ms->video_finished);
		if (! ms->audio_finished) {
			decode_audio(ms);
		}

		if (! ms->video_finished) {
			decode_video(ms);
		}

		SDL_LockMutex(ms->lock);

		if (!ms->ready) {
			ms->ready = 1;
			SDL_CondBroadcast(ms->cond);
		}

		if (!(ms->needs_decode || ms->quit)) {
			/* SDL_CondWait(ms->cond, ms->lock); */
		}

		ms->needs_decode = 0;

		SDL_UnlockMutex(ms->lock);
	}
}


int media_read_audio(struct MediaState *ms, Uint8 *stream, int len) {
#ifdef __EMSCRIPTEN__
    media_read_sync(ms);
#endif

	SDL_LockMutex(ms->lock);

    if(!ms->ready) {
	    SDL_UnlockMutex(ms->lock);
	    memset(stream, 0, len);
	    return len;
	}

	int rv = 0;

	if (ms->audio_duration >= 0) {
		int remaining = (ms->audio_duration - ms->audio_read_samples) * BPS;
		if (len > remaining) {
			len = remaining;
		}

		if (!remaining) {
			ms->audio_finished = 1;
		}

	}

	while (len) {

		if (!ms->audio_out_frame) {
			ms->audio_out_frame = dequeue_frame(&ms->audio_queue);
			ms->audio_out_index = 0;
		}

		if (!ms->audio_out_frame) {
			break;
		}

		AVFrame *f = ms->audio_out_frame;

		int avail = f->nb_samples * BPS - ms->audio_out_index;
		int count;

		if (len > avail) {
			count = avail;
		} else {
			count = len;
		}

		memcpy(stream, &f->data[0][ms->audio_out_index], count);

		ms->audio_out_index += count;

		ms->audio_read_samples += count / BPS;
		ms->audio_queue_samples -= count / BPS;

		rv += count;
		len -= count;
		stream += count;

		if (ms->audio_out_index >= f->nb_samples * BPS) {
			av_frame_free(&ms->audio_out_frame);
			ms->audio_out_index = 0;
		}
	}

	/* Only signal if we've consumed something. */
	if (rv) {
		ms->needs_decode = 1;
		SDL_CondBroadcast(ms->cond);
	}

	SDL_UnlockMutex(ms->lock);

	if (ms->audio_duration >= 0) {
		if ((ms->audio_duration - ms->audio_read_samples) * BPS < len) {
			len = (ms->audio_duration - ms->audio_read_samples) * BPS;
		}

		memset(stream, 0, len);
		ms->audio_read_samples += len / BPS;
		rv += len;
	}

	return rv;
}

void media_wait_ready(struct MediaState *ms) {
#ifndef __EMSCRIPTEN__
    SDL_LockMutex(ms->lock);

    while (!ms->ready) {
        SDL_CondWait(ms->cond, ms->lock);
    }

    SDL_UnlockMutex(ms->lock);
#endif
}


double media_duration(MediaState *ms) {
	return ms->total_duration;
}

void media_start(MediaState *ms) {

#ifdef __EMSCRIPTEN__
    decode_sync_start(ms);
#else

    char buf[1024];

	snprintf(buf, 1024, "decode: %s", ms->filename);
	SDL_Thread *t = SDL_CreateThread(decode_thread, buf, (void *) ms);
	ms->thread = t;
#endif
}


MediaState *media_open(SDL_RWops *rwops, const char *filename) {

    deallocate_deferred();

    MediaState *ms = av_calloc(1, sizeof(MediaState));
	if (ms == NULL) {
		return NULL;
	}

	ms->filename = av_strdup(filename);
	if (ms->filename == NULL) {
		deallocate(ms);
		return NULL;
	}
	ms->rwops = rwops;

#ifndef __EMSCRIPTEN__
	ms->cond = SDL_CreateCond();
	if (ms->cond == NULL) {
		deallocate(ms);
		return NULL;
	}
	ms->lock = SDL_CreateMutex();
	if (ms->lock == NULL) {
		deallocate(ms);
		return NULL;
	}
#endif

	ms->audio_duration = -1;
	ms->frame_drops = 1;

	return ms;
}

/**
 * Sets the start and end of the stream. This must be called before
 * media_start.
 *
 * start
 *    The time in the stream at which the media starts playing.
 * end
 *    If not 0, the time at which the stream is forced to end if it has not
 *    already. If 0, the stream plays until its natural end.
 */
void media_start_end(MediaState *ms, double start, double end) {
	ms->skip = start;

	if (end >= 0) {
		if (end < start) {
			ms->audio_duration = 0;
		} else {
			ms->audio_duration = (int) ((end - start) * audio_sample_rate);
		}
	}
}

/**
 * Marks the channel as having video.
 */
void media_want_video(MediaState *ms, int video) {
	ms->want_video = 1;
	ms->frame_drops = (video != 2);
}

void media_pause(MediaState *ms, int pause) {
    if (pause && (ms->pause_time == 0)) {
        ms->pause_time = current_time;
    } else if ((!pause) && (ms->pause_time > 0)) {
        ms->time_offset += current_time - ms->pause_time;
        ms->pause_time = 0;
    }
}

void media_close(MediaState *ms) {

	if (!ms->thread) {
		deallocate(ms);
		return;
	}

	/* Tell the decoder to terminate. It will deallocate everything for us. */
	SDL_LockMutex(ms->lock);
	ms->quit = 1;

#ifdef __EMSCRIPTEN__
	media_read_sync_finish(ms);
#endif

	SDL_CondBroadcast(ms->cond);
	SDL_UnlockMutex(ms->lock);

}

void media_advance_time(void) {
	current_time = SPEED * av_gettime() * 1e-6;
}

void media_sample_surfaces(SDL_Surface *rgb, SDL_Surface *rgba) {
	rgb_surface = rgb;
	rgba_surface = rgba;
}

void media_init(int rate, int status, int equal_mono) {

    deallocate_mutex = SDL_CreateMutex();

	audio_sample_rate = rate / SPEED;
	audio_equal_mono = equal_mono;

    if (status) {
        av_log_set_level(AV_LOG_INFO);
    } else {
        av_log_set_level(AV_LOG_ERROR);
    }

}
