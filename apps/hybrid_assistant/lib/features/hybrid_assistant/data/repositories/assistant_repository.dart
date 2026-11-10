import '../../../../core/constants.dart';
import '../../domain/models/rule_model.dart';
import '../../domain/services/hot_patch_manager.dart';
import '../../domain/services/rule_engine.dart';
import '../../domain/services/token_budget_service.dart';
import '../datasources/connectivity_guard.dart';
import '../datasources/gemini_client.dart';
import '../datasources/local_rules_loader.dart';

/// Lokal motor ile Gemini arasında karar köprüsü.
///
/// Akış: lokal kural → (gerekirse) token bütçesini kullanıcıya sor →
/// online ise Firebase AI Logic açıklama; değilse offline fallback.
class AssistantRepository {
  AssistantRepository({
    required this.ruleEngine,
    required this.geminiClient,
    required this.hotPatchManager,
    required this.localRulesLoader,
    required this.connectivityGuard,
    required this.tokenBudgetService,
    required this.firebaseReady,
  });

  final RuleEngine ruleEngine;
  final GeminiClient geminiClient;
  final HotPatchManager hotPatchManager;
  final LocalRulesLoader localRulesLoader;
  final ConnectivityGuard connectivityGuard;
  final TokenBudgetService tokenBudgetService;
  final bool firebaseReady;

  Future<void> initialize() async {
    final bundled = await localRulesLoader.loadBundled();
    ruleEngine.applyPack(bundled);
    await hotPatchManager.hydrateEngine(ruleEngine);
    await tokenBudgetService.load();
    await connectivityGuard.start();
  }

  Future<AssistantResult> handle({
    required String query,
    String? intent,
  }) async {
    final context = RuleContext(
      query: query,
      intent: intent ?? _guessIntent(query),
    );
    final match = ruleEngine.evaluate(context);

    if (match == null) {
      return AssistantResult(
        source: AssistantSource.offlineFallback,
        title: 'Yedek yanıt',
        body: connectivityGuard.fallbackMessage(),
        engineStatus: EngineStatus.localActive,
      );
    }

    final action = match.rule.then.action;
    final localMessage =
        match.rule.then.message ?? 'Kural eşleşti: ${match.rule.id}';

    if (action == 'answer_local' ||
        action == 'fallback' ||
        !match.rule.then.allowCloud) {
      return AssistantResult(
        source: AssistantSource.localRule,
        title: 'Yerel kural: ${match.rule.id}',
        body: localMessage,
        ruleId: match.rule.id,
        engineStatus: EngineStatus.localActive,
      );
    }

    if (connectivityGuard.isOffline) {
      return AssistantResult(
        source: AssistantSource.offlineFallback,
        title: 'Yerel kural (çevrimdışı)',
        body: connectivityGuard.fallbackMessage(localRuleMessage: localMessage),
        ruleId: match.rule.id,
        engineStatus: EngineStatus.offline,
      );
    }

    final budget = tokenBudgetService.evaluate(
      estimatedTokens: AppConstants.estimatedExplainTokens,
    );
    if (budget.needsUserPrompt) {
      return AssistantResult(
        source: AssistantSource.needsUser,
        title: 'Günlük token maliyeti',
        body: budget.reason,
        ruleId: match.rule.id,
        needsTokenBudgetPrompt: true,
        budgetDecision: budget,
        pendingLocalSummary: localMessage,
        pendingQuery: query,
        engineStatus: EngineStatus.awaitingBudget,
      );
    }

    return continueCloudExplain(
      query: query,
      localMessage: localMessage,
      ruleId: match.rule.id,
    );
  }

  Future<AssistantResult> continueCloudExplain({
    required String query,
    required String localMessage,
    String? ruleId,
  }) async {
    try {
      final explanation = await geminiClient.explain(
        query: query,
        localDecisionSummary: localMessage,
      );
      await tokenBudgetService.recordUsage(
        explanation.totalTokens == 0
            ? AppConstants.estimatedExplainTokens
            : explanation.totalTokens,
      );
      return AssistantResult(
        source: AssistantSource.cloudExplain,
        title: 'Yerel karar + bulut açıklama',
        body: '$localMessage\n\n${explanation.text}',
        ruleId: ruleId,
        tokensUsed: explanation.totalTokens,
        engineStatus: EngineStatus.geminiConnected,
      );
    } catch (error) {
      final detail = error.toString();
      return AssistantResult(
        source: AssistantSource.offlineFallback,
        title: 'Bulut hatası — yedek',
        body: '${connectivityGuard.fallbackMessage(localRuleMessage: localMessage)}\n\n$detail',
        ruleId: ruleId,
        errorDetail: detail,
        engineStatus: EngineStatus.offline,
      );
    }
  }

  String _guessIntent(String query) {
    final q = query.toLowerCase();
    if (q.contains('merhaba') || q.contains('selam') || q.contains('hello')) {
      return 'greet';
    }
    if (q.contains('neden') || q.contains('açıkla') || q.contains('explain')) {
      return 'explain';
    }
    return 'unknown';
  }
}

enum AssistantSource {
  localRule,
  cloudExplain,
  offlineFallback,
  needsUser,
}

enum EngineStatus {
  localActive,
  geminiConnected,
  offline,
  awaitingBudget,
}

class AssistantResult {
  const AssistantResult({
    required this.source,
    required this.title,
    required this.body,
    required this.engineStatus,
    this.ruleId,
    this.needsTokenBudgetPrompt = false,
    this.budgetDecision,
    this.pendingLocalSummary,
    this.pendingQuery,
    this.tokensUsed,
    this.errorDetail,
  });

  final AssistantSource source;
  final String title;
  final String body;
  final EngineStatus engineStatus;
  final String? ruleId;
  final bool needsTokenBudgetPrompt;
  final TokenBudgetDecision? budgetDecision;
  final String? pendingLocalSummary;
  final String? pendingQuery;
  final int? tokensUsed;

  /// Bulut çağrısı düşerse yutulan istisnanın metni. Ağ kopukluğu değil.
  final String? errorDetail;
}
