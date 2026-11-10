import 'package:flutter_test/flutter_test.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/models/rule_model.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/services/rule_engine.dart';

void main() {
  test('önceliğe göre yerel kural eşleştirir', () {
    final engine = RuleEngine();
    engine.applyPack(
      RulePack.fromJson({
        'schema_version': '1.0',
        'pack_id': 't',
        'version': '1.0.0',
        'rules': [
          {
            'id': 'greet',
            'priority': 10,
            'when': {'field': 'intent', 'op': 'eq', 'value': 'greet'},
            'then': {'action': 'answer_local', 'message': 'hi'},
          },
          {
            'id': 'any',
            'priority': 100,
            'when': {'field': 'query', 'op': 'contains', 'value': ''},
            'then': {'action': 'fallback', 'message': 'fallback'},
          },
        ],
      }),
    );

    final match = engine.evaluate(
      const RuleContext(query: 'merhaba', intent: 'greet'),
    );
    expect(match?.rule.id, 'greet');
  });
}
