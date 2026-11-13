// Execute pinned MainLoop.js (src/mainloop.js) with a scripted requestAnimationFrame clock.
const path=require('path');
const SRC=path.join(__dirname,'..','upstream','src','mainloop.js');
const cases=JSON.parse(require('fs').readFileSync(0,'utf8'));
const out=[];
for(const p of cases){
  let queue=[];
  globalThis.window={requestAnimationFrame:cb=>{queue.push(cb);return queue.length},cancelAnimationFrame:()=>{}};
  delete require.cache[require.resolve(SRC)];
  const ML=require(SRC);
  const ts=p.timestep_ms===undefined?1000/60:p.timestep_ms;
  ML.setSimulationTimestep(ts);
  if(p.max_fps!==undefined)ML.setMaxAllowedFPS(p.max_fps);
  let updates=0,alpha=null,frames=[],cur=null,total=0,discarded=0;
  ML.setUpdate(()=>{updates++;total++;});
  ML.setDraw(a=>{alpha=a;});
  ML.setEnd((fps,panic)=>{cur={fps:fps,panic:panic};if(panic&&p.discard_on_panic){discarded+=ML.resetFrameDelta();}});
  ML.start();
  const T=p.frame_timestamps_ms;
  // first callback: the start frame (draw(1) only)
  let cb=queue.shift();cb(T[0]);
  frames.push({t:T[0],ran:true,updates:0,alpha:1,fps:60,panic:false,start:true});
  for(let i=1;i<T.length;i++){
    cb=queue.shift();updates=0;alpha=null;cur=null;cb(T[i]);
    if(cur===null)frames.push({t:T[i],ran:false,updates:0,alpha:null,fps:null,panic:false,start:false});
    else frames.push({t:T[i],ran:true,updates:updates,alpha:alpha,fps:cur.fps,panic:cur.panic,start:false});
  }
  ML.stop();
  out.push({frames:frames,total_updates:total,simulated_ms:total*ts,discarded_ms:discarded,panic_frames:frames.filter(f=>f.panic).length});
}
process.stdout.write(JSON.stringify(out));
