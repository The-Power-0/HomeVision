package com.phlox.tvwebbrowser.webengine.gecko.delegates

import android.util.Log
import com.phlox.tvwebbrowser.webengine.gecko.GeckoWebEngine
import org.json.JSONObject
import org.mozilla.geckoview.WebExtension

class AppWebExtensionBackgroundPortDelegate(val port: WebExtension.Port, val webEngine: GeckoWebEngine): WebExtension.PortDelegate {
    override fun onPortMessage(message: Any, port: WebExtension.Port) {
        //Log.d(TAG, "onPortMessage: $message")
        try {
            val msgJson = message as JSONObject
            when (msgJson.getString("action")) {
                "onBeforeRequest" -> {
                    Log.i(TAG, "onBeforeRequest: " + msgJson.toString())
                    val data = msgJson.getJSONObject("details")
                    val requestId = data.getInt("requestId")
                    val msg = JSONObject()
                    msg.put("action", "onResolveRequest")
                    // No content filtering: allow each request and still reply.
                    msg.put("data", JSONObject().put("requestId", requestId).put("block", false))
                    port.postMessage(msg)
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    override fun onDisconnect(port: WebExtension.Port) {
        Log.d(TAG, "onDisconnect")
        webEngine.appHomeContentScriptPortDelegate = null
    }

    companion object {
        val TAG: String = AppWebExtensionBackgroundPortDelegate::class.java.simpleName
    }
}