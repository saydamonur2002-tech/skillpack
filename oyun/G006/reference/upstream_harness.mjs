// Execute pinned Yuka (src/) steering on each reference input. 2D (x,y) maps to Yuka (x,0,y).
import {readFileSync} from 'fs';
const U=new URL('../upstream/src/',import.meta.url);
const {Vehicle}=await import(new URL('steering/Vehicle.js',U));
const {MovingEntity}=await import(new URL('core/MovingEntity.js',U));
const {Vector3}=await import(new URL('math/Vector3.js',U));
const B=n=>import(new URL('steering/behaviors/'+n+'.js',U));
const {SeekBehavior}=await B('SeekBehavior');const {FleeBehavior}=await B('FleeBehavior');const {ArriveBehavior}=await B('ArriveBehavior');const {PursuitBehavior}=await B('PursuitBehavior');
function face(ent,vx,vy,h){
  if(h!==undefined){ent.lookAt(new Vector3(ent.position.x+Math.sin(h),0,ent.position.z+Math.cos(h)));return;}
  if(vx*vx+vy*vy>1e-8)ent.lookAt(new Vector3(ent.position.x+vx,0,ent.position.z+vy));
}
const out=[];
for(const p of JSON.parse(readFileSync(0,'utf8'))){
  const v=p.vehicle,prm=p.params||{};const veh=new Vehicle();
  veh.position.set(v.x,0,v.y);veh.velocity.set(v.vx||0,0,v.vy||0);
  veh.maxSpeed=v.max_speed===undefined?1:v.max_speed;veh.maxForce=v.max_force===undefined?100:v.max_force;veh.mass=v.mass===undefined?1:v.mass;
  face(veh,v.vx||0,v.vy||0,v.heading);
  let ev=null,tgt=null,beh;
  if(p.behavior==='pursuit'){const e=p.evader;ev=new MovingEntity();ev.position.set(e.x,0,e.y);ev.velocity.set(e.vx||0,0,e.vy||0);face(ev,e.vx||0,e.vy||0,e.heading);
    beh=new PursuitBehavior(ev,prm.prediction_factor===undefined?1:prm.prediction_factor);}
  else{tgt=new Vector3(p.target.x,0,p.target.y);
    beh=p.behavior==='seek'?new SeekBehavior(tgt):p.behavior==='flee'?new FleeBehavior(tgt,prm.panic_distance===undefined?10:prm.panic_distance):new ArriveBehavior(tgt,prm.deceleration===undefined?3:prm.deceleration,prm.tolerance||0);}
  veh.steering.add(beh);
  const dt=p.dt_s===undefined?1/60:p.dt_s,every=p.record_every||1,steps=p.steps||1;const traj=[];let mind=null;
  for(let i=1;i<=steps;i++){
    veh.update(dt);
    if(ev){const np=new Vector3().copy(ev.position).add(new Vector3().copy(ev.velocity).multiplyScalar(dt));face(ev,ev.velocity.x,ev.velocity.z);ev.position.copy(np);}
    const o=ev?ev.position:tgt;const d=Math.sqrt((o.x-veh.position.x)**2+(o.z-veh.position.z)**2);mind=mind===null?d:Math.min(mind,d);
    if(i%every===0)traj.push({step:i,x:veh.position.x,y:veh.position.z,vx:veh.velocity.x,vy:veh.velocity.z,distance:d});
  }
  out.push({behavior:p.behavior,steps:steps,final:{x:veh.position.x,y:veh.position.z,vx:veh.velocity.x,vy:veh.velocity.z,speed:veh.velocity.length()},trajectory:traj,min_distance:mind});
}
process.stdout.write(JSON.stringify(out));
