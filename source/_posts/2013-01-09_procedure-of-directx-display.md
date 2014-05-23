date: 2013-01-09
title: DirectX显示流程学习小结
permalink: procedure-of-directx-display
tags: [directx,programming]
---

下面说一下近来对DX学习的一些自己的理解，不对的地方请提出。下面部分内容可以直接到微软WP8开发者页面查询，[点击链接](http://msdn.microsoft.com/zh-cn/library/windowsphone/develop/jj714079(v=vs.105).aspx)。

## 无法正常显示图像的原因
* 设备初始化过程中出现异常
* 三种视图初始化或设置错误
* 着色器编写错误
* 纹理资源视图设置
* 二维投影视图设置与三维投影视图设定时，位图顶点缓存位置设置的区别
* 交换链创建时，建议交换链创建时缓存结构格式使用 `DXGI_FORMAT_B8G8R8A8_UNORM` 。在调用 `D3D11CreateDeviceAndSwapChain` 或者 `D3D11CreateDevice` 的时候，添加 `D3D11_CREATE_DEVICE_BGRA_SUPPORT` 的标志选项。
* 注意纹理生成时的格式处理（ `DXGI_FORMAT_B8G8R8A8_UNORM` 与 `DXGI_FORMAT_R8G8B8A8_UNORM` 的区别），BGRA与RGBA的区别将造成红蓝两色相反

基本上DX的使用过程中需要注意的地方都是一些小细节问题，稍微出现一点点差错就会造成图像无法显示、显示错误之类的问题，而且比较多的时候都不会有

## 桌面DirectX程序与WP8上的DirectX Component之间的区别
桌面程序中仍然需要绑定HWND等句柄。内容刷新过程可以使用WM\_PAINT、ValidateRect和InvalidateRect等传统的窗体消息循环过程。通过WM\_PAINT消息通知DirectX组件进行初始化及屏幕刷新等信息。不使用WM\_PAINT消息循环亦可，但需要在DX中自行处理消息响应。

使用DirectX的原因是由于WP8系统上不支持传统的GDI函数，无法直接进行屏幕显示内容的刷新。

WP8上使用DirectX Component则与上述流程有所不同。注意以下几点：

* WP8上的DX Component，需要与XAML中的DrawingSurfaceBackgroundGrid或DrawingSurface这两个控件进行绑定。
* 绑定控件后，两种控件都会有不同的接口需要实现。（[后续列出](#dxctrlapi)）
* 两种控件的绑定过程中，DX设备与交换链中的初始化过程不一样，前者将不需要自行初始化交换链，性能更好。
* 桌面程序中可以调用的DX接口更丰富，WP8中的部分接口实现需要重新封装成异步操作，提高UI的响应效率。
* HLSL编写的着色器程序，在WP8编译过程中需要使用编译器对其进行处理，桌面程序则可以在应用程序启动的时候使用相应的API（`D3DX11CompileFromFile`）进行编译。性能自然是前者更好，因此仍然需要重新编写测试工程中的DX组件。
* 桌面程序的窗口大小可变，WP8上的应用窗口大小不可变，两者之间的区别会影响DX组件中对交换链的创建处理、纹理大小的创建之类的问题。这也是为何桌面上的游戏程序一般均进行窗口大小锁定，避免Resize过程对显示内容造成影响。
* 桌面上的DX在初始化的过程中需要检查显卡支持的分辨率，在创建过程需要注意窗口的大小是否符合显卡的大小。当然，我们可以固定创建一个分辨率固定的设备，在纹理生成过程通过更改纹理的顶点缓存位置进行显示区域的修改。在WP8上不需要注意此过程。
* WP8的DX组件需要通过复制”同步纹理“来更新显示内容，此接口可以处理为死循环，则会实现高性能屏幕输出，但CPU占用率较高。可以根据自己的需要来修改相应的循环过程。

## 接口代码 <a id="dxctrlapi"></a>
下面的DX接口代码可以在`DrawingSurfaceNative.h`头文件中查询。

##### DrawingSurfaceBackgroundGrid:

    IDrawingSurfaceBackgroundContentProviderNative : public IUnknown
    {
    public:
        virtual HRESULT STDMETHODCALLTYPE Connect( 
            /* [annotation][in] */ 
            _In_  IDrawingSurfaceRuntimeHostNative *host,
            /* [annotation][in] */ 
            _In_  ID3D11Device1 *hostDevice) = 0;
        
        virtual void STDMETHODCALLTYPE Disconnect( void) = 0;
        
        virtual HRESULT STDMETHODCALLTYPE PrepareResources( 
            /* [annotation][in] */ 
            _In_  const LARGE_INTEGER *presentTargetTime,
            /* [annotation][in][out] */ 
            _Inout_  DrawingSurfaceSizeF *desiredRenderTargetSize) = 0;
        
        virtual HRESULT STDMETHODCALLTYPE Draw( 
            /* [annotation][in] */ 
            _In_  ID3D11Device1 *hostDevice,
            /* [annotation][in] */ 
            _In_  ID3D11DeviceContext1 *hostDeviceContext,
            /* [annotation][in] */ 
            _In_  ID3D11RenderTargetView *hostRenderTargetView) = 0;
        
    };
    

##### DrawingSurface:

    IDrawingSurfaceContentProviderNative : public IUnknown
    {
    public:
        virtual HRESULT STDMETHODCALLTYPE Connect( 
            /* [annotation][in] */ 
            _In_  IDrawingSurfaceRuntimeHostNative *host) = 0;
        
        virtual void STDMETHODCALLTYPE Disconnect( void) = 0;
        
        virtual HRESULT STDMETHODCALLTYPE PrepareResources( 
            /* [annotation][in] */ 
            _In_  const LARGE_INTEGER *presentTargetTime,
            /* [annotation][out] */ 
            _Out_  BOOL *isContentDirty) = 0;
        
        virtual HRESULT STDMETHODCALLTYPE GetTexture( 
            /* [annotation][in] */ 
            _In_  const DrawingSurfaceSizeF *surfaceSize,
            /* [annotation][out] */ 
            _Outptr_  IDrawingSurfaceSynchronizedTextureNative **synchronizedTexture,
            /* [annotation][out] */ 
            _Out_  DrawingSurfaceRectF *textureSubRectangle) = 0;
        
    };

上述的接口代码中可以看到两者的区别比较明显的是：DSBG控件将由系统创建DX设备、设备上下文、RenderTargetView资源视图。而DrawingSurface则只会负责传入控件的大小和同步纹理（SynchronizedTexture），其他DX所需的资源将要由我们自行创建。但需要注意的是，即使是使用DSBG，我们也可以使用自行创建的设备，具体可以参考HybridMarbleMaze这个示例游戏，游戏对比了两种控件的效率，后者效率仅为前者的2/3。

## DirecXHelper.h
此文件封装了一部分WP8平台上文件读取和错误信息抛出的函数，帮助我们更方便地创建异步操作。

    #pragma once
    #include <wrl/client.h>
    #include <ppl.h>
    #include <ppltasks.h>
    #include <memory>

    namespace DX
    {
        inline void ThrowIfFailed(HRESULT hr)
        {
            if (FAILED(hr))
            {
                // Set a breakpoint on this line to catch DirectX API errors
                throw Platform::Exception::CreateException(hr);
            }
        }

        struct ByteArray { Platform::Array<byte>^ data; };

        // function that reads from a binary file asynchronously
        inline Concurrency::task<ByteArray> ReadDataAsync(Platform::String^ filename)
        {
            using namespace Windows::Storage;
            using namespace Concurrency;
            auto folder = Windows::ApplicationModel::Package::Current->InstalledLocation;
            task<StorageFile^> getFileTask(folder->GetFileAsync(filename));
            // Create a local to allow the DataReader to be passed between lambdas.
            auto reader = std::make_shared<Streams::DataReader^>(nullptr);
            return getFileTask.then([](StorageFile^ file)
            {
                return file->OpenReadAsync();
            }).then([reader](Streams::IRandomAccessStreamWithContentType^ stream)
            {
                *reader = ref new Streams::DataReader(stream);
                return (*reader)->LoadAsync(static_cast<uint32>(stream->Size));
            }).then([reader](uint32 count)
            {
                auto a = ref new Platform::Array<byte>(count);
                (*reader)->ReadBytes(a);
                ByteArray ba = { a };
                return ba;
            });
        }
    }

ReadDataAsync函数是示例工程中提供的用于异步读取着色器编译后的cso文件的接口，当然也可以用于其他地方的文件读取。只需要简单地将文件读取调用封装成Task即可。

## XAML中的D3D
下面摘录一部分来自微软官网的文档：

每次 XAML 引擎更新 XAML UI 时，它都会调用 Draw 方法。当前帧完成后，对 RequestAdditionalFrame 的调用将立即请求 XAML 引擎重新绘制屏幕。要降低应用的耗电量，您可以修改模板代码，以便每次调用 Draw 方法时不会调用 RequestAdditionalFrame。每次更新 UI 时，XAML 引擎仍然调用 Draw，但它不会立即尝试重新绘制。当应用显示不需要在尽可能最高的帧速率下进行重新绘制的静态内容时，这特别有用。
