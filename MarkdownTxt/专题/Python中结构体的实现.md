## Python中结构体的实现

```python
# encoding=utf-8
# 第一种方式： class实现


class stu1:
    def __init__(self):
        pass

    def setx(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

    def getx(self):
        print("id={id},name={name},age={age}"
              .format(id=self.id, name=self.name, age=self.age))


if __name__=="__main__":
    das = [stu1() for _ in range(4)]
    das[0].setx(1, 'A', 10)
    das[1].setx(2, 'B', 30)

    das[0].getx()
    das[1].getx()
    # setx(das[0], 1, 'A', 10)
    # setx(das[1], 2, 'B', 30)
    #
    # getx(das[0])
    # getx(das[1])
```

```python
# 第二种 通过numpy创建结构体，实则类似Tab的表
import numpy as np

stu2 = np.dtype({'names':['id','name','age'], 'formats':['I','S32','I']})

das = np.array([(0,'defx',8)]*10, dtype=stu2)

print(das)
das[1]['id'] = 1
print(das[1])
```

