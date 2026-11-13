// Runs pinned upstream geolib v2.0.24 (getDistance via orderByDistance) on JSON inputs from stdin; no network.
// Dataset reading and category filtering are re-implemented here independently of the Python port.
'use strict';
var path = require('path'), fs = require('fs');
var geolib = require(path.join(__dirname, '..', 'upstream', 'src', 'geolib.js'));
var dataDir = process.env.SKILLPACK_MAP_DATA || path.join(__dirname, '..', 'tests', 'fixtures');
var inputs = JSON.parse(fs.readFileSync(0, 'utf8'));
var out = inputs.map(function (p) {
  var fc = JSON.parse(fs.readFileSync(path.join(dataDir, p.dataset + '_places.geojson'), 'utf8'));
  var cats = p.categories || [], radius = p.radius_m === undefined ? 1000 : p.radius_m;
  var rows = [];
  fc.features.forEach(function (f) {
    var pr = f.properties || {};
    if (!f.geometry || f.geometry.type !== 'Point' || !pr.name) return;
    if (cats.length && cats.indexOf(pr.category) < 0) return;
    if (p.name_contains && String(pr.name).toLowerCase().indexOf(p.name_contains.toLowerCase()) < 0) return;
    if (p.operation === 'nearby' && !cats.length && pr.category === 'street' && !p.include_streets) return;
    rows.push({latitude: f.geometry.coordinates[1], longitude: f.geometry.coordinates[0], name: pr.name, category: pr.category});
  });
  var ordered = geolib.orderByDistance({latitude: p.center.lat, longitude: p.center.lon}, rows);
  var inside = ordered.filter(function (r) { return r.distance <= radius; });
  if (p.operation === 'categories') {
    var c = {}; inside.forEach(function (r) { c[r.category] = (c[r.category] || 0) + 1; });
    var top = Object.keys(c).map(function (k) { return {category: k, count: c[k]}; });
    top.sort(function (a, b) { return b.count - a.count || (a.category < b.category ? -1 : 1); });
    return {operation: 'categories', categories: top};
  }
  var lim = p.limit === undefined ? 10 : p.limit;
  return {operation: 'nearby', found_within_radius: inside.length,
          results: inside.slice(0, lim).map(function (r) { return {name: r.name, category: r.category, distance_m: r.distance}; })};
});
process.stdout.write(JSON.stringify(out));
