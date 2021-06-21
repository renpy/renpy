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
        primary_volume : 1.0,
        secondary_volume : 1.0,
    };


    channels[channel] = c;

    return c;
};

/**
 * Starts channel `c` playing, if it is not playing.
 */
let start_playing = (c) => {

    let p = c.playing;

    if (p === null) {
        return;
    }

    if (p.started) {
        return;
    }

    if (p.source === null) {
        return;
    }

    if (p.end >= 0) {
        p.source.start(0, p.start, p.end);
    } else {
        p.source.start(0, p.start);
    }

    p.started = true;
};

/**
 * Called when a channel ends naturally, to move things along.
 */
let on_end = (c) => {

    if (c.playing.source !== null) {
        c.playing.source.disconnect();
    }

    c.playing = c.queued;
    c.queued = null;

    start_playing(c);
};


renpyAudio = { };

renpyAudio.queue = (channel, file, name, start, end) => {

    let c = get_channel(channel);
    let array = FS.readFile(file);

    let q = { 
        source : null, 
        buffer : null,
        name : name, 
        start : start, 
        end : end, 
        started : false
    };

    if (c.playing === null) {
        c.playing = q;
    } else {
        c.queued = q;
    }

    context.decodeAudioData(array.buffer, (buffer) => {
        var source = context.createBufferSource();
        source.buffer = buffer;
        source.connect(context.destination);
        source.onended = () => { on_end(c); };

        q.source = source;
        q.buffer = buffer;

        start_playing(c);
    });
};

renpyAudio.stop = (channel) => {
};

renpyAudio.dequeue = (channel) => {
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
};


renpyAudio.unpause = (channel) => {
};


renpyAudio.unpauseAll = () => {
};

renpyAudio.get_pos = (channel) => {
    return 0.0 * 1000;
};


renpyAudio.get_duration = (channel) => {
    return 0.0 * 1000;
};


renpyAudio.set_volume = (channel, volume) => {
};

renpyAudio.set_secondary_volume = (channel, volume) => {
};

renpyAudio.get_volume = (channel) => {
    return 1.0 * 1000;
};

console.log("_audio.js loaded.");
