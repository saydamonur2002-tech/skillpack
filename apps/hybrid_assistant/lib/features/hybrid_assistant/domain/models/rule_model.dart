/// Kural yapısının (JSON) veri modeli.
/// Çalıştırılabilir kod alanı taşımaz — yalnız bildirimsel veri.
class RulePack {
  RulePack({
    required this.schemaVersion,
    required this.packId,
    required this.version,
    required this.rules,
    this.updatedAt,
    this.cloudMaxTokensPerDay,
    this.onExceed = 'ask_user',
  });

  final String schemaVersion;
  final String packId;
  final String version;
  final DateTime? updatedAt;
  final int? cloudMaxTokensPerDay;
  final String onExceed;
  final List<RuleModel> rules;

  factory RulePack.fromJson(Map<String, dynamic> json) {
    final budget = json['budget'] as Map<String, dynamic>?;
    return RulePack(
      schemaVersion: json['schema_version'] as String,
      packId: json['pack_id'] as String,
      version: json['version'] as String,
      updatedAt: json['updated_at'] != null
          ? DateTime.tryParse(json['updated_at'] as String)
          : null,
      cloudMaxTokensPerDay: budget?['cloud_max_tokens_per_day'] as int?,
      onExceed: (budget?['on_exceed'] as String?) ?? 'ask_user',
      rules: (json['rules'] as List<dynamic>)
          .map((e) => RuleModel.fromJson(e as Map<String, dynamic>))
          .toList()
        ..sort((a, b) => a.priority.compareTo(b.priority)),
    );
  }

  Map<String, dynamic> toJson() => {
        'schema_version': schemaVersion,
        'pack_id': packId,
        'version': version,
        if (updatedAt != null)
          'updated_at': updatedAt!.toUtc().toIso8601String(),
        'budget': {
          if (cloudMaxTokensPerDay != null)
            'cloud_max_tokens_per_day': cloudMaxTokensPerDay,
          'on_exceed': onExceed,
        },
        'rules': rules.map((r) => r.toJson()).toList(),
      };
}

class RuleModel {
  RuleModel({
    required this.id,
    required this.priority,
    required this.when,
    required this.then,
    this.description,
  });

  final String id;
  final int priority;
  final String? description;
  final RuleWhen when;
  final RuleThen then;

  factory RuleModel.fromJson(Map<String, dynamic> json) => RuleModel(
        id: json['id'] as String,
        priority: json['priority'] as int,
        description: json['description'] as String?,
        when: RuleWhen.fromJson(json['when'] as Map<String, dynamic>),
        then: RuleThen.fromJson(json['then'] as Map<String, dynamic>),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'priority': priority,
        if (description != null) 'description': description,
        'when': when.toJson(),
        'then': then.toJson(),
      };
}

class RuleWhen {
  RuleWhen({
    this.field,
    this.op,
    this.value,
    this.all = const [],
    this.any = const [],
  });

  final String? field;
  final String? op;
  final Object? value;
  final List<RuleWhen> all;
  final List<RuleWhen> any;

  factory RuleWhen.fromJson(Map<String, dynamic> json) {
    final all = json['all'];
    if (all is List) {
      return RuleWhen(
        all: all
            .map((e) => RuleWhen.fromJson(e as Map<String, dynamic>))
            .toList(),
      );
    }
    final any = json['any'];
    if (any is List) {
      return RuleWhen(
        any: any
            .map((e) => RuleWhen.fromJson(e as Map<String, dynamic>))
            .toList(),
      );
    }
    return RuleWhen(
      field: json['field'] as String?,
      op: json['op'] as String?,
      value: json['value'],
    );
  }

  Map<String, dynamic> toJson() => {
        if (all.isNotEmpty) 'all': all.map((e) => e.toJson()).toList(),
        if (any.isNotEmpty) 'any': any.map((e) => e.toJson()).toList(),
        if (field != null) 'field': field,
        if (op != null) 'op': op,
        if (value != null) 'value': value,
      };
}

class RuleThen {
  RuleThen({
    required this.action,
    this.message,
    this.allowCloud = false,
    this.settings = const [],
  });

  final String action;
  final String? message;
  final bool allowCloud;

  /// battery_saver, display, storage. Yalnız ayar sayfası açar.
  final List<String> settings;

  factory RuleThen.fromJson(Map<String, dynamic> json) => RuleThen(
        action: json['action'] as String,
        message: json['message'] as String?,
        allowCloud: json['allow_cloud'] as bool? ?? false,
        settings: (json['settings'] as List<dynamic>?)
                ?.map((e) => e as String)
                .toList() ??
            const [],
      );

  Map<String, dynamic> toJson() => {
        'action': action,
        if (message != null) 'message': message,
        'allow_cloud': allowCloud,
        if (settings.isNotEmpty) 'settings': settings,
      };
}

class RuleContext {
  const RuleContext({
    required this.query,
    this.intent,
    this.category,
    this.confidence,
    this.values = const {},
  });

  final String query;
  final String? intent;
  final String? category;
  final double? confidence;
  final Map<String, Object?> values;

  Object? operator [](String field) {
    switch (field) {
      case 'query':
        return query;
      case 'intent':
        return intent;
      case 'category':
        return category;
      case 'confidence':
        return confidence;
      default:
        return values[field];
    }
  }
}

class RuleMatch {
  const RuleMatch({required this.rule, required this.pack});

  final RuleModel rule;
  final RulePack pack;
}
