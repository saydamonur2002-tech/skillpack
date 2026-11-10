import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../../data/repositories/assistant_repository.dart';
import '../../domain/services/token_budget_service.dart';
import '../widgets/app_check_debug_token_banner.dart';
import '../widgets/status_card.dart';

/// Tek işlevli minimalist ana ekran (durum, giriş, sonuç/log).
class HomeScreen extends StatefulWidget {
  const HomeScreen({
    super.key,
    required this.repository,
    required this.tokenBudgetService,
    this.appCheckDebugToken,
  });

  final AssistantRepository repository;
  final TokenBudgetService tokenBudgetService;

  /// Debug derlemede Firebase konsoluna eklenecek App Check anahtarı.
  final String? appCheckDebugToken;

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _controller = TextEditingController();
  final _logs = <String>[];
  AssistantResult? _result;
  EngineStatus _status = EngineStatus.localActive;
  bool _busy = false;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _log(String line) {
    setState(() {
      _logs.insert(0, '${TimeOfDay.now().format(context)}  $line');
      if (_logs.length > 40) _logs.removeLast();
    });
  }

  Future<void> _submit() async {
    final query = _controller.text.trim();
    if (query.isEmpty || _busy) return;
    setState(() => _busy = true);
    _log('sorgu: $query');
    try {
      final result = await widget.repository.handle(query: query);
      if (!mounted) return;

      if (result.needsTokenBudgetPrompt) {
        _log('günlük token maliyeti kullanıcıya soruluyor');
        final approved = await _askDailyTokenBudget(result.budgetDecision);
        if (!mounted) return;
        if (approved == true &&
            result.pendingQuery != null &&
            result.pendingLocalSummary != null) {
          final continued = await widget.repository.continueCloudExplain(
            query: result.pendingQuery!,
            localMessage: result.pendingLocalSummary!,
            ruleId: result.ruleId,
          );
          setState(() {
            _result = continued;
            _status = continued.engineStatus;
          });
          _log('kaynak: ${continued.source.name}');
          return;
        }
        setState(() {
          _result = AssistantResult(
            source: AssistantSource.localRule,
            title: 'Yerel kural (bulut atlandı)',
            body: result.pendingLocalSummary ?? result.body,
            ruleId: result.ruleId,
            engineStatus: EngineStatus.localActive,
          );
          _status = EngineStatus.localActive;
        });
        _log('bulut atlandı — yalnız yerel');
        return;
      }

      setState(() {
        _result = result;
        _status = result.engineStatus;
      });
      _log('kaynak: ${result.source.name}');
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  Future<bool?> _askDailyTokenBudget(TokenBudgetDecision? decision) {
    final suggested = widget.tokenBudgetService.dailyLimit ?? 2000;
    final controller = TextEditingController(text: '$suggested');

    return showModalBottomSheet<bool>(
      context: context,
      isScrollControlled: true,
      backgroundColor: const Color(0xFF1A2220),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
      ),
      builder: (context) {
        return Padding(
          padding: EdgeInsets.only(
            left: 24,
            right: 24,
            top: 24,
            bottom: MediaQuery.viewInsetsOf(context).bottom + 24,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                'Günlük bulut token limiti',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: const Color(0xFFE7F0EC),
                      fontWeight: FontWeight.w600,
                    ),
              ),
              const SizedBox(height: 8),
              Text(
                decision?.reason ??
                    'Bulut açıklaması token harcar. Günlük üst sınırı siz seçin.',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: const Color(0xFFB5C4BE),
                    ),
              ),
              if (decision != null) ...[
                const SizedBox(height: 12),
                Text(
                  'Bugün kullanılan: ${decision.usedToday}'
                  '${decision.dailyLimit != null ? ' / ${decision.dailyLimit}' : ''}'
                  '\nBu istek tahmini: ${decision.estimatedTokens} token',
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: const Color(0xFF8FA39A),
                      ),
                ),
              ],
              const SizedBox(height: 16),
              TextField(
                controller: controller,
                keyboardType: TextInputType.number,
                style: const TextStyle(color: Color(0xFFE7F0EC)),
                decoration: const InputDecoration(
                  labelText: 'Günlük max token',
                  labelStyle: TextStyle(color: Color(0xFF8FA39A)),
                  enabledBorder: UnderlineInputBorder(
                    borderSide: BorderSide(color: Color(0xFF3A4A44)),
                  ),
                ),
              ),
              const SizedBox(height: 20),
              Row(
                children: [
                  TextButton(
                    onPressed: () => Navigator.pop(context, false),
                    child: const Text('Yalnız yerel'),
                  ),
                  const Spacer(),
                  FilledButton(
                    onPressed: () async {
                      final value = int.tryParse(controller.text.trim());
                      if (value == null || value < 0) return;
                      await widget.tokenBudgetService
                          .setDailyLimitFromUser(value);
                      if (context.mounted) Navigator.pop(context, true);
                    },
                    child: const Text('Kaydet ve devam'),
                  ),
                ],
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color(0xFF0E1714),
              Color(0xFF1C2B26),
              Color(0xFF243830),
            ],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  'skillpack',
                  style: theme.textTheme.headlineMedium?.copyWith(
                    color: const Color(0xFFD5E8DE),
                    fontWeight: FontWeight.w700,
                    letterSpacing: -0.5,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  'Karar yerelde. Açıklama — siz onaylarsanız — bulutta.',
                  style: theme.textTheme.bodyMedium?.copyWith(
                    color: const Color(0xFF9BB0A6),
                  ),
                ),
                const SizedBox(height: 16),
                StatusCard(
                  status: _status,
                  firebaseReady: widget.repository.firebaseReady,
                ),
                if (kDebugMode && widget.appCheckDebugToken != null) ...[
                  const SizedBox(height: 12),
                  AppCheckDebugTokenBanner(token: widget.appCheckDebugToken!),
                ],
                const SizedBox(height: 20),
                TextField(
                  controller: _controller,
                  style: const TextStyle(color: Color(0xFFE7F0EC)),
                  cursorColor: const Color(0xFF7CB89A),
                  textInputAction: TextInputAction.send,
                  onSubmitted: (_) => _submit(),
                  decoration: InputDecoration(
                    hintText: 'Bir soru yazın…',
                    hintStyle: const TextStyle(color: Color(0xFF6E8178)),
                    filled: true,
                    fillColor: const Color(0x33203028),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                    suffixIcon: IconButton(
                      onPressed: _busy ? null : _submit,
                      icon: _busy
                          ? const SizedBox(
                              width: 18,
                              height: 18,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : const Icon(Icons.arrow_upward_rounded),
                      color: const Color(0xFF7CB89A),
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                if (_result != null) ...[
                  Text(
                    _result!.title,
                    style: theme.textTheme.titleMedium?.copyWith(
                      color: const Color(0xFFC5DDD0),
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    _result!.body,
                    style: theme.textTheme.bodyLarge?.copyWith(
                      color: const Color(0xFFDDE8E2),
                      height: 1.45,
                    ),
                  ),
                  if (_result!.tokensUsed != null) ...[
                    const SizedBox(height: 8),
                    Text(
                      'Bu yanıt ≈ ${_result!.tokensUsed} token',
                      style: theme.textTheme.labelSmall?.copyWith(
                        color: const Color(0xFF7A9086),
                      ),
                    ),
                  ],
                  const SizedBox(height: 20),
                ],
                Text(
                  'Loglar',
                  style: theme.textTheme.labelLarge?.copyWith(
                    color: const Color(0xFF8FA39A),
                  ),
                ),
                const SizedBox(height: 8),
                Expanded(
                  child: ListView.builder(
                    itemCount: _logs.length,
                    itemBuilder: (context, index) {
                      return Padding(
                        padding: const EdgeInsets.only(bottom: 4),
                        child: Text(
                          _logs[index],
                          style: theme.textTheme.bodySmall?.copyWith(
                            color: const Color(0xFF6E8178),
                            fontFamily: 'monospace',
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
