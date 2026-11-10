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
      themeMode: ThemeMode.system,
      theme: _calmBlueTheme(Brightness.light),
      darkTheme: _calmBlueTheme(Brightness.dark),
      home: HomeScreen(
        repository: bootstrap.repository,
        tokenBudgetService: bootstrap.tokenBudgetService,
        probe: bootstrap.systemProbe,
        appCheckDebugToken: bootstrap.appCheckDebugToken,
      ),
    );
  }
}

ThemeData _calmBlueTheme(Brightness brightness) {
  const seed = Color(0xFF3D6FBF);
  final scheme = ColorScheme.fromSeed(seedColor: seed, brightness: brightness);
  final radius = BorderRadius.circular(12);
  final outline = OutlineInputBorder(
    borderRadius: radius,
    borderSide: BorderSide(color: scheme.outline),
  );
  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    scaffoldBackgroundColor: scheme.surface,
    cardTheme: CardThemeData(
      color: scheme.surfaceContainerLow,
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: radius),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: scheme.primary,
        foregroundColor: scheme.onPrimary,
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: scheme.primary,
        side: BorderSide(color: scheme.outline),
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: scheme.surfaceContainerHighest,
      hintStyle: TextStyle(color: scheme.onSurfaceVariant),
      border: outline,
      enabledBorder: outline,
      disabledBorder: outline.copyWith(
        borderSide: BorderSide(color: scheme.outlineVariant),
      ),
      focusedBorder: outline.copyWith(
        borderSide: BorderSide(color: scheme.primary, width: 2),
      ),
      errorBorder: outline.copyWith(
        borderSide: BorderSide(color: scheme.error),
      ),
      focusedErrorBorder: outline.copyWith(
        borderSide: BorderSide(color: scheme.error, width: 2),
      ),
    ),
  );
}
