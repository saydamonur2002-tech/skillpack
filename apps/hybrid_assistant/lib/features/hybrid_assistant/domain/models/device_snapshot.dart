/// Uygulama ön plandayken okunan cihaz ölçümü. İşlemci sıcaklığı yok.
class DeviceSnapshot {
  const DeviceSnapshot({
    this.batteryPercent,
    this.isCharging = false,
    this.pluggedType = 'none',
    this.batteryTempRaw,
    this.health = 'unknown',
    this.isPowerSaveMode = false,
    this.thermalSupported = false,
    this.thermalStatus,
    this.thermalHeadroom,
    this.availMem,
    this.totalMem,
    this.lowMemory = false,
    this.availableBytes,
    this.totalBytes,
    this.isMetered = false,
  });

  final int? batteryPercent;
  final bool isCharging;

  /// none, ac, usb, wireless, dock.
  final String pluggedType;
  final int? batteryTempRaw;

  /// Sistem durum kodu: unknown, good, overheat, dead, over_voltage,
  /// unspecified_failure, cold.
  final String health;
  final bool isPowerSaveMode;
  final bool thermalSupported;

  /// Android ısı kodu. 0 yok … 6 kapanma. API 29 altında null.
  final int? thermalStatus;

  /// API 30+. NaN veya destek yoksa null.
  final double? thermalHeadroom;
  final int? availMem;
  final int? totalMem;
  final bool lowMemory;
  final int? availableBytes;
  final int? totalBytes;
  final bool isMetered;

  static const empty = DeviceSnapshot();

  /// AOSP BatteryService: ham değer santigratın onda biridir.
  double? get batteryTempC => batteryTempCFromRaw(batteryTempRaw);

  bool get isPlugged => pluggedType != 'none';

  /// Kullanılan bellek yüzdesi: (totalMem - availMem) / totalMem.
  int? get memoryUsedPercent {
    final total = totalMem;
    final avail = availMem;
    if (total == null || avail == null || total <= 0) return null;
    final used = (total - avail).clamp(0, total);
    return ((used / total) * 100).round();
  }

  Map<String, Object?> toRuleValues() => {
        'battery_level': batteryPercent,
        'is_charging': isCharging,
        'is_plugged': isPlugged,
        'battery_temp_c': batteryTempC,
        'health': health,
        'power_save': isPowerSaveMode,
        'thermal_supported': thermalSupported,
        'thermal_status': thermalStatus,
        'low_memory': lowMemory,
        'available_bytes': availableBytes,
        'is_metered': isMetered,
      };

  /// Buluta giden yük: yalnız sayı ve durum kodu.
  Map<String, Object> toCloudFigures() => {
        if (batteryPercent != null) 'batteryLevel': batteryPercent!,
        if (batteryTempC != null) 'batteryTempC': batteryTempC!,
        if (thermalStatus != null) 'thermalStatus': thermalStatus!,
        'isCharging': isCharging,
        'pluggedType': pluggedType,
        'isPowerSaveMode': isPowerSaveMode,
        'isMetered': isMetered,
      };

  factory DeviceSnapshot.fromMap(Map<Object?, Object?> raw) {
    return DeviceSnapshot(
      batteryPercent: _asInt(raw['batteryPercent']),
      isCharging: raw['isCharging'] == true,
      pluggedType: raw['pluggedType'] as String? ?? 'none',
      batteryTempRaw: _asInt(raw['batteryTempRaw']),
      health: raw['health'] as String? ?? 'unknown',
      isPowerSaveMode: raw['isPowerSaveMode'] == true,
      thermalSupported: raw['thermalSupported'] == true,
      thermalStatus: _asInt(raw['thermalStatus']),
      thermalHeadroom: _asDouble(raw['thermalHeadroom']),
      availMem: _asInt(raw['availMem']),
      totalMem: _asInt(raw['totalMem']),
      lowMemory: raw['lowMemory'] == true,
      availableBytes: _asInt(raw['availableBytes']),
      totalBytes: _asInt(raw['totalBytes']),
      isMetered: raw['isMetered'] == true,
    );
  }
}

int? _asInt(Object? value) {
  if (value == null) return null;
  if (value is int) return value;
  if (value is double) return value.round();
  if (value is num) return value.toInt();
  return null;
}

double? _asDouble(Object? value) {
  if (value == null) return null;
  if (value is double) {
    if (value.isNaN) return null;
    return value;
  }
  if (value is num) return value.toDouble();
  return null;
}

double? batteryTempCFromRaw(int? raw) {
  if (raw == null) return null;
  return raw / 10.0;
}

String formatByteSize(int bytes) {
  final gb = bytes / 1000000000;
  if (gb >= 10) return '${gb.toStringAsFixed(0)} GB';
  if (gb >= 1) return '${gb.toStringAsFixed(1)} GB';
  final mb = bytes / 1000000;
  return '${mb.toStringAsFixed(0)} MB';
}

String pluggedLabel(String type) {
  return switch (type) {
    'ac' => 'AC',
    'usb' => 'USB',
    'wireless' => 'Kablosuz',
    'dock' => 'Dok',
    _ => 'Takılı değil',
  };
}

String thermalStatusLabel({
  required bool supported,
  required int? status,
}) {
  if (!supported) return 'Bu telefonda yok';
  return switch (status) {
    0 => 'Yok',
    1 => 'Hafif',
    2 => 'Orta',
    3 => 'Ciddi',
    4 => 'Kritik',
    5 => 'Acil',
    6 => 'Kapanma',
    _ => 'Bilinmiyor',
  };
}
