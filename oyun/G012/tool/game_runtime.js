/* Skillpack city game runtime. Original work, MIT License, Copyright (c) 2026 Skillpack contributors.
   Formulas mirror the skill packs: G003 bicycle model, G004 circle-vs-box push-out, G006 seek/arrive/flee/pursuit,
   G007 wanted rules, G008 missions, G009 integer money, G010 save envelope. The model built this file once; it runs alone. */
(function(root){
'use strict';
var doc=root.document;
var C=JSON.parse(doc.getElementById('game-config').textContent);
var W=C.map.width,H=C.map.height,T=C.map.tiles,R=C.wanted_rules,V=C.vehicle,N=C.npc;
var DT=C.loop.timestep_ms/1000;
// ---------- deterministic random (xorshift32, same as G002) ----------
var rngState=(C.map.seed>>>0)||0x9E3779B9;
function rnd(){var x=rngState;x^=x<<13;x>>>=0;x^=x>>>17;x^=x<<5;x>>>=0;rngState=x;return x;}
// ---------- maths shared with the skills ----------
function wrap(a){var m=2*Math.PI,r=(a+Math.PI)%m;if(r<0)r+=m;return r-Math.PI;}           // G003 angle_mod
function carStep(s,acc,steerDeg){                                                          // G003 State.update
  var L=V.wheelbase_m,ms=V.max_steer_deg*Math.PI/180,d=steerDeg*Math.PI/180;
  d=Math.min(Math.max(d,-ms),ms);
  var x=s.x+s.v*Math.cos(s.yaw)*DT,y=s.y+s.v*Math.sin(s.yaw)*DT;
  var yaw=wrap(s.yaw+s.v/L*Math.tan(d)*DT),v=s.v+acc*DT;
  return {x:x,y:y,yaw:yaw,v:v};
}
function circleBox(cx,cy,r,bx,by,bw,bh){                                                   // G004 circle vs box, returns push for the circle
  var px=Math.max(bx,Math.min(cx,bx+bw)),py=Math.max(by,Math.min(cy,by+bh));
  var dx=cx-px,dy=cy-py,d2=dx*dx+dy*dy;
  var inside=cx>bx&&cx<bx+bw&&cy>by&&cy<by+bh;
  if(!inside){if(d2>r*r)return null;var d=Math.sqrt(d2);if(d===0)return null;return [dx/d*(r-d),dy/d*(r-d)];}
  var l=cx-bx,rt=bx+bw-cx,t=cy-by,b=by+bh-cy,m=Math.min(l,rt,t,b);
  if(m===l)return [-(l+r),0];if(m===rt)return [rt+r,0];if(m===t)return [0,-(t+r)];return [0,b+r];
}
function len(x,y){return Math.sqrt(x*x+y*y);}
function norm(x,y){var d=len(x,y)||1;return [x/d,y/d];}
function seekF(a,tx,ty){var d=norm(tx-a.x,ty-a.y);return [d[0]*a.ms-a.vx,d[1]*a.ms-a.vy];}            // G006 SeekBehavior
function arriveF(a,tx,ty,dec){var dx=tx-a.x,dy=ty-a.y,dist=len(dx,dy);if(dist>0){var sp=Math.min(dist/dec,a.ms);return [dx*sp/dist-a.vx,dy*sp/dist-a.vy];}return [-a.vx,-a.vy];}
function fleeF(a,tx,ty,panic){var dx=a.x-tx,dy=a.y-ty;if(dx*dx+dy*dy>panic*panic)return [0,0];var d=norm(dx,dy);if(d[0]===0&&d[1]===0)d=[0,1];return [d[0]*a.ms-a.vx,d[1]*a.ms-a.vy];}
function pursuitF(a,ex,ey,evx,evy,edx,edy,pf){                                                  // G006 PursuitBehavior
  var dx=ex-a.x,dy=ey-a.y,ahead=dx*a.hx+dy*a.hy>0,facing=a.hx*edx+a.hy*edy<-0.95;
  if(ahead&&facing)return seekF(a,ex,ey);
  var t=len(dx,dy)/(a.ms+len(evx,evy))*pf;return seekF(a,ex+evx*t,ey+evy*t);
}
function integrate(a,f){                                                                        // G006 Vehicle.update
  var m=len(f[0],f[1]);if(a.mf<=0)f=[0,0];else if(m>a.mf){f=norm(f[0],f[1]);f=[f[0]*a.mf,f[1]*a.mf];}
  a.vx+=f[0]/a.mass*DT;a.vy+=f[1]/a.mass*DT;
  if(a.vx*a.vx+a.vy*a.vy>a.ms*a.ms){var n=norm(a.vx,a.vy);a.vx=n[0]*a.ms;a.vy=n[1]*a.ms;}
  var nx=a.x+a.vx*DT,ny=a.y+a.vy*DT;
  if(a.vx*a.vx+a.vy*a.vy>1e-8){var h=norm(nx-a.x,ny-a.y);a.hx=h[0];a.hy=h[1];}
  a.x=nx;a.y=ny;
}
function tile(x,y){x=Math.floor(x);y=Math.floor(y);if(x<0||y<0||x>=W||y>=H)return 'B';return T[y][x];}
function pushOut(o,r){var hit=false;for(var yy=Math.floor(o.y)-1;yy<=Math.floor(o.y)+1;yy++)for(var xx=Math.floor(o.x)-1;xx<=Math.floor(o.x)+1;xx++){
  if(tile(xx+.5,yy+.5)!=='B')continue;var p=circleBox(o.x,o.y,r,xx,yy,1,1);if(p){o.x+=p[0];o.y+=p[1];hit=true;}}return hit;}
// ---------- game state ----------
var P=C.map.points,S;
function agent(x,y,ms,mf){return {x:x,y:y,vx:0,vy:0,hx:0,hy:1,ms:ms,mf:mf,mass:1};}
function newState(){
  var sp=P.spawn;
  var s={time:0,player:{x:sp.x,y:sp.y,yaw:0,v:0,health:100},money:C.economy.start_money,inventory:{},
    wanted:{stars:0,heat:0,unseen:0},missions:{},active:null,mctx:null,cashTaken:[],peds:[],traffic:[],police:[],
    msg:'',msgT:0,over:null,overT:0,bustT:0,sirenT:0,lastCrash:-9,paused:false,log:[]};
  C.routes.pedestrians.forEach(function(r,i){var a=agent(r[0][0]+.5,r[0][1]+.5,N.ped_max_speed,N.ped_max_force);a.route=r;a.wp=0;a.dir=1;a.down=0;a.id=i;s.peds.push(a);});
  C.routes.traffic.forEach(function(r,i){var a=agent(r[0][0]+.5,r[0][1]+.5,N.traffic_max_speed,N.traffic_max_force);a.route=r;a.wp=0;a.dir=1;a.id=i;s.traffic.push(a);});
  C.missions.forEach(function(m){s.missions[m.id]='locked';});
  return s;
}
function say(t){S.msg=t;S.msgT=3;}
function sound(name){if(root.__sfx)root.__sfx(name);}
// ---------- wanted level (G007 rules) ----------
function level(h){var n=0;R.star_thresholds.forEach(function(t){if(h>=t)n++;});return n;}
function crime(type,witnessed){
  var add=R.heat[type]*(witnessed?R.witness_multiplier:1);
  S.wanted.heat=Math.min(R.max_heat,S.wanted.heat+add);S.wanted.stars=Math.max(S.wanted.stars,level(S.wanted.heat));
  if(witnessed)S.wanted.unseen=0;S.log.push(type);
}
function wantedTick(dt,seen){
  var w=S.wanted;if(seen){w.unseen=0;return;}
  var before=w.unseen;w.unseen+=dt;var cd=R.cooldown_s[w.stars];
  if(w.stars>0&&w.unseen>=cd){var over=before<cd?Math.min(dt,w.unseen-Math.max(cd,before)):dt;
    w.heat=Math.max(0,w.heat-R.decay_per_s*over);var was=w.stars;w.stars=Math.min(w.stars,level(w.heat));if(w.stars<was)say(w.stars?'Bir yıldız düştü':'Polisten kurtuldun!');}
}
function witnessed(){var r=R.search_radius_tiles[Math.max(1,S.wanted.stars)];for(var i=0;i<S.police.length;i++){var c=S.police[i];if(len(c.x-S.player.x,c.y-S.player.y)<r)return true;}return false;}
// ---------- missions (G008) ----------
var BY={};C.missions.forEach(function(m){BY[m.id]=m;});
function activate(){
  for(var i=0;i<C.mission_order.length;i++){var id=C.mission_order[i],m=BY[id];
    if((S.missions[id]==='locked'||S.missions[id]==='available')&&(m.requires||[]).every(function(r){return S.missions[r]==='done';})){
      S.missions[id]='active';S.active=id;S.mctx={elapsed:0,picked:false,had:S.wanted.stars>0,count:0};say('Görev: '+(m.title||id));return;}}
  S.active=null;S.mctx=null;
}
function near(t,r){return len(S.player.x-(t[0]+.5),S.player.y-(t[1]+.5))<=r;}
function finish(id){var m=BY[id];S.missions[id]='done';S.money=Math.min(1e9,S.money+(m.reward||0));sound('mission_complete');say('Görev tamam! +$'+(m.reward||0));activate();if(!S.active)say('Bütün görevler bitti!');}
function missionTick(dt,collect){
  var id=S.active;if(!id)return;var m=BY[id],c=S.mctx,r=m.radius||1.5;c.elapsed+=dt;
  if(m.time_limit_s&&c.elapsed>m.time_limit_s){c.elapsed=0;c.picked=false;c.count=0;say('Süre doldu, tekrar dene');return;}
  if(S.wanted.stars>0)c.had=true;
  if(m.type==='goto'&&near(m.target,r))finish(id);
  else if(m.type==='deliver'){if(!c.picked&&near(m.pickup,r)){c.picked=true;say('Paketi aldın, teslim et');sound('pickup');}else if(c.picked&&near(m.target,r))finish(id);}
  else if(m.type==='escape'&&c.had&&S.wanted.stars===0)finish(id);
  else if(m.type==='collect'&&collect){c.count+=collect;if(c.count>=(m.count||1))finish(id);}
}
function missionTarget(){var id=S.active;if(!id)return null;var m=BY[id];if(m.type==='deliver')return S.mctx.picked?m.target:m.pickup;if(m.type==='goto')return m.target;return null;}
// ---------- input ----------
var keys={},pressed={};
function key(k,down){if(down&&!keys[k])pressed[k]=true;keys[k]=down;}
function on(a,b){for(var i=0;i<a.length;i++)if(keys[a[i]])return true;return false;}
function hit(a){for(var i=0;i<a.length;i++)if(pressed[a[i]]){return true;}return false;}
// ---------- one fixed physics step ----------
function respawn(atPolice,fine){
  var p=atPolice?P.police_station:P.spawn,a=atPolice?P.police_station.road_access:P.spawn.tile;
  S.player={x:a[0]+.5,y:a[1]+.5,yaw:0,v:0,health:100};S.money=Math.max(0,S.money-fine);
  S.wanted={stars:0,heat:0,unseen:0};S.police=[];S.bustT=0;
}
function updatePolice(){
  var want=R.police_units[S.wanted.stars],f=R.police_speed_factor[S.wanted.stars];
  while(S.police.length<want){var st=P.police_station.road_access,k=S.police.length;
    var c=agent(st[0]+.5+(k%2)*.6,st[1]+.5+Math.floor(k/2)*.6,N.police_max_speed,N.police_max_force);S.police.push(c);}
  if(S.police.length>want)S.police.length=want;
  var p=S.player,evx=p.v*Math.cos(p.yaw),evy=p.v*Math.sin(p.yaw),edx=Math.cos(p.yaw),edy=Math.sin(p.yaw);
  S.police.forEach(function(c){c.ms=N.police_max_speed*f;integrate(c,pursuitF(c,p.x,p.y,evx,evy,edx,edy,N.prediction_factor));
    if(pushOut(c,0.4)){c.vx*=0.5;c.vy*=0.5;}});
}
function follow(a,arrive){
  var w=a.route[a.wp],tx=w[0]+.5,ty=w[1]+.5;
  if(len(tx-a.x,ty-a.y)<0.35){a.wp+=a.dir;if(a.wp>=a.route.length||a.wp<0){a.dir=-a.dir;a.wp+=2*a.dir;}if(a.wp<0)a.wp=0;if(a.wp>=a.route.length)a.wp=a.route.length-1;w=a.route[a.wp];tx=w[0]+.5;ty=w[1]+.5;}
  return arrive?arriveF(a,tx,ty,N.arrive_deceleration):seekF(a,tx,ty);
}
function update(ms){
  var dt=ms/1000;
  if(hit(['KeyP']))S.paused=!S.paused;
  if(hit(['KeyK']))saveGame();
  if(hit(['KeyL']))loadGame();
  if(S.paused){pressed={};return;}
  S.time+=dt;if(S.msgT>0)S.msgT-=dt;
  if(S.over){S.overT-=dt;if(S.overT<=0){respawn(S.over==='busted',S.over==='busted'?Math.floor(S.money/10):100);S.over=null;}pressed={};return;}
  var p=S.player,up=on(['ArrowUp','KeyW']),down=on(['ArrowDown','KeyS']);
  var steer=(on(['ArrowRight','KeyD'])?1:0)-(on(['ArrowLeft','KeyA'])?1:0);
  var acc=up?V.accel:down?(p.v>0.2?-V.brake:-V.reverse_accel):0;
  if(on(['Space']))acc=p.v>0?-V.brake*1.5:p.v<0?V.brake*1.5:0;
  acc-=p.v*V.drag;
  var n=carStep(p,acc,steer*V.max_steer_deg);
  var tl=tile(n.x,n.y),vmax=tl==='R'?V.max_v:V.max_v*V.offroad_factor;
  n.v=Math.min(Math.max(n.v,V.min_v),vmax);n.health=p.health;S.player=p=n;
  if(pushOut(p,V.radius)){if(Math.abs(p.v)>2&&S.time-S.lastCrash>0.5){S.lastCrash=S.time;sound('crash');p.health-=Math.abs(p.v)*1.5;}p.v*=-0.3;}
  if(hit(['KeyH']))sound('horn');
  var seen=witnessed();
  // pedestrians: arrive along their route, flee from a fast car, get knocked down
  S.peds.forEach(function(a){
    if(a.down>0){a.down-=dt;if(a.down<=0){var w=a.route[0];a.x=w[0]+.5;a.y=w[1]+.5;a.vx=a.vy=0;a.wp=0;}return;}
    var f=(Math.abs(p.v)>3)?fleeF(a,p.x,p.y,N.flee_panic_distance):[0,0];
    if(f[0]===0&&f[1]===0)f=follow(a,true);
    integrate(a,f);pushOut(a,0.25);
    if(len(a.x-p.x,a.y-p.y)<V.radius+0.25){if(Math.abs(p.v)>2){a.down=10;crime('hit_pedestrian',seen);sound('crash');say('Yayaya çarptın!');}else{var d=norm(a.x-p.x,a.y-p.y);a.x=p.x+d[0]*(V.radius+0.26);a.y=p.y+d[1]*(V.radius+0.26);}}
  });
  // traffic: seek along road routes; bumping them is a crime; F steals a stopped-next-to car
  S.traffic.forEach(function(a){
    integrate(a,follow(a,false));pushOut(a,0.35);
    var d=len(a.x-p.x,a.y-p.y);
    if(d<V.radius+0.4){var u=norm(p.x-a.x,p.y-a.y),o=V.radius+0.4-d;p.x+=u[0]*o;p.y+=u[1]*o;if(Math.abs(p.v)>2){crime('hit_vehicle',seen);sound('crash');}p.v*=0.5;}
    if(d<1.4&&Math.abs(p.v)<0.5&&hit(['KeyF'])){S.player={x:a.x,y:a.y,yaw:Math.atan2(a.hy,a.hx),v:0,health:100};var w=a.route[0];a.x=w[0]+.5;a.y=w[1]+.5;a.vx=a.vy=0;a.wp=0;crime('steal_car',seen);say('Araba çaldın!');p=S.player;}
  });
  updatePolice();
  S.police.forEach(function(c){var d=len(c.x-p.x,c.y-p.y);if(d<V.radius+0.4){var u=norm(p.x-c.x,p.y-c.y),o=V.radius+0.4-d;p.x+=u[0]*o;p.y+=u[1]*o;if(Math.abs(p.v)>3)crime('hit_police',true);}});
  var close=S.police.some(function(c){return len(c.x-p.x,c.y-p.y)<1.2;});
  S.bustT=(close&&Math.abs(p.v)<1)?S.bustT+dt:0;
  wantedTick(dt,seen&&S.wanted.stars>0);
  if(S.wanted.stars>0){S.sirenT-=dt;if(S.sirenT<=0){S.sirenT=2;sound('siren');}}
  // cash pickups (count as 'collect' for missions)
  var got=0;P.cash.forEach(function(c,i){if(S.cashTaken.indexOf(i)<0&&len(p.x-c.x,p.y-c.y)<0.8){S.cashTaken.push(i);S.money+=C.economy.cash_amount;got++;sound('cash');say('+$'+C.economy.cash_amount);}});
  // paint shop: clears the wanted level when unseen; E buys a repair kit
  var ps=P.paint_shop;
  if(len(p.x-(ps.road_access[0]+.5),p.y-(ps.road_access[1]+.5))<1.2&&Math.abs(p.v)<1){
    var price=C.economy.catalog.paint_job.price;
    if(S.wanted.stars>0){if(S.wanted.unseen<R.paint_shop_min_unseen_s)say('Polis izliyor, boyama yok');else if(S.money>=price){S.money-=price;S.wanted={stars:0,heat:0,unseen:0};sound('cash');say('Boyandı, aranma bitti (-$'+price+')');}else if(S.msgT<=0)say('Boya için $'+price+' gerekli');}
    if(hit(['KeyE'])){var k=C.economy.catalog.repair_kit;if(S.money>=k.price){S.money-=k.price;p.health=Math.min(100,p.health+50);say('Tamir edildi (-$'+k.price+')');}else say('Para yetmiyor');}
  }
  missionTick(dt,got);
  if(p.health<=0){S.over='wasted';S.overT=3;sound('wasted');}
  else if(S.bustT>2){S.over='busted';S.overT=3;sound('wasted');}
  pressed={};
}
// ---------- save / load (G010 envelope: canonical JSON + FNV-1a 32) ----------
function q(v){if(v===null||typeof v!=='object'){if(typeof v==='number'){return Math.floor(v*1000+0.5)/1000;}return v;}
  if(Array.isArray(v))return v.map(q);var o={};Object.keys(v).sort().forEach(function(k){o[k]=q(v[k]);});return o;}
function canonical(s){return JSON.stringify(q(s));}
function fnv(str){var b=unescape(encodeURIComponent(str)),h=0x811c9dc5;for(var i=0;i<b.length;i++){h^=b.charCodeAt(i);h=Math.imul(h,0x01000193)>>>0;}return ('0000000'+h.toString(16)).slice(-8);}
function snapshot(){var p=S.player,inv={};Object.keys(S.inventory).forEach(function(k){if(S.inventory[k])inv[k]=S.inventory[k];});
  return {seed:C.map.seed,time_s:S.time,player:{x:p.x,y:p.y,yaw:p.yaw,v:p.v,health:Math.max(0,Math.min(100,p.health))},money:S.money,inventory:inv,
    wanted:{stars:S.wanted.stars,heat:S.wanted.heat,seconds_unseen:S.wanted.unseen},missions:S.missions,active_mission:S.active,cash_taken:S.cashTaken.slice()};}
function envelope(){var c=canonical(snapshot());return JSON.stringify({format:C.save.format,version:C.save.version,checksum:'fnv1a32:'+fnv(c),state:JSON.parse(c)});}
function restore(text){
  var e;try{e=JSON.parse(text);}catch(x){return 'bozuk kayıt';}
  if(!e||e.format!==C.save.format)return 'başka bir oyunun kaydı';if(e.version!==C.save.version)return 'desteklenmeyen kayıt sürümü';
  if('fnv1a32:'+fnv(canonical(e.state))!==e.checksum)return 'kayıt değiştirilmiş ya da bozuk';
  if(e.state.seed!==C.map.seed)return 'kayıt başka bir haritaya ait';
  var s=e.state;S=newState();S.time=s.time_s;S.player={x:s.player.x,y:s.player.y,yaw:s.player.yaw,v:s.player.v,health:s.player.health};
  S.money=s.money;S.inventory=s.inventory;S.wanted={stars:s.wanted.stars,heat:s.wanted.heat,unseen:s.wanted.seconds_unseen||0};
  S.missions=s.missions;S.cashTaken=s.cash_taken||[];S.active=null;
  if(s.active_mission&&S.missions[s.active_mission]==='active'){S.active=s.active_mission;S.mctx={elapsed:0,picked:false,had:S.wanted.stars>0,count:0};}else activate();
  return null;
}
function saveGame(){try{root.localStorage.setItem('skillpack-city-save',envelope());say('Kaydedildi');}catch(x){say('Kayıt yapılamadı');}}
function loadGame(){var t=null;try{t=root.localStorage.getItem('skillpack-city-save');}catch(x){}if(!t){say('Kayıt yok');return;}var err=restore(t);say(err?'Yüklenemedi: '+err:'Yüklendi');}
// ---------- drawing ----------
var cv=doc.getElementById('game'),g=cv&&cv.getContext?cv.getContext('2d'):null,TS=C.render.tile_px;
var COL={R:'#3b3f45',S:'#b9b4a8',P:'#4f8f3a',B:'#8a6f5a'};
var BID=[],BN=0;(function(){for(var y=0;y<H;y++){BID.push([]);for(var x=0;x<W;x++)BID[y].push(-1);}
  for(var y0=0;y0<H;y0++)for(var x0=0;x0<W;x0++){if(T[y0][x0]!=='B'||BID[y0][x0]>=0)continue;var st=[[x0,y0]];BID[y0][x0]=BN;
    while(st.length){var c=st.pop();[[1,0],[-1,0],[0,1],[0,-1]].forEach(function(d){var nx=c[0]+d[0],ny=c[1]+d[1];if(nx>=0&&ny>=0&&nx<W&&ny<H&&T[ny][nx]==='B'&&BID[ny][nx]<0){BID[ny][nx]=BN;st.push([nx,ny]);}});}BN++;}})();
function bcol(x,y){var s=['#8a6f5a','#7b7f8c','#9a8466','#6f7d74','#8c6d6d','#a0705a'];return s[(BID[y][x]*7+3)%s.length];}
function box(x,y,yaw,l,w,col){g.save();g.translate(x*TS,y*TS);g.rotate(yaw);g.fillStyle=col;g.fillRect(-l/2*TS,-w/2*TS,l*TS,w*TS);g.fillStyle='rgba(255,255,255,.55)';g.fillRect(l/4*TS,-w/2.6*TS,l/6*TS,w/1.3*TS);g.restore();}
function dot(x,y,r,col){g.beginPath();g.arc(x*TS,y*TS,r*TS,0,7);g.fillStyle=col;g.fill();}
function draw(){
  if(!g)return;var cw=cv.width=cv.clientWidth||800,ch=cv.height=cv.clientHeight||600,p=S.player;
  g.fillStyle='#1d2b1d';g.fillRect(0,0,cw,ch);g.save();
  var ox=cw/2-p.x*TS,oy=ch/2-p.y*TS;g.translate(Math.round(ox),Math.round(oy));
  var x0=Math.max(0,Math.floor(-ox/TS)),y0=Math.max(0,Math.floor(-oy/TS)),x1=Math.min(W,x0+Math.ceil(cw/TS)+2),y1=Math.min(H,y0+Math.ceil(ch/TS)+2);
  for(var y=y0;y<y1;y++)for(var x=x0;x<x1;x++){var t=T[y][x];g.fillStyle=t==='B'?bcol(x,y):COL[t];g.fillRect(x*TS,y*TS,TS+1,TS+1);
    if(t==='B'&&(x+1>=W||T[y][x+1]!=='B')){g.fillStyle='rgba(0,0,0,.25)';g.fillRect(x*TS+TS*.6,y*TS,TS*.4,TS);}
    if(t==='R'&&(x+y)%2===0){g.fillStyle='rgba(255,255,255,.08)';g.fillRect(x*TS+TS*.45,y*TS+TS*.45,TS*.1,TS*.1);}}
  var tg=missionTarget();if(tg){var pulse=.6+.25*Math.sin(S.time*5);dot(tg[0]+.5,tg[1]+.5,pulse,'rgba(255,215,0,.75)');}
  var ps=P.paint_shop.road_access;dot(ps[0]+.5,ps[1]+.5,.45,'#2f7de1');var st=P.police_station.road_access;dot(st[0]+.5,st[1]+.5,.4,'#123a8c');
  P.cash.forEach(function(c,i){if(S.cashTaken.indexOf(i)<0)dot(c.x,c.y,.22,'#2ecc40');});
  S.peds.forEach(function(a){dot(a.x,a.y,.22,a.down>0?'#7a1f1f':'#f2d16b');});
  S.traffic.forEach(function(a){box(a.x,a.y,Math.atan2(a.hy,a.hx),.95,.5,'#d9d9d9');});
  S.police.forEach(function(c){box(c.x,c.y,Math.atan2(c.hy,c.hx),1,.52,(Math.floor(S.time*6)%2)?'#1f4fd1':'#d11f1f');});
  box(p.x,p.y,p.yaw,1,.52,'#e8452c');g.restore();hud(cw,ch);
}
function hud(cw,ch){
  var p=S.player;g.fillStyle='rgba(0,0,0,.55)';g.fillRect(8,8,250,74);g.fillStyle='#fff';g.font='bold 18px sans-serif';
  g.fillText('$'+S.money,18,32);g.fillStyle='#f5c518';g.fillText('★★★★★'.slice(0,S.wanted.stars)+'☆☆☆☆☆'.slice(0,5-S.wanted.stars),110,32);
  g.fillStyle='#555';g.fillRect(18,42,150,8);g.fillStyle='#3ad16b';g.fillRect(18,42,150*Math.max(0,p.health)/100,8);
  g.fillStyle='#fff';g.font='13px sans-serif';var m=S.active?BY[S.active]:null;g.fillText(m?(m.title||m.id):'Görev yok',18,68);
  var mm=Math.max(1,Math.floor(110/Math.max(W,H)));g.fillStyle='rgba(0,0,0,.5)';g.fillRect(cw-W*mm-14,8,W*mm+6,H*mm+6);
  for(var y=0;y<H;y++)for(var x=0;x<W;x++){var t=T[y][x];if(t==='S')continue;g.fillStyle=t==='R'?'#777':t==='P'?'#3c7':'#a87';g.fillRect(cw-W*mm-11+x*mm,11+y*mm,mm,mm);}
  g.fillStyle='#f33';g.fillRect(cw-W*mm-12+p.x*mm,10+p.y*mm,3,3);
  if(S.msgT>0||S.over||S.paused){g.fillStyle='rgba(0,0,0,.6)';g.fillRect(cw/2-180,ch-70,360,40);g.fillStyle='#fff';g.font='bold 16px sans-serif';g.textAlign='center';
    g.fillText(S.over==='wasted'?'HURDA OLDUN':S.over==='busted'?'TUTUKLANDIN':S.paused?'DURAKLATILDI':S.msg,cw/2,ch-44);g.textAlign='left';}
}
// ---------- start ----------
S=newState();activate();
function step(ms){update(ms===undefined?C.loop.timestep_ms:ms);}
root.__GAME__={get state(){return S;},step:step,key:key,carStep:carStep,circleBox:circleBox,pursuitF:pursuitF,integrate:integrate,agent:agent,
  envelope:envelope,restore:restore,canonical:canonical,fnv:fnv,config:C,reset:function(){S=newState();activate();}};
if(root.addEventListener){
  var map={};
  root.addEventListener('keydown',function(e){if(!root.__sfx&&root.__makeSfx)root.__sfx=root.__makeSfx();key(e.code,true);var h=doc.getElementById('help');if(h)h.style.display='none';if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space'].indexOf(e.code)>=0)e.preventDefault();});
  root.addEventListener('keyup',function(e){key(e.code,false);});
  var pads=doc.querySelectorAll?doc.querySelectorAll('[data-key]'):[];
  Array.prototype.forEach.call(pads,function(b){var k=b.getAttribute('data-key');
    b.addEventListener('touchstart',function(e){e.preventDefault();if(!root.__sfx&&root.__makeSfx)root.__sfx=root.__makeSfx();key(k,true);var h=doc.getElementById('help');if(h)h.style.display='none';});
    b.addEventListener('touchend',function(e){e.preventDefault();key(k,false);});});
}
if(root.MainLoop&&!root.__HEADLESS__){
  root.MainLoop.setSimulationTimestep(C.loop.timestep_ms).setUpdate(update).setDraw(draw)
    .setEnd(function(fps,panic){if(panic)root.MainLoop.resetFrameDelta();}).start();   // G001: discard backlog on panic
}
})(typeof window!=='undefined'?window:this);
