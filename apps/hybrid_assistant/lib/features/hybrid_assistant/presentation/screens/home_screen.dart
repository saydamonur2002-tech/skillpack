import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../../data/datasources/system_probe.dart';
import '../../data/repositories/assistant_repository.dart';
import '../../domain/models/device_snapshot.dart';
import '../../domain/services/privacy_guard.dart';
import '../../domain/services/token_budget_service.dart';
import '../widgets/app_check_debug_token_banner.dart';
import '../widgets/device_panels.dart';
import '../widgets/status_card.dart';

/// Tek işlevli minimalist ana ekran (durum, giriş, sonuç/log).
class HomeScreen extends StatefulWidget {
  const HomeScreen({
    super.key,
    required this.repository,
    required this.tokenBudgetService,
    required this.probe,
    this.appCheckDebugToken,
  });

  final AssistantRepository repository;
  final TokenBudgetService tokenBudgetService;
  final SystemProbe probe;

  /// Debug derlemede Firebase konsoluna eklenecek App Check anahtarı.
  final String? appCheckDebugToken;

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> with WidgetsBindingObserver {
  final _controller = TextEditingController();
  final _logs = <String>[];
  AssistantResult? _result;
  EngineStatus _status = EngineStatus.localActive;
  DeviceSnapshot _snapshot = DeviceSnapshot.empty;
  StreamSubscription<DeviceSnapshot>? _snapshots;
  bool _busy = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _snapshots = widget.probe.snapshots.listen((snapshot) {
      if (mounted) setState(() => _snapshot = snapshot);
    });
    widget.probe.start();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      widget.probe.start();
    } else if (state == AppLifecycleState.paused ||
        state == AppLifecycleState.detached) {
      widget.probe.stop();
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _snapshots?.cancel();
    widget.probe.stop();
    _controller.dispose();
    super.dispose();
  }

  void _logResult(AssistantResult result) {
    if (result.ruleId != null) {
      _log('kural: ${result.ruleId}');
    }
    final throttle = result.throttleReason;
    if (throttle != null && throttle.isNotEmpty) {
      _log('kısıt: $throttle');
    }
    _log('kaynak: ${result.source.name}');
    if (result.source == AssistantSource.offlineFallback ||
        result.ruleId == 'unknown') {
      _log('yedek: ${result.title}');
    }
    final detail = result.errorDetail;
    if (detail != null && detail.isNotEmpty) {
      _log('yedek: $detail');
    }
  }

  Future<void> _refresh() async {
    setState(() => _busy = true);
    try {
      final snapshot = await widget.probe.read();
      if (!mounted) return;
      final result = await widget.repository.reevaluateLocal();
      setState(() {
        _snapshot = snapshot;
        _result = result;
        _status = result.engineStatus;
      });
      _log('yenile');
      _logResult(result);
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  Future<void> _openSettings(String target) async {
    final opened = await widget.probe.openSettings(target);
    if (!mounted) return;
    if (!opened) {
      _log('yedek: bu telefonda bu sayfa yok');
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Bu telefonda bu sayfa yok')),
      );
    }
  }

  void _log(String line) {
    final safe = PrivacyGuard.mask(line);
    setState(() {
      _logs.insert(0, '${TimeOfDay.now().format(context)}  $safe');
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
          _logResult(continued);
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
      _logResult(result);
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  Future<bool?> _askDailyTokenBudget(TokenBudgetDecision? decision) {
    final suggested = widget.tokenBudgetService.dailyLimit ?? 2000;
    final controller = TextEditingController(text: '$suggested');

    final sheetTheme = Theme.of(context);
    return showModalBottomSheet<bool>(
      context: context,
      isScrollControlled: true,
      backgroundColor: sheetTheme.colorScheme.surface,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
      ),
      builder: (context) {
        final theme = Theme.of(context);
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
                style: theme.textTheme.titleLarge?.copyWith(
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                decision?.reason ??
                    'Bulut açıklaması token harcar. Günlük üst sınırı siz seçin.',
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: theme.colorScheme.onSurfaceVariant,
                ),
              ),
              if (decision != null) ...[
                const SizedBox(height: 12),
                Text(
                  'Bugün kullanılan: ${decision.usedToday}'
                  '${decision.dailyLimit != null ? ' / ${decision.dailyLimit}' : ''}'
                  '\nBu istek tahmini: ${decision.estimatedTokens} token',
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: theme.colorScheme.onSurfaceVariant,
                  ),
                ),
              ],
              const SizedBox(height: 16),
              TextField(
                controller: controller,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Günlük max token',
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
    final scheme = theme.colorScheme;
    final page = <Widget>[
      Text(
        'skillpack',
        style: theme.textTheme.headlineMedium?.copyWith(
          fontWeight: FontWeight.w700,
          letterSpacing: -0.5,
        ),
      ),
      const SizedBox(height: 6),
      Text(
        'Karar yerelde. Açıklama — siz onaylarsanız — bulutta.',
        style: theme.textTheme.bodyMedium?.copyWith(
          color: scheme.onSurfaceVariant,
        ),
      ),
      const SizedBox(height: 16),
      DeviceLiveCards(snapshot: _snapshot),
      const SizedBox(height: 12),
      SystemHealthPanel(snapshot: _snapshot),
      const SizedBox(height: 12),
      StatusCard(
        status: _status,
        firebaseReady: widget.repository.firebaseReady,
        cloudError: _result?.errorDetail != null,
        freeBytes: _snapshot.availableBytes,
        totalBytes: _snapshot.totalBytes,
      ),
      if (_result?.throttleReason != null) ...[
        const SizedBox(height: 8),
        Text(
          _result!.throttleReason!,
          style: theme.textTheme.bodySmall?.copyWith(color: scheme.tertiary),
        ),
      ],
      if (_result != null && _result!.settings.isNotEmpty) ...[
        const SizedBox(height: 8),
        SettingsShortcutButtons(
          targets: _result!.settings,
          onOpen: _openSettings,
        ),
      ],
      Align(
        alignment: Alignment.centerLeft,
        child: TextButton(
          onPressed: _busy ? null : _refresh,
          child: const Text('Durumu yenile'),
        ),
      ),
      if (kDebugMode && widget.appCheckDebugToken != null) ...[
        const SizedBox(height: 12),
        AppCheckDebugTokenBanner(token: widget.appCheckDebugToken!),
      ],
      const SizedBox(height: 12),
      TextField(
        controller: _controller,
        scrollPadding: const EdgeInsets.only(bottom: 96),
        textInputAction: TextInputAction.send,
        onSubmitted: (_) => _submit(),
        decoration: InputDecoration(
          hintText: 'Bir soru yazın…',
          suffixIcon: IconButton(
            onPressed: _busy ? null : _submit,
            icon: _busy
                ? const SizedBox(
                    width: 18,
                    height: 18,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Icon(Icons.arrow_upward_rounded),
          ),
        ),
      ),
      const SizedBox(height: 20),
      if (_result != null) ...[
        Text(
          _result!.title,
          style: theme.textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          _result!.body,
          style: theme.textTheme.bodyLarge?.copyWith(height: 1.45),
        ),
        if (_result!.tokensUsed != null) ...[
          const SizedBox(height: 8),
          Text(
            'Bu yanıt ≈ ${_result!.tokensUsed} token',
            style: theme.textTheme.labelSmall?.copyWith(
              color: scheme.onSurfaceVariant,
            ),
          ),
        ],
        const SizedBox(height: 20),
      ],
      Text(
        'Loglar',
        style: theme.textTheme.labelLarge?.copyWith(
          color: scheme.onSurfaceVariant,
        ),
      ),
      const SizedBox(height: 8),
    ];

    return Scaffold(
      resizeToAvoidBottomInset: true,
      body: SafeArea(
        child: CustomScrollView(
          keyboardDismissBehavior: ScrollViewKeyboardDismissBehavior.onDrag,
          slivers: [
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(20, 16, 20, 0),
              sliver: SliverList(
                delegate: SliverChildListDelegate(page),
              ),
            ),
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(20, 0, 20, 24),
              sliver: SliverList(
                delegate: SliverChildBuilderDelegate(
                  (context, index) {
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 4),
                      child: Text(
                        _logs[index],
                        style: theme.textTheme.bodySmall?.copyWith(
                          color: scheme.onSurfaceVariant,
                          fontFamily: 'monospace',
                        ),
                      ),
                    );
                  },
                  childCount: _logs.length,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
