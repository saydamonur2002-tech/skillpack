// Execute pinned ZzFX.js ZZFX.buildSamples (randomness forced to 0) on each reference input.
import {readFileSync} from 'fs';
import {createHash} from 'crypto';
globalThis.AudioContext=class{constructor(){this.sampleRate=44100;}}; // no audio device needed to build samples
const {ZZFX}=await import(new URL('../upstream/ZzFX.js',import.meta.url));
const out=[];
for(const c of JSON.parse(readFileSync(0,'utf8'))){
  const P=c.params; const args=P.slice();args[1]=0;
  const b=ZZFX.buildSamples(...args);const n=b.length;
  let peak=0,ss=0;for(const x of b){peak=Math.max(peak,Math.abs(x));ss+=x*x;}
  const q=new Int16Array(n);for(let j=0;j<n;j++){const r=b[j]*32767;let v=Math.round(r);if(Math.abs(r%1)===0.5)v=2*Math.round(r/2);q[j]=Math.max(-32768,Math.min(32767,v));}
  const head=Array.from(b.slice(0,c.samples_head===undefined?8:c.samples_head));
  const at={};const idx=n>=16?[...Array(16).keys()].map(j=>j*Math.floor(n/16)):[...Array(n).keys()];for(const j of idx)at[String(j)]=b[j];
  out.push({params:P,sample_count:n,duration_s:n/44100,peak:peak,rms:n?Math.sqrt(ss/n):0,samples_head:head,samples_at:at,int16_sha256:createHash('sha256').update(Buffer.from(q.buffer)).digest('hex')});
}
process.stdout.write(JSON.stringify(out));
