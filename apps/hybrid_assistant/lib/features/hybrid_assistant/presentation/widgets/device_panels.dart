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
        _tile('Pil', snapshot.batteryPercent == null ? '—' : '%${snapshot.batteryPercent}'),
        _tile('Şarj', pluggedLabel(snapshot.pluggedType)),
        _tile('Pil sıcaklığı', temp == null ? '—' : '${temp.toStringAsFixed(1)} °C'),
        _tile('Güç tasarrufu', snapshot.isPowerSaveMode ? 'Açık' : 'Kapalı'),
        _tile('Boş depolama', free == null ? '—' : formatByteSize(free)),
      ],
    );
  }

  Widget _tile(String label, String value) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0x33203028),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: const TextStyle(color: Color(0xFF8FA39A), fontSize: 11),
          ),
          const SizedBox(height: 2),
          Text(
            value,
            style: const TextStyle(
              color: Color(0xFFE7F0EC),
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
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFF3A4A44)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Sistem sağlığı',
            style: TextStyle(
              color: Color(0xFFD5E8DE),
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 6),
          Text(
            'Isı durumu: $thermal',
            style: const TextStyle(color: Color(0xFFB5C4BE)),
          ),
          const SizedBox(height: 4),
          Text(
            memory == null ? 'Bellek: ölçülemedi' : 'Bellek: %$memory kullanım',
            style: const TextStyle(color: Color(0xFFB5C4BE)),
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
