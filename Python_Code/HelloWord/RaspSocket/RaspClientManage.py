from RaspSocket.MyTcpSockBase import SkBase


class RaspOp:
    def __init__(self):
        self.FuncList = []
        self.RaspSocket = SkBase()
        self.RaspSocket.SetOutFunc(self.RaspFuncRun)
        self.RaspSocket.Connect(('192.168.7.53', 9910))

    def ReConnect(self):
        if not self.RaspSocket.SkConnFlag:
            self.RaspSocket.Connect(('192.168.7.53', 9910))

    def RaspSingIn(self, func):
        if func not in self.FuncList:
            self.FuncList.append(func)

    def RaspFuncRun(self, res):
        print('Res Finds:',res.find('$'))
        if res.find('$') != -1:
            resop = res.split('$')
            for f in self.FuncList:
                f(resop[1], resop[2], resop[3], resop[4])
        else:
            print('One Res: ', res)
            pass

    def SendCount(self, n):
        if isinstance(n, int) and n >= -1:
            self.RaspSocket.SkSend(self.RaspSocket.GetRaspOrder('SetSocketCount,%d' % (n,)))

    def GetConnFlag(self):
        return self.RaspSocket.SkConnFlag

    def GetLotCount(self):
        self.RaspSocket.SkSend(self.RaspSocket.GetRaspOrder('SetSocketCount,%d' % (-1,)))

    def StopGetCount(self):
        self.RaspSocket.SkSend(self.RaspSocket.GetRaspOrder('SetSocketCount,%d' % (0,)))

    def SendRaspUp(self,style):
        self.RaspSocket.SkSend(self.RaspSocket.GetRaspOrder('RequestSetUpDate,%d,U-Disk UpDate' % (style,)))


def ShowRaspResult(rd, rg, vd, vg):
    print('R=%s RG=%s,V=%s VG=%s' % (rd, rg, vd, vg))


if __name__ == "__main__":
    Dev = RaspOp()
    Dev.RaspSingIn(ShowRaspResult)
    while True:
        tx = input('Input:')
        if tx == '-1':
            break;
        elif tx == '0':
            Dev.ReConnect();
        elif tx == '1':
            Dev.SendCount(5)
        elif tx == '2':
            print(Dev.GetConnFlag())
        elif tx == '3':
            Dev.GetLotCount()
        elif tx == '4':
            Dev.StopGetCount()
        elif tx == '5':
            Dev.SendRaspUp(1)
        elif tx == '6':
            Dev.SendRaspUp(4)