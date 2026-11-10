import 'package:flutter_test/flutter_test.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/services/rule_schema_validator.dart';

void main() {
  final validator = RuleSchemaValidator();

  test('geçerli kural paketini kabul eder', () {
    final result = validator.validate({
      'schema_version': '1.0',
      'pack_id': 'hybrid-assistant.demo',
      'version': '1.0.0',
      'budget': {
        'cloud_max_tokens_per_day': 2000,
        'on_exceed': 'ask_user',
      },
      'rules': [
        {
          'id': 'greet',
          'priority': 10,
          'when': {'field': 'intent', 'op': 'eq', 'value': 'greet'},
          'then': {
            'action': 'answer_local',
            'message': 'Merhaba',
            'allow_cloud': false,
          },
        },
      ],
    });
    expect(result.isValid, isTrue);
  });

  test('çalıştırılabilir kod alanını reddeder', () {
    final result = validator.validate({
      'schema_version': '1.0',
      'pack_id': 'bad.pack',
      'version': '1.0.0',
      'rules': [
        {
          'id': 'evil',
          'priority': 1,
          'when': {'field': 'intent', 'op': 'eq', 'value': 'x'},
          'then': {
            'action': 'answer_local',
            'script': 'print("nope")',
          },
        },
      ],
    });
    expect(result.isValid, isFalse);
    expect(result.errors.any((e) => e.contains('yasaklı')), isTrue);
  });
}
