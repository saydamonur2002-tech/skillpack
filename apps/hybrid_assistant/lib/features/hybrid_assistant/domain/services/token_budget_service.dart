import '../../../../core/constants.dart';
import '../../../../core/storage/local_storage.dart';

/// Günlük bulut token bütçesi — maliyeti kullanıcıya sorar (`ask_user`).
class TokenBudgetService {
  TokenBudgetService({required LocalStorage storage}) : _storage = storage;

  final LocalStorage _storage;

  int? _dailyLimit;
  int _usedToday = 0;
  String _dayStamp = '';
  bool _consentGiven = false;

  int? get dailyLimit => _dailyLimit;
  int get usedToday => _usedToday;
  bool get hasUserChosenLimit => _consentGiven && _dailyLimit != null;

  Future<void> load() async {
    final prefs = await _storage.prefs();
    _dayStamp = _todayStamp();
    final storedDay = prefs.getString(AppConstants.prefsDayStamp) ?? '';
    if (storedDay != _dayStamp) {
      _usedToday = 0;
      await prefs.setInt(AppConstants.prefsUsedToday, 0);
      await prefs.setString(AppConstants.prefsDayStamp, _dayStamp);
    } else {
      _usedToday = prefs.getInt(AppConstants.prefsUsedToday) ?? 0;
    }
    if (prefs.containsKey(AppConstants.prefsDailyLimit)) {
      _dailyLimit = prefs.getInt(AppConstants.prefsDailyLimit);
    }
    _consentGiven = prefs.getBool(AppConstants.prefsConsent) ?? false;
  }

  Future<void> setDailyLimitFromUser(int limit) async {
    if (limit < 0) {
      throw ArgumentError('Günlük token limiti negatif olamaz.');
    }
    final prefs = await _storage.prefs();
    _dailyLimit = limit;
    _consentGiven = true;
    await prefs.setInt(AppConstants.prefsDailyLimit, limit);
    await prefs.setBool(AppConstants.prefsConsent, true);
  }

  TokenBudgetDecision evaluate({required int estimatedTokens}) {
    if (!_consentGiven || _dailyLimit == null) {
      return TokenBudgetDecision.askUser(
        reason: 'Günlük bulut token limiti henüz seçilmedi.',
        usedToday: _usedToday,
        dailyLimit: _dailyLimit,
        estimatedTokens: estimatedTokens,
      );
    }

    if (_usedToday + estimatedTokens > _dailyLimit!) {
      return TokenBudgetDecision.askUser(
        reason: 'Günlük token kotası aşılacak. Devam için onay gerekli.',
        usedToday: _usedToday,
        dailyLimit: _dailyLimit,
        estimatedTokens: estimatedTokens,
      );
    }

    return TokenBudgetDecision.allow(
      usedToday: _usedToday,
      dailyLimit: _dailyLimit!,
      estimatedTokens: estimatedTokens,
    );
  }

  Future<void> recordUsage(int tokens) async {
    if (tokens <= 0) return;
    await load();
    _usedToday += tokens;
    final prefs = await _storage.prefs();
    await prefs.setInt(AppConstants.prefsUsedToday, _usedToday);
    await prefs.setString(AppConstants.prefsDayStamp, _dayStamp);
  }

  String _todayStamp() {
    final now = DateTime.now().toUtc();
    return '${now.year}-${now.month.toString().padLeft(2, '0')}-${now.day.toString().padLeft(2, '0')}';
  }
}

enum TokenBudgetOutcome { allow, askUser }

class TokenBudgetDecision {
  const TokenBudgetDecision._({
    required this.outcome,
    required this.reason,
    this.usedToday = 0,
    this.dailyLimit,
    this.estimatedTokens = 0,
  });

  const TokenBudgetDecision.allow({
    required int usedToday,
    required int dailyLimit,
    required int estimatedTokens,
  }) : this._(
          outcome: TokenBudgetOutcome.allow,
          reason: 'Bütçe uygun.',
          usedToday: usedToday,
          dailyLimit: dailyLimit,
          estimatedTokens: estimatedTokens,
        );

  const TokenBudgetDecision.askUser({
    required String reason,
    required int usedToday,
    required int? dailyLimit,
    required int estimatedTokens,
  }) : this._(
          outcome: TokenBudgetOutcome.askUser,
          reason: reason,
          usedToday: usedToday,
          dailyLimit: dailyLimit,
          estimatedTokens: estimatedTokens,
        );

  final TokenBudgetOutcome outcome;
  final String reason;
  final int usedToday;
  final int? dailyLimit;
  final int estimatedTokens;

  bool get needsUserPrompt => outcome == TokenBudgetOutcome.askUser;
}
