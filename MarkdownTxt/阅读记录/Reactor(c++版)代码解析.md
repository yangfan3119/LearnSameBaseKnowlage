## 一、Linux下使用epoll实现

[使用C++简单实现reactor模式](https://blog.csdn.net/baidu20008/article/details/41378761?utm_source=blogxgwz9)

### 0 Reactor样例类图

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\1416619195_2170.png)

### 1. Singleton

```c++
#ifndef _SINGLETON_H
#define _SINGLETON_H

template <class T> class Singleton
{
public:
    static inline T* instance();	//必须为静态的
    void release();
protected:
    Singleton(){}
    ~Singleton(){}
    T* _instance;
}
template<class T>
inline T* Singleton<T>::instance()	// 获取单例模式内部变量
{
    if(!_instance)
        _instance = new T;
    return _instance;
}
template<class T>
void Singleton<T>::release()	// 删除该对象指针
{
    if(!_instance)
        return;
    delete _instance;
    _instance = 0;
}
#define DECLARE_SINGLETON_MEMBER(_Ty) \
		template <> _Ty* Singleton<_Ty>::_instance = NULL;	// 初始化

#endif//_SINGLETON_H
```

单态模式模板父类。

### 2. Global

```c++
// global.h 文件
#include "reactor.h"		// 与Reactor形成组合关系，统领所有反应堆(Reactor)操作
#include "singleton.h"		// 与Singleton形成泛化继承关系

class reactor::Reactor;
class Global : public Singleton<Global>
{
public:
    Global(void);
    ~Global(void);

    reactor::Reactor* g_reactor_ptr;	//成员变量反应堆指针
};
#define sGlobal Global::instance()
```

```c++
// global.cc 文件
#include "global.h"
DECLARE_SINGLETON_MEMBER(Global);
Global::Global(void)
{
    g_reactor_ptr = new reactor::Reactor();
}
Global::~Global(void)
{
    delete g_reactor_ptr;
    g_reactor_ptr = NULL;
}
```

### 3. Reactor

```c++
//Reactor命名空间
namespace reactor{
    typedef unsigned int event_t;
    typedef int handle_t;
    enum {
        kReadEvent    = 0x01,
        kWriteEvent   = 0x02,
        kErrorEvent   = 0x04,
        kEventMask    = 0xff
    };
    //该命名空间包含的类
    class EventHandler;	
    class Reactor;
    class ReactorImplementation;
    class EventDemultiplexer;
    class EpollDemultiplexer : public EventDemultiplexer;
}
```

```c++
// 类声明
class ReactorImplementation;	// 某一类反应堆
class Reactor	// 反应堆 堆容器
{
public:
    Reactor();
    ~Reactor();
    
    int RegisterHandler(EventHandler * handler, event_t evt);	//事件注册
    int RemoveHandler(EventHandler * handler);	//事件删除
    void HandleEvents();	//事件执行
    int RegisterTimerTask(heap_timer* timerevent);	//定时事件
private:
    Reactor(const Reactor &);
    Reactor & operator=(const Reactor &);
private:
    ReactorImplementation * m_reactor_impl;	//某一个事件堆指针
};
```

```c++
Reactor::Reactor()
{
    m_reactor_impl = new ReactorImplementation();
}
Reactor::~Reactor()
{
    delete m_reactor_impl;
}
int Reactor::RegisterHandler(EventHandler * handler, event_t evt)
{
    return m_reactor_impl->RegisterHandler(handler, evt);
}
int Reactor::RemoveHandler(EventHandler * handler)
{
    return m_reactor_impl->RemoveHandler(handler);
}
void Reactor::HandleEvents()
{
    m_reactor_impl->HandleEvents();
}
int Reactor::RegisterTimerTask(heap_timer* timerevent)
{
    return m_reactor_impl->RegisterTimerTask(timerevent);
}
```

由上实现内容可知当前Reactor与m_reactor_impl是组合关系，生命周期一致。且该堆容器的使用就是对事件类的执行。

### 4.ReactorImplementation

```c++
class ReactorImplementation		//主体接口同Reactor保持一致
{
public:
    ReactorImplementation();
    ~ReactorImplementation();

    int RegisterHandler(EventHandler * handler, event_t evt);
    int RemoveHandler(EventHandler * handler);
    void HandleEvents();
    int RegisterTimerTask(heap_timer* timerevent);
private:
    EventDemultiplexer *                m_demultiplexer;	//Epoll处理接口
    std::map<handle_t, EventHandler *>  m_handlers;		//事件及句柄容器
    time_heap* m_eventtimer;							//定时器容器
};
```

```c++
ReactorImplementation::ReactorImplementation()
{
    m_demultiplexer = new EpollDemultiplexer();	//具体的Epoll处理类
    m_eventtimer = new time_heap(INITSIZE);		//定时器容器创建 INITSIZE=100
}
ReactorImplementation::~ReactorImplementation()
{
    delete m_demultiplexer;
}

int ReactorImplementation::RegisterHandler(EventHandler * handler, event_t evt)
{
    handle_t handle = handler->GetHandle();
    std::map<handle_t, EventHandler *>::iterator it = m_handlers.find(handle);
    if (it == m_handlers.end())	//事件未注册时则注册否则直接返回
    {
        m_handlers[handle] = handler;
    }
    return m_demultiplexer->RequestEvent(handle, evt); //返回Epoll注册是否成功
}
int ReactorImplementation::RemoveHandler(EventHandler * handler)
{
    handle_t handle = handler->GetHandle();
    m_handlers.erase(handle);
    return m_demultiplexer->UnrequestEvent(handle);	//返回Epoll删除是否成功
}
//parm timeout is useless.
void ReactorImplementation::HandleEvents()	//执行
{
    int timeout = 0;	//定时器部分
    if (m_eventtimer->top() == NULL)
    {
        timeout = 0;
    }
    else
    {
        timeout = ((m_eventtimer->top())->expire - time(NULL)) * 1000;
    }
    m_demultiplexer->WaitEvents(&m_handlers, timeout, m_eventtimer);//执行
}
int ReactorImplementation::RegisterTimerTask(heap_timer* timerevent)//添加定时器任务
{
    if (timerevent == NULL)
        return -1;
    m_eventtimer->add_timer(timerevent);
    return 0;
}
```

从类图中可见该类**依赖于**`EventDemultiplexer`和`time_heap`，其作用分别时执行处理以及定时器。

定时器部分的实现如下

```c++
// m_demultiplexer->WaitEvents 传入定时器
int EpollDemultiplexer::WaitEvents(
    std::map<handle_t, EventHandler *> * handlers,
    int timeout, time_heap* event_timer)
{
    std::vector<epoll_event> ep_evts(m_fd_num);
    int num = epoll_wait(m_epoll_fd, &ep_evts[0], ep_evts.size(), timeout);
    if (num > 0) { /*有任务时处理，执行部分*/ }
    if (event_timer != NULL)	//定时器部分
    {
        event_timer->tick();	//遍历定时器中的任务并判断是否超时，超时则执行定时器中的任务
    }
    return num;
}
```

```c++
// 定时器类
class heap_timer
{
public:
    heap_timer( int delay )
    {
        expire = time( NULL ) + delay; //超时时间
    }
public:
   time_t expire;
   void (*cb_func)( client_data* );	//超时任务
   client_data* user_data;	//超时任务的参数
};
```

### 5. EventHandle

```c++
class EventHandler //事件抽象类
{
public:
    virtual handle_t GetHandle() const = 0;
    virtual void HandleRead() {}
    virtual void HandleWrite() {}
    virtual void HandleError() {}

protected:
    EventHandler() {}
    virtual ~EventHandler() {}
};
```

### 6. TimeClient

```c++
reactor::Reactor g_reactor; //事件堆初始化定义

const size_t kBufferSize = 1024;
char g_read_buffer[kBufferSize];
char g_write_buffer[kBufferSize];

class TimeClient : public reactor::EventHandler
{
public:
    TimeClient() : EventHandler()
    {
        m_handle = socket(AF_INET, SOCK_STREAM, 0); //事件句柄为socket连接
        assert(IsValidHandle(m_handle));	//断言是否创建成功
    }
    ~TimeClient() { close(m_handle); }	//析构函数中关闭该链接
    
    bool ConnectServer(const char * ip, unsigned short port) //外部初始化连接接口
    {
        struct sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        addr.sin_addr.s_addr = inet_addr(ip);
        if (connect(m_handle, (struct sockaddr *)&addr, sizeof(addr)) < 0)
        {
            ReportSocketError("connect");
            return false;
        }
        return true;
    }
    virtual reactor::handle_t GetHandle() const
    {
        return m_handle;
    }
    virtual void HandleRead()
    {
        memset(g_read_buffer, 0, kBufferSize);
        int len = recv(m_handle, g_read_buffer, kBufferSize, 0);
        if (len > 0)
        {
            fprintf(stderr, "%s", g_read_buffer);
            g_reactor.RegisterHandler(this, reactor::kWriteEvent);
        }
        else // Error输出
    }
    virtual void HandleWrite()
    {
        memset(g_write_buffer, 0, kBufferSize);
        int len = sprintf(g_write_buffer, "time\r\n");
        len = send(m_handle, g_write_buffer, len, 0);
        if (len > 0)
        {
            fprintf(stderr, "%s", g_write_buffer);
            g_reactor.RegisterHandler(this, reactor::kReadEvent);
        }
        else // Error输出
    }
    virtual void HandleError() //错误时
    {
        close(m_handle);
        exit(0);
    }
private:
    reactor::handle_t  m_handle; //在c++中，句柄均为整型数据
};
```

该事件的应用如下

```c++
TimeClient client; //创建该事件
client.ConnectServer(argv[1], atoi(argv[2])); //socket连接，此处应该有执行是否成功的判断
g_reactor.RegisterHandler(&client, reactor::kWriteEvent); //注册，WriteEvent为写入信号
while (1)
{
    g_reactor.HandleEvents();	//执行事件
    sleep(1);
}
g_reactor.RemoveHandler(&client); //注销该事件类
```

跟踪如上事件反映如下：

```
1. main函数中先手注册 client,kWriteEvent 信号

2. g_reactor.HandleEvents();//执行事件 ，此处执行map中的 client,kWriteEvent 事件
3. 执行client对象的HandleWrite()函数 
4. client::HandleWrite()发送完成后再注册 client,kReadEvent 信号

5. g_reactor.HandleEvents();//执行事件 ，此处执行map中的 client,kReadEvent 事件
6. 执行client对象的HandleRead()函数 
7. client::HandleRead()读取到结果后再注册 client,kWriteEvent 信号

8. g_reactor.HandleEvents();//执行事件 ，此处执行map中的 client,kWriteEvent 事件
	...		又类同于步骤2
```

由如上步骤分析可见，事件信号的注册和执行是分开的，通过统一的Reactor来管理多个事件以及多个信号

### 7. reactor_server_test.cc文件

```c++
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <assert.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#include <string>

#include "test_common.h"
#include "global.h"

//reactor::Reactor g_reactor;
#define g_reactor (*(sGlobal->g_reactor_ptr))

const size_t kBufferSize = 1024;
char g_read_buffer[kBufferSize];
char g_write_buffer[kBufferSize];

// socket服务器监听到的一个链路句柄操作
class RequestHandler : public reactor::EventHandler
{
public:
    RequestHandler(reactor::handle_t handle) :
        EventHandler(),
        m_handle(handle)
    {}

    virtual reactor::handle_t GetHandle() const
    {
        return m_handle;
    }

    virtual void HandleWrite()
    {
        struct tm *ttime;
        char now[64];
        time_t tt;

        memset(now, 0, 64);
        tt = time(NULL);
        ttime = localtime(&tt);
        strftime(now, 64, "%Y-%m-%d %H:%M:%S", ttime);        

        memset(g_write_buffer, 0, sizeof(g_write_buffer));
        int len = sprintf(g_write_buffer, "current time: %s\r\n", now);
        len = send(m_handle, g_write_buffer, len, 0);
        if (len > 0)
        {
            fprintf(stderr, "send response to client, fd=%d\n", (int)m_handle);
            g_reactor.RegisterHandler(this, reactor::kReadEvent);
        }
        else
        {
            ReportSocketError("send");
        }
    }

    virtual void HandleRead()
    {
        memset(g_read_buffer, 0, sizeof(g_read_buffer));
        int len = recv(m_handle, g_read_buffer, kBufferSize, 0);
        if (len > 0)
        {
            if (strncasecmp("time", g_read_buffer, 4) == 0)
            {
                g_reactor.RegisterHandler(this, reactor::kWriteEvent);
            }
            else if (strncasecmp("exit", g_read_buffer, 4) == 0)
            {
                close(m_handle);
                g_reactor.RemoveHandler(this);
                delete this;
            }
            else
            {
                fprintf(stderr, "Invalid request: %s", g_read_buffer);
                close(m_handle);
                g_reactor.RemoveHandler(this);
                delete this;
            }
        }
        else
        {
            ReportSocketError("recv");
        }
    }

    virtual void HandleError()
    {
        fprintf(stderr, "client %d closed\n", m_handle);
        close(m_handle);
        g_reactor.RemoveHandler(this);
        delete this;
    }

private:

    reactor::handle_t m_handle;
};

class TimeServer : public reactor::EventHandler
{
public:

    TimeServer(const char * ip, unsigned short port) :
        EventHandler(),
        m_ip(ip),
        m_port(port)
    {}

    bool Start()
    {
        m_handle = socket(AF_INET, SOCK_STREAM, 0);
        if (!IsValidHandle(m_handle))
        {
            ReportSocketError("socket");
            return false;
        }

        struct sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_port = htons(m_port);
        addr.sin_addr.s_addr = inet_addr(m_ip.c_str());
        if (bind(m_handle, (struct sockaddr *)&addr, sizeof(addr)) < 0)
        {
            ReportSocketError("bind");
            return false;
        }

        if (listen(m_handle, 10) < 0)
        {
            ReportSocketError("listen");
            return false;
        }
        return true;
    }

    virtual reactor::handle_t GetHandle() const
    {
        return m_handle;
    }

    virtual void HandleRead()
    {
        struct sockaddr addr;
        socklen_t addrlen = sizeof(addr);
        reactor::handle_t handle = accept(m_handle, &addr, &addrlen);
        if (!IsValidHandle(handle))
        {
            ReportSocketError("accept");
        }
        else
        {
            RequestHandler * handler = new RequestHandler(handle);
            if (g_reactor.RegisterHandler(handler, reactor::kReadEvent) != 0)
            {
                fprintf(stderr, "error: register handler failed\n");
                delete handler;
            }
        }
    }

private:

    reactor::handle_t     m_handle;
    std::string           m_ip;
    unsigned short        m_port;
};

void printHelloworld(client_data* data)
{
    fprintf(stderr, "timertask : Hello world from timerTask!\n");
}

int main(int argc, char ** argv)
{
    if (argc < 3)
    {
        fprintf(stderr, "usage: %s ip port\n", argv[0]);
        return EXIT_FAILURE;
    }

    TimeServer server(argv[1], atoi(argv[2]));
    if (!server.Start())
    {
        fprintf(stderr, "start server failed\n");
        return EXIT_FAILURE;
    }
    fprintf(stderr, "server started!\n");

    heap_timer* printtask = new heap_timer(5);
    printtask->cb_func = printHelloworld;

    fprintf(stderr, "register a task which will be run is five seconds!\n");
    g_reactor.RegisterTimerTask(printtask);

    while (1)
    {
        g_reactor.RegisterHandler(&server, reactor::kReadEvent);
        g_reactor.HandleEvents();
    }
    return EXIT_SUCCESS;
}
```

---

## 二、epoll延伸

### 2.1 简述

**Epoll：**当前非常出色的**IO多路复用**技术，同样Epoll 是一种高效的管理socket的模型。

**优点：**

> 1. epoll没有最大并发连接的限制，上限是最大可以打开文件的数目，这个数字一般远大于2048, 一般来说这个数目和系统内存关系很大，具体数目可以cat /proc/sys/fs/file-max察看。
> 2. 效率提升，Epoll最大的优点就在于它只管你“活跃”的连接，而跟连接总数无关，因此在实际的网络环境中，Epoll的效率就会远远高于select和poll。
> 3. 内存拷贝，Epoll在这点上使用了“共享内存”，这个内存拷贝也省略了。

```c
// 基本接口
// epoll_create建立一个epoll对象。参数size是内核保证能够正确处理的最大句柄数
int epoll_create(int size);	
// 操作事件句柄，增删改
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);
// epoll_wait在调用时，在给定的timeout时间内，当在监控的所有句柄中有事件发生时，就返回用户态的进程。
int epoll_wait(int epfd, struct epoll_event *events,int maxevents, int timeout);

// 基本数据机构
typedef union epoll_data {
    void ptr;
    int fd;
    __uint32_t u32;
    __uint64_t u64;
} epoll_data_t;

struct epoll_event {
    __uint32_t events;    / Epoll events /
        epoll_data_t data;    / User data variable /
};
```

### 2.2 c++简单示例代码

```c
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<assert.h>
#include<stdio.h>
#include<unistd.h>
#include<errno.h>
#include<string.h>
#include<fcntl.h>
#include<stdlib.h>
#include<sys/epoll.h>
#include<pthread.h>
#include<iostream>
#define MAX_EVENT_NUMBER 1024//最大事件连接数
#define BUFFER_SIZE 1024//接收缓冲区大小
using namespace std;
struct fds{//文件描述符结构体，用作传递给子线程的参数
    int epollfd;
    int sockfd;
};
int setnonblocking(int fd){//设置文件描述符为非阻塞
    int old_option=fcntl(fd,F_GETFL);
    int new_option=old_option|O_NONBLOCK;
    fcntl(fd,F_SETFL,new_option);
    return old_option;
}
void addfd(int epollfd,int fd,bool oneshot){//为文件描述符添加事件
    epoll_event event;
    event.data.fd=fd;
    event.events=EPOLLIN|EPOLLET;
    if(oneshot){//采用EPOLLONETSHOT事件
        event.events|=EPOLLONESHOT;
    }
    epoll_ctl(epollfd,EPOLL_CTL_ADD,fd,&event);
    setnonblocking(fd);
}
void reset_oneshot(int epollfd,int fd){//重置事件
    epoll_event event;
    event.data.fd=fd;
    event.events=EPOLLIN|EPOLLET|EPOLLONESHOT;
    epoll_ctl(epollfd,EPOLL_CTL_MOD,fd,&event);
}
void* worker(void* arg){//工作者线程(子线程)接收socket上的数据并重置事件
    int sockfd=((fds*)arg)->sockfd;
    int epollfd=((fds*)arg)->epollfd;//事件表描述符从arg参数(结构体fds)得来
    cout<<"start new thread to receive data on fd:"<<sockfd<<endl;
    char buf[BUFFER_SIZE];
    memset(buf,'\0',BUFFER_SIZE);//缓冲区置空
    while(1){
        int ret=recv(sockfd,buf,BUFFER_SIZE-1,0);//接收数据
        if(ret==0){//关闭连接
            close(sockfd);
            cout<<"close "<<sockfd<<endl;
            break;
        }
        else if(ret<0){
            if(errno==EAGAIN){//并非网络出错，而是可以再次注册事件
                reset_oneshot(epollfd,sockfd);
                cout<<"reset epollfd"<<endl;
                break;
            }
        }
        else{
            cout<<buf;
            sleep(5);//采用睡眠是为了在5s内若有新数据到来则该线程继续处理，否则线程退出
        }
    }
    cout<<"thread exit on fd:"<<sockfd;
    //_exit(0);//这个会终止整个进程！！
    return NULL;
}
int main(int argc,char* argv[]){
    if(argc<=2){
        cout<<"argc<=2"<<endl;
        return 1;
    }
    const char* ip=argv[1];
    int port=atoi(argv[2]);
    int ret=0;
    struct sockaddr_in address;
    bzero(&address,sizeof(address));
    address.sin_family=AF_INET;
    inet_pton(AF_INET,ip,&address.sin_addr);
    address.sin_port=htons(port);
    int listenfd=socket(PF_INET,SOCK_STREAM,0);
    assert(listenfd>=0);
    ret=bind(listenfd,(struct sockaddr*)&address,sizeof(address));
    assert(ret!=-1);
    ret=listen(listenfd,5);
    assert(ret!=-1);
    epoll_event events[MAX_EVENT_NUMBER];
    int epollfd=epoll_create(5);
    assert(epollfd!=-1);
    addfd(epollfd,listenfd,false);//不能将监听端口listenfd设置为EPOLLONESHOT否则会丢失客户连接
    while(1){
        int ret=epoll_wait(epollfd,events,MAX_EVENT_NUMBER,-1);//等待事件发生
        if(ret<0){
            cout<<"epoll error"<<endl;
            break;
        }
        for(int i=0;i<ret;i++){
            int sockfd=events[i].data.fd;
            if(sockfd==listenfd){//监听端口
                struct sockaddr_in client_address;
                socklen_t client_addrlength=sizeof(client_address);
                int connfd=accept(listenfd,(struct sockaddr*)&client_address,&client_addrlength);
                addfd(epollfd,connfd,true);//新的客户连接置为EPOLLONESHOT事件
            }
            else if(events[i].events&EPOLLIN){//客户端有数据发送的事件发生
                pthread_t thread;
                fds fds_for_new_worker;
                fds_for_new_worker.epollfd=epollfd;
                fds_for_new_worker.sockfd=sockfd;
                pthread_create(&thread,NULL,worker,(void*)&fds_for_new_worker);//调用工作者线程处理数据
            }
            else{
                cout<<"something wrong"<<endl;
            }
        }
    }
    close(listenfd);
    return 0;
}
```

### 2.3 ET 和 LT

​	epoll独有的两种模式`ET(Edge Triggered)`与`LT(Level Triggered)`。无论是LT和ET模式，都适用于以上所说的流程。区别是，LT模式下，只要一个句柄上的事件一次没有处理完，会在以后调用epoll_wait时次次返回这个句柄，而ET模式仅在第一次返回。

​	这件事怎么做到的呢？当一个socket句柄上有事件时，内核会把该句柄插入上面所说的准备就绪list链表，这时我们调用epoll_wait，会把准备就绪的socket拷贝到用户态内存，然后清空准备就绪list链表，最后，epoll_wait干了件事，就是检查这些socket，如果不是ET模式（就是LT模式的句柄了），并且这些socket上确实有未处理的事件时，又把该句柄放回到刚刚清空的准备就绪链表了。所以，非ET的句柄，只要它上面还有事件，epoll_wait每次都会返回。而ET模式的句柄，除非有新中断到，即使socket上的事件没有处理完，也是不会次次从epoll_wait返回的。

### 2.4 socket复用问题

​	在前面说过，epoll有两种触发的方式即LT（水平触发）和ET（边缘触发）两种，在前者，只要存在着事件就会不断的触发，直到处理完成，而后者只触发一次相同事件或者说只在从非触发到触发两个状态转换的时候儿才触发。这会出现一种情况，**就是即使我们使用ET模式, 一个socket上的某个事件还是可能被触发多次,** 这在并发程序中会引起一个问题.

比如,**一个线程(或者进程)在读取完某个socket上的数据后开始处理这些数据, 而在处理数据的过程中该socket上又有新数据可读(EPOLLIN再次被触发), 此时如果应用程序调度另外一个线程来读取这些数据, 就会出现两个线程同时操作一个socket的局面**, 这会使程序的健壮性大降低而编程的复杂度大大增加. 这显然不是我们所期望的.

解决这种现象有两种方法

- ﻿第一种是在单独的线程或进程里解析数据，也就是说，接收数据的线程接收到数据后立刻将数据转移至另外的线程。
- 第二种方法就是使用EPOLLONESHOT事件. 对于注册了EPOLLONESHOT事件的文件描述符, 操作系统最多触发其上注册的一个可读, 可写或者异常事件, 且只触发一次, 除非我们使用epoll_ctl和函数重置该文件描述符上注册的EPOLLONESHOT事件.

这样, 当一个线程在处理某个socket的时候, 其他线程就不可能有机会操作该socket

但是反过来思考, 注册了EPOLLONESHOT事件的socket一旦被某个线程处理完毕, 该线程就有责任立即**重置**这个socket上的EPOLLONESHOT事件, 以确保这个socket下一次可读的时候, 其EPOLLIN事件能被再次触发, 进而让其他线程有机会处理这个socket.

## 三、I/O延伸

### 3.1 阻塞式I/O模型

​	在阻塞式I/O模型中，数据可读和读取数据这两个操作被合并在了一个系统调用中，对于单个套接字是否可读的判断，必须要等到实际数据接收完成才行，阻塞耗时是不确定的。

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\694961-20160615000203682-1289444499.png)

### 3.2 非阻塞式I/O模型

​	在非阻塞I/O模型中，虽然数据可读和读取数据这两个操作依旧在一个系统调用中，但是如果没有数据可读，系统调用将立即返回一个错误。此时我们可以**对多个连接套接字轮流调用read，直到某次调用收到了实际数据，我们才针对这次收到的数据进行处理**。通过这种方式，我们能够初步解决服务器同时读取多个客户数据的问题。但是这种**在一个线程内对多个非阻塞描述符循环调用read的方式，我们称之为轮询**。应用持续轮询内核，以查看某个操作是否就绪，这往往会消耗大量CPU时间，同时也会给整个服务器带来极大的额外开销。

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\694961-20160615000252120-2128340309.png)

### 3.3 改良非阻塞I/O模型

​	在`非阻塞I/O模型`的基础上增加**多线程**，一个线程管理一路socket客户的读写。即`thread-per-connection`方案。此时对于某一个客户连接操作仅仅影响该路线程而已。此时线程数和连接数为一对一关系。

​	而当有大批量连接时，电脑频繁的创建和销毁线程会造成连接问题。所以该模式不适合频繁的短连接操作。此时可以通过*线程池*来改良该方案。

​	但，终究该方案的**伸缩性受到线程数的限制**，对于存在的一两百个连接而创建的一两百个线程数，系统还能勉强支撑，但是如果同时存在几千个线程的话，这将会对操作系统的调度程序产生极大的负担。同时更多的线程也会对内存大小提出很高的要求。

### 3.4 I/O复用

​	**解决服务器对多个连接套接字的读取的关键，其一是需将可读判断与实际读取数据相分离；其二是能同时支持多个套接字可读判断。因此我们需要一种能够预先告知内核的能力，使得内核一旦发现进程指定的一个或多个I/O条件就绪，即输入已经准备好被读取，它就通知进程。这个行为称之为I/O复用。**

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\694961-20160615000332932-1825735981.png)



​	Epoll是Linux内核为处理大批量文件描述符而做了改进的poll，是Linux下多路复用I/O接口的增强版本，支持水平触发和边缘触发两种方式。相对于select等I/O复用方式，它具有支持大数目的描述符，I/O效率不随注册的描述符数目增加而线性下降（传统的select以及poll的效率会因为注册描述符数量的线形递增而导致呈二次乃至三次方的下降），和使用mmap加速内核与用户空间的消息传递等优点。本系统将采用水平触发的epoll作为具体I/O复用的系统调用。

## 四、Reactor模式

### 4.1 介绍

​	将整个问题抽象。每个已经连接的套接字描述符就是一个事件源，每一个套接字接收到数据后的进一步处理操作作为一个事件处理器。我们将需要被处理的事件处理源及其事件处理器注册到一个类似于epoll的事件分离器中。事件分离器负责等待事件发生。一旦某个事件发送，事件分离器就将该事件传递给该事件注册的对应的处理器，最后由处理器负责完成实际的读写工作。这种方式就是Reactor模式的事件处理方式。

　　相对于之前普通函数调用的事件处理方式，Reactor模式是一种以事件驱动为核心的机制。在Reactor模式中，应用程序不是主动的调用某个API完成处理，而是逆置了事件处理流程，应用程序需要提供相应的事件接口并注册到Reactor上，如果相应的事件发生，Reactor将主动调用应用程序注册的接口，通过注册的接口完成具体的事件处理。

### 4.2 模式优点

Reactor模式是编写高性能网络服务器的必备技术之一，一些常用网络库如libevent、muduo等都是通过使用Reactor模式实现了网络库核心。它具有如下优点：

- 响应速度快，不必为单个同步时间所阻塞，虽然Reactor本身依然是需要同步的；
- 编程简单，可以最大程度的避免复杂的多线程及同步问题，并且避免了多线程/进程的切换开销；
- 可扩展性强，可以很方便的通过增加Reactor实例个数来充分利用CPU资源；
- 可复用性强，Reactor模式本身与具体事件处理逻辑无关，具有很高的复用性。

### 4.3 模式组成

Reactor模式由事件源、事件反应器、事件分离器、事件处理器等组件组成，具体介绍如下：

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\694961-20160615000546026-550521873.png)

- l  事件源（handle）：由操作系统提供，用于识别每一个事件，如Socket描述符、文件描述符等。在服务端系统中用一个整数表示。该事件可能来自外部，如来自客户端的连接请求、数据等。也可能来自内部，如定时器事件。
- l  事件反应器（reactor）：定义和应用程序控制事件调度，以及应用程序注册、删除事件处理器和相关描述符相关的接口。它是事件处理器的调度核心，使用事件分离器来等待事件的发生。一旦事件发生，反应器先是分离每个事件，然后调度具体事件的事件处理器中的回调函数处理事件。
- l  事件分离器（demultiplexer）：是一个有操作系统提供的I/O复用函数，在此我们选用epoll。用来等待一个或多个事件的发生。调用者将会被阻塞，直到分离器分离的描述符集上有事件发生。
- l  事件处理器（even handler）：事件处理程序提供了一组接口，每个接口对应了一种类型的事件，供reactor在相应的事件发生时调用，执行相应的事件处理。一般每个具体的事件处理器总是会绑定一个有效的描述符句柄，用来识别事件和服务

### 4.4 事件处理流程

其一为事件注册部分，其二为事件分发部分，具体论述如下。

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\694961-20160615000644135-1240443370.png)

​	在事件注册部分，应用程序首先将期待注册的套接字描述符作为事件源，并将描述符和该事件对应的事件处理回调函数封装到具体的事件处理器中，并将该事件处理器注册到事件反应器中。事件反应器接收到事件后，进行相应处理，并将注册信息再次注册到事件分离器epoll中。最后在epoll分离器中，通过epoll_ctl进行添加描述符及其事件，并层层返回注册结果。

　　在事件处理部分，首先事件反应器通过调用事件分离器的epoll_wait，使线程阻塞等待注册事件发生。此时如果某注册事件发生，epoll_wait将会返回，并将包含该注册事件在内的事件集返回给事件反应器。反应器接收到该事件后，根据该事件源找到该事件的事件处理器，并判断事件类型，根据事件类型在该事件处理器调用之前注册时封装的具体回调函数，在这个具体回调函数中完成事件处理。

　　根据Reactor模式具体的事件处理流程可知，应用程序只参与了最开始的事件注册部分。对于之后的整个事件等待和处理的流程中，应用程序并不直接参与，最终的事件处理也是委托给了事件反应器进行。因此通过使用Reactor模式，应用程序无需关心事件是怎么来的，是什么时候来的，我们只需在注册事件时设置好相应的处理方式即可。这也反映了设计模式中的“好莱坞原则”，具体事件的处理过程被事件反应器控制反转了。







