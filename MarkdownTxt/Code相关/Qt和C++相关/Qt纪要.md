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



### 二、Qt Designer

#### 2.1 界面使用

1. 先做控件的拖拽创建。完成基本的控件功能。
2. 做控件的关联整理，哪些是成行的，哪些式成列的。哪些又是呈现网格的。理顺关系
3. 做控件大小的调整。
4. 做控件美化，使用css格式插入。
5. 关联主程序的业务逻辑和数据处理。

*注意：*做控件美化时，可以现在Designer中创建希望拥有的格式，在集合整理到统一的css文件中即可。

#### 2.2 关键点记录

- 窗口部件
  1. 添加控件：从左侧的部件列表中选中需要的部件，拖到右侧的设计窗口上就可以了
  2. 复制控件：按住ctrl，鼠标点击要复制的控件，按住向外拉，就得到了复制的控件
  3. 删除控件：鼠标点击要删除的控件，右键删除或按delete键
  4. 选中多个控件：鼠标向外拉出一个矩形，覆盖要选中的控件，或者按住ctrl，依次点击要选中的控件
  5. 控件位置，大小等相关属性：详见属性编辑器和布局

- 属性编辑器：可以用来编辑控件的相关属性，有从父类Widget继承而来的属性，也有自己控件独特的属性，使用时比较方便。

- 布局管理器的使用： 

  Qt 的布局管理器负责在父窗口部件区域内构建子窗口部件。这些管理器可以使其中 的窗口部件自动定位并重新调整子窗口部件、保持窗口部件敏感度最小化的变化和默认尺 寸，并可在内容或文本字体更改时自动重新定位。在 Qt Designer 中，完全可以使用布局管理器来定位控件。

  > 1. 布局类的继承关系： QLayout 类是 Qt 的几何管理器的基类，它派生自 QObject 类和 QLayoutItem 类，是一 个抽象基类，必须被派生类所重新实现。它的派生类主要有 QBoxLayout， QGridLayout， QFormLayout 以及 QStackedLayout。而 QBoxLayout又派生出QHBoxLayout和QVBoxLayout2个子类。除了这些内建布局器，常用的还有QSplitter分裂器布局，QSpacerItem弹簧。
  >
  > 2. 布局管理器的属性设置：以下图QVBoxLayout为例，layoutLeftMargin，layoutRightMargin。。。这4个属性用于设置布局内的控件距布局边缘(上，下，左，右)的空白距离。layoutSpacing这个属性用于设置布局内的控件之间的空白距离。还有其他一些属性，这里不再列举。 

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\20170927141544779.png)

> 3. 顶级布局：在将所有控件布局完成后，还需要点一下主窗口，然后再选择一种布局，称之顶级布局。如果不设顶级布局的话，控件无法与主窗口建立起联系，这样在主窗口大小改变时控件不能随之变化。

常见布局器的使用及效果

| 布局               | 说明                                                         | 效果                                                         |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Box水平或垂直布局  | 将选中的界面元素置于一个水平或垂直布局中                     | ![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\20170925181418391.png) |
| Grid栅格布局       | 将选中的界面元素置于一个栅格布局中，每个控件占据一块方形格子 | ![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\20170925181730644.png) |
| Form表单布局       | 将控件以两列的形式布局在表单中。左列标签label，右列输入控件如LineEdit | ![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\20170925182542136.png) |
| Splitter分裂器布局 | 创建一个分裂器水平或垂直布局，选中的控件长度可由用户在水平或垂直方向上拖动 | ![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\20170925183409358.png) |
| Spacer间隔布局     | 像弹簧一样，占据空白空间，用于限制控件扩展和控制控件之间间隔 | ![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\20170925183829736.png) |

> 4.**窗口控件的大小控制** 
>
> 要想在布局时和主窗口大小改变时控制控件的大小，QWidget里有一些方法如下： 
> - sizeHint：这个属性所保存的QSize的值是一个推荐这个窗体尺寸的一个值，sizeHint() 函数会返回这个推荐值 
> - minimumSizeHint：与sizeHint一样，只不过这个属性保存的是推荐这个窗体最小尺寸的一个值 
> - minimumSize和maximumSize：这2个属性保存的是窗体的最小尺寸和最大尺寸，窗体的尺寸被限制在这2个尺寸之间，可以自己设置。 
> - sizePolicy：这个属性用于设置窗体在 水平/垂直 方向上的伸展属性，在窗体没有被布局的情况下是不起作用的，QSizePolicy::Policy 枚举值有如下几个：

| 属性值                        | 描述                                                         |
| ----------------------------- | ------------------------------------------------------------ |
| QSizePolicy::Fixed            | widget 的实际尺寸只 参考 sizeHint() 的返回值，当主窗口在水平/垂直方向上大小改变时它不能随之变化 |
| QSizePolicy::Minimum          | 可以随主窗口伸展收缩，不过widget尺寸不能小于sizeHint()       |
| QSizePolicy::Maximum          | 可以随主窗口伸展收缩，不过widget尺寸不能大于sizeHint()       |
| QSizePolicy::Preferred        | 可以随主窗口伸展收缩，但在争夺空白空间上没有优势             |
| QSizePolicy::Expanding        | 可以随主窗口伸展收缩，在布局时它会尽可能多地去获取额外的空间，也就是比 Preferred 更具优势 |
| QSizePolicy::MinimumExpanding | 可以随主窗口伸展收缩，不过widget尺寸不能小于sizeHint(),同时它比 Preferred 更具优势去获取额外空间 |
| QSizePolicy::Ignored          | 忽略 sizeHint() 的作用                                       |

	#### 2.3 实际操作注意点

1.  在已有代码中添加Ui时注意Ui库写法。==**Ui**==

```c++
namespace Ui {					// 重点
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();


private slots:
    
    void on_BtnTest_clicked();

    void on_BtnDesign_clicked();

private:
    Ui::MainWindow *ui;			// 重点
};
```

```c++
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)		// 重点
{
    ui->setupUi(this);			// 重点
}

MainWindow::~MainWindow()
{
    delete ui;					// 重点
}
```

2. 控件名称的改变，会导致槽函数名称的变化，使得原有名称无法关联到控件，因此需做处理。



#### 2.4 样式表 StyleSheet

[图文讲解：QT样式表StyleSheet的使用与加载](https://blog.csdn.net/qq_31073871/article/details/79943093)

[Qt 之 样式表的使用——设置样式的方法](https://blog.csdn.net/goforwardtostep/article/details/60884870)

[Qt常用QSS集合](https://www.jianshu.com/p/2ecf26464f78)

[QT自定义控件大全](https://blog.csdn.net/qq_19004627/article/details/79736557)



### 三、其他

#### 3.0 鼠标指针Cursor

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\6157840_1325147073H3kN.png)

```c++
Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);
    setCursor(QCursor(Qt::OpenHandCursor));
}
```

#### 3.1 表格相关

```css
QTableView , QTableWidget{
    selection-background-color:#44c767;
    background-color:white;/*整个表格的背景色，这里为白色*/
    border:1px solid #E0DDDC;/*边框为1像素，灰色*/
    gridline-color:lightgray;/*这个是表格的格子线的颜色，为亮灰*/
}
/*这里是表格表头样式*/
QHeaderView::section{
    background-color:white;/*背景色 白色*/
    border:0px solid #E0DDDC;/*先把边框宽度设为0，即隐藏所有表头边框*/
    border-bottom:1px solid #E0DDDC;/*然后只显示下边框，因为上边框和左右边框是整个Table的边框，都显示会有2px的边框宽度*/
    height:20px;/*表头高度*/
}
```

```css
QScrollBar:vertical{        //垂直滑块整体  
    background:#FFFFFF;  //背景色  
    padding-top:20px;    //上预留位置（放置向上箭头）  
    padding-bottom:20px; //下预留位置（放置向下箭头）  
    padding-left:3px;    //左预留位置（美观）  
    padding-right:3px;   //右预留位置（美观）  
    border-left:1px solid #d7d7d7;
}//左分割线  
QScrollBar::handle:vertical{//滑块样式  
    background:#dbdbdb;  //滑块颜色  
    border-radius:6px;   //边角圆润  
    min-height:80px;
}    //滑块最小高度  
QScrollBar::handle:vertical:hover{//鼠标触及滑块样式  
    background:#d0d0d0;
} //滑块颜色  
QScrollBar::add-line:vertical{//向下箭头样式  
    background:url(:/images/resource/images/checkout/down.png) center no-repeat;
}
QScrollBar::sub-line:vertical{//向上箭头样式  
    background:url(:/images/resource/images/checkout/up.png) center no-repeat;
} 

QScrollBar:horizontal{
    background:#FFFFFF;
    padding-top:3px;  
    padding-bottom:3px;  
    padding-left:20px;  
    padding-right:20px;
}  
QScrollBar::handle:horizontal{  
    background:#dbdbdb;  
    border-radius:6px;  
    min-width:80px;
}  
QScrollBar::handle:horizontal:hover{  
    background:#d0d0d0;
}  
QScrollBar::add-line:horizontal{  
    background:url(:/images/resource/images/checkout/right.png) center no-repeat;
}  
QScrollBar::sub-line:horizontal{  
    background:url(:/images/resource/images/checkout/left.png) center no-repeat;
} 
```

```css
QHeaderView::down-arrow { 
	subcontrol-position: center right;
	image: url(:/sort_down_arrow.png);
	padding-right: 8px;
}
 
QHeaderView::up-arrow { 
	subcontrol-position: center right;
	image: url(:/sort_up_arrow.png);
	padding-right: 8px;
}
```

**分页样式**

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\20160130202706619)

##### 3.1.1 表列宽

```c++
ui->tableWidget->horizontalHeader()->setResizeMode(0, QHeaderView::ResizeToContents);
ui->tableWidget->horizontalHeader()->setResizeMode(2, QHeaderView::Stretch);
ui->tableWidget->horizontalHeader()->setResizeMode(3, QHeaderView::ResizeToContents);
```

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\1558002741408.png)

##### 3.1.2 表设置

```c++
table_widget->horizontalHeader()->setStretchLastSection(true); //设置充满表宽度
table_widget->verticalHeader()->setResizeMode(QHeaderView::ResizeToContents);
table_widget->verticalHeader()->setDefaultSectionSize(10); //设置行高
table_widget->setFrameShape(QFrame::NoFrame); //设置无边框
table_widget->setShowGrid(false); //设置不显示格子线
table_widget->verticalHeader()->setVisible(false); //设置垂直头不可见
table_widget->setSelectionMode(QAbstractItemView::ExtendedSelection);  //可多选（Ctrl、Shift、  Ctrl+A都可以）
table_widget->setSelectionBehavior(QAbstractItemView::SelectRows);  //设置选择行为时每次选择一行
table_widget->setEditTriggers(QAbstractItemView::NoEditTriggers); //设置不可编辑
table_widget->horizontalHeader()->resizeSection(0,150); //设置表头第一列的宽度为150
table_widget->horizontalHeader()->setFixedHeight(25); //设置表头的高度

table_widget->setStyleSheet("selection-background-color:lightblue;"); //设置选中背景色

table_widget->horizontalHeader()->setStyleSheet("QHeaderView::section{background:skyblue;}"); //设置表头背景色



//设置水平、垂直滚动条样式

table_widget->horizontalScrollBar()->setStyleSheet("QScrollBar{background:transparent; height:10px;}"
                                                   "QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}"
                                                   "QScrollBar::handle:hover{background:gray;}"
                                                   "QScrollBar::sub-line{background:transparent;}"
                                                   "QScrollBar::add-line{background:transparent;}");

table_widget->verticalScrollBar()->setStyleSheet("QScrollBar{background:transparent; width: 10px;}"
                                                 "QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}"
                                                 "QScrollBar::handle:hover{background:gray;}"
                                                 "QScrollBar::sub-line{background:transparent;}"
                                                 "QScrollBar::add-line{background:transparent;}");
```

