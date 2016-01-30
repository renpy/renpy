#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libswresample/swresample.h>

#include <SDL.h>
#include <SDL_thread.h>


/* The output audio sample rate. */
static int audio_sample_rate = 44100;

// http://dranger.com/ffmpeg/


/*******************************************************************************
 * SDL_RWops <-> AVIOContext
 * */

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

//static double get_time(void) {
//	return av_gettime() * 1e-6;
//}


typedef struct PacketQueue {
	AVPacketList *first;
	AVPacketList *last;
} PacketQueue;

typedef struct FrameQueue {
	AVFrame *first;
	AVFrame *last;
} FrameQueue;

typedef struct MediaState {

	SDL_RWops *rwops;
	char *filename;

	/* The condition and lock. */
	SDL_cond* cond;
	SDL_mutex* lock;

	/* The decode thread. */
	SDL_Thread *decode_thread;

	/* This becomes true once the decode thread has finished initializing
	 * and the readers and writers can do their thing.
	 */
	int ready;

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

	/* Queues of packets going to the audio and video
	 * streams.
	 */
	PacketQueue video_packet_queue;
	PacketQueue audio_packet_queue;


	/**
	 * The queue of converted audio frames.
	 */
	FrameQueue audio_queue;
	int audio_queue_samples;
	int audio_queue_target_seconds;
	AVFrame *audio_decode_frame;
	AVFrame *audio_out_frame;
	int audio_out_index;

	SwrContext *swr;


} MediaState;


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


static void enqueue_packet(PacketQueue *pq, AVPacket *pkt) {
	AVPacketList *pl = av_malloc(sizeof(AVPacketList));

	pl->pkt = *pkt;
	pl->next = NULL;

	if (!pq->first) {
		pq->first = pq->last = pl;
	}
}

static int dequeue_packet(PacketQueue *pq, AVPacket *pkt) {
	if (! pq->first ) {
		return 0;
	}


	AVPacketList *pl = pq->first;

	*pkt = pl->pkt;

	pq->first = pl->next;

	if (!pq->first) {
		pq->last = NULL;
	}

	av_free(pl);

	return 1;

}

/**
 * Reads a packet from one of the queues, filling the other queue if
 * necessary.
 */
int read_packet(MediaState *ms, PacketQueue *pq, AVPacket *pkt) {
	AVPacket scratch;

	while (1) {
		if (dequeue_packet(pq, pkt)) {
			return 1;
		}

		if (av_read_frame(ms->ctx, &scratch)) {
			return 0;
		}

		av_dup_packet(&scratch);

		if (scratch.stream_index == ms->video_stream) {
			enqueue_packet(&ms->video_packet_queue, &scratch);
		} else if (scratch.stream_index == ms->audio_stream) {
			enqueue_packet(&ms->audio_packet_queue, &scratch);
		} else {
			av_free_packet(&scratch);
		}
	}


}

static AVCodecContext *find_context(AVFormatContext *ctx, int index) {

	if (index == -1) {
		return NULL;
	}

	AVCodec *codec;
	AVCodecContext *codec_ctx = NULL;
	AVCodecContext *codec_ctx_orig = ctx->streams[index]->codec;

	codec = avcodec_find_decoder(codec_ctx_orig->codec_id);

	if (codec == NULL) {
		return NULL;
	}

	codec_ctx = avcodec_alloc_context3(codec);

	if (avcodec_copy_context(codec_ctx, codec_ctx_orig)) {
		goto fail;
	}

	if (avcodec_open2(codec_ctx, codec, NULL)) {
		goto fail;
	}

	return codec_ctx;

fail:
	avcodec_free_context(&codec_ctx);
	return NULL;
}

/**
 * Decodes audio. Returns 0 if no audio was decoded, or 1 if some audio was
 * decoded.
 */
static void decode_audio(MediaState *ms) {
	AVPacket pkt;
	AVPacket pkt_temp;
	AVFrame *converted_frame;

	if (!ms->audio_context) {
		ms->audio_finished = 1;
		return;
	}

	if (ms->audio_decode_frame == NULL) {
		ms->audio_decode_frame = av_frame_alloc();
	}

	while (ms->audio_queue_samples < ms->audio_queue_target_seconds * audio_sample_rate ) {

		if (!read_packet(ms, &ms->audio_packet_queue, &pkt)) {
			pkt.data = NULL;
			pkt.size = 0;
			break;
		}

		pkt_temp = pkt;

		while (pkt_temp.size) {
			int got_frame;
			int read_size = avcodec_decode_audio4(ms->audio_context, ms->audio_decode_frame, &got_frame, &pkt_temp);

			if (read_size < 0) {
				break;
			}

			pkt_temp.data += read_size;
			pkt_temp.size -= read_size;

			if (!got_frame) {
				if (pkt.data == NULL) {
					ms->audio_finished = 1;
					return;
				}

				break;
			}

			if (!ms->audio_decode_frame->channel_layout) {
				ms->audio_decode_frame->channel_layout = av_get_default_channel_layout(ms->audio_decode_frame->channels);
			}

			converted_frame = av_frame_alloc();
			converted_frame->sample_rate = audio_sample_rate;
			converted_frame->channel_layout = AV_CH_LAYOUT_STEREO;
			converted_frame->format = AV_SAMPLE_FMT_S16;

			if(swr_convert_frame(ms->swr, converted_frame, ms->audio_decode_frame) == 0) {
				ms->audio_queue_samples += converted_frame->nb_samples;
				enqueue_frame(&ms->audio_queue, converted_frame);
			} else {
				av_frame_free(&converted_frame);
			}

		}

	}

	return;

}


static int decode_thread(void *arg) {
	MediaState *ms = (MediaState *) arg;

	int err;

	SDL_LockMutex(ms->lock);
	ms->ready = 1;

	AVIOContext *io_context = rwops_open(ms->rwops);

	AVFormatContext *ctx = avformat_alloc_context();
	ms->ctx = ctx;

	ctx->pb = io_context;

	err = avformat_open_input(&ctx, ms->filename, NULL, NULL);
	if (err) {
		goto finish;
	}

	err = avformat_find_stream_info(ctx, NULL);
	if (err) {
		goto finish;
	}

	ms->video_stream = -1;
	ms->audio_stream = -1;

	for (int i = 0; i < ctx->nb_streams; i++) {
		if (ctx->streams[i]->codec->codec_type == AVMEDIA_TYPE_VIDEO) {
			if (ms->video_stream == -1) {
				ms->video_stream = i;
			}
		}

		if (ctx->streams[i]->codec->codec_type == AVMEDIA_TYPE_AUDIO) {
			if (ms->audio_stream == -1) {
				ms->audio_stream = i;
			}
		}
	}

	ms->video_context = find_context(ctx, ms->video_stream);
	ms->audio_context = find_context(ctx, ms->audio_stream);

	ms->swr = swr_alloc();


	// TODO: Audio duration stuff from line 1503 of ffdecode.c


	while (!(ms->audio_finished)) {

		if (! ms->audio_finished) {
			decode_audio(ms);
		}

		SDL_CondBroadcast(ms->cond);
		SDL_CondWait(ms->cond, ms->lock);

	}





finish:

	avcodec_free_context(&ms->video_context);
	avcodec_free_context(&ms->audio_context);

	if (ctx) {
		avformat_free_context(ctx);
	}

	av_free(io_context->buffer);
	av_free(io_context);

	SDL_UnlockMutex(ms->lock);

	return 0;
}


int ffpy2_audio_decode(struct MediaState *ms, Uint8 *stream, int len) {
	SDL_LockMutex(ms->lock);

	while (!ms->ready) {
		SDL_CondWait(ms->cond, ms->lock);
	}


	int rv = 0;

	while (len) {

		if (!ms->audio_out_frame) {
			ms->audio_out_frame = dequeue_frame(&ms->audio_queue);
			ms->audio_out_index = 0;
		}

		if (!ms->audio_out_frame) {
			break;
		}

		AVFrame *f = ms->audio_out_frame;

		int count;
		int avail = f->nb_samples * 4 - ms->audio_out_index;

		if (len > avail) {
			count = avail;
		} else {
			count = len;
		}

		memcpy(stream, &f->data[0][ms->audio_out_index], count);

		ms->audio_queue_samples -= count / 4;
		ms->audio_out_index += count;
		rv += count;
		len -= count;
		stream += count;

		if (ms->audio_out_index >= f->nb_samples * 4) {
			av_frame_free(&ms->audio_out_frame);
			ms->audio_out_index = 0;
		}


	}

	SDL_CondBroadcast(ms->cond);
	SDL_UnlockMutex(ms->lock);

	return rv;
}

void ffpy2_start(MediaState *ms) {
	char buf[1024];

	snprintf(buf, 1024, "decode: %s", ms->filename);
	SDL_CreateThread(decode_thread, buf, (void *) ms);
}


MediaState *ffpy2_alloc(SDL_RWops *rwops, const char *filename) {
	MediaState *ms = av_calloc(1, sizeof(MediaState));

	ms->filename = av_strdup(filename);
	ms->rwops = rwops;

	ms->cond = SDL_CreateCond();
	ms->lock = SDL_CreateMutex();

	ms->audio_queue_target_seconds = 3;

	return ms;
}


void ffpy2_close(MediaState *is) {
}


void ffpy2_init(int rate, int status) {

	audio_sample_rate = rate;

    av_register_all();

    if (status) {
        av_log_set_level(AV_LOG_INFO);
    } else {
        av_log_set_level(AV_LOG_ERROR);
    }

}


