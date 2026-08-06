# DataVision 发布说明

## 1.0.0（初始定制版）

基于 TV Bro 源码定制为数据大屏 Kiosk 应用：

* 品牌化：应用更名为 DataVision，更换图标与包名（im.xcode.datavision）
* Kiosk 模式：启动即全屏展示配置的大屏页面，隐藏全部浏览器 UI；未配置地址时自动引导设置
* 长按 BACK/MENU 键退出 Kiosk，直接进入设置界面（可修改大屏地址）
* 启动时自动恢复最后一次访问的页面；设置中修改大屏地址后下次启动生效
* 断网自愈：加载失败按 5s/10s/30s 指数退避自动重试，网络恢复立即重载
* 可选定时自动刷新（分钟级配置）
* 4K 显示优化：GeckoView 渲染密度强制为 1.0，消除电视 DPI 放大导致的视口缩放
* 内置自动升级：检查 GitHub Release 版本清单，弹窗提示并下载对应架构 APK 安装
* 大屏域名自动豁免广告拦截
* 内置主页移除 TV Bro logo 与常用网址快捷入口
* Kiosk 相关界面文案中文本地化
* Release 构建支持 ABI 拆分（-PenableAbiSplits），单架构包 143~196 MB
