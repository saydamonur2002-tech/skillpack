import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

/// Debug derlemede App Check anahtarını gösterir ve kopyalatır.
///
/// Release derlemesinde hiçbir şey çizmez.
class AppCheckDebugTokenBanner extends StatelessWidget {
  const AppCheckDebugTokenBanner({super.key, required this.token});

  final String token;

  @override
  Widget build(BuildContext context) {
    if (!kDebugMode) return const SizedBox.shrink();

    final theme = Theme.of(context);
    final scheme = theme.colorScheme;
    return Container(
      padding: const EdgeInsets.fromLTRB(12, 12, 12, 4),
      decoration: BoxDecoration(
        color: scheme.surfaceContainerLow,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            'App Check debug anahtarı',
            style: theme.textTheme.labelLarge?.copyWith(
              color: scheme.onSurface,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'Kopyalayıp Firebase konsolunda App Check debug token '
            'listesine ekleyin.',
            style: theme.textTheme.bodySmall?.copyWith(
              color: scheme.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: 8),
          SelectableText(
            token,
            style: theme.textTheme.bodyMedium?.copyWith(
              color: scheme.onSurface,
              fontFamily: 'monospace',
              letterSpacing: 0.2,
            ),
          ),
          Align(
            alignment: Alignment.centerRight,
            child: TextButton.icon(
              onPressed: () => _copy(context),
              icon: const Icon(Icons.copy_rounded, size: 16),
              label: const Text('Kopyala'),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _copy(BuildContext context) async {
    await Clipboard.setData(ClipboardData(text: token));
    if (!context.mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Anahtar kopyalandı')),
    );
  }
}
