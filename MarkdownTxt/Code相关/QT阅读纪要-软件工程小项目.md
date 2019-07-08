### [阅读纪要——软件工程小项目技术总结](https://blog.csdn.net/qq78442761/column/info/14442)

---

#### 1.数据库相关

```c++
//mysql断开连接
QString sqlquery = "exit";
sql->setQuery(sqlquery);
```

```mysql
# mysql 查询前10条
SELECT * FROM rasp_collgather LIMIT 0,10;
SELECT id,g_name,dates,remask_tip FROM rasp_collgather LIMIT 0,5;
```

**QSqlTableModel**提供了一个可读写单张SQL表的可变及数据模型。

``` c++
# QSqlTableModel的使用
void QSqlQueryModel::setQuery ( const QSqlQuery & query );
void QSqlQueryModel::setQuery ( const QString & query, const QSqlDatabase & db = QSqlDatabase() );
# 关于该model和数据库的链接部分如如下想法：
# 1. 使用QSqlQuery加载时，则db必须在QSqlQuery中设置。
# 2. 使用QString时，该类会自动从本地提取一个db数据库，即默认的master数据库。
```

*关于QSqlDatabase的猜想：*

*1. 默认创建的应该为一个主查询句柄，可以支撑QSql的各种其他体系查询，比如默认的情况下直接用QSqlQuery创建查询也没关系。只要在使用前成功的创建并打开数据库。*

```c++
db = QSqlDatabase::addDatabase("QMYSQL");
# 默认主数据库链路的创建
# 可以支撑默认的查询语句
例如：
1.  QString sqlquery = "SELECT * FROM rasp_collgather LIMIT 0,10;";
	QSqlQueryModel *model = new QSqlQueryModel();
    model->setQuery(sqlquery);	//可以成功执行
2.	QSqlQuery que;
    que.exec(sqlquery)；	//可以成功执行
```

*2. 多链路数据库时可以使用添加链路名称的形式来创建非默认链接，此时在默认情况下的查询等操作无法完成，必须加上创建的非默认数据库。***注意：该形式下每一次操作必须加上db，且创建的对象不具有绑定该数据库的功能**

```c++
db = QSqlDatabase::addDatabase("QMYSQL", "MysqlName");
# 自定义数据库链路的创建，无法支撑默认的数据库相关类的查询等操作
例如：
1.  QString sqlquery = "SELECT * FROM rasp_collgather LIMIT 0,10;";
	QSqlQueryModel *model = new QSqlQueryModel();
    model->setQuery(sqlquery);	//不可以执行
	model->setQuery(sqlquery, db);	//可以执行
2.	QSqlQuery que;
    que.exec(sqlquery)；	//可以成功执行
	QSqlQuery que(db);
    que.exec(sqlquery);	//可以执行
```

**QSqlTableModel**可以配合QT自带的相关类操作：**QTableView、QListView等**

```c++
// 自定义设置，该设置可以绑定该model
QTableView *tbview = new QTableView();
tbview->setModel(model);	//如需解绑使用setModel(NULL)即可

// model 为QSqlTableModel
    model->setQuery(sqlquery);
    model->setHeaderData(0,Qt::Horizontal,"编号");
    model->setHeaderData(1,Qt::Horizontal,"组名");
    model->setHeaderData(2,Qt::Horizontal,"日期");
    model->setHeaderData(3,Qt::Horizontal,"备注");

// 完成后即可进行Show操作
tbview->show();		
//当然不进行该操作也是可以的，其实绑定后执行model的Set操作即会更新该Table
```

> 绑定QTableView类，有一个注意点是：两个Tab时，Tab1,Tab2同时绑定一个model时，当model执行sql查询语句或者其他语句时，Tab1和Tab2同时刷新。因此如果有不同表需要使用，请绑定不同的model即可。

QSqlQueryModel是一个基于SQL查询的只读模型：

```c++
// model执行完Query语句后读取数据可通过如下方式读取。
for (int i = 0; i < model.rowCount(); ++i) 
{
     int id = model.record(i).value("id").toInt();
     QString name = model.record(i).value("name").toString();
     qDebug() << id << name;
 }
```

**延伸：**

1. QSqlQueryModel提供一个基于SQL查询的<span style="color:red;" >只读模型</span>。

2. QSqlTableModel提供一个以此只能对一个SQL表进行操作的<span style="color:red;">可读可写模型</span>

```c++
QSqlTableModel model;
model.setTable("employee");
model.setFilter("salary > 50000");
model.setSort(2, Qt::DescendingOrder);
model.select();

for (int i = 0; i < model.rowCount(); ++i) {
    QString name = model.record(i).value("name").toString();
    int salary = model.record(i).value("salary").toInt();
    qDebug() << name << salary;
}
// 同样可以对QSqlTableModel进行写操作
for (int i = 0; i < model.rowCount(); ++i) {
    QSqlRecord record = model.record(i);
    double salary = record.value("salary").toInt();
    salary *= 1.1;
    record.setValue("salary", salary);
    model.setRecord(i, record);
}
model.submitAll();
```

3. QSqlRelationalTableModel扩展了QSqlTableModel来提供了对外键(foreign key)的支持。一个外键是一个表中的一个字段与另一个表中的主键(primary key)字段之间的一一映射。

```c++
model->setTable("employee"); 
model->setRelation(2, QSqlRelation("city", "id", "name"));
model->setRelation(3, QSqlRelation("country", "id", "name"));
```

#### 2. XML文件及运行外部程序

作者使用了XML文件来放置外部程序的路径：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<program>
	<pro id="1">
    	<title>MYSQL</title>
        <dir>D:\\SQLdd\\SQL.exe</dir>
    </pro>
    <pro id="2">
    	<title>OtherFun</title>
        <dir>D:\\Func\\Func.exe</dir>
    </pro>
</program>
```

```c++
#include <QDomDocument>
#include <QDomNode>
// 作者通过QDomDocument、 QDomNode来读取XML的各个节点，回去程序名以及路径
#include <QProcess>
// 通过 QProcess 中的 start 函数来运行外部程序。
```

**延伸：**

- *关于 QProcess的使用：*

  > 一、启动外部程序的两种方式
  > 　　1）一体式：void QProcess::start(const QString & program,const QStringList &arguments,OpenMode mode = ReadWrite)
  > 　　　　外部程序启动后，将随主程序的退出而退出。
  > 　　2）分离式：void QProcess::startDetached(const QString & program,const QStringList & arguments,const QString&workingDirectory=QString(),qint64 *pid =0)
  > 　　　　外部程序启动后，当主程序退出时并不退出，而是继续运行。
  > 二、启动之前需要做的工作：
  > 　　启动一个外部程序，需要传递外部程序的路径和执行参数，参数用QStringList来带入。
  > 　　1）设置路径
  > 　　　　void QProcess::setProgram(const QString & program)
  > 　　2)设置参数【可选】
  > 　　　　void QProcess::setArguments(const QStringList & arguments)
  > 　　3）启动
  > 　　选择启动函数（两种方式）

#### 3. Qt状态栏的设置

实则是一个*StatusBar->addWigget()*即可实现，关于时间的刷新还是用的 *QTimerEvent* 来完成，每隔2s来刷新。

比较简单此处不详述。

#### 4. socket环境搭建

作者使用了虚拟机环境，使用**Vmware虚拟机**创建windows 7的环境。网络上使用NAT的模式（与虚拟机共享主机的IP地址）。

同时通过配置虚拟机的网络环境：勾选使用本地DHCP服务将IP地址分配给虚拟机，并设置子网IP和子网掩码。

关闭本地和虚拟机系统的防火墙，通过ping来完成网络校验。

该项目客户端放在虚拟机上，而服务器放在本地机器上。

#### 5. TCP服务器和客户端的搭建

**服务器的搭建**，主要使用QTcpServer做服务器，QTcpSocket做连接。关键代码如下：

```c++
// 自定义server继承与QTcpServer
class MyServer : public QTcpServer
{
// 用于记录Tcpsocket的链路。
QList<TcpClientSocket*> tcpClientSocketList;
// 添加信号，从客户端接收的信息对内上传
signals:
    void updateServer(QString,char*,int);
// 创建槽函数，用于绑定socket的接收到的信息
public slots:
    void updateClients(QString, char *, int);
    void slotDisconnected(int);	//关闭链接
// 重写服务器端监听端口和ip后，主动连接的链路响应。
protected:
    void incomingConnection(int socketDescriptor);
}
```

```c++
// 亮点:
// 每一次连接即对socket设置一次Descriptor，实际上为每一次链接Server生成的id
tcpClientSocket->setSocketDescriptor(socketDescriptor);
//然后通过底层socket在断开时发送的断开信号来管理QList<TcpClientSocket*>，socket寄存容器。
```

**客户端的搭建**，还是很简单的，创建socket，连接即可，完成接收和发送的绑定即可。

```c++
// 亮点：
// 使用QHostAddress来创建ip链路地址，然后连接。
if(ServerIP->setAddress(ip))
    // 为合法的ip地址
else
    // 为不合法的ip地址
// 该种方式应该也可以用来加载IPV6的地址。此处比直接用QString的方式链接好很多，可以做到标准化选择。
```

#### 6. 加解密——使用3DES

*在日常设计及开发中，为确保数据传输和数据存储的安全，可通过特定的算法，将数据明文加密成复杂的密文。目前主流加密手段大致可分为单向加密和双向加密。*

- 单向加密：通过对数据进行摘要计算生成密文，密文不可逆推还原。算法代表：Base64，MD5，SHA;

- 双向加密：与单向加密相反，可以把密文逆推还原成明文，双向加密又分为对称加密和非对称加密。
  - 对称加密：指数据使用者必须拥有相同的密钥才可以进行加密解密，就像彼此约定的一串暗号。算法代表：DES，3DES，AES，IDEA，RC4，RC5;
  - 非对称加密：相对对称加密而言，无需拥有同一组密钥，非对称加密是一种“信息公开的密钥交换协议”。非对称加密需要公开密钥和私有密钥两组密钥，公开密钥和私有密钥是配对起来的，也就是说使用公开密钥进行数据加密，只有对应的私有密钥才能解密。这两个密钥是数学相关，用某用户密钥加密后的密文，只能使用该用户的加密密钥才能解密。如果知道了其中一个，并不能计算出另外一个。因此如果公开了一对密钥中的一个，并不会危害到另外一个密钥性质。这里把公开的密钥为公钥，不公开的密钥为私钥。算法代表：RSA，DSA。

**3DES算法：**是三重数据加密，且可以逆推的一种算法方案。但由于3DES的算法是公开的，所以算法本身没有秘钥可言，主要依靠唯一秘钥来确保数据加解密的安全。目前为止，无人能破解3DES。（也称为EDSede,加密-解密-加密的过程）。EDS算法执行三次

此处作者的代码如下：（作者使用的是一个**libdes**的第三方库）

```c++
// 加密过程，三次加密的秘钥
char key1[] = "qwertyui";
char key2[] = "asdfghjk";
char key3[] = "zxcvbnm";

// 加密，Code为libdes第三方库
Code des1(key1);
Code des2(key2);
Code des3(key3);
QString d2=QString::fromUtf8(UserNameData);
des1.EncryptName(UserNameData, UserNameData);	//第一次加密
des2.DevryptName(UserNameData, UserNameData);	//第二次解密
des3.EncryptName(UserNameData, UserNameData);	//第三次加密

```

```c++
// 解密过程，三次加密的秘钥
char key1[] = "qwertyui";
char key2[] = "asdfghjk";
char key3[] = "zxcvbnm";

// 解密，Code为libdes第三方库，逆执行加密流程
Code des1(key1);
Code des2(key2);
Code des3(key3);
des3.DevryptName(temp1,temp1);	//逆推第三次加密过程
des2.EncryptName(temp1,temp1);	//逆推第二次解密过程
des1.DevryptName(temp1,temp1);	//逆推第一次加密过程
```

```sequence
title: 加解密基本流程
输入->明文: Str转byte
明文->密文: key1做DES加密
密文->明文: key2做DES解密
明文->密文: key3做DES加密
密文->输出: 输出加密结果

输入->密文: 密文字符串转为byte
密文->明文: key3做DES解密
明文->密文: key2做DES加密
密文->明文: key1做DES解密
明文->输出: 输出解密结果
```

此处唯一的疑惑是关于**libdes中的EDS解密部分代码**。或许以后的实践中需要找到QT下可以使用DES加密库或者3DES加密库。由于版本问题可能不好找，因此此处贴出[DES算法详解，留待后用](https://blog.csdn.net/tandesir/article/details/8044681)。

#### 7. 界面重画

作者此处介绍了两种技术：1. 添加背景图以及取消边框。2. 鼠标拖动窗口。

##### 1. 添加背景图——使用的是重绘事件完成

```c++
//取消标题栏的显示
setWindowFlags(Qt::FramelessWindowHint);

//背景透明
setAttribute(Qt::WA_TranslucentBackground);
m_backGroundImage=new QPixmap();
m_backGroundImage->load(":/image/login.png");

// 窗口绘制——背景重绘
void Login::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);
    QRect frameRect = rect();
    painter.drawPixmap(frameRect, *m_backGroundImage);
}
```

*延伸：关于**setAttribute()**函数说明。*

**setAttribute()函数是用来改变窗口属性的。**

**QT::WA_TranslucentBackground：**设置窗口背景透明。

**QT::WA_DeleteOnClose：**设置窗口上所有new出来的控件自销毁的操作。对窗口本身而言必须为指针，否则还造成二次销毁报错。

**QT::WA_ShowModal：**窗口模态装换。（this->setAttribute(Qt::WA_ShowModal, true);实测有效)

*模态对话框就是指在子对话框弹出时，焦点被强行集中于该子对话框，子对话框不关闭，用户将无法操作其他的窗口。*

*非模态相反，用户仍然可以操作其他的窗口，包括该子对话框的父对话框。*

##### 2. 鼠标拖动

已实现过此处直接上代码参考：

```c++
void Login::mousePressEvent(QMouseEvent *event)
{
    // 只响应左键
    if (event->button() == Qt::LeftButton)
    {
        m_dragging = true;
        m_startPosition = event->globalPos();
        m_framePosition = frameGeometry().topLeft();
    }
}
void Login::mouseMoveEvent(QMouseEvent *event)
{
    // 只响应左键
    if (event->buttons() == Qt::LeftButton)
    {
        if(m_dragging)
        {
            // delta 相对偏移量,
            QPoint delta = event->globalPos() - m_startPosition;
            // 新位置：窗体原始位置  + 偏移量
            move(m_framePosition + delta);
        }
    }
}
void Login::mouseReleaseEvent ( QMouseEvent * event )
{
    // 结束dragging
    m_dragging = false;
}
```



















