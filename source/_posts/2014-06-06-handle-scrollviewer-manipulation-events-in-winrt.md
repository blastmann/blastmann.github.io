title: WinRT下ScrollViewer的Manipulation事件如何响应
permalink: 'handle-scrollviewer-manipulation-events-in-winrt'
date: 2014-06-06 12:44:13
tags: [winrt,wp8.1,xaml]
---

## 前言

WP 8.1发布了，并且官方也宣布了Universal App的开发方式。可以针对Windows 8.1和Windows Phone 8.1的同时开发一个项目。UI部分只需要简单适配一下就可以了，大部分API都是共用的（个人对8.1研究不大深入，这里说的只是个大概的理解，有错误请指正）。

## XAML App和Silverlight 8.1

8.1环境下面，有个概念要搞清楚：XAML App和Silverlight App不是一回事。虽然大家都用XAML，但8.1 XAML App的UI模型和Silverlight的模型不大一样，而且XAML App支持使用C/C++进行UI编程，这样做起来好像是会对内存控制上好一点。

可惜的是，XAML App暂时还不能完全替代掉Silverlight App，但这肯定是一个趋势。而且看Silverlight App中控件的API在8.1下面基本没有增加（其实我也觉得XAML App里面的控件用起来更爽）。

## 正题

说了那么多，下面讲一下这次的正题。在XAML App下，`UIElement`引入了`ManipulationMode`的概念。下面是官方解释：

> 如果要处理操作事件（例如从您应用程序代码中 UI 元素的 ManipulationStarted），则必须将 ManipulationMode 设置为其他值，而不是 System 或 None。
> 
> ManipulationMode 的典型默认值为 System 而不是 None。该值为 System 时，源自该元素的操作可以由根据 直接操作API 的 Windows 
> 
> ]运行时基础结构处理。例如，ScrollViewer 按其控件逻辑处理用户操作，并将它们作为控件的滚动事件处理。System 值还可启用响应操作事件的个性动画。
> Slider 和 ToggleSwitch 具有默认模板，将 ManipulationMode 值设置为 None，因此，None 将是在设计时所看到的默认值。
> 
> 指定相关的操作模式
> 你可以在代码或 XAML 中使用所示的逗号语法将多个按标志的 ManipulationModes 值指定为 ManipulationMode 属性的值。例如，可以合并 TranslateX、TranslateY、Rotate 和 Scale，或者它们的任意组合。但是，并非所有组合都有效。仅当特定控件使用 ManipulationModes 后，才会强制实施有效性，因此设置存在的问题（ManipulationModes 的无效组合）不到运行时可能不会出现。不要合并 Translate* 值与 TranslateRails* 值，因为它们被视为独占值，不合并惯性值与非惯性值。All 值不是所有标志的实际附加值，因此，All 不一定表示所有值的组合有效，或已设置任何特定值。
在 Windows 8 上，如果将 ManipulationMode 设置为一个将 System 与其他值组合的值，将会引发异常。从 Windows 8.1 开始，你可以将 System 与其他值结合使用。

简单理解为：如果我们想要使用`Manipulation**`事件的话，在使用时必须将该控件的`ManipulationMode`修改为非`System`和`None`，否则系统将会接管触摸事件。

那回到这次的主题，我们想在`ScrollViewer`上对它作水平方向的平移该怎么做呢？本来我以为只要在ScrollViewer上修改它的`ManipulationMode`就可以了，结果修改之后，并没有任何反应，绑定的`ManipulationDelta`事件并不会响应：

``` xaml
<ScrollViewer x:Name="sv" Height="200" ManipulationMode="TranslateX" ManipulationDelta="UIElement_OnManipulationDelta">
    <Border Height="600" Background="Red">
        <TextBlock>1</TextBlock>
    </Border>
</ScrollViewer>
```

```csharp
private void UIElement_OnManipulationDelta(object sender, ManipulationDeltaRoutedEventArgs e)
{
    Debug.WriteLine(e.Delta.Translation.X);
}
```

后面想了一下，会不会是因为它的子控件`Border`上的事件被截获了呢？于是我又改了一下，在`Border`上绑定了一个`ManipulationDelta`事件，结果还是没有响应：

``` xaml
<ScrollViewer x:Name="sv" Height="200" ManipulationMode="TranslateX" ManipulationDelta="UIElement_OnManipulationDelta">
    <Border Height="600" Background="Red" ManipulationDelta="BorderOnManipulationDelta">
        <TextBlock>1</TextBlock>
    </Border>
</ScrollViewer>
```

于是我决定修改一下`Border`的`ManipulationMode`。发现如果修改成`All`，那`ScrollViewer`就无法正常滚动了，坑大发了。再次研读上面关于`ManipulationMode`的备注，发现这个属性的比较神奇，如果修改成非`System`外的值，那将由开发者自己去处理对应的触摸事件（这不就跟IE10开始使用那个坑爹属性`-ms-touch-action`一样吗？！）。不过XAML App里面对这个属性提供了一个神奇的使用方法：属性组合。也就是`ManipulationMode`这个属性里面，可以将多个模式组合使用。

也就是说`ManipulationMode`可以接受以下的设置方式：

```
ManipulationMode = "TranslateX,TranslateY,Rotate,Scale"
```

那这时候`Manipulation**`事件会在响应的参数里面给出TranslateX\TranslateY\Rotate\Scale等相应的响应值。

回到主题：这属性跟`ScrollViewer`有什么关系啊？还是有点关系哈，看示例代码：

``` xaml
<ScrollViewer x:Name="sv" Height="200" ManipulationDelta="UIElement_OnManipulationDelta">
    <Border Height="600" Background="Red" ManipulationMode="System, TranslateX">
        <TextBlock>1</TextBlock>
    </Border>
</ScrollViewer>
```

如果我对`ScrollViewer`的子控件添加`ManipulationMode="System,TranslateX`，那就相当于告诉系统：子控件的触摸事件除了水平方向之外，其它的都按照系统默认的响应处理。

这样一来，子控件就不会截获掉水平方向的触摸事件，而我在上层`ScrollViewer`的触摸事件绑定也可以正常响应了！

### 备注

WinRT下面对触摸事件的处理感觉是怪怪的，没有以前直观。像`ScrollViewer`的触摸事件响应，如果按照此文的方法做处理，只能针对非滚动方向做截获。意思就是：如果你的`ScrollViewer`需要水平方向的滚动，那你加上对应的`ManipulationMode`之后，水平方向的触摸就会交给你自己做处理了，也就是！如果你什么都不处理，你的`ScrollViewer`就没有办法做水平滚动啦！

所以说，此法只适合在非滚动方向上的触摸事件响应。PS：有用过IE上那个`touch-action`属性的同学应该挺好理解这问题的。