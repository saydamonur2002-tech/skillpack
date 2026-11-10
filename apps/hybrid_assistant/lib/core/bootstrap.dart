import 'package:firebase_app_check/firebase_app_check.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

import '../features/hybrid_assistant/data/datasources/connectivity_guard.dart';
import '../features/hybrid_assistant/data/datasources/gemini_client.dart';
import '../features/hybrid_assistant/data/datasources/local_rules_loader.dart';
import '../features/hybrid_assistant/data/repositories/assistant_repository.dart';
import '../features/hybrid_assistant/domain/services/hot_patch_manager.dart';
import '../features/hybrid_assistant/domain/services/rule_engine.dart';
import '../features/hybrid_assistant/domain/services/token_budget_service.dart';
import 'firebase/firebase_options_stub.dart';
import 'storage/local_storage.dart';

/// Uygulama bağımlılıklarını ayağa kaldırır.
class AppBootstrap {
  late final LocalStorage localStorage;
  late final RuleEngine ruleEngine;
  late final HotPatchManager hotPatchManager;
  late final LocalRulesLoader localRulesLoader;
  late final ConnectivityGuard connectivityGuard;
  late final TokenBudgetService tokenBudgetService;
  late final GeminiClient geminiClient;
  late final AssistantRepository repository;
  bool firebaseReady = false;

  Future<void> init() async {
    localStorage = LocalStorage();
    ruleEngine = RuleEngine();
    hotPatchManager = HotPatchManager(storage: localStorage);
    localRulesLoader = LocalRulesLoader();
    connectivityGuard = ConnectivityGuard();
    tokenBudgetService = TokenBudgetService(storage: localStorage);

    try {
      await Firebase.initializeApp(
        options: DefaultFirebaseOptions.currentPlatform,
      );
      await _activateAppCheck();
      await FirebaseAuth.instance.signInAnonymously();
      geminiClient = FirebaseAiGeminiClient();
      firebaseReady = true;
    } catch (error, stack) {
      debugPrint('Firebase bootstrap skipped/failed: $error\n$stack');
      geminiClient = StubGeminiClient();
      firebaseReady = false;
    }

    repository = AssistantRepository(
      ruleEngine: ruleEngine,
      geminiClient: geminiClient,
      hotPatchManager: hotPatchManager,
      localRulesLoader: localRulesLoader,
      connectivityGuard: connectivityGuard,
      tokenBudgetService: tokenBudgetService,
      firebaseReady: firebaseReady,
    );
    await repository.initialize();
  }

  Future<void> _activateAppCheck() async {
    if (kDebugMode) {
      await FirebaseAppCheck.instance.activate(
        providerAndroid: const AndroidDebugProvider(),
        providerApple: const AppleDebugProvider(),
      );
    } else {
      await FirebaseAppCheck.instance.activate(
        providerAndroid: const AndroidPlayIntegrityProvider(),
        providerApple: const AppleAppAttestProvider(),
      );
    }
  }
}
