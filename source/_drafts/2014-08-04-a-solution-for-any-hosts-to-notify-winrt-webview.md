title: 让WinRT 8.1 Webview支持任意站点下的JS通知
permalink: a-solution-for-any-hosts-to-notify-winrt-8.1-webview
tags: [winrt,webview]
---

WinRT 8.1下，微软增强了Webview控件的大部分功能，同时也废弃了几个允许脚本通知（ScriptNotify)的属性。关于ScriptNotify，在8.1的帮助文档里面有这么一段注释：

> To enable an external web page to fire the ScriptNotify event when calling window.external.notify, you must include the page's URI in the ApplicationContentUriRules section of the app manifest. (You can do this in Visual Studio on the Content URIs tab of the Package.appxmanifest designer.) The URIs in this list must use HTTPS and may contain subdomain wildcards (for example, "https://*.microsoft.com"), but they can't contain domain wildcards (for example, "https://*.com" and "https://*.*"). The manifest requirement does not apply to content that originates from the app package, uses an ms-local-stream:// URI, or is loaded using NavigateToString.
Note  If you have more then one subdomain, you must use one wildcard for each subdomain. For example, "https://*.microsoft.com" matches with "https://any.microsoft.com" but not with "https://this.any.microsoft.com."
These changes do not affect apps compiled for Windows 8, even when running on Windows 8.1.

> AllowedScriptNotifyUris, AnyScriptNotifyUri, and AllowedScriptNotifyUrisProperty are not supported in apps compiled for Windows 8.1.

也就是说，只有在应用开发过程中，开发者主动添加在`Package.appxmanifest`中的，并且只能是HTTPS下的Uri才可以进行脚本通知。
