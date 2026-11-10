import 'dart:convert';
import 'dart:io';

import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../constants.dart';

/// Kural dosyalarını ve yamaları cihazda saklar.
///
/// Play politikası: yalnız JSON veri. Çalıştırılabilir kod yazılmaz.
class LocalStorage {
  LocalStorage();

  Future<Directory> _rulesDirectory() async {
    final root = await getApplicationSupportDirectory();
    final dir = Directory('${root.path}/rules');
    if (!await dir.exists()) {
      await dir.create(recursive: true);
    }
    return dir;
  }

  Future<File> activeRulesFile() async {
    final dir = await _rulesDirectory();
    return File('${dir.path}/${AppConstants.activeRulesFile}');
  }

  Future<File> previousRulesFile() async {
    final dir = await _rulesDirectory();
    return File('${dir.path}/${AppConstants.previousRulesFile}');
  }

  Future<Map<String, dynamic>?> readActiveRules() async {
    final file = await activeRulesFile();
    if (!await file.exists()) return null;
    return jsonDecode(await file.readAsString()) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>?> readPreviousRules() async {
    final file = await previousRulesFile();
    if (!await file.exists()) return null;
    return jsonDecode(await file.readAsString()) as Map<String, dynamic>;
  }

  /// Aktif kuralları yedeğe alır, sonra yeni içeriği yazar.
  Future<void> writeActiveRulesWithBackup(Map<String, dynamic> json) async {
    final active = await activeRulesFile();
    final previous = await previousRulesFile();
    if (await active.exists()) {
      await active.copy(previous.path);
    }
    await active.writeAsString(
      const JsonEncoder.withIndent('  ').convert(json),
    );
  }

  Future<void> writePreviousRules(Map<String, dynamic> json) async {
    final previous = await previousRulesFile();
    await previous.writeAsString(
      const JsonEncoder.withIndent('  ').convert(json),
    );
  }

  /// Yedekten aktife kopyalar (bozuk yama rollback).
  Future<Map<String, dynamic>?> restorePreviousToActive() async {
    final previous = await previousRulesFile();
    final active = await activeRulesFile();
    if (!await previous.exists()) return null;
    await previous.copy(active.path);
    return jsonDecode(await active.readAsString()) as Map<String, dynamic>;
  }

  Future<SharedPreferences> prefs() => SharedPreferences.getInstance();
}
