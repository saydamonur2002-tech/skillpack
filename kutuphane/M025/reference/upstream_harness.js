// Runs the pinned upstream node-geohash main.js on JSON inputs read from stdin; no network.
'use strict';
var path = require('path');
var geohash = require(path.join(__dirname, '..', 'upstream', 'main.js'));
var inputs = JSON.parse(require('fs').readFileSync(0, 'utf8'));
var names = ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest'];
var out = inputs.map(function (p) {
    if (p.operation === 'encode') {
        var n = p.length === undefined ? 9 : p.length;
        return {operation: 'encode', geohash: geohash.encode(p.latitude, p.longitude, n), length: n};
    }
    if (p.operation === 'decode') {
        var d = geohash.decode(p.geohash);
        return {operation: 'decode', geohash: p.geohash.toLowerCase(), latitude: d.latitude, longitude: d.longitude,
                error: d.error, bbox: geohash.decode_bbox(p.geohash)};
    }
    var list = geohash.neighbors(p.geohash), nb = {};
    names.forEach(function (k, i) { nb[k] = list[i]; });
    return {operation: 'neighbors', geohash: p.geohash.toLowerCase(), neighbors: nb, clockwise_from_north: list};
});
process.stdout.write(JSON.stringify(out));
