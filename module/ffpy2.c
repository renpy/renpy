#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>

#include <SDL.h>
#include <SDL_thread.h>

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

} MediaState;

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

static int decode_thread(void *arg) {
	MediaState *ms = (MediaState *) arg;
	int err;

	SDL_LockMutex(ms->lock);
	ms->ready = 1;

	AVIOContext *io_context = rwops_open(ms->rwops);
	AVFormatContext *ctx = avformat_alloc_context();
	ctx->pb = io_context;

	err = avformat_open_input(&ctx, ms->filename, NULL, NULL);
	if (err) {
		goto finish;
	}

	err = avformat_find_stream_info(ctx, NULL);
	if (err) {
		goto finish;
	}

	int video_stream = -1;
	int audio_stream = -1;

	for (int i = 0; i < ctx->nb_streams; i++) {
		if (ctx->streams[i]->codec->codec_type == AVMEDIA_TYPE_VIDEO) {
			if (video_stream == -1) {
				video_stream = i;
			}
		}

		if (ctx->streams[i]->codec->codec_type == AVMEDIA_TYPE_AUDIO) {
			if (audio_stream == -1) {
				audio_stream = i;
			}
		}
	}


	AVCodecContext *video_context = find_context(ctx, video_stream);
	AVCodecContext *audio_context = find_context(ctx, audio_stream);


finish:

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

	SDL_UnlockMutex(ms->lock);

	return 0;
}

void ffpy2_start(MediaState *ms) {
	char buf[1024];

	snprintf(buf, 1024, "decode: %s", ms->filename);
	SDL_CreateThread(decode_thread, buf, (void *) ms);
}


MediaState *ffpy2_allocate(SDL_RWops *rwops, const char *filename) {
	MediaState *ms = av_calloc(1, sizeof(MediaState));

	ms->filename = av_strdup(filename);
	ms->rwops = rwops;

	ms->cond = SDL_CreateCond();
	ms->lock = SDL_CreateMutex();


	return ms;
}


void ffpy2_close(MediaState *is) {
}


void ffpy2_init(int rate, int status) {

    av_register_all();

    if (status) {
        av_log_set_level(AV_LOG_INFO);
    } else {
        av_log_set_level(AV_LOG_ERROR);
    }

}


