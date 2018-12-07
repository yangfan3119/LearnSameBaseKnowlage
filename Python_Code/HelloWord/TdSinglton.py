from ThreadingTarget import MyTd


class TdSinglton(MyTd):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance==None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        print('TdSinglton Init')

    def Run(self):
        while self.isStop:
            print('TdSinglton Run',self.MyCount)
            self.MyCount+=1
            self.MySleep(3)
        self.isRuning = False

if __name__=="__main__":
    print('Begin ABS')
    A = TdSinglton()
    B = TdSinglton()
    while True:
        tx=input('Input:')
        if tx=='a0':
            A.Stop()
        elif tx=='a1':
            A.Start()
        elif tx=='a2':
            A.ShowThdSta()
        elif tx=='b0':
            B.Stop()
        elif tx=='b1':
            B.Start()
        elif tx=='b2':
            B.ShowThdSta()