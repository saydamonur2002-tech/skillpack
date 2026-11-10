import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/services/settings_intents.dart';

void main() {
  test('ayar intent eylemleri sistem sabitleriyle kurulur', () {
    expect(
      SettingsIntents.actionsFor('battery_saver'),
      ['android.settings.BATTERY_SAVER_SETTINGS'],
    );
    expect(
      SettingsIntents.actionsFor('display'),
      ['android.settings.DISPLAY_SETTINGS'],
    );
    expect(
      SettingsIntents.actionsFor('storage'),
      [
        'android.os.storage.action.MANAGE_STORAGE',
        'android.settings.INTERNAL_STORAGE_SETTINGS',
      ],
    );
  });

  test('arayüz kopyasında ve kural eylemlerinde yasaklı söz yok', () {
    const banned = ['boost', 'hızlandır', 'ram temizle', 'optimize et'];
    final files = [
      File('assets/configs/default_skills.json'),
      ...Directory('lib/features/hybrid_assistant/presentation')
          .listSync(recursive: true)
          .whereType<File>()
          .where((file) => file.path.endsWith('.dart')),
    ];
    final blob = files.map((file) => file.readAsStringSync()).join('\n');
    final lower = blob.toLowerCase();
    for (final word in banned) {
      expect(lower.contains(word), isFalse, reason: word);
    }
  });
}
