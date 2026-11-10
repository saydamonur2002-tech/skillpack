import '../models/device_snapshot.dart';

/// Ağır iş (bulut ve varsa yerel model) bu koşullarda kesilir.
class ThrottleDecision {
  const ThrottleDecision.allow() : reason = null;

  const ThrottleDecision.skip(this.reason);

  final String? reason;
  bool get skip => reason != null;
}

class WorkThrottle {
  const WorkThrottle._();

  static ThrottleDecision evaluate(DeviceSnapshot snapshot) {
    final thermal = snapshot.thermalStatus;
    final hot = (snapshot.thermalSupported && thermal != null && thermal >= 2) ||
        ((snapshot.batteryTempC ?? -1) >= 40);
    if (hot) {
      return const ThrottleDecision.skip('Isı yüksek, bulut atlandı');
    }
    if (snapshot.lowMemory) {
      return const ThrottleDecision.skip('Bellek baskısı, yalnız yerel kural');
    }
    final lowBattery = snapshot.batteryPercent != null &&
        snapshot.batteryPercent! < 20 &&
        !snapshot.isCharging;
    if (snapshot.isPowerSaveMode || lowBattery) {
      return const ThrottleDecision.skip('Pil düşük, yalnız yerel kural');
    }
    return const ThrottleDecision.allow();
  }
}
