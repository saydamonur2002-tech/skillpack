import 'dart:convert';

import 'package:flutter/services.dart';

import '../../../../core/constants.dart';
import '../../domain/models/rule_model.dart';

/// Dahili `default_skills.json` dosyasını okuyan sınıf.
class LocalRulesLoader {
  LocalRulesLoader({this.assetPath = AppConstants.defaultSkillsAsset});

  final String assetPath;

  Future<RulePack> loadBundled() async {
    final raw = await rootBundle.loadString(assetPath);
    return RulePack.fromJson(jsonDecode(raw) as Map<String, dynamic>);
  }

  Future<String> loadBundledRaw() => rootBundle.loadString(assetPath);
}
