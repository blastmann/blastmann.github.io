date: 2013-02-05 09:35
title: 如何编写一个 Sublime Text 2 插件
permalink: how-to-create-a-st2-plugin
tags: [st2,plugin]
---

最近折腾了一个调用 ScriptOgr.am 的 API 发布博客文章的小插件，主要是参考了 Prefixr 这个插件编写而成的。在编写过程中算是把 Python 这东西入门了一点，下面总结一点东西，分享。

网上关于如何编写 ST2 插件的文章：[点击进入](http://net.tutsplus.com/tutorials/python-tutorials/how-to-create-a-sublime-text-2-plugin/)

下面的代码内容托管在我的 Github 上，有兴趣可以[点击这里](https://github.com/blastmann/ScriptOgrSender)。

## Step 1: 创建一个新的插件
创建新插件的步骤很简单，只需要点击菜单栏上的 Tools->New Plugin.. 即可，ST2将自动创建一个简单的插件模板，代码如下：

    import sublime, sublime_plugin
    class ExampleCommand(sublime_plugin.TextCommand):
        def run(self, edit):
            self.view.insert(edit, 0, "Hello, World!")

在 Packages 文件夹里面，创建一个属于你自己的插件名字的文件夹，然后将代码保存到其中，即可以在 Console 中运行下面的命令：

    view.run_command('example')

命令运行完成后，当前窗口将自动插入一行字符 "Hello, World!"。恭喜你，插件的编写就是这么简单。

## Step 2: 命令类型及其命名
关于 Sublime Text 2 中的命令类型，本人通过查找 `sublime_plugin.py` 中定义的类，大概知道有下面几种：

* Application Command - 调用 ST2 本身的程序命令
* Window Command - 对应当前窗口的命令
* Text Command - 文字处理型命令

在创建属于我们自己的插件时，我们可能需要继承上面列出的几种命令中的其中一种或多种来实现我们自己的功能。

关于插件中的命令命名，我们在定义自己的插件命令时，需要注意以下格式：

- 命令需要通过定义类来声明，命令类至少需要继承上面的三种命令这一
- 类的名称中以 `Command` 来结尾，`Command` 前的名称即为命令的名称
- 命令名称需要注意使用驼峰式命名，在 Sublime Text 2 中，驼峰式命名将转换为通过下划线 `_` 分隔的命名。例如：`TextSelectCommand` 最后将转换为 `text_select`。

## Step 3: 线程
在我的插件里面，需要通过 HTTP 来提交属于博客文章内容。如果在主线程中创建 HTTP Post 请求的话，整个 Sublime Text 将会失去响应，直到请求完成。因此我们需要将请求代码放到另外一个单独的线程中进行。

    thread = ScriptOgrApiCall(filename, content, 'post', self.user_id, self.proxy_server, 500)
    threads.append(thread)
    thread.start()

创建线程后，HTTP 请求将在后台进行，减轻对主界面的影响。

## Step 4: 创建线程
为了将我们需要提交的内容放置到单独的线程中，我创建了一个单独的 ApiCall 类，负责接收请求的内容。

线程初始化时，我定义了好几个参数以传入线程中进行处理，参数基本对应 ScriptOgr.am 中的 API 请求而制定的：

    class ScriptOgrApiCall(threading.Thread):
        """docstring for ScriptOgrApiCall"""
        def __init__(self, filename, filedata, operation, user_id, proxy_server, timeout):
            threading.Thread.__init__(self)
            self.filename  = filename
            self.filedata  = filedata
            self.operation = operation
            self.timeout   = timeout
            self.user_id   = user_id
            self.proxy     = proxy_server
            self.response  = None
            self.result    = None

下面就是在此类中创建不同函数以适应调用需要，具体代码不再列出。

## Step 5: 结果处理
线程执行完毕后，我将服务器返回的 JSON 解析后输出赋予线程中的 response 属性。解析 JSON 时使用的是 Python 自带的 JSON 模块。

    def parse_response(self):
        response = json.loads(self.response)
        if response['status'] == 'success':
            if self.operation == 'post':
                self.response = 'Successfully post your article'
            elif self.operation == 'delete':
                self.response = 'Successfully delete your article'
        elif response['status'] == 'failed':
            self.response = response['reason']

## Step 6: 管理线程
在创建自己的命令时，我先行创建一个命令基类，定义一些需要重复使用的函数：

    class ScriptOgrCommandBase(sublime_plugin.TextCommand):
        """docstring for CommandBase"""
        def __init__(self, view):
            # Inherit from class TextCommand
            sublime_plugin.TextCommand.__init__(self, view)

创建好基类后，定义一个线程管理类，负责监控线程的运行情况，如线程完成后，则打印出服务器返回的信息：

    def handle_threads(self, threads, i=0, dir=0):
        next_threads = []
        for thread in threads:
            if thread.is_alive():
                next_threads.append(thread)
            else:
                print '\nScriptOgr.am api response: ' + thread.get_response() + '\n'
                sublime.status_message('ScriptOgr.am api response: ' + thread.get_response())
            if thread.result == False:
                continue
        threads = next_threads

        if len(threads):
            before = i % 8
            after = (7) - before
            if not after:
                dir = -1
            if not before:
                dir = 1
            i += dir
            self.view.set_status('operating', 'ScriptOgrSender is opearting [%s=%s]' % \
                (' ' * before, ' ' * after))

            sublime.set_timeout(lambda: self.handle_threads(threads, i, dir), 100)
            return
        self.view.erase_status('operating')

其中调用了一些 ST2 本身提供的 API，如 `set_status`、`erase_status` 等，用于将信息更新至 ST2 窗口下方的状态栏中。

## Step 7: 插件配置文件
很多插件都会自带一个配置文件（以 `.sublime-settings` 后缀结尾的文件），用以配置用户的参数，我们也可以将一些有可能修改的字段定义在插件配置文件中，日后便不用修改代码，直接修改配置文件即可。

下面是我的配置文件示例（JSON格式）：

    /* ScriptOgr default setting */
    {
        "proxy_server" : "",
        "user_id" : "",
        "base_url": "http://scriptogr.am/api/article/"
    }

读取文件配置的代码如下，调用一下 Sublime Text 2 提供的 API 即可。

    settings = sublime.load_settings('ScriptOgrSender.sublime-settings')
    base_url = settings.get('base_url')
    self.user_id = settings.get('user_id')
    self.proxy_server = settings.get('proxy_server')

## Step 8: 快捷键绑定
ST2 中的快捷键绑定可以说是最强大的功能之一了，其可定义性极高，只需要稍微理解一下示例中的定义即可创建出属于自己的快捷键绑定了。

ScriptOgrSender 中的快捷键绑定如下：

    [
        {
            "keys": ["shift+alt+p"],
            "command": "post_scr",
            "context":
                [
                    { "key": "selector", "operator": "equal", "operand": "text.html.markdown" }
                ]
        },
        {
            "keys": ["shift+alt+d"],
            "command": "del_post_scr",
            "context":
                [
                    { "key": "selector", "operator": "equal", "operand": "text.html.markdown" }
                ]
        }
    ]

其中， `keys` 即需要绑定的快捷键组合，ST2 提供了 Ctrl\Alt\Shift\Super 等常用的辅助键定义（`Super` 即键盘上的 Windows 键，或者是 Mac OS X 中的 Command 键）， `command` 即快捷键对应的命令，其定义请参考本文第一步。 `context` 字段定义了一个快捷键启用的上下文，即只有在 `text.html.markdown` 格式中才启用上面的快捷键。

## Step 9: 添加菜单选项
下面说一下菜单选项，如果需要在 `Preferences` 菜单中添加插件相关的配置菜单项，请自行添加一个 `Main.sublime-menu` 文件，用于定义主菜单项目。内容太长在文章中就不贴出来了，具体可以参考其他插件中的文件。

另外，需要在右键菜单中添加快捷选项的话，请添加一个 `Context.sublime-menu`，简单内容如下：

    [
        { "command": "post_scr", "caption": "Post to ScriptOgr.am" },
        { "command": "del_post_scr", "caption": "Delete this post on ScriptOgr.am" }
    ]

## Step 10: 发布你的插件包
如果需要将你亲自编写的插件发布到 Package Control 上，可以参照官网上的说明（[点击查看](http://wbond.net/sublime_packages/package_control/package_developers)）。

## 开始编写属于你自己的插件吧！
上面的内容都是兴趣使然的结果，本来对 Python 这语言也有一点点兴趣的我，由于没有什么实质的需求，一直没有怎么学习。通过自己编写这样的一个简单的小插件，感觉除了对 Python 语言本身熟悉一点点之外，还在过程中感受到之前的编程中没有使用过的小技巧的好处。感觉自己逐渐地对编程有点感觉了，不然也不会不停地去思考如何去增强代码的复用程度，精简代码中的冗余部分。

总的来说，自行去编写一个属于自己的插件这件事情，还是一件挺有意义的事情来的。一方面可以满足到自己的需求，另外一方面也可以锻炼到自己。另外， Sublime Text 3 已经发布测试版本了，平台也切换到 Python 3 了，到时还需要检查插件运行是否正常。