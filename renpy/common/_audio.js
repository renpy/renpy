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
        paused : false,
    };

    c.destination = c.stereo_pan;
    c.stereo_pan.connect(c.fade_volume);
    c.fade_volume.connect(c.primary_volume);
    c.primary_volume.connect(c.secondary_volume);
    c.secondary_volume.connect(context.destination);

    channels[channel] = c;

    return c;
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

    if (c.paused) {
        return;
    }

    context.resume();
    p.source.connect(c.destination);

    if (p.fadeout === null) {
        let value = c.fade_volume.gain.value;
        c.fade_volume.gain.cancelScheduledValues(context.currentTime);
        c.fade_volume.gain.value = value;

        if (p.fadein > 0) {
            c.fade_volume.gain.value = 0.01;
            c.fade_volume.gain.linearRampToValueAtTime(1.0, context.currentTime + p.fadein);
        } else {
            c.fade_volume.gain.value = 1.0;
        }
    }

    if (p.end >= 0) {
        p.source.start(0, p.start, p.end);
    } else {
        p.source.start(0, p.start);
    }

    if (p.fadeout !== null) {
        let value = c.fade_volume.gain.value;
        c.fade_volume.gain.cancelScheduledValues(context.currentTime);
        c.fade_volume.gain.value = value;
        c.fade_volume.gain.linearRampToValueAtTime(0.0, context.currentTime + p.fadeout);
        c.playing.source.stop(context.currentTime + p.fadeout);
    }

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
    
    p.source.stop()
    p.start += (context.currentTime - p.started);
    p.started = null;
}


/**
 * Stops playing channel `c`.
 */
let stop_playing = (c) => {


    if (c.playing !== null && c.playing.source !== null) {
        c.playing.source.stop()
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


renpyAudio.queue = (channel, file, name,  paused, fadein, tight, start, end) => {

    let c = get_channel(channel);
    let array = FS.readFile(file);

    let q = { 
        source : null, 
        buffer : null,
        name : name, 
        start : start, 
        end : end, 
        started : null,
        fadein : fadein,
        fadeout: null,
        tight : tight
    };

    if (c.playing === null) {
        c.playing = q;
        c.paused = paused;
    } else {
        c.queued = q;
    }

    context.decodeAudioData(array.buffer, (buffer) => {

        var source = context.createBufferSource();
        source.buffer = buffer;
        source.onended = () => { on_end(c); };

        q.source = source;
        q.buffer = buffer;

        start_playing(c);
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

    let value = c.fade_volume.gain.value;
    c.fade_volume.gain.cancelScheduledValues(context.currentTime);
    c.fade_volume.gain.value = value;
    c.fade_volume.gain.linearRampToValueAtTime(0.0, context.currentTime + delay);
    p.source.stop(context.currentTime + delay);

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

// let oldChannel7 = -1;

renpyAudio.queue_depth = (channel) => {
    let rv = 0;
    let c = get_channel(channel);

    if (c.playing !== null) {
        rv += 1;
    }

    if (c.queued !== null) {
        rv += 1;
    }

    // if (channel == 7 && oldChannel7 != rv) {
    //     console.log(c.playing, c.queued);
    //     console.log("queue_depth", rv);
    //     oldChannel7 = rv;
    // }

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


renpyAudio.unpauseAll = () => {
    for (let i of Object.entries(channel)) {
        start_playing(i[1]);
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
    c.primary_volume.gain.value = volume;
};


renpyAudio.set_secondary_volume = (channel, volume, delay) => {
    let c = get_channel(channel);
    let control = c.secondary_volume.gain;

    let value = control.value;
    control.cancelScheduledValues(context.currentTime);
    control.value = value;
    control.linearRampToValueAtTime(volume, context.currentTime + delay);
};


renpyAudio.get_volume = (channel) => {
    return c.primary_volume.gain * 1000;
};


renpyAudio.set_pan = (channel, pan, delay) => {

    let c = get_channel(channel);
    let control = c.stereo_pan.pan;

    let value = control.value;
    control.cancelScheduledValues(context.currentTime);
    control.value = value;
    control.linearRampToValueAtTime(pan, context.currentTime + delay);
};

renpyAudio.tts = (s) => {
    console.log("tts: " + s);

    let u = new SpeechSynthesisUtterance(s);
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
};

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
