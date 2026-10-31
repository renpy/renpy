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

// Run with node --test testcases/pytests/test_voice_speed_web.js.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

class Buffer {
    constructor(channels, length, sampleRate) {
        this.numberOfChannels = channels;
        this.length = length;
        this.sampleRate = sampleRate;
        this.duration = length / sampleRate;
        this.data = Array.from({length: channels}, () => new Float32Array(length));
    }
    getChannelData(ch) { return this.data[ch]; }
}

function backend() {
    class Context {
        constructor() { this.currentTime = 0; this.state = 'running'; this.destination = {}; }
        createBuffer(...args) { return new Buffer(...args); }
        createBufferSource() {
            return {start(...args) { this.arguments = args; }, stop(...args) { this.stopArguments = args; }, connect() {}, disconnect() {}};
        }
        createStereoPanner() { return this.createGain(); }
        createGain() { return {gain: {value: 1, cancelScheduledValues() {}, setValueAtTime() {}}, connect() {}}; }
        resume() { return Promise.resolve(); }
        decodeAudioData(data, callback) { callback(this.decoded); }
    }
    const sandbox = {AudioContext: Context, HTMLVideoElement: class {}, speechSynthesis: null, performance, setTimeout, console};
    vm.createContext(sandbox);
    vm.runInContext(fs.readFileSync(path.join(__dirname, '../../renpy/common/_audio.js'), 'utf8'), sandbox);
    const audio = sandbox.renpyAudio;
    audio.getFilter = () => null;
    audio.connectFilter = () => {};
    audio.disconnectFilter = () => {};
    return {audio, stretch: vm.runInContext('stretch_buffer', sandbox), channel: n => vm.runInContext(`get_channel(${n})`, sandbox)};
}

function tone(rate = 48000, channels = 2) {
    const buffer = new Buffer(channels, Math.round(rate * 1.2), rate);
    for (let i = 0; i < buffer.length; i++) {
        buffer.data[0][i] = 0.5 * Math.sin(2 * Math.PI * 440 * i / rate);
        for (let ch = 1; ch < channels; ch++) buffer.data[ch][i] = -buffer.data[0][i];
    }
    return buffer;
}

function frequency(buffer) {
    const pcm = buffer.data[0];
    const crossings = [];
    for (let i = Math.floor(pcm.length / 5); i < pcm.length * 4 / 5; i++) {
        if (pcm[i - 1] <= 0 && pcm[i] > 0) crossings.push(i);
    }
    assert.ok(crossings.length > 5);
    return (crossings.length - 1) * buffer.sampleRate / (crossings.at(-1) - crossings[0]);
}

async function ready(channel) {
    const deadline = performance.now() + 5000;
    while (!channel.playing?.source || channel.queued && !channel.queued.source) {
        assert.ok(performance.now() < deadline, 'Audio preparation timed out');
        await new Promise(resolve => setTimeout(resolve, 1));
    }
}

for (const rate of [22050, 44100, 48000]) {
    for (const speed of [0.5, 1, 1.5, 2, 3]) {
        test(`duration, pitch and opposite-phase stereo at ${rate} Hz, ${speed}x`, async () => {
            const {stretch} = backend();
            const input = tone(rate);
            const output = await stretch(input, speed);
            assert.ok(Math.abs(output.duration - input.duration / speed) < 1 / rate);
            assert.ok(Math.abs(frequency(output) - 440) < 2);
            for (let i = 0; i < output.length; i++) {
                assert.ok(Number.isFinite(output.data[0][i]));
                assert.ok(output.data[0][i] === -output.data[1][i]);
            }
            if (speed === 1) assert.equal(output, input);
        });
    }
}

test('silent and very short voices remain finite', async () => {
    const {stretch} = backend();
    for (const size of [1, 17, 1920]) {
        for (const speed of [0.5, 3]) {
            const output = await stretch(new Buffer(1, size, 48000), speed);
            assert.ok(output.data[0].every(sample => sample === 0));
        }
    }
});

test('queue captures independent rates and preserves source clocks through pause and seek', async () => {
    const {audio, channel} = backend();
    audio.context.decoded = tone();
    audio.queue(0, 'tone.wav', 'tone.wav', false, 0, false, 0.1, 1.1, 1, null, [1], 2);
    await ready(channel(0));
    const first = channel(0).playing;
    assert.equal(first.source.arguments[1], 0.05);
    assert.equal(first.source.arguments[2], 0.5);
    audio.queue(0, 'tone.wav', 'tone.wav', false, 0, false, 0, -1, 1, null, [1], 0.5);
    await ready(channel(0));
    assert.equal(channel(0).queued.playback_speed, 0.5);
    assert.equal(channel(0).playing.playback_speed, 2);
    assert.notEqual(channel(0).queued.buffer, first.buffer);
    audio.context.currentTime = 0.2;
    assert.equal(audio.get_pos(0), 500);
    assert.equal(audio.get_duration(0), 1200);
    audio.pause(0);
    audio.context.currentTime = 1;
    assert.equal(audio.get_pos(0), 500);
    audio.seek(0, 0.7);
    audio.unpause(0);
    assert.equal(first.source.arguments[1], 0.35);
    audio.context.currentTime = 1.1;
    assert.ok(Math.abs(audio.get_pos(0) - 900) < 1e-6);
    first.source.onended();
    assert.equal(channel(0).playing.playback_speed, 0.5);
    audio.stop(0);
    assert.equal(audio.queue_depth(0), 0);
});

test('stopping during preparation cannot restart a stale voice', async () => {
    const {audio, channel} = backend();
    audio.context.decoded = tone();
    audio.queue(0, 'tone.wav', 'tone.wav', false, 0, false, 0, -1, 1, null, [1], 0.5);
    audio.stop(0);
    await new Promise(resolve => setTimeout(resolve, 100));
    assert.equal(channel(0).playing, null);
});

test('explicit end excludes following source audio from stretching', async () => {
    const {stretch} = backend();
    const input = new Buffer(2, 48000, 48000);
    input.data[0].fill(0.8, 24000);
    input.data[1].fill(0.8, 24000);
    const output = await stretch(input, 0.5, 0.5);
    assert.equal(output.duration, 1);
    assert.ok(output.data[0].every(sample => sample === 0));
});


test('queue promotion during decoding still prepares the promoted request', async () => {
    const {audio, channel} = backend();
    let decoded;
    audio.context.decodeAudioData = (data, callback) => { decoded = callback; };
    audio.queue(0, 'tone.wav', 'tone.wav', false, 0, false, 0, -1, 1, null, [1], 2);
    audio.queue(0, 'tone.wav', 'tone.wav', false, 0, false, 0, -1, 1, null, [1], 0.5);
    audio.fadeout(0, 0);
    decoded(tone());
    await ready(channel(0));
    assert.equal(channel(0).playing.playback_speed, 0.5);
    assert.equal(channel(0).playing.buffer.duration, 2.4);
});


async function rateReady(channel) {
    const deadline = performance.now() + 5000;
    while (!channel.playing?.source || channel.playing.preparing || channel.playing.playback_speed !== channel.playing.requested_speed) {
        assert.ok(performance.now() < deadline, 'Live rate change timed out');
        await new Promise(resolve => setTimeout(resolve, 1));
    }
}

test('live rates preserve source position, pitch, queue rates and paused state', async () => {
    const {audio, channel} = backend();
    audio.context.decoded = tone();
    audio.queue(0, 'tone.wav', 'tone.wav', false, 0, false, 0, -1, 1, null, [1], 1);
    await ready(channel(0));
    audio.queue(0, 'tone.wav', 'tone.wav', false, 0, false, 0, -1, 1, null, [1], 0.5);
    await ready(channel(0));
    const playing = channel(0).playing, originalSource = playing.source;
    audio.context.currentTime = 0.2;
    audio.set_playback_speed(0, 2);
    await rateReady(channel(0));
    assert.equal(audio.get_pos(0), 200);
    assert.equal(audio.get_playback_speed(0), 2000);
    assert.equal(playing.source.arguments[1], 0.1);
    assert.ok(Math.abs(frequency(playing.buffer) - 440) < 2);
    assert.equal(channel(0).queued.playback_speed, 0.5);
    originalSource.onended();
    assert.equal(channel(0).playing, playing);
    audio.context.currentTime = 0.3;
    assert.ok(Math.abs(audio.get_pos(0) - 400) < 1e-6);
    audio.pause(0);
    audio.set_playback_speed(0, 0.5);
    await rateReady(channel(0));
    assert.equal(channel(0).paused, true);
    assert.ok(Math.abs(audio.get_pos(0) - 400) < 1e-6);
    audio.unpause(0);
    audio.context.currentTime = 0.5;
    assert.ok(Math.abs(audio.get_pos(0) - 500) < 1e-6);
});

test('rapid slider updates apply only the latest requested rate', async () => {
    const {audio, channel} = backend();
    audio.context.decoded = tone();
    audio.queue(0, 'tone.wav', 'tone.wav', false, 0, false, 0, -1, 1, null, [1], 1);
    await ready(channel(0));
    audio.context.currentTime = 0.4;
    for (const rate of [0.5, 3, 1, 2, 0.75]) audio.set_playback_speed(0, rate);
    await rateReady(channel(0));
    assert.equal(audio.get_playback_speed(0), 750);
    assert.equal(audio.get_pos(0), 400);
    assert.equal(channel(0).playing.buffer.duration, 1.6);
});

test('rate changes before decoding use the latest rate', async () => {
    const {audio, channel} = backend();
    let decoded;
    audio.context.decodeAudioData = (data, callback) => { decoded = callback; };
    audio.queue(0, 'tone.wav', 'tone.wav', false, 0, false, 0, -1, 1, null, [1], 1);
    audio.set_playback_speed(0, 3);
    audio.set_playback_speed(0, 0.75);
    decoded(tone());
    await rateReady(channel(0));
    assert.equal(channel(0).playing.buffer.duration, 1.6);
});

test('live changes keep an existing fadeout deadline', async () => {
    const {audio, channel} = backend();
    audio.context.decoded = tone();
    audio.queue(0, 'tone.wav', 'tone.wav', false, 0, false, 0, -1, 1, null, [1], 1);
    await ready(channel(0));
    audio.fadeout(0, 1);
    audio.context.currentTime = 0.2;
    audio.set_playback_speed(0, 2);
    await rateReady(channel(0));
    assert.equal(channel(0).playing.source.stopArguments[0], 1);
});

for (const speed of [0.5, 1, 2]) {
    test(`tight queue keeps its fade deadline after a live change to ${speed}x`, async () => {
        const {audio, channel} = backend();
        audio.context.decoded = tone();
        audio.queue(0, 'first.wav', 'first.wav', false, 0, true, 0, -1, 1, null, [1], 1);
        await ready(channel(0));
        audio.queue(0, 'next.wav', 'next.wav', false, 0, true, 0, -1, 1, null, [1], 1);
        await ready(channel(0));
        const queued = channel(0).queued;
        audio.fadeout(0, 2);
        audio.context.currentTime = 0.2;
        audio.set_playback_speed(0, speed);
        await rateReady(channel(0));

        // The playing clip ends either naturally or at the fade's deadline.
        audio.context.currentTime = Math.min(2, 0.2 + (1.2 - 0.2) / speed);
        channel(0).playing.source.onended();
        assert.equal(channel(0).playing, queued);
        assert.equal(queued.playback_speed, 1);
        assert.equal(queued.source.stopArguments[0], 2);
        assert.equal(queued.fadeout_deadline, 2);
    });
}
