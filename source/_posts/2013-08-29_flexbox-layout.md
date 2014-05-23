date: 2013-08-29 16:10
title: Flexbox 布局简述
permalink: flexbox-layout
tags: [webdev,css3,ie11]
---

# Flexbox 布局简述

Flexbox 布局将有下面一系列的属性设置：

* flex-basis
* flex-grow
* flex-shrink
* flex
* align-items
* align-self
* align-content
* order
* justify-content
* flex-wrap

## flex\flex-grow\flex-shrink\flex-basis

`flex` 属性是 `flex-grow`\\`flex-shrink`\\`flex-basis` 的速写。下面先讲述一下这一系列的属性。

### flex-basis

> 作用：设置弹性项目的初始宽度。  
> 初始值：auto  
> 可接受的值：非负数，单位可以为CSS提供的长度单位

效果图如下：

[![flex-basis](http://d.pr/i/mluE.png)](http://d.pr/i/mluE)

### flex-grow

> 作用：设置弹性项目宽度比例系数。*flex grow*设置后将根据外容器剩余宽度和弹性项目的数量来分配对应弹性项目的宽度。
> 初始值：0  
> 可接受的值：非负数

效果图如下：

[![flex-grow](http://d.pr/i/8Uie.png)](http://d.pr/i/8Uie)

外层 flex 容器宽度为 600px，`.dodgerBlue`的系数设置为2，`.limeGreen`的系数设置为1。则布局后`.dodgerBlue`的宽度为200px，`.limeGreen`宽度为100px。弹性项目按比例均分外层容器的宽度。

值得一提的是，如果弹性项目设置有宽度或者`flex-basis`，布局时顺序将变化为：先按项目本身设定的宽度或 flex-basis 进行布局，再在剩余空间中根据 flex-grow 系数进行剩余空间分配（在元素内包含文字时弹性项目的大小也会发生变化，具体分配规则暂时还不清楚）。效果图如下（`.dodgerBlue`的初始宽度为200px，`.limeGreen`没有设置初始宽度）：

[![flex-grow-and-flex-basis](http://d.pr/i/iaDC.png)](http://d.pr/i/iaDC)

### flex-shrink

> 作用：设置弹性项目压缩比例系数。*flex shrink*设置后将根据外容器本身宽度和弹性项目的数量来分配对应弹性项目的宽度。  
> 初始值：0  
> 可接受的值：非负数

与 `flex-grow` 相反，`flex-shrink`在基于弹性项目本身的宽度上再对其宽度按系数进行压缩，具体分配规则暂时确定是：在 `flex-basis` 存在的情况下，按照 `flex-shrink` 的值确定弹性项目的分配比例，如外层容器为100px，`.dodgerBlue` 宽度为100%、压缩系数为3，`limeGreen` 宽度也为100%、压缩系数为1。此时按照压缩系数对弹性项目的宽度进行重新分配，则 `.dodgerBlue` 需要压缩100px/4*3=75px，最终宽度为25px。

需要注意的是，在 IE10 下，弹性项目的表现与 `flex-shrink:0` 效果相同，即 `flex-shrink:0` 时项目本身不进行宽度压缩。

示例代码：

    .dodgerBlue{
        background: dodgerBlue;
        flex-basis:100%;
        flex-shrink:3;
    }

    .limeGreen{
        background: limeGreen;
        flex-basis:100%;
    }

效果图如下：

[![flex-shrink](http://d.pr/i/pjvM.png)](http://d.pr/i/pjvM)

需要注意的是，`flex-shrink` 只在弹性项目充满外层容器后才会生效，而 `flex-grow` 则在外层容器空间尚未完全分配时起效。

### flex

此属性是上述三个属性的速写属性，可授受的值为：

    flex: none |[<'flex-grow'> <'flex-shrink'>?||<'flex-basis'>]

## order

> 作用：设置弹性项目在弹性容器中的显示顺序，一般来说弹性项目的显示顺序与源代码中的元素声明顺序相同，除非特别声明 `order` 属性。
> 初始值：0  
> 可接受的值：整数

**注意**：在`order`相同的情况下，顺序将以元素声明顺序确定。

示例代码：

    #flex{
        width: 300px;
        height: 200px;
        overflow: hidden;
        display: flex;
    }

    .dodgerBlue{
        background: dodgerBlue;
        flex-basis:100%;
        order:2;
    }

    .limeGreen{
        background: limeGreen;
        flex-basis:100%;
        order:0;
    }

    .yellowGreen{
        background: yellowGreen;
        flex-basis:100%;
        order:1;
    }

效果图：

[![flex-order](http://d.pr/i/n8LP.png)](http://d.pr/i/n8LP)

## flex-direction

> 作用：设置弹性项目的显示方向  
> 初始值：row  
> 可接受的值：row | row-reverse | column | column-reverse

属性比较容易理解，不截图了。

## flex-wrap

> 作用：设置弹性项目在分配空间时横向空间到分配完后是否进行换行分配，此时纵向空间将结合弹性项目本身的高度和弹性盒本身的高度来确定。  
> 初始值：nowrap  
> 可接受的值：nowrap | wrap | wrap-reverse

属性比较容易理解，不截图了。

## flex-flow

即 `flex-direction` 和 `flex-wrap`　的速写属性，可授受的值为：

    flex-flow: <'flex-direction'> <'flex-wrap'>

## align-items/align-self/align-content/justify-content

### align-items

> 作用：对弹性盒设置弹性项目的对齐方式  
> 初始值：stretch  
> 可接受的值：flex-start | flex-end | center | stretch | baseline

### align-self

> 作用：对弹性项目本身设置其对齐方式  
> 初始值：auto  
> 可接受的值：auto | flex-start | flex-end | center | baseline | stretch

`auto`：如果弹性项目的父元素是一个弹性容器，`align-self`与弹性容器的`align-items`属性的值一致。否则其值为**stretch**。

### align-content

> 作用：让弹性项目之间的行间距按照设置的值进行分布，分布方向与 `flex-direction` 中设置的方向相同
> 初始值：stretch  
> 可接受的值：flex-start | flex-end | center | space-between | space-around | stretch

两个特别的值说明：

 * space-between：弹性项目在 `flex-direction` 设置的方向上进行两端对齐
 * space-around：弹性项目在行间距中间的位置进行对齐

效果图：

[![align-content](http://d.pr/i/X3il.png)](http://d.pr/i/X3il)

### justify-content

> 作用：设置弹性项目在主分布轴上的对齐方式（与文字对齐方式类似）  
> 初始值：flex-start  
> 可接受的值：flex-start | flex-end | center | space-between | space-around

直接看图比较好理解：

[![justify-content](http://d.pr/i/yXgF.png)](http://d.pr/i/yXgF)