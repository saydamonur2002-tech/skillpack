import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:hybrid_assistant/core/storage/local_storage.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/data/datasources/connectivity_guard.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/data/datasources/gemini_client.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/data/datasources/local_rules_loader.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/data/datasources/system_probe.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/data/repositories/assistant_repository.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/models/device_snapshot.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/models/rule_model.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/services/hot_patch_manager.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/services/rule_engine.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/services/token_budget_service.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/domain/services/work_throttle.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('ısı pil ve bellek ağır işi keser', () {
    expect(
      WorkThrottle.evaluate(
        const DeviceSnapshot(thermalSupported: true, thermalStatus: 2),
      ).reason,
      'Isı yüksek, bulut atlandı',
    );
    expect(
      WorkThrottle.evaluate(const DeviceSnapshot(batteryTempRaw: 400)).reason,
      'Isı yüksek, bulut atlandı',
    );
    expect(
      WorkThrottle.evaluate(
        const DeviceSnapshot(batteryPercent: 12, isCharging: false),
      ).reason,
      'Pil düşük, yalnız yerel kural',
    );
    expect(
      WorkThrottle.evaluate(const DeviceSnapshot(isPowerSaveMode: true)).reason,
      'Pil düşük, yalnız yerel kural',
    );
    expect(
      WorkThrottle.evaluate(const DeviceSnapshot(lowMemory: true)).reason,
      'Bellek baskısı, yalnız yerel kural',
    );
    expect(
      WorkThrottle.evaluate(
        const DeviceSnapshot(batteryPercent: 80, batteryTempRaw: 250),
      ).skip,
      isFalse,
    );
  });

  test('kısıt varken gemini çağrılmaz', () async {
    final gemini = _RecordingGemini();
    final probe = _FakeProbe(
      const DeviceSnapshot(thermalSupported: true, thermalStatus: 2),
    );
    final repo = _repo(gemini, probe);
    final result = await repo.handle(query: 'bunu neden yaptın');
    expect(gemini.calls, 0);
    expect(result.throttleReason, 'Isı yüksek, bulut atlandı');
    expect(result.source, AssistantSource.localRule);
  });

  test('serin cihazda bulut yüküne kullanıcı cümlesi girmez', () async {
    SharedPreferences.setMockInitialValues({});
    final gemini = _RecordingGemini();
    final probe = _FakeProbe(
      const DeviceSnapshot(
        batteryPercent: 80,
        batteryTempRaw: 250,
        pluggedType: 'none',
      ),
    );
    final repo = _repo(gemini, probe);
    await repo.continueCloudExplain(
      query: 'ahmet@site.com bunu neden yaptın',
      localMessage: 'Yerel karar',
      ruleId: 'explain-need',
    );
    expect(gemini.calls, 1);
    expect(gemini.lastFigures, isNot(contains('ahmet')));
    expect(gemini.lastFigures, contains('batteryLevel'));
  });
}

AssistantRepository _repo(_RecordingGemini gemini, _FakeProbe probe) {
  final engine = RuleEngine()
    ..applyPack(
      RulePack.fromJson({
        'schema_version': '1.0',
        'pack_id': 't',
        'version': '1.0.0',
        'rules': [
          {
            'id': 'explain-need',
            'priority': 1,
            'when': {'field': 'intent', 'op': 'eq', 'value': 'explain'},
            'then': {
              'action': 'ask_cloud_explain',
              'message': 'Yerel kural eşleşti',
              'allow_cloud': true,
            },
          },
        ],
      }),
    );
  final storage = LocalStorage();
  return AssistantRepository(
    ruleEngine: engine,
    geminiClient: gemini,
    hotPatchManager: HotPatchManager(storage: storage),
    localRulesLoader: LocalRulesLoader(),
    connectivityGuard: ConnectivityGuard(),
    tokenBudgetService: TokenBudgetService(storage: storage),
    firebaseReady: true,
    systemProbe: probe,
  );
}

class _RecordingGemini implements GeminiClient {
  int calls = 0;
  String? lastFigures;

  @override
  Future<GeminiExplanation> explain({
    required String figures,
    required String localDecisionSummary,
    int maxOutputTokens = 256,
  }) async {
    calls += 1;
    lastFigures = figures;
    return const GeminiExplanation(
      text: 'kısa',
      promptTokens: 1,
      candidatesTokens: 1,
    );
  }

  @override
  Future<String> proposeRulePatchJson({
    required String currentRulesJson,
    required String instruction,
  }) async {
    return currentRulesJson;
  }
}

class _FakeProbe implements SystemProbe {
  _FakeProbe(this.latest);

  @override
  DeviceSnapshot latest;

  @override
  Stream<DeviceSnapshot> get snapshots => const Stream.empty();

  @override
  Future<void> start() async {}

  @override
  Future<void> stop() async {}

  @override
  Future<DeviceSnapshot> read() async => latest;

  @override
  Future<bool> openSettings(String target) async => true;
}
