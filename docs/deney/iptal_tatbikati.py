"""İptal tatbikatı: TUF deposu (kök/hedefler/anlık görüntü/zaman damgası) + iptal listesi hedef dosyası.

Kullanım: python iptal_tatbikati.py
Gereken: pip install "tuf>=7" "securesystemslib[crypto]"
"""
import json, os, shutil, sys, threading, time, datetime as dt, functools, http.server
from tuf.api.metadata import Metadata, Root, Targets, Snapshot, Timestamp, MetaFile, TargetFile
from tuf.api.serialization.json import JSONSerializer
from tuf.ngclient import Updater, UpdaterConfig
from tuf.api import exceptions as E
from securesystemslib.signer import CryptoSigner

import tempfile; BASE=tempfile.mkdtemp(prefix="tufdrill-")
REPO=f"{BASE}/repo"; MD=f"{REPO}/metadata"; TG=f"{REPO}/targets"; os.makedirs(MD); os.makedirs(TG)
now=lambda: dt.datetime.now(dt.timezone.utc)
signers={r: CryptoSigner.generate_ed25519() for r in ("root","targets","snapshot","timestamp")}
root=Root(expires=now()+dt.timedelta(days=365), consistent_snapshot=False)
for r,s in signers.items(): root.add_key(s.public_key, r)
md={"root":Metadata(root),"targets":Metadata(Targets(expires=now()+dt.timedelta(days=30))),
    "snapshot":Metadata(Snapshot(expires=now()+dt.timedelta(days=7))),"timestamp":Metadata(Timestamp(expires=now()+dt.timedelta(days=1)))}
ser=JSONSerializer()

def publish(revoked, ts_expire=None):
    path=f"{TG}/iptal_listesi.json"
    json.dump({"surum":md["targets"].signed.version,"olusturma":now().isoformat(),"iptal":revoked}, open(path,"w"), ensure_ascii=False)
    md["targets"].signed.targets["iptal_listesi.json"]=TargetFile.from_file("iptal_listesi.json", path)
    md["snapshot"].signed.meta["targets.json"]=MetaFile(md["targets"].signed.version)
    md["timestamp"].signed.snapshot_meta=MetaFile(md["snapshot"].signed.version)
    if ts_expire: md["timestamp"].signed.expires=ts_expire
    for r in ("targets","snapshot","timestamp"):
        md[r].signatures.clear(); md[r].sign(signers[r]); md[r].to_file(f"{MD}/{r}.json", ser)
def bump():
    for r in ("targets","snapshot","timestamp"): md[r].signed.version+=1

md["root"].sign(signers["root"]); md["root"].to_file(f"{MD}/1.root.json", ser); shutil.copy(f"{MD}/1.root.json", f"{MD}/root.json")
publish([])

h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=REPO); h.log_message=lambda *a: None
srv=http.server.ThreadingHTTPServer(("127.0.0.1",0), h); port=srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

def client(name):
    d=f"{BASE}/{name}"; os.makedirs(f"{d}/md", exist_ok=True); os.makedirs(f"{d}/dl", exist_ok=True)
    if not os.path.exists(f"{d}/md/root.json"): shutil.copy(f"{MD}/1.root.json", f"{d}/md/root.json")  # güven kökü: ilk kurulumda elden
    u=Updater(f"{d}/md", f"http://127.0.0.1:{port}/metadata/", f"{d}/dl", f"http://127.0.0.1:{port}/targets/", config=UpdaterConfig(prefix_targets_with_hash=False), bootstrap=open(f"{MD}/1.root.json","rb").read())
    u.refresh(); info=u.get_targetinfo("iptal_listesi.json")
    p=u.find_cached_target(info) or u.download_target(info)
    return json.load(open(p))

PKG="sha256:7d8170762d059f096e91d2d8723ef461e5d7fa26eb788025fe6f4d5584341747"
print("1) ilk senkron, 3 istemci:", [len(client(f"istemci{i}")["iptal"]) for i in range(3)], "iptal kaydı")
t0=time.time(); bump(); publish([{"paket":PKG,"surum_araligi":"<=1.2.0","gerekce":"zararli","ciddiyet":"yuksek","tarih":now().date().isoformat()}])
res=[any(x["paket"]==PKG for x in client(f"istemci{i}")["iptal"]) for i in range(3)]
print(f"2) iptal yayımlandı -> istemcilerde görüldü mü: {res}  (çekme+doğrulama süresi {1000*(time.time()-t0):.0f} ms, yerel ağ)")

print("3) saldırı: hedef dosyayı imzasız değiştir (aynada iptal listesini boşalt)")
shutil.copy(f"{TG}/iptal_listesi.json", f"{BASE}/yedek.json"); json.dump({"iptal":[]}, open(f"{TG}/iptal_listesi.json","w"))
shutil.rmtree(f"{BASE}/yeni", ignore_errors=True)
try: client("yeni"); print("   !!! KABUL EDİLDİ (kötü)")
except Exception as e: print("   reddedildi:", type(e).__name__)
shutil.copy(f"{BASE}/yedek.json", f"{TG}/iptal_listesi.json")

print("4) saldırı: geri sarma (eski, iptalsiz metadata'yı sun)")
old=f"{BASE}/eski"; os.makedirs(old)
for r in ("targets","snapshot","timestamp"): shutil.copy(f"{MD}/{r}.json", f"{old}/{r}.json")
bump(); publish([{"paket":PKG,"gerekce":"zararli"},{"paket":"sha256:beef","gerekce":"lisans-ihlali"}]); client("istemci0")
for r in ("targets","snapshot","timestamp"): shutil.copy(f"{old}/{r}.json", f"{MD}/{r}.json")
try: client("istemci0"); print("   !!! KABUL EDİLDİ (kötü)")
except Exception as e: print("   reddedildi:", type(e).__name__, "-", str(e)[:70])

print("5) saldırı: dondurma (süresi dolmuş zaman damgası sunulmaya devam ediyor)")
bump(); bump(); publish([{"paket":PKG,"gerekce":"zararli"}], ts_expire=now()+dt.timedelta(seconds=2)); client("istemci1"); time.sleep(3)
try: client("istemci1"); print("   !!! KABUL EDİLDİ (kötü)")
except Exception as e: print("   reddedildi:", type(e).__name__, "-", str(e)[:70])
srv.shutdown()
