// Runs the pinned upstream simplify.js on JSON inputs read from stdin; no network.
'use strict';
var path = require('path');
var simplify = require(path.join(__dirname, '..', 'upstream', 'simplify.js'));
var inputs = JSON.parse(require('fs').readFileSync(0, 'utf8'));
var out = inputs.map(function (p) {
    var pts = p.points.map(function (q, i) { return {x: q[0], y: q[1], i: i}; });
    var res = simplify(pts, p.tolerance, p.highest_quality);
    return {points: res.map(function (q) { return [q.x, q.y]; }),
            kept_indices: res.map(function (q) { return q.i; }),
            input_count: pts.length, output_count: res.length};
});
process.stdout.write(JSON.stringify(out));
