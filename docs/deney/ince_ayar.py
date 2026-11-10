"""Betikle etiketlenmiş sentetik veriyle küçük modele LoRA ince ayarı ve öncesi/sonrası ölçüm.

Deterministik betik (truth) koliyi rampaya atar; model bu çiftlerden öğrenir.
İstemde kural metni YOKTUR: model kuralı yalnız örneklerden çıkarmak zorundadır.

Kullanım:
  python ince_ayar.py <model_dizini> [--egitim 640] [--parti 8] [--lr 3e-4] [--cikti adaptor/]
Gereken: pip install torch transformers peft
"""
import argparse, json, random, re, time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model

ap = argparse.ArgumentParser()
ap.add_argument("model"); ap.add_argument("--egitim", type=int, default=640)
ap.add_argument("--parti", type=int, default=8); ap.add_argument("--lr", type=float, default=3e-4)
ap.add_argument("--taze", type=int, default=200); ap.add_argument("--cikti", default="")
ap.add_argument("--hiz-olc", action="store_true", help="3 adım at, süreyi yaz, çık")
a = ap.parse_args()
torch.manual_seed(0)

def truth(k):
    if not re.fullmatch(r"\d{13}", k["barkod"]): return "insan"
    if k["agirlik_kg"] > 25: return "agir"
    if k["hedef"] == "IST": return "3"
    if k["kirilacak"]: return "5"
    return "1"

def digits(r, n): return "".join(r.choice("0123456789") for _ in range(n))

def koli(r, sehirler, bozuk_turleri):
    if r.random() < 0.2:
        t = r.choice(bozuk_turleri)
        b = {"12": digits(r, 12), "harf": (lambda d, i: d[:i] + r.choice("ABXO") + d[i + 1:])(digits(r, 13), r.randrange(13)),
             "14": digits(r, 14), "11": digits(r, 11), "bosluk": digits(r, 6) + " " + digits(r, 6)}[t]
    else:
        b = digits(r, 13)
    return {"barkod": b, "agirlik_kg": r.randint(1, 60) if r.random() < 0.6 else r.randint(20, 31),
            "hedef": r.choice(sehirler), "kirilacak": r.random() < 0.35}

# İlk denemedeki 20 koli (beceri_olcumu.py ile aynı tohum ve aynı üretim sırası)
r0 = random.Random(7); ilk20 = []
for i in range(20):
    ilk20.append({"barkod": r0.choice(["8690000000017", "869000000001", "86900000000A7", "8691234567890"]) if i % 4 == 0
                  else "".join(r0.choice("0123456789") for _ in range(13)),
                  "agirlik_kg": r0.choice([2, 8, 14, 24, 25, 26, 31, 40]), "hedef": r0.choice(["IST", "ANK", "IZM", "IST"]),
                  "kirilacak": r0.choice([True, False, False])})

SEHIR = ["IST", "IST", "ANK", "IZM", "KON", "TRB"]
key = lambda k: json.dumps(k, sort_keys=True)
yasak = {key(k) for k in ilk20}
r = random.Random(11)
taze = []
while len(taze) < a.taze:
    k = koli(r, SEHIR, ["12", "harf"])
    if key(k) not in yasak: taze.append(k); yasak.add(key(k))
# Eğitimde hiç görülmeyen şehirler ve bozuk barkod biçimleri
gorulmemis = [koli(r, ["IST", "BUR", "ADA", "GAZ"], ["14", "11", "bosluk"]) for _ in range(80)]
for k in gorulmemis: yasak.add(key(k))
egitim = []
while len(egitim) < a.egitim:
    k = koli(r, SEHIR, ["12", "harf"])
    if key(k) not in yasak: egitim.append(k)

SYS = 'Depo koli ayırma. Koliyi rampaya ata. Yalnız JSON ver: {"rampa": "..."}'
tok = AutoTokenizer.from_pretrained(a.model); tok.padding_side = "left"
def istem(k):
    return tok.apply_chat_template([{"role": "system", "content": SYS}, {"role": "user", "content": json.dumps(k, ensure_ascii=False)}],
                                   tokenize=False, add_generation_prompt=True)
def cevap(k): return json.dumps({"rampa": truth(k)}) + tok.eos_token

model = AutoModelForCausalLM.from_pretrained(a.model, dtype=torch.float32, low_cpu_mem_usage=True)

@torch.no_grad()
def olc(ad, kume, parti=16):
    model.eval(); ok = 0; t = time.time(); hatalar = {}
    for i in range(0, len(kume), parti):
        b = kume[i:i + parti]
        enc = tok([istem(k) for k in b], return_tensors="pt", padding=True)
        out = model.generate(**enc, max_new_tokens=12, do_sample=False, pad_token_id=tok.pad_token_id)
        for k, o in zip(b, out):
            txt = tok.decode(o[enc["input_ids"].shape[1]:], skip_special_tokens=True)
            try: got = str(json.loads(txt).get("rampa")).strip().lower()
            except Exception: got = "?"
            if got == truth(k): ok += 1
            else: hatalar[f"{truth(k)}->{got}"] = hatalar.get(f"{truth(k)}->{got}", 0) + 1
    enbuyuk = sorted(hatalar.items(), key=lambda x: -x[1])[:5]
    print(f"  {ad}: {ok}/{len(kume)} doğru ({100*ok/len(kume):.0f}%) | {time.time()-t:.0f} sn | hatalar: {enbuyuk}", flush=True)
    return ok

def hepsini_olc(baslik):
    print(baslik, flush=True)
    olc("ilk denemenin 20 kolisi", ilk20); olc("taze koliler (aynı dağılım)", taze); olc("görülmemiş şehir/barkod biçimi", gorulmemis)

if not a.hiz_olc: hepsini_olc("ÖNCE (ince ayarsız, istemde kural yok):")

model = get_peft_model(model, LoraConfig(r=16, lora_alpha=32, lora_dropout=0.0, task_type="CAUSAL_LM",
                                         target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "up_proj", "down_proj", "gate_proj"]))
egitilen = sum(p.numel() for p in model.parameters() if p.requires_grad); toplam = sum(p.numel() for p in model.parameters())
print(f"eğitilen parametre: {egitilen/1e6:.1f}M / {toplam/1e6:.0f}M ({100*egitilen/toplam:.2f}%)", flush=True)
opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr, weight_decay=0.0)

def parti_hazirla(b):
    ids, lab = [], []
    for k in b:
        p = tok(istem(k), add_special_tokens=False)["input_ids"]; c = tok(cevap(k), add_special_tokens=False)["input_ids"]
        ids.append(p + c); lab.append([-100] * len(p) + c)          # kayıp yalnız cevap tokenlarında
    m = max(map(len, ids))
    pad = lambda x, v: [[v] * (m - len(s)) + s for s in x]
    return torch.tensor(pad(ids, tok.pad_token_id)), torch.tensor(pad(lab, -100)), torch.tensor([[0] * (m - len(s)) + [1] * len(s) for s in ids])

model.train(); adim = len(egitim) // a.parti; t0 = time.time()
for s in range(adim):
    x, y, mask = parti_hazirla(egitim[s * a.parti:(s + 1) * a.parti])
    for g in opt.param_groups: g["lr"] = a.lr * min(1.0, (s + 1) / 5) * (1 - 0.9 * s / adim)   # ısınma + doğrusal azalma
    loss = model(input_ids=x, attention_mask=mask, labels=y).loss
    loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); opt.zero_grad()
    if s % 5 == 0 or s == adim - 1:
        print(f"adım {s+1}/{adim} kayıp {loss.item():.4f} | {(time.time()-t0)/(s+1):.1f} sn/adım | dizi {x.shape[1]} token", flush=True)
    if a.hiz_olc and s == 2: raise SystemExit
print(f"eğitim süresi: {(time.time()-t0)/60:.1f} dk, {adim*a.parti} örnek, 1 tur", flush=True)
hepsini_olc("SONRA (LoRA ince ayarlı, istemde kural yok):")
if a.cikti: model.save_pretrained(a.cikti); print("adaptör kaydedildi:", a.cikti)
