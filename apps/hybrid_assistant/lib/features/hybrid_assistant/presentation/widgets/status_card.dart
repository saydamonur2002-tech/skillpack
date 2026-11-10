import 'package:flutter/material.dart';

import '../../data/repositories/assistant_repository.dart';

/// "Lokal Motor Aktif" veya "Gemini'ye Bağlandı" göstergesi.
class StatusCard extends StatelessWidget {
  const StatusCard({
    super.key,
    required this.status,
    required this.firebaseReady,
  });

  final EngineStatus status;
  final bool firebaseReady;

  @override
  Widget build(BuildContext context) {
    final (label, color) = switch (status) {
      EngineStatus.localActive => (
          'Lokal Motor Aktif',
          const Color(0xFF7CB89A),
        ),
      EngineStatus.geminiConnected => (
          'Gemini\'ye Bağlandı',
          const Color(0xFF6AA8D6),
        ),
      EngineStatus.offline => (
          'Çevrimdışı — yerel yedek',
          const Color(0xFFC4A35A),
        ),
      EngineStatus.awaitingBudget => (
          'Günlük token onayı bekleniyor',
          const Color(0xFFB89A7C),
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
            child: Text(
              firebaseReady ? label : '$label · Firebase stub',
              style: Theme.of(context).textTheme.labelMedium?.copyWith(
                    color: const Color(0xFF9BB0A6),
                  ),
            ),
          ),
        ],
      ),
    );
  }
}
