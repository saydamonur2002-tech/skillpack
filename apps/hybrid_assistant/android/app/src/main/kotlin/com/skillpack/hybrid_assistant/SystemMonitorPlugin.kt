package com.skillpack.hybrid_assistant

import android.app.ActivityManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.ConnectivityManager
import android.net.Network
import android.os.BatteryManager
import android.os.Build
import android.os.Environment
import android.os.Handler
import android.os.Looper
import android.os.PowerManager
import android.os.StatFs
import android.provider.Settings
import io.flutter.plugin.common.BinaryMessenger
import io.flutter.plugin.common.EventChannel
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel

/**
 * Uygulama dinlerken pil, ısı, bellek, depolama ve tarifeli ağı okur.
 * Zamanlayıcı yok. İşlemci sıcaklığı okunmaz.
 */
class SystemMonitorPlugin private constructor(
    private val context: Context,
) : EventChannel.StreamHandler, MethodChannel.MethodCallHandler {

    private val main = Handler(Looper.getMainLooper())
    private var sink: EventChannel.EventSink? = null
    private var batteryReceiver: BroadcastReceiver? = null
    private var powerReceiver: BroadcastReceiver? = null
    private var networkCallback: ConnectivityManager.NetworkCallback? = null
    private var thermalListener: PowerManager.OnThermalStatusChangedListener? = null

    override fun onListen(arguments: Any?, events: EventChannel.EventSink) {
        sink = events
        register()
        emit(sample())
    }

    override fun onCancel(arguments: Any?) {
        unregister()
        sink = null
    }

    override fun onMethodCall(call: MethodCall, result: MethodChannel.Result) {
        when (call.method) {
            "read" -> {
                val snap = sample()
                emit(snap)
                result.success(snap)
            }
            "openSettings" -> result.success(openSettings(call.argument("target")))
            else -> result.notImplemented()
        }
    }

    private fun register() {
        batteryReceiver = object : BroadcastReceiver() {
            override fun onReceive(c: Context?, intent: Intent?) {
                emit(sample())
            }
        }
        registerReceiver(batteryReceiver!!, IntentFilter(Intent.ACTION_BATTERY_CHANGED))

        powerReceiver = object : BroadcastReceiver() {
            override fun onReceive(c: Context?, intent: Intent?) {
                emit(sample())
            }
        }
        registerReceiver(
            powerReceiver!!,
            IntentFilter(PowerManager.ACTION_POWER_SAVE_MODE_CHANGED),
        )

        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val callback = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) = emit(sample())
            override fun onLost(network: Network) = emit(sample())
        }
        networkCallback = callback
        try {
            cm.registerDefaultNetworkCallback(callback)
        } catch (_: RuntimeException) {
            networkCallback = null
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val pm = context.getSystemService(Context.POWER_SERVICE) as PowerManager
            val listener = PowerManager.OnThermalStatusChangedListener { emit(sample()) }
            thermalListener = listener
            pm.addThermalStatusListener({ command -> main.post(command) }, listener)
        }
    }

    private fun unregister() {
        batteryReceiver?.let { runCatching { context.unregisterReceiver(it) } }
        powerReceiver?.let { runCatching { context.unregisterReceiver(it) } }
        batteryReceiver = null
        powerReceiver = null
        networkCallback?.let { callback ->
            val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
            runCatching { cm.unregisterNetworkCallback(callback) }
        }
        networkCallback = null
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            thermalListener?.let { listener ->
                val pm = context.getSystemService(Context.POWER_SERVICE) as PowerManager
                runCatching { pm.removeThermalStatusListener(listener) }
            }
        }
        thermalListener = null
    }

    private fun registerReceiver(receiver: BroadcastReceiver, filter: IntentFilter) {
        if (Build.VERSION.SDK_INT >= 33) {
            context.registerReceiver(receiver, filter, Context.RECEIVER_NOT_EXPORTED)
        } else {
            context.registerReceiver(receiver, filter)
        }
    }

    private fun emit(snapshot: Map<String, Any?>) {
        main.post { sink?.success(snapshot) }
    }

    private fun sample(): Map<String, Any?> {
        val battery = context.registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
        val level = battery?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
        val scale = battery?.getIntExtra(BatteryManager.EXTRA_SCALE, -1) ?: -1
        val percent = if (level >= 0 && scale > 0) (level * 100) / scale else null
        val status = battery?.getIntExtra(
            BatteryManager.EXTRA_STATUS,
            BatteryManager.BATTERY_STATUS_UNKNOWN,
        ) ?: BatteryManager.BATTERY_STATUS_UNKNOWN
        val plugged = battery?.getIntExtra(BatteryManager.EXTRA_PLUGGED, 0) ?: 0
        val tempRaw = if (battery?.hasExtra(BatteryManager.EXTRA_TEMPERATURE) == true) {
            battery.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0)
        } else {
            null
        }
        val health = battery?.getIntExtra(
            BatteryManager.EXTRA_HEALTH,
            BatteryManager.BATTERY_HEALTH_UNKNOWN,
        ) ?: BatteryManager.BATTERY_HEALTH_UNKNOWN
        val charging = status == BatteryManager.BATTERY_STATUS_CHARGING ||
            status == BatteryManager.BATTERY_STATUS_FULL

        val pm = context.getSystemService(Context.POWER_SERVICE) as PowerManager
        val thermalSupported = Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q
        val thermalStatus = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            pm.currentThermalStatus
        } else {
            null
        }
        val headroom = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            val value = pm.getThermalHeadroom(0)
            if (value.isNaN()) null else value.toDouble()
        } else {
            null
        }

        val am = context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
        val mem = ActivityManager.MemoryInfo()
        am.getMemoryInfo(mem)
        val stat = StatFs(Environment.getDataDirectory().path)
        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val metered = runCatching { cm.isActiveNetworkMetered }.getOrDefault(false)

        return mapOf(
            "batteryPercent" to percent,
            "isCharging" to charging,
            "pluggedType" to pluggedType(plugged),
            "batteryTempRaw" to tempRaw,
            "health" to healthName(health),
            "isPowerSaveMode" to pm.isPowerSaveMode,
            "thermalSupported" to thermalSupported,
            "thermalStatus" to thermalStatus,
            "thermalHeadroom" to headroom,
            "availMem" to mem.availMem,
            "totalMem" to mem.totalMem,
            "lowMemory" to mem.lowMemory,
            "availableBytes" to stat.availableBytes,
            "totalBytes" to stat.totalBytes,
            "isMetered" to metered,
        )
    }

    private fun pluggedType(plugged: Int): String {
        if (plugged and BatteryManager.BATTERY_PLUGGED_AC != 0) return "ac"
        if (plugged and BatteryManager.BATTERY_PLUGGED_USB != 0) return "usb"
        if (plugged and BatteryManager.BATTERY_PLUGGED_WIRELESS != 0) return "wireless"
        if (Build.VERSION.SDK_INT >= 33 &&
            plugged and BatteryManager.BATTERY_PLUGGED_DOCK != 0
        ) {
            return "dock"
        }
        if (plugged != 0) return "ac"
        return "none"
    }

    private fun healthName(health: Int): String = when (health) {
        BatteryManager.BATTERY_HEALTH_GOOD -> "good"
        BatteryManager.BATTERY_HEALTH_OVERHEAT -> "overheat"
        BatteryManager.BATTERY_HEALTH_DEAD -> "dead"
        BatteryManager.BATTERY_HEALTH_OVER_VOLTAGE -> "over_voltage"
        BatteryManager.BATTERY_HEALTH_UNSPECIFIED_FAILURE -> "unspecified_failure"
        BatteryManager.BATTERY_HEALTH_COLD -> "cold"
        else -> "unknown"
    }

    private fun openSettings(target: String?): Boolean {
        val actions = when (target) {
            "battery_saver" -> listOf(Settings.ACTION_BATTERY_SAVER_SETTINGS)
            "display" -> listOf(Settings.ACTION_DISPLAY_SETTINGS)
            "storage" -> listOf(
                "android.os.storage.action.MANAGE_STORAGE",
                Settings.ACTION_INTERNAL_STORAGE_SETTINGS,
            )
            else -> return false
        }
        for (action in actions) {
            try {
                context.startActivity(
                    Intent(action).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK),
                )
                return true
            } catch (_: android.content.ActivityNotFoundException) {
                continue
            }
        }
        return false
    }

    companion object {
        fun register(context: Context, messenger: BinaryMessenger) {
            val plugin = SystemMonitorPlugin(context.applicationContext)
            EventChannel(messenger, "com.skillpack.hybrid_assistant/system_events")
                .setStreamHandler(plugin)
            MethodChannel(messenger, "com.skillpack.hybrid_assistant/system_methods")
                .setMethodCallHandler(plugin)
        }
    }
}
