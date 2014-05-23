date: 2013-05-27 16:41
title: Windows Phone UI 开发中的各种诡异
permalink: ui-dev-tricks-in-windows-phone
tags: [windows,wp8]
---

## 自定义 TextBox 的诡异地方
自己自定义了一个`TextBox`，`TextBox`样式设置高度之类的属性，然后发现里面选中的时候选择手柄没有显示完整，于是发现可以通过设置 `MaxHeight` 来让手柄显示正常。

[参考资料：FrameworkElement中的高度信息][FrameworkElement]

> **依赖项属性标识符字段： `MaxHeightProperty`**

> 这是 `FrameworkElement` 上的三个用于指定高度信息的属性之一。 另外两个是 `MinHeight` 和 `Height`。 如果这三个值之间存在冲突，则应用程序确定高度的实际顺序是：首先必须采用 `MinHeight`；然后采用 `MaxHeight`；最后，如果这些值中的每个值都在限制之内，则采用 `Height`。

> 从技术角度讲，允许 `MaxHeight` 的值不是整数，但应通常避免这种情况，并且一般通过默认的布局舍入行为来舍入这些值。

## ScrollViewer 做渐变动画时内容变模糊

在测试的示例代码中基本结构是在一个`ScrollViewer`中内嵌一个`StackPanel`，然后添加一个`TextBlock`和一个`Button`。点击`Button`，触发`Button`上的`Click`事件，启动外层`Grid`上的渐变动画。

测试结果如下：

- 当`ScrollViewer`中内容不多的时候（不超过最外层`Grid`的高度），动画显示正常，内容不会出现模糊。
- 复制示例代码中的`TextBlock`，确保`ScrollViewer`高度大于外层`Grid`高度，再次点击`Button`进行测试，动画显示正常，但动画过程中内容变模糊，直至动画完成。

根据动画进行过程中的内存情况分析，猜测动画过程中，如对`ScrollViewer`本身及其外层窗口进行渐变动画，`ScrollViewer`将自动开启`BitmapCache`（渲染大小为1X），造成一定程度的模糊，同时内存也会对应上升一定程度（动画结束后内存释放）。

暂时发现比较好的解决方法是：直接对内嵌于`ScrollViewer`中的`Panel`控件做动画，模糊问题可以得到解决。但`ListBox` \ `LLS`等控件该怎么获取内部`ScrollViewer`中的控件，这是一个问题，或者是对其中的`ItemsPresenter`进行动画吧。

示例代码如下（包含多余的样式代码）：

*  XAML:
        
        <Grid x:Name="ContentPanel" Grid.Row="1" Margin="12,0,12,0">
            <ScrollViewer Name="ContentSV">
                <StackPanel Name="ContentSP">
                    <Button Content="Fade Grid" Click="FadeGrid_OnClick"/>
                    <Button Content="Fade ScrollViewer" Click="FadeSV_OnClick"></Button>
                    <Button Content="Fade StackPanel" Click="FadeSP_OnClick"/>

                    <TextBlock TextWrapping="Wrap">
                        Lorem ipsum Pariatur sint occaecat sunt sint do labore adipisicing 
                        eiusmod incididunt culpa laborum consequat magna dolor labore sunt sed 
                        ullamco anim adipisicing do pariatur ea esse qui sint magna in voluptate 
                        Duis id ut anim id.
                    </TextBlock>

                    <TextBlock TextWrapping="Wrap">
                        Lorem ipsum Pariatur sint occaecat sunt sint do labore adipisicing 
                        eiusmod incididunt culpa laborum consequat magna dolor labore sunt sed 
                        ullamco anim adipisicing do pariatur ea esse qui sint magna in voluptate 
                        Duis id ut anim id.
                    </TextBlock>

                    <TextBlock TextWrapping="Wrap">
                        Lorem ipsum Pariatur sint occaecat sunt sint do labore adipisicing 
                        eiusmod incididunt culpa laborum consequat magna dolor labore sunt sed 
                        ullamco anim adipisicing do pariatur ea esse qui sint magna in voluptate 
                        Duis id ut anim id.
                    </TextBlock>

                    <TextBlock TextWrapping="Wrap">
                        Lorem ipsum Pariatur sint occaecat sunt sint do labore adipisicing 
                        eiusmod incididunt culpa laborum consequat magna dolor labore sunt sed 
                        ullamco anim adipisicing do pariatur ea esse qui sint magna in voluptate 
                        Duis id ut anim id.
                    </TextBlock>

                    <TextBlock TextWrapping="Wrap">
                        Lorem ipsum Pariatur sint occaecat sunt sint do labore adipisicing 
                        eiusmod incididunt culpa laborum consequat magna dolor labore sunt sed 
                        ullamco anim adipisicing do pariatur ea esse qui sint magna in voluptate 
                        Duis id ut anim id.
                    </TextBlock>
                </StackPanel>
            </ScrollViewer>
        </Grid>


* C#:
        
        private void FadeInAndOut(DependencyObject dObj)
        {
            var storyb = new Storyboard();
            Duration Show_Duration = new Duration(new TimeSpan(0, 0, 0, 0, 450));
            DoubleAnimation m_OpacityAni = new DoubleAnimation();
            m_OpacityAni.Duration = Show_Duration;
            m_OpacityAni.From = 1.0;
            m_OpacityAni.To = 0.0;
            m_OpacityAni.AutoReverse = true;

            storyb.Children.Add(m_OpacityAni);

            Storyboard.SetTarget(m_OpacityAni, dObj);
            Storyboard.SetTargetProperty(m_OpacityAni, new PropertyPath("(UIElement.Opacity)"));

            storyb.Begin();
        }

        private void FadeGrid_OnClick(object sender, RoutedEventArgs e)
        {
            FadeInAndOut(ContentPanel);
        }

        private void FadeSP_OnClick(object sender, RoutedEventArgs e)
        {
            FadeInAndOut(ContentSP);
        }

        private void FadeSV_OnClick(object sender, RoutedEventArgs e)
        {
            FadeInAndOut(ContentSV);
        }

## ApplicationBar 的坑爹处

`ApplicationBar` 的透明度很坑爹，如果透明度为`1`，它将表现为属于页面的一部分，将占据页面中部分空间。如果透明度小于`1`（如`0.99`），它将表现为覆盖在页面之上，不会占据页面的空间。

那这个时候就有问题了。如果我们页面中有一个 `ListBox` （或者 `LLS` ），我们需要将它滚动至最后一项时， `ApplicationBar` 透明度小于`1`时将会阻挡其显示。有什么办法可以解决这个问题呢？

1.  Hard Code `ListBox`（或`LLS`） 父容器的高度或者外边距

    这种方法个人觉得并不好用，如果页面不考虑旋转的话还好，如果要考虑旋转的话，就必须在旋转的时候注意设置其父容器的高度（`Height`）或外边距（`Margin`）。这样我们需要计算的数字比较多，容易造成混乱，而且每次旋转之后都要重新设置高度或者外边距，自适应性不好。不过，原始的方法总是比较实用的对吧。

2.  为 `LongListSelector` 设置 `ListFooter` 

    查看了官方文档之后发现`LLS`本身有两个很有趣的属性：`ListFooter`和`ListHeader`关于这两个部分的位置，官方文档上有一个图描述得非常清楚：

    ![Header&Footer](http://i.msdn.microsoft.com/dynimg/IC619230.png)

    经测试，这种方法相当于在`LLS`头部或尾部添加了一个特殊项，我们只要将这个特定项设置为空的、有一定高度（一般是 72px）的元素即可。测试出来的效果跟系统的`人脉`中显示效果一致，滚动至底部后将出现一定的空白用于分隔列表与 ApplicationBar。

    ![People](http://d.pr/i/iHMH.png)

    第二种方法比第一种方法好的地方就是：不需要另外指定`Margin`或者`Height`这样的属性，所有元素都是自适应的，比起第一种方法要灵活一点。特别是在`Pivot`和`Panorama`控件下，不同的页面中对`ApplicationBar`的要求不一样，当`ApplicationBar`高度不统一时，我们就需要对其列表控件的高度或外边距进行多个设置，不甚灵活。

3.   `ListBox` 怎么办？

    经少量测试，如果给`ListBox`最后添加上一项空白项的话，可能会造成选项错误。Google 之后发现，还是有一些比较 Tricky 的方法的。下面列出一种：

    对`ListBox`的模板进行修改，在`ItemsPrestenter`下面添加一个高度为`72px`的空白项。示例代码：

        <ControlTemplate>
            <ScrollViewer Height="{Binding Height,RelativeSource={RelativeSource Mode=TemplatedParent}}">
                <StackPanel>
                    <ItemsPresenter />
                    <Canvas Height="72" />
                </StackPanel>
            </ScrollViewer>
        </ControlTemplate>

    但是这种方法有 Bug，造成`VirtualizingStackPanel`的数据虚拟化失效，暂时没有找到除了设置固定高度之外的解决方法。

## ToolKit 中的 SlideInEffects 在 WP8 中无效

原因：WP8 中，`LongListSelector`、`Panorama` 和 `Pivot` 属于框架中的一部分，它们的 `ManipulationCompleted` 事件默认被标识为 `handled`，以提高界面的流畅性。

如果真的要处理 Pivot 控件的 `ManipulationCompleted` 事件的话，可以把 `SlideInEffects.cs` 的 `OnParentPivotPropertyChanged` 函数中的

    newPivot.ManipulationCompleted += Pivot_ManipulationCompleted;

替换为：

    newPivot.AddHandler(Pivot.ManipulationCompletedEvent, new EventHandler<ManipulationCompletedEventArgs>(Pivot_ManipulationCompleted), true);

但处理效果不好，会导致动画效果异常。原因是 `SelectionChanged` 事件在 `ManipulationCompleted` 事件完成之后才会触发，因此造成动画效果异常。

比较丑陋的解决方法是：将 `SelectionChanged` 事件处理与 `ManipulationCompleted` 对调，同时将 `fromRight` 变量抽取为静态变量，让动画在 `SelectionChanged` 事件中进行处理。[**点击这里下载**](http://d.pr/f/MiSr)。

## Toolkit 中的 HubTile 滑动展开到最大后消失及没有适配 WP8 的新翻转效果

经过排查发现，原因应该是 `Generic.xaml` 中的状态动画没有对 `Collapsed` 状态进行定义。另外，文件里的动画也很久没有更新了，没有适配 WP8 首屏瓷砖翻转时的 `BackEase` 效果。我在原来的 `HubTile` 基础上加了一些内容，主要更新点是：

* 当瓷砖中有具体信息时，瓷砖不会采用滑动展开的动画，只会使用翻转动画。
* 稍微调整了一下动画触发的时间，减少等待。
* 适配 WP8 的动画效果。

具体可以[点击这里](http://d.pr/f/7tlo)下载代码。

## ListPicker 选项初始位置偏移的问题

在升级 Windows Phone Toolkit 的开发测试过程中出现过这么一个现象：

> `ListPicker` 的初始化一切都很正常，但是在完成初始化之后，选项的第一项位移有些许偏移，而且在初次打开的时候会比较卡。

![ListPicker](http://d.pr/i/fkdl.png)

调试中发现：当 `ListPicker` 在绑定 `SelectionChanged` 事件后，进行添加数据的操作将会引起 `SelectionChanged` 事件的反复调用，估计是反复调用 `SelectionChanged` 引起的问题。

解决错位的问题：只需要把数据绑定完成之后，再进行事件绑定操作即可，避免事件反复触发进行控件布局异常。

## 点击事件与背景色

点击事件的触发与元素的背景色有关系，示例代码：

* XAML:

        <Grid x:Name="ContentPanel" Grid.Row="1" Margin="12,0,12,0" Tap="ContentPanel_OnTap">
            <Grid Tap="UIElement_OnTap" Height="300"></Grid>
        </Grid>

* CS:

        private void ContentPanel_OnTap(object sender, GestureEventArgs e)
        {
            System.Diagnostics.Debug.WriteLine(e.OriginalSource.ToString() + "1");
            e.Handled = true;
        }

        private void UIElement_OnTap(object sender, GestureEventArgs e)
        {
            System.Diagnostics.Debug.WriteLine(e.OriginalSource.ToString() + "2");
            e.Handled = true;
        }

* 大致布局如下，高亮框为内嵌高度为300px的 Grid：

    ![Layout](http://d.pr/i/Fcl2.png)

示例很简单，只是两个 Grid 的嵌套加上 `Tap` 事件的简单输出。运行的时候可以发现，我们点击外层 Grid 时输出窗口并没有输出内容，但点击中间的 Grid 时则有输出 `System.Windows.Controls.Grid2` 的信息，而两者的区别仅在于背景色的设置。在设计流式布局时，要注意这个问题，有时候点击事件没有触发的原因仅仅是因为外层的容器没有设置一个透明的背景色。

当 `Background` 属性为空时，点击该元素并不会触发 `Tap` 事件，只有当 `Background` 属性不为空（如不想影响显示效果，可设置为 `Transparent`），点击事件才会触发。

## 莫名其妙的 TextBox 获取焦点事件触发（2013-05-27更新）

页面结构基本如下：

    - Grid
      - ScrollViewer
        - StackPanel
          - TextBox
          - TextBlock

问题就是，当我们点击 TextBlock 设置 Grid 进行隐藏时，ScrollViewer 很神奇地会让 TextBox 触发 `GotFocus` 事件，导致页面隐藏后出现软键盘。

废话不多说了，直接看代码：

* XAML:

        <Grid x:Name="ContentPanel" Grid.Row="1" Margin="12,0,12,0">
            <Grid.RowDefinitions>
                <RowDefinition Height="Auto"></RowDefinition>
                <RowDefinition Height="*"></RowDefinition>
            </Grid.RowDefinitions>

            <Button Grid.Row="0" Click="ButtonBase_OnClick">Display</Button>

            <Grid Grid.Row="1" Name="canvas" GotFocus="UIElement_OnGotFocus">
                <ScrollViewer Name="SV" GotFocus="UIElement_OnGotFocus" >
                    <StackPanel>
                        <TextBox Name="TB" GotFocus="UIElement_OnGotFocus" Width="200" />
                        <TextBlock Margin="0,50,0,0" Tap="ButtonBase_OnClick" 
                                   GotFocus="UIElement_OnGotFocus">Hide</TextBlock>
                    </StackPanel>
                </ScrollViewer>
            </Grid>

* CS:

        private void ButtonBase_OnClick(object sender, RoutedEventArgs e)
        {
            System.Diagnostics.Debug.WriteLine("Click: " + sender.GetType());
            
            // 在修改`Visibility`前禁用ScrollViewer
            SV.IsEnabled = canvas.Visibility != Visibility.Visible;
            
            canvas.Visibility = canvas.Visibility == Visibility.Visible
                                    ? Visibility.Collapsed
                                    : Visibility.Visible;
        }

        private void UIElement_OnGotFocus(object sender, RoutedEventArgs e)
        {
            System.Diagnostics.Debug.WriteLine("GotFocus: " + sender.GetType() + ", Source: " + e.OriginalSource);
        }

暂时的解决方法是：在隐藏外层 Grid 时，对 `ScrollViewer.IsEnabled` 设置为 `False`，或者直接对 ScrollViewer 设置隐藏，两个方法都不会触发到 TextBox 的 `GotFocus` 事件。


[FrameworkElement]: http://msdn.microsoft.com/zh-cn/library/windowsphone/develop/system.windows.frameworkelement.maxheight(v=vs.105).aspx
