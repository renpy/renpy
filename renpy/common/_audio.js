/* Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

/**
 * A map from channel to channel object.
 */
let channels = { };
let next_chan_id = 0;

let context = new AudioContext();

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
        playing : null,
        queued : null,
        stereo_pan : context.createStereoPanner(),
        fade_volume : context.createGain(),
        primary_volume : context.createGain(),
        secondary_volume : context.createGain(),
        relative_volume : context.createGain(),
        paused : false,
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
 * Given an audio parameter, linearly ramps it from start to end over
 * duration seconds.
 */
let linearRampToValue = (param, start, end, duration) => {
    param.cancelScheduledValues(context.currentTime);

    let points = 30;

    for (let i = 0; i <= points; i++) {
        let done = i / points;
        param.setValueAtTime(interpolate(start, end, done), context.currentTime + interpolate(0, duration, done));
    }
}

/**
 * Given an audio parameter, sets it to the given value.
 */
let setValue= (param, value) => {
    param.cancelScheduledValues(context.currentTime);
    param.setValueAtTime(value, context.currentTime);
}

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

    if (c.paused) {
        return;
    }

    context.resume();
    p.source.connect(c.destination);

    if (p.fadeout === null) {
        if (p.fadein > 0) {
            linearRampToValue(c.fade_volume.gain, c.fade_volume.gain.value, 1.0, p.fadein);
        } else {
            setValue(c.fade_volume.gain, 1.0);
        }
    }

    if (p.end >= 0) {
        p.source.start(0, p.start, p.end - p.start);
    } else {
        p.source.start(0, p.start);
    }

    if (p.fadeout !== null) {
        linearRampToValue(c.fade_volume.gain, c.fade_volume.gain.value, 0.0, p.fadeout);
        try {
            c.playing.source.stop(context.currentTime + p.fadeout);
        } catch (e) {
        }

    }

    setValue(c.relative_volume.gain, p.relative_volume);

    p.started = context.currentTime;
    p.started_once = true;
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

    p.start += (context.currentTime - p.started);
    p.started = null;
}


/**
 * Stops playing channel `c`.
 */
let stop_playing = (c) => {


    if (c.playing !== null && c.playing.source !== null) {
        try {
            c.playing.source.stop()
        } catch (e) {
        }

        c.playing.source.disconnect();
    }

    c.playing = c.queued;
    c.queued = null;
};


/**
 * Called when a channel ends naturally, to move things along.
 */
let on_end = (c) => {
    if (c.playing !== null && c.playing.started !== null) {
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
                }).catch( (e) => {
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

    setValue(c.relative_volume.gain, p.relative_volume);

    p.started = c.video_el.currentTime;  // XXX Probably not ready yet
    p.started_once = true;
};

let video_pause = (c) => {
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

renpyAudio = { };


renpyAudio.queue = (channel, file, name,  paused, fadein, tight, start, end, relative_volume) => {

    const c = get_channel(channel);

    if (file.startsWith('url:')) {
        const url = new URL(file.slice(4), window.location);
        if (!c.video) {
            throw new Error('URL resources are only supported for videos');
        }

        const q = {
             url: url,
             name : name,
             start : start,  // TODO?
             end : end,  // TODO?
             relative_volume : relative_volume,
             started : null,
             fadein : fadein,  // TODO?
             fadeout: null,  // TODO?
             tight : tight,  // TODO?
             started_once: false,

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
            c.video_el.playsInline = true;  // For autoplay on Safari
            document.body.appendChild(c.video_el);

            c.video_el.addEventListener('loadedmetadata', function() {
                c.video_size = [c.video_el.videoWidth, c.video_el.videoHeight];
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

            c.video_el.addEventListener('playing', function() {
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
            c.paused = paused;
        } else {
            c.queued = q;
        }

        video_start(c);
        return;
    }

    const q = {
        source : null,
        buffer : null,
        name : name,
        start : start,
        end : end,
        relative_volume : relative_volume,
        started : null,
        fadein : fadein,
        fadeout: null,
        tight : tight,
        started_once : false,
        file: file,
    };

    function reuseBuffer(c) {
        // We can re-use the audio buffer, but not the buffer source
        c.queued.buffer = c.playing.buffer;
        c.queued.source = context.createBufferSource();
        c.queued.source.buffer = c.playing.buffer;
        c.queued.source.onended = () => { on_end(c); };

        start_playing(c);
    }

    if (c.playing === null) {
        c.playing = q;
        c.paused = paused;
    } else {
        c.queued = q;
        if (c.playing.file === file) {
            // Same file, re-use the data to reduce memory and CPU footprint
            if (c.playing.buffer !== null) {
                reuseBuffer(c);
            } else {
                // Not ready yet, wait for decodeAudioData() to complete
            }

            return;
        }
    }

    const array = FS.readFile(file);
    context.decodeAudioData(array.buffer, (buffer) => {

        const source = context.createBufferSource();
        source.buffer = buffer;
        source.onended = () => { on_end(c); };

        q.source = source;
        q.buffer = buffer;

        start_playing(c);

        if (c.playing === q && c.queued !== null && c.queued.file === q.file) {
            // Same file, re-use the data to reduce memory and CPU footprint
            reuseBuffer(c);
        }
    }, () => {
        console.log(`The audio data in ${file} could not be decoded. The file format may not be supported by this browser.`);
    });
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
    if (c.playing == null || c.playing.started == null) {
        c.playing = c.queued;
        c.queued = null;
        start_playing(c);
        return;
    }

    let p = c.playing;

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

    let remaining = delay + context.currentTime - p.started - p.buffer.duration;

    if (remaining > 0 && c.queued) {
        c.queued.fadeout = remaining;
    } else {
        c.queued = null;
    }

};

renpyAudio.queue_depth = (channel) => {
    let rv = 0;
    let c = get_channel(channel);

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
    if (c.video) {
        video_start(c);
    } else {
        start_playing(c);
    }
};


renpyAudio.unpauseAllAtStart = () => {
    for (let i of Object.entries(channels)) {
        const c = i[1];
        if (c.playing && ! c.playing.started_once && c.paused) {
            c.paused = false;
            if (c.video) {
                video_start(c);
            } else {
                start_playing(c);
            }
        }
    }
};


renpyAudio.get_pos = (channel) => {

    let c = get_channel(channel);
    let p = c.playing;

    if (p === null) {
        return 0;
    }

    let rv = p.start;

    if (p.started !== null) {
        if (c.video) {
            rv += c.video_el.currentTime - p.started;
        } else {
            rv += (context.currentTime - p.started);
        }
    }

    return rv * 1000;
};


renpyAudio.get_duration = (channel) => {
    let c = get_channel(channel);
    let p = c.playing;

    if (c.video) {
        if (c.video_el) {
            const duration = c.video_el.duration;
            if (Number.isFinite(duration)) {
                return duration * 1000;
            }
        }
    } else if (p.buffer) {
        return p.buffer.duration * 1000;
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
    return c.primary_volume.gain * 1000;
};


renpyAudio.set_pan = (channel, pan, delay) => {

    let c = get_channel(channel);
    let control = c.stereo_pan.pan;

    linearRampToValue(control, control.value, pan, delay);
};

renpyAudio.tts = (s, v) => {
    console.log("tts:", s, "volume:", v);

    v = v || 1.0;

    let u = new SpeechSynthesisUtterance(s);
    u.volume = v;
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
};

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

renpyAudio.set_video = (channel, video, loop) => {
    const c = get_channel(channel);
    c.video = !!video;
    c.loop = !!loop;
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
    renpyAudio._nodump = {'queue_depth': 1, 'playing_name': 1, 'video_ready': 1, 'read_video': 1};
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
//TODO? renpy_get('config.web_video_prompt').then((msg) => {
//TODO?     renpyAudio._web_video_prompt = msg;
//TODO? });
