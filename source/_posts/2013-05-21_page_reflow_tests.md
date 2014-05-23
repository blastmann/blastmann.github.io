date: 2013-05-21 09:24
title: 测定页面 Reflow 耗时的办法
permalink: page-reflow-tests
tags: [programming,reflow]
---

最近在查阅关于浏览器 Reflow 性能的资料，在《[影响 reflow 的因素及其优化](http://www.planabc.net/2009/04/13/reflow/)》中看到这么一个测试页面 Reflow 性能的脚本：

    var a=document.getElementById('text');
    a.innerHTML = "text";
    var t0 = new Date();
    a.offsetHeight;
    var t1 = new Date();
    alert(t1-t0);

原理：通常 `offsetHeight` 总是要等 Reflow 完成才能计算出来，所以脚本会被阻塞直到 Reflow 完成。

