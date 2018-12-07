'''
print('Hello World!')
print(\'''多
行
输
出
是
否
靠
谱\''')
L = [
    ['Apple', 'Google', 'Microsoft'],
    ['Java', 'Python', 'Ruby', 'PHP'],
    ['Adam', 'Bart', 'Lisa']
]
print(L[0][0])
print(L[1][1])
print(L[2][2])

s = input('birth:')
birth = int(s)
if birth>2000:
	print('00后')
else:
	print('90后')

height = 1.70
weight = (float)(input('weight:'))

BMI = weight / (height*height)
print('BMI = ',BMI)
if(BMI<18.5):
	print('过轻')
elif BMI<25:
	print('正常')
elif BMI<28:
	print('过重')
elif BMI<32:
	print('肥胖')
else:
	print('严重肥胖')

n1 = 255
n2 = 10000
print(hex(n1))
print(format(n2,'t'))

'''
import math

def quadratic(a,b,c):
	delt = b*b-4*a*c
	if(delt>=0):
		root1 = (-b+math.sqrt(delt))/(2*a)
		root2 = (-b-math.sqrt(delt))/(2*a)
		return root1,root2
	
def power(x,n=2):
	s = 1;
	while n>0:
		n -= 1
		s = s*x
	return s
	
def calc(*numbers):
	sum = 0
	for n in numbers:
		sum = sum + n*n
	return sum

def person(name,age,**kw):
	if 'city' in kw:
		pass#有city参数
	print('name:',name,'age:',age,'others:',kw)
'''
print('quadratic(2,3,1) = ',quadratic(2,3,1))
print('quadratic(1,3,-4) = ',quadratic(1,3,-4))

print(power(5))
print(power(5,2))

L = [1,2,3]
print(calc(1,2,3))
print(calc(1,2,3,4,5))
print(calc(*L))

person('jack',23,citys='guangdong',addr='shenzhen',zipcode=123456)
kw = {'Param1':1,'Param2':2}
person('jackson',5,**kw)
'''
def hanno(n,a,b,c):
	if n==1:
		print('move:',a,'-->',c)
	else:
		hanno(n-1,a,c,b)
		hanno(1,a,b,c)
		hanno(n-1,b,a,c)
'''
hanno(3,'A','B','C')
'''
def trim(s):
	#print('[%s]'%s)
	if len(s)>=1:
		if s[0]==' ':
			s = trim(s[1:])
		elif s[-1]==' ':
			s = trim(s[:-1])
	return s
'''
if trim('hello  ') != 'hello':
    print('测试失败!')
elif trim('  hello') != 'hello':
    print('测试失败!')
elif trim('  hello  ') != 'hello':
    print('测试失败!')
elif trim('  hello  world  ') != 'hello  world':
    print('测试失败!')
elif trim('') != '':
    print('测试失败!')
elif trim('    ') != '':
    print('测试失败!')
else:
    print('测试成功!')
'''
from collections import Iterable, Iterator
def g():
	yield 1
	yield 2
	yield 3
	yield 4
'''
print('Iterable? g():', isinstance(g(), Iterable))
print('Iterator? g():', isinstance(g(), Iterator))

print('next():')
it = iter([1, 2, 3, 4, 5])
print(next(it))
print(next(it))
print(next(it))
print(next(it))
print(next(it))

L = ['Hello', 'World', 18, 'Apple', None]
print([s.lower() for s in L if isinstance(s,str)])
'''

def yanghui():
	L = [1]
	n = 0
	while n<=10000:
		yield L
		L = [1,*[L[i]+L[i+1] for i in range(0,len(L)-1) if len(L)>=2],1]
		n += 1
	return 'done'
	
def triangles(max):
	for i,n in enumerate(yanghui()):
		print(n)
		if i==max-1:
			break
'''
triangles(15)
'''
def normalize(name):
	if (len(name)>1)and(name[0]>'Z'):
		#chr(ord(name[0])-(ord('a')-ord('A')))
		name = name[0].upper()+name[1:]
		#print(x)
	return name
'''
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)
'''
from functools import reduce

def prod(L):
	return reduce(lambda x,y:x*y,L)
'''
print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
if prod([3, 5, 7, 9]) == 945:
    print('测试成功!')
else:
    print('测试失败!')

x = "123456.2.1"
print(x.find('.'))
'''





