// Loads a generated index.html headless and evaluates its runtime formulas on the cases given on stdin.
const fs=require('fs'),vm=require('vm');
const html=fs.readFileSync(process.argv[2],'utf8');
const cfg=/<script type="application\/json" id="game-config">([\s\S]*?)<\/script>/.exec(html)[1];
const blocks=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const noop=()=>{};const ctx2d=new Proxy({},{get:(t,k)=>k in t?t[k]:noop,set:(t,k,v)=>{t[k]=v;return true;}});
const win={__HEADLESS__:true,requestAnimationFrame:()=>0,cancelAnimationFrame:noop,addEventListener:noop,localStorage:{getItem:()=>null,setItem:noop},
  document:{getElementById:id=>id==='game-config'?{textContent:cfg}:id==='game'?{getContext:()=>ctx2d}:{style:{}},querySelectorAll:()=>[]}};
win.window=win;vm.createContext(win);for(const b of blocks)vm.runInContext(b,win);
const G=win.__GAME__;const c=JSON.parse(fs.readFileSync(0,'utf8'));const out={};
let s={x:0,y:0,yaw:0,v:0};for(const k of c.car){for(let i=0;i<k.repeat;i++)s=G.carStep(s,k.acceleration,k.steer_deg);}out.car=s;
out.boxes=c.boxes.map(b=>G.circleBox(b[0],b[1],b[2],b[3],b[4],1,1));
const p=c.pursuit,a=G.agent(p.vehicle.x,p.vehicle.y,p.vehicle.max_speed,p.vehicle.max_force);a.vx=p.vehicle.vx;a.vy=p.vehicle.vy;
const hv=Math.hypot(a.vx,a.vy);if(hv*hv>1e-8){a.hx=a.vx/hv;a.hy=a.vy/hv;}
const e={x:p.evader.x,y:p.evader.y,vx:p.evader.vx,vy:p.evader.vy};const he=Math.hypot(e.vx,e.vy);const ed=he*he>1e-8?[e.vx/he,e.vy/he]:[0,1];
for(let i=0;i<p.steps;i++){G.integrate(a,G.pursuitF(a,e.x,e.y,e.vx,e.vy,ed[0],ed[1],1));e.x+=e.vx*G.config.loop.timestep_ms/1000;e.y+=e.vy*G.config.loop.timestep_ms/1000;}
out.pursuit={x:a.x,y:a.y,vx:a.vx,vy:a.vy};
G.state.money=777;G.state.player.x=3.14159;G.state.wanted.stars=2;G.state.wanted.heat=61.25;out.envelope=G.envelope();
out.fnv=c.fnv.map(t=>G.fnv(t));
process.stdout.write(JSON.stringify(out));
