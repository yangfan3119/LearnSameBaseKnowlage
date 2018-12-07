

class Singlton:
    __instance = None
    __info = ''

    def __new__(cls, *args, **kwargs):
        if cls.__instance==None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        print('Init')

    def OutInfo(self):
        return self.__info

    def InInfo(self,info):
        self.__info = info

A = Singlton()
A.InInfo('ABS')
print(A.OutInfo())

B = Singlton()
B.InInfo('123')
print(A.OutInfo(),B.OutInfo())