title: MVVM SideKick使用心得
permalink: mvvmsidekick-experience
date: 2014-09-27 16:48:24
tags:
---

框架之前做练手的时候也有用过一段时间，当时就当作一般的MVVM来用了一下，也没有用到像页面跳转的那种功能。昨天经韦恩叔指点之后，好好学习了一下类似Unity IoC框架，终于对这个框架有点感觉了。

## ViewModelLocator

这两天遇到这么一个需求：在一个ListView里面封装的列表，点击不同的列表项再对应生成该页面的VM，最后用StageManager进行跳转。

刚开始的时候相着这个应该可以用Factory来解决，但是大叔的框架里面VM似乎不推荐使用类继承的方法来进行扩展。问了一下，叔说：“接口继承，在ServiceLocator里面注册好了最后拿来用就行。”

当时确实不知道ServiceLocator这东西，在叔的指引下翻了一下Unity框架的书，才大概了解类的生成还能用这么一种方法进行扩展，用起来确实挺灵活的。

ViewModelLocator也是ServiceLocator的一种，除了用来注册VM的生成，它还负责VM->View的绑定。

暂时我对这需求的解决方法是：在选中项中添加一个特定的字段和一个公共的Interface，特定字段与VML中注册VM时使用的Key一致，然后调用VML.Resolve进行类的生成。