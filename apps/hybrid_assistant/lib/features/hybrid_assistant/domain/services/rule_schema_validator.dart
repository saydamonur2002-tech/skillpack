/// Hot-patch öncesi JSON şema + yasaklı kod alanı kontrolü.
class RuleSchemaValidator {
  static const allowedRootKeys = {
    'schema_version',
    'pack_id',
    'version',
    'updated_at',
    'budget',
    'rules',
  };

  static const allowedFields = {
    'intent',
    'query',
    'category',
    'confidence',
    'battery_level',
    'is_charging',
    'is_plugged',
    'battery_temp_c',
    'health',
    'power_save',
    'thermal_supported',
    'thermal_status',
    'low_memory',
    'available_bytes',
    'is_metered',
  };

  static const allowedOps = {
    'eq',
    'contains',
    'starts_with',
    'gte',
    'lte',
    'gt',
    'lt',
  };

  static const allowedSettings = {'battery_saver', 'display', 'storage'};

  static const forbiddenKeys = {
    'code',
    'script',
    'scripts',
    'bytecode',
    'wasm',
    'eval',
    'javascript',
    'dart',
    'native',
    'executable',
    'shell',
    'command',
    'url_to_code',
    'download_url',
  };

  ValidationResult validate(Map<String, dynamic> json) {
    final errors = <String>[];
    _rejectForbidden(json, r'$', errors);

    for (final key in json.keys) {
      if (!allowedRootKeys.contains(key)) {
        errors.add('Bilinmeyen kök alan: $key');
      }
    }

    if (json['schema_version'] != '1.0') {
      errors.add('schema_version "1.0" olmalı');
    }

    final packId = json['pack_id'];
    if (packId is! String ||
        !RegExp(r'^[a-z0-9][a-z0-9._-]{0,127}$').hasMatch(packId)) {
      errors.add('pack_id geçersiz');
    }

    final version = json['version'];
    if (version is! String ||
        !RegExp(r'^[0-9]+\.[0-9]+\.[0-9]+$').hasMatch(version)) {
      errors.add('version SemVer olmalı (x.y.z)');
    }

    final budget = json['budget'];
    if (budget != null) {
      if (budget is! Map<String, dynamic>) {
        errors.add('budget nesne olmalı');
      } else {
        final max = budget['cloud_max_tokens_per_day'];
        if (max != null && (max is! int || max < 0)) {
          errors.add('cloud_max_tokens_per_day >= 0 tamsayı olmalı');
        }
        final onExceed = budget['on_exceed'];
        if (onExceed != null &&
            (onExceed is! String ||
                !{'ask_user', 'local_only', 'deny'}.contains(onExceed))) {
          errors.add('on_exceed ask_user|local_only|deny olmalı');
        }
      }
    }

    final rules = json['rules'];
    if (rules is! List || rules.isEmpty) {
      errors.add('rules boş olamaz');
    } else if (rules.length > 200) {
      errors.add('rules en fazla 200 olabilir');
    } else {
      for (var i = 0; i < rules.length; i++) {
        _validateRule(rules[i], i, errors);
      }
    }

    return errors.isEmpty
        ? const ValidationResult.ok()
        : ValidationResult.failed(errors);
  }

  void _validateRule(Object? raw, int index, List<String> errors) {
    if (raw is! Map<String, dynamic>) {
      errors.add('rules[$index] nesne olmalı');
      return;
    }
    _rejectForbidden(raw, 'rules[$index]', errors);

    for (final required in ['id', 'priority', 'when', 'then']) {
      if (!raw.containsKey(required)) {
        errors.add('rules[$index].$required zorunlu');
      }
    }

    final when = raw['when'];
    if (when is Map<String, dynamic>) {
      _validateWhen(when, 'rules[$index].when', errors);
    }

    final then = raw['then'];
    if (then is Map<String, dynamic>) {
      _rejectForbidden(then, 'rules[$index].then', errors);
      if (!{'answer_local', 'ask_cloud_explain', 'ask_user', 'fallback'}
          .contains(then['action'])) {
        errors.add('rules[$index].then.action geçersiz');
      }
      final settings = then['settings'];
      if (settings != null) {
        if (settings is! List ||
            settings.any((item) => !allowedSettings.contains(item))) {
          errors.add('rules[$index].then.settings geçersiz');
        }
      }
    }
  }

  void _validateWhen(Map<String, dynamic> when, String path, List<String> errors) {
    _rejectForbidden(when, path, errors);
    final all = when['all'];
    final any = when['any'];
    if (all != null || any != null) {
      final list = all ?? any;
      if (list is! List || list.isEmpty) {
        errors.add('$path bileşik koşul boş');
        return;
      }
      for (var i = 0; i < list.length; i++) {
        final child = list[i];
        if (child is Map<String, dynamic>) {
          _validateWhen(child, '$path[$i]', errors);
        } else {
          errors.add('$path[$i] nesne olmalı');
        }
      }
      return;
    }
    if (!allowedFields.contains(when['field'])) {
      errors.add('$path.field geçersiz');
    }
    if (!allowedOps.contains(when['op'])) {
      errors.add('$path.op geçersiz');
    }
  }

  void _rejectForbidden(
    Map<String, dynamic> map,
    String path,
    List<String> errors,
  ) {
    for (final key in map.keys) {
      if (forbiddenKeys.contains(key.toLowerCase())) {
        errors.add('$path.$key yasaklı (yalnız JSON veri; kod indirilemez)');
      }
      final value = map[key];
      if (value is Map<String, dynamic>) {
        _rejectForbidden(value, '$path.$key', errors);
      } else if (value is List) {
        for (var i = 0; i < value.length; i++) {
          final item = value[i];
          if (item is Map<String, dynamic>) {
            _rejectForbidden(item, '$path.$key[$i]', errors);
          }
        }
      }
    }
  }
}

class ValidationResult {
  const ValidationResult.ok()
      : isValid = true,
        errors = const [];

  const ValidationResult.failed(this.errors) : isValid = false;

  final bool isValid;
  final List<String> errors;
}
