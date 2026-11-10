import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:hybrid_assistant/features/hybrid_assistant/presentation/widgets/app_check_debug_token_banner.dart';

void main() {
  testWidgets('debug anahtarını ve kopyala düğmesini gösterir', (tester) async {
    const token = '123a4567-b89c-42d3-a456-789012345678';

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: AppCheckDebugTokenBanner(token: token),
        ),
      ),
    );

    expect(find.text('App Check debug anahtarı'), findsOneWidget);
    expect(find.text(token), findsOneWidget);
    expect(find.text('Kopyala'), findsOneWidget);
  });
}
