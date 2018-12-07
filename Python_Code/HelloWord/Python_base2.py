

def _odd_iter():
	n = 1
	while True:
		n = n+2
		yield n
		
def _not_divisble(n):
	return lambda x:x % n > 0

def premit():
	yield 2
	it = _odd_iter()
	while True:
		n = next(it)
		yield n
		it = filter(_not_divisble(n), it)
'''
m = 0
for n in premit():
	if(n<=2018/2):
		m += 1
		print(n)
	else:
		break
print("All num counts=",m)
'''
def is_palindrome(n):
	s = str(n)
	ns = len(s)
	for i in range(0,ns):
		if(s[i]!=s[ns-i-1]):
			return False
	return True
'''
output = filter(is_palindrome, range(1, 1000))
print('1~1000:', list(output))

sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
['Zoo', 'Credit', 'bob', 'about']
'''

L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

def by_name(t):
	return t[1]
'''
L2 = sorted(L,key=by_name, reverse=True)
print(L2)
'''

def CreateCounter():
	n = 0
	def Counter():
		n = n + 1
		def Adds():
			return n
		return Adds
	return Counter()

'''
counterA = CreateCounter()
print(counterA(), counterA(), counterA(), counterA(), counterA()) # 1 2 3 4 5
counterB = CreateCounter()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')

n = 3
L = list(filter(lambda x:x%n>0, range(1,20)))
print(L)
'''

import time,functools

def ShowTime():
	return (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	
def log(func):
	@functools.wraps(func)
	def wrapper(*args, **kw):
		print("B %s  %s"%(func.__name__,ShowTime()))
		res = func(*args, **kw)
		print("E %s  %s"%(func.__name__,ShowTime()))
		return res
	return wrapper

@log
def fast(x, y):
    time.sleep(2)
    return x + y;
		
@log
def slow(x, y, z):
    time.sleep(4)
    return x * y * z;

'''
s = slow(11,22,33)
f = fast(11,22)
'''
#print(f,s,ShowTime())
#print(fast.__name__,slow.__name__)
def Beishu(n):
	L = []
	for i in range(1,2018):
		if i*n <= 2018:
			L.append(i*n)
		else:
			break
	return L
			
def DeleSome(L):
	Lx = L
	for i in range(0,len(L)-1):
		for y in L[i:]:
			if(L[i]!=y) and (y%L[i]==0):
				Lx[i] = 0
				break
	Ly = []
	for x in Lx:
		if x!=0:
			Ly.append(x)
	return Ly
'''
i = 5
while(i > 0):
	i -= 1
	x = int(input("最小公约数："))
	L = Beishu(2)
	print('相同公约数的最多值',len(L),'\n',L[:5],'...',L[-5:])
	Lx = DeleSome(L)
	print('去掉可以整除的倍数',len(Lx),'\n',Lx[:5],'...',Lx[-5:])
	print('=================\n')
'''

class Student(object):
	def __init__(self,name,score):
		self.name = name
		self.score = score
	
	def print_score(self):
		print("%s: %d"%(self.name,self.score))

'''	
a = Student("Job",76)
a.age = 8
a.print_score()
print(a.age)
print(a)
'''