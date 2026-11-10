import 'dart:math';

import 'package:flutter_test/flutter_test.dart';
import 'package:hybrid_assistant/core/firebase/app_check_debug_token.dart';

void main() {
  test('debug token UUID v4 biçimindedir ve aynı tohumla sabittir', () {
    final first = createAppCheckDebugToken(random: Random(7));
    final second = createAppCheckDebugToken(random: Random(7));

    expect(first, second);
    expect(appCheckDebugTokenPattern.hasMatch(first), isTrue);
    expect(
      createAppCheckDebugToken(random: Random(8)),
      isNot(first),
    );
  });
}
