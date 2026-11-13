// Runs pinned upstream mapbox/geojson-area index.js on JSON inputs from stdin; no network.
// index.js requires the npm module 'wgs84'; only its RADIUS constant (6378137) is used, provided here as a shim.
'use strict';
var path = require('path'), Module = require('module');
var realResolve = Module._resolveFilename;
var shim = path.join(__dirname, 'wgs84_shim.js');
require.cache[shim] = {id: shim, filename: shim, loaded: true, exports: {RADIUS: 6378137}};
Module._resolveFilename = function (req) { if (req === 'wgs84') return shim; return realResolve.apply(this, arguments); };
var area = require(path.join(__dirname, '..', 'upstream', 'index.js'));
var inputs = JSON.parse(require('fs').readFileSync(0, 'utf8'));
function rings(g) { if (g.type === 'Polygon') return [g.coordinates]; if (g.type === 'MultiPolygon') return g.coordinates;
  if (g.type === 'GeometryCollection') return [].concat.apply([], g.geometries.map(rings)); return []; }
var out = inputs.map(function (p) {
  if (p.operation === 'ring') { var a = area.ring(p.geometry.coordinates);
    return {operation: 'ring', signed_area_m2: a, orientation: a > 0 ? 'clockwise' : (a < 0 ? 'counterclockwise' : 'degenerate')}; }
  var A = area.geometry(p.geometry);
  return {operation: 'area', area_m2: A, area_ha: A / 1e4, area_km2: A / 1e6,
          ring_signed_areas_m2: rings(p.geometry).map(function (poly) { return poly.map(area.ring); })};
});
process.stdout.write(JSON.stringify(out));
