// Runs pinned upstream chrisveness/geodesy latlon-spherical.js (ES module) on JSON inputs from stdin; no network.
import LatLon from '../upstream/latlon-spherical.js';
import { readFileSync } from 'node:fs';
const inputs = JSON.parse(readFileSync(0, 'utf8'));
const num = v => (Number.isNaN(v) ? null : v);
const out = inputs.map(p => {
  const R = p.radius_m === undefined ? 6371e3 : p.radius_m;
  const a = new LatLon(p.from.lat, p.from.lon);
  if (p.operation === 'destination') { const d = a.destinationPoint(p.distance_m, p.bearing_deg, R); return {operation: 'destination', lat: d.lat, lon: d.lon}; }
  const b = new LatLon(p.to.lat, p.to.lon);
  if (p.operation === 'bearing') return {operation: 'bearing', initial_bearing_deg: num(a.initialBearingTo(b)), final_bearing_deg: num(a.finalBearingTo(b))};
  if (p.operation === 'midpoint') { const m = a.midpointTo(b); return {operation: 'midpoint', lat: m.lat, lon: m.lon}; }
  if (p.operation === 'distance') return {operation: 'distance', distance_m: a.distanceTo(b, R)};
  return {operation: 'cross_track', cross_track_m: new LatLon(p.point.lat, p.point.lon).crossTrackDistanceTo(a, b, R)};
});
process.stdout.write(JSON.stringify(out));
