title: Swift使用感受
permalink: feeling-swift
date: 2014-07-08 09:59:46
tags: [iOS,Swift]
---

## 写在前面

Apple这次发布Swift语言，是想把OC开发者渐渐迁移到新平台上面吧。暂时来说，Swift具备了很多OC不具备的语言特性，更方便智商不够用的开发者来到iOS平台进行开发。但是，Swift离取代OC的日子还有点远。因为Swift的特性还不能完全覆盖OC的所有特性（举个例子：KVO暂时还没有）。所以未来有一段时间都会是两种语言并行使用。

在Xcode 6正式版还没有出来之前，不建议用Swift来做主力开发语言。因为Xcode 6 Beta对Swift的支持实在是有问题（至少在我的机器上是这样）。智能提示经常提示一些乱七八槽的东西，而且崩溃的机率也很大。

所以，暂时还是学好OC比较有用。虽然Swift更安全更方便，但是用OC先摸一下iOS平台上的坑，还是有必要的。

下面的内容有点乱，随便看看就好。

## Swift初体验

### 1. 基础点

1. 有动态语言的语法特征，但用的是类型推导，是编译型语言
2. 有泛型，个人觉得最直观的体现就是Array和Dictionary终于是强类型的了但还有些很神奇的坑。
3. 可空类型，有助于进行链式调用编写。
4. 官方文档上没有发现有`public` \ `private`等关键字，全部定义都是公有，这样真没有问题么？虽然类型安全了，但是API编写可能存在比较大的风险。
5. var定义的是变量，let定义的是常量（简单理解）。
6. ...这里想到再补充吧

### 2. 闭包

闭包就跟OC里面的Block差不多（Block就是一个实现得丑了一点的闭包）。

``` swift

class HTMLElement: NSObject {
    let name: String
    let text: String?
    
    @lazy var asHTML: () -> String = {
        [unowned self] in
        if let text = self.text {
            return "<\(self.name)>\(text)</\(self.name)>"
        } else {
            return "<\(self.name) />"
        }
    }
    
    init(name: String, text: String? = nil) {
        self.name = name
        self.text = text
    }
    
    deinit {
        println("\(name) is being deinitialized")
    }
}

```

##### Nested Function也算是一种闭包

``` swift

func makeIncrementor(forIncrement amount: Int) -> () -> Int {
    var runningTotal = 0
    func incrementor() -> Int {
        runningTotal += amount
        return runningTotal
    }
    return intrementor
}

```

### 3. 泛型（赞）

Swift里面可以使用泛型了，但是使用了泛型的话就不能与OC进行对接，这点需要事先声明。因为泛型不可以与OC进行对接，所以下面的代码会出现链接错误：

``` swift
class errorNSObject<T> : NSObject {
    let member: T
    init(aMember: T) {
        self.member = aMember
    }
}
```

反正我把`NSObject`的继承去掉之后就可以正常使用了，我觉得Xcode在这个提示上面可以更清晰一些，beta3里面如果有这样的编码，编译时只会提示链接错误，而且错误信息也不是很清晰。

## 与Objetive-C混合使用

### 1. 模块引用

从OC代码中引用Swift模块，只需要OC文件中引入对应的头文件，示例：

``` objc
#import "TestSwiftApp-Swift.h"
```

需要注意的是，`TestSwiftApp`这个前缀是在Build Settings是进行设置的。可以设置对应的`Product Module Name`来修改（默认是空，所以使用`Product Name`进行代替）。

如果要在Swift中使用OC代码，则需要在一个名字为`#ProductName#-Bridging-Header.h`的头文件中引用所有需要暴露给Swift的模块头文件。

### 2. 与OC API的结合使用

#### 构造函数的差别

``` objc
OBJECTIVE-C

UITableView *myTableView = [[UITableView alloc] initWithFrame:CGRectZero style:UITableViewStyleGrouped];
In Swift, you do this:
```

``` swift
SWIFT

let myTableView: UITableView = UITableView(frame: CGRectZero, style: .Grouped)
```

#### id类型与AnyObject

挺容易理解，id类型在Swift里面对应的就是AnyObject了。与OC混合使用的时候，难免会遇到NSArray、NSDictionary相互转换的情况，从OC转换过来的数组和字典里面所存的数据都是用AnyObject，转换后可以通过`as?`进行安全的类型转换。

### 3. @objc标记

如果你的类不是继承自NSObject或者OC编写的类，但又想兼容OC，可以使用`@objc`标记。

### 4. 内省方法

OC里面可以使用`isKindOfClass:`之类的方法进行对象的类型判断，Swift中可以直接通过`is`、`as`这两个关键字进行代替。

### 5. OC混合编程中无法使用的Swift特性

* Generics：泛型
* Tuples：元组
* Enumerations defined in Swift：定义在Swift中的枚举类型
* Structures defined in Swift：定义在Swift中的值类型
* Top-level functions defined in Swift：定义在Swift中的最上层函数？（一些工具类的函数可能会写在一个Swift文件中，但不属于任何类）
* Global variables defined in Swift：全局变量
* Typealiases defined in Swift：类型别名
* Swift-style variadics：Swift的可变参数
* Nested types：nested类型
* Curried functions：咖喱函数（我的智商暂时不够用，理解不了，大概是指nested函数）

## 坑s

都已经到Xcode beta3了，Swift开发环境还是一堆堆的坑，下面简单记录一下。

### 1. Xcode自动补全没反应，索引服务经常挂掉。

坑爹的是我输入一个`for`，感觉它应该给我提示自动补全一个for循环吧，结果它竟然给我提示`fork()`！而且提示里面还没有for循环的选项可以用！

### 2. delegate模式的使用

``` swift

//@class_protocol protocol ModalViewControllerDelegate {
@objc protocol ModalViewControllerDelegate {
    func modalViewControllerDidClickedDismissButton(viewController: ModalViewController)
}

class ModalViewController: UIViewController {
    // 使用weak关键字意图解决循环引用
    weak var delegate: ModalViewControllerDelegate?
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        if let sView = self.view {
            sView.backgroundColor = UIColor.lightGrayColor()
            
            if let button = UIButton.buttonWithType(UIButtonType.System) as? UIButton {
                button.frame = CGRect(x: 80, y: 210, width: 160, height: 40)
                button.setTitle("Dismiss me", forState: UIControlState.Normal)
                button.addTarget(self, action: "buttonClicked:", forControlEvents: UIControlEvents.TouchUpInside)
                
                self.view.addSubview(button)
            }
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func buttonClicked(sender: AnyObject) {
        self.delegate?.modalViewControllerDidClickedDismissButton(self)
    }
}

```

使用delegate模式时，一般都会用`weak`去解决循环引用。但直接使用`weak`的话，编译器会提示

> `weak` cannot be applied to non-class type `xxxx`

[StackOverflow上说这种情况](http://stackoverflow.com/questions/24066304/how-can-i-make-a-weak-protocol-reference-in-pure-swift-w-o-objc)需要对protocol添加关键字`@objc`或者`@class_protocol`。但现阶段使用后者的话，运行的时候程序会Crash。这是Bug吧？

### 3. `[unowned self]`导致崩溃

OC里面，当我们在使用heap block的时候，会注意到如果在block中对self进行引用的话，很容易会造成循环引用导致的内存泄漏。这时我们会使用`__weak`关键字解决这问题，例如：

``` objc

- (void)startPolling {
    __weak EOCClass *weakSelf = self;
    _pollTimer = [NSTimer eoc_scheduledTimerWithTimeInterval:5.0
                                                       block:^{
                                                    EOCClass *strongSelf = weakSelf;
                                                    [strongSelf p_doPoll];
                                                        }
                                                    repeats:YES];
}

```

在Swift中，使用属性或方法返回闭包时，官方文档上说也可以使用`unowned`关键字解决这问题。用`weak`的话应该也可以，例如：

``` swift

// 使用unowned
var asHTML: () -> String = {
    [unowned self] in
    if let text = self.text {
        return "<\(self.name)>\(text)</\(self.name)>"
    } else {
        return "<\(self.name) />"
    }
}

// 使用weak
var asHTML: () -> String = {
    [weak self] in
    if let text = self?.text {
        return "<\(self?.name)>\(text)</\(self?.name)>"
    } else {
        return "<\(self?.name) />"
    }
}

```

测试结果暂时显示，使用`unowned`的话会导致Crash。这估计是坑吧……

### 4. 多线程

用Swift重写了一次PrimeFinder，多线程方面还是可以正常使用GCD提供的功能，就是一些block的生成需要注意一下，把语法改一下就好。

由于Swift里面暂时没找到`@synchronized`这加锁的语法，所以暂时会用下面的代码代替。

``` swift

objc_sync_enter(self)
...
objc_sync_exit(self)

```

注意一下加锁的对象就好。在重写的时候发现了一个死锁的情况，例如：

``` swift
class PrimeFinder {
    var primes: [Int] = []
...

    func start() {
...
        let isPrime: dispatch_block_t = {
            [weak self] in
            for (var n = 2; n < number; n++) {
                if ((number % n) == 0) {
                    return
                }
            }
            
            objc_sync_enter(self?.primes)
            self?.primes.append(number)
            objc_sync_exit(self?.primes)
        }
...
    }
}

```

在加锁的时候使用的是`self?.primes`可能为空，导致死锁。如果单独使用一个常量`let syncObject: NSObject`来代替的话则没有问题。另外，block里面使用`unowned`似乎是一件很危险的事情，经常会出现Crash。