date: 2013-06-18 19:14
title: window.external.notify() 与 UglifyJS 压缩优化冲突
permalink: external-notify-cant-use-with-uglifyjs-compressor
tags: [webdev,wp8,javascript]
---

近期研究了一下 UglifyJs 对 JS 代码的压缩，发现 UglifyJS 压缩后，无法调用 `window.external.notify()` 方法，JS 代码如下：

    function MyNotify () {
        try{
            alert("Notify");
            window.external.notify("Notify");
        } catch (e){
            alert(e.message);
        }
    }

    function MyNotifyCompressed(){
        try {
            alert("Notify"), window.external.notify("Notify");
        } catch (e) {
            alert(e.message);
        }
    }

UglifyJS 在压缩 JS 代码时，压缩选项（-c)中有这么一个参数：

> sequences -- join consecutive simple statements using the comma operator

此选项默认是开启状态。当此选项处于开启状态时，UglifyJS 将会把多行代码压缩为一行并使用逗号进行分隔。压缩后，利用 `InvokeScript()` 调用 `MyNotifyCompressed()` 函数，系统将提示：

> Object doesn't support this action

`window.external.notify()` 方法无法正常使用，则在程序中的一些逻辑无法正常处理。到底为什么无法调用这个方法呢？暂时也不大明白，可能是作用域出现问题了。

如果使用逗号相连导致不能直接调用 `window.external.notify()` 的话，那还是把它单独封装成一个函数好了。