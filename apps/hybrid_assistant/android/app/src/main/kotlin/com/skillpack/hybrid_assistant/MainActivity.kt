package com.skillpack.hybrid_assistant

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine

class MainActivity : FlutterActivity() {
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        SystemMonitorPlugin.register(this, flutterEngine.dartExecutor.binaryMessenger)
    }
}
