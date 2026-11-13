// Execute pinned SAT.js on each reference pair.
const SAT=require(require('path').join(__dirname,'..','upstream','SAT.js'));
const V=SAT.Vector;
function shape(s){
  if(s.type==='circle')return ['c',new SAT.Circle(new V(s.x,s.y),s.r)];
  if(s.type==='box')return ['p',new SAT.Box(new V(s.x,s.y),s.w,s.h).toPolygon()];
  const p=new SAT.Polygon(new V(s.x,s.y),s.points.map(q=>new V(q[0],q[1])));
  if(s.angle)p.setAngle(s.angle);
  return ['p',p];
}
const out=[];
for(const c of JSON.parse(require('fs').readFileSync(0,'utf8'))){
  const res=[];
  for(const pr of c.pairs){
    const [ta,a]=shape(pr.a),[tb,b]=shape(pr.b);const r=new SAT.Response();
    const hit=ta==='c'&&tb==='c'?SAT.testCircleCircle(a,b,r):ta==='p'&&tb==='c'?SAT.testPolygonCircle(a,b,r):ta==='c'?SAT.testCirclePolygon(a,b,r):SAT.testPolygonPolygon(a,b,r);
    if(!hit)res.push({collides:false,overlap:null,overlap_n:null,overlap_v:null,a_in_b:null,b_in_a:null,push_a:null});
    else res.push({collides:true,overlap:r.overlap,overlap_n:[r.overlapN.x,r.overlapN.y],overlap_v:[r.overlapV.x,r.overlapV.y],a_in_b:r.aInB,b_in_a:r.bInA,push_a:[-r.overlapV.x,-r.overlapV.y]});
  }
  out.push({count:res.length,colliding:res.filter(x=>x.collides).length,results:res});
}
process.stdout.write(JSON.stringify(out));
