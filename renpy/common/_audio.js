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
        paused : false,
    };

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

    p.source.connect(context.destination);

    if (p.end >= 0) {
        p.source.start(0, p.start, p.end);
    } else {
        p.source.start(0, p.start);
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
    stop_playing(c);
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
        started : null
    };

    if (c.playing === null) {
        c.playing = q;
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
    });
};

renpyAudio.stop = (channel) => {
    let c = get_channel(channel);
    c.queued = null;
    stop_playing(c);
};

renpyAudio.dequeue = (channel) => {
    let c = get_channel(channel);
    c.queued = null;
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
};

renpyAudio.set_secondary_volume = (channel, volume) => {
};

renpyAudio.get_volume = (channel) => {
    return 1.0 * 1000;
};
