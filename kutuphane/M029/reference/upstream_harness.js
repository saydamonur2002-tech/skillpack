// Runs pinned upstream mapbox/tilebelt v1.0.1 index.js on JSON inputs from stdin; no network.
'use strict';
var path = require('path');
var tb = require(path.join(__dirname, '..', 'upstream', 'index.js'));
var inputs = JSON.parse(require('fs').readFileSync(0, 'utf8'));
var out = inputs.map(function (p) {
  var op = p.operation, t = p.tile;
  switch (op) {
    case 'point_to_tile': var r = tb.pointToTile(p.lon, p.lat, p.zoom);
      return {operation: op, tile: r, quadkey: tb.tileToQuadkey(r), path: r[2] + '/' + r[0] + '/' + r[1]};
    case 'point_to_tile_fraction': return {operation: op, tile: tb.pointToTileFraction(p.lon, p.lat, p.zoom)};
    case 'quadkey_to_tile': return {operation: op, tile: tb.quadkeyToTile(p.quadkey)};
    case 'bbox_to_tile': return {operation: op, tile: tb.bboxToTile(p.bbox)};
    case 'tile_to_bbox': return {operation: op, bbox: tb.tileToBBOX(t)};
    case 'tile_to_geojson': return {operation: op, geometry: tb.tileToGeoJSON(t)};
    case 'tile_to_quadkey': return {operation: op, quadkey: tb.tileToQuadkey(t)};
    case 'children': return {operation: op, tiles: tb.getChildren(t)};
    case 'parent': return {operation: op, tile: tb.getParent(t)};
    case 'siblings': return {operation: op, tiles: tb.getSiblings(t)};
  }
});
process.stdout.write(JSON.stringify(out));
