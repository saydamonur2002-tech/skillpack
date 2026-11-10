import 'package:flutter_test/flutter_test.dart';
import 'package:hybrid_assistant/core/storage/local_storage.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/services/token_budget_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  test('limit seçilmeden bulut çağrısı kullanıcıya sorulur', () async {
    final service = TokenBudgetService(storage: LocalStorage());
    await service.load();
    final decision = service.evaluate(estimatedTokens: 400);
    expect(decision.outcome, TokenBudgetOutcome.askUser);
    expect(decision.needsUserPrompt, isTrue);
  });

  test('kullanıcı limiti kaydedince izin verir', () async {
    final service = TokenBudgetService(storage: LocalStorage());
    await service.load();
    await service.setDailyLimitFromUser(5000);
    final decision = service.evaluate(estimatedTokens: 400);
    expect(decision.outcome, TokenBudgetOutcome.allow);
  });
}
