# Pandas打卡学习笔记（二）

## Task02:  第二个任务--Pandas基础知识

本次学习计划的第二个task，继续冲

### 一、文件的读取和写入

#### 1.文件的读取

​    在前期学习深度学习搭建神经网络的时候，只接触到了一点的pandas的用法，其中用的最多的--就是Pandas的文件读取。（之前常用的数据集的格式是csv和txt格式）

```python
import pandas as pd
#读取的方法也很简单
file1 = pd.read_csv(path)
file2 = pd.read_table(path)
file3 = pd.read_excel(path)

#还用一些在读取函数中会用到的参数
#header=None:第一行不做为列名
#index = None :不要索引
#index_col 表示把某一列或几列作为索引
# usecols 表示读取列的集合（默认是全部列都读取的）
# parse_dates 表示需要转化为时间的列
#sep=:很好用的分割参数，在一个数据集中遇到过是空格分割的数据集，用这个参数就可以完美的解决
```

ps:看到这里才发现read_table中的sep参数需要的是正则参数，之后使用到的时候要注意了，需要转义的符号要转义好

#### 2.数据的写入

一般在数据写入中，最常用的操作是把 `index` 设置为 `False` 

```python
#像是这样的
df_csv.to_csv('data/my_csv_saved.csv', index=False)
```

`pandas` 中没有定义 `to_table` 函数，但是 `to_csv` 可以保存为 `txt` 文件，并且允许自定义分隔符，常用制表符 `\t` 分割

新知识点：表格也可以转换为markdown和latex格式

但需要安装包---tabulate（目前还没有试过）

### 二、基本的数据结构

主要使用的有两种pandas的基本数据存储结构

存储一维的-----Series

存储二维的-----DataFrame

#### 1.Series

组成Series的四个部分

- 序列的值Data
- 索引index(也可以给索引起一个总的名字)
- 存储的类型dtype
- 序列的名字name

```python
#一个具体的构成，可以是这样的
s = pd.Series(
            data = [1,2,3,4]
            index = pd.Index(['r1', 'r2', 'r3', 'r4'])
            dtype = 'object'
            name = 'panda_test'
) 
```

`object` 代表了一种混合类型

`pandas` 把纯字符串序列也默认认为是一种 `object` 类型的序列，但它也可以用 `string` 类型存储

对于各属性的获取方法

```python
s.values
s.index
s.dtype
s.name
#获取序列的长度，使用的是
s.shape
```

Ps:如果想要取出单个索引对应的值，也可以通过 `[index_item]` 来取出。

#### 2.DataFrame

它在 `Series` 的基础上增加了列索引

数据框可以由二维的 `data` 与行列索引来构造

像是书中的代码写的那样：

```python
data = [[1, 'a', 1.2], [2, 'b', 2.2], [3, 'c', 3.2]]

df = pd.DataFrame(data = data,
                  index = ['row_%d'%i for i in range(3)],
                   columns=['col_0', 'col_1', 'col_2']) df
Out[32]: 
       col_0 col_1  col_2
row_0      1     a    1.2
row_1      2     b    2.2
row_2      3     c    3.2
```

但更多的时候，采用的是从列索引名到数据的映射来构造数据，最后在加上行索引

也是书上举的例子：

```python
In [33]: df = pd.DataFrame(data = {'col_0': [1,2,3], 'col_1':list('abc'),
   ....:                           'col_2': [1.2, 2.2, 3.2]},
   ....:                   index = ['row_%d'%i for i in range(3)])
   ....: 

In [34]: df
Out[34]: 
       col_0 col_1  col_2
row_0      1     a    1.2
row_1      2     b    2.2
row_2      3     c    3.2
```

因为这个从列索引名到数据的映射来构造数据的方式，在 `DataFrame` 中可以用 `[col_name]` 与 `[col_list]` 来取出相应的列与由多个列组成的表。

同时与 `Series` 类似，在数据框中同样可以取出相应的属性，通过 `.T` 还可以把 `DataFrame` 进行转置

### 三、常用基本函数

使用.columns可以获取文件的Index的list

#### 1.汇总函数

常用于数据文件的各个数据的提取和分析使用(为数不多的之前使用过的函数)

- `head（n）, tail（n）` 函数分别表示返回表或者序列的前 `n` 行和后 `n` 行，其中 `n` 默认为5
- `info（）, describe（）` 分别返回表的 信息概况 和表中 数值列对应的主要统计量 

> 书中的小提醒：`info, describe` 只能实现较少信息的展示，如果想要对一份数据集进行全面且有效的观察，特别是在列较多的情况下，推荐使用 [pandas-profiling](https://pandas-profiling.github.io/pandas-profiling/docs/master/index.html) 包

#### 2.特征统计量函数

常见的统计函数有： `sum(), mean(), median(), var(), std(), max(), min()`

这些函数都有一个公共的参数axis=，和其他常用的函数一样

**axis=0:是每列的操作；axis=1:是每行的操作**

特殊记录的函数是 `quantile(), count(), idxmax()`

分别返回的是分位数、非缺失值个数、最大值对应的索引

新知识点：`quantile()：分位数的操作

分位数：亦称**分位点**，是指将一个[随机变量](https://baike.baidu.com/item/随机变量/828980)的[概率分布](https://baike.baidu.com/item/概率分布/828907)范围分为几个等份的数值点，常用的有[中位数](https://baike.baidu.com/item/中位数/3087401)（即二分位数）、[四分位数](https://baike.baidu.com/item/四分位数/5040599)、[百分位数](https://baike.baidu.com/item/百分位数/10064171)等。

#### 3.唯一值函数

对序列使用 `unique` 和 `nunique` 可以分别得到其唯一值组成的列表和唯一值的个数.

例如书上的代码：

```python
In [57]: df['School'].unique()
Out[57]: 
array(['Shanghai Jiao Tong University', 'Peking University',
       'Fudan University', 'Tsinghua University'], dtype=object)

In [58]: df['School'].nunique()
Out[58]: 4
```

`value_counts` 可以得到唯一值和其对应出现的频数

```python
df['School'].value_counts()
>>> 
Tsinghua University              69
Shanghai Jiao Tong University    57
Fudan University                 40
Peking University                34
Name: School, dtype: int64
```

当要求观察多个列的组合的唯一值时，

可以使用新学到的函数drop_duplicates()函数，接收多个列名的list

来取多个列组合的唯一值，其中，关键的参数是keep=

- **默认值** `first` 表示每个组合保留第一次出现的所在行
- `last` 表示每一种的组合成保留最后一次出现的所在行
- `False` 表示把所有重复组合所在的行剔除

下面是书上的代码实列：

```python
In [60]: df_demo = df[['Gender','Transfer','Name']]

In [61]: df_demo.drop_duplicates(['Gender', 'Transfer'])
Out[61]: 
    Gender Transfer            Name
0   Female        N    Gaopeng Yang
1     Male        N  Changqiang You
12  Female      NaN        Peng You
21    Male      NaN   Xiaopeng Shen
36    Male        Y    Xiaojuan Qin
43  Female        Y      Gaoli Feng

In [62]: df_demo.drop_duplicates(['Gender', 'Transfer'], keep='last')
Out[62]: 
     Gender Transfer            Name
147    Male      NaN        Juan You
150    Male        Y   Chengpeng You
169  Female        Y   Chengquan Qin
194  Female      NaN     Yanmei Qian
197  Female        N  Chengqiang Chu
199    Male        N     Chunpeng Lv

In [63]: df_demo.drop_duplicates(['Name', 'Gender'],
                            keep=False).head() # 保留只出现过一次的性别和姓名组合
   
Out[63]: 
   Gender Transfer            Name
0  Female        N    Gaopeng Yang
1    Male        N  Changqiang You
2    Male        N         Mei Sun
4    Male        N     Gaojuan You
5  Female        N     Xiaoli Qian

In [64]: df['School'].drop_duplicates() # 在Series上也可以使用
Out[64]: 
0    Shanghai Jiao Tong University
1                Peking University
3                 Fudan University
5              Tsinghua University
Name: School, dtype: object
```

而duplicated函数的功能与drop_duplicates相似

但duplicated返回的是唯一值的布尔列表，keep的参数还是一样的功能。

duplicated返回的序列：把重复元素设为 `True` ，否则为 `False` 。 `drop_duplicates` 等价于把 `duplicated` 为 `True` 的对应行剔除。

实例的代码块为：

```python
In [65]: df_demo.duplicated(['Gender', 'Transfer']).head()
Out[65]: 
0    False
1    False
2     True
3     True
4     True
dtype: bool

In [66]: df['School'].duplicated().head() # 在Series上也可以使用
Out[66]: 
0    False
1    False
2     True
3    False
4     True
Name: School, dtype: bool
```

#### 4.替换函数

大部分的替换操作，都是针对某一列来进行的操作。

`pandas` 中的替换函数可以归纳为三类：映射替换、逻辑替换、数值替换。

replace()：映射替换的一种，可以通过字典构造，或者传入两个列表来进行替换

```python
#假如要替换的是性别的value值
#提取出性别的所在列，使用的是replace的字典构造的方式，head()出五个来看看结果
df['Gender'].replace({Male: 0 ,Female: 1}).head()

>>>
0    0
1    1
2    1
3    0
4    1
Name: Gender, dtype: int64
```

新方法：replace()的特殊方向上的替换，指定的参数为：method=

- method= `ffill` 用前面一个最近的未被替换的值进行替换
- method= bfill  使用后面最近的未被替换的值进行替换

```python
s = pd.Series(['a', 1, 'b', 2, 1, 1, 'a'])

s.replace([1, 2], method='ffill')
>>>
0    a
1    a
2    b
3    b
4    b
5    b
6    a
dtype: object

s.replace([1, 2], method='bfill')
>>>
0    a
1    b
2    b
3    a
4    a
5    a
6    a
dtype: object
```

PS：要使用正则的替换方式，还是使用str.replace()的方式比较稳妥。

逻辑替换

包括了 `where` 和 `mask` ，这两个函数是完全对称的

-  `where` 函数在传入条件为 `False` 的对应行进行替换，当不指定替换值时，替换为缺失值
- `mask` 在传入条件为 `True` 的对应行进行替换，当不指定替换值时，替换为缺失值

```python
s = pd.Series([-1, 1.2345, 100, -50])

s.where(s<0)
>>>
0    -1.0
1     NaN
2     NaN
3   -50.0
dtype: float64

s.where(s<0, 100)
>>>
0     -1.0
1    100.0
2    100.0
3    -50.0
dtype: float64

s.mask(s<0)
>>>
0         NaN
1      1.2345
2    100.0000
3         NaN
dtype: float64

s.mask(s<0, -50)
>>>
0    -50.0000
1      1.2345
2    100.0000
3    -50.0000
dtype: float64
```

特殊的替换方式，传入的替换条件是---与调用的被替换的Series索引相同的布尔·序列，就可以完成逻辑替换的功能。

```python
#像是这样的情况
s_condition=pd.Series([True,False,true,...],index=s.index)
```

在数值替换中：包含的是这三种方法

1. round()方法:表示的是取整的方法
2. abs():表示的是取绝对值的方法
3. clip():表示的是取截断的方法

```python
#具体的用法
#round()
s = pd.Series([1,2,3,4])
s.round(n)#参数n:数值表达式，表示从小数点位数。
#abs()
s.abs()
#clip()截断函数的用法
#在查阅官方的文档后才看懂书上的那句话
#。clip(a,b)----代表的是 per column using lower and upper thresholds表示上下截断边界

s.clip(1,2)
>>>
0   1
1   2
2   2
3   2
dtype: float64

```

练一练

> 在 `clip` 中，超过边界的只能截断为边界值，如果要把超出边界的替换为自定义的值，应当如何做？

```python
#个人的想法
#使用的是where(),clip().fillna()的组合
#数据量大的话时间复杂度应该会挺高的
#但是暂时没想到其他的方法
    data = pd.Series([1,2,3,4,5])
    data2 = data.where((data >= 1)|(data <= 2))#先把超过上下限的赋为空
    print(data2.clip(1, 2).fillna(value=100))#clip后再赋特定的值
```

#### 5.排序函数

排序共有两种方式，其一为值排序，其二为索引排序，对应的函数是 `sort_values` 和 `sort_index` 。

书上的演示方便：先利用 `set_index` 方法把年级和姓名两列作为索引（多级索引的内容和索引设置的方法将在第三章进行详细讲解）

```python
df_demo = df[['Grade', 'Name', 'Height',
               'Weight']].set_index(['Grade','Name'])

#先使用的是sort_value()的方法
#默认参数 ascending=True 为升序
df_demo.sort_values('Height').head()
#当使用的是多列排序的组合的情况时
#保持身高降序排列，体重升序排列
#在体重相同的情况下，对身高进行排序（体重是优先排序的选择）
df_demo.sort_values(['Weight','Height'],ascending=[True,False]).head()
```

索引排序的用法和值排序完全一致，只不过元素的值在索引中，此时需要指定索引层的名字或者层号

索引层的名字或者层号用--参数level来表示

字符串的排列顺序由字母顺序决定。

```python
df_demo.sort_index(level=['Grade','Name'],ascending=[True,False]).head()

>>>
                        Height  Weight
Grade    Name                         
Freshman Yanquan Wang    163.5    55.0
         Yanqiang Xu     152.4    38.0
         Yanqiang Feng   162.3    51.0
         Yanpeng Lv        NaN    65.0
         Yanli Zhang     165.1    52.0
```

#### 6.apply方法

常用于 `DataFrame` 的行迭代或者列迭代，它的 `axis` 含义与特征统计聚合函数一样的， `apply` 的参数往往是一个以序列为输入的函数

**axis=0:是每列的操作（默认的）；axis=1:是每行的操作**

对于 `.mean()` ，使用 `apply` 可以如下地写出

```python
df_demo = df[['Height', 'Weight']]

def my_mean(x):
    res = x.mean()
    return res
 

df_demo.apply(my_mean)
>>>
Height    163.218033
Weight     55.015873
dtype: float64

#利用 lambda 表达式使得书写简洁
df_demo.apply(lambda x:x.mean())#x 就指代被调用的 df_demo 表中逐个输入的序列
#若指定 axis=1 ，那么每次传入函数的就是行元素组成的 Series
```

知识点： `mad` 函数返回的是一个序列中偏离该序列均值的绝对值大小的均值。

例如序列1,3,7,10中，均值为5.25，每一个元素偏离的绝对值为4.25,2.25,1.75,4.75，这个偏离序列的均值为3.25。

PS：要谨慎的使用apply，除非是真的要使用自定义的需求的情况下，才会选择apply函数。

### 四、窗口对象

引言：`pandas` 中有3类窗口，分别是滑动窗口 `rolling` 、扩张窗口 `expanding` 以及指数加权窗口 `ewm` 。

#### 1.滑动窗口

要使用滑窗函数，就必须先要对一个序列使用 `.rolling` 得到滑窗对象，其最重要的参数为窗口大小 `window` 

```python
s = pd.Series([1,2,3,4,5])
roller = s.rolling(window = 3)#之后滑动对象的操作的范围，都与滑动对象有关。
```

PS：在得到了滑窗对象后，能够使用相应的聚合函数进行计算，需要注意的是窗口包含当前行所在的元素

```python
 s = pd.Series([1,2,3,4,5])
 roller = s.rolling(window = 3)
 roller.mean()
 >>>
0    NaN
1    NaN
2    2.0  #(1+2+3)/3
3    3.0  #(2+3+4)/3
4    4.0  #(3+4+5)/3
dtype: float64
#窗口的大小有关
```

对于滑动相关系数或滑动协方差的计算，也是相似的滑动计算的方法。

此外，还支持使用 `apply` 传入自定义函数.(其传入值是对应窗口的 `Series` )

还有一组类滑动窗口的函数

它们的公共参数为 `periods=n` ，默认为1

- shift(n):表示取向前第 `n` 个元素的值
- diff(n):与向前第 `n` 个元素做差（与 `Numpy` 中不同，后者表示 `n` 阶差分）
- pct_change(n):与向前第 `n` 个元素相比计算增长率

将其视作类滑窗函数的原因是，它们的功能可以用窗口大小为 `n+1` 的 `rolling` 方法等价代替

这里的 `n` 可以为负，表示反方向的类似操作。

书本上的例子：

```python
In [104]: s = pd.Series([1,3,6,10,15])

In [105]: s.shift(2)
Out[105]: 
0    NaN
1    NaN
2    1.0
3    3.0
4    6.0
dtype: float64

In [106]: s.diff(3)
Out[106]: 
0     NaN
1     NaN
2     NaN
3     9.0
4    12.0
dtype: float64

In [107]: s.pct_change()
Out[107]: 
0         NaN
1    2.000000
2    1.000000
3    0.666667
4    0.500000
dtype: float64

In [108]: s.shift(-1)
Out[108]: 
0     3.0
1     6.0
2    10.0
3    15.0
4     NaN
dtype: float64

In [109]: s.diff(-2)
Out[109]: 
0   -5.0
1   -7.0
2   -9.0
3    NaN
4    NaN
dtype: float64
```

练一练

> `rolling` 对象的默认窗口方向都是向前的，某些情况下用户需要向后的窗口，例如对1,2,3设定向后窗口为2的 `sum` 操作，结果为3,5,NaN，此时应该如何实现向后的滑窗操作？（提示：使用 `shift` ）

```python
    #有点感觉不大行，但是能得出正确的答案(用了两种方法)
     # data = pd.Series([1,2,3])
    # #反向的为2的滑动窗口
    # #先得出反向的shift(-1)的数据
    # back_data= data.shift(-1)
    # print(back_data)
    # print(data + back_data)
    data = pd.Series([1, 2, 3])[::-1]
    print(data.rolling(2).sum()[::-1])
```

#### 2.扩展窗口

扩张窗口又称累计窗口，可以理解为一个动态长度的窗口，其窗口的大小就是从序列开始处到具体操作的对应位置，其使用的聚合函数会作用于这些逐步扩张的窗口上。具体地说，设序列为a1, a2, a3, a4，则其每个位置对应的窗口即[a1]、[a1, a2]、[a1, a2, a3]、[a1, a2, a3, a4]。

例子：

```python
s = pd.Series([1, 3, 6, 10])
s.expanding().mean()
>>>
0    1.000000
1    2.000000
2    3.333333
3    5.000000
dtype: float64
```

练一练

> `cummax, cumsum, cumprod` 函数是典型的类扩张窗口函数，请使用 `expanding` 对象依次实现它们。

```python
s.expanding().max()
s.expanding().sum()
s.expanding().prod()
```
练习的代码在代码的文件夹
