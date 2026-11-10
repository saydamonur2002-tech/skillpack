import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/data/datasources/local_rules_loader.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/models/device_snapshot.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/models/rule_model.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/services/rule_engine.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/services/rule_schema_validator.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('ham pil sıcaklığı onda bire bölünür', () {
    expect(batteryTempCFromRaw(412), 41.2);
    expect(batteryTempCFromRaw(null), isNull);
  });

  test('bellek yüzdesi total ve avail üzerinden', () {
    const snapshot = DeviceSnapshot(totalMem: 1000, availMem: 250);
    expect(snapshot.memoryUsedPercent, 75);
  });

  test('paketlenmiş kurallar şemaya uyar ve eşleşir', () async {
    final raw = await rootBundle.loadString(
      'assets/configs/default_skills.json',
    );
    final json = jsonDecode(raw) as Map<String, dynamic>;
    expect(RuleSchemaValidator().validate(json).isValid, isTrue);

    final engine = RuleEngine()..applyPack(await LocalRulesLoader().loadBundled());

    expect(
      engine
          .evaluate(_ctx({
            'thermal_supported': true,
            'thermal_status': 4,
          }))
          ?.rule
          .id,
      'thermal-severe',
    );
    expect(
      engine
          .evaluate(_ctx({
            'thermal_supported': false,
            'battery_temp_c': 41,
          }))
          ?.rule
          .id,
      'battery-temp-high',
    );
    expect(
      engine
          .evaluate(_ctx({
            'thermal_supported': true,
            'thermal_status': 0,
            'health': 'overheat',
            'battery_temp_c': 30,
            'battery_level': 80,
            'available_bytes': 5000000000,
          }))
          ?.rule
          .id,
      'charge-overheat',
    );
    expect(
      engine
          .evaluate(_ctx({
            'battery_level': 12,
            'is_charging': false,
            'battery_temp_c': 25,
            'thermal_supported': true,
            'thermal_status': 0,
            'available_bytes': 5000000000,
          }))
          ?.rule
          .id,
      'battery-low',
    );
    expect(
      engine
          .evaluate(_ctx({
            'low_memory': true,
            'battery_level': 80,
            'battery_temp_c': 25,
            'thermal_supported': true,
            'thermal_status': 0,
            'available_bytes': 5000000000,
          }))
          ?.rule
          .id,
      'low-memory',
    );
    final storage = engine.evaluate(_ctx({
      'available_bytes': 500000000,
      'battery_level': 80,
      'battery_temp_c': 25,
      'thermal_supported': true,
      'thermal_status': 0,
    }));
    expect(storage?.rule.id, 'storage-low');
    expect(storage?.rule.then.settings, ['storage']);
  });
}

RuleContext _ctx(Map<String, Object?> values) {
  return RuleContext(query: 'durum', intent: 'unknown', values: values);
}
