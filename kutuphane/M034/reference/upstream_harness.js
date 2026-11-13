// Runs pinned upstream mapbox/sphericalmercator v1.1.0 px/ll on JSON inputs from stdin; no network.
'use strict';
var path = require('path');
var SM = require(path.join(__dirname, '..', 'upstream', 'sphericalmercator.js'));
var merc = new SM({size: 256});
var inputs = JSON.parse(require('fs').readFileSync(0, 'utf8'));
var out = inputs.map(function (p) {
  if (p.operation === 'unproject') return {operation: 'unproject', zoom: p.zoom, lonlat: p.pixels.map(function (xy) { return merc.ll(xy, p.zoom); })};
  var px = p.points.map(function (q) { return merc.px([q.lon, q.lat], p.zoom); });
  return {operation: 'project', zoom: p.zoom, pixels: px, lonlat_roundtrip: px.map(function (xy) { return merc.ll(xy, p.zoom); })};
});
process.stdout.write(JSON.stringify(out));
