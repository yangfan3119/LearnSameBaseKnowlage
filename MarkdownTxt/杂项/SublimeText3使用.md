## 一、安装

[下载地址](http://www.sublimetext.com/)

### 1.0 插件安装异常

官网下载的安装包就是一个编辑器，没有相关插件，因此必须安装**插件管理程序**,即`Package Control`。

非常不幸的发现该插件存在一个巨严重的问题，就是该插件的地址需要翻墙。

**所以该记录就是给不能科学上网的同学提供的。**

本文涉及相关文件下载：https://pan.baidu.com/s/1RZiOlauRcLQi348rQYp-nA，提取码为：nmm2。

下载文件包括：

1. Sublime Text Build 3207 x64 Setup.exe ——win 64位安装包
2. Ghelper_1.4.6.beta.zip ——谷歌上网助手
3. Package Control.sublime-package ——Package Control安装包
4. channel_v3.json ——插件安装包

说明顺序为我解决该问题的过程。

一、安装

下载并安装Sublime Text Build 3207 x64 Setup.exe。安装完成后，显然至少需要一个插件，汉化包。

所以就必须拥有Package Control

二、安装Package Control

对于可以进行科学上网的同学正常的安装流程如下

>- 按ctrl+shift+p,调出隐藏搜索窗口
>- 在搜索框输入“install”,点击第一个匹配项“install package”,
>- 搜索插件`ChineseLocalizations`然后安装即可

经过查证发现这个下载包需要翻墙，但显然本作者暂时没有这个功能，所以只能迂回一下，安装谷歌上网助手`Ghelper_1.4.6.beta.zip`，通过谷歌帐号，在浏览器中安装这个插件就可以访问部分外部地址。当然有时间和帐号的限制。此处仅暂时用于这个Package Control包的下载。

三、离线安装Package Control

下载包：`Package Control.sublime-package`

> 1. Preferences -> Browse Packages (此时会打开**Packages**的文件夹，'.../Sublime Text 3/Packages')
>
> 2. 访问上级目录下的Installed Packages('.../Sublime Text 3/Installed Packages/')，并把如上安装包包存在该目录中。

如上操作后，软件会自行加载这个包，约5秒左右，我们就可以在`Preferences `中看到`Packages Setting 和 Packages Control`。

但是此时依然不能正常下载插件。需要执行第四步

四、修改用户文件

文件：`channel_v3.json`

保存该文件到一个安全目录(不包含中文目录)，例：

```
D:\\SublimeTextFile\\channel_v3.json
```

> Preferences -> Packages Setting ->Packages Control -> Setting User

会打开`Package Control.sublime-settings`文件

```json
// 原
{
	"bootstrapped": true
}
// 添加 channel_v3.json 后,如下
{
	"bootstrapped": true,
	"channels":
	[
		"D:\\SublimeTextFile\\channel_v3.json"
	],
}
```

如此就可以正常的下载插件了。

### 1.1 汉化

- 按ctrl+shift+p,调出隐藏搜索窗口
- 在搜索框输入“install”,点击第一个匹配项“install package”,
- 搜索插件`ChineseLocalizations`然后安装即可

