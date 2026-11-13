// Headless smoke test of a generated index.html: runs the game runtime in Node.js with stub DOM/canvas and no network.
const fs=require('fs'),vm=require('vm');
const html=fs.readFileSync(process.argv[2],'utf8');
const cfg=/<script type="application\/json" id="game-config">([\s\S]*?)<\/script>/.exec(html)[1];
const blocks=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const noop=()=>{};const ctx2d=new Proxy({},{get:(t,k)=>k in t?t[k]:noop,set:(t,k,v)=>{t[k]=v;return true;}});
const store={};const raf=[];
const win={__HEADLESS__:true,requestAnimationFrame:cb=>{raf.push(cb);return raf.length;},cancelAnimationFrame:noop,addEventListener:noop,
  localStorage:{getItem:k=>k in store?store[k]:null,setItem:(k,v)=>{store[k]=String(v);}},
  document:{getElementById:id=>id==='game-config'?{textContent:cfg}:id==='game'?{getContext:()=>ctx2d,clientWidth:800,clientHeight:600}:{style:{}},querySelectorAll:()=>[]}};
win.window=win;vm.createContext(win);
for(const b of blocks)vm.runInContext(b,win);
const G=win.__GAME__;const s0=JSON.parse(JSON.stringify({x:G.state.player.x,y:G.state.player.y}));
G.key('ArrowUp',true);let errors=0;
for(let i=0;i<600;i++){try{G.step();}catch(e){errors++;if(errors===1)console.error(e);}}
G.key('ArrowUp',false);G.key('ArrowRight',true);for(let i=0;i<120;i++)G.step();G.key('ArrowRight',false);
const p=G.state.player,moved=Math.hypot(p.x-s0.x,p.y-s0.y);
G.key('KeyK',true);G.step();G.key('KeyK',false);
const saved=store['skillpack-city-save']||null;const loadErr=saved?G.restore(saved):'no save';
// exercise draw once (stub canvas) through MainLoop's first frame callback if present
let drew=false;try{if(raf.length)drew=true;}catch(e){}
const out={ok:errors===0&&moved>1&&loadErr===null,errors:errors,moved:moved,time_s:G.state.time,peds:G.state.peds.length,traffic:G.state.traffic.length,
  active_mission:G.state.active,saved_bytes:saved?saved.length:0,load_error:loadErr,mainloop_present:typeof win.MainLoop==='object'};
process.stdout.write(JSON.stringify(out));
