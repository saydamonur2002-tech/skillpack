# hybrid_assistant

Tek işlevli hibrit yapay zeka mobil iskeleti.

**Karar betikte, açıklama modelde.** Lokal JSON kural motoru karar verir; Gemini yalnız açıklama (ve imzalı JSON kural yaması) üretir.

## Klasör yapısı

```
lib/
├── main.dart
├── app.dart
├── core/
│   ├── constants.dart
│   ├── bootstrap.dart
│   ├── firebase/firebase_options_stub.dart
│   └── storage/local_storage.dart
└── features/hybrid_assistant/
    ├── data/
    │   ├── datasources/
    │   │   ├── gemini_client.dart          # Firebase AI Logic + App Check
    │   │   ├── local_rules_loader.dart
    │   │   └── connectivity_guard.dart
    │   └── repositories/assistant_repository.dart
    ├── domain/
    │   ├── models/rule_model.dart
    │   └── services/
    │       ├── rule_engine.dart
    │       ├── hot_patch_manager.dart      # şema → imza → yedek → yaz
    │       ├── rule_schema_validator.dart
    │       └── token_budget_service.dart   # günlük maliyeti kullanıcıya sor
    └── presentation/
        ├── screens/home_screen.dart
        └── widgets/status_card.dart
assets/configs/default_skills.json
```

## Güvenlik

1. **API anahtarı yok** — `firebase_ai` + App Check; Google GenAI SDK anahtarı gömülmez.
2. **Hot-patch yalnız JSON veri** — kod/script alanları reddedilir (Play politikası).
3. **Yazmadan önce** şema + imza; eski sürüm `rules.prev.json` yedeğinde.

## Günlük token

`TokenBudgetService` + UI: limit yoksa / kota aşılacaksa kullanıcıya sorulur (`ask_user`).

## Kurulum

```bash
cd apps/hybrid_assistant
flutter pub get
flutterfire configure   # firebase_options_stub yerine gerçek options
npx firebase-tools init ailogic
flutter test
flutter run
```
