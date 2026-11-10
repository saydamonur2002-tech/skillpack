import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
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
import 'package:hybrid_assistant/features/hybrid_assistant/presentation/screens/home_screen.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('küçük ekranda ana sayfa kayar ve taşmaz', (tester) async {
    await tester.binding.setSurfaceSize(const Size(320, 480));
    addTearDown(() => tester.binding.setSurfaceSize(null));

    final storage = LocalStorage();
    final engine = RuleEngine()
      ..applyPack(
        RulePack.fromJson({
          'schema_version': '1.0',
          'pack_id': 't',
          'version': '1.0.0',
          'rules': [
            {
              'id': 'unknown',
              'priority': 1,
              'when': {'field': 'query', 'op': 'contains', 'value': ''},
              'then': {'action': 'fallback', 'message': 'yedek'},
            },
          ],
        }),
      );
    final repo = AssistantRepository(
      ruleEngine: engine,
      geminiClient: _QuietGemini(),
      hotPatchManager: HotPatchManager(storage: storage),
      localRulesLoader: LocalRulesLoader(),
      connectivityGuard: ConnectivityGuard(),
      tokenBudgetService: TokenBudgetService(storage: storage),
      firebaseReady: true,
      systemProbe: _StillProbe(),
    );

    await tester.pumpWidget(
      MaterialApp(
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF3D6FBF)),
        ),
        home: HomeScreen(
          repository: repo,
          tokenBudgetService: repo.tokenBudgetService,
          probe: repo.systemProbe,
        ),
      ),
    );
    await tester.pump();
    expect(tester.takeException(), isNull);

    expect(find.text('skillpack'), findsOneWidget);
    final pageScroll = find.byType(Scrollable).first;
    await tester.scrollUntilVisible(
      find.text('Loglar'),
      250,
      scrollable: pageScroll,
    );
    await tester.scrollUntilVisible(
      find.byType(TextField),
      200,
      scrollable: pageScroll,
    );
    expect(find.byType(TextField), findsOneWidget);
    expect(find.text('Loglar'), findsOneWidget);
    expect(tester.takeException(), isNull);

    tester.view.viewInsets = const FakeViewPadding(bottom: 260);
    await tester.pump();
    await tester.scrollUntilVisible(
      find.byType(TextField),
      120,
      scrollable: pageScroll,
    );
    await tester.enterText(find.byType(TextField), 'merhaba');
    await tester.pump();
    expect(tester.takeException(), isNull);
    expect(find.text('merhaba'), findsOneWidget);
  });
}

class _QuietGemini implements GeminiClient {
  @override
  Future<GeminiExplanation> explain({
    required String figures,
    required String localDecisionSummary,
    int maxOutputTokens = 256,
  }) async {
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

class _StillProbe implements SystemProbe {
  @override
  DeviceSnapshot latest = DeviceSnapshot.empty;

  @override
  Stream<DeviceSnapshot> get snapshots => const Stream.empty();

  @override
  Future<void> start() async {}

  @override
  Future<void> stop() async {}

  @override
  Future<DeviceSnapshot> read() async => latest;

  @override
  Future<bool> openSettings(String target) async => false;
}
