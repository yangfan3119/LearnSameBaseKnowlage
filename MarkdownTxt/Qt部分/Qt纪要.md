## Qt纪要

### 一、记录说明

#### 1.1 零散前叙

编写Qt应用我们需要有Qt库、编译器（vs和gcc）、调试器（gdb），最后还需要Qt Creator这一IDE将它们都整合到一起为我们所用。

---

g++和gcc的区别：

编译阶段是相同的，连接阶段g++默认链接c++库，gcc没有。所以一般情况下用gcc编译c文件，用g++编译cpp文件。但是也可以用gcc编译cpp文件，但后面需要加一个选项-lstdc++，作用时链接c++库还可以用g++编译c文件。

---

Qt开发的基本思路：Qt终端的创建编译运行项目

```mermaid
graph LR
A[项目创建]-->B[源码编译]
B-->C[程序运行]
C-->D[发布程序]
```

---

创建一个工程后，例如创建Helloworld工程后的文件列表，工程选择的继承基类为：**QDialog**

| 文件                | 说明                                                         |
| ------------------- | ------------------------------------------------------------ |
| helloworld.pro      | 项目文件，包含项目的组织方式、编译方式、链接等。             |
| helloworld.pro.user | 包含了与用户相关的项目信息，**多数情况下更换编译环境需要删掉这个重新本地创建** |
| hellodialog.h       | 新建的HelloDialog类的头文件                                  |
| hellodialog.cpp     | 新建的HelloDialog类的源文件                                  |
| main.cpp            | 项目运行主函数入口                                           |
| hellodialog.ui      | 设计师设计的界面，对应的是界面文件                           |

---

**终端下使用命令行创建、编译、运行项目**

```sh
#进入项目目录下---路径不能有中文
#1. 编译ui文件，使用uic编译工具，从ui文件生成头文件
uic -o ui_hellodialog.h hellodialog.ui
#2. 构件.pro文件，使用qmake -project命令来生成pro工程文件。
#3. 在.pro文件最后边添加一行代码
Qt += widgets 
#此处可能出错，因为Qt4不兼容，因此可以使用另一句
greatherThan(QT_MAJOR_VERSION,4):QT += widgets
#4. 命令行输入qmake，生成用于编译的Makefile文件
qmake
#运行后生成三个文件连个目录
#Dir:	debug	release
#File:	Makefile(包含编译信息)	Makefile.Debug	Makefile.Release
#5. 编译程序
mingw32-make -f Makefile.Debug
```

从命令行的编译过程，可以看到，ui文件的作用是使用设计师程序做界面的相关设定，生成***.ui**文件，然后由uic命令生成g++环境下可以识别的**.h**文件。即此就整合了视图资源和代码的集合。

再有通过minGW的qmake命令，可以生成工程文件用来组织编译以及资源(库文件)整合。最终生成需要的程序

---

#### 1.2 Qt发布说明

debug版本和release版本区别。一般发布release版本

**图标添加：**

```.pro文件中
//.pro文件中添加
RC_ICONS = myico.ico
```

**创建程序文件夹：**

编译成exe程序后，在其他的win环境下并不能直接运行，因为缺少必要的库文件，因此必须添加相关连的库文件。此处可以使用MinGW自带的命令完成

1. exe文件移到一个空文件夹中
2. 打开MinGW终端，cd到程序所在目录下
3. 键入命令**windeployqt  hello.exe**，即可自动复制依赖库文件到该目录下。
4. **把程序用到的本地资源移植到该目录下，包括：字体，图片，文本等等。否则报错**

---

#### 1.3 信号与槽关联

1. **显示关联**

   ```c++
   connect(btn,SIGNAL(clicked()),this,SLOT(btnClicked()));
   ```

2. **自动关联**

   ```c++
   //通过命名规范实现
   void on_<窗口部件名称>_<信号名称>_(<信号参数>)；
   例如：
   void on_btn_clicked();
   //如上自动关联失败则需要调用如下函数，在类构造函数中调用
   QMetaObject::connectSlotsByName(this);
   ```

---



























