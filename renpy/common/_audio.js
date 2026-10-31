/* Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation files
 * (the "Software"), to deal in the Software without restriction,
 * including without limitation the rights to use, copy, modify, merge,
 * publish, distribute, sublicense, and/or sell copies of the Software,
 * and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

/** If DEBUG_OUT is true, extra debug information are shown in console */
// const DEBUG_OUT = true;
const DEBUG_OUT = false;

const USE_FRAME_CB = 'requestVideoFrameCallback' in HTMLVideoElement.prototype;

renpyAudio = {};

/**
 * A map from channel to channel object.
 */
let channels = {};
let next_chan_id = 0;

let context = new AudioContext();
renpyAudio.context = context;

/**
 * Given a channel number, gets the channel object, creating a new channel
 * object if required.
 */
let get_channel = (channel) => {

    let c = channels[channel];

    if (c) {
        return c;
    }

    c = {
        playing: null,
        queued: null,
        stereo_pan: context.createStereoPanner(),
        fade_volume: context.createGain(),
        primary_volume: context.createGain(),
        secondary_volume: context.createGain(),
        relative_volume: context.createGain(),
        paused: false,
        video: false,
        video_el: null,
        chan_id: next_chan_id++,
        media_source: null,
        video_size: null,
        is_playing: false,
        frame_ready: false,
        loop: false,
    };

    c.destination = c.stereo_pan;
    c.stereo_pan.connect(c.fade_volume);
    c.fade_volume.connect(c.primary_volume);
    c.primary_volume.connect(c.secondary_volume);
    c.secondary_volume.connect(c.relative_volume);
    c.relative_volume.connect(context.destination);

    channels[channel] = c;

    return c;
};

let interpolate = (a, b, done) => {
    return a + (b - a) * done;
}

/**
 * Coerces `value` to a finite number, falling back to `dflt`.
 */
let finite = (value, dflt) => {
    value = Number(value);
    return Number.isFinite(value) ? value : dflt;
}

/**
 * Given an audio parameter, linearly ramps it from start to end over
 * duration seconds.
 */
let linearRampToValue = (param, start, end, duration) => {
    param.cancelScheduledValues(context.currentTime);

    // Guard against non-finite inputs.
    start = finite(start, param.value);
    end = finite(end, param.value);
    duration = Math.max(0, finite(duration, 0));

    let points = 30;

    for (let i = 0; i <= points; i++) {
        let done = i / points;
        param.setValueAtTime(interpolate(start, end, done), context.currentTime + interpolate(0, duration, done));
    }
}

/**
 * Given an audio parameter, sets it to the given value.
 */
let setValue = (param, value) => {
    value = finite(value, param.value);
    param.cancelScheduledValues(context.currentTime);
    param.setValueAtTime(value, context.currentTime);
}

/**
 * Creates a buffer source for the play object `p` on channel `c`, wiring
 * up an `onended` handler that knows which source it belongs to.
 */
let create_source = (c, buffer) => {
    let source = context.createBufferSource();
    source.buffer = buffer;
    source.started = false;
    source.onended = () => { on_end(c, source); };
    return source;
}

/**
 * Time-stretches decoded voices without changing pitch. WSOLA aligns
 * overlapping waveform segments; all channels use the same alignment to
 * preserve the stereo image, including opposite-phase stereo.
 *
 * Work is split into short tasks so preparing a long voice does not block
 * input or rendering. The normal-speed path does not copy or process PCM.
 */
const tempo_buffers = new WeakMap();
let stretch_buffer = (buffer, speed, end = -1) => {
    if (speed === 1.0) {
        return Promise.resolve(buffer);
    }

    let cached = tempo_buffers.get(buffer);
    if (!cached) {
        cached = new Map();
        tempo_buffers.set(buffer, cached);
    }
    const key = `${speed}:${end}`;
    if (cached.has(key)) {
        return cached.get(key);
    }

    const promise = (async () => {
        const rate = buffer.sampleRate;
        const length = end >= 0 ? Math.min(buffer.length, Math.round(end * rate)) : buffer.length;
        const size = Math.max(1, Math.round(length / speed));
        const result = context.createBuffer(buffer.numberOfChannels, size, rate);
        const input = [], output = [];
        for (let ch = 0; ch < buffer.numberOfChannels; ch++) {
            input.push(buffer.getChannelData(ch).subarray(0, length));
            output.push(result.getChannelData(ch));
        }

        const hop = Math.max(1, Math.round(rate * 0.02));
        const window = hop * 2;
        const search = Math.round(rate * 0.012);
        const stride = Math.max(1, Math.round(rate / 6000));
        let deadline = performance.now() + 8;

        for (let pos = 0; pos < size; pos += hop) {
            const expected = Math.round(pos * speed);
            const low = Math.max(0, expected - search);
            const high = Math.max(low, Math.min(length - window, expected + search));
            let best = Math.min(expected, high);
            let bestScore = -Infinity;

            if (pos > 0) {
                // Normalized correlation avoids preferring louder fragments.
                const score = (candidate) => {
                    let cross = 0, energy = 0;
                    for (let ch = 0; ch < input.length; ch++) {
                        for (let j = 0; j < hop && pos + j < size; j += stride) {
                            const a = output[ch][pos + j];
                            const b = input[ch][candidate + j] || 0;
                            cross += a * b;
                            energy += b * b;
                        }
                    }
                    return cross / Math.sqrt(energy + 1e-20);
                };
                // Coarse search followed by sample-accurate refinement.
                for (let candidate = low; candidate <= high; candidate += stride) {
                    const value = score(candidate);
                    if (value > bestScore) {
                        bestScore = value;
                        best = candidate;
                    }
                }
                const coarse = best;
                for (let candidate = Math.max(low, coarse - stride); candidate <= Math.min(high, coarse + stride); candidate++) {
                    const value = score(candidate);
                    if (value > bestScore) {
                        bestScore = value;
                        best = candidate;
                    }
                }
            }

            for (let ch = 0; ch < input.length; ch++) {
                for (let j = 0; j < window && pos + j < size; j++) {
                    const sample = input[ch][best + j] || 0;
                    if (pos > 0 && j < hop) {
                        const weight = j / hop;
                        output[ch][pos + j] = output[ch][pos + j] * (1 - weight) + sample * weight;
                    } else {
                        output[ch][pos + j] = sample;
                    }
                }
            }

            if (performance.now() >= deadline) {
                await new Promise(resolve => setTimeout(resolve, 0));
                deadline = performance.now() + 8;
            }
        }
        return result;
    })();

    cached.set(key, promise);
    // A looping file may be requested at many speeds over a session.
    while (cached.size > 4) {
        cached.delete(cached.keys().next().value);
    }
    promise.catch(() => cached.delete(key));
    return promise;
};

/**
 * Attempts to start playing channel `c`.
 */
let start_playing = (c) => {

    let p = c.playing;

    if (p === null) {
        return;
    }

    if (p.started !== null) {
        return;
    }

    if (p.source === null) {
        return;
    }

    if (p.source.started) {
        return;
    }

    if (c.paused) {
        return;
    }

    if (p.synchro_start) {
        return;
    }

    context.resume();

    renpyAudio.connectFilter(c.playing.filter, c.playing.source, c.destination);

    if (p.fadeout === null) {
        if (p.fadein > 0) {
            linearRampToValue(c.fade_volume.gain, c.fade_volume.gain.value, 1.0, p.fadein);
        } else {
            setValue(c.fade_volume.gain, 1.0);
        }
    }

    p.source.started = true;

    if (p.end > 0 && p.end > p.start) {
        p.source.start(0, p.start / p.playback_speed, (p.end - p.start) / p.playback_speed);
    } else {
        p.source.start(0, p.start / p.playback_speed);
    }

    if (p.fadeout !== null) {
        p.fadeout_deadline ??= context.currentTime + p.fadeout;
        p.fadeout = Math.max(0, p.fadeout_deadline - context.currentTime);
        linearRampToValue(c.fade_volume.gain, c.fade_volume.gain.value, 0.0, p.fadeout);
        try {
            c.playing.source.stop(context.currentTime + p.fadeout);
        } catch (e) {
        }

    }

    setValue(c.relative_volume.gain, finite(p.relative_volume, 1.0));

    p.started = context.currentTime;
};


let pause_playing = (c) => {

    if (c.paused) {
        return;
    }

    c.paused = true;

    let p = c.playing;

    if (p === null) {
        return;
    }

    if (p.source === null) {
        return;
    }

    if (p.started === null) {
        return;
    }

    try {
        p.source.stop()
    } catch (e) {
    }

    p.source = create_source(c, p.buffer);

    p.start += (context.currentTime - p.started) * p.playback_speed;
    p.started = null;
}


/**
 * Stops playing channel `c`.
 */
let stop_playing = (c) => {


    if (c.playing !== null && c.playing.source !== null) {

        renpyAudio.disconnectFilter(c.playing.filter, c.playing.source, c.destination);

        try {
            c.playing.source.stop()
        } catch (e) {
        }
    }

    c.playing = c.queued;
    c.queued = null;
};


/**
 * Called when a channel ends naturally, to move things along.
 */
let on_end = (c, source) => {
    if (c.playing !== null && c.playing.started !== null &&
        (source === undefined || c.playing.source === source)) {
        stop_playing(c);
    }

    start_playing(c);
};

let video_start = (c) => {
    const p = c.playing;

    if (p === null) {
        return;
    }

    if (p.started !== null) {
        return;
    }

    // TODO Check if video has already been started?

    if (c.paused) {
        return;
    }

    if (c.video_el === null) {
        return;
    }

    c.video_el.loop = c.loop;

    if (p.fadeout === null) {
        if (p.fadein > 0) {
            linearRampToValue(c.fade_volume.gain, c.fade_volume.gain.value, 1.0, p.fadein);
        } else {
            setValue(c.fade_volume.gain, 1.0);
        }
    }

    c.video_el.src = p.url;
    c.video_el.play().then(() => {
        // TODO?
    }).catch((e) => {
        switch (e.name) {
            case 'NotAllowedError':
                // Autoplay not allowed until user interacts with page unless video is muted
                console.warn('Playing video as muted to prevent autoplay blocking');
                c.video_el.muted = true;
                c.video_el.play().then(() => {
                    // TODO?
                }).catch((e) => {
                    console.warn('Video is NOT playing even when muted', e.name);
                    renpyAudio.videoPlayPrompt(renpyAudio._web_video_prompt, c.video_el);
                });
                break;

            case 'AbortError':
                // Happens when user interacts while video playback is starting
                break;

            default:
                Module.print(`Cannot play ${p.name} ([${e.name}] ${e})`);
                throw e;
        }
    });

    if (p.fadeout !== null) {  // XXX Should not be possible for video
        linearRampToValue(c.fade_volume.gain, c.fade_volume.gain.value, 0.0, p.fadeout);
        try {
            c.playing.source.stop(context.currentTime + p.fadeout);
        } catch (e) {
        }

    }

    setValue(c.relative_volume.gain, finite(p.relative_volume, 1.0));

    p.started = c.video_el.currentTime;  // XXX Probably not ready yet
};

let video_pause = (c) => {
    const p = c.playing;

    if (p === null) {
        c.paused = true;
        c.video_el?.pause();
        return;
    }

    if (p.started === null) {
        return;
    }

    c.paused = true;
    c.video_el?.pause();

    //TODO? p.start += (context.currentTime - p.started);
    p.started = null;
};

let video_stop = (c) => {
    if (c.video_el !== null) {
        c.video_el.src = '';
    }

    if (c.playing !== null) {
        const q = c.playing;
        // FIXME Update debug stats for WebGL version
        if (DEBUG_OUT) {
            const period = q.period_stats[1] > 0 ? q.period_stats[0] / q.period_stats[1] : 0;
            const fetch = q.fetch_stats[1] > 0 ? q.fetch_stats[0] / q.fetch_stats[1] : 0;
            const draw = q.draw_stats[1] > 0 ? q.draw_stats[0] / q.draw_stats[1] : 0;
            const blob = q.blob_stats[1] > 0 ? q.blob_stats[0] / q.blob_stats[1] : 0;
            const array = q.array_stats[1] > 0 ? q.array_stats[0] / q.array_stats[1] : 0;
            const file = q.file_stats[1] > 0 ? q.file_stats[0] / q.file_stats[1] : 0;
            console.debug(`period=${period} (${q.period_stats[1]})`,
                `fetch=${fetch} (${q.fetch_stats[1]})`,
                `draw=${draw} (${q.draw_stats[1]})`,
                `blob=${blob} (${q.blob_stats[1]})`,
                `array=${array} (${q.array_stats[1]})`,
                `file=${file} (${q.file_stats[1]})`);
        }

        // Always show FPS in console
        const draw_fps = q.draw_stats[1] > 1 ? q.draw_stats[1] * 1000.0 / (q.draw_stats[3] - q.draw_stats[2]) : 0;
        const file_fps = q.file_stats[1] > 1 ? q.file_stats[1] * 1000.0 / (q.file_stats[3] - q.file_stats[2]) : 0;
        console.debug(`draw_fps=${draw_fps.toFixed(1)}`,
            `renpy_fps=${file_fps.toFixed(1)}`);
    }

    c.playing = c.queued;
    c.queued = null;

    if (c.playing == null && c.video_el !== null) {
        // Channel is not used anymore, release resources
        c.media_source.disconnect();
        c.media_source = null;

        c.video_size = null;

        c.video_el.parentElement.removeChild(c.video_el);
        c.video_el = null;
    }
};

let on_video_end = (c) => {
    if (c.playing !== null && c.playing.started !== null) {
        video_stop(c);
    }

    video_start(c);
};


renpyAudio.set_channel_count = (count) => {
    try {
        context.destination.channelCount = count;
    } catch (e) {
        console.warn("Cannot set channel count:", e);
    }
}


renpyAudio.queue = (channel, file, name, synchro_start, fadein, tight, start, end, relative_volume, afid, array, playback_speed = 1.0) => {

    const c = get_channel(channel);

    start = Math.max(0, finite(start, 0));
    end = finite(end, -1);
    fadein = Math.max(0, finite(fadein, 0));
    relative_volume = finite(relative_volume, 1.0);
    if (!Number.isFinite(playback_speed) || playback_speed < 0.5 || playback_speed > 3.0) {
        throw new RangeError('Voice speed must be between 0.5 and 3.0.');
    }

    if (file.startsWith('url:')) {
        const url = new URL(file.slice(4), window.location);
        if (!c.video) {
            throw new Error('URL resources are only supported for videos');
        }

        const q = {
            url: url,
            name: name,
            start: start,  // TODO?
            end: end,  // TODO?
            relative_volume: relative_volume,
            started: null,
            fadein: fadein,  // TODO?
            fadeout: null,  // TODO?
            tight: tight,  // TODO?
            filter: renpyAudio.getFilter(afid),
            synchro_start: synchro_start,

            period_stats: [0, 0],  // time sum, count
            fetch_stats: [0, 0],
            draw_stats: [0, 0, 0, 0],  // time sum, count, first timestamp, last timestamp
            blob_stats: [0, 0],
            array_stats: [0, 0],
            file_stats: [0, 0, 0, 0],  // time sum, count, first timestamp, last timestamp
        };

        if (c.video_el === null) {
            c.video_el = document.createElement('video');
            c.video_el.style.display = 'none';
            c.video_el.crossOrigin = 'anonymous';
            c.video_el.playsInline = true;  // For autoplay on Safari
            document.body.appendChild(c.video_el);

            c.video_el.addEventListener('loadedmetadata', function () {
                c.video_size = [c.video_el.videoWidth, c.video_el.videoHeight];
            });

            c.video_el.addEventListener('error', function (e) {

            });

            c.media_source = context.createMediaElementSource(c.video_el);
            c.media_source.connect(c.destination);

            c.video_el.addEventListener('ended', (e) => {
                c.is_playing = false;
                on_video_end(c);
            });

            c.video_el.addEventListener('paused', (e) => {
                c.is_playing = false;
            });

            c.video_el.addEventListener('playing', function () {
                c.is_playing = true;
            });

            if (USE_FRAME_CB) {
                // Get notified when a new video frame is available (not supported by Firefox)
                const onVideoFrame = () => {
                    c.frame_ready = true;
                    if (c.video_el !== null) {
                        c.video_el.requestVideoFrameCallback(onVideoFrame);
                    }
                };
                c.frame_ready = false;
                c.video_el.requestVideoFrameCallback(onVideoFrame);
            }
        }

        if (c.playing === null) {
            c.playing = q;
            c.paused = false;
        } else {
            c.queued = q;
        }

        video_start(c);
        return;
    } else if (c.video) {
        throw new Error('Videos must not be stored in game.zip.');
    }

    const q = {
        source: null,
        buffer: null,
        original_buffer: null,
        playback_speed: playback_speed,
        requested_speed: playback_speed,
        preparing: false,
        name: name,
        start: start,
        end: end,
        relative_volume: relative_volume,
        started: null,
        fadein: fadein,
        fadeout: null,
        tight: tight,
        name: name,
        filter: renpyAudio.getFilter(afid),
        synchro_start: synchro_start,
    };

    function failedRequest(request, error) {
        console.error(`Could not prepare audio ${request.name}:`, error);
        if (c.playing === request) {
            stop_playing(c);
            start_playing(c);
        } else if (c.queued === request) {
            c.queued = null;
        }
    }

    function prepareBuffer(request, buffer) {
        if (c.playing !== request && c.queued !== request) {
            return;
        }
        request.original_buffer = buffer;
        if (request.preparing) {
            return;
        }
        request.preparing = true;
        const speed = request.requested_speed;
        stretch_buffer(buffer, speed, request.end).then(stretched => {
            request.preparing = false;
            // Decode/stretch completion must not resurrect stopped playback.
            if (c.playing !== request && c.queued !== request) {
                return;
            }
            // Coalesce rapid slider changes rather than starting a full PCM
            // conversion for every pointer movement.
            if (speed !== request.requested_speed) {
                prepareBuffer(request, buffer);
                return;
            }
            if (c.playing === request && request.source !== null) {
                const position = renpyAudio.get_pos(channel) / 1000;
                if (request.started !== null) {
                    renpyAudio.disconnectFilter(request.filter, request.source, c.destination);
                    try {
                        request.source.stop();
                    } catch (e) {
                    }
                }
                request.start = position;
                request.started = null;
            }
            request.playback_speed = speed;
            request.buffer = stretched;
            request.source = create_source(c, stretched);
            start_playing(c);
        }).catch(error => {
            request.preparing = false;
            failedRequest(request, error);
        });
    }
    q.prepare = buffer => prepareBuffer(q, buffer);

    if (c.playing === null) {
        c.playing = q;
        c.paused = false;
    } else {
        c.queued = q;
        if (c.playing.name === name) {
            // Share decoding, but prepare each request at its own rate.
            // Each request waits independently so a queue promotion while
            // decoding/stretching is pending cannot strand the new playback.
            q.decode = c.playing.decode;
            q.decode.then(buffer => prepareBuffer(q, buffer), error => failedRequest(q, error));
            return;
        }
    }

    if (array === null) {
        array = FS.readFile(file);
    } else {
        array = new Uint8Array(array);
    }

    q.decode = new Promise((resolve, reject) => {
        context.decodeAudioData(array.buffer, resolve, reject);
    });
    q.decode.then(buffer => prepareBuffer(q, buffer), error => failedRequest(q, error));
};


renpyAudio.stop = (channel) => {
    let c = get_channel(channel);
    c.queued = null;
    if (c.video) {
        video_stop(c);
    } else {
        stop_playing(c);
    }
};


renpyAudio.dequeue = (channel, even_tight) => {

    let c = get_channel(channel);

    if (c.queued && c.queued.tight && !even_tight) {
        return;
    }

    c.queued = null;
};


renpyAudio.fadeout = (channel, delay) => {

    let c = get_channel(channel);

    delay = Math.max(0, finite(delay, 0));

    if (c.playing == null || c.playing.started == null) {
        c.playing = c.queued;
        c.queued = null;
        start_playing(c);
        return;
    }

    let p = c.playing;
    p.fadeout_deadline = context.currentTime + delay;
    p.fadeout = delay;

    linearRampToValue(c.fade_volume.gain, c.fade_volume.gain.value, 0.0, delay);

    if (c.video) {
        setTimeout(renpyAudio.stop, delay * 1000.0, channel);
        return;
    }

    try {
        p.source.stop(context.currentTime + delay);
    } catch (e) {
    }

    if (c.queued === null || !c.queued.tight) {
        return;
    }

    const end = p.end > 0 ? Math.min(p.end, p.original_buffer.duration) : p.original_buffer.duration;
    let remaining = delay + context.currentTime - p.started - (end - p.start) / p.playback_speed;

    if (remaining > 0 && c.queued) {
        c.queued.fadeout = remaining;
        c.queued.fadeout_deadline = p.fadeout_deadline;
    } else {
        c.queued = null;
    }

};

renpyAudio.queue_depth = (channel) => {
    let rv = 0;
    let c = get_channel(channel);

    // Try to resume the audio context if it's been interrupted (iOS Safari feature)
    if (context.state === "interrupted") {
        context.resume();
    }

    if (c.playing !== null) {
        rv += 1;
    }

    if (c.queued !== null) {
        rv += 1;
    }

    return rv;
};


renpyAudio.playing_name = (channel) => {
    let c = get_channel(channel);

    if (c.playing !== null) {
        return c.playing.name;
    }

    return "";
};


renpyAudio.pause = (channel) => {

    let c = get_channel(channel);
    if (c.video) {
        video_pause(c);
    } else {
        pause_playing(c);
    }
};


renpyAudio.unpause = (channel) => {
    let c = get_channel(channel);
    c.paused = false;
    if (c.video) {
        video_start(c);
    } else {
        start_playing(c);
    }
};


renpyAudio.get_pos = (channel) => {

    let c = get_channel(channel);
    let p = c.playing;

    if (p === null) {
        return -1;
    }

    let rv = p.start;

    if (p.started !== null) {
        if (c.video) {
            rv += c.video_el.currentTime - p.started;
        } else {
            rv += (context.currentTime - p.started) * p.playback_speed;
        }
    }

    return rv * 1000;
};

renpyAudio.set_playback_speed = (channel, speed) => {
    if (!Number.isFinite(speed) || speed < 0.5 || speed > 3.0) {
        throw new RangeError('Voice speed must be between 0.5 and 3.0.');
    }
    const c = get_channel(channel), p = c.playing;
    if (c.video || p === null || speed === p.requested_speed) {
        return;
    }
    p.requested_speed = speed;
    if (p.original_buffer !== null) {
        p.prepare(p.original_buffer);
    }
};

renpyAudio.get_playback_speed = (channel) => {
    const p = get_channel(channel).playing;
    return (p ? p.requested_speed : 1.0) * 1000;
};


renpyAudio.seek = (channel, position) => {
    let c = get_channel(channel);
    let p = c.playing;

    if (p === null) {
        return;
    }

    position = Math.max(0, position);
    if (p.end > 0) {
        position = Math.min(position, p.end);
    }

    if (c.video && c.video_el) {
        c.video_el.currentTime = position;
        p.start = position;
        p.started = c.paused ? null : c.video_el.currentTime;
        return;
    }

    if (!p.buffer) {
        return;
    }

    position = Math.min(position, p.original_buffer.duration);

    if (p.source !== null && p.started !== null) {
        renpyAudio.disconnectFilter(p.filter, p.source, c.destination);
        try {
            p.source.stop();
        } catch (e) {
        }
    }

    p.source = create_source(c, p.buffer);
    p.start = position;
    p.started = null;

    if (!c.paused) {
        start_playing(c);
    }
};


renpyAudio.get_duration = (channel) => {
    let c = get_channel(channel);
    let p = c.playing;

    if (p === null) {
        return 0;
    }

    if (c.video) {
        if (c.video_el) {
            const duration = c.video_el.duration;
            if (Number.isFinite(duration)) {
                return duration * 1000;
            }
        }
    } else if (p.buffer) {
        return p.original_buffer.duration * 1000;
    }

    return 0;
};


renpyAudio.set_volume = (channel, volume) => {
    let c = get_channel(channel);
    setValue(c.primary_volume.gain, volume);
};


renpyAudio.set_secondary_volume = (channel, volume, delay) => {
    let c = get_channel(channel);
    let control = c.secondary_volume.gain;

    linearRampToValue(control, control.value, volume, delay);
};


renpyAudio.get_volume = (channel) => {
    const c = get_channel(channel);
    return c.primary_volume.gain.value * 1000;
};


renpyAudio.set_pan = (channel, pan, delay) => {

    let c = get_channel(channel);
    let control = c.stereo_pan.pan;

    linearRampToValue(control, control.value, pan, delay);
};

renpyAudio.replace_audio_filter = (channel, afid, primary) => {
    let c = get_channel(channel);
    let filter = renpyAudio.getFilter(afid);

    if (c.playing && c.playing.source && primary) {
        renpyAudio.disconnectFilter(c.playing.filter, c.playing.source, c.destination);
        c.playing.filter = filter;
        renpyAudio.connectFilter(filter, c.playing.source, c.destination);
    }

    if (c.queued) {
        c.queued.filter = filter;
    }
};


renpyAudio.periodic = () => {
    let ready = true;

    for (let c of Object.values(channels)) {

        if (c.playing) {
            if (c.playing.synchro_start) {
                if (c.playing.buffer === null) {
                    ready = false;
                }

                if (c.queued) {
                    c.queued.synchro_start = false;
                }
            }
        }

        if (c.queued && c.queued.synchro_start) {
            ready = false;
        }
    }

    if (ready) {
        for (let c of Object.values(channels)) {
            if (c.playing && c.playing.synchro_start) {
                c.playing.synchro_start = false;
                start_playing(c);
            }
        }
    }
};

/* A map from voice name to voice object. */
let tts_voices = { };

renpyAudio.tts = (s, v, rate, voice) => {
    v = v || 1.0;
    rate = rate || 1.0;

    let u = new SpeechSynthesisUtterance(s);
    u.volume = v;
    u.rate = rate;

    let speechVoice = tts_voices[voice];
    if (speechVoice) {
        u.voice = speechVoice;
    }

    speechSynthesis.cancel();
    speechSynthesis.speak(u);
};


renpyAudio.update_tts_voices = () => {
    tts_voices = {};

    let voices = (speechSynthesis && speechSynthesis.getVoices) ? Array.from(speechSynthesis.getVoices()) : [];
    if (!voices.length) {
        return;
    }

    let navLangs = (typeof navigator !== "undefined" && navigator.languages && navigator.languages.length)
        ? Array.from(navigator.languages)
        : [(typeof navigator !== "undefined" && (navigator.language || navigator.userLanguage)) || "en"];

    let norm = (l) => (l || "").toLowerCase().replace(/_/g, "-");
    let base = (l) => norm(l).split("-")[0];

    let normNavLangs = navLangs.map(norm);
    let normNavBases = navLangs.map(base);

    let isNormalVoice = (v) => {
        let name = v.name || "";
        let lang = v.lang || "";
        return !name.includes("+") && !name.includes("@") && !lang.includes("+");
    };

    let scoreVoice = (v) => {
        let normal = isNormalVoice(v);
        let vLang = norm(v.lang);
        let vBase = base(v.lang);

        let langRank = -1;
        let exact = false;
        for (let i = 0; i < normNavLangs.length; i++) {
            if (vLang === normNavLangs[i]) {
                langRank = i;
                exact = true;
                break;
            } else if (vBase === normNavBases[i] && langRank === -1) {
                langRank = i;
                exact = false;
            }
        }

        let tier;
        if (normal) {
            if (langRank !== -1) {
                tier = exact ? 0 : 1;
            } else {
                tier = 2;
            }
        } else {
            if (langRank !== -1) {
                tier = 3;
            } else {
                tier = 4;
            }
        }

        return {
            tier: tier,
            isDefault: v.default ? 0 : 1,
            langRank: langRank === -1 ? 999 : langRank,
            lang: v.lang || "",
            name: v.name || "",
        };
    };

    voices.sort((a, b) => {
        let sA = scoreVoice(a);
        let sB = scoreVoice(b);

        if (sA.tier !== sB.tier) return sA.tier - sB.tier;
        if (sA.isDefault !== sB.isDefault) return sA.isDefault - sB.isDefault;
        if (sA.langRank !== sB.langRank) return sA.langRank - sB.langRank;
        if (sA.lang !== sB.lang) return sA.lang.localeCompare(sB.lang);
        return sA.name.localeCompare(sB.name);
    });

    let count = 0;
    for (let v of voices) {
        let key = v.lang + ": " + v.name;
        if (!tts_voices[key]) {
            tts_voices[key] = v;
            count++;
            if (count >= 25) {
                break;
            }
        }
    }
}

if (speechSynthesis) {
    speechSynthesis.onvoiceschanged = renpyAudio.update_tts_voices;
    renpyAudio.update_tts_voices();
}


renpyAudio.get_tts_voices = () => {
    return JSON.stringify(Object.keys(tts_voices));
}


renpyAudio.can_play_types = (l) => {
    let a = document.createElement("audio");

    for (let i of l) {
        if (!a.canPlayType(i)) {
            console.log("Can't play", i);
            return 0;
        } else {
            console.log("Can play", i);
        }
    }

    return 1;
}

renpyAudio.set_video = (channel, video, loop, web_video_prompt) => {
    const c = get_channel(channel);
    c.video = !!video;
    c.loop = !!loop;
    renpyAudio._web_video_prompt = web_video_prompt;
}

renpyAudio.video_ready = (channel) => {
    const c = get_channel(channel);
    if (USE_FRAME_CB) return c.frame_ready;
    return c.video && c.video_el !== null && c.is_playing && c.video_size !== null;
}

renpyAudio.get_video_size = (channel) => {
    const c = get_channel(channel);
    if (c.video_el !== null && c.video_size !== null) {
        return c.video_size[0] + "x" + c.video_size[1];
    }

    return "";
}

renpyAudio.read_video = (channel, video_tex, width, height) => {
    const c = get_channel(channel);

    if (USE_FRAME_CB && !c.frame_ready) return 1;

    if (c.video && c.video_el !== null && c.is_playing && c.video_size !== null) {
        const start = performance.now();
        const q = c.playing;
        const gl = GL.currentContext.GLctx;
        const texture = GL.textures[video_tex];

        if (texture == null) {
            console.warn(`OpenGL texture #${video_tex} not found!`);
            return -2;
        }

        if (c.video_size[0] != width || c.video_size[1] != height) {
            // Video size has changed, notify Ren'Py about it
            return -1;
        }

        const level = 0;
        const internalFormat = gl.RGBA;
        const srcFormat = gl.RGBA;
        const srcType = gl.UNSIGNED_BYTE;
        gl.bindTexture(gl.TEXTURE_2D, texture);
        gl.texImage2D(
            gl.TEXTURE_2D,
            level,
            internalFormat,
            srcFormat,
            srcType,
            c.video_el
        );

        // Turn off mips and set wrapping to clamp to edge so it
        // will work regardless of the dimensions of the video.
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);

        if (q !== null) {
            const cur_ts = performance.now();
            q.file_stats[0] += cur_ts - start;
            q.file_stats[1]++;
            if (q.file_stats[2] == 0) q.file_stats[2] = cur_ts;
            q.file_stats[3] = cur_ts;
        }

        if (USE_FRAME_CB) c.frame_ready = false;

        return 0;
    }

    return 1;
}

if (DEBUG_OUT) {
    // DEBUG Dumps all method calls to renpyAudio
    renpyAudio._nodump = { 'queue_depth': 1, 'playing_name': 1, 'video_ready': 1, 'read_video': 1 };
    renpyAudio = new Proxy(renpyAudio, {
        get(target, prop) {
            const origMethod = target[prop];
            if (!(prop in target._nodump) && typeof origMethod == 'function') {
                return function (...args) {
                    console.debug(prop, ...args);
                    return origMethod.apply(target, args);
                }
            }
            return origMethod;
        }
    });
}


if (context.state == "suspended") {
    let unlockContext = () => {
        context.resume().then(() => {
            document.body.removeEventListener('click', unlockContext, true);
            document.body.removeEventListener('touchend', unlockContext, true);
            document.body.removeEventListener('touchstart', unlockContext, true);
        });
    };

    document.body.addEventListener('click', unlockContext, true);
    document.body.addEventListener('touchend', unlockContext, true);
    document.body.addEventListener('touchstart', unlockContext, true);
}

renpyAudio._videoPrompt = null;
renpyAudio._blockedVideos = [];

renpyAudio.videoPlayPrompt = (message, video) => {
    renpyAudio.videoPlayPromptHide();

    const videoPrompt = document.createElement("div");
    videoPrompt.append(message);

    videoPrompt.style.position = "absolute";
    videoPrompt.style.top = "0";
    videoPrompt.style.bottom = "0";
    videoPrompt.style.left = "0";
    videoPrompt.style.right = "0";
    videoPrompt.style.font = "24px sans-serif";
    videoPrompt.style.color = "white";
    videoPrompt.style.textAlign = "center";
    videoPrompt.style.textShadow = "0 0 2px black";
    videoPrompt.style.display = "flex";
    videoPrompt.style.justifyContent = "center";
    videoPrompt.style.alignItems = "center";
    videoPrompt.style.cursor = "pointer";

    if (video !== undefined) {
        // Add video to _blockedVideos just in case multiple Movie() are blocked
        renpyAudio._blockedVideos.push(video);
    }

    videoPrompt.addEventListener('click', () => {
        renpyAudio.videoPlayPromptHide();
        const videos = renpyAudio._blockedVideos;
        renpyAudio._blockedVideos = [];
        videos.forEach((video_el) => {
            if (video_el.parentElement !== null) {
                video_el.muted = false;
                video_el.play().then(() => {
                    // TODO?
                }).catch((e) => {
                    console.warn('Cannot play video after interaction, giving up', e.name);
                    throw e;
                });
            }
        });
    });

    renpyAudio._videoPrompt = videoPrompt;
    document.body.append(videoPrompt);
};

renpyAudio.videoPlayPromptHide = () => {
    if (renpyAudio._videoPrompt) {
        renpyAudio._videoPrompt.remove();
    }

    renpyAudio._videoPrompt = null;
};

renpyAudio._web_video_prompt = 'Click to play the video.';
