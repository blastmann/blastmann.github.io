title: WebViewJavascriptBridge For WinRT
permalink: webviewjavascriptbridge-for-winrt
date: 2014-12-06 20:37:51
tags: [winrt,webview,js]
---

直奔主题，之前说了[如何在WinRT 8.1下面通过`ScriptNotify`接收页面JS对Native Code发送的消息](/post/a-solution-for-any-hosts-to-notify-winrt-81-webview.html)。虽然示例工程也说得比较清楚，但是没有封装成一个类似iOS/OSX下面的[WebViewJavscriptBridge](https://github.com/marcuswestin/WebViewJavascriptBridge)插件。于是这两天闲来无事，将其封装成Runtime Component。Repo：[WebViewJavascriptBridgeRT](https://github.com/blastmann/WebViewJavascriptBridgeRT)。

整个Bridge跟iOS下面的封装几乎一样，主体JS也是从那边拿过来改了适配了一下就用了。整体流程在示例App里面写得比较清楚，就不重复写了。主要流程就是：新建桥接->注册回调接口->对页面发送消息或调用注册接口。

不同于ObjC，在解析JS回传的JSON时，由于不建议使用`dynamic`，因此暂时建议在回传的时候统一对结果进行`stringify`处理，获取到结果的字符串后再自行解析成所需对象。JSON解析引用了JSON.Net，速度还是挺不错的。

暂时发现在WebView里面回调本地代码似乎有点性能问题，后面需要再跟进一下。然后再研究一下回传结果的解析函数能否使用泛型重写，这样似乎能更方便地处理回传结果的解析问题，避免上面的限制。