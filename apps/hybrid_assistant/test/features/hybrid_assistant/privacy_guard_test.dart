import 'package:flutter_test/flutter_test.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/models/device_snapshot.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/services/privacy_guard.dart';

void main() {
  test('e-posta telefon TC IBAN ve plakayı maskeler', () {
    const validTc = '10000000078';
    const invalidTc = '10000000079';
    const iban = 'TR330006100519786457841326';
    final masked = PrivacyGuard.mask(
      'posta a.b@site.com tel +90 532 111 22 33 ve 05321112233 '
      'tc $validTc bozuk $invalidTc iban $iban plaka 34 ABC 123 '
      'yanlis 99 AB 12',
    );

    expect(masked, contains('[e-posta]'));
    expect(masked, contains('[telefon]'));
    expect(masked, contains('[tc-no]'));
    expect(masked, contains('[iban]'));
    expect(masked, contains('[plaka]'));
    expect(masked, isNot(contains('a.b@site.com')));
    expect(masked, isNot(contains('532')));
    expect(masked, isNot(contains(validTc)));
    expect(masked, contains(invalidTc));
    expect(masked, isNot(contains('TR33')));
    expect(masked, contains('99 AB 12'));
  });

  test('bulut yükü yalnız sayı ve durum kodu taşır', () {
    const snapshot = DeviceSnapshot(
      batteryPercent: 18,
      batteryTempRaw: 412,
      isCharging: false,
      pluggedType: 'usb',
      isPowerSaveMode: true,
      thermalSupported: true,
      thermalStatus: 3,
      isMetered: true,
    );
    final figures = snapshot.toCloudFigures();
    final text = PrivacyGuard.figuresText(figures);
    expect(PrivacyGuard.figuresAreSafe(figures), isTrue);
    expect(text, contains('batteryLevel: 18'));
    expect(text, contains('batteryTempC: 41.2'));
    expect(text, isNot(contains('@')));
    expect(text, isNot(contains('Ahmet')));
  });
}
