date: 2012-12-25 11:54
title: 在Windows下面使用MarkdownEditing
permalink: mod-mdediting-for-win
tags: markdown
---

MarkdownEditing是[ttscoff](https://github.com/ttscoff)编写的一个Sublime Text 2插件，用于在ST2中进行Markdown文件的编写。插件中添加一系列的快捷键和自动处理，方便大家在ST2中进行MD的编写。虽然暂时还比不上专门用来处理Markdown编写的MarkdownPad之类的软件，但对习惯使用ST2的同学们来说有这么一个插件还是很好的。

MarkdownEditing插件所在的Github：[戳我进入](https://github.com/ttscoff/MarkdownEditing)。

由于作者暂时只添加了为Mac OS X的快捷键绑定，同时提交到Package Control里面的版本安装的时候提示不支持Windows（实际上是支持的）。所以我们只好直接到Github里面把整个Repo拉下来吧。

下面所说的配置内容可以[点击此处下载](http://d.pr/f/TEr6)。

## 安装

1. 通过 `Preferences -> Browse Packages...` 打开Packages目录，将 `MarkdownEditing` 的Repo复制到Packages目录下面。

		Windows: git clone https://github.com/ttscoff/MarkdownEditing.git %APPDATA%\Sublime/ Text/ 2/\MarkdownEditing	

2. 重启ST2完成安装。

初次启动的时候可能会提示错误，原因是Windows下面默认没有安装`Menlo`这个字体，所以我们需要打开`Markdown.sublime-settings`和`MultiMarkdown.sublime-settings`这两个文件，将`font-face`选项注释掉。

    // "font_face": "Menlo",

如此操作则可以将字体设置还原为ST2默认的设置。另外，这两个设置文件中还有不少选项可以进行修改，下面的设置可以自行修改测试。插件中默认提供了两个不同的色彩文件，修改`color_scheme`可以切换Markdown的语法高亮格式。

    {
        "extensions":
        [
            "md",
            "mdown",
            "mmd",
            "txt"
        ],
        "trim_trailing_white_space_on_save": false,
        // "font_face": "Menlo",
        // "font_size": 15,
        "font_options": [ "subpixel_antialias", "no_round", "directwrite"],
        "color_scheme": "Packages/MarkdownEditing/MarkdownEditor.tmTheme",
        // "color_scheme": "Packages/MarkdownEditing/MarkdownEditor-Focus.tmTheme",
        "translate_tabs_to_spaces": true,
        "word_wrap": true,
        "wrap_width": 70,
        "draw_centered": true,
        "auto_match_enabled": true,
        "line_padding_top": 5,
        "caret_style": "wide",
        "highlight_line": true,
        // add trailing #'s to headlines
        "match_header_hashes": false
    }

## MarkdownEditing的功能
下面将列出MarkdownEditing提供的功能。

### 语法增强类
- 星号\*、下划线\_和反引号\`自动配对
- 如输入的自动配对符号中间内容为空时，删除第一个符号时将直接删除整对符号
- 如输入自动配对符号后直接输入空格，则自动删除后面自动配对的符号
- 波浪线 `~` 包围的内容将转换为HTML中的 `<del></del>` 标签
- 当创建了列表后，回车将自动添加一个列表项。如列表项为空，再次回车将删除该列表项

### 快捷键类（根据自行修改的`Default (Windows).sublime-keymap`列出）
MarkdownEditing在Windows下面的快捷键需要自行根据`Default (OSX).sublime-keymap`中的内容进行修改，添加到`Default (Windows).sublime-keymap`中。

- `Ctrl+Win+V` 选中的内容将自动转换为行内式超链接，链接到剪贴板中的内容
- `Ctrl+Win+R` 选中的内容将自动转换为参考式超链接，链接到剪贴板中的内容
- `Ctrl+Alt+R` 弹出提示框插入一个参考式超链接，在提示框中输入链接内容和定义参考ID[^3]
- `Ctrl+Win+K` 插入一个标准的行内式超链接
- `Win+Shift+K` 插入一个标准的行内式图片（此快捷键可能与输入法有冲突）
- `Ctrl+1` 至 `Ctrl+6` 插入一级至六级标题
- `Win+Alt+i` 选中的内容转换为*斜体*
- `Win+Alt+b` 选中的内容转换为**粗体**[^1]
- `Ctrl+Shift+6` 自动插入一个脚注，并跳转到该脚注的定义中。
- `Alt+Shift+F` 查找没有定义的脚注并自动添加其定义链接
- `Alt+Shift+G` 查找没有定义的参考式超链接并自动添加其定义链接
- `Ctrl+Alt+S` 脚注排序
- `Ctrl+Shift+.` 缩进当前内容
- `Ctrl+Shift+,` 提前当前内容