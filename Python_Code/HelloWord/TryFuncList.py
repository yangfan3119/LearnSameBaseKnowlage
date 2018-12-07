
def fa(x):
    print('fa ',x)

def fb(x):
    print('fb ',x)

def fc(x):
    print('fc ',x)

def FuncList(flist,x):
    print('FuncList Run:')
    for f in flist:
        f(x)

if __name__=="__main__":
    funcl = []
    funcl.append(fa)
    funcl.append(fb)
    FuncList(funcl,10)

    funcl.append(fc)
    FuncList(funcl,20)

    funcl.remove(fa)
    FuncList(funcl,30)