[ACM算法日常链接](https://mp.weixin.qq.com/s?__biz=MzUzMjU2NjYxMA==&mid=100000086&idx=1&sn=a4c9a7b7897c1d2065338ea6fdb4806d&chksm=7ab0066b4dc78f7dc1f6c681be25e9a116dddd56cbe4ae80d78147b13b7df1c19714dca64a94&scene=18&xtrack=1#rd)

# ACM算法日常

## 一、上卷-基本

### 1.1 枚举

#### 1.1.1 求素数

HDU 3823——枚举法

**题意：**即求一个数，能使a，b与之相加后，成为素数，并且a与b之间没有其他的素数。

**做法：**该题的关键是将20000000之前的素数打表，然后求其每个之间的差值，相等的存放到同一个数组中。

```c
// 该题目的核心是求素数列
/*	素数的计算
双重循环：2,3,4,5...s
		2,3,4,5...M/i
	上下依次相乘，计算出所有结合
*/
for (int i = 2; i <= s; i++) {
    if (is_prime[i]) {
        /*求出最大值*/
        for (int j = 2; j <= MAX_VALUE / i; j++) {
            is_prime[i * j] = 0;
        }
    }
}
```

### 1.2 贪心

#### 1.2.1 取最大结果

[HDU 1009](http://acm.hdu.edu.cn/showproblem.php?pid=1009)

**题意：**FatMouse有M个catFood，喜欢吃javaBean。一个warehouse有很多个房间，每个房间均有`J[i]的catFood`和`F[i]的javaBean`，他们的兑换(trade)方案为，`price = J[i]/F[i]`。求FatMouse最多能换多少javaBean。

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct trade_s {
    //注意这里只能是整数
    int javaBean, catFood;
    double normalize;//兑换标准，即单价
} trade_t;

static trade_t w[1100];

//用qsort函数必须注意这个函数返回的是int类型，所以这里会返回1和-1
int cmp(const void * x, const void * y) {
    //注意这里直接用减法并且返回1和-1
    return ((trade_t*)x)->normalize - ((trade_t*)y)->normalize > 0 ? -1 : 1;
}

int main() {
    // 获取w[n]的交易基本数据，其中单价
    ...
        //排序——依据单价排序。注意此处的qsort用法
        qsort(w, n, sizeof(trade_t), cmp);
    for (i = 0; i < n; i++) {
        if (m >= w[i].catFood) {
            //如果支付得起，则买完这个房间，然后更新sum以及M(-花费)数据。
        } else {
            //支付不起，以单价购买量乘以重量
            break;
        }
    }
    // sum为贪心法的结果
    ...
}
```

**想法：**贪心法的使用就是为获取最优结果，而每一次都从最优步骤开始执行。该算法的核心为排序，即问题解在某一个维度下的最优排序，使得最终结果达到最佳。所以此法**排序是核心**。

#### 1.2.2 超市限期促销商品

**题目大意是：** 超市有堆商品要卖，但是它们有不同的利润和期限，得在此期限前卖出去，**不一定要全部卖出**，但是**要求利润可以最大化**。这些商品是从**同一天开始**一起贩卖的，每天**只能卖一种**商品。 

例：这堆商品分为a,b,c,d四种 

**(pa,da)=(50,2) ,  (pb,db)=(10,1) ,  (pc,dc)=(20,2) ,  (pd,dd)=(30,1)** 

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\640.webp)

总共卖的天数=商品中期限最长的时间，所以为2天

0-1第1天d=30(要把a留到第二天卖，所以只有三种可以选，同选利润最大的)

0-2第2天a=50(只有a和c可以卖，选择利润最大的)

```tex
这是典型的贪心算法问题（活动安排）+优先队列。
 输入不定测试组，以文件结尾结束，每组先输入一个n，然后是输入n组 pi di，表示第i个商品的利润和deadline 
    1. 按照 dx  和  px 从大到小排序
    2. 建立优先队列 big
    3. 从截止日期开始一天一天往前找截止日期内的，且还没有被卖过的，利润最大的商品
    4. 在 big 中 push() 进 day 到 最大截止日期的所有商品的利润值
    5. 注意不要重复压入哦
```

```c++
#include <iostream>
#include <queue>
#include <algorithm>
#define maxn 100001
using namespace std;
int out[maxn], longth = 0;
class X
{
public:
    int px;		// 利润最高次之
    int dx;		// 截止日期优先
};
bool sort_dx_px(const X &x1, const X &x2)
{
    if (x1.dx > x2.dx)  return true;
    else if (x1.dx == x2.dx)
    {
        if (x1.px > x2.px)
            return true;
        else
            return false;
    }
    else
        return false;
}
int main()
{
    int n = 0;
    while (scanf("%d", &n) != EOF)
    {
        X *x = new X[n];                //动态构建，节约空间
        int maxx = 0;                   //当前数据组的最大利润
        if (n == 0)
        {
            out[longth++] = 0;
            continue;
        }
        for (int i = 0; i < n; i++)
            cin >> x[i].px >> x[i].dx;
        sort(x, x + n, sort_dx_px);     // 按照 dx 和 px 从小到大排列
        priority_queue<int> big;        //优先队列
        //从截止日期 一天一天 往前找 期限内的利润最大的商品
        for (int day = x[0].dx; day > 0; day--)
        {
            for (int i = 0;i < n && day <= x[i].dx; i++)
            {
                if (x[i].dx >= day)	// 当截止日期大于等于当前天数时，则直接选择
                {
                    maxx += x[i].px;
                    x[i].dx = -1;	//让其等于最大天数
                    break;
                }
            }
        }
        out[longth++] = maxx;
        delete[] x;     //消除内存空间
    }
    for (int i = 0; i < longth; i++)
    {
        cout << out[i] << endl;
    }
    return 0;
}
```

### 1.3 递归

#### 1.3.1 字符串扩展

**HDU 1274** 递归是一种分析方法，可以帮助我们看清楚事物的本质。 如果确定了用递归法解题，思考的重点应该放到建立原问题和子问题之间的联系上面。 

Sample Input:	*1(1a2b1(ab)1c)*	*3(ab2(4ab))*

Sample Output:	*abbabc*		*abaaaabaaaababaaaabaaaababaaaabaaaab*

```python
t0 = '3a15bcd'
t1 = '1(1a2b1(ab)1c)'
t2 = '3(ab2(4ab))'

class acm1_3:

    def __init__(self):
        self.pri = ''

    def Run(self, s):
        self.pri = ''
        self.ans(s)
        print(self.pri)

    def ans(self, s:str):
        if s is None:
            return None
        if s[0] == ')':
            return 0

        i = 0
        while(i < len(s)):
            if s[i]==')':
                return i
            if s[i].isalpha():
                self.priAdd(s[i])
                i+=1
                continue

            D = 0
            while(s[i].isdigit()):
                D = D*10+int(s[i])
                i+=1
            D = D if D!=0 else 1
            if s[i]=='(':
                for j in range(D):
                    t = self.ans(s[i+1:])
                i += t+1
            elif s[i].isalpha():
                for j in range(D):
                    self.priAdd(s[i])
            i += 1


    def priAdd(self, s):
        self.pri += s

if __name__=="__main__":
    acm = acm1_3()
    acm.Run(t2)
```

**解题思路**：

​        数据量并不大，我们只需模拟即可，分两种策略

**step1** : 如果是数字， 代表需要循环输出， 此时又分两种策略

​        1：如果后面是“（”， 则需要循环一个字符串， 即递归即可

​        2：如果后面是单个字母， 只需把后面的一个字母循环输出多次即可

**step2**：如果是字母， 直接输出

### 1.4 回溯

消防车Firetruck(DFS+回溯）- UVA 208

```c++
#include <iostream>
#include <cstring>
#include <cstdio>
using namespace std;
const int maxn=21+4;
int map[maxn][maxn]={0};//用来存储地图
int mark[maxn];//用来记录走过的点，以便输出
bool m[maxn];//用来记忆该点有没有被访问过
int n,ans1;//ans1记录总共有多少条路径
void dfs(int x,int ans)//x表示所在的地点，ans表示这是去到的第几个地点
{
    if(x==n)
    {
        ans1++;
        cout<<'1';
        for(int i=1;i<ans;i++)
            cout<<' '<<mark[i];
        cout<<endl;return ;
    }
    for(int i=2;i<maxn;i++)//从2开始逐个搜索，因为是从1出发，不能再回到1
        if(map[x][i]==1&&!m[i])//如果i点与x点连通，而且i点没被访问过
        {
            mark[ans]=i;m[i]=true;
            dfs(i,ans+1);
            m[i]=false;
        }
    return ;
}
int main()
{
    //freopen("text.txt","r",stdin);//文件输入
    int cnt=1;
    while(cin>>n)
    {
        memset(map,0,sizeof(map));//一轮下来，有些数据要被重置
        int x=1,y=1;
        ans1=0;//重置
        while(true)
        {
            cin>>x>>y;
            if(x==0||y==0)break;
            map[x][y]=map[y][x]=1;//构建矩阵地图
        }
        cout<<"CASE "<<cnt++<<":"<<endl;
        dfs(1,1);
        cout<<"There are "<<ans1<<" routes from the firestation to streetcorner "<<n<<"."<<endl;
    }
    return 0;
}
```

```python
import numpy as np

f1 = [(1, 2), (1, 3), (3, 4), (3, 5), (4, 6), (5, 6), (2, 3), (2, 4)]
f2 = [(2, 3), (3, 4), (5, 1), (1, 6), (7, 8), (8, 9), (2, 5), (5, 7), (3, 1), (1, 8), (4, 6), (6, 9)]

InputDa = [{'n': 6, 'da': f1}, {'n': 4, 'da': f2}]


class Firetruck_DFS:

    def __init__(self):
        self.map = np.zeros(1)
        self.old = []
        self.finish = 0
        self.ans_i = 0

    def initParam(self):
        self.old = []
        self.finish = 0
        self.ans_i = 0

    def CreateMap(self, n, fx):
        self.map = np.zeros((21, 21), dtype=int)
        for a,b in fx:
            self.map[a][b] = self.map[b][a] = 1

    def Run(self, n, fx):
        self.initParam()
        self.CreateMap(n+1, fx)
        # print('n= %d, da='%(n), fx)
        self.finish = n
        self.dfs(1)

    def dfs(self, now):
        if now == self.finish:
            s = '1'
            for x in self.old:
                  s += ' %d'%(x)
            self.ans_i += 1
            print('%d : (%s)'%(self.ans_i, s))
        else:
            for i in range(2, 21):
                if self.map[now][i] == 1 and i not in self.old:
                    self.old.append(i)
                    self.dfs(i)
                    self.old.remove(i)


if __name__=="__main__":
    d = Firetruck_DFS()
    for dicx in InputDa:
        k, v = dicx['n'], dicx['da']
        print(k, v)
        d.Run(k, v)
```

### 1.5 递推

计算折线型连接下点与点的距离（即沿折线走的路线长度）吧。

![](E:\GitHubCode\LearnSameBaseKnowlage\MarkdownTxt\mdPic\640-1554974073832.webp)

对于第一步来说，比较难的地方在于如何计算距离，这里的距离分为两个部分，一部分是45度的斜线，另一部分是从点(n,0)到点(0, n+1)的长度，归纳起来可以自己画个图，参考代码注释很容易就能明白了。

```c
#include<stdio.h>
#include<math.h>

double distance(int x, int y)
{
    double dis = 0;
    double segment = sqrt(2.0);

    //45度线的总和
    for (int i = 1; i <= x + y; i++)
        dis += (i * segment);

    //减去多加的最后一部分
    dis -= (y * segment);

    //加上斜线的总和（包括第一条竖线）
    //勾股定理
    for (int i = 0; i < x + y; i++)
        dis += sqrt((double)i * i + (double)(i + 1) * (i + 1));

    return dis;
}

int main()
{
    int count, x1, x2, y1, y2;
    scanf("%d", &count);

    while (count--)
    {
        scanf("%d%d%d%d", &x1, &y1, &x2, &y2);
        //递推算法
        //先计算从(0,0)到(x,y)的距离
        //再计算差值
        double ans = fabs(distance(x1, y1) - distance(x2, y2));
        printf("%.3f\n", ans);
    }

    return 0;
}
```



```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/*读取数字，并且操作字符串*/
double digit(char ** exp_)
{
    char * exp = *exp_;
    double number = 0;
    for (*exp; *exp && *exp != ' '; ++(exp)) {
        //每前进一步，计算数字
        number = number * 10 + *exp - '0';
        ++(*exp_);
    };
    //空格，继续前进一步，注意防止越界
    if(*exp){
        ++(*exp_);
    }
    return number;
}

/*读取操作符，并且操作字符串*/
char function(char ** exp)
{
    //读取字符，前进一步
    char f = *(*exp)++;
    //空格，继续前进一步
    (*exp)++;
    return f;
}

//计算表达式的值
//使用数组作为容器
double calc(char * exp)
{
    double numbers[205];
    //将第一个数字保存在0号位置
    numbers[0] = digit(&exp);
    int i = 0;

    while (*exp) {
        //读取操作符
        char f = function(&exp);
        //读取下一个数字
        double next_value = digit(&exp);
        //如果是乘法和除法，直接将结果存在原位置
        if (f == '*')numbers[i] *= next_value;
        else if (f == '/')numbers[i] /= next_value;
        //如果是加法和减法，则将结果保存在下一位，这是优先级处理的关键点
        else if (f == '+')numbers[++i] = next_value;
        else
        {
            //除法
            numbers[++i] = -next_value;
        }
    }
    //最后只需要进行加法操作，将所有存的数据累加
    for (i; i > 0; i--)
        numbers[0] += numbers[i];
    //返回累加结果
    return numbers[0];
}

int main(int argc, char const *argv[])
{
    char exp[300];
    memset(exp, 0, sizeof(exp));
    //输入表达式
    while (gets(exp) && strcmp(exp, "0"))
    {
        //计算结果
        double value = calc(exp);
        //清空字符串
        memset(exp, 0, sizeof(exp));
        //输出结果
        printf("%.2lf\n", value);
    }

    return 0;
}
```

















