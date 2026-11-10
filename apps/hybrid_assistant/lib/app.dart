import 'package:flutter/material.dart';

import 'core/bootstrap.dart';
import 'features/hybrid_assistant/presentation/screens/home_screen.dart';

/// Tema, yönlendirme ve global ayarlar.
class HybridAssistantApp extends StatelessWidget {
  const HybridAssistantApp({super.key, required this.bootstrap});

  final AppBootstrap bootstrap;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'skillpack',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF7CB89A),
          brightness: Brightness.dark,
        ),
      ),
      home: HomeScreen(
        repository: bootstrap.repository,
        tokenBudgetService: bootstrap.tokenBudgetService,
        probe: bootstrap.systemProbe,
        appCheckDebugToken: bootstrap.appCheckDebugToken,
      ),
    );
  }
}
