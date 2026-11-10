/// Buluta ve kayıtlara gitmeden önce düz metni maskeler.
///
/// Asıl koruma: açıklama isteğinde kullanıcı cümlesi değil, yalnız sayılar gider.
/// Bu süzgeç regex tabanlıdır ve kusursuz değildir.
class PrivacyGuard {
  const PrivacyGuard._();

  static const allowedFigureKeys = {
    'batteryLevel',
    'batteryTempC',
    'thermalStatus',
    'isCharging',
    'pluggedType',
    'isPowerSaveMode',
    'isMetered',
  };

  static const pluggedCodes = {'none', 'ac', 'usb', 'wireless', 'dock'};

  static String mask(String input) {
    var text = input;
    text = text.replaceAllMapped(_iban, (m) {
      final compact = m.group(0)!.replaceAll(RegExp(r'\s+'), '');
      if (!_ibanChecksumOk(compact)) return m.group(0)!;
      return '[iban]';
    });
    text = text.replaceAll(_email, '[e-posta]');
    text = text.replaceAllMapped(_phone, (m) {
      final digits = m.group(0)!.replaceAll(RegExp(r'\D'), '');
      if (digits.length < 10 || digits.length > 13) return m.group(0)!;
      return '[telefon]';
    });
    text = text.replaceAllMapped(_elevenDigits, (m) {
      if (!_tcOk(m.group(0)!)) return m.group(0)!;
      return '[tc-no]';
    });
    text = text.replaceAll(_plate, '[plaka]');
    return text;
  }

  static String figuresText(Map<String, Object> figures) {
    return figures.entries.map((e) => '${e.key}: ${e.value}').join('\n');
  }

  static bool figuresAreSafe(Map<String, Object> figures) {
    if (figures.keys.any((key) => !allowedFigureKeys.contains(key))) {
      return false;
    }
    for (final value in figures.values) {
      if (value is num || value is bool) continue;
      if (value is String && pluggedCodes.contains(value)) continue;
      return false;
    }
    return true;
  }

  static final _email = RegExp(
    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
  );

  static final _phone = RegExp(
    r'(?:\+90|0)[\s-]*5\d{2}(?:[\s-]*\d){7}',
  );

  static final _elevenDigits = RegExp(r'(?<!\d)\d{11}(?!\d)');

  static final _iban = RegExp(
    r'TR(?:\s*\d){24}',
    caseSensitive: false,
  );

  static final _plate = RegExp(
    r'(?<!\d)(0[1-9]|[1-7][0-9]|8[01])\s*[A-Za-zÇĞİÖŞÜçğıöşü]{1,3}\s*\d{2,4}(?!\d)',
  );

  static bool _tcOk(String digits) {
    if (digits.length != 11 || digits.startsWith('0')) return false;
    final d = digits.codeUnits.map((c) => c - 48).toList();
    if (d.any((n) => n < 0 || n > 9)) return false;
    final odd = d[0] + d[2] + d[4] + d[6] + d[8];
    final even = d[1] + d[3] + d[5] + d[7];
    final tenth = ((odd * 7) - even) % 10;
    final tenthNorm = tenth < 0 ? tenth + 10 : tenth;
    if (d[9] != tenthNorm) return false;
    final eleventh = d.take(10).reduce((a, b) => a + b) % 10;
    return d[10] == eleventh;
  }

  static bool _ibanChecksumOk(String compact) {
    if (!RegExp(r'^TR\d{24}$', caseSensitive: false).hasMatch(compact)) {
      return false;
    }
    final upper = compact.toUpperCase();
    final rearranged = upper.substring(4) + upper.substring(0, 4);
    final expanded = StringBuffer();
    for (final code in rearranged.codeUnits) {
      if (code >= 48 && code <= 57) {
        expanded.writeCharCode(code);
      } else {
        expanded.write(code - 55);
      }
    }
    var remainder = 0;
    for (final code in expanded.toString().codeUnits) {
      remainder = (remainder * 10 + (code - 48)) % 97;
    }
    return remainder == 1;
  }
}
