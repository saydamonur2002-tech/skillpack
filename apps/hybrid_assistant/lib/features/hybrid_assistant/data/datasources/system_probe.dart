import 'dart:async';

import 'package:flutter/services.dart';

import '../../domain/models/device_snapshot.dart';

/// Ön plan ölçümü. 5 saniyelik yoklama ve ön plan servisi yok.
abstract class SystemProbe {
  DeviceSnapshot get latest;

  Stream<DeviceSnapshot> get snapshots;

  Future<void> start();

  Future<void> stop();

  Future<DeviceSnapshot> read();

  /// Sayfa yoksa false. Uygulama düşmez.
  Future<bool> openSettings(String target);
}

class AndroidSystemProbe implements SystemProbe {
  AndroidSystemProbe();

  static const _events =
      EventChannel('com.skillpack.hybrid_assistant/system_events');
  static const _methods =
      MethodChannel('com.skillpack.hybrid_assistant/system_methods');

  final _controller = StreamController<DeviceSnapshot>.broadcast();
  StreamSubscription<dynamic>? _sub;
  DeviceSnapshot _latest = DeviceSnapshot.empty;

  @override
  DeviceSnapshot get latest => _latest;

  @override
  Stream<DeviceSnapshot> get snapshots => _controller.stream;

  @override
  Future<void> start() async {
    if (_sub != null) return;
    _sub = _events.receiveBroadcastStream().listen(
      (event) {
        if (event is! Map) return;
        _latest = DeviceSnapshot.fromMap(event);
        if (!_controller.isClosed) _controller.add(_latest);
      },
      onError: (Object _) {},
    );
  }

  @override
  Future<void> stop() async {
    await _sub?.cancel();
    _sub = null;
  }

  @override
  Future<DeviceSnapshot> read() async {
    final raw = await _methods.invokeMapMethod<Object?, Object?>('read');
    _latest = DeviceSnapshot.fromMap(raw ?? const {});
    if (!_controller.isClosed) _controller.add(_latest);
    return _latest;
  }

  @override
  Future<bool> openSettings(String target) async {
    final opened = await _methods.invokeMethod<bool>(
      'openSettings',
      {'target': target},
    );
    return opened ?? false;
  }
}
