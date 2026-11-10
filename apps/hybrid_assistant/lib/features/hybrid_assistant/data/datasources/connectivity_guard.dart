import 'dart:async';

import 'package:connectivity_plus/connectivity_plus.dart';

/// Çevrimdışı durumlar için ağ gözlemcisi.
class ConnectivityGuard {
  ConnectivityGuard({Connectivity? connectivity})
      : _connectivity = connectivity ?? Connectivity();

  final Connectivity _connectivity;
  StreamSubscription<List<ConnectivityResult>>? _sub;
  bool _online = true;

  bool get isOnline => _online;
  bool get isOffline => !_online;

  static const offlineMessage =
      'Çevrimdışısınız. Karar yerel kurallarla verildi; bulut açıklaması ertelendi.';

  Future<void> start() async {
    final current = await _connectivity.checkConnectivity();
    _online = _hasNetwork(current);
    _sub = _connectivity.onConnectivityChanged.listen((results) {
      _online = _hasNetwork(results);
    });
  }

  bool _hasNetwork(List<ConnectivityResult> results) {
    if (results.isEmpty) return false;
    return results.any((r) => r != ConnectivityResult.none);
  }

  String fallbackMessage({String? localRuleMessage}) {
    if (localRuleMessage != null && localRuleMessage.trim().isNotEmpty) {
      return '$localRuleMessage\n\n$offlineMessage';
    }
    return offlineMessage;
  }

  Future<void> dispose() async {
    await _sub?.cancel();
  }
}
