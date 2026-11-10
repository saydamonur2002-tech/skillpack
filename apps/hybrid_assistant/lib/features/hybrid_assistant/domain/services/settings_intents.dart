/// Sistem ayar sayfaları. Uygulama ayarı kendisi değiştirmez.
class SettingsIntents {
  const SettingsIntents._();

  static const batterySaver = 'android.settings.BATTERY_SAVER_SETTINGS';
  static const display = 'android.settings.DISPLAY_SETTINGS';
  static const internalStorage = 'android.settings.INTERNAL_STORAGE_SETTINGS';
  static const manageStorage = 'android.os.storage.action.MANAGE_STORAGE';

  static const targets = ['battery_saver', 'display', 'storage'];

  static List<String> actionsFor(String target) {
    return switch (target) {
      'battery_saver' => const [batterySaver],
      'display' => const [display],
      'storage' => const [manageStorage, internalStorage],
      _ => const [],
    };
  }

  static String labelFor(String target) {
    return switch (target) {
      'battery_saver' => 'Güç tasarrufu ayarı',
      'display' => 'Ekran ayarı',
      'storage' => 'Depolama ayarı',
      _ => 'Ayar',
    };
  }
}
