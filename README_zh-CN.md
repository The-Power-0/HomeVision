# DataVision

**[English](README.md)**

基于 [TV Bro](https://github.com/truefedex/tv-bro) 开源源码深度定制的**安卓电视数据大屏 Kiosk 应用**，可将任意网页以全屏方式长期展示在安卓电视上，适用于数据看板、监控大屏等场景。

- 包名：`im.xcode.datavision`
- 版本：1.0.0
- 渲染引擎：GeckoView（内置，无需系统 WebView）
- 默认大屏地址：无（首次启动引导在设置中配置）

## 核心功能

### Kiosk 展示模式
- 启动即全屏展示配置的大屏页面，隐藏浏览器 UI（地址栏、菜单、标签页、虚拟光标菜单均不可见）
- 首次启动未配置地址时自动打开设置引导配置
- 首次启动（无历史记录）打开设置中的大屏地址；之后每次启动**自动恢复最后访问的页面**
- 在设置中修改大屏地址后，下次启动强制打开新地址（一次性生效，之后继续"记住最后页面"行为）
- 首次启动显示操作提示（长按 MENU/BACK 键退出）

### 断网自愈
- 页面加载失败自动重试：5 秒 → 10 秒 → 30 秒递增间隔，之后每 30 秒持续重试（重试当前页面地址）
- 检测到网络恢复后立即重新加载当前页面
- 支持可选的定时自动刷新（设置中的"自动重载间隔"，单位分钟，0 为关闭）

### 显示优化（4K 大屏）
- 针对电视高密度显示（如 240dpi）导致的视口缩放问题，通过 `DensityOneContextWrapper` 将 GeckoView 的渲染密度强制为 1.0，网页视口与物理像素 1:1 对应（等效 Chrome 100% 缩放效果），App 自身 UI 不受影响

### 内置自动升级
- 启动时检查本仓库 `latest_version.json` 清单（release 渠道），发现新版本后弹窗展示更新日志，确认后下载对应 CPU 架构的 APK 并引导安装
- APK 侧载安装时默认开启自动检查，可在设置 → 版本页关闭

### 其他定制
- 大屏页面所在域名自动豁免广告拦截，避免误伤数据组件
- 内置主页已移除 TV Bro logo 和常用网址快捷入口
- 中文界面（Kiosk 相关文案已本地化）
- 保持屏幕常亮（Kiosk 期间）

## 使用操作

| 操作 | 方式 |
|---|---|
| 退出 Kiosk 模式 | 长按遥控器 **BACK** 或 **MENU** 键（约 1 秒），直接进入设置界面 |
| 修改大屏地址 | 退出 Kiosk → 设置 → Kiosk 模式地址 → 保存 → 按提示重启 |
| 重新进入 Kiosk | 重启 App 后自动进入（无需手动操作） |
| 关闭电视屏保 | 需在电视系统设置中关闭，或 ADB：`adb shell settings put secure screensaver_enabled 0`（App 无权限阻止系统屏保） |

## 构建

环境：Android SDK + JDK（Gradle Wrapper 自动下载依赖）。

```powershell
# Release 构建 + ABI 拆分（推荐，产物与官方发布包体积一致）
.\gradlew.bat :app:assembleGenericGeckoIncludedRelease -PenableAbiSplits

# 签名（使用本机 debug 密钥，产物可直接安装）
powershell -ExecutionPolicy Bypass -File .\tools\sign_apks.ps1
```

产物位于 `app\build\outputs\apk\genericGeckoIncluded\release\`：

| 文件 | 架构 | 体积 |
|---|---|---|
| `app-generic-geckoIncluded-arm64-v8a-release.apk` | arm64（**电视常用**） | ~179 MB |
| `app-generic-geckoIncluded-armeabi-v7a-release.apk` | arm32 | ~143 MB |
| `app-generic-geckoIncluded-x86_64-release.apk` | x86_64（模拟器） | ~196 MB |

说明：
- 不传 `-PenableAbiSplits` 会打出包含全部架构的 universal 包（约 495 MB）
- `geckoExcluded` flavor 不含 GeckoView（约 3 MB），依赖系统 WebView，不支持本项目的 DPI 修复，一般不使用
- 正式分发建议使用正式签名密钥（在 `build.gradle.kts` 中配置 `KEYSTORE_PATH` 等环境变量）；**升级安装要求新旧 APK 签名一致**

## 发布与自动升级

仓库内置 GitHub Actions 发布流水线（`.github/workflows/release.yml`）：

1. 在 GitHub 仓库 Settings → Secrets 中配置 `KEYSTORE_BASE64`、`KEYSTORE_PASSWORD`、`KEY_ALIAS`、`KEY_PASSWORD`
2. Actions → Release → Run workflow，输入版本号（如 `1.1.0`）
3. 流水线自动构建、签名、创建 Release 并上传三个架构的 APK（文件名以 `-arm64-v8a.apk` 等结尾，供升级时按架构匹配）
4. 发版后修改仓库根目录 `latest_version.json`：`latestVersionCode`/`latestVersionName` 指向新版本，补充下载链接与 changelog，提交到 main 分支
5. 已安装的电视在下次启动时检测到新版本并提示升级

注意：`build.gradle.kts` 中的 `versionCode` 必须同步递增，否则升级检查不会触发。

## 定制涉及的关键文件

| 文件 | 作用 |
|---|---|
| `app\common\...\Config.kt` | Kiosk 配置项（模式开关、大屏地址、自动刷新间隔） |
| `app\...\activity\main\MainActivity.kt` | Kiosk 生命周期、按键退出、断网恢复、启动恢复逻辑 |
| `app\gecko\...\GeckoWebEngine.kt` | GeckoView 创建点应用密度包装 |
| `app\gecko\...\DensityOneContextWrapper.kt` | DPI 修复核心（density=1.0 的 Context 包装） |
| `app\gecko\...\delegates\MyNavigationDelegate.kt` | 加载失败自动重试（指数退避） |
| `app\...\dialogs\settings\MainSettingsView.kt` | Kiosk 设置界面 |
| `app\src\main\assets\pages\home\index.html` | 内置主页（已移除 logo 与常用网址） |
| `app\src\main\res\values-zh\strings.xml` | Kiosk 相关中文文案 |

## 辅助工具（`tools\` 目录）

| 脚本 | 用途 |
|---|---|
| `sign_apks.ps1` | 用本机 debug 密钥批量签名 release APK（自动探测 SDK 路径） |
| `list_apks.ps1` | 列出构建产物及体积 |
| `find_sdk.ps1` | 定位本机 Android SDK/build-tools 路径 |
| `verify_url_in_apk.ps1` | 验证指定字符串（如默认大屏 URL）是否已打入 APK |

## 许可与来源

本项目基于 TV Bro 源码修改。根据 TV Bro 的 [BSD 派生许可](LICENSE.md)：派生应用不得使用 "TV Bro" 名称、原图标与原 application id，且需在界面中注明来源。本应用已在关于页面标注 "Based on TV Bro sources" 并提供原项目链接。

- 原项目：https://github.com/truefedex/tv-bro
