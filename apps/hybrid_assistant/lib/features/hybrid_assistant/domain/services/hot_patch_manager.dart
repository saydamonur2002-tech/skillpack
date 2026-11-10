import 'dart:convert';

import 'package:crypto/crypto.dart';
import 'package:flutter/services.dart';

import '../../../../core/constants.dart';
import '../../../../core/storage/local_storage.dart';
import '../models/rule_model.dart';
import 'rule_engine.dart';
import 'rule_schema_validator.dart';

/// Gemini'den gelen yeni kuralı lokal dosyaya yama yapar.
///
/// Sıra: 1) şema  2) imza  3) eski sürümü yedekle  4) yaz.
/// Yalnız JSON veri; kod indirmez. Bozuksa `rules.prev.json` ile döner.
class HotPatchManager {
  HotPatchManager({
    required LocalStorage storage,
    RuleSchemaValidator? validator,
  })  : _storage = storage,
        _validator = validator ?? RuleSchemaValidator();

  final LocalStorage _storage;
  final RuleSchemaValidator _validator;
  String? _publicKeyMaterial;

  Future<void> loadPublicKey() async {
    try {
      _publicKeyMaterial =
          (await rootBundle.loadString(AppConstants.rulesPublicKeyAsset))
              .trim();
    } catch (_) {
      _publicKeyMaterial = null;
    }
  }

  Future<void> hydrateEngine(RuleEngine engine) async {
    await loadPublicKey();
    final active = await _storage.readActiveRules();
    if (active == null) return;

    final validation = _validator.validate(active);
    if (validation.isValid) {
      engine.applyPack(RulePack.fromJson(active));
      return;
    }
    await rollback(engine);
  }

  Future<HotPatchResult> applySignedEnvelope({
    required String envelope,
    required RuleEngine engine,
  }) async {
    await loadPublicKey();
    final verified = _verifyEnvelope(envelope);
    if (verified == null) {
      return const HotPatchResult.rejected('İmza doğrulanamadı veya key yok');
    }
    return _applyVerifiedJson(verified, engine);
  }

  Future<HotPatchResult> rollback(RuleEngine engine) async {
    final restored = await _storage.restorePreviousToActive();
    if (restored == null) {
      return const HotPatchResult.rejected('Yedek kural dosyası yok');
    }
    final validation = _validator.validate(restored);
    if (!validation.isValid) {
      return HotPatchResult.rejected(
        'Yedek şeması bozuk: ${validation.errors.join('; ')}',
      );
    }
    engine.applyPack(RulePack.fromJson(restored));
    return HotPatchResult.rolledBack(engine.pack!.version);
  }

  Future<HotPatchResult> _applyVerifiedJson(
    String jsonString,
    RuleEngine engine,
  ) async {
    Map<String, dynamic> json;
    try {
      final cleaned = _stripMarkdownFence(jsonString);
      final decoded = jsonDecode(cleaned);
      if (decoded is! Map<String, dynamic>) {
        return const HotPatchResult.rejected('Kök değer JSON nesnesi olmalı');
      }
      json = decoded;
    } catch (e) {
      return HotPatchResult.rejected('JSON parse hatası: $e');
    }

    final validation = _validator.validate(json);
    if (!validation.isValid) {
      return HotPatchResult.rejected(
        'Şema doğrulama başarısız: ${validation.errors.join('; ')}',
      );
    }

    final incoming = RulePack.fromJson(json);
    if (engine.pack != null && !await (await _storage.activeRulesFile()).exists()) {
      await _storage.writePreviousRules(engine.pack!.toJson());
    }

    try {
      await _storage.writeActiveRulesWithBackup(incoming.toJson());
      engine.applyPack(incoming);
      return HotPatchResult.applied(incoming.version);
    } catch (e) {
      await rollback(engine);
      return HotPatchResult.rejected('Uygulama hatası, yedeke dönüldü: $e');
    }
  }

  /// Geliştirme zarfı: base64url(payload).hex(hmac). Üretimde Ed25519.
  String? _verifyEnvelope(String envelope) {
    final parts = envelope.split('.');
    if (parts.length != 2) return null;
    if (_publicKeyMaterial == null ||
        _publicKeyMaterial!.contains('REPLACE') ||
        _publicKeyMaterial!.startsWith('DEV_ONLY')) {
      return null;
    }
    final payloadB64 = parts[0];
    final givenSig = parts[1].toLowerCase();
    final digest =
        Hmac(sha256, utf8.encode(_publicKeyMaterial!)).convert(utf8.encode(payloadB64));
    if (digest.toString() != givenSig) return null;
    try {
      final normalized = base64Url.normalize(payloadB64);
      return utf8.decode(base64Url.decode(normalized));
    } catch (_) {
      return null;
    }
  }

  String _stripMarkdownFence(String raw) {
    final trimmed = raw.trim();
    final fence = RegExp(r'^```(?:json)?\s*([\s\S]*?)\s*```$');
    final match = fence.firstMatch(trimmed);
    return match != null ? match.group(1)!.trim() : trimmed;
  }
}

class HotPatchResult {
  const HotPatchResult.applied(this.version)
      : status = HotPatchStatus.applied,
        message = null;

  const HotPatchResult.rolledBack(this.version)
      : status = HotPatchStatus.rolledBack,
        message = null;

  const HotPatchResult.rejected(this.message)
      : status = HotPatchStatus.rejected,
        version = null;

  final HotPatchStatus status;
  final String? version;
  final String? message;

  bool get isSuccess =>
      status == HotPatchStatus.applied || status == HotPatchStatus.rolledBack;
}

enum HotPatchStatus { applied, rolledBack, rejected }
