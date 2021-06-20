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

renpyAudio = { };


let playing = false;

renpyAudio.play = (channel, file, name, start, stop) => {

    if (playing) return;
    playing = true;

    let array = FS.readFile(file);
    let context = new AudioContext();
    let source = context.createBufferSource();

    context.decodeAudioData(array.buffer, (buffer) => {
        source.buffer = buffer;
        source.connect(context.destination)
        source.ended = () => { console.log("done.") };
        source.start(0);
    });
};

renpyAudio.queue = (channel, file, name, start, stop) => {
};

renpyAudio.stop = (channel) => {
};

renpyAudio.dequeue = (channel) => {
};

renpyAudio.queue_depth = (channel) => {
    return 0;
};

renpyAudio.playing_name = (channel) => {
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

