from threading import Thread
from time import sleep


class MyThread:
    isStop = False
    isRunning = False

    def __init__(self):
        self.thrd = None
        self.Run = None

    def SetRun(self,run):
        self.Run = run

    def MySleep(self,tm):
        sleep(tm)

    def Stop(self):
        self.isStop = False
        self.isRunning = False

    def Start(self):
        if self.Run is None:
            return -1
        else:
            self.isStop = True
            if not self.isRunning:
                self.thrd = Thread(target=self.Run)
                self.thrd.start()
                self.isRunning = True
                print('MyTh connect Succ!')
                return self.thrd.ident
            else:
                print('MyTh connect has been connected')

    def ShowThdStatue(self):
        return self.thrd.isAlive()