import 'package:flutter_test/flutter_test.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/models/rule_model.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/services/rule_engine.dart';

void main() {
  test('iskelet kural motoru smoke', () {
    final engine = RuleEngine();
    engine.applyPack(
      RulePack.fromJson({
        'schema_version': '1.0',
        'pack_id': 'smoke',
        'version': '0.0.1',
        'rules': [
          {
            'id': 'x',
            'priority': 1,
            'when': {'field': 'query', 'op': 'contains', 'value': ''},
            'then': {'action': 'fallback', 'message': 'ok'},
          },
        ],
      }),
    );
    expect(engine.isReady, isTrue);
  });
}
