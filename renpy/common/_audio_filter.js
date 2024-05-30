/* Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

let afidToFilter = {0 : null};

/**
 * Given an afid, return the filter associated with it. Returns null if the
 * filter is not found.
 *
 * @param {number} afid
 */
renpyAudio.getFilter = function (afid) {
    return afidToFilter[afid] || null;
}

/**
 * Associate a filter with an afid.
 */
renpyAudio.allocateFilter = function (afid, filter) {
    afidToFilter[afid] = filter;
}

/**
 * Disassociate a filter with an afid.
 */
renpyAudio.deallocateFilter = function (afid) {
    delete afidToFilter[afid];
}

/**
 * Connect a filter to a source and destination.
 */
renpyAudio.connectFilter = function (filter, source, destination) {

    if (filter === null) {
        source.connect(destination);
        return;
    }

    for (let input of filter.inputs) {
        source.connect(input);
    }

    for (let output of filter.outputs) {
        output.connect(destination);
    }

}

/**
 * Disconnect a filter from a source and destination.
 */
renpyAudio.disconnectFilter = function (filter, source, destination) {
    if (filter === null) {
        source.disconnect(destination);
        return;
    }

    for (let input of filter.inputs) {
        source.disconnect(input);
    }

    for (let output of filter.outputs) {
        output.disconnect(destination);
    }
}


renpyAudio.filter = { }
let filter = renpyAudio.filter;

/**
 * Connects a filter to a filter.
 */
filter.filterToFilter = function (filter1, filter2) {
    for (let output of filter1.outputs) {
        for (let input of filter2.inputs) {
            output.connect(input);
        }
    }
}


/**
 * Connects a filter to a node.
 */
filter.filterToNode = function(filter, node) {
    for (let output of filter.outputs) {
        output.connect(node);
    }
};

/**
 * Connects a node to a filter.
 */
filter.nodeToFilter = function(node, filter) {
    for (let input of filter.inputs) {
        node.connect(input);
    }
}

filter.Null = function() {
    let node = new GainNode(renpyAudio.context, { gain: 1 });

    return {
        inputs: [ node ],
        outputs: [ node ],
    };
}

filter.Crossfade = function(afid1, afid2, t) {
    let filter1 = renpyAudio.getFilter(afid1);
    let filter2 = renpyAudio.getFilter(afid2);

    let gain1 = new GainNode(renpyAudio.context, { gain: 1 });
    let gain2 = new GainNode(renpyAudio.context, { gain: 0 });

    filter.filterToNode(filter1, gain1);
    filter.filterToNode(filter2, gain2);

    gain1.gain.linearRampToValueAtTime(0, renpyAudio.context.currentTime + t);
    gain2.gain.linearRampToValueAtTime(1, renpyAudio.context.currentTime + t);

    return {
        inputs: [ ...filter1.inputs, ...filter2.inputs ],
        outputs: [gain1, gain2],
    };
};


filter.Biquad = function(kind, frequency, Q, gain) {
    let node = new BiquadFilterNode(renpyAudio.context, {
        type: kind,
        frequency: frequency,
        Q: Q,
        gain: gain
    });

    return {
        inputs: [node],
        outputs: [node],
    };
};

filter.Sequence = function(...filters) {
    let first = filters[0];
    let last = filters[filters.length - 1];

    for (let i = 0; i < filters.length - 1; i++) {
        filter.filterToFilter(filters[i], filters[i + 1]);
    }

    return {
        inputs: first.inputs,
        outputs: last.outputs,
    };
}

filter.Mix = function(...filters) {
    let inputs = [];
    let outputs = [];

    for (let f of filters) {
        inputs.push(...f.inputs);
        outputs.push(...f.outputs);
    }

    return {
        inputs: inputs,
        outputs: outputs,
    };
}

filter.Multiply = function(factor) {
    let node = new GainNode(renpyAudio.context, { gain: factor });

    return {
        inputs: [node],
        outputs: [node],
    };
}


filter.Delay = function(delay) {

    if (typeof delay !== "number") {
        delay = delay[0];
    }

    let node = new DelayNode(renpyAudio.context, { delayTime: delay });

    return {
        inputs: [node],
        outputs: [node],
    };
}

filter.Comb = function(delay, child, multiplier, wet) {
    if (typeof delay !== "number") {
        delay = delay[0];
    }

    let delayNode = new DelayNode(renpyAudio.context, { delayTime: delay });
    let multiplierNode = new GainNode(renpyAudio.context, { gain: multiplier });


    filter.nodeToFilter(delayNode, child);
    filter.filterToNode(child, multiplierNode);
    multiplierNode.connect(delayNode);

    let rv = {
        inputs: [ delayNode ],
        outputs: [ multiplierNode ],
    };

    if (wet) {
        let gainNode = new GainNode(renpyAudio.context, { gain: 1.0 - wet });
        inputs.push(gainNode);
        outputs.push(gainNode);
    }


    return rv;
}


filter.WetDry = function(child, wet, dry) {
    let wetNode = new GainNode(renpyAudio.context, { gain: wet });
    let dryNode = new GainNode(renpyAudio.context, { gain: dry });

    filter.filterToNode(child, wetNode);

    return {
        inputs: [...child.inputs, dryNode],
        outputs: [wetNode, dryNode],
    };
}
