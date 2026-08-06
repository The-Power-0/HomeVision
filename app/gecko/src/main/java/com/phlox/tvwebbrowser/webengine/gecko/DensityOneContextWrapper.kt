package com.phlox.tvwebbrowser.webengine.gecko

import android.content.Context
import android.content.ContextWrapper
import android.content.res.Resources
import android.util.DisplayMetrics

/**
 * DataVision: TV displays usually report a density > 1 (e.g. 1.5 at 240dpi), which makes
 * GeckoView shrink the web viewport to physicalPixels / density and then upscale the
 * rendering, squeezing and blurring desktop-style dashboard layouts.
 *
 * GeckoView derives the viewport density from its context resources, so wrapping the
 * GeckoView context with density 1.0 forces a 1:1 physical-pixels viewport
 * (devicePixelRatio = 1), like a desktop browser. The app UI itself keeps the real
 * density because only the GeckoView is created with this wrapper.
 */
class DensityOneContextWrapper(base: Context) : ContextWrapper(base) {

    private val densityOneResources: Resources by lazy {
        val metrics = DisplayMetrics()
        metrics.setTo(base.resources.displayMetrics)
        metrics.density = 1.0f
        metrics.scaledDensity = 1.0f
        metrics.densityDpi = DisplayMetrics.DENSITY_DEFAULT
        @Suppress("DEPRECATION")
        Resources(base.assets, metrics, base.resources.configuration)
    }

    override fun getResources(): Resources = densityOneResources
}
