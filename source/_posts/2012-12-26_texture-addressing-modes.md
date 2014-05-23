date: 2012-12-26 12:16
title: Texture Addressing Modes（纹理地址模式）  
permalink: texture-addressing-modes
tags: #directx
---

Direct3D中的纹理都是位图，所以任何位图数据都可以赋予给一个Direct3D原始数据。除此之外，D3D还可以支持更多的高级渲染技术，例如纹理混合和光源映射。想得到更多相关的信息，可以参阅[Texture Blending](http://msdn.microsoft.com/en-us/library/windows/desktop/bb206241(v=vs.85).aspx)和[Light mapping with Textures](http://msdn.microsoft.com/en-us/library/windows/desktop/bb174695(v=vs.85).aspx)。

如果你的应用程序创建了一个HAL（硬件抽象层）设备或者一个软设备，则可以使用8/16/24/32/64或者128位的纹理。

## Texture Addressing Modes（纹理地址模式）
### Wrap Texture Address Mode
### Mirror Texture Address Mode
### Clamp Texture Address Mode
### Border Color Texture Address Mode

## Texture Dirty Regions（纹理污染区域）
通过指定纹理中的污染区域，应用程序可以只更新纹理中的部分区域。只有被标明为污染的区域才会调用``IDirect3DDevice9::UpdateTexture``来拷贝更新区域。然而，污染区域的声明还需要考虑对齐优化的问题。当纹理创建完成后，整个纹理都会被认为是受污染的（脏的）。只有下面的操作会影响纹理的污染状态：

* 在纹理中添加一个污染区域
* 锁定部分纹理缓存，此操作将自动添加锁定区域为污染区域
* 在``IDirect3DDevice9::UpdateSurface``中使用表面级别的纹理作为目标纹理
* 在``IDirect3DDevice9::UpdateTexture``中将纹理作为源，用来清除源纹理中的污染区域
* 使用``IDirect3DSurface9::GetDC``来返回设备上下文

因为每种纹理都有不同类型的污染区域，所以各个纹理类型都有相应的方法取得相应的信息。

* `IDirect3DCubeTexture9::AddDirtyRect`
* `IDirect3DTexture9::AddDirtyRect`
* `IDirect3DVolumeTexture9::AddDirtyBox` 

当使用`NULL`作为`pDirtyRect`或者`pDirtyBox`作为参数传入上述方法中时，污染区域将会扩展覆盖至整个纹理。

每个锁定方法都可以传入`D3DLOCK_NO_DIRTY_UPDATE`用于防止纹理的污染状态改变。
详情可以参阅[Locking Resource](http://msdn.microsoft.com/en-us/library/windows/desktop/bb174707(v=vs.85).aspx)。

## Texture Palettes（纹理调色板）
D3D9支持对纹理进行调色。在`IDirect3DDevice9`对象中，有一套256色的调色板。可以通过`IDirect3DDevice9::SetCurrentTexturePalette`设置当前的调色板属性。