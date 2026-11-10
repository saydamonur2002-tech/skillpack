// ignore_for_file: unused_import
import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;
import 'package:flutter/foundation.dart'
    show defaultTargetPlatform, kIsWeb, TargetPlatform;

/// Geçici stub. Gerçek değerler için:
/// `dart pub global activate flutterfire_cli && flutterfire configure`
///
/// Bu dosya API anahtarı içermez. Firebase proje kimlikleri istemci tarafında
/// herkese açık yapılandırmadır; Gemini API anahtarı sunucuda / Firebase AI
/// Logic tarafında kalır.
class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      throw UnsupportedError('Web henüz yapılandırılmadı.');
    }
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return android;
      case TargetPlatform.iOS:
        return ios;
      default:
        throw UnsupportedError(
          'Bu platform için firebase_options henüz yok. '
          '`flutterfire configure` çalıştırın.',
        );
    }
  }

  static const FirebaseOptions android = FirebaseOptions(
    apiKey: 'AIzaSyDYXyvuiAY2VBGlTzkM8iXcNHIRGtXLbWs',
    appId: '1:1040345550813:android:60ca4a7cd628aec8aff034',
    messagingSenderId: '1040345550813',
    projectId: 'mini-asistan-139c0',
    storageBucket: 'mini-asistan-139c0.firebasestorage.app',
  );

  static const FirebaseOptions ios = FirebaseOptions(
    apiKey: 'REPLACE_WITH_FIREBASE_WEB_API_KEY',
    appId: '1:000000000000:ios:0000000000000000000000',
    messagingSenderId: '000000000000',
    projectId: 'REPLACE_PROJECT_ID',
    storageBucket: 'REPLACE_PROJECT_ID.appspot.com',
    iosBundleId: 'com.skillpack.hybridAssistant',
  );
}
