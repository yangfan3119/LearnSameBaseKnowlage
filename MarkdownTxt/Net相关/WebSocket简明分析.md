---
typora-copy-images-to: ..\mdPic
---

## 一、说明 ##
WebSocket，HTTP协议的一部分，在原有的短连接或者说一问一答的基础上增加的长连接服务，算是补充。
**可用来干什么？**
在web客户端和Web服务器端建立长连接形式，类似于Socket的链接，可以任意收发信息。
**开发过程**
因项目需求使用python开发，因为Web端就是用Django开发的，所以。。。

1. python上开发WebSocket，网上查到的是使用**dwebsocket**库来开发，网上学习了一种使用方式，发现有很多异常无法处理，而且网上的样例实在匮乏，再加上我Web开发短板太多，或者对我而言理解它的使用方式太慢。综上，弃用
    [**dwebsocket库样例连接**](https://www.cnblogs.com/huguodong/p/6611602.html)

2. WebSocket在python上的另一种开发方式，直接使用Socket开发，我们很清楚的知道WebSocket是建立在HTTP上使用TCP协议做的开发，基于此我们完全可以使用Socket来进行WebSocket的开发，区别于C/S模式的开发在于WebSockt的协议上，需要遵循它的标准协议进行连接和通信。**以下我将叙述使用该方式的开发过程**
***
## 二、开发参考链接 ##
非常感谢如下两个链接博客作者对我的帮助：
[JetpropelledSnake21 ：Python Web学习笔记之WebSocket通信过程与实现](https://www.cnblogs.com/JetpropelledSnake/p/9033064.html)
详细说明了WebSocket协议使用Socket开发的过程，博客写的非常棒，但同时有一些细节确实困扰了我很长时间。
[CoderFocus ：原来你是这样的WebSocket](https://www.cnblogs.com/songwenjie/p/8575579.html)
详细说明了通过底层抓包分析WebSocket的过程，解决了很多细节问题。
****
## 三、开发过程
### 3.1 连接
**客户端程序如下**
```javascript
<script type="text/javascript">
        var ws;
        function startWS() {//连接
            console.log('will connect:', document.getElementById('Server_IP').innerHTML);
            ws = new WebSocket('ws://' + document.getElementById('Server_IP').innerHTML + ':9913');
			//9913为创建socket的端口号，可以和网页端口号不同
            ws.onopen = function (msg) {
                console.log('WebSocket opened');
            };
            ws.onmessage = function (message) {//接收消息
                console.log('receive message: ' + message.data);
            };
            ws.onerror = function (error){
                console.log('Error: ' + error.name + error.number);
            };
            ws.onclose = function () {
                console.log('WebSocket closed!');
            };
        }

        function sendMessage() {//发送消息
            console.log('Sending a message...');
            var text = document.getElementById('message');
            if(ws.readyState==1){
                ws.send(text.value);
            } else {
                console.log('WebSocket has Closed!');
            }
        }
        function CloseSocket() {//关闭
            console.log('Close My Socket');
            if(ws.readyState==1){
                ws.close();
            }
        }
        window.onbeforeunload = function () {
            ws.onclose = function () {};
            ws.close();
        }
    </script>
```
**WebSocket通过readyState来判断连接状态**
0 ：CONNECTING，正在建立连接连接，还没有完成。
1 ：OPEN，连接成功建立，可以进行通信。
2 ：CLOSING，连接正在进行关闭握手，即将关闭。
3 : CLOSED，连接已经关闭或者根本没有建立。
### 3.2 建立websocket的握手连接
**客户端创建连接后会发送如下消息**
```
GET / HTTP/1.1
Host: 127.0.0.1:9913
Connection: Upgrade
Pragma: no-cache
Cache-Control: no-cache
Upgrade: websocket
Origin: http://127.0.0.1:9915
Sec-WebSocket-Version: 13
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: csrftoken=W58zlrDnjzaLekwp5i3LCyjf0LkH1k8MnflhHczFZj0g7HhBei266yAqUMCUmTgL; sessionid=fmafra1eoxixqvri982wn20t9ijlm6ve
Sec-WebSocket-Key: pO5nV5UZg1q2wAcE4Hb39g==
Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits

```
**关键信息：Sec-WebSocket-Version和Sec-WebSocket-Key**
**关于版本：** 经过跟踪查询dwebsocket库中的代码发现当前websocket存在两种协议: **safari**和**13**两种版本，此处用新版本即版本号为13的协议作为通讯。
dwebsocket中关于13版本号的协议内容在**protocols.py文件中，类名为：WebSocketProtocol13**，关于连接以及相关的通信协议都可以在其中找到。
**关于秘钥 Sec-WebSocket-Key** 的内容需要做转换处理，代码如下：
```python
#摘自dwebsocket库的protocols.py文件中
def compute_accept_value(key):#key为bytes类型
    """Computes the value for the Sec-WebSocket-Accept header,
    given the value for Sec-WebSocket-Key.
    """
    sha1 = hashlib.sha1()
    sha1.update(key)
    sha1.update(b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11")  # Magic value
    return base64.b64encode(sha1.digest())
```
**服务端返回信息**
```python
#摘自dwebsocket库的protocols.py文件中
def accept_connection(header_key):
	Accept = compute_accept_value(header_key).decode("utf8")
    accept_header = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: WebSocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Accept: %s\r\n"
        "\r\n" % (Accept)
    )
    return accept_header.encode('utf8')
```
服务端返回如上信息就可以与Web客户端建立连接。
**注意：回复信息必须跟一个\r\n的换行，而且只能跟一个。该符号是告诉客户端回复信息结束的标志，跟多个会引起客户端不断发送空结果，且连接建立不成功。所以必须有，且只能有一个。**
**这个注意事项耗费我2个小时找无法建立链接的原因。特此提醒各位**

### 3.3 通信 
**客户端到服务器的信息解析**
![摘自参考博客](https://images2018.cnblogs.com/blog/1078987/201803/1078987-20180315190609151-1724857868.png)
按照如上方式进行解析即可：
例如：

```python
客户端发送："Hello World"
服务端接收：b'\x81\x8b\x04\x89\xe4)L\xec\x88Ek\xa9\x93Fv\xe5\x80'

如上接收信息做二进制处理，按照WebSocket协议头解析如下
第一段：b'\x81' = 0b1000 0001
Fin = 1，则说明当前数据包是最后一个，没有后续数据包，如果为0则还有后续数据包。"此处是关键的数据包连接判断"
opcode = 1，说明当前数据的格式为文本格式
'Webdocket数据帧中OPCODE定义：'
#0x0表示附加数据帧
#0x1表示文本数据帧
#0x2表示二进制数据帧
#0x3-7暂时无定义，为以后的非控制帧保留
#0x8表示连接关闭
#0x9表示ping
#0xA表示pong
#0xB-F暂时无定义，为以后的控制帧保留
此处尤其注意关闭的操作码为0x8,直接做结束处理即可。

第二段：b'\8b' = 0b1000 1011
mask = 1，说明该条信息包含掩码，掩码在后续4个字节中
payloadLen = 11，说明该条信息包含的数据长度为11个
此处关于长度有一个说明：
payload DataLen:
1. len<= 125(0b1111 1101)：关于长度的字节描述就结束了，长度为低7位。
2. len = 126(0b1111 1110)：后续两个字节为真实长度
3. len = 127(0b1111 1111)：后续八个字节为真实长度

第三段：b'\x04\x89' 掩码部分
用于对数据进行掩码操作

第四段：b'\xe4)L\xec\x88Ek\xa9\x93Fv\xe5\x80' 数据部分
直接用掩码转换即可
#摘自dwebsocket库
def mask_or_unmask(mask, data):
    """Websocket masking function.
    `mask` is a `bytes` object of length 4; `data` is a `bytes` object of any length.
    Returns a `bytes` object of the same length as `data` with the mask applied
    as specified in section 5.3 of RFC 6455.
    This pure-python implementation may be replaced by an optimized version when available.
    """
    mask = array.array("B", mask)
    unmasked = array.array("B", data)
    print('error: ', mask, unmasked)
    for i in range(len(data)):
        unmasked[i] = unmasked[i] ^ mask[i % 4]
    return unmasked.tobytes()
```
如上我们就简要分析了WebSocket客户端给服务端发送信息的结果解析，简而言之：
**Fin(1bit) +Unuse(3bit) + opcode(4bit)**
**+ mask(1bit) + dalen(7bit) +[dalen(16bit or 64bit)] + [mask(32bit)]**
**+ data(datalen bit)**
此处需要注意的就是datalen，数据长度的值根据大小占用不同的数位。另外就是掩码部分，如掩码(mask)位=0，则后续直接就是明文，否则就需要用掩码做转化处理。
**服务器到客户端的信息封装(封装表和客户端到服务端的一致)**
此处需要说明的是封装注意点：
1. Fin码根据包数量做判断
2. opcode根据需要做选择
3. datalen根据不同情况做长度和位置的选择
4. mask一般服务器到客户端无需添加mask，故直接传明文也没有任何问题。

因此则有回复信息组成如下：
1. **Fin(1bit) + Unuse(3bit) + opcode(4bit)**
2. **+ Mask(1bit=0) + dalen(7bit) +[dalen(16bit or 64bit)]** 
3. **+ data(dalen bit)**

## 四、注意点 ##
### 4.1 关闭操作
会返回 opcode=0x8 的信息。该信息包含主动或被动关闭，关闭网页也会返回关闭信息，主动关闭连接也会返回关闭信息
### 4.2 websocket版本
本文说明的是Sec-websocket-Version: 13 版本的通信协议
### 4.3 关于代码
关于websocket协议所有的代码均可以在dwebsocket库中找到，尤其是protocols.py文件中，所以详细代码我这边就不提供了，理解了协议内容，即使用C#或者C++或者java等其他开发语言开发也不在话下。

---

## 五、WebSocket拓展

WebSocket类似HTTP协议，是为了弥补HTTP协议的缺陷：通信只能有客户端发起，HTTP协议做不到服务器主动向客户端推送信息。

WebSocket协议诞生于2008年，2011年成为国际标准。当前基本所有浏览器都支持了，但存在版本的差异

WebSocket最大特点就是，服务器可以主动向客户端推送消息，客户端也可以主动向服务器推送消息，实现真正的平等对话，始于服务器推送技术的一种。

![WebSocket和HTTP的协议握手交互](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\1287779-20180404165107083-997801929.png)

其他特点包括：
（1）建立在 TCP 协议之上，服务器端的实现比较容易。
（2）与 HTTP 协议有着良好的兼容性。默认端口也是80和443，并且握手阶段采用 HTTP 协议，因此握手时不容易屏蔽，能通过各种 HTTP 代理服务器。
（3）数据格式比较轻量，性能开销小，通信高效。
（4）可以发送文本，也可以发送二进制数据。
（5）没有同源限制，客户端可以与任意服务器通信。
（6）协议标识符是ws（如果加密，则为wss），服务器网址就是 URL。

![HTTP类型和WebSocket类型](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\1287779-20180404165618881-1720601312.png)

**对于低端不支持WebSocket的浏览器，一般有几个解决方案：**

1. 使用轮询或长连接的方式实现伪WebSocket的通信
2. 使用flash或其他方法实现一个[websocket客户端](https://segmentfault.com/q/1010000005000671/a-1020000005003936).

3. 创建一个Web socket，[链接使用java开发](https://blog.csdn.net/u011925826/article/details/17532465)

#### 5.1 WebSocket学习笔记——关于不同环境的兼容性问题

https://www.cnblogs.com/bluedoctor/p/3534087.html

后续分析和解决

