## 一、CRM

![1555572248650](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\1555572248650.png)

### 1. sqlite数据库的使用

```c++
// 可以保存为 *.db 文件
mDefaultDB = QCoreApplication::applicationDirPath() + "\\crm.db";
QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
db.setDatabaseName(mDefaultDB);
```

```c++
//使用QSqlQuery来执行sql语句
QSqlQuery sql_query;	
QString create_sql = "create table if not exists Customer (name varchar(100) primary key,remark varchar(200))"; //创建数据表

QString insert_sql = "insert into Customer values(\"%1\",%2,%3,%4,\"%5\",\"%6\",\"%7\",\"%8\",\"%9\",\"%10\",\"%11\")";    //插入数据

sql_query.prepare(create_sql); //创建表
if(!sql_query.exec()) //查看创建表是否成功
{
    qDebug()<<QObject::tr("Table Create failed");
    qDebug()<<sql_query.lastError();
}
```

### 2. 系统文件夹打开与定位

```c++
QString fileName;
fileName = QFileDialog::getOpenFileName(this,"打开文件","","Database Files(*.db)");
fileName = QFileDialog::getSaveFileName(this,"保存到文件","","Database Files(*.db)");
```

```c++
if(QFile::exists(fileName))	// 如果存在，则删除文件
	QFile::remove(fileName);
```

### 3. 额外窗口的打开

两种方式：1. 按钮触发后使用局部变量完成，完成添加数据操作。2.表格单项触发，完成更新数据操作。

即不同的打开方式对应不同的显示以及数据操作，此处分叙。

```c++
// mainwindow.cpp中如下
// 1. 按钮触发
void MainWindow::on_btnAdd_clicked()
{
    DlgItem dlg(NULL);	//新增时传入NULL数据
    connect(&dlg,&DlgItem::sigAddItem,this,MainWindow::slotAddItem);
    dlg.exec();
}
// 2. 表格双击触发
void MainWindow::on_tableView_doubleClicked(const QModelIndex &index)
{
    QString name = mModel->item(index.row(),0)->text();
    Customer *p = FindItem(name);
    if(p)
    {
        DlgItem dlg(p);	//修改时传入一组有效数据
        if(QDialog::Accepted == dlg.exec())
        {	// 更新表格数据
            mModel->item(index.row(),0)->setText(p->name);
            mModel->item(index.row(),1)->setText(Type2String(p->type));
            ...;

            DeleteFromDb(name);
            InsertToDb(p);
        }
    }
}
```

而在另一个窗口的操作和显示有如下分析：

```c++
// 构造函数区别
DlgItem::DlgItem(Customer* item,QWidget *parent) : QDialog(parent),ui(new Ui::DlgItem)
{
    ui->setupUi(this);
    mItem = item;
    if(mItem)	//显而易见item值的区别使得界面在构造中产生例区别
    {

    }
}
```

**此处引入：模式对话框和非模式对话框。**

> *非模式对话框*   是和同一个程序中其它窗口操作无关的对话框。在字处理软件中查找和替换对话框通常是非模式的来允许同时与应用程序主窗口和对话框进行交互。调用show()来显示非模式对话框。show()立即返回，这样调用代码中的控制流将会继续。在实践中你将会经常调用show()并且在调用show()的函数最后，控制返回主事件循环。

> 模式对话框	就是阻塞同一应用程序中其它可视窗口的输入的对话框：用户必须完成这个对话框中的交互操作并且关闭了它之后才能访问应用程序中的其它任何窗口。模式对话框有它们自己的本地事件循环。用来让用户选择一个文件或者用来设置应用程序参数的对话框通常是模式的。调用exec()来显示模式对话框。当用户关闭这个对话框，exec()将提供一个可用的 **返回值** 并且这时流程控制继续从调用exec()的地方进行。通常，我们连接默认按钮，例如“OK”到 accept() 槽并且把“Cancel”连接到reject()槽，来使对话框关闭并且返回适当的值。另外我们也可以连接done()槽，传递给它[Accepted](http://www.kuqin.com/qtdocument/qdialog.html#DialogCode-enum)或[Rejected](http://www.kuqin.com/qtdocument/qdialog.html#DialogCode-enum)。

显然，由上概念可知此处使用的即为模式对话框，在执行dlg.exec()后主程序阻塞。通过信号来更新数据，或者通过返回值来更新数据。

```c++
// Dialog中使用Accepted和rejected信号
void DlgItem::on_btnAdd_clicked()
{
    ...;
	accept();	// 返回 QDialog::Accepted 信号
}
void DlgItem::on_btnCancel_clicked() { reject(); }	// 返回 QDialog::Rejected 信号
```

### 4. 关于表格

**QTableView：**

```c++
// 初始化操纵
{
    QTableView* t = ui->tableView;
    t->setEditTriggers(QTreeView::NoEditTriggers);			//不能编辑
    t->setSelectionBehavior(QTreeView::SelectRows);			//一次选中整行
    t->setAlternatingRowColors(true);
    
    //引入 QStandardItemModel 操纵表格中的数据
    mModel = new QStandardItemModel(t);
    mModel->setHorizontalHeaderLabels( headers );
    
    // 关联 mModel 类指针
    t->setModel(mModel);
    
    // mModel的使用
    QList<QStandardItem*> items;
    QStandardItem* item1 = new QStandardItem(p->name);
    QStandardItem* item2 = new QStandardItem(Type2String(p->type));
    QStandardItem* item3 = new QStandardItem(Area2String(p->area));
    items.append(item1);
    items.append(item2);
    items.append(item3);
    mModel->appendRow(items);
    
    // 调整表格单列的宽度
    t->horizontalHeader()->resizeSection(i,200);
}
// 选中删除
{
    int row = ui->tableView->currentIndex().row();
    qDebug()<<"row = "<<row;
    QString name = mModel->item(row,0)->text();
    DeleteItem(name);

    mModel->removeRow(row);
}
```

mModel的使用主要为表格数据的操作。tableView用于信号和显示的操作。

**tableWidget**

```c++
ui->tableWidget->setRowCount(20);	//设置表格行
for(int i=0;i<20;i++)	//设置表格各个项
{
    ui->tableWidget->setItem(i,0,new QTableWidgetItem(""));
    ui->tableWidget->setItem(i,1,new QTableWidgetItem(""));
    ui->tableWidget->setItem(i,2,new QTableWidgetItem(""));
    ui->tableWidget->setItem(i,3,new QTableWidgetItem(""));
    ui->tableWidget->setItem(i,4,new QTableWidgetItem(""));
    ui->tableWidget->setItem(i,5,new QTableWidgetItem(""));
}
// 添加内容
ui->tableWidget->item(i,0)->setText(row[0]);
// 添加颜色
ui->tableWidget->item(i,0)->setBackground(Qt::red);
```

### 5. 关于数据过滤操作

```c++
//区域过滤
if(!mFilterArea.isEmpty())	// 过滤条件, 存在则进行判定是否为要求数据，是则通过，否则剔除
{
    if(mFilterArea != sArea)
    {
        continue;
    }
}
//省份过滤
if(!mFilterProvince.isEmpty())  
{
    if(mFilterProvince != sProvince)
    {
        continue;
    }
}
```

### 6. 关于QComboBox和QLabel

```c++
// 基本的清空选择操作 
void DlgItem::on_combo2_currentTextChanged(const QString &text)
{
    ui->combo3->clear();
    if(text == "华东")
    {
        ui->combo3->addItems(QStringList()<<"山东"<<"浙江"<<"江苏"<<"安徽"<<"上海"<<"福建");
    }
    else if(text == "华南")
    {
        ui->combo3->addItems(QStringList()<<"广东"<<"广西"<<"海南");
    }
    else{
        ...;
    }
}
```

```c++
void DlgItem::on_edit1_textChanged(const QString &arg1)	// 存在更改操作
{
    ui->labelTip->setText("");
}
```

## 二、InputTool

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\1555645116738.png)

### 1. 单例模式的使用

```c++
// .h文件
static frmInput *Instance() {
        if (!_instance) {
            _instance = new frmInput;
        }
        return _instance;
    }
static frmInput *_instance;     //实例对象
// .cpp文件
frmInput *frmInput::_instance = 0;
```

显然是用于不管打开何种输入控件仅使用一组键盘对象。

### 2. 鼠标拖动

```c++
//鼠标拖动事件
void mouseMoveEvent(QMouseEvent *e);
//鼠标按下事件
void mousePressEvent(QMouseEvent *e);
//鼠标松开事件
void mouseReleaseEvent(QMouseEvent *);

void frmInput::mouseMoveEvent(QMouseEvent *e)
{
    if (mousePressed && (e->buttons() && Qt::LeftButton)) {
        this->move(e->globalPos() - mousePoint);
        e->accept();
    }
}
void frmInput::mousePressEvent(QMouseEvent *e)
{
    if (e->button() == Qt::LeftButton) {
        mousePressed = true;
        mousePoint = e->globalPos() - this->pos();
        e->accept();
    }
}
void frmInput::mouseReleaseEvent(QMouseEvent *)
{
    mousePressed = false;
}
```

### 3. 全局焦点变化

```c++
//绑定全局改变焦点信号槽
connect(qApp, SIGNAL(focusChanged(QWidget *, QWidget *)),
        this, SLOT(focusChanged(QWidget *, QWidget *)));
```

#### 3.1 焦点判定分析：

`(nowWidget != 0 && !this->isAncestorOf(nowWidget))` 含义为当前焦点控件非空，且焦点不在虚拟键盘上

`(oldWidget == 0x0 && !isFirst)` oldwidget为0即为焦点从有对象转为无对象，再转为有对象时的情况。

```c++
void frmInput::focusChanged(QWidget *oldWidget, QWidget *nowWidget)
{
    //qDebug() << "oldWidget:" << oldWidget << " nowWidget:" << nowWidget;
    if (nowWidget != 0 && !this->isAncestorOf(nowWidget)) {
        //在Qt5和linux系统中(嵌入式linux除外),当输入法面板关闭时,焦点会变成无,然后焦点会再次移到焦点控件处
        //这样导致输入法面板的关闭按钮不起作用,关闭后马上有控件获取焦点又显示.
        //为此,增加判断,当焦点是从有对象转为无对象再转为有对象时不要显示.
        //这里又要多一个判断,万一首个窗体的第一个焦点就是落在可输入的对象中,则要过滤掉
#ifndef __arm__
        if (oldWidget == 0x0 && !isFirst) { // 过滤掉初始焦点为0的情况，即系统默认指向时
            return;
        }
#endif

        isFirst = false;
        QWidget * pModalWidget = QApplication::activeModalWidget () ;
        if (NULL != pModalWidget && pModalWidget->inherits("QDialog"))
        {
            Qt::WindowModality Modality = pModalWidget->windowModality();
            /*Qt::NonModal       The window is not modal and does not block input to other windows.
          非模态对话框

          Qt::WindowModal        The window is modal to a single window hierarchy and blocks input to its parent window, all grandparent windows, and all siblings of its parent and grandparent windows.
          窗口级模态对话框，即只会阻塞父窗口、父窗口的父窗口及兄弟窗口。（半模态对话框）

          Qt::ApplicationModal       The window is modal to the application and blocks input to all windows.
          应用程序级模态对话框，即会阻塞整个应用程序的所有窗口。（模态对话框）
          */
            if(Qt::ApplicationModal == Modality)	//遇到模态对话框则小写且不显示
            {
                //需要将输入法切换到最初的原始状态--小写,同时将之前的对象指针置为零
                currentWidget = 0;
                currentLineEdit = 0;
                currentTextEdit = 0;
                currentPlain = 0;
                currentBrowser = 0;
                currentEditType = "";
                currentType = "min";
                changeType(currentType);
                this->setVisible(false);
                return;
            }
        }
        // 如下一段为焦点关注为需求控件时才会配置和显示虚拟键盘。
        if (nowWidget->inherits("QLineEdit")) {
            currentLineEdit = (QLineEdit *)nowWidget;
            currentEditType = "QLineEdit";
            ShowPanel();
        } else if (nowWidget->inherits("QTextEdit")) {
            currentTextEdit = (QTextEdit *)nowWidget;
            currentEditType = "QTextEdit";
            ShowPanel();
        } else if (nowWidget->inherits("QPlainTextEdit")) {
            currentPlain = (QPlainTextEdit *)nowWidget;
            currentEditType = "QPlainTextEdit";
            ShowPanel();
        } else if (nowWidget->inherits("QTextBrowser")) {
            currentBrowser = (QTextBrowser *)nowWidget;
            currentEditType = "QTextBrowser";
            ShowPanel();
        } else if (nowWidget->inherits("QComboBox")) {
            QComboBox *cbox = (QComboBox *)nowWidget;
            //只有当下拉选择框处于编辑模式才可以输入
            if (cbox->isEditable()) {
                currentLineEdit = cbox->lineEdit() ;
                currentEditType = "QLineEdit";
                ShowPanel();
            }
        } else if (nowWidget->inherits("QSpinBox") ||
                   nowWidget->inherits("QDoubleSpinBox") ||
                   nowWidget->inherits("QDateEdit") ||
                   nowWidget->inherits("QTimeEdit") ||
                   nowWidget->inherits("QDateTimeEdit")) {
            currentWidget = nowWidget;
            currentEditType = "QWidget";
            ShowPanel();
        } else {
            //需要将输入法切换到最初的原始状态--小写,同时将之前的对象指针置为零
            currentWidget = 0;
            currentLineEdit = 0;
            currentTextEdit = 0;
            currentPlain = 0;
            currentBrowser = 0;
            currentEditType = "";
            currentType = "min";
            changeType(currentType);
            this->setVisible(false);
        }

        //根据用户选择的输入法位置设置-居中显示-底部填充-显示在输入框正下方
        if (currentPosition == "center") {
            QPoint pos = QPoint(deskWidth / 2 - frmWidth / 2, deskHeight / 2 - frmHeight / 2);
            this->setGeometry(pos.x(), pos.y(), frmWidth, frmHeight);
        } else if (currentPosition == "bottom") {
            this->setGeometry(0, deskHeight - frmHeight, deskWidth, frmHeight);
        } else if (currentPosition == "control") {
            QRect rect = nowWidget->rect();
            QPoint pos = QPoint(rect.left(), rect.bottom() + 2);
            pos = nowWidget->mapToGlobal(pos);
            this->setGeometry(pos.x(), pos.y(), frmWidth, frmHeight);
        }
    }
}
```

#### 3.2 位置变化

`QPoint`和`QRectF`的使用

```c++
if (currentPosition == "center") 	// 居中显示
{
    QPoint pos = QPoint(deskWidth / 2 - frmWidth / 2, deskHeight / 2 - frmHeight / 2);
    this->setGeometry(pos.x(), pos.y(), frmWidth, frmHeight);
}
else if (currentPosition == "bottom") //底部显示
{
    this->setGeometry(0, deskHeight - frmHeight, deskWidth, frmHeight);
}
else if (currentPosition == "control") //控件底部显示
{
    QRect rect = nowWidget->rect();
    QPoint pos = QPoint(rect.left(), rect.bottom() + 2);
    pos = nowWidget->mapToGlobal(pos);
    this->setGeometry(pos.x(), pos.y(), frmWidth, frmHeight);
}
```

### 4. Btn信号处理

#### 4.1 Btn绑定

```c++
// 获取界面内的所有QPushButton按钮集合，然后绑定统一的事件相应函数
QList<QPushButton *> btn = this->findChildren<QPushButton *>();
foreach (QPushButton * b, btn) {
    connect(b, SIGNAL(clicked()), this, SLOT(btn_clicked()));
}
```

#### 4.2 Btn事件相应

==`QObject::Sender()返回发送信号的对象的指针，返回类型为QObject *`==

```c++
void frmInput::btn_clicked()
{
    //如果当前焦点控件类型为空,则返回不需要继续处理
    if (currentEditType == "") {
        return;
    }
    QPushButton *btn = (QPushButton *)sender();
    
    QString objectName = btn->objectName();
    if (objectName == "btnType") {
        if (currentType == "min") {
            currentType = "max";
        } else if (currentType == "max") {
            currentType = "chinese";
        } else if (currentType == "chinese") {
            currentType = "min";
        }
        changeType(currentType);
    } else if (objectName == "btnDelete") {
        //如果当前是中文模式,则删除对应拼音,删除完拼音之后再删除对应文本输入框的内容
        if (currentType == "chinese") {
            QString txt = ui->labPY->text();
            int len = txt.length();
            if (len > 0) {
                ui->labPY->setText(txt.left(len - 1));
                selectChinese();
            } else {
                deleteValue();
            }
        } else {
            deleteValue();
        }
    } else if (objectName == "btnPre") {
        if (currentPY_index >= 20) {
            //每次最多显示10个汉字,所以每次向前的时候索引要减20
            if (currentPY_index % 10 == 0) {
                currentPY_index -= 20;
            } else {
                currentPY_index = currentPY_count - (currentPY_count % 10) - 10;
            }
        } else {
            currentPY_index = 0;
        }
        showChinese();
    } else if (objectName == "btnNext") {
        if (currentPY_index < currentPY_count - 1) {
            showChinese();
        }
    } else if (objectName == "btnClose") {
        this->setVisible(false);
    } else if (objectName == "btnSpace") {
        insertValue(" ");
    } else {
        QString value = btn->text();
        //如果是&按钮，因为对应&被过滤,所以真实的text为去除前面一个&字符
        if (objectName == "btnOther7") {
            value = value.right(1);
        }
        //当前不是中文模式,则单击按钮对应text为传递参数
        if (currentType != "chinese") {
            insertValue(value);
        } else {
            //中文模式下,不允许输入特殊字符,单击对应数字按键取得当前索引的汉字
            if (btn->property("btnOther").toBool()) {
                if (ui->labPY->text().length() == 0) {
                    insertValue(value);
                }
            } else if (btn->property("btnNum").toBool()) {
                if (ui->labPY->text().length() == 0) {
                    insertValue(value);
                } else if (objectName == "btn0") {
                    setChinese(0);
                } else if (objectName == "btn1") {
                    setChinese(1);
                } else if (objectName == "btn2") {
                    setChinese(2);
                } else if (objectName == "btn3") {
                    setChinese(3);
                } else if (objectName == "btn4") {
                    setChinese(4);
                } else if (objectName == "btn5") {
                    setChinese(5);
                } else if (objectName == "btn6") {
                    setChinese(6);
                } else if (objectName == "btn7") {
                    setChinese(7);
                } else if (objectName == "btn8") {
                    setChinese(8);
                } else if (objectName == "btn9") {
                    setChinese(9);
                }
            } else if (btn->property("btnLetter").toBool()) {
                ui->labPY->setText(ui->labPY->text() + value);
                selectChinese();
            }
        }
    }
}
```

#### 4.3 Btn属性设置

```c++
ui->btnOther1->setProperty("btnOther", true);
ui->btn0->setProperty("btnNum", true);
ui->btna->setProperty("btnLetter", true);
```

```c++
bool frmInput::checkPress()
{
    //只有属于输入法键盘的合法按钮才继续处理
    bool num_ok = btnPress->property("btnNum").toBool();
    bool other_ok = btnPress->property("btnOther").toBool();
    bool letter_ok = btnPress->property("btnLetter").toBool();
    if (num_ok || other_ok || letter_ok) {
        return true;
    }
    return false;
}
```



### 5. 系统事件过滤

```c++
//绑定按键事件过滤器
qApp->installEventFilter(this);
```

此过程包括两部分，注册事件以及事件过滤。eventFilter过程在最终控件事件相应前到达。

```c++
//事件过滤器,用于识别鼠标单击汉字标签处获取对应汉字
bool frmInput::eventFilter(QObject *obj, QEvent *event)
{
    if (event->type() == QEvent::MouseButtonPress) {
        if (obj == ui->labCh0) {
            setChinese(0);
        } else if (obj == ui->labCh1) {
            setChinese(1);
        } else if (obj == ui->labCh2) {
            setChinese(2);
        } else if (obj == ui->labCh3) {
            setChinese(3);
        } else if (obj == ui->labCh4) {
            setChinese(4);
        } else if (obj == ui->labCh5) {
            setChinese(5);
        } else if (obj == ui->labCh6) {
            setChinese(6);
        } else if (obj == ui->labCh7) {
            setChinese(7);
        } else if (obj == ui->labCh8) {
            setChinese(8);
        } else if (obj == ui->labCh9) {
            setChinese(9);
        } else if (currentEditType != "" && obj != ui->btnClose) {
            ShowPanel();
        }
        btnPress = (QPushButton *)obj;
        if (checkPress()) {
            isPress = true;
            timerPress->start(500);
        }
        return false;
    } else if (event->type() == QEvent::MouseButtonRelease) {
        btnPress = (QPushButton *)obj;
        if (checkPress()) {
            isPress = false;
            timerPress->stop();
        }
        return false;
    } else if (event->type() == QEvent::KeyPress) {
        //如果输入法窗体不可见,则不需要处理
        if (!isVisible()) {
            return QWidget::eventFilter(obj, event);
        }

        QKeyEvent *keyEvent = static_cast<QKeyEvent *>(event);
        //Shift切换输入法模式,esc键关闭输入法面板,空格取第一个汉字,退格键删除
        //中文模式下回车键取拼音,中文模式下当没有拼音时可以输入空格
        if (keyEvent->key() == Qt::Key_Space) {
            if (ui->labPY->text() != "") {
                setChinese(0);
                return true;
            } else {
                return false;
            }
        } else if (keyEvent->key() == Qt::Key_Return 
                   || keyEvent->key() == Qt::Key_Enter) {
            insertValue(ui->labPY->text());
            ui->labPY->setText("");
            selectChinese();
            return true;
        } else if (keyEvent->key() == Qt::Key_Shift) {
            ui->btnType->click();
            return true;
        } else if (keyEvent->key() == Qt::Key_Escape) {
            ui->btnClose->click();
            return true;
        } else if (keyEvent->key() == Qt::Key_Backspace) {
            ui->btnDelete->click();
            return true;
        } else if (keyEvent->text() == "+" || keyEvent->text() == "=") {
            if (ui->labPY->text() != "") {
                ui->btnNext->click();
                return true;
            } else {
                return false;
            }
        } else if (keyEvent->text() == "-" || keyEvent->text() == "_") {
            if (ui->labPY->text() != "") {
                ui->btnPre->click();
                return true;
            } else {
                return false;
            }
        } else if (keyEvent->key() == Qt::Key_CapsLock) {
            if (currentType != "max") {
                currentType = "max";
            } else {
                currentType = "min";
            }
            changeType(currentType);
            return true;
        } else {
            if (currentEditType == "QWidget") {
                return false;
            }
            QString key;
            if (currentType == "chinese") {
                key = keyEvent->text();
            } else if (currentType == "min") {
                key = keyEvent->text().toLower();
            } else if (currentType == "max") {
                key = keyEvent->text().toUpper();
            }
            QList<QPushButton *> btn = this->findChildren<QPushButton *>();
            foreach (QPushButton * b, btn) {
                if (b->text() == key) {
                    b->click();
                    return true;
                }
            }
        }
        return false;
    }
    return QWidget::eventFilter(obj, event);
}
```

#### 5.1 一般流程

判定信号类型：`event->type()`可以是：`QEvent::MouseButtonPress`**鼠标按下事件。**`QEvent::MouseButtonRelease`**鼠标松开事件。**`QEvent::KeyPress`**键盘按下事件。**

信号类型进一步约束为键盘按键类型：

`QKeyEvent *keyEvent = static_cast<QKeyEvent *>(event);`

```c++
//按钮特殊类型时
if(keyEvent->key() == Qt::Key_Space){}
if(keyEvent->key() == Qt::Key_Return || keyEvent->key() == Qt::Key_Enter){}
if(keyEvent->key() == Qt::Key_Shift) {}
if(keyEvent->key() == Qt::Key_Backspace){}
// 按钮特殊符号时
if(keyEvent->text() == "-" || keyEvent->text() == "_"){}
// 按钮为普通字母或数字时的处理
QList<QPushButton *> btn = this->findChildren<QPushButton *>();
foreach (QPushButton * b, btn) {
    if (b->text() == key) {
        b->click();
        return true;
    }
}
```

#### 5.2 关于长按处理

显然按钮的长按操作，包括键盘长按操作和鼠标长按操作。此处仅找到鼠标事件的长按操作。实现如下

```c++
// 初始化
timerPress = new QTimer(this);
connect(timerPress, SIGNAL(timeout()), this, SLOT(reClicked()));
// 鼠标信号处理
if (event->type() == QEvent::MouseButtonPress) {
    ...;
    if (checkPress()) {
        isPress = true;
        timerPress->start(500);
    }
}
// 超时设置
void frmInput::reClicked()
{
    if (isPress) {
        timerPress->setInterval(30);
        btnPress->click();
    }
}
```

 首次长按超时为500ms,然后会触发连续的30ms间隔的重复click()相应

### 6. 文本输入的增删操作

```c++
void frmInput::insertValue(QString value)
{
    if (currentEditType == "QLineEdit") {
        currentLineEdit->insert(value);
    } else if (currentEditType == "QTextEdit") {
        currentTextEdit->insertPlainText(value);
    } else if (currentEditType == "QPlainTextEdit") {
        currentPlain->insertPlainText(value);
    } else if (currentEditType == "QTextBrowser") {
        currentBrowser->insertPlainText(value);
    } else if (currentEditType == "QWidget") {
        QKeyEvent keyPress(QEvent::KeyPress, 0, Qt::NoModifier, QString(value));
        QApplication::sendEvent(currentWidget, &keyPress);
    }
}
```

```c++
void frmInput::deleteValue()
{
    if (currentEditType == "QLineEdit") {
        currentLineEdit->backspace();
    } else if (currentEditType == "QTextEdit") {
        //获取当前QTextEdit光标,如果光标有选中,则移除选中字符,否则删除光标前一个字符
        QTextCursor cursor = currentTextEdit->textCursor();
        if(cursor.hasSelection()) {
            cursor.removeSelectedText();
        } else {
            cursor.deletePreviousChar();
        }
    } else if (currentEditType == "QPlainTextEdit") {
        //获取当前QTextEdit光标,如果光标有选中,则移除选中字符,否则删除光标前一个字符
        QTextCursor cursor = currentPlain->textCursor();
        if(cursor.hasSelection()) {
            cursor.removeSelectedText();
        } else {
            cursor.deletePreviousChar();
        }
    } else if (currentEditType == "QTextBrowser") {
        //获取当前QTextEdit光标,如果光标有选中,则移除选中字符,否则删除光标前一个字符
        QTextCursor cursor = currentBrowser->textCursor();
        if(cursor.hasSelection()) {
            cursor.removeSelectedText();
        } else {
            cursor.deletePreviousChar();
        }
    } else if (currentEditType == "QWidget") {
        QKeyEvent keyPress(QEvent::KeyPress, Qt::Key_Delete, Qt::NoModifier, QString());
        QApplication::sendEvent(currentWidget, &keyPress);
    }
}
```

### 7. 样式设置

```c++
    if (currentStyle == "blue") 
    {	//blue--淡蓝色  
        changeStyle("#DEF0FE", "#C0DEF6", "#C0DCF2", "#386487");
    } else if (currentStyle == "dev") 
    {	//dev--dev风格  
        changeStyle("#C0D3EB", "#BCCFE7", "#B4C2D7", "#324C6C");
    } else if (currentStyle == "gray") 
    {	//gray--灰色  
        changeStyle("#E4E4E4", "#A2A2A2", "#A9A9A9", "#000000");
    } else if (currentStyle == "lightgray") 
    {	//lightgray--浅灰色  
        changeStyle("#EEEEEE", "#E5E5E5", "#D4D0C8", "#6F6F6F");
    } else if (currentStyle == "darkgray") 
    {	//darkgray--深灰色  
        changeStyle("#D8D9DE", "#C8C8D0", "#A9ACB5", "#5D5C6C");
    } else if (currentStyle == "black") 
    {	// black--黑色  
        changeStyle("#4D4D4D", "#292929", "#D9D9D9", "#CACAD0");
    } else if (currentStyle == "brown") 
    {	//brown--灰黑色  
        changeStyle("#667481", "#566373", "#C2CCD8", "#E7ECF0");
    } else if (currentStyle == "silvery")
    {	//silvery--银色
        changeStyle("#E1E4E6", "#CCD3D9", "#B2B6B9", "#000000");
    }
```



```c++
void frmInput::changeStyle(QString topColor, QString bottomColor, QString borderColor, QString textColor)
{
    QStringList qss;
    qss.append(QString("QWidget#frmInput{background:qlineargradient"
                       "(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 %1,stop:1 %2);}")
               .arg(topColor).arg(bottomColor));
    qss.append("QPushButton{padding:5px;border-radius:3px;}");

    qss.append(QString("QPushButton:hover{background:qlineargradient"
                       "(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 %1,stop:1 %2);}")
               .arg(topColor).arg(bottomColor));
    qss.append(QString("QLabel,QPushButton{color:%1;}").arg(textColor));

    qss.append(QString("QPushButton#btnPre,"
                       "QPushButton#btnNext,"
                       "QPushButton#btnClose{padding:5px;}"));

    qss.append(QString("QPushButton{border:1px solid %1;}")
               .arg(borderColor));

    qss.append(QString("QLineEdit{"
                       "border:1px solid %1;"
                       "border-radius:5px;"
                       "padding:2px;"
                       "background:none;"
                       "selection-background-color:%2;"
                       "selection-color:%3;}")
               .arg(borderColor).arg(bottomColor).arg(topColor));

    this->setStyleSheet(qss.join(""));
}
```

1. `QWidget#frmInput{...}` QWidget下的实体类样式设置。
2. `QPushButton#btnPre,QPushButton#btnNextQPushButton#btnClose{padding:5px;}`并行设置。
3. `QLineEdit{}`统一设置。
4. `QPushButton{}`和 `QPushButton:hover{}`按钮的样式和选中设置。

