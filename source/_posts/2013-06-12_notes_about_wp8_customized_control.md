date: 2013-06-12 16:54
title: Windows Phone 自定义控件学习小记
permalink: notes-about-wp8-customized-control
tags: [note,wp8]
---

## 自定义控件的简单过程记录

1.  新建项目（Windows Phone Class Library）
2.  新建一个类，继承自 `Control` 类，并在构造函数中定义 `DefaultStyleKey`，示例如下：

        public class CustomControl : Control
        {
            public CustomControl()
            {
                DefaultStyleKey = typeof (CustomControl);
            }
        }

3.  在项目中添加一个新文件夹，名字定义为：Themes（必须是这个名字）。
4.  在 Themes 文件夹中添加一个 `Generic.xaml` 文件，内建一个自定义的资源字典，示例如下：

        <ResourceDictionary
            xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
            xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
            xmlns:phoneClassLibrary1="clr-namespace:PhoneClassLibrary1">
            
            <Style TargetType="phoneClassLibrary1:CustomControl">
                <Style.Setters>
                    <Setter Property="Background" Value="{StaticResource PhoneAccentBrush}"/>
                    <Setter Property="Template">
                        <Setter.Value>
                            <ControlTemplate TargetType="phoneClassLibrary1:CustomControl">
                                <Border BorderThickness="{StaticResource PhoneBorderThickness}" 
                                        BorderBrush="{StaticResource PhoneBorderBrush}" 
                                        Background="{StaticResource PhoneAccentBrush}" />
                            </ControlTemplate>
                        </Setter.Value>
                    </Setter>
                </Style.Setters>
            </Style>
        </ResourceDictionary>

    **注意**：Style 在定义时切莫声明 `Key` 值，否则会造成样式无法索引，编译通过、运行正常但控件无法显示。

5.  在 Windows Phone 应用程序工程中引用此类库项目，尝试添加以上定义的 `CustomControl`，编译运行，观察是否正常显示。运行截图如下：

    ![CustomControl](http://d.pr/i/PX3B.png)
