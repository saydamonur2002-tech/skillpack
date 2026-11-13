// Runs the pinned upstream polyline.js on JSON inputs read from stdin; no network.
'use strict';
var path = require('path');
var polyline = require(path.join(__dirname, '..', 'upstream', 'src', 'polyline.js'));
var inputs = JSON.parse(require('fs').readFileSync(0, 'utf8'));
var out = inputs.map(function (p) {
    var prec = p.precision === undefined ? 5 : p.precision;
    if (p.operation === 'encode') {
        return {operation: 'encode', precision: prec, encoded: polyline.encode(p.coordinates, prec), point_count: p.coordinates.length};
    }
    var c = polyline.decode(p.encoded, prec);
    return {operation: 'decode', precision: prec, coordinates: c, point_count: c.length};
});
process.stdout.write(JSON.stringify(out));
