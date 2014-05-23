date: 2012-12-26 
title: 《浏览器工作原理》学习笔记
permalink: my-notes-about-how-browsers-work
tags: [notes,browser]
---

学习内容来自于HTML5Rocks网站，[《浏览器的工作原理：现代浏览器幕后揭秘》](http://www.html5rocks.com/zh/tutorials/internals/howbrowserswork/)，简单输入输出一下读后笔记。

## 解析
解析文档是指将文档转化成有意义的结构，也就是可让代码理解和使用的结构。

解析得到的结果通常是代表了文档结构的节点树，它称作解析树或者语法树。

### HTML解析
#### HTML语法定义
常规解析器都不适用于HTML，HTML并不能很容易地用解析器所需的的上下文无关的语法来定义。

有一种可以定义HTML的正规格式：DTD（Document Type Definition，文档类型定义），但它还是与上下文无关的语法。原因是HTML的语法处理很宽容，允许省略某些隐匿添加的标记，有时还能省略一些起始或者结束标记等等。

#### DOM
解析器输出的“解析树”是由DOM元素与属性节点构成的树结构。DOM是文档对象模型（Document Object Model）的缩写。它是HTML文档的对象表示，同时也是外部内容与HTML元素之间的接口。

[HTML5规范详细地打描述了解析算法](http://www.whatwg.org/specs/web-apps/current-work/multipage/parsing.html)。此算法由两个阶段组成：标记化和树构建。

![HTML解析流程][fig9]
[fig9]:http://1-ps.googleusercontent.com/x/s.html5rocks-hrd.appspot.com/www.html5rocks.com/zh/tutorials/internals/howbrowserswork/308x400ximage017.png.pagespeed.ic.BGy2jYmiQr.jpg "HTML5规范中的解析流程"

#### 解析算法

我们在之前章节已经说过，HTML 无法用常规的自上而下或自下而上的解析器进行解析。

原因在于：

* 语言的宽容本质。
* 浏览器历来对一些常见的无效 HTML 用法采取包容态度。
* 解析过程需要不断地反复。源内容在解析过程中通常不会改变，但是在 HTML 中，脚本标记如果包含 document.write，就会添加额外的标记，这样解析过程实际上就更改了输入内容。

HTML的解析算法由两个阶段组成：标记化和树构建

##### 标记化算法

	<html>
		<body>
			Hello world
		</body>
	</html>

初始状态是数据状态，当遇到字符`<`时，状态更改为“标记打开状态”。接收一个`a-z`字符会创建“起始标记”，状态更改为“标记名称状态”。这个状态会一直保持到接收`>`。在此期间接收的每个字符都会附加到新的标记名称上。在本例中，我们创建的标记是`html`标记。

遇到`>`标记时，会发送当前的标记，状态发回“数据状态”。`<body>`标记也会进行同样的处理。目前`html`和`body`标记均已发出。现在我们回到“数据状态”。接收到`Hello world`中的`H`字符时，将创建并发送字符标记，直到接收`</body>`中的`<`。我们将为`Hello world`中的每个字符都发送一个字符标记。

现在我们回到“标记打开状态”。接收下一个输入字符`/`时，会创建`end tag token`并改为“标记名称状态”。我们会再次保持这个状态，直到接收`>`。然后将发送新的标记，并回到“数据状态”。`</html>`输入也会进行同样的处理。

![标记化算法](http://www.html5rocks.com/zh/tutorials/internals/howbrowserswork/image019.png)

##### 树构建算法

树构建阶段的输入是一个来自标记化阶段的标记序列。第一个模式是**“initial mode”**。接收HTML标记后转为**“before html”**模式，并在这个模式下重新处理此标记。这样会创建一个HTMLHtmlElement元素，并奖其附加到Document根对象上。

后续状态：

1. **“before head”**，接收“body”标记，创建HTMLHeadElement，添加到树中。
2. **“in head”**模式，然后转入**“after head”**模式。创建并插入HTMLBodyElement，然后模式转变为**“body”**。
3. 接收body中的字符串，然后创建并插入**“text”**节点，其他字符也将附加到该节点
4. 接收body结束标记，触发**after body**模式，接收剩余的HTML结束标记。解析过程结束。

![树构建算法](http://www.html5rocks.com/zh/tutorials/internals/howbrowserswork/image022.gif)

#### 解析结束后的操作
文档标记为交互状态，可以解析处于“deferred”模式的脚本。

#### 浏览器容错机制
浏览器会纠正任何无效内容，然后继续工作。Webkit在HTML解析器类的形状注释中对此做了相应的概括：

解析器对标记化输入内容进行解析，以构建文档树。如果文档的格式正确，就直接进行解析。遗憾的是，我们不得不处理很多格式错误的 HTML 文档，所以解析器必须具备一定的容错性。
	
我们至少要能够处理以下错误情况：
	
1. 明显不能在某些外部标记中添加的元素。在此情况下，我们应该关闭所有标记，直到出现禁止添加的元素，然后再加入该元素。
2. 我们不能直接添加的元素。这很可能是网页作者忘记添加了其中的一些标记（或者其中的标记是可选的）。这些标签可能包括：HTML HEAD BODY TBODY TR TD LI（还有遗漏的吗？）。
3. 向 inline 元素内添加 block 元素。关闭所有 inline 元素，直到出现下一个较高级的 block 元素。
4. 如果这样仍然无效，可关闭所有元素，直到可以添加元素为止，或者忽略该标记。

### CSS解析

词法语法（词汇）是针对各个标记用正则表达式定义的：

	comment   \/\*[^*]*\*+([^/*][^*]*\*+)*\/
	num   [0-9]+|[0-9]*"."[0-9]+
	nonascii  [\200-\377]
	nmstart   [_a-z]|{nonascii}|{escape}
	nmchar    [_a-z0-9-]|{nonascii}|{escape}
	name    {nmchar}+
	ident   {nmstart}{nmchar}*

语法是采用BNF格式描述的。[什么是BNF格式](http://www.douban.com/group/topic/7580567/)？豆瓣里面有解释。

#### Webkit CSS 解析器

![Webkit CSS解析](http://1-ps.googleusercontent.com/x/s.html5rocks-hrd.appspot.com/www.html5rocks.com/zh/tutorials/internals/howbrowserswork/image023.png.pagespeed.ce.uVfINk36yE.png)

## 呈现树构建（Render Tree）
在 DOM 树构建的同时，浏览器还会构建另一个树结构：呈现树。这是由可视化元素按照其显示顺序而组成的树，也是文档的可视化表示。它的作用是让您按照正确的顺序绘制内容。

在Webkit中，如果一个元素需要创建特殊的呈现器，就会替换`createRenderer`方法。呈现器所指向的样式对象中包含了一些和几何无关的信息。

### 呈现树与DOM树的关系

![呈现树与DOM树的关系](http://www.html5rocks.com/zh/tutorials/internals/howbrowserswork/image025.png)

### 样式计算
#### 共享样式数据

Webkit 节点会引用样式对象 (RenderStyle)。这些对象在某些情况下可以由不同节点共享。这些节点是同级关系，并且：

* 这些元素必须处于相同的鼠标状态（例如，不允许其中一个是“:hover”状态，而另一个不是）
* 任何元素都没有 ID
* 标记名称应匹配
* 类属性应匹配
* 映射属性的集合必须是完全相同的
* 链接状态必须匹配
* 焦点状态必须匹配
* 任何元素都不应受属性选择器的影响，这里所说的“影响”是指在选择器中的任何位置有任何使用了属性选择器的选择器匹配
* 元素中不能有任何 inline 样式属性
* 不能使用任何同级选择器。WebCore 在遇到任何同级选择器时，只会引发一个全局开关，并停用整个文档的样式共享（如果存在）。这包括 + 选择器以及 :first-child 和 :last-child 等选择器。



