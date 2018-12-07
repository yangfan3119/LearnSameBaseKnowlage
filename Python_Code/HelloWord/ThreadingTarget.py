from threading import Thread
from time import sleep

class MyTd:
    isStop = False
    isRuning = False
    MyCount = 0

    def __init__(self):
        print("Init")
        self.thrd = None

    def Run(self):
        while self.isStop:
            print('MyCount=',self.MyCount)
            self.MyCount+=1
            self.MySleep(3)
        self.isRuning = False

    def MySleep(self,tsleep):
        sleep(tsleep)

    def Stop(self):
        print('Td Stop')
        self.isStop = False

    def Start(self):
        print('Td Start')
        self.isStop = True
        if not self.isRuning:
            self.thrd = Thread(target=self.Run);
            self.thrd.start()
            self.isRuning = True
            return self.thrd.ident
        print('It Has Begining.')

    def ShowThdSta(self):
        print(self.thrd.isAlive())

if __name__=="__main__":
    print("ASDFASDF")
    mytd = MyTd()
    while True:
        od = input('Input Order：')
        if od=='exit':
            break
        elif od=='start':
            print(mytd.Start())
        elif od=='stop':
            mytd.Stop()
        elif od=='0':
            mytd.ShowThdSta()
        elif od=='1':
            print('ActiveThreadCount:',threading.activeCount())
