# cli/

skillpack v0.1-taslak referans çalıştırıcısı: paketi doğrular, test eder, imzalar, yükler ve yürütür. Kurallar [spec/SKILLPACK_v0.1.md](../spec/SKILLPACK_v0.1.md) içindedir.

Durum: 🚧 MVP. Python 3.10+. Bağımlılıklar: PyYAML, jsonschema, cryptography.

## Kurulum

```bash
pip install -e "cli/[mcp]"     # MCP sunucusu dahil
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

MCP üzerinden paket eylem yapmaz (yalnız önerir) ve değerlerin kullanıcıya onaylatılması uygulamaya kalır. Ayrıntı: spesifikasyon Bölüm 14.

## Komutlar

| Komut | İş |
|---|---|
| `init <dizin>` | Geçerli bir paket iskeleti üretir. |
| `validate <paket>` | Şema, akış kuralları, onay kaydı, kişisel veri taraması. |
| `test <paket>` | `tests/cases.yaml` vakalarını koşar. |
| `keygen --out <dosya> --trust <dizin>` | Ed25519 anahtar çifti üretir. |
| `sign <paket> --key <dosya>` | Doğrular, test eder, sonra imzalar. |
| `verify <paket>` | İmza, özet ve (verilirse) iptal listesi denetimi. |
| `list` | Depodaki paketleri ve reddedilenleri gerekçesiyle listeler. |
| `run <ad>` | Paketi adıyla yürütür. `--set girdi=değer`, `--json`, `--journal`. |
| `ask "<cümle>"` | Yönlendirir ve yürütür. `--router keyword\|ollama`. |
| `serve` | Paketleri MCP araçları olarak sunar (stdio). `--sensor ad=dosya`, `--journal`. |
| `route-test` | Paketlerdeki yönlendirme örneklerinin isabetini ölçer. |

`list`, `run`, `ask`, `serve` ve `route-test` için varsayılan depo `examples/`, güvenilen anahtarlar `examples/trust/` dizinidir (`--packs`, `--trust`, `--revocations` ile değişir).

Teknik taslakta planlanan `pack` ve `publish` komutları henüz yok.

## Yapı

| Dosya | İş |
|---|---|
| `skillpack/expr.py` | Güvenli ifade değerlendirici (`eval` yok). |
| `skillpack/flow.py` | Akış yorumlayıcısı. Karar buradadır; model çağrısı içermez. |
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
