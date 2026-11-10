import '../models/rule_model.dart';

/// Lokal kural motoru — eşik ve mantık kontrolü.
///
/// Yalnızca bildirimsel JSON kurallarını yorumlar. Eval / dinamik kod yok.
/// İlke: karar betikte, açıklama modelde.
class RuleEngine {
  RulePack? _pack;

  RulePack? get pack => _pack;
  bool get isReady => _pack != null;

  void applyPack(RulePack pack) {
    if (pack.schemaVersion != '1.0') {
      throw StateError('Desteklenmeyen schema_version: ${pack.schemaVersion}');
    }
    _pack = pack;
  }

  RuleMatch? evaluate(RuleContext context) {
    final pack = _pack;
    if (pack == null) return null;

    for (final rule in pack.rules) {
      if (_matches(rule.when, context)) {
        return RuleMatch(rule: rule, pack: pack);
      }
    }
    return null;
  }

  bool _matches(RuleWhen when, RuleContext context) {
    final left = context[when.field];
    final right = when.value;

    switch (when.op) {
      case 'eq':
        return left?.toString() == right.toString();
      case 'contains':
        if (left is! String || right is! String) return false;
        if (right.isEmpty) return true;
        return left.toLowerCase().contains(right.toLowerCase());
      case 'starts_with':
        if (left is! String || right is! String) return false;
        return left.toLowerCase().startsWith(right.toLowerCase());
      case 'gte':
        return _asNum(left) != null &&
            _asNum(right) != null &&
            _asNum(left)! >= _asNum(right)!;
      case 'lte':
        return _asNum(left) != null &&
            _asNum(right) != null &&
            _asNum(left)! <= _asNum(right)!;
      default:
        return false;
    }
  }

  double? _asNum(Object? value) {
    if (value is num) return value.toDouble();
    if (value is String) return double.tryParse(value);
    return null;
  }
}
