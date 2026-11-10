"""Mini ölçüm: aynı görev, (a) becerisiz (b) paketlenmiş beceriyle; küçük yerel modelde.

Kullanım:
  python beceri_olcumu.py <model.gguf> [--n 20] [--kip kisa|gerekce|serbest] [--max-token N] [--ayrinti]

Kipler:
  kisa     çıktı JSON'a zorlanır, düşünmeye yer yok (varsayılan sınır 40 token)
  gerekce  JSON içinde önce "kontrol" alanı istenir (varsayılan sınır 160 token)
  serbest  biçim zorlaması yok; model adım adım yazar, son satırda "RAMPA: x" verir
           (varsayılan sınır 600 token)
--ayrinti verilirse becerisiz tur atlanır ve yanlış cevaplar yazdırılır.
Gereken: pip install llama-cpp-python
"""
import argparse, json, os, random, re, time
from collections import Counter
from llama_cpp import Llama

ap = argparse.ArgumentParser()
ap.add_argument("model"); ap.add_argument("--n", type=int, default=20)
ap.add_argument("--kip", choices=["kisa", "gerekce", "serbest"], default="kisa")
ap.add_argument("--max-token", type=int, default=0); ap.add_argument("--ayrinti", action="store_true")
ap.add_argument("--baglam", type=int, default=4096)
a = ap.parse_args()
MAXTOK = a.max_token or {"kisa": 40, "gerekce": 160, "serbest": 600}[a.kip]
random.seed(7)

def truth(k):  # deterministik referans (scripts/koli_sinifla.py'nin yapacağı iş)
    if not re.fullmatch(r"\d{13}", k["barkod"]): return "insan"
    if k["agirlik_kg"] > 25: return "agir"
    if k["hedef"] == "IST": return "3"
    if k["kirilacak"]: return "5"
    return "1"

cases = []
for i in range(a.n):
    cases.append({
        "barkod": random.choice(["8690000000017", "869000000001", "86900000000A7", "8691234567890"]) if i % 4 == 0
                  else "".join(random.choice("0123456789") for _ in range(13)),
        "agirlik_kg": random.choice([2, 8, 14, 24, 25, 26, 31, 40]),
        "hedef": random.choice(["IST", "ANK", "IZM", "IST"]),
        "kirilacak": random.choice([True, False, False])})

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = open(os.path.join(HERE, "depo-koli-ayirma", "SKILL.md"), encoding="utf-8").read().split("---", 2)[2]
RULES = """Kurallar (sırayla uygula, ilk eşleşen geçerlidir):
R0: barkod tam 13 rakam değilse -> rampa "insan"
R1: agirlik_kg 25'ten büyükse -> rampa "agir"
R2: hedef "IST" ise -> rampa "3"
R3: kirilacak true ise -> rampa "5"
R4: aksi halde -> rampa "1"
"""
OUT = {
    "kisa": 'Yalnız JSON ver: {"rampa": "...", "kural": "..."}',
    "gerekce": 'Önce kuralları R0dan başlayarak sırayla tek tek kontrol et, ilk eşleşende dur. '
               'Yalnız JSON ver: {"kontrol": "R0: ... R1: ...", "kural": "...", "rampa": "..."}',
    "serbest": "Adım adım düşün. R0'dan başla; her kural için kolinin ilgili değerini yaz, koşulun sağlanıp "
               "sağlanmadığını söyle. Koşulu sağlanan ilk kuralda dur, sonraki kurallara bakma. "
               "En son satıra yalnız şunu yaz: RAMPA: <değer>",
}[a.kip]
sys_a = "Sen bir depo asistanısın. Koliyi doğru rampaya ata. " + OUT
sys_b = SKILL + "\n" + RULES + OUT
llm = Llama(a.model, n_ctx=a.baglam, n_threads=os.cpu_count(), n_gpu_layers=-1, verbose=False, seed=1)

def norm(s):
    return str(s).lower().replace("ı", "i").replace("ğ", "g").replace("rampa", "").strip(' ":.*`\n')

def answer(text):
    if a.kip == "serbest":
        m = re.findall(r"RAMPA\s*:\s*([^\n]+)", text, flags=re.I)
        return norm(m[-1]) if m else "?"
    try: return norm(json.loads(text).get("rampa"))
    except Exception: return "?"

def run(sysmsg):
    ok = tin = tout = kesik = 0; t = time.time(); yanlis = Counter()
    for k in cases:
        kw = {} if a.kip == "serbest" else {"response_format": {"type": "json_object"}}
        r = llm.create_chat_completion(messages=[{"role": "system", "content": sysmsg},
                                                 {"role": "user", "content": json.dumps(k, ensure_ascii=False)}],
                                       temperature=0, max_tokens=MAXTOK, **kw)
        tin += r["usage"]["prompt_tokens"]; tout += r["usage"]["completion_tokens"]
        kesik += r["choices"][0]["finish_reason"] == "length"
        text = r["choices"][0]["message"]["content"]; got = answer(text)
        if got != truth(k):
            yanlis[f"beklenen {truth(k)} -> verilen {got}"] += 1
            if a.ayrinti: print("   YANLIŞ", k, "| beklenen", truth(k), "| verilen", got, "\n      ", text.strip().replace("\n", " / ")[-300:])
        else: ok += 1
    return ok, tin, tout, time.time() - t, kesik, yanlis

turlar = (("b) beceriyle", sys_b),) if a.ayrinti else (("a) becerisiz", sys_a), ("b) beceriyle", sys_b))
print(f"model={os.path.basename(a.model)} kip={a.kip} max_token={MAXTOK} n={a.n}")
for name, s in turlar:
    ok, tin, tout, dt, kesik, yanlis = run(s)
    print(f"{name}: doğru {ok}/{a.n} | girdi {tin/a.n:.0f} tok/görev, çıktı {tout/a.n:.0f} tok/görev | "
          f"{dt/a.n:.1f} sn/görev | ~{tout/dt:.1f} tok/s (prefill dahil) | sınırda kesilen {kesik}")
    for h, c in yanlis.most_common(): print(f"     {c}x {h}")
print("doğru cevap dağılımı:", dict(Counter(truth(k) for k in cases)))
