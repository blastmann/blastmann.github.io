date: 2013-05-23 21:00
title: 创建宽度高度自适应的 Windows Phone App 界面布局
permalink: create-a-flexible-wp-app-page-layout
tags: [windows,wp8]
---

#### [1] 利用好 Grid 的分行/分列功能

Grid 提供了分行/分列的属性，示例代码如下：

    <Grid.RowDefinitions>
        <RowDefinition Height="Auto"/>
        <RowDefinition Height="*"/>
        <RowDefinition Height="2*"/>
    </Grid.RowDefinitions>

其中行高（列宽）有几种取值方式：

1. 直接指定数值。此方式最直接，将直接指定具体高度或宽度。
2. 使用 `Auto` 值。使用 `Auto` 的话，Grid 将根据该行/列内容计算其占据空间的大小。
3. 使用 `*` 值。使用 `*` 的话，Grid 将根据其他的行/列占据空间后剩余的空间来计算此行/列的大小。此值还支持比例计算，如示例代码中的 `2*`，表示 Grid 的空间在第一行计算完成后，剩余空间将均分为3份，第二行占据一份，第三行占据两份。

分行/分列的属性在实现页面基础布局的情况下十分有用。但需要注意不要在数据模板中使用过于复杂的 Grid 结构，否则会导致大量计算资源消耗在计算 Grid 布局上。

相关资料：《[关于 WPF 中的面板性能分析](http://scriptogr.am/blastmann/post/wpf-panels-performance)》

#### [2] 注意对齐属性的区别

1.  `HorizontalAlignment` / `VerticalAlignment` （水平对齐和垂直对齐）

    `HorizontalAlignment` 和 `VerticalAlignment` 是 FrameworkElement 中定义的两个属性。当 FrameworkElement 位于面板或项控件中时，这两个属性将会有应用，设置后影响此元素的布局。默认值是 `Stretch`，如果需要建立一个自适应的布局，最好不要修改此值。

    - `HorizontalAlignment` 取值： `Left` / `Right` / `Center` / `Stretch`。
    - `VerticalAlignment` 取值： `Top` / `Bottom` / `Center` / `Stretch`。

    当前元素没有设置宽度（或高度）时，如使用除 `Stretch` 以外的值，会导致元素的大小变为该元素内部的元素占据的大小。如：

        <Border Height="50" BorderBrush="White" BorderThickness="3" Background="Red"
                HorizontalAlignment="Left">
        </Border>

    则此 `Border` 的宽度将变为0。因此，注意 `Stretch` 的使用。

2.  `HorizontalContentAlignment` / `VerticalContentAlignment` （内容水平对齐和内容垂直对齐）

    `HorizontalContentAlignment` 和 `VerticalContentAlignment` 是 Control 中实现的两个属性，主要影响控件内元素的排列位置，默认值分别是 `HorizontalAlignment.Left` 和 `VerticalAlignment.Top`。同样地，如果将属性设置为 `Stretch` 的话，则内部元素在没有设置固定大小时将会得到拉伸处理。

    - `HorizontalContentAlignment` 取值： `Left` / `Right` / `Center` / `Stretch`。
    - `HorizontalContentAlignment` 取值： `Top` / `Bottom` / `Center` / `Stretch`。

强调这两个属性的原因是，当我们需要实现弹性布局时，使用 `Stretch` 可以免除频繁设置元素大小的困扰。