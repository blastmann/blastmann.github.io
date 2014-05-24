title: Effective Objective-C 阅读记录
permalink: effective-objetive-c-note
date: 2014-05-24 12:31:59
tags:
---

关键的最佳实践：

## 第一章：了解OC

1. Item 2: 减少头文件的引用：在.h文件中添加#import的时候，其它文件引用此.h文件时也会导入其它的头文件。此时可以使用@class转发声明，然后在.m中再引入该类的头文件。简单地说就是只在Implementation中进行头文件的引用，减少多重引用。使用这种方法声明的时候，如果外部需要访问该类的方法/属性，则需要再引用该类的头文件，否则会报错。
2. Item 4: 常量使用类型常量定义更好，减少使用宏定义。因为在头文件中定义宏的话，所有引用它的地方都会进行宏替换，相当于添加了一些不必要的暴露。

## 第二章：对象、消息和运行时

1. Item 9: 学会使用类簇，更好地 封装不同的数据和逻辑（书中介绍的是抽象类的使用）
2. Item 11: 理解objc_msgSend的作用
    * OC中函数调用的流程中会应用到动态绑定
    * OC中的函数调用声明，最终都是使用objc_msgSend()函数进行消息发送的。
3. Item 12: 理解消息转发的过程
    * 当一个对象接收一个它不明白的方法，对象会开始消息转发，根据对象的继承关系进行消息转发，最终传递至根对象（一般是NSObject）。如果找不到实现的方法，则Runtime最终会抛出异常。
    * 消息转发有两种途径。
		- 动态方法解析：当一个对接收到了一个未知的类方法 调用时，对象会执行resolveInstanceMethod进行方法的动态解析，此时会在类中查找已经实现的接口。（必须注意，调用的方法一定要有实现，否则会失败进入第二阶段的查找）
		- 接收者替换：当动态查找无法找到指定Selector方法时，接收者可以指定一个方法替换者进行消息转发。具体会使用forwardingTargetForSelector这个方法。
		- 完全转发机制（Full Forwarding Mechanism）：触发此机制时，Runtime会创建一个NSInvocation对象（内含Selector\Object\Arguments），使用forwardInvocation进行对象的转发，最终成功调用时可以直接对NSInvocation对象进行Invoke

4. Item 12: 消息转发过程中，Selector对应的名字有可能发生改变。
5. Item 14: 理解OC中的Class Object：OC中的对象声明基本都是使用指针，对象比较时优先使用内省函数，避免部分对象重写了消息转发流程引发错误的消息转发。

### 第三章：接口和API设计

1. Item 15: 使用正确的前缀，避免使用命名空间。因为OC中并不存在命名空间的概念，因此如果前缀使用不正确，将会导致程序链接出错（函数符号名称有可能发生重复，导致链接错误）。即使是没有在头文件中声明的函数，也会出现在符号表中的（本来就没有private的概念）。
2. Item 17: 重写description方法可以方便输出对象的信息
3. Item 21: 理解OC的异常模型：即使使用ARC的情况下，应用执行时如果抛出异常信息，则异常对象前的资源不会正常释放，容易造成内存泄漏。建议是使用NSError进行普通异常信息传递，出现严重异常时才向外抛出NSException。使用NSError时，需要在API中传入NSError对象。
4. Item 22: 理解NSCopying协议：实现NSCopying协议时，建议都是重写copyWithZone:，而且需要仔细检查对象内部的变量是需要浅复制还是深复制。

## 第四章：协议和分类

1. Item 23: 对象间通信请使用Delegate或Data Source Protocols：使用delegate时，注意声明过程中必须将delegate声明为weak，否则会造成循环引用。
2. Item 27: 使用class-continuation category来隐藏实现细节。
3. Item 28: 使用协议来提供匿名对象（暂时未明白怎么做）

## 第五章：内存管理

1. Item 29: 理解引用计数。
2. Item 31: 只在dealloc中进行引用解除和KVO清理。如果一个对象持有了系统资源（如文件描述符），则此类对象应该有一个统一的cleanup\close接口，便于调用它的对象在使用完成后释放相关的系统资源。另外，不建议在dealloc方法中调用当前对象的方法，因为当前对象在进入dealloc时一般处于生命周期要结束的时候，调用其它方法有可能在方法未完成调用的时候出现对象被回收的情况，导致应用crash。
3. Item 32: 注意异常处理流程时的内存管理。在ARC下，我们会以为try/catch语句在使用时，系统会自动处理掉异常抛出前的对象释放，实际不会！而且在ARC下，我们不能在finally语句中手动调用release方法，这样会导致明显的内存泄漏（这不是Bug吗？！）。EOC建议是使用NSError代替大部分NSException，如果真的需要捕获异常，则建议打开-fobjc-arc-exceptions。
4. Item 33: 使用弱引用避免发生循环引用。
5. Item 35: 使用僵尸对象来帮助调试内存问题。Cocoa框架有一个“僵尸”特性，当调试启用时，

## 第六章：block和GCD
1. Item 37: 理解block。block跟C#里面的委托差不多，定义之后会引用作用域外的变量。需要注意的是：
    * block中引用的外部变量不能在block中进行修改（除非变量声明为__block）。
    * block的声明一般是分配在栈上，如果在if/else语句（即不同的作用域中）进行block的赋值，则有可能造成函数调用出错。如果真要这样使用，建议在赋值时添加copy，将block分配到堆中（此时则需要注意block的生命周期）。
    * 如果block在定义的时候没有捕获到任何外部变量，则block会转化成全局block。全局block永远不会回收（单例对象）。
2. Item 38: 使用typedefs来定义常用block类型。例子：
```objective-c
    typedef int(^EOCSomeBlock)(BOOL flag, int value);  
    EOCSomeBlock block = ^(BOOL flag, int value){ // implementation };
```
3. Item 42: 使用GCD替代performSelector及其相关。在if/else语句中为selector进行赋值，有可能会导致在ARC环境下面出现内存泄漏。原因是在if/else中使用selector时，编译器不确定selector的类型，进而无法确定performSelector能否正常执行，使得ARC不知道该 对象能否正常释放导致编译时没有添加release语句，导致了泄漏。
4. Item 43: 合理使用GCD和Operation Queue。原因：
    * 使用NSOperation的时候，可以通过设置内部的标识来中止任务，但GCD只要加入队列后就无法取消（Fire and Forget）。
    * 任务间依赖。NSOperation可以设置不同的任务间有依赖关系。
    * Key-Value观察。
    * 任务优先级。NSOperation可以设置优先级，通过优先级的设置来调整任务的顺序。GCD没有现成的方法来达到这一目的，它的优先级设置是面对整个任务队列的，无法设置队列内每个block独自的优先级。
    * 重用性。除非你使用了SDK提供的NSOperation子类（如NSBlockOperation），否则你需要自己实现一个子类。
5. Item 44: 使用Dispatch Group。（未明白到底有什么具体好处）
6. Item 45: 使用dispatch_once 来进行线程安全一次性代码执行。具体应用在单例模式中。
7. Item 46: 避免使用dispatch_get_current_queue。原因是在使用dispatch_sync的时候如果发生dispatch_get_current_queue，将会导致死锁。（不知道理解得对不对，因为书里面介绍的情况比较多）。

## 第7章 - 系统框架

1. Item 48: 使用迭代器块取代for循环。
    * 快速迭代。类似C#里面的foreach，只要使用for-in语法即可，用来遍历NSArray比较方便。
    * 使用block进行遍历。内建的几个集合类都支持使用block进行遍历，这样遍历的时候有时会比使用for-in更方便。还支持使用NSEnumerationOptions进行反向遍历或并行遍历。
2. Item 49: Use toll-free bridging for collections with custom memory-management semantics（不是很明白在说什么）
    * __bridge：ARC仍然对该OC对象有拥有权。
    * __bridge_retained：ARC将拥有权交出（后续处理需要用户自行释放，使用CFRelease）
    * __bridge_transfer：将拥有权交给ARC
3. Item 50: 使用NSCache代替NSDictionary作为缓存。
4. Item 51: 让initialize和load的函数实现保持简洁。
5. Item 52: NSTimer会保持对象的引用。如果一个对象内建NSTimer，Timer本身对该对象有引用，则会引发循环引用。导致对象本身在外部引用移除后，仍然不能被释放。使用block可以一定程度上解决这问题。使用Category拓展NSTimer，添加一个使用block的静态方法。
    
