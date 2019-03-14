# Windows10 下的docker安装与入门

## 一、使用docker toolbox安装docker

对于Windows用户来说，使用docker toolbox来安装docker是最简单的方式

docker toolbox是一个工具集，它主要包含以下一些内容：

- Docker CLI 客户端，用来运行docker引擎创建镜像和容器
- Docker Machine. 可以让你在windows的命令行中运行docker引擎命令
- Docker Compose. 用来运行docker-compose命令
- Kitematic. 这是Docker的GUI版本
- Docker QuickStart shell. 这是一个已经配置好Docker的命令行环境
- Oracle VM Virtualbox. 虚拟机

由于Docker引擎的守护进程使用的是Linux的内核，所以我们不能够直接在windows中运行docker引擎。而是需要运行Docker Machine命令 docker-machine， 在你的机器上创建和获得一个Linux虚拟机，用这个虚拟机才可以在你的windows系统上运行Docker引擎

### 第一步：检查你当前的windows系统是否符合要求：

1. 运行Docker设备**必须是win7及以上版本的64bit系统**
2. 设备必须支持硬件加速
3. 设备必须支持虚拟化

### 第二步： 安装docker toolbox

[docker toolbox安装](https://www.docker.com/products/docker-desktop)，该工具会安装一下几个软件，如部分已安装则无需安装，否则下一步即可

- Windows版的Docker客户端
- Docker Toolbox管理工具和ISO镜像
- Oracle VM Virtualbox
- Git MSYS-git Unix 工具

安装完成后会在桌面上看到三个图标：

*Oracle VM VirtualBox*、*Docker Quickstart Terminal*、*Kitematic(Alpha)*

### 第三步：安装docker

**双击运行Docker Quickstart Terminal**,启动后会形成一个鲸鱼的图形并自动分配一个*docker-machine ip: 192.168.99.100*

**docker 测试：**

```
docker run hello-world
```

1. 第一次运行会下载这个镜像
2. 然后运行会出现一句Hello from Docker.

## 二、docker初次使用

创建一个鲸鱼说话的小镜像程序

### 2.1 下载并运行镜像

```
docker run docker/whalesay cowsay boo-boo
 _________
< boo-boo >
 ---------
    \
     \
      \
                    ##        .
              ## ## ##       ==
           ## ## ## ##      ===
       /""""""""""""""""___/ ===
  ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
       \______ o          __/
        \    \        __/
          \____\______/

```

初次使用如本地无该镜像则自动下载

### 2.2 编写Dockerfile文件，生成自定义镜像

创建文件名: *Dockerfile* 的二进制文件，然后用记事本打开写入如下内容

```
FROM docker/whalesay:latest

RUN apt-get -y update && apt-get install -y fortunes

CMD /usr/games/fortune -a | cowsay
```

*cd*到文件目录运行如下命令

>docker build -t docker-whale . 

docker-whale为新创建的镜像名称

最后的   **.**   指代当前目录下的Dockerfile文件

### 2.3 查看及验证

```
# 查看docker的镜像：
neware@neware-PC MINGW64 /e/GitHubCode/web_develop (master)
$ docker images
REPOSITORY                TAG        IMAGE ID            CREATED             SIZE
my_webtest                latest     365156662306        30 minutes ago      299MB
docker-whale              latest     2186a433c3c8        41 minutes ago      254MB
ubuntu                    16.04      7e87e2b3bf7a        5 weeks ago         117MB
hello-world               latest     fce289e99eb9        8 weeks ago         1.84kB
dongweiming/web_develop   latest     5c99b9e833b7        2 years ago         6.18GB
docker/whalesay           latest     6b362a9f73eb        3 years ago         247MB
```

```
# 运行docker-whale镜像
neware@neware-PC MINGW64 /e/GitHubCode/web_develop (master)
$ docker run docker-whale
 __________________________________
/ A CONS is an object which cares. \
|                                  |
\ -- Bernie Greenberg.             /
 ----------------------------------
    \
     \
      \
                    ##        .
              ## ## ##       ==
           ## ## ## ##      ===
       /""""""""""""""""___/ ===
  ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
       \______ o          __/
        \    \        __/
          \____\______/

```





## 三、Docker基本原理及快速入门

http://www.cnblogs.com/SzeCheng/p/6822905.html

























