import 'package:firebase_ai/firebase_ai.dart';

import '../../../../core/constants.dart';
import '../../domain/services/privacy_guard.dart';

/// Gemini bağlantısı.
///
/// Doğrudan API anahtarı **kullanılmaz**. Firebase AI Logic + App Check
/// üzerinden gider; istekleri yalnız doğrulanmış uygulama yapabilir.
abstract class GeminiClient {
  Future<GeminiExplanation> explain({
    required String figures,
    required String localDecisionSummary,
    int maxOutputTokens = 256,
  });

  Future<String> proposeRulePatchJson({
    required String currentRulesJson,
    required String instruction,
  });
}

class GeminiExplanation {
  const GeminiExplanation({
    required this.text,
    required this.promptTokens,
    required this.candidatesTokens,
  });

  final String text;
  final int promptTokens;
  final int candidatesTokens;

  int get totalTokens => promptTokens + candidatesTokens;
}

class FirebaseAiGeminiClient implements GeminiClient {
  FirebaseAiGeminiClient({this.modelName = AppConstants.geminiModel});

  final String modelName;

  GenerativeModel get _model {
    final ai = FirebaseAI.googleAI(useLimitedUseAppCheckTokens: true);
    return ai.generativeModel(model: modelName);
  }

  @override
  Future<GeminiExplanation> explain({
    required String figures,
    required String localDecisionSummary,
    int maxOutputTokens = 256,
  }) async {
    final safeFigures = PrivacyGuard.mask(figures);
    final safeDecision = PrivacyGuard.mask(localDecisionSummary);
    final response = await _model.generateContent(
      [
        Content.text(
          'You explain a local rule-engine decision. '
          'Do not invent a new decision. Keep the answer short.\n'
          'Device figures:\n$safeFigures\n'
          'Local decision: $safeDecision',
        ),
      ],
      generationConfig: GenerationConfig(maxOutputTokens: maxOutputTokens),
    );
    final usage = response.usageMetadata;
    return GeminiExplanation(
      text: response.text?.trim().isNotEmpty == true
          ? response.text!.trim()
          : 'Açıklama üretilemedi.',
      promptTokens: usage?.promptTokenCount ?? 0,
      candidatesTokens: usage?.candidatesTokenCount ?? 0,
    );
  }

  @override
  Future<String> proposeRulePatchJson({
    required String currentRulesJson,
    required String instruction,
  }) async {
    final response = await _model.generateContent([
      Content.text(
        'Return ONLY a JSON object that conforms to HybridAssistantRulePack. '
        'No markdown. No executable code. No scripts. Data only.\n'
        'Instruction: ${PrivacyGuard.mask(instruction)}\n'
        'Current rules JSON:\n${PrivacyGuard.mask(currentRulesJson)}',
      ),
    ]);
    return response.text?.trim() ?? '';
  }
}

/// Firebase yapılandırılmadan iskelet / test için.
class StubGeminiClient implements GeminiClient {
  @override
  Future<GeminiExplanation> explain({
    required String figures,
    required String localDecisionSummary,
    int maxOutputTokens = 256,
  }) async {
    return GeminiExplanation(
      text:
          '[stub] Yerel karar: ${PrivacyGuard.mask(localDecisionSummary)}. '
          'Ölçüm:\n${PrivacyGuard.mask(figures)}',
      promptTokens: 0,
      candidatesTokens: 0,
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
