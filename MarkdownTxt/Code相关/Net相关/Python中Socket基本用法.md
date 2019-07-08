## Python中的Socket库的基本用法

*python我们熟悉，一种编程语言。socket一种网络连接协议，可以用来实现各种协议，例如TCP、UDP等等。Socket的使用使我们可以便捷的搭建C/S架构的系统，以及其他需要网络支撑的系统。*

*Socket在Python中的应用也是为了实现网络通信的目的，因此熟悉Socket的基本用法就有了必要性*

**此处因为已经熟知并在其他语言上熟悉了Socket的各种通信用法，故而此处不多做详细描述，仅仅贴出详细代码，并根据一个基础课程做一个文件传输的应用。**

### 一、服务器代码

```python
# TCP协议
import Socket

# 实例化服务器，默认参数为tcp协议
sk = socket.socket()
# 定义绑定的ip和port
ip_port = ("127.0.0.1", 8888)
sk.bind(ip_port)
# 最大连接数
sk.listen(5)
# 接收新连接链路
conn, addr = sk.accept()
# 定义信息
Request = "Hello World!"
# 返回信息，3.x以上版本需发送byte类型数据
conn.send(Request.encode())
# 关闭连接
conn.close()
```

```python
# UDP协议下的服务器连接
import socket

sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_port = ("127.0.0.1",8889)
sk.bind(ip_port)
while True:
    data = sk.recv(1024)
    print(data.decode())
```



### 二、客户端代码

```python
# TCP协议
import socket

# 实例化
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 访问服务器的端口和ip
ip_port = ("127.0.0.1",8888)
# 连接主机
client.connect(ip_port)
# 接收主机信息
data = client.recv(1024)
# 打印接收到的数据
# 3.x以上版本接收到的为byte类型数据
print(data.decode())
client.close()
```

```python
# UDP协议下的客户端连接
import socket

sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_port = ("127.0.0.1",8889)
while True:
    msg_input = input("请输入发送消息：")
    if msg_input is None:
        break
    sk.sendto(msg_input.encode(), ip_port)
sk.close()
```



### 三、基本注意事项

#### 3.1 创建

通过**socket.socket(family, type, proto, fileno)**函数来决定链接的类型。可以知道的就是默认是TCP连接，可以进行UDP连接

| family 地址簇   | 含义                               |
| --------------- | ---------------------------------- |
| socket.AF_INET  | IPv4 (默认)                        |
| socket.AF_INET6 | IPV6                               |
| socket.AF_UNIX  | 只能够用于单一的Unix系统进程间通信 |

| type 类型             | 含义                          |
| --------------------- | ----------------------------- |
| socket.SOCK_STREAM    | 流式socket, for TCP（默认）   |
| socket.SOCK_DGRAM     | 数据报文式socket， for UDP    |
| socket.SOCK_RAW       | 原始套接字                    |
| socket.SOCK_RDM       | 可靠UDP形式（会进行数据校验） |
| socket.SOCK_SEQPACKET | 可靠的连续数据包服务          |

| proto: 协议号    | 含义                          |
| ---------------- | ----------------------------- |
| 0                | 默认，可以省略                |
| CAN_RAW、CAN_BCM | 地址簇为AF_CAN，可能是CAN协议 |

#### 3.2 编码

再次注意，传送和接收到的数据均为byte格式。接收之所以是1024个，因为底层链路层存在一个缓存的问题。单条最大通信长度是有限制的，印象中是1100左右，因此此处1024是一个约定俗成的固定值。

#### 3.4 多链路通信

对服务器而言，设定了**sk.listen(5)**，说明最大的连接监听数为5个，但并不意味这可以同时接收5个，可以使用socketServer库来完成多链路的接收问题。也可以自己通过多线程的方式完成该操作。

但是对于UDP连接而言，因为UDP协议是一个短连接，*连接-->发送-->断开*，每一次都是如此。因此可以只开启一个服务器循环就可以，同时接受不同客户端的信息。

```python
# TCP SocketServer多线程非阻塞
import socketserver

class MyServer(socketserver.BaseRequestHandler):
    # 顺序执行setup、handle、finish
    # 参与执行的主题函数为handle，当他执行失败时依然可以继续执行
    def setup(self):
        pass

    def handle(self):
        conn = self.request
        msg = "Hello World!"
        conn.send(msg.encode())
        while True:
            data = conn.recv(1024)
            print(data.decode())
            if data == b'exit':
                break
            reqs = b"Get It:" + data
            conn.send(reqs)

    def finish(self):
        pass

# 主函数
if __name__=="__main__":
    server = socketserver.ThreadingTCPServer(("127.0.0.1",8888), MyServer)
    server.serve_forever()
```

通过**socketserver**库函数就可以实现多线程，非阻塞运行状态下的socket服务器接收发送。

### 四、发送文件

#### 4.1 服务器端

```python
import socket

# 实例化服务器，默认参数为tcp协议
sk = socket.socket()
# 定义绑定的ip和port
ip_port = ("127.0.0.1", 8888)
sk.bind(ip_port)
# 最大连接数
sk.listen(5)
# 接收数据
conn, addr = sk.accept()
finish = True
while finish:
    with open("Mypic.jpg", "ab") as f:
        data = conn.recv(1024)
        if data == b"quit":
            break
        f.write(data)
    conn.send('succ'.encode())
    # print("MySuit", finish)
sk.close()
```



#### 4.2 客户端程序

```python
import socket

# 实例化
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 访问服务器的端口和ip
ip_port = ("127.0.0.1",8888)
# 连接主机
client.connect(ip_port)
# 打开文件
with open("overwatch.jpg", "rb") as f:
    for da in f:
        client.send(da)
        data = client.recv(1024)
        if data != b'succ':
            break
client.send("quit".encode())
client.close()

```



#### 4.3 说明

如上方式耗时比较长，暂时不清楚为什么，可能是文件写入耗时较长，之后会再做调整后验证该问题。

另外关于文件传输过程中的字长和结构也可以做一定的处理。