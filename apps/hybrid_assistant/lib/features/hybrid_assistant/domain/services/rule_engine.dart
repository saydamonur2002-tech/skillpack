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
    if (when.all.isNotEmpty) {
      return when.all.every((child) => _matches(child, context));
    }
    if (when.any.isNotEmpty) {
      return when.any.any((child) => _matches(child, context));
    }
    final field = when.field;
    final op = when.op;
    if (field == null || op == null) return false;
    final left = context[field];
    final right = when.value;

    switch (op) {
      case 'eq':
        return left?.toString() == right?.toString();
      case 'contains':
        if (left is! String || right is! String) return false;
        if (right.isEmpty) return true;
        return left.toLowerCase().contains(right.toLowerCase());
      case 'starts_with':
        if (left is! String || right is! String) return false;
        return left.toLowerCase().startsWith(right.toLowerCase());
      case 'gte':
        return _cmp(left, right, (a, b) => a >= b);
      case 'lte':
        return _cmp(left, right, (a, b) => a <= b);
      case 'gt':
        return _cmp(left, right, (a, b) => a > b);
      case 'lt':
        return _cmp(left, right, (a, b) => a < b);
      default:
        return false;
    }
  }

  bool _cmp(Object? left, Object? right, bool Function(double, double) test) {
    final a = _asNum(left);
    final b = _asNum(right);
    if (a == null || b == null) return false;
    return test(a, b);
  }

  double? _asNum(Object? value) {
    if (value is num) return value.toDouble();
    if (value is String) return double.tryParse(value);
    return null;
  }
}
