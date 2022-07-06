/* Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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

/**
 * A map from channel to channel object.
 */
let channels = { };

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
        p.source.start(0, p.start, p.end);
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

renpyAudio = { };


renpyAudio.queue = (channel, file, name,  paused, fadein, tight, start, end, relative_volume) => {

    const c = get_channel(channel);

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
    stop_playing(c);
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
    pause_playing(c);
};


renpyAudio.unpause = (channel) => {
    let c = get_channel(channel);
    start_playing(c);
};


renpyAudio.unpauseAllAtStart = () => {
    for (let i of Object.entries(channels)) {
        if (i[1].playing && ! i[1].playing.started_once ) {
            start_playing(i[1]);
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
        rv += (context.currentTime - p.started);
    }

    return rv * 1000;
};


renpyAudio.get_duration = (channel) => {
    let c = get_channel(channel);
    let p = c.playing;

    if (p.buffer) {
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
    return c.primary_volume.gain * 1000;
};


renpyAudio.set_pan = (channel, pan, delay) => {

    let c = get_channel(channel);
    let control = c.stereo_pan.pan;

    linearRampToValue(control, control.value, pan, delay);
};

renpyAudio.tts = (s) => {
    console.log("tts: " + s);

    let u = new SpeechSynthesisUtterance(s);
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
