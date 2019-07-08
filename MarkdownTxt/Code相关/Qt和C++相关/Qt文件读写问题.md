---
typora-copy-images-to: ..\mdPic
---

## Qt文件的读写操作

### 一、Qt文件读写基本描述

#### 1.1 QFile实现文件的读写

```c++
QFile(const QString & name)
QFile(QObject *parent)
QFile(const QString & name, QObject *parent)
/*
1. 从QFile的构造函数我们知道，可以直接在调用构造函数的时候就传递文件名给QFile类
2. 对于先生成QFile对象然后调用setFileName()方法来设置文件，其中文件名中的路径分隔符要求必须是'/',其他分隔符QFile不支持。
*/
```

```c++
/*基本功能*/
copy()			//复制文件
exists()		//检查文件是否存在
open()			//打开文件
remove()		//删除文件
rename()		//修改文件名
setFileName()	//设置文件名
size()			//文件大小
pos()			//文件光标当前位置
seek()			//设置文件光标位置
atEnd()			//判断当前是否为文件尾
read()			//读取文件内容
close()			//关闭文件
```

#### 1.2 QFile中关于QIODevice的宏定义

| 模式       | 值     | 描述                                                         |
| ---------- | ------ | ------------------------------------------------------------ |
| NotOpen    | 0x0000 | 不打开                                                       |
| ReadOnly   | 0x0001 | 只读方式                                                     |
| WriteOnly  | 0x0002 | 只写方式，不存在自建                                         |
| ReadWrite  | 0x0003 | 读写方式(ReadOnly\|WriteOnly)                                |
| Append     | 0x0004 | 数据写入文件末尾                                             |
| Truncate   | 0x0008 | 打开文件前被截断，源数据丢失，覆盖                           |
| Text       | 0x0010 | 读的时候，文件结束位转为‘\n’，写的时候转为本地模式。例:win32位时结束位为‘\r\n’ |
| UnBuffered | 0x0020 | 不缓存                                                       |

#### 1.3 基本实现Qt

```c++
void ReadTxtFile()
{
    QFile file("L:/qtDir/file/readIt.txt");
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    
    QByteArry t = file.readAll();
    TxtLable.setText(QString(t));//bytes类型读取，并转为QString类型
    file.close();
}
```

```c++
void WriteTxtFile(QString tx)
{
    QFile file("L:/qtDir/file/readIt.txt");
    file.open(QIODevice::WriteOnly | QIODevice::Text);
    file.write(tx.toUtf8());//写入bytes类型
    file.close();
}
```

### 二、流数据QTextStream的引入

#### 2.1 QTextStream说明

​	一般用于操作二进制文件。流数据的模式也是二进制类型文件常用的操作。类似的QDateStream，此处QTextStream是纯文本文件的操作。至于其他的XML、HTML等也可以有QTextStream操作，但此处QTextStream的引入是通过Qt的文本文件读写而产生的，此处不做延伸描述

**QtextStream的类说明：**

1. 自动将Unicode编码同操作系统的编码进行转换，所以此处无需额外操作(使用SetCodec()做编码设定)
2. 对不同系统下的换行符自动做转换，统一使用'\n'使用，当然也可以使用readline来自动获取每一行的数据。
3. 使用16位的QChar作为基础的数据存储单位
4. 支持C++de 标准类型，如int等
5. 读取操作时，标记为为段首，所以每一次读取都会刷新标记。写入时则在文件末尾处标记，写入字符也为段尾位置。

```c++
/*常用函数*/
//读取txt文件maxlen个字符。“Hello”,read(1)=>'H',read(1)=>'e'...
QString read(qint64 maxlen);
//读取一整行文档
QString readLine(qint64 maxlen=0);
//读取全部文档
QStirng readAll();
//重定位
bool seek(qint64 pos);
```

### 三、实际问题说明

#### 3.1 Log的文件多次打开关闭问题

因为Qt软件中增加日志系统，所以在程序的各个模块中都有标记或错误等信息抛出并记录到本地文件中。但在实际操作中，往往需要进行短小的日志信息记录下来，例如开机后的版本说明。每一次的写入操作均会进行一次完成的文件读取和写入操作。为提高系统的实效性，特此研究。

#### 3.2 文件打开关闭的耗时测试

```c++
//每一次打开写入再关闭时代码如下
void WriteAll(int Ct)
{
    QString pathname = QString("%1/WriteAll.txt").arg(SysDir);

    int count = Ct;
    while (count-->0) {
        QFile file(pathname);
        file.open(QIODevice::WriteOnly | QIODevice::Append | QIODevice::Text);

        QTextStream inx(&file);
        inx<<"I'm OK; "<<count;
        inx.flush();
        file.close();
    }
}
/*
Ct: 1000，DeltaT = 0.249
Ct: 10000，DeltaT = 2.556	/	2.418
*/
```

```c++
//每一次打开写入再关闭时代码如下
void WriteOnce(int Ct)
{
	QString pathname = QString("%1/WriteOnce.txt").arg(SysDir);

    int count = Ct;
    QFile file(pathname);
    file.open(QIODevice::WriteOnly | QIODevice::Append | QIODevice::Text);

    QTextStream inx(&file);
    while (count-->0) {
    inx<<"I'm OK; "<<count;
    }
    inx.flush();
    file.close();
}
/*
Ct: 1000，DeltaT = 0.06
Ct: 10000，DeltaT = 0.022	/	0.005
*/
```

结论：

1. 每一次打开关闭确实占用很多时间
2. 时间差在数量级上相差巨大，越是巨大的写入需求，差异越明显。
3. 在一次打开，N次写入的过程中，显然发现写入所占用的时间几乎可以忽略不计，而占用时间的是文件在创建过程所花费的时间。
4. 以1000条为基准的话，即使同一时刻需要1000条Log的写入，依然只需要0.249s，即意味着在无特定需求的时候，不用刻意改变一打开一写入一关闭的模式。

#### 3.3 文件打开过程中的完整写入过程观察

```c++
//使用QFile打开文件。
QFile fx(pathname);
if(!fx.open(QIODevice::WriteOnly | QIODevice::Append | QIODevice::Text))
{
    qDebug()<<"FileOpenError:"<<fx.errorString();
}
//打开文件后，其他指针不能重复打开，否则会报错，File（Addr） is already opened
//在外部系统中，也无法对文件做删除操作。但是可以打开，也可以写入其他内容。
```

```c++
QTextStream fxstream(&fx);
fxstream<<"I'm OK; "<<"\r\n";
fxstream.flush();
fx.close();
//以上所有操作均无法看出系统的额外操作。即在以上操作过程中，文件依然可以被打开，以及可以查看到文件中写入的实时内容。
//基本可以判断即使不做close操作文件依然不会造成内容丢失。至于其他额外的不安全时间暂时无法排查。
```

**注意：**在程序写入文件的过程中，从系统中对文件做其他操作出现如下问题：

| 操作              | 现象                                                         |
| ----------------- | ------------------------------------------------------------ |
| 外部删除          | 无法删除，提示文件已被打开无法操作                           |
| 外部写入内容A     | 文件打开时，位置自动移到末尾，并记录下位置指针，程序再写入内容B时，会按照字节长度逐步覆盖A。 |
| 外部修改-等长度时 | 因等长度的内容修改，使得当前程序的记录位置不会发生改变，因此程序继续写入后，不会发生异常，内容上不会产生任何问题。 |
| 外部修改-非等长度 | 因长度不同，造成程序的写入位置与修改后的段尾位置不一致，此时程序仍然会以记录下的位置来写入内容。两者中间使用空字节来替代，NUL |

简而言之，外部可修改但不能删除，修改后的文本，程序只会对标记位置之后的内容做**覆盖处理**，且位置之间出现空的情况，则**自动补齐**，补到标记位位置，然后继续写入内容。

