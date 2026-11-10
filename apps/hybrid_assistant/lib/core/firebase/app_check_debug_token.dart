import 'dart:math';

import 'package:flutter/foundation.dart';

import '../constants.dart';
import '../storage/local_storage.dart';

final RegExp appCheckDebugTokenPattern = RegExp(
  r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
);

/// Firebase konsoluna kaydedilecek App Check debug anahtarı (UUID v4).
///
/// Yalnızca hata ayıklama derlemelerinde üretilir. Depoda sabit bir anahtar
/// tutulmaz; değer cihazda SharedPreferences içinde kalır.
String createAppCheckDebugToken({Random? random}) {
  final rng = random ?? Random.secure();
  final bytes = List<int>.generate(16, (_) => rng.nextInt(256));
  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;

  String hex(int byte) => byte.toRadixString(16).padLeft(2, '0');
  final h = bytes.map(hex).join();
  return '${h.substring(0, 8)}-${h.substring(8, 12)}-'
      '${h.substring(12, 16)}-${h.substring(16, 20)}-${h.substring(20)}';
}

/// Kayıtlı debug anahtarını okur; yoksa veya bozuksa yenisini saklar.
Future<String> loadOrCreateAppCheckDebugToken(LocalStorage storage) async {
  try {
    final prefs = await storage.prefs();
    final existing = prefs.getString(AppConstants.prefsAppCheckDebugToken);
    if (existing != null && appCheckDebugTokenPattern.hasMatch(existing)) {
      return existing;
    }
    final created = createAppCheckDebugToken();
    await prefs.setString(AppConstants.prefsAppCheckDebugToken, created);
    return created;
  } catch (error, stack) {
    debugPrint('App Check debug token persistence failed: $error\n$stack');
    return createAppCheckDebugToken();
  }
}
