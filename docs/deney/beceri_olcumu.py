"""Mini ölçüm: aynı görev, (a) becerisiz (b) paketlenmiş beceriyle; küçük yerel modelde.

Kullanım: python beceri_olcumu.py <model.gguf> [N=20] [v]
  v verilirse yalnız (b) çalışır ve yanlış cevaplar yazdırılır.
Gereken: pip install llama-cpp-python
"""
import json, sys, time, random, re
from llama_cpp import Llama
model=sys.argv[1]; N=int(sys.argv[2]) if len(sys.argv)>2 else 20
random.seed(7); VERBOSE=len(sys.argv)>3
def truth(k):  # deterministik referans (scripts/koli_sinifla.py'nin yapacağı iş)
    if not re.fullmatch(r"\d{13}", k["barkod"]): return "insan"
    if k["agirlik_kg"]>25: return "agir"
    if k["hedef"]=="IST": return "3"
    if k["kirilacak"]: return "5"
    return "1"
cases=[]
for i in range(N):
    k={"barkod": random.choice(["8690000000017","869000000001","86900000000A7","8691234567890"]) if i%4==0 else "".join(random.choice("0123456789") for _ in range(13)),
       "agirlik_kg": random.choice([2,8,14,24,25,26,31,40]), "hedef": random.choice(["IST","ANK","IZM","IST"]), "kirilacak": random.choice([True,False,False])}
    cases.append(k)
import os; SKILL=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"depo-koli-ayirma","SKILL.md"), encoding="utf-8").read().split("---",2)[2]
RULES="""Kurallar (sırayla uygula, ilk eşleşen geçerlidir):
R0: barkod tam 13 rakam değilse -> rampa "insan"
R1: agirlik_kg 25'ten büyükse -> rampa "agir"
R2: hedef "IST" ise -> rampa "3"
R3: kirilacak true ise -> rampa "5"
R4: aksi halde -> rampa "1"
"""
OUT='Yalnız JSON ver: {"rampa": "...", "kural": "..."}'
sys_a="Sen bir depo asistanısın. Koliyi doğru rampaya ata. "+OUT
sys_b=SKILL+"\n"+RULES+OUT
llm=Llama(model, n_ctx=2048, n_threads=4, verbose=False, seed=1)
def run(sysmsg):
    ok=0; tin=tout=0; t=time.time()
    for k in cases:
        r=llm.create_chat_completion(messages=[{"role":"system","content":sysmsg},{"role":"user","content":json.dumps(k)}], temperature=0, max_tokens=40, response_format={"type":"json_object"})
        tin+=r["usage"]["prompt_tokens"]; tout+=r["usage"]["completion_tokens"]
        try: got=str(json.loads(r["choices"][0]["message"]["content"]).get("rampa")).strip().lower()
        except Exception: got="?"
        got=got.replace("ı","i").replace("ğ","g").replace("rampa","").strip(' "')
        if VERBOSE and got!=truth(k): print("   YANLIŞ", k, "->", r["choices"][0]["message"]["content"].strip()[:70], "| beklenen", truth(k))
        ok+= got==truth(k)
    dt=time.time()-t
    return ok,tin,tout,dt
for name,s in (("b) beceriyle",sys_b),) if VERBOSE else (("a) becerisiz",sys_a),("b) beceriyle",sys_b)):
    ok,tin,tout,dt=run(s)
    print(f"{name}: doğru {ok}/{N} | girdi {tin/N:.0f} tok/görev, çıktı {tout/N:.0f} tok/görev | {dt/N:.1f} sn/görev | üretim ~{tout/dt:.1f} tok/s (4 çekirdek CPU, prefill dahil)")
from collections import Counter; print("doğru cevap dağılımı:", dict(Counter(truth(k) for k in cases)))
