import 'package:firebase_ai/firebase_ai.dart';

import '../../../../core/constants.dart';

/// Gemini bağlantısı.
///
/// Doğrudan API anahtarı **kullanılmaz**. Firebase AI Logic + App Check
/// üzerinden gider; istekleri yalnız doğrulanmış uygulama yapabilir.
abstract class GeminiClient {
  Future<GeminiExplanation> explain({
    required String query,
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
    required String query,
    required String localDecisionSummary,
    int maxOutputTokens = 256,
  }) async {
    final response = await _model.generateContent(
      [
        Content.text(
          'You explain a local rule-engine decision. '
          'Do not invent a new decision. Keep the answer short.\n'
          'User query: $query\n'
          'Local decision: $localDecisionSummary',
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
        'Instruction: $instruction\n'
        'Current rules JSON:\n$currentRulesJson',
      ),
    ]);
    return response.text?.trim() ?? '';
  }
}

/// Firebase yapılandırılmadan iskelet / test için.
class StubGeminiClient implements GeminiClient {
  @override
  Future<GeminiExplanation> explain({
    required String query,
    required String localDecisionSummary,
    int maxOutputTokens = 256,
  }) async {
    return GeminiExplanation(
      text:
          '[stub] Yerel karar: $localDecisionSummary. Firebase AI Logic bağlanınca gerçek açıklama gelir.',
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
