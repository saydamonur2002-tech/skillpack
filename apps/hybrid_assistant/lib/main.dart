import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'app.dart';
import 'core/bootstrap.dart';

/// Uygulamanın başlangıç noktası ve ana çatı.
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
  ]);

  final bootstrap = AppBootstrap();
  await bootstrap.init();

  runApp(HybridAssistantApp(bootstrap: bootstrap));
}
