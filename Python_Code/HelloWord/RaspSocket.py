import socket


class RaspOrder:
    __Order = {}
    def __init__(self):
        self.AddBaseOrder()

    def AddBaseOrder(self):
        self.__Order['RequestDataValue']='#RX#RequestDataValue,4#RW#'
        self.__Order['SetSocketCount'] = '#RX#SetSocketCount,-1#RW#'

    def GetOrder(self,key):
        return self.__Order.get(key,'error').encode()

class SkData:

    def __init__(self):
        self.__das = ''

    def Add(self,da):
        self.__das += da
        res = []
        while True:
            ib = self.__das.find('#RX#')
            ie = self.__das.find('#RW#')
            if ib!=-1 and ib<ie:
                res.append(self.__das[ib+4:ie])
                self.__das = self.__das[ie+4:]
            else:
                break
        return res

class SkBase:
    __instance = None
    __das = ''
    __sk = None
    __OutFunc = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance==None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self,func):
        self.__das = ''
        self.__OutFunc = func
        self.__sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def GetOrder(self,od):
        res = '#RX#'+od+'#RW#'
        return res.encode()

    def Add(self,da):
        self.__das += da
        res = []
        while True:
            ib = self.__das.find('#RX#')
            ie = self.__das.find('#RW#')
            if ib!=-1 and ib<ie:
                res.append(self.__das[ib+4:ie])
                self.__das = self.__das[ie+4:]
            else:
                break
        return res

    def Connect(self,addr):
        try:
            self.__sk.connect(addr)
            self.__sk.send(self.GetOrder('RequestDataValue,4'))
            self.__sk.send(self.GetOrder('SetSocketCount,-1'))
            while True:
                d = self.__sk.recv(1024).decode()
                rx = self.Add(d)
                for msg in rx:
                    self.__OutFunc(msg)
        except:
            print('连接错误')
            self.__OutFunc('连接错误')
        self.__sk.close()

def PrintIt(data):
    if data.find('$') >= 0:
        dalist = data.split('$')
        print(dalist[1],'mΩ')
    else:
        print(data)

if __name__=='__main__':
    # od = RaspOrder()
    # skda = SkData()
    # sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # # try:
    # sk.connect(('192.168.7.53', 9910))
    # print('connect succ!0',od.GetOrder('RequestDataValue'))
    #
    # sk.send(od.GetOrder('RequestDataValue'))
    # sk.send(od.GetOrder('SetSocketCount'))
    # print('connect succ!1')
    #
    # while True:
    #     d = sk.recv(1024).decode()
    #     rx = skda.Add(d)
    #     for msg in rx:
    #         PrintIt(msg)
    # except:
    #     print('Socket Error!')
    addr = ('127.0.0.1', 7878)
    Mysocket = SkBase(PrintIt)
    Mysocket.Connect(addr)