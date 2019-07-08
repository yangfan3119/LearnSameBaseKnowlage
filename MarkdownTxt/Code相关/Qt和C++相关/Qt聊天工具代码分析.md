## 一、总述

​	本程序分为客户端和服务器程序。采用C/S架构搭建。socket TCP通信方式，JSON格式数据格式传输。

​	服务器端存储用户注册信息，用于文件和聊天消息的交互和转发。基本通信情况的信息汇总，以及相关改密码等操作。

​	客户端用于聊天群的记录、朋友列表的记录、消息的存储。

​	基本功能类似QQ这种聊天工具类似。

## 二、Server

### 2.1 database

#### 2.1.0 建表

| id       | name   | passwd   | status   | groupId  | lasttime     |
| -------- | ------ | -------- | -------- | -------- | ------------ |
| 唯一标识 | 用户名 | 用户密码 | 线上状态 | 组群编号 | 最后登录时间 |

```sqlite
CREATE TABLE USERINFO (id INT PRIMARY KEY, name varchar(20), passwd varchar(20), head varchar(20), status INT, groupId INT, lasttime DATETIME);
```

记录用户信息，包含：用户名、密码、头像、状态、聊天室编号、时间。

| id       | groupId | name | head | userId | identity |
| -------- | ------- | ---- | ---- | ------ | -------- |
| 唯一标识 | 群组id  | 群名 | 头像 | 用户id | 用户身份 |

```sqlite
CREATE TABLE GROUPINFO (id INT PRIMARY KEY, groupId INT, name varchar(20), head varchar(20), userId INT, identity INT);
```

记录聊天室信息，包含：聊天室编号，名称，头像，用户编号，身份。

```sqlite
CREATE TABLE USERHEAD (id INT PRIMARY KEY, name varchar(20), data varchar);
```

用户头像信息汇总。头像信息为图片地址。

```sqlite
// 例：
INSERT INTO USERINFO VALUES(1, 'admin', '123456', '2.bmp', 0, 1, '');
```

#### 2.1.1 更新用户状态

功能：用户更新用户当前状态，包括当前的上线状态和下线状态。

实现：

```c++
typedef enum {
    ConnectedHost = 0x01,
    DisConnectedHost,

    LoginSuccess,       // 登录成功
    LoginPasswdError,   // 密码错误

    OnLine,				// 在线状态
    OffLine,			// 离线状态

    RegisterOk,
    RegisterFailed,

    AddFriendOk,
    AddFriendFailed,
} E_STATUS;
```

```c++
void DataBaseMagr::ChangeAllUserStatus()
{
    QSqlQuery query("SELECT * FROM USERINFO ORDER BY id;");
    while (query.next()) {
        // 更新为下线状态
        UpdateUserStatus(query.value(0).toInt(), OffLine);
    }
}
void DataBaseMagr::UpdateUserStatus(const int &id, const quint8 &status)
{
    // 组织sql语句
    QString strSql = "UPDATE USERINFO SET status=";
    strSql += QString::number(status);
    strSql += QString(",lasttime='");
    strSql += DATE_TME_FORMAT;
    strSql += QString("' WHERE id=");
    strSql += QString::number(id);

    // 执行数据库操作
    QSqlQuery query(strSql);
    query.exec();
}
```

技巧：

```c++
// 关于数据库中的时间戳，直接使用宏定义方式实现
#define DATE_TME_FORMAT     QDateTime::currentDateTime().toString("yyyy/MM/dd hh:mm:ss")
```

#### 2.1.2 获取所有用户信息

使用JSON完成信息汇总：

```c++
QJsonArray DataBaseMagr::GetAllUsers()
{
    QSqlQuery query("SELECT * FROM USERINFO ORDER BY id;");
    QJsonArray jsonArr;
    while (query.next()) {
        QJsonObject jsonObj;
        jsonObj.insert("id", query.value("id").toInt());
        jsonObj.insert("name", query.value("name").toString());
        jsonObj.insert("passwd", query.value("passwd").toString());
        jsonObj.insert("head", query.value("head").toString());
        jsonObj.insert("status", query.value("status").toInt());
        jsonObj.insert("groupId", query.value("groupId").toInt());
        jsonObj.insert("lasttime", query.value("lasttime").toString());
        jsonArr.append(jsonObj);
    }
    return jsonArr;
}
```

此处存在的包含关系为： `QJsonObject`为单组数据，`QJsonArray`为`QJsonObject`的集合格式。

`QJsonObject jsonObj = jsonArry.at(i).toObject();`

#### 2.1.3 其他业务

##### a. 获取基本信息

```c++
// 获取当前id的用户状态，返回 QJsonObject 数据
sql = "SELECT [name],[status],[head] FROM USERINFO WHERE id=%d;";
// 获取当前用户的在线状态
sql = "SELECT [status] FROM USERINFO WHERE id=%d;";
// 获取用户名
sql = "SELECT [name] FROM USERINFO WHERE id='%d';";
// 获取用户头像
sql = "SELECT [head] FROM USERINFO WHERE id='%d';";
```

##### b. 登录校验

```c++
// 登录校验
{
    // 1. 查询用户信息
    sql = "SELECT [id],[head],[status] FROM USERINFO WHERE name='%s' AND passwd='%s';";
    // 2. 判断记录中的最新状态，如果已在线则返回错误，否则更新在线状态
    if (OnLine == query.value("status").toInt())
    {
        nId = -2;
        code = -2;
    }
    else
    {
        // 更新在线信息
        UpdateUserStatus(nId, OnLine);
        code = 0;
    }
    // 3.返回查询信息
    jsonObj.insert("id", nId);
    jsonObj.insert("msg", nId < 0 ? "error" : "ok");
    jsonObj.insert("head", strHead);
    jsonObj.insert("code", code);
}
```

##### c. 用户注册

```c++
// 用户注册, 传入参数： name passwd
{
    // 1. 通过name查询是否存在该用户
    sql = "SELECT [id] FROM USERINFO WHERE name='%s';";
    // 2. 编纂id号，此处顺序产生该id号，故需查询id最大值，然后+1即为新用户的id号。
    sql = "SELECT [id] FROM USERINFO ORDER BY id DESC;";
    // 3. 创建新用户
    QSqlQuery query;
    query.prepare("INSERT INTO USERINFO (id, name, passwd, head, status, groupId, lasttime) VALUES (?, ?, ?, ?, ?, ?, ?);");
    query.bindValue(0, nId + 1);
    query.bindValue(1, name);
    query.bindValue(2, passwd);
    query.bindValue(3, "0.bmp");
    query.bindValue(4, 0);
    query.bindValue(5, 0);
    query.bindValue(6, DATE_TME_FORMAT);
    query.exec();
}
```

```c++
// 添加好友 —— 服务器端仅做一个验证，该用户是否为注册用户。
sql = "SELECT [id],[status],[head] FROM USERINFO WHERE name='%s';";
```

##### d. 创建加入群

```c++
// 加入群 ——   @param userId：聊天室表中userId 		@param name:聊天室名称
{
    // 1. 判断聊天室是否存在
    sql = "SELECT [groupId] FROM GROUPINFO WHERE name='%s';"%(name);
    // 2. 聊天室存在，再判断该用户是否加入群 —— groupId = 1查询结果
    sql = "SELECT [userId] FROM GROUPINFO WHERE groupId='%s';";
    // 3. 聊天室存在，但该用户不在群中则创建该群和人的对应关系
    query.prepare("INSERT INTO GROUPINFO (id, groupId, name, userId, identity) VALUES (?, ?, ?, ?, ?);");
    query.bindValue(0, nIndex);
    query.bindValue(1, nGroupId);
    query.bindValue(2, name);
    query.bindValue(3, userId);
    query.bindValue(4, 3);
	query.exec();
    // 4. 聊天室不存在时，则返回错误。
    // 5. 聊天室存在，且用户也在该聊天室中，则返回错误码
}
```

```c++
// 创建聊天室群	@param userId：聊天室表中userId 		@param name:聊天室名称
{
    // 1. 判断聊天室是否存在
    sql = "SELECT [id],[groupId],[head] FROM GROUPINFO WHERE name='' AND userId='';";
    // 2. 聊天室存在，返回聊天室基本信息：id groupId head
    // 3. 聊天室不存在，则做两个查询： id最大值；groupId最大值，为该userId下的groupId最大值；
    // 4. 根据新ID重新创建用户
    query.prepare("INSERT INTO GROUPINFO (id, groupId, name, head, userId, identity) "
                      "VALUES (?, ?, ?, ?, ?, ?);");
    query.bindValue(0, nIndex);
    query.bindValue(1, nGroupId);
    query.bindValue(2, name);
    query.bindValue(3, "1.bmp");
    query.bindValue(4, userId);
    query.bindValue(5, 1);
	query.exec();
    // 4. 聊天室不存在时，则返回错误。
    // 5. 聊天室存在，且用户也在该聊天室中，则返回错误码
}
```

##### e. 群操作

```c++
// 获取群下所有用户
sql = "SELECT [userId] FROM GROUPINFO WHERE groupId='%d';";
sql = "SELECT [name],[head],[status] FROM USERINFO WHERE id='%d';";
```

#### 2.1.4 总结

- 使用SQLITE数据库，默认db文件存储地址为程序运行目录。
- 程序运行初始化，立即加载数据文件，然后执行建表语句。然后立刻更新用户数据为下线状态。
- 关于时间戳的使用，通过宏操作完成。QT中数据库加载一次后，该数据库会保存记录下来，后续sql语句可以直接使用。
- 使用`QJsonObject`、`QJsonArray`来回传数据。

### 2.2 tcpserver

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\1555917404841.png)

从上图可知，作者设计的结构为总分模式，服务管理类为父类，子类分为消息服务器和文件服务器，并分别管理消息链路和文件链路。

#### 2.2.1 Server类

```c++
// 服务管理类
class TcpServer : public QObject {
    Q_OBJECT
public:
    explicit TcpServer(QObject *parent = 0); // 初始化创建QTcpServer类，并绑定新连接的信号
    ~TcpServer();	// 关闭监听

    bool StartListen(int port = 6666);	//实现监听
    void CloseListen();	//关闭监听
signals:
    void signalUserStatus(const QString &text);
protected:
    QTcpServer *m_tcpServer;
protected slots:	// 继承虚函数
    virtual void SltNewConnection() = 0;		//相应新连接，并创建该路socket
    virtual void SltConnected() = 0;			//连接成功
    virtual void SltDisConnected() = 0;			//断开连接
};
```

```c++
TcpServer::TcpServer(QObject *parent) : QObject(parent) {
    m_tcpServer = new QTcpServer(this);
    connect(m_tcpServer, SIGNAL(newConnection()), this, SLOT(SltNewConnection()));
}
TcpServer::~TcpServer() {
    if (m_tcpServer->isListening()) m_tcpServer->close();
}
bool TcpServer::StartListen(int port) {
    if (m_tcpServer->isListening()) m_tcpServer->close();
    bool bOk = m_tcpServer->listen(QHostAddress::Any, port);
    return bOk;
}
void TcpServer::CloseListen() {
    m_tcpServer->close();
}
```

#### 2.2.2 TcpMsgServer类

```c++
// 消息服务器
class TcpMsgServer : public TcpServer
{
    Q_OBJECT
public:
    explicit TcpMsgServer(QObject *parent = 0);
    ~TcpMsgServer();
signals:
    void signalDownloadFile(const QJsonValue &json);
private:
    QVector < ClientSocket * > m_clients;	// 客户端管理
public slots:
    void SltTransFileToClient(const int &userId, const QJsonValue &json);	//文件转发
private slots:
    void SltNewConnection();
    void SltConnected();
    void SltDisConnected();
    void SltMsgToClient(const quint8 &type, const int &id, const QJsonValue &json);	
};
```

```c++
TcpMsgServer::TcpMsgServer(QObject *parent) : TcpServer(parent) {}
TcpMsgServer::~TcpMsgServer() {
    foreach (ClientSocket *client, m_clients) {	// 依次关闭所有链接
        m_clients.removeOne(client);
        client->Close();
    }
}
// 有新的客户端连接进来,并创建新的链接
void TcpMsgServer::SltNewConnection() {
    ClientSocket *client = new ClientSocket(this, m_tcpServer->nextPendingConnection());
    connect(client, SIGNAL(signalConnected()), this, SLOT(SltConnected()));
    connect(client, SIGNAL(signalDisConnected()), this, SLOT(SltDisConnected()));
} 
// 通过验证后，才可以加入容器进行管理
void TcpMsgServer::SltConnected() {
    ClientSocket *client = (ClientSocket *)this->sender();
    if (NULL == client) return;

    connect(client, SIGNAL(signalMsgToClient(quint8,int,QJsonValue)),
            this, SLOT(SltMsgToClient(quint8,int,QJsonValue)));
    connect(client, SIGNAL(signalDownloadFile(QJsonValue)), 
            this, SIGNAL(signalDownloadFile(QJsonValue)));

    Q_EMIT signalUserStatus(QString("用户 [%1] 上线").arg(DataBaseMagr::Instance()->GetUserName(client->GetUserId())));
    m_clients.push_back(client);
}
 // 有客户端下线
void TcpMsgServer::SltDisConnected() {
    ClientSocket *client = (ClientSocket *)this->sender();
    if (NULL == client) return;

    for (int i = 0; i < m_clients.size(); i++) {
        if (client == m_clients.at(i))
        {
            m_clients.remove(i);
            Q_EMIT signalUserStatus(QString("用户 [%1] 下线").arg(DataBaseMagr::Instance()->GetUserName(client->GetUserId())));
            return;
        }
    }
//disconnect: 连接信号，断开连接信号，消息转发信号，文件下载信号
    disconnect(client, SIGNAL(signalConnected()), this, SLOT(SltConnected()));
    disconnect(client, SIGNAL(signalDisConnected()), this, SLOT(SltDisConnected()));
    disconnect(client, SIGNAL(signalMsgToClient(quint8,int,QJsonValue)),
               this, SLOT(SltMsgToClient(quint8,int,QJsonValue)));
    disconnect(client, SIGNAL(signalDownloadFile(QJsonValue)), this, SIGNAL(signalDownloadFile(QJsonValue)));
}
// 消息转发控制
void TcpMsgServer::SltMsgToClient(const quint8 &type, const int &id, const QJsonValue &json) {
    // 查找要发送过去的id
    for (int i = 0; i < m_clients.size(); i++) {
        if (id == m_clients.at(i)->GetUserId()) {
            m_clients.at(i)->SltSendMessage(type, json);
            return;
        }
    }
}
void TcpMsgServer::SltTransFileToClient(const int &userId, const QJsonValue &json)
{
    // 查找要发送过去的id
    for (int i = 0; i < m_clients.size(); i++) {
        if (userId == m_clients.at(i)->GetUserId()) {
            m_clients.at(i)->SltSendMessage(SendFile, json);
            return;
        }
    }
}
```

#### 2.2.3 TcpFileServer类

```c++
class TcpFileServer : public TcpServer {
    Q_OBJECT
public :
    explicit TcpFileServer(QObject *parent = 0);
    ~TcpFileServer();
signals:
    void signalRecvFinished(int id, const QJsonValue &json);
private:
    QVector < ClientFileSocket * > m_clients; // 客户端管理
private slots:
    void SltNewConnection();
    void SltConnected();
    void SltDisConnected();
    void SltClientDownloadFile(const QJsonValue &json); // 文件下载
};
```

```c++
TcpFileServer::TcpFileServer(QObject *parent) : TcpServer(parent) {}
TcpFileServer::~TcpFileServer() {
    foreach (ClientFileSocket *client, m_clients) {
        m_clients.removeOne(client);
        client->Close();
    }
}
void TcpFileServer::SltNewConnection() {
    ClientFileSocket *client = new ClientFileSocket(this, m_tcpServer->nextPendingConnection());
    connect(client, SIGNAL(signalConnected()), this, SLOT(SltConnected()));
    connect(client, SIGNAL(signalDisConnected()), this, SLOT(SltDisConnected()));
}
void TcpFileServer::SltConnected() {
    ClientFileSocket *client = (ClientFileSocket *)this->sender();
    if (NULL == client) return;
    m_clients.push_back(client);
}
void TcpFileServer::SltDisConnected() {
    ClientFileSocket *client = (ClientFileSocket *)this->sender();
    if (NULL == client) return;

    for (int i = 0; i < m_clients.size(); i++) {
        if (client == m_clients.at(i)) {
            m_clients.remove(i);
            return;
        }
    }

    disconnect(client, SIGNAL(signalConnected()), this, SLOT(SltConnected()));
    disconnect(client, SIGNAL(signalDisConnected()), this, SLOT(SltDisConnected()));
}
// 客户端请求下载文件
void TcpFileServer::SltClientDownloadFile(const QJsonValue &json)
{
    // 根据ID寻找连接的socket
    if (json.isObject()) {
        QJsonObject jsonObj = json.toObject();
        qint32 nId = jsonObj.value("from").toInt();
        qint32 nWid = jsonObj.value("id").toInt();;
        QString fileName = jsonObj.value("msg").toString();
        qDebug() << "get file" << jsonObj << m_clients.size();
        for (int i = 0; i < m_clients.size(); i++) {
            if (m_clients.at(i)->CheckUserId(nId, nWid))
            {
                m_clients.at(i)->StartTransferFile(fileName);
                return;
            }
        }
    }
}
```

#### 2.2.4 ClientSocket类

```c++
// 服务端socket管理类
class ClientSocket : public QObject
{
    Q_OBJECT
public:
    explicit ClientSocket(QObject *parent = 0, QTcpSocket *tcpSocket = NULL);
    ~ClientSocket();

    int GetUserId() const;
    void Close();

private:
    QTcpSocket *m_tcpSocket;
    int         m_nId;
    // 消息解析和抓转发处理
    void ParseLogin(const QJsonValue &dataVal);
    void ParseUserOnline(const QJsonValue &dataVal);
    void ParseLogout(const QJsonValue &dataVal);
    void ParseUpdateUserHead(const QJsonValue &dataVal);

    void ParseReister(const QJsonValue &dataVal);
    void ParseAddFriend(const QJsonValue &dataVal);
    void ParseAddGroup(const QJsonValue &dataVal);
    void ParseCreateGroup(const QJsonValue &dataVal);

    void ParseGetMyFriend(const QJsonValue &dataVal);
    void ParseGetMyGroups(const QJsonValue &dataVal);

    void ParseRefreshFriend(const QJsonValue &dataVal);
    void ParseRefreshGroups(const QJsonValue &dataVal);

    void ParseFriendMessages(const QByteArray &reply);
    void ParseGroupMessages(const QByteArray &reply);

signals:
    void signalConnected();
    void signalDisConnected();
    void signalDownloadFile(const QJsonValue &json);
    void signalMsgToClient(const quint8 &type, const int &id, const QJsonValue &dataVal);

public slots:
    // 消息回发
    void SltSendMessage(const quint8 &type, const QJsonValue &json);

private slots:
    void SltConnected();
    void SltDisconnected();
    void SltReadyRead();
};
```

```c++
// 核心代码实现
ClientSocket::ClientSocket(QObject *parent, QTcpSocket *tcpSocket) : QObject(parent) {
    m_nId = -1;	// 链路用户ID默认为-1，在正式建立用户连接后更新数据
    
    if (tcpSocket == NULL) 
        tcpSocket = new QTcpSocket(this);//服务管理类中为错误链路时则重新建立
    m_tcpSocket = tcpSocket;
	// socket核心三信号，数据读取响应，连接成功响应，连接断开响应。
    connect(m_tcpSocket, SIGNAL(readyRead()), this, SLOT(SltReadyRead()));
    connect(m_tcpSocket, SIGNAL(connected()), this, SLOT(SltConnected()));
    connect(m_tcpSocket, SIGNAL(disconnected()), this, SLOT(SltDisconnected()));
}
ClientSocket::~ClientSocket() {}
int ClientSocket::GetUserId() const { return m_nId;}
void ClientSocket::Close() { m_tcpSocket->abort(); }	//断开连接
void ClientSocket::SltConnected() { // 此处连接成功信号，并不意味着连接成功
    qDebug() << "connected";		// 只有当链路用户信息解析成功才算正式建立连接
    //    Q_EMIT signalConnected();
}
void ClientSocket::SltDisconnected() {
    qDebug() << "disconnected";
    DataBaseMagr::Instance()->UpdateUserStatus(m_nId, OffLine); //更新登录时间
    Q_EMIT signalDisConnected();		//向服务管理类发送断开连接信号
}
// 读取socket数据
void ClientSocket::SltReadyRead()
{	//此处实际应该做一个数据缓存，因为并不是所有数据都能依次发送过来
    // 读取socket数据
    QByteArray reply = m_tcpSocket->readAll();	
    QJsonParseError jsonError;
    // 转化为 JSON 文档
    QJsonDocument doucment = QJsonDocument::fromJson(reply, &jsonError);
    // 解析未发生错误
    if (!doucment.isNull() && (jsonError.error == QJsonParseError::NoError)) {
        // JSON 文档为对象
        if (doucment.isObject()) {
            // 转化为对象
            QJsonObject jsonObj = doucment.object();
            int nType = jsonObj.value("type").toInt();
            QJsonValue dataVal = jsonObj.value("data");

            switch (nType) {
            case Register:	ParseReister(dataVal);		break;	//注册
            case Login:		ParseLogin(dataVal);		break;	//登入
            case UserOnLine:ParseUserOnline(dataVal);   break;	//好友上线通知
            case Logout:	// 登出
                {
                    ParseLogout(dataVal);
                    Q_EMIT signalDisConnected();
                    m_tcpSocket->abort();
                }
                break;
            case UpdateHeadPic:	ParseUpdateUserHead(dataVal);	break;//更新用户头像文件
            case AddFriend:		ParseAddFriend(dataVal);        break;//添加好友
            case AddGroup:		ParseAddGroup(dataVal);			break;//添加聊天室
            case CreateGroup:	ParseCreateGroup(dataVal);		break;//创建聊天室
            case GetMyFriends:	ParseGetMyFriend(dataVal);		break;//获取好友
            case GetMyGroups:	ParseGetMyGroups(dataVal);		break;//获取聊天室
            case RefreshFriends:ParseRefreshFriend(dataVal);	break;//更新好友
            case RefreshGroups:	ParseRefreshGroups(dataVal);	break;//更新聊天室

            case SendMsg:
            case SendFile:
            case SendPicture:	ParseFriendMessages(reply);		break;//发送图片
            case SendGroupMsg:	ParseGroupMessages(reply);		break;//发送聊天室消息
            case SendFace:		ParseGroupMessages(reply);		break;//发送表情
            case SendFileOk:									break;
            case GetFile:		Q_EMIT signalDownloadFile(dataVal);		break;//获取文件
            default:
                break;
            }
        }
    }
}
```

通过协议解析可知两点：

1. 消息类型分为：文本信息以及文件信息。文本信息直接处理，而文件信息，则发送一个命令信息，让目标客户端发送一次文件处理的请求链接，包括上传，下载，以及更新等。
2. 消息的处理分为：服务器本地信息处理，包括客户端信息自查询等内容，不进行链路间的交互。另一路就是两个或者多个链路做信息交互——转发。通过服务管理类完成，通过信号`signalMsgToClient`发送到管理类。

#### 2.2.5 ClientFileSocket类

用于处理文件交互的类

```c++
class ClientFileSocket : public QObject
{
    Q_OBJECT
public:
    explicit ClientFileSocket(QObject *parent = 0, QTcpSocket *tcpSocket = NULL);
    ~ClientFileSocket();

    void Close();
    bool CheckUserId(const qint32 nId, const qint32 &winId);

    // 文件传输完成
    void FileTransFinished();
    void StartTransferFile(QString fileName);
signals:
    void signalConnected();
    void signalDisConnected();

    void signalRecvFinished(int id, const QJsonValue &json);

private:
    /************* Receive file *******************/
    quint64 loadSize;
    quint64 bytesReceived;  	//已收到数据的大小
    quint64 fileNameSize;  		//文件名的大小信息
    QString fileReadName;   	//存放文件名
    QByteArray inBlock;   		//数据缓冲区
    quint64 ullRecvTotalBytes;  //数据总大小
    QFile *fileToRecv;  		//要发送的文件

    QTcpSocket *m_tcpSocket;

    /************* Receive file *******************/
    quint16 blockSize;  		//存放接收到的信息大小
    QFile *fileToSend;  		//要发送的文件
    quint64 ullSendTotalBytes;  //数据总大小
    quint64 bytesWritten;  		//已经发送数据大小
    quint64 bytesToWrite;   	//剩余数据大小
    QByteArray outBlock;  		//数据缓冲区，即存放每次要发送的数据

    bool m_bBusy;

    // 需要转发的用户id
    qint32 m_nUserId;
    // 当前用户的窗口好友的id
    qint32 m_nWindowId;
private:
    void InitSocket();

private slots:
    void displayError(QAbstractSocket::SocketError); // 显示错误
    // 文件接收
    void SltReadyRead();
    // 发送
    void SltUpdateClientProgress(qint64 numBytes);
};
```

```c++
// 核心实现
ClientFileSocket::ClientFileSocket(QObject *parent, QTcpSocket *tcpSocket) :
    QObject(parent)
{
    // 将整个大的文件分成很多小的部分进行发送，每部分为4字节
    loadSize            = 50 * 1024;
    ullSendTotalBytes   = 0;
    ullRecvTotalBytes   = 0;
    bytesWritten        = 0;
    bytesToWrite        = 0;
    bytesReceived       = 0;

    fileNameSize        = 0;
    m_bBusy             = false;

    m_nUserId           = -1;
    m_nWindowId         = -1;

    // 本地文件存储
    fileToSend = new QFile(this);
    fileToRecv = new QFile(this);

    // 客户端
    if (tcpSocket == NULL) 
        tcpSocket = new QTcpSocket(this);
    m_tcpSocket = tcpSocket;

    // 我们更新进度条
    connect(m_tcpSocket, SIGNAL(readyRead()), this, SLOT(SltReadyRead()));
    connect(m_tcpSocket, SIGNAL(disconnected()), this, SIGNAL(signalDisConnected()));
    // 当有数据发送成功时，我们更新进度条
    connect(m_tcpSocket, SIGNAL(bytesWritten(qint64)), 
            this, SLOT(SltUpdateClientProgress(qint64)));
}
ClientFileSocket::~ClientFileSocket() {}
void ClientFileSocket::Close() { m_tcpSocket->abort(); }

// 用户socket检测，通过此函数进行判断连接的socket
bool ClientFileSocket::CheckUserId(const qint32 nId, const qint32 &winId) {
    return ((m_nUserId == nId) && (m_nWindowId == winId));
}

/**
 * @brief ClientFileSocket::startTransferFile
 * 下发文件
 * @param type 0 表示单纯的语音文件，1表示文字+语音，客户端只收不显示
 * @param fileName  文件名
 */
void ClientFileSocket::StartTransferFile(QString fileName)
{
    if (m_bBusy) return;

    if (!m_tcpSocket->isOpen()) {
        return;
    }

    // 要发送的文件
    fileToSend = new QFile((-2 == m_nWindowId ? MyApp::m_strHeadPath : MyApp::m_strRecvPath) + fileName);

    if (!fileToSend->open(QFile::ReadOnly))
    {
        qDebug() << "open file error!";
        return;
    }

    ullSendTotalBytes = fileToSend->size(); // 文件总大小

    QDataStream sendOut(&outBlock, QIODevice::WriteOnly);
    sendOut.setVersion(QDataStream::Qt_4_8);

    QString currentFileName = fileName.right(fileName.size() - fileName.lastIndexOf('/')-1);

    // 依次写入总大小信息空间，文件名大小信息空间，文件名
    sendOut << qint64(0) << qint64(0) << currentFileName;

    // 这里的总大小是文件名大小等信息和实际文件大小的总和
    ullSendTotalBytes += outBlock.size();

    // 返回outBolock的开始，用实际的大小信息代替两个qint64(0)空间
    sendOut.device()->seek(0);
    sendOut << ullSendTotalBytes << qint64((outBlock.size() - sizeof(qint64)*2));

    // 发送完头数据后剩余数据的大小
    bytesToWrite = ullSendTotalBytes - m_tcpSocket->write(outBlock);

    outBlock.resize(0);
    m_bBusy = true;
    qDebug() << "Begin to send file" << fileName << m_nUserId << m_nWindowId;
}

/**
 * @brief ClientFileSocket::SltUpdateClientProgress
 * @param numBytes
 */
void ClientFileSocket::SltUpdateClientProgress(qint64 numBytes)
{
    // 已经发送数据的大小
    bytesWritten += (int)numBytes;
    // 如果已经发送了数据
    if (bytesToWrite > 0)
    {
        // 每次发送loadSize大小的数据，这里设置为4KB，如果剩余的数据不足4KB，就发送剩余数据的大小
        outBlock = fileToSend->read(qMin(bytesToWrite, loadSize));

        // 发送完一次数据后还剩余数据的大小
        bytesToWrite -= (int)m_tcpSocket->write(outBlock);

        // 清空发送缓冲区
        outBlock.resize(0);
    }
    else
    {
        // 如果没有发送任何数据，则关闭文件
        if (fileToSend->isOpen())
            fileToSend->close();
    }

    // 发送完毕
    if (bytesWritten >= ullSendTotalBytes)
    {
        if (fileToSend->isOpen())
            fileToSend->close();

        bytesWritten = 0;  // clear fot next send
        ullSendTotalBytes = 0;
        bytesToWrite = 0;
        qDebug() << "send ok" << fileToSend->fileName();
        FileTransFinished();
    }
}

void ClientFileSocket::displayError(QAbstractSocket::SocketError)
{
    m_tcpSocket->abort();
}

void ClientFileSocket::FileTransFinished()
{
    ullSendTotalBytes   = 0;
    ullRecvTotalBytes   = 0;
    bytesWritten        = 0;
    bytesToWrite        = 0;
    bytesReceived       = 0;

    fileNameSize        = 0;
    m_bBusy = false;
}
```

由上代码可见，该类实现类两个功能，分别为文件的接收和下发。

**文件下发**，两步完成。两步间通过`m_tcpSocket, SIGNAL(bytesWritten(qint64))`信号来连接，即第一步发送成功后会触发该信号，以此**达到顺序发送的目的**。

a. 发送信息总长度、文件名长度、文件名。用`QDataStream`来加载缓冲数据`outBlock`。

```c++
QString currentFileName = fileName.right(fileName.size() - fileName.lastIndexOf('/')-1);

QDataStream sendOut(&outBlock, QIODevice::WriteOnly);
sendOut.setVersion(QDataStream::Qt_4_8);
// 依次写入总大小信息空间，文件名大小信息空间，文件名
sendOut << qint64(0) << qint64(0) << currentFileName;
// 这里的总大小是文件名大小等信息和实际文件大小的总和
ullSendTotalBytes += outBlock.size();
// 返回outBolock的开始，用实际的大小信息代替两个qint64(0)空间
sendOut.device()->seek(0);
sendOut << ullSendTotalBytes << qint64((outBlock.size() - sizeof(qint64)*2));
// 发送完头数据后剩余数据的大小
bytesToWrite = ullSendTotalBytes - m_tcpSocket->write(outBlock);

outBlock.resize(0);
```

b. 发送文件内容。通过`outBlock = fileToSend->read(qMin(bytesToWrite, loadSize));`完成缓存写入

```c++
// 已经发送数据的大小
bytesWritten += (int)numBytes;
// bytesToWrite剩余数据长度判定
if (bytesToWrite > 0)
{
    // 每次发送loadSize大小的数据，这里设置为4KB，如果剩余的数据不足4KB，就发送剩余数据的大小
    outBlock = fileToSend->read(qMin(bytesToWrite, loadSize));

    // 发送完一次数据后还剩余数据的大小
    bytesToWrite -= (int)m_tcpSocket->write(outBlock);

    // 清空发送缓冲区
    outBlock.resize(0);
}
// 发送完成判断，如果发送完成则关闭文件
if (bytesWritten >= ullSendTotalBytes)
{
    if (fileToSend->isOpen())
        fileToSend->close();

    qDebug() << "send ok" << fileToSend->fileName();
    FileTransFinished();
}
```

**文件接收**。分三步

1. 接收`in >> m_nUserId >> m_nWindowId;`用户ID和窗口用户ID
2. 接收`in >> ullRecvTotalBytes >> fileNameSize;`和`in >> fileReadName;`。含义同发送数据头信息
3. 接收文件数据。`fileToRecv->write(inBlock);`。
4. 最后，关闭文件。初始化相关参数

```c++
// 更新进度条，实现文件的接收
void ClientFileSocket::SltReadyRead()
{
    QDataStream in(m_tcpSocket);
    in.setVersion(QDataStream::Qt_4_8);

    // 连接时的消息
    if (0 == bytesReceived && (-1 == m_nUserId) && (-1 == m_nWindowId) &&
            (m_tcpSocket->bytesAvailable() == (sizeof(qint32) * 2)))
    {
        // 保存ID，方便发送文件
        in >> m_nUserId >> m_nWindowId;
        qDebug() << "File server Get userId" << m_nUserId << m_nWindowId;
        Q_EMIT signalConnected();
        return;
    }

    // 如果接收到的数据小于等于20个字节，那么是刚开始接收数据，我们保存为头文件信息
    if (bytesReceived <= (sizeof(qint64)*2))
    {
        int nlen = sizeof(qint64) * 2;
        // 接收数据总大小信息和文件名大小信息
        if ((m_tcpSocket->bytesAvailable() >= nlen) && (fileNameSize == 0))
        {
            in >> ullRecvTotalBytes >> fileNameSize;
            if (0 != ullRecvTotalBytes) bytesReceived += nlen;
        }

        // 接收文件名，并建立文件
        if((m_tcpSocket->bytesAvailable() >= (qint64)fileNameSize) &&
                ((qint64)fileNameSize != 0) &&
                (0 != ullRecvTotalBytes))
        {
            in >> fileReadName;
            bytesReceived += fileNameSize;

            fileToRecv->setFileName((-2 == m_nWindowId ? MyApp::m_strHeadPath : MyApp::m_strRecvPath) + fileReadName);

            if (!fileToRecv->open(QFile::WriteOnly | QIODevice::Truncate))
            {
                qDebug() << "open file error" << fileReadName;
                return;
            }
            qDebug() << "begin to recv files" << fileReadName;
        }
    }

    //如果接收的数据小于总数据，那么写入文件
    if (bytesReceived < ullRecvTotalBytes)
    {
        bytesReceived += m_tcpSocket->bytesAvailable();
        inBlock = m_tcpSocket->readAll();

        if (fileToRecv->isOpen())
            fileToRecv->write(inBlock);

        inBlock.resize(0);
    }

    // 接收数据完成时
    if ((bytesReceived >= ullRecvTotalBytes) && (0 != ullRecvTotalBytes))
    {
        fileToRecv->close();
        bytesReceived = 0; // clear for next receive
        ullRecvTotalBytes = 0;
        fileNameSize = 0;
        qDebug() << "recv ok" << fileToRecv->fileName();
        // 数据接受完成
        FileTransFinished();
    }
}
```

### 2.3 CMessageBox

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\1555983367133.png)

```c++
// 此处仅给出类内容，具体实现暂不给出。因为比较简单。
class CustomDialog : public QDialog {
    Q_OBJECT
public:
    explicit CustomDialog(QWidget *parent = 0);
    ~CustomDialog();

protected:
    QPoint mousePoint;
    bool m_mousePressed;

    void mouseMoveEvent(QMouseEvent *e);
    void mousePressEvent(QMouseEvent *e);
    void mouseReleaseEvent(QMouseEvent *);
};
```

```c++
class CBaseDialog : public CustomDialog {
    Q_OBJECT
public:
    explicit CBaseDialog(QWidget *parent = 0);
    ~CBaseDialog();
    
    void SetWinIcon(QPixmap pixmap);
    void SetWinTitle(const QString &text);
private:
    QWidget         *widgetWinTitle;
    QLabel          *labelWinIcon;
    QLabel          *labelWinTitle;
    QPushButton     *btnWinMin;
    QPushButton     *btnWinClose;

protected:
    QWidget         *widgetBody;
};
```

```c++
class CMessageBox : public CBaseDialog
{
    Q_OBJECT
public:
    typedef enum {		// 消息会话框类型
        Information =  0x01,		//消息通知
        Warnings,					//警告
        Questions,					//询问
        Error,						//错误
    } E_MSGTYPE;

public:
    explicit CMessageBox(QWidget *parent = 0);
    ~CMessageBox();

    // 显示消息。content:信息内容；msgType:会话框类型；title:会话框标题
    void ShowMessage(const QString &content, const quint8 &msgType = CMessageBox::Information, const QString &title = "");
    void StartTimer();

    static int Infomation(QWidget *parent, const QString &content, 
    						const QString &title = "提示");
    static int Question(QWidget *parent, const QString &content, 
    						const QString &title = "询问");
    static int Warning(QWidget *parent, const QString &content, 
    						const QString &title = "告警");
private:
    QLabel      *labelIcon;
    QLabel      *labelMsgContent;

    QPushButton *btnOk;
    QPushButton *btnCancel;

    QTimer      *m_timer;
    int         m_nTimerCnt;
public slots:
    void SltTimerOut();
};

```

### 2.4 QStackedWidget

QStackedWidget继承自QFrame。

QStackedWidget类提供了多页面切换的布局，一次只能看到一个界面。

QStackedWidget可用于创建类似于QTabWidget提供的用户界面。

```c++
QPushButton *pButton = new QPushButton(this);
QLabel *pFirstPage= new QLabel(this);
QLabel *pSecondPage = new QLabel(this);
QLabel *pThirdPage = new QLabel(this);
m_pStackedWidget = new QStackedWidget(this);

pButton->setText(QStringLiteral("点击切换"));
pFirstPage->setText(QStringLiteral("一去丶二三里"));
pSecondPage->setText(QStringLiteral("青春不老，奋斗不止！"));
pThirdPage->setText(QStringLiteral("纯正开源之美，有趣、好玩、靠谱。。。"));

// 添加页面（用于切换）
m_pStackedWidget->addWidget(pFirstPage);
m_pStackedWidget->addWidget(pSecondPage);
m_pStackedWidget->addWidget(pThirdPage);

QVBoxLayout *pLayout = new QVBoxLayout();
pLayout->addWidget(pButton, 0, Qt::AlignLeft | Qt::AlignVCenter);
pLayout->addWidget(m_pStackedWidget);
pLayout->setSpacing(10);
pLayout->setContentsMargins(10, 10, 10, 10);
setLayout(pLayout);

// 连接切换按钮信号与槽
connect(pButton, &QPushButton::clicked, this, &MainWindow::switchPage);

// 切换页面
void MainWindow::switchPage()
{
    int nCount = m_pStackedWidget->count();
    int nIndex = m_pStackedWidget->currentIndex();

    // 获取下一个需要显示的页面索引
    ++nIndex;

    // 当需要显示的页面索引大于等于总页面时，切换至首页
    if (nIndex >= nCount)
        nIndex = 0;

    m_pStackedWidget->setCurrentIndex(nIndex);
}
```

#### 接口

- int addWidget(QWidget * widget)

  添加页面，并返回页面对应的索引

- int count() const

  获取页面数量

- int currentIndex() const

  获取当前页面的索引

- QWidget * currentWidget() const

  获取当前页面

- int indexOf(QWidget * widget) const

  获取QWidget页面所对应的索引

- int insertWidget(int index, QWidget * widget)

  在索引index位置添加页面

- void removeWidget(QWidget * widget)

  移除QWidget页面，并没有被删除，只是从布局中移动，从而被隐藏。

- QWidget * widget(int index) const

  获取索引index所对应的页面

#### 信号

- void currentChanged(int index)

  当前页面发生变化时候发射，index为新的索引值

- void widgetRemoved(int index)

  页面被移除时候发射，index为页面对应的索引值

#### 共有槽函数

- void setCurrentIndex(int index)

  设置索引index所在的页面为当前页面

- void setCurrentWidget(QWidget * widget)

  设置QWidget页面为当前页面

#### 总结

一般情况，常用的两种方式：

- 根据currentWidget()来判断当前页面，然后通过setCurrentWidget()来设置需要显示的页面。
- 根据currentIndex()来判断当前页面索引，然后通过setCurrentIndex()来设置需要显示的页面。

### 2.5 样式

```css
*{	font-family: "微软雅黑"; }

/*主界面样式*/
QWidget#MainWindow {		//主界面
    border: 1px solid #A5A6A8;
    border-radius: 2px;
    background-color: #4A7ABB;
    /*background-image: url(:/resource/background/background.png);*/
}
QWidget#LoginWidget {		//登录界面背景
   background-image: url(:/resource/background/background.png);
}
QWidget#widgetUser {		//登录界面输入
    background-color: #50F1F2;
    border: 1px solid #4A7ABB;
    border-radius: 2px;
}
QWidget#widgetWinTitle {	//窗口抬头
    background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #387ECC,stop:1 #3869C4);
}
QWidget#widgetnav {
    background-color: #4A7ABB;
}

QWidget#widgetBody {
    background-color: #4A7ABB;
}

QWidget#widgetStatus {
    background-color: #666666;
}

QWidget#widgetStatus QLabel {
    color: #FFFFFF;
    font: 14px;
}

QStackedWidget#stackedWidgetFunc {
    background-color: #FFFFFF;
}

QWidget#widgetWinTitle QLabel {
    color: #FFFFFF;
    font: bold 16px;
    font-family: "幼圆";
}

QPushButton#btnWinMin,QPushButton#btnWinClose, QPushButton#btnWinMenu {
    border: none;
    border-radius: 0px;
    background-color: transparent;
    min-width: 24px;
    min-height: 24px;
}

QPushButton#btnWinMin:hover {
    padding-top: 2px;
    border: 1px solid #FFFFFF;
}

QPushButton#btnWinClose:hover {
    padding-top: 2px;
    background-color: #FF0000;
}
/*end 主界面样式 end*/

/*滚动条样式*/
QScrollBar:horizontal{
    background:#C7E5D6;
    padding:0px;
    border-radius:6px;
    max-height:12px;
}

QScrollBar::handle:horizontal{
    background:#9FB7AB;
    min-width:50px;
    border-radius:6px;
}

QScrollBar::handle:horizontal:hover{
    background:#5F6E66;
}

QScrollBar::handle:horizontal:pressed{
    background:#5F6E66;
}

QScrollBar::add-page:horizontal{
    background:none;
}

QScrollBar::sub-page:horizontal{
    background:none;
}

QScrollBar::add-line:horizontal{
    background:none;
}

QScrollBar::sub-line:horizontal{
    background:none;
}

QScrollBar:vertical{
    background:#C7E5D6;
    padding:0px;
    border-radius:6px;
    max-width:12px;
}

QScrollBar::handle:vertical{
    background:#9FB7AB;
    min-height:50px;
    border-radius:6px;
}

QScrollBar::handle:vertical:hover{
    background:#5F6E66;
}

QScrollBar::handle:vertical:pressed{
    background:#5F6E66;
}

QScrollBar::add-page:vertical{
    background:none;
}

QScrollBar::sub-page:vertical{
    background:none;
}

QScrollBar::add-line:vertical{
    background:none;
}

QScrollBar::sub-line:vertical{
    background:none;
}

QScrollArea{
    border:0px;
}
/*end 滚动条样式 end*/

/*系统菜单条样式*/
QMenu{
    color:#000000;
    background-color:#EDEEEE;
    margin:0px;
    padding:3px 10px;
}

QMenu:disabled{
    color:#000000;
    background-color:#FFFFFF;
    border:1px solid #A8B2AC;
    margin:0px;
}

QMenu::item{
    padding: 3px 20px;
}

QMenu::indicator{
    width: 13px;
    height: 13px;
}

QMenu::item:selected,QMenuBar::item:selected{
    color: #FFFFFF;
    border: 0px solid #9FB7AB;
    background-color: #009BDB;
}

QMenu::separator{
    height: 1px;
    background-color: #B5C1CA;
}

/*end 系统菜单样式 end*/


/* 登录界面样式 */
QPushButton {
    border: 1px solid #666666;
    border-radius: 2px;
    background: #FFFFFF;
    color: #000000;
    font: 12px;
    padding-top: 0px;
    min-width: 80px;
    min-height: 27px;
}

QPushButton:hover {
    color: #333333;
    padding-top: 2px;
}


QWidget#widgetNav QPushButton {
    border: none;
    border-radius: 0px;
    background-color: none;
    color: #FFFFFF;
    font: bold 14px;
    min-width: 120px;
    min-height: 40px;
}

QWidget#widgetNav QPushButton:hover {
    border: 1px solid #03D303;
}

QWidget#widgetNav QPushButton:checked {
    border: 1px solid #D3D3D3;
}

QWidget#widgetNav QPushButton:pressed {
    border: 1px solid #D3D3D3;
}


QLineEdit {
    border: 1px solid #D1D1D1;
    min-height: 22px;
    background-color: #FFFFFF;
}

QLineEdit:focus {
    border: 1px solid #1583DD;
}

```

类同于HTML中的CSS样式格式以及使用方式。

