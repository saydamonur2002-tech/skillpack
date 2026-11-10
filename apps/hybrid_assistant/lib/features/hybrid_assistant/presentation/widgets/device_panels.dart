import 'package:flutter/material.dart';

import '../../domain/models/device_snapshot.dart';
import '../../domain/services/settings_intents.dart';

/// Pil, şarj, sıcaklık, güç tasarrufu ve boş depolama.
class DeviceLiveCards extends StatelessWidget {
  const DeviceLiveCards({super.key, required this.snapshot});

  final DeviceSnapshot snapshot;

  @override
  Widget build(BuildContext context) {
    final temp = snapshot.batteryTempC;
    final free = snapshot.availableBytes;
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: [
        _tile(context, 'Pil', snapshot.batteryPercent == null ? '—' : '%${snapshot.batteryPercent}'),
        _tile(context, 'Şarj', pluggedLabel(snapshot.pluggedType)),
        _tile(context, 'Pil sıcaklığı', temp == null ? '—' : '${temp.toStringAsFixed(1)} °C'),
        _tile(context, 'Güç tasarrufu', snapshot.isPowerSaveMode ? 'Açık' : 'Kapalı'),
        _tile(context, 'Boş depolama', free == null ? '—' : formatByteSize(free)),
      ],
    );
  }

  Widget _tile(BuildContext context, String label, String value) {
    final scheme = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color: scheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: TextStyle(color: scheme.onSurfaceVariant, fontSize: 11),
          ),
          const SizedBox(height: 2),
          Text(
            value,
            style: TextStyle(
              color: scheme.onSurface,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}

/// Isı durumu ve bellek kullanım yüzdesi.
class SystemHealthPanel extends StatelessWidget {
  const SystemHealthPanel({super.key, required this.snapshot});

  final DeviceSnapshot snapshot;

  @override
  Widget build(BuildContext context) {
    final memory = snapshot.memoryUsedPercent;
    final thermal = thermalStatusLabel(
      supported: snapshot.thermalSupported,
      status: snapshot.thermalStatus,
    );
    final scheme = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: scheme.surfaceContainerLow,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Sistem sağlığı',
            style: TextStyle(
              color: scheme.onSurface,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 6),
          Text(
            'Isı durumu: $thermal',
            style: TextStyle(color: scheme.onSurfaceVariant),
          ),
          const SizedBox(height: 4),
          Text(
            memory == null ? 'Bellek: ölçülemedi' : 'Bellek: %$memory kullanım',
            style: TextStyle(color: scheme.onSurfaceVariant),
          ),
        ],
      ),
    );
  }
}

class SettingsShortcutButtons extends StatelessWidget {
  const SettingsShortcutButtons({
    super.key,
    required this.targets,
    required this.onOpen,
  });

  final List<String> targets;
  final Future<void> Function(String target) onOpen;

  @override
  Widget build(BuildContext context) {
    if (targets.isEmpty) return const SizedBox.shrink();
    return Wrap(
      spacing: 8,
      children: [
        for (final target in targets)
          OutlinedButton(
            onPressed: () => onOpen(target),
            child: Text(SettingsIntents.labelFor(target)),
          ),
      ],
    );
  }
}
