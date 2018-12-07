class Day65(object):
    
    def __init__(self):
        self.N = 100000000
        self.Lx, self.L_x = self.xPow2()
        
    def xPow2(self):
        L = []
        L_ = []
        for i in range(self.N):
            t = i*i;
            if t > self.N:
                break
            else:
                L.append(t)
                L_.append(i)
        return L,L_
    
    def GetARes(self,a):
        if (a-13<=0) or (a+13>self.N):
            return 0,0
        else:
            return a-13,a+13
    
    def GetBRes(self,a1,a2):
        Lb = []
        Lb_x = []
        for pow2x in self.Lx:
            if(pow2x%a2==0):
                b = pow2x//a2
                x1 = a1*b
                if(x1 in self.Lx):
                    Lb.append(b)
                    xi = self.L_x[self.Lx.index(x1)]
                    xi_ = self.L_x[self.Lx.index(pow2x)]
                    Lb_x.append([xi,xi_])
                    break
        return Lb, Lb_x
    
    def GetBRes_new1(self):
        ax = []
        for i in range(len(self.Lx)):
            for j in range(i+1,len(self.Lx)):
                t = self.Lx[j]-self.Lx[i]
                if(t%26==0):
                    b = t/26
                    if(self.Lx[j]%b==0) and (self.Lx[i]%b==0):
                        a = (self.Lx[j]+ self.Lx[i])/(2*b)
                        if a not in ax:
                            print('b = ',t/26,'Lx1 = ',self.Lx[j],self.Lx[i],'  a = ',a)
                            ax.append(a)
                    
		
dx = Day65()
for a in range(dx.N):
    a1, a2 = dx.GetARes(a)
    if(a1==0)or(a2==0):
        continue
    else:
        Lb,Lb_ = dx.GetBRes(a1,a2)
        if len(Lb) > 0:
            print('可能值有：a = %d'%a,'(%d-13=%d)*%d = (%d)^2   '%(a,a1,Lb[0],Lb_[0][0]), '(%d+13=%d)*%d = (%d)^2'%(a,a2,Lb[0],Lb_[0][1])) 