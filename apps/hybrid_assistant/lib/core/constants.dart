/// API endpoint'leri ve varsayılan ayarlar.
///
/// Gemini API anahtarı burada **yok**. Bulut erişimi Firebase AI Logic +
/// App Check üzerinden yapılır; anahtar sunucuda kalır.
class AppConstants {
  const AppConstants._();

  /// Firebase AI Logic model kimliği (anahtar değil).
  ///
  /// gemini-2.5-flash yeni projelerde kapanmış durumda; güncel kısa model.
  static const String geminiModel = 'gemini-3.5-flash-lite';

  /// Paketlenmiş temel kural seti (Skillpack).
  static const String defaultSkillsAsset = 'assets/configs/default_skills.json';

  /// Hot-patch şema dosyası.
  static const String rulesSchemaAsset = 'assets/configs/rules.schema.json';

  /// İmza doğrulama için public key (private key uygulamada olmaz).
  static const String rulesPublicKeyAsset = 'assets/keys/rules_public_key.pem';

  /// Yerel aktif / yedek kural dosya adları.
  static const String activeRulesFile = 'rules.active.json';
  static const String previousRulesFile = 'rules.prev.json';

  /// Açıklama çağrısı için kabaca token tahmini (kullanıcıya gösterilir).
  static const int estimatedExplainTokens = 400;

  /// Bütçe politikası: günlük token maliyetini kullanıcıya sor.
  static const String onExceedPolicy = 'ask_user';

  /// SharedPreferences anahtarları.
  static const String prefsAppCheckDebugToken = 'app_check_debug_token';
  static const String prefsDailyLimit = 'cloud_max_tokens_per_day';
  static const String prefsUsedToday = 'cloud_tokens_used_today';
  static const String prefsDayStamp = 'cloud_tokens_day';
  static const String prefsConsent = 'cloud_budget_consent_given';
}
