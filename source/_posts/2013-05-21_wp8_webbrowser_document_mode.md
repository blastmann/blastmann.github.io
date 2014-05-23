date: 2013-05-21 10:39
title: 关于 WP8 中 WebBrowser 控件的文档模式
permalink: wp8-webbrowser-document-mode
tags: [webdev,wp8]
---

IE 有个很诡异的地方就是：如果 HTML 文档里面没有声明 `<!DOCTYPE>` 的话，将会触发其「[怪异模式][QuirksMode]」。同时，WP8 上的 `WebBrowser` 控件本身有个 Bug 就是当我们使用 `NavigateToString()` 时，如果 HTML 代码中对 `<!DOCTYPE>` 进行声明了话，那 `WebBrowser` 将不能渲染该 HTML 代码（[参考文章][WebBrowserBroken]）。

该参考文章给出的方法是利用独立存储来解决这个问题，代码如下：

    var client = new WebClient(); 
    var content = await client.DownloadStringTaskAsync(url);
    var store = IsolatedStorageFile.GetUserStoreForApplication();

    using (var writeFile = new StreamWriter(new IsolatedStorageFileStream("htmlcontent.html", FileMode.Create, FileAccess.Write, store))) 
    { 
        writeFile.Write(content); 
        writeFile.Close(); 
    }
     
    var uri = new Uri("htmlcontent.html", UriKind.Relative);
    WebBrowser.Navigate(uri);

PS：记得要给我们的 HTML 文档加上 `<!doctype html>` ，这样可以让 WebBrowser 运行在 IE10 的模式下面，对 HTML5 的支持最好，而且对 DOM 的操作速度也会快上不少。

**2013-05-20更新**：今天看到 StackOverflow 上关于这个问题的另外一个答案（[点击进入][wbencode]），`WebBrowser` 中 `NavigateToString()` 失效的根本原因应是 `String` 的编码问题。由于 `String` 类型的编码是 UTF-16，如果在 HTML 代码中插入 `<meta charset="UTF-8">` 的声明，`NavigateToString()` 将无法正确显示页面。

**2013-05-21相关资料**：

* [<Defining document compatibility>][doc-compat]，在此文档中有简介 IE 中关于文档模式的一些问题。特别指出 IE9 及以前的版本，浏览器处理 Quirks Mode 的时候页面功能的支持将相当于 IE5.5。
* [<Specifying legacy document modes>][legacy-doc-modes]，此文档主要是介绍不同的 `<!DOCTYPE>` 下对应的文档模式。

#### 关于 WebBrowser 的文档模式检测

很简单地过程，只要使用 `documentMode()` 输出一下文档模式即可。简单测试代码：

* XAML:

        <StackPanel>
            <TextBlock FontSize="{StaticResource PhoneFontSizeLarge}" Margin="{StaticResource PhoneMargin}">doctype and flexbox test</TextBlock>
            <phone:WebBrowser Name="wb1" IsScriptEnabled="True" Height="300" Margin="{StaticResource PhoneMargin}"></phone:WebBrowser>

            <phone:WebBrowser Name="wb2" IsScriptEnabled="True" Height="300" Margin="{StaticResource PhoneMargin}"></phone:WebBrowser>
        </StackPanel>

* CS:

        using Microsoft.Phone.Controls;
        namespace PhoneApp3
        {
            public partial class MainPage : PhoneApplicationPage
            {
                // Constructor
                public MainPage()
                {
                    InitializeComponent();

                    var s2 = @"<!doctype html>
                            <html lang='en'>
                            <head>
                            <title>Document</title>
                            <style type='text/css'>
                            .flex{display: -ms-flexbox;}
                            .flex div{-ms-flex:1 0 auto; width: 200px; height: 200px;}
                            .red{background: red;}
                            .blue{background: blue;}
                            .green{background: green;}
                            </style>
                            </head>
                            <body>
                            <p>DocumentMode: <span id='mode' style='color:red'></span></p>
                            <div class='flex'>
                            <div class='red'></div>
                            <div class='blue'></div>
                            <div class='green'></div>
                            </div>
                            </body>
                            <script>
                            var m = document.getElementById('mode');
                            m.innerText = document.documentMode;
                            </script>
                            </html>
                            ";

                    var s3 = @"
                            <html lang='en'>
                            <head>
                            <title>Document</title>
                            <style type='text/css'>
                            .flex{display: -ms-flexbox;}
                            .flex div{-ms-flex:1 0 auto; width: 200px; height: 200px;}
                            .red{background: red;}
                            .blue{background: blue;}
                            .green{background: green;}
                            </style>
                            </head>
                            <body>
                            <p>DocumentMode: <span id='mode' style='color:red'></span></p>
                            <div class='flex'>
                            <div class='red'></div>
                            <div class='blue'></div>
                            <div class='green'></div>
                            </div>
                            </body>
                            <script>
                            var m = document.getElementById('mode');
                            m.innerText = document.documentMode;
                            </script>
                            </html>
                            ";

                    wb1.NavigateToString(s2);
                    wb2.NavigateToString(s3);
                }
            }
        }

启动程序即可得到测试结果，我们应该尽可能地让浏览器保持在最新的文档模式中工作，保持最好的 HTML 支持和 JS 性能。

**2013-05-22更新**：WebBrowser 控件在显示大量文字的时候性能很差，原因未明。

[QuirksMode]: http://zh.wikipedia.org/zh-cn/%E6%80%AA%E5%BC%82%E6%A8%A1%E5%BC%8F
[WebBrowserBroken]: http://mikaelkoskinen.net/webbrowser-navigatetostring-broken-in-windows-phone-8-and-also-affects-windows-phone-7-apps-solution-included/
[wbencode]: http://stackoverflow.com/questions/16276833/windows-8-phone-webbrowser-navigatetostring-does-not-work-when-meta-tag-meta-ch
[doc-compat]: http://msdn.microsoft.com/en-us/library/ie/cc288325
[legacy-doc-modes]: http://msdn.microsoft.com/en-us/library/ie/jj676915(v=vs.85).aspx