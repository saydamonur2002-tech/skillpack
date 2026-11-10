import 'package:flutter/material.dart';

import '../../data/repositories/assistant_repository.dart';
import '../../domain/models/device_snapshot.dart';

/// "Lokal Motor Aktif" veya "Gemini'ye Bağlandı" göstergesi.
class StatusCard extends StatelessWidget {
  const StatusCard({
    super.key,
    required this.status,
    required this.firebaseReady,
    this.cloudError = false,
    this.freeBytes,
    this.totalBytes,
  });

  final EngineStatus status;
  final bool firebaseReady;
  final int? freeBytes;
  final int? totalBytes;

  /// Bulut çağrısı hata verdi. Ağ durumu değil.
  final bool cloudError;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final (label, color) = cloudError
        ? ('Bulut hatası', scheme.error)
        : switch (status) {
      EngineStatus.localActive => ('Lokal Motor Aktif', scheme.primary),
      EngineStatus.geminiConnected => (
          'Gemini\'ye Bağlandı',
          scheme.tertiary,
        ),
      EngineStatus.offline => ('Çevrimdışı — yerel yedek', scheme.error),
      EngineStatus.awaitingBudget => (
          'Günlük token onayı bekleniyor',
          scheme.secondary,
        ),
    };

    return Semantics(
      label: label,
      child: Row(
        children: [
          Container(
            width: 8,
            height: 8,
            decoration: BoxDecoration(
              color: color,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  firebaseReady ? label : '$label · Firebase stub',
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: scheme.onSurface,
                      ),
                ),
                if (freeBytes != null && totalBytes != null)
                  Text(
                    'Depolama ${formatByteSize(freeBytes!)} boş / ${formatByteSize(totalBytes!)}',
                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                          color: scheme.onSurfaceVariant,
                        ),
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
