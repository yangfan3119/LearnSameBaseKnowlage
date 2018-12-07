from RaspSocket.MyThreadObj import MyThread
import socket


class SkBase:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'queue_das'):
            setattr(self, 'queue_das', '')

        if not hasattr(self, 'OutFuncs'):
            setattr(self, 'OutFuncs', None)

        if not hasattr(self, 'SinglSk'):
            setattr(self, 'SinglSk', None)

        if not hasattr(self, 'SkConnFlag'):
            setattr(self, 'SkConnFlag', False)

        if not hasattr(self, 'DevAddr'):
            setattr(self, 'DevAddr', None)

        if not hasattr(self, 'SkThrd'):
            setattr(self, 'SkThrd', None)
            self.SkThrd = MyThread()
            self.SkThrd.SetRun(self.skRun)
        print('SkBase Init',hasattr(self,'SkThrd'))

    def GetRaspOrder(self, od):
        res = '#RX#' + od + '#RW#'
        return res

    def SkSend(self, order):
        if self.DevAddr == None:
            return False
        if not self.SkConnFlag:
            return False
        self.SinglSk.send(order.encode())

    def skRun(self):
        if self.DevAddr == None or self.OutFuncs == None or self.SkConnFlag == True:
            return
        try:
            self.SinglSk = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            self.SinglSk.connect(self.DevAddr)
            self.SkConnFlag = True
            self.SkSend(self.GetRaspOrder('XinweiClientRight,10'))
            self.SkSend(self.GetRaspOrder('RequestDataValue,4'))
            self.SkSend(self.GetRaspOrder('SetSocketCount,0'))
            while self.SkThrd.isStop:
                d = self.SinglSk.recv(1024).decode()
                rx = self.RaspAdd(d)
                for msg in rx:
                    if not self.SkConnFlag:
                        break
                    self.OutFuncs(msg)
        except Exception as e:
            print('断开连接',str(e))
            self.OutFuncs('断开连接')
            self.SkConnFlag = False
        self.SinglSk.close()
        self.SkThrd.Stop()

    def RaspAdd(self, da):
        self.queue_das += da
        res = []
        while True:
            ib = self.queue_das.find('#RX#')
            ie = self.queue_das.find('#RW#')
            if ib != -1 and ib < ie:
                res.append(self.queue_das[ib + 4:ie])
                self.queue_das = self.queue_das[ie + 4:]
            else:
                break
        return res

    def SetOutFunc(self, fun):
        self.OutFuncs = fun

    def Connect(self, addr):
        self.DevAddr = addr
        self.SkThrd.Start()

    def GetConnectStatus(self):
        return self.SkConnFlag

    def DisConnect(self):
        self.SinglSk.close()
        self.SkThrd.Stop()


def RaspShow(da):
    if da.find('$') >= 0:
        dalist = da.split('$')
        print(dalist[1], 'mΩ')
    else:
        print(da)


if __name__ == "__main__":
    sk = SkBase()
    sk.SetOutFunc(RaspShow)
    while True:
        tx = input('Input:')
        if tx == '0':
            break;
        elif tx == '1':
            sk.Connect(('192.168.7.53', 9910))
        elif tx == '2':
            sk.DisConnect()
        elif tx == '3':
            sk.SkSend(sk.GetRaspOrder('SetSocketCount,5'))
