# cli/

skillpack v0.1-taslak referans çalıştırıcısı: paketi doğrular, test eder, imzalar, yükler ve yürütür. Kurallar [spec/SKILLPACK_v0.1.md](../spec/SKILLPACK_v0.1.md) içindedir.

Durum: 🚧 MVP. Python 3.10+. Bağımlılıklar: PyYAML, jsonschema, cryptography. İsteğe bağlı: `mcp` (MCP sunucusu), `tuf` (imzalı iptal listesi; python-tuf).

## Kurulum

```bash
pip install -e "cli/[mcp,tuf]" # MCP sunucusu ve imzalı iptal listesi dahil
pip install -e cli/            # yalnız terminal kullanımı
```

Kurmadan denemek için depo kökünde `PYTHONPATH=cli python3 -m skillpack ...` da çalışır.

## Deneme

Depo kökünde:

```bash
skillpack list                                   # imzası geçen paketler
skillpack ask "Tedarikçi tavuk getirdi, kabul edeyim mi?"
skillpack run rulman-isi-titresim --set ambient_c=25
skillpack route-test                             # yönlendirme örnekleri
```

`ask`, cümleden paketi seçer ve akışı yürütür; eksik değerleri size sorar. Cevap bilinmiyorsa boş bırakın ya da `bilmiyorum` yazın: akış tahmin yürütmez, "ustaya sor" sonucuna gider.

Yerel modelle yönlendirme (Ollama kurulu ve model indirilmiş olmalı):

```bash
skillpack ask "Motorda titreşim 6 mm/s, ses de var" --router ollama --model qwen2.5:7b
skillpack route-test --router ollama --model qwen2.5:7b
```

Model yalnız paketi seçer ve söylenen değerleri çıkarır; çıkardığı her değer size onaylatılır. Model yanıt vermezse anahtar kelime yönlendiricisine düşülür.

## MCP sunucusu

`skillpack serve`, depodaki her imzalı paketi bir MCP aracı olarak sunar (stdio). MCP destekleyen bir uygulamada sunucu tanımı genellikle şu biçimdedir; dosyanın yeri uygulamaya göre değişir:

```json
{
  "mcpServers": {
    "skillpack": {
      "command": "skillpack",
      "args": ["serve", "--packs", "/tam/yol/examples", "--trust", "/tam/yol/examples/trust",
               "--journal", "/tam/yol/calistirmalar.jsonl"]
    }
  }
}
```

Uygulamadaki model aracı çağırır. Değer eksikse araç sorulacak soruyu döndürür; model kullanıcıya sorar ve aracı yeniden çağırır. Bütün değerler gelince araç hükmü, ustanın mesajını ve kullandığı değerleri döndürür.

Bağlı yazılımlar:

- `--sensor ad=dosya` — paketin beyan ettiği sensörün değeri bu dosyadan okunur. Örnek: `--sensor bearing_temp_c=/run/olcum/rulman.txt`. Dosyayı başka bir program günceller.
- `--journal dosya` — tamamlanan her çalıştırma JSON Lines olarak eklenir.

MCP üzerinden paket eylem yapmaz (yalnız önerir). Sensör okuması modelin verdiği değerden önce gelir; girdi `max_age_s` beyan ediyorsa dosyanın son yazılma anına göre bayat okuma kullanılmaz. Modelin aktardığı değerler, uygulama MCP'nin girdi isteme özelliğini destekliyorsa, hükümden önce kullanıcıya doğrudan onaylatılır; desteklemiyorsa sonuç "onaylatılmadı" uyarısıyla döner. Ayrıntı: spesifikasyon Bölüm 14.

## İmzalı iptal listesi ve kurulum kaydı

İptal listesi The Update Framework (python-tuf) ile dağıtılır. Yayıncı tarafı:

```bash
skillpack revocations publish --repo /srv/iptal --keys ~/iptal-anahtarlari           # depoyu kurar
skillpack revocations publish --repo /srv/iptal --keys ~/iptal-anahtarlari \
    --pack-id sha256:... --reason zararli                                             # kayıt ekler
skillpack revocations publish --repo /srv/iptal --keys ~/iptal-anahtarlari           # zaman damgasını tazeler
```

`/srv/iptal` dizini düz bir web sunucusundan ya da taşınabilir bellekten sunulur. İlk komutun yazdırdığı `1.root.json` istemcilere elden verilir. İstemci tarafı:

```bash
skillpack revocations sync --source https://ornek.org/iptal --root guven-koku.json --cache ~/.skillpack/iptal
skillpack revocations status --cache ~/.skillpack/iptal
skillpack serve --revocation-cache ~/.skillpack/iptal --state ~/.skillpack/kurulu.json
```

`--revocation-cache` verildiğinde son eşitleme 7 günden eskiyse hiçbir paket yüklenmez (`--revocation-max-age-days` ile değişir). `--state`, her paketin son kabul edilen sürümünü ve yayıncı anahtarını kaydeder; eski sürüme geri sarma, aynı sürümde içerik değişimi ve başka anahtarla imzalanmış aynı adlı paket reddedilir. Bilerek geri dönmek için: `skillpack forget <ad> --state ~/.skillpack/kurulu.json`.

`publish` dört rolün anahtarını tek dizinde şifresiz tutar; küçük kurulum ve deneme içindir.

## Komutlar

| Komut | İş |
|---|---|
| `init <dizin>` | Geçerli bir paket iskeleti üretir. |
| `validate <paket>` | Şema, akış kuralları, onay kaydı, kişisel veri taraması. |
| `test <paket>` | `tests/cases.yaml` vakalarını koşar. |
| `keygen --out <dosya> --trust <dizin>` | Ed25519 anahtar çifti üretir. |
| `sign <paket> --key <dosya>` | Doğrular, test eder, sonra imzalar. |
| `verify <paket>` | İmza, özet ve (verilirse) iptal listesi denetimi. |
| `revocations sync\|status\|publish` | İmzalı iptal listesini eşitler, durumunu gösterir, yayımlar. |
| `forget <ad> --state <dosya>` | Paketi kurulum kaydından siler. |
| `list` | Depodaki paketleri ve reddedilenleri gerekçesiyle listeler. |
| `run <ad>` | Paketi adıyla yürütür. `--set girdi=değer`, `--json`, `--journal`. |
| `ask "<cümle>"` | Yönlendirir ve yürütür. `--router keyword\|ollama`. |
| `serve` | Paketleri MCP araçları olarak sunar (stdio). `--sensor ad=dosya`, `--journal`. |
| `route-test` | Paketlerdeki yönlendirme örneklerinin isabetini ölçer. |

`list`, `run`, `ask`, `serve` ve `route-test` için varsayılan depo `examples/`, güvenilen anahtarlar `examples/trust/` dizinidir (`--packs`, `--trust` ile değişir). Aynı komutlar `--revocation-cache`, `--revocation-max-age-days`, `--state` ve yalnız deneme için imzasız `--revocations` seçeneklerini alır.

Teknik taslakta planlanan `pack` ve `publish` komutları henüz yok.

## Yapı

| Dosya | İş |
|---|---|
| `skillpack/expr.py` | Güvenli ifade değerlendirici (`eval` yok); tür kuralları, sınırlar, üç değerli mantık. |
| `skillpack/flow.py` | Akış yorumlayıcısı. Karar buradadır; model çağrısı içermez. Kaynak önceliği, tazelik ve tehlike kuralları burada uygulanır. |
| `skillpack/revocation.py` | İmzalı iptal listesi: TUF ile yayımlama ve eşitleme. |
| `skillpack/state.py` | Kurulum kaydı: geri sarma ve yayıncı değişimi denetimi. |
| `skillpack/pack.py` | Paketi okuma ve doğrulama. |
| `skillpack/signing.py` | Özet, Ed25519 imza, doğrulama, iptal. |
| `skillpack/registry.py` | Yerel depo; her istekte yeniden tarar. |
| `skillpack/mcp_server.py` | MCP bağlaması: paket → araç, durumsuz çağrı, sensör bağı, kayıt defteri. |
| `skillpack/router.py` | Terminal kullanımı için anahtar kelime ve Ollama yönlendiricileri. |
| `skillpack/host.py` | İnsan, sensör ve eylem arayüzü. Yeni ortam buraya uyarlanır. |
| `skillpack/schemas/` | JSON Schema dosyaları. |

## Testler

```bash
cd cli && python3 -m unittest discover -s . -t .
```

MCP sunucusu testlerde resmî MCP Python SDK'sının istemcisiyle, hem süreç içinde hem stdio üzerinden ayrı süreç olarak sınanır (SDK kurulu değilse bu testler atlanır). Ollama yönlendiricisi testlerde gerçek modelle değil, Ollama'nın `/api/chat` yanıt biçimini taklit eden yerel bir sunucuyla sınanır.
