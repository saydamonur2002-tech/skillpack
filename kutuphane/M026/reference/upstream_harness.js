// Runs pinned upstream geolib v2.0.24 src/geolib.js on JSON inputs from stdin; no network.
'use strict';
var path = require('path');
var geolib = require(path.join(__dirname, '..', 'upstream', 'src', 'geolib.js'));
var inputs = JSON.parse(require('fs').readFileSync(0, 'utf8'));
function ring(r) { var o = r; if (r.length > 1 && r[0][0] === r[r.length-1][0] && r[0][1] === r[r.length-1][1]) o = r.slice(0, -1);
  return o.map(function (c) { return {latitude: c[1], longitude: c[0]}; }); }
function polys(g) { return g.type === 'Polygon' ? [g.coordinates] : g.coordinates; }
var out = inputs.map(function (p) {
  var ps = polys(p.geometry), outer = [];
  ps.forEach(function (poly) { outer = outer.concat(ring(poly[0])); });
  if (p.operation === 'contains') {
    return {operation: 'contains', results: p.points.map(function (pt) {
      var q = {latitude: pt.lat, longitude: pt.lon}, which = null;
      for (var k = 0; k < ps.length; k++) {
        if (geolib.isPointInside(q, ring(ps[k][0])) && !ps[k].slice(1).some(function (h) { return geolib.isPointInside(q, ring(h)); })) { which = k; break; }
      }
      return {lat: pt.lat, lon: pt.lon, inside: which !== null, polygon_index: which};
    })};
  }
  var b = geolib.getBounds(outer);
  if (p.operation === 'bbox') return {operation: 'bbox', bounds: b, bbox: [b.minLng, b.minLat, b.maxLng, b.maxLat]};
  var c = geolib.getCenter(outer);
  return {operation: 'center', center_of_bounds: geolib.getCenterOfBounds(outer),
          vertex_mean_center: {latitude: parseFloat(c.latitude), longitude: parseFloat(c.longitude)}};
});
process.stdout.write(JSON.stringify(out));
