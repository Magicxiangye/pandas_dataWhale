---
title: "Pandas打卡学习(三)"
tag: "Pandas"
---

# Pandas打卡学习笔记（三）

## Task03:  第三个任务--第三章：索引

### 一、索引器

#### 1.表的索引

在读取数据的时候，索引就是最经常能够用到的方法之一。其中，列索引是最常见的索引形式。像是通过[ ]来实现，通过[列名]从常见的二维数据DataFrame中去除相对应的一列或者多列。

```python
#像是上一个任务的宝可梦文件数据
df = pd.read_csv('data/pokemon.csv')
#列索引取出某一列
df['Total'].head(5)
```

如果要取出多个列，则可以通过 `[列名组成的列表]` ，其返回值为一个 `DataFrame` 

```python
#取出多个列
df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].head(5)
```

当要取出的单列的列名没带有空格，可以用用 `.列名` 取出，这和 `[列名]` 是等价的。

```python
#像是
df.Total.head()
#与下面这种写法是等价的
df['Total'].head()
```

#### 2.序列的行索引

序列的行索引分为好几种的情况

##### （1）以字符串为索引的 Series

Series只有单列，所以较为方便的可以取出。

取出单个索引的对应元素，则可以使用 `[索引名]` 当`Series` 只有单个值对应，则返回这个标量值，如果有多个值对应，则返回一个 `Series`

```python
 s = pd.Series([1, 2, 3, 4, 5, 6],
                index=['a', 'b', 'a', 'a', 'a', 'c'])
 s['b']#只有单个值对应的索引
 s['a']#多个值对应，返回一个Series
 s[['c', 'b']]#取出多个索引对应的元素
```

当要求出多个索引的对应元素的时候，可以使用类似多列索引一样的方法来使用：可以使用[items的列表]

特殊的：当要取出的是某两个索引之间的元素，且这两个索引的值都是唯一的，可以使用切片的方法（这里的切片会包含两个端点）

```python
s['c': 'b': -2]
#要注意的是，两个索引的方顺序问题
#-2表示的是切片的步长，正负号代表的是方向
>>>这个语句的输出
c    6
a    4
b    2
dtype: int64
```

##### （2）以整数为索引的 Series

知识点：在使用数据的读入函数时，如果不特别指定所对应的列作为索引，那么会生成从0开始的整数索引作为默认索引。当然，**任意一组符合长度要求的整数都可以作为索引。**

和上面的字符串的索引方式一样，分为单个索引和多个的索引，使用 `[索引名]`和使用[索引名的的列表]，可以取出对应索引 元素 的值。

```python
s = pd.Series(['a', 'b', 'c', 'd', 'e', 'f'],
              index=[1, 3, 1, 2, 5, 4])
#单个的情况
 s[1]
#多个的情况
s[[2,3]]
```

使用整数索引的切片，像字符串一样，切片取出对应索引位置的值

（要注意一下这里的整数切片同 `Python` 中的切片一样不包含右端点----好像端点都不包括吧？？？（标记一下））

```python
#我的测试代码(好像左端点也没有)
s = pd.Series(['a', 'b', 'c', 'd', 'e', 'f'],
              index=[1, 3, 1, 2, 5, 4])
print(s[1:-1:1])
>>>
3    b
1    c
2    d
5    e
dtype: object
```

#### 3.loc索引器

这是对于DataFrame的行的选取的方法。

对于DataFrame而言，有两种的索引器，(1)**基于元素**的loc索引器（2）**基于位置**的iloc索引器

loc` 索引器的一般形式是 `loc[*, *]

- 第一个 `*` 代表行的选择
- 第二个 `*` 代表列的选择
- 如果省略第二个位置写作 `loc[*]` ，这个 `*` 是指行的筛选。

 `*` 的位置一共有五类合法对象，分别是：单个元素、元素列表、元素切片、布尔列表以及函数。

书上的任务把相应文件的Name列设置为索引方便学习引用。

```python
df = pd.read_csv('data/learn_pandas.csv')
#set_index方法来实现
df_demo = df.set_index('Name')
```

##### （1）* 为单个元素

直接取出相应的行或列，如果该元素在索引中重复则结果为 `DataFrame`，否则为 `Series`

```python
#单个元素的索引，就是看成为行索引器
df_demo.loc['Qiang Sun'] # 多个人叫此名字
#就会输出 DataFrame
df_demo.loc['Quan Zhao'] # 名字唯一
#就会输出为 Series
```

同时选择行和列，就会定位到相对应的元素，单个的话，就返回的是单个的元素，多个元素匹配的话，就返回一个Series

```python
#使用的列子
df_demo.loc['Qiang Sun', 'School']
```

##### （2）* 为元素的列表

取出列表中所有元素值对应的行或列

```python
In [22]: df_demo.loc[['Qiang Sun','Quan Zhao'], ['School','Gender']]
Out[22]: 
                                  School  Gender
Name                                            
Qiang Sun            Tsinghua University  Female
Qiang Sun            Tsinghua University  Female
Qiang Sun  Shanghai Jiao Tong University  Female
Quan Zhao  Shanghai Jiao Tong University  Female
```

##### （3）* 为切片

`Series` 使用字符串索引时提到，如果是唯一值的起点和终点字符，那么就可以使用切片，并且包含两个端点，PS：如果不唯一则报错

```python
In [23]: df_demo.loc['Gaojuan You':'Gaoqiang Qian', 'School':'Gender']
Out[23]: 
                                      School      Grade  Gender
Name                                                           
Gaojuan You                 Fudan University  Sophomore    Male
Xiaoli Qian              Tsinghua University   Freshman  Female
Qiang Chu      Shanghai Jiao Tong University   Freshman  Female
Gaoqiang Qian            Tsinghua University     Junior  Female
```

如果 `DataFrame` 使用整数索引，其使用整数切片的时候和上面字符串索引的要求一致，都是 元素 切片，包含端点且起点、终点不允许有重复值。

```python
df_loc_slice_demo = df_demo.copy()
#索引倒序
df_loc_slice_demo.index = range(df_demo.shape[0],0,-1)
#切片法
 df_loc_slice_demo.loc[5:3]
 #提取索引5,4,3(默认的步长为1)
```

##### （4）* 为布尔列表

数据处理中，根据条件来筛选行是极其常见的，此处传入 `loc` 的布尔列表与 `DataFrame` 长度相同，且列表为 `True` 的位置所对应的行会被选中， `False` 则会被剔除。（可以传入的是Series，同时iloc传入的时候，只能传入的是序列的.value(在第四节有提到)）

例如，选出体重超过70kg的学生：

```python
df_demo.loc[df_demo.Weight>70].head()
```

传入元素列表，也可以通过 `isin` 方法返回的布尔列表等价写出

例如选出所有大一和大四的同学信息：

```python
In [29]: df_demo.loc[df_demo.Grade.isin(['Freshman', 'Senior'])].head()
Out[29]: 
                                       School     Grade  Gender  Weight Transfer
Name                                                                            
Gaopeng Yang    Shanghai Jiao Tong University  Freshman  Female    46.0        N
Changqiang You              Peking University  Freshman    Male    70.0        N
Mei Sun         Shanghai Jiao Tong University    Senior    Male    89.0        N
Xiaoli Qian               Tsinghua University  Freshman  Female    51.0        N
Qiang Chu       Shanghai Jiao Tong University  Freshman  Female    52.0        N
```

PS:对于复合条件而言，可以用 `|（或）, &（且）, ~（取反）` 的组合来实现

练一练

> `select_dtypes` 是一个实用函数，它能够从表中选出相应类型的列，若要选出所有数值型的列，只需使用 `.select_dtypes('number')` ，请利用布尔列表选择的方法结合 `DataFrame` 的 `dtypes` 属性在 `learn_pandas` 数据集上实现这个功能

```python
  #能出正确的结果，但是好像每次提取的数值的列名不太一样（不懂是什么原因），等等大佬的视频讲解
    df = pd.read_csv('data/learn_pandas.csv')
    #df_demo = df.set_index('Name')
    #若要选出所有数值型的列
    #布尔的选择列表
    #print(df_demo.dtypes)
    condition_dtype = df.dtypes.isin(['int64','float64'])
    final_col = list(df.dtypes.loc[condition_dtype].index)
    print(df[final_col].head())
    
 >>>

```

#####  (5) * 为函数

函数的用法，必须返回的是loc[ ]所能接受的合法形式中的一种。

像是前几个小节中见到的一样，返回的值使得 * 为单个元素、多个元素、切片、布尔列表的结果中的一个，才可以正常的使用这个功能来

需要注意的是函数的形式参数 `x` 本质上即为使用该功能的Series或者DataFrame。

```python
#将条件的布尔列表返回写入函数中
 def condition(x):
      condition = x.School == 'Fudan University'
      return condition
 #这样才可以在loc中使用
 df_demo.loc[condition]
```

同样的，支持函数，就肯定的支持lambda-匿名函数的使用，但是匿名函数的返回值，同样要是四个中的一个。

像是返回一行中的人的性别,就用到了匿名函数的方法

```python
 df_demo.loc[lambda x:'Quan Zhao', lambda x:'Gender']
```

对于 `Series` 也可以使用 `loc` 索引，其遵循的原则与 `DataFrame` 中用于行筛选的 `loc[*]` 完全一致。

使用知识点：

在对表或者序列赋值时，**应当在使用一层索引器后直接进行赋值操作**，这样做是由于进行多次索引后赋值是赋在临时返回的 `copy` 副本上的，而没有真正修改元素从而报出

```python
#像书本上的这个例子中
In [43]: df_chain = pd.DataFrame([[0,0],[1,0],[-1,0]], columns=list('AB'))

In [44]: df_chain
Out[44]: 
   A  B
0  0  0
1  1  0
2 -1  0

In [45]: import warnings

In [46]: with warnings.catch_warnings():
   ....:     warnings.filterwarnings('error')
   ....:     try:
   ....:         df_chain[df_chain.A!=0].B = 1 # 使用方括号列索引后，再使用点的列索引
   ....:     except Warning as w:
   ....:         Warning_Msg = w
   ....: 

In [47]: print(Warning_Msg)

A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy

In [48]: df_chain
Out[48]: 
   A  B
0  0  0
1  1  0
2 -1  0

#索引一层后，该赋值的要马上赋值
In [49]: df_chain.loc[df_chain.A!=0,'B'] = 1

In [50]: df_chain
Out[50]: 
   A  B
0  0  0
1  1  1
2 -1  1
```

#### 4.iloc索引器

使用与 `loc` 完全类似，只不过是针对位置进行筛选

相对应的位置也是有五类的合法对象，分别是：整数、整数列表、整数切片、布尔列表以及函数，和loc一样还是函数返回值必须是前面的四类中的一个。---函数的输入同样也是使用这个方法的对象本身。

```python
#使用的方式
df_demo.iloc[1,1]# 第二行第二列(序号是从零开始的)
#.iloc[行， 列]
df_demo.iloc[[0, 1], [0,1]]#输出的将是前两行前两列
#使用整合的切片的话，切片是不包含结束端点的值的
 df_demo.iloc[1: 4, 2:4]
 #输出将会是
 >>>
                  Gender  Weight
Name                          
Changqiang You    Male    70.0
Mei Sun           Male    89.0
Xiaojuan Sun    Female    41.0
#函数的用法也是返回值必须还是四种中的一个
#python的slice也是不包括结束端点的
df_demo.iloc[lambda x: slice(1, 4)]
```

不同于loc[]的使用，在使用布尔列表的时候要特别注意，不能传入 `Series` 而必须传入序列的 `values` ，否则会报错

（所以在使用布尔筛选的时候还是应当优先考虑 `loc` 的方式。）

例如，选出体重超过80kg的学生：

```python
df_demo.iloc[(df_demo.Weight>80).values].head()
#输出
>>>
                                       School      Grade Gender  Weight Transfer
Name                                                                            
Mei Sun         Shanghai Jiao Tong University     Senior   Male    89.0        N
Qiang Zheng     Shanghai Jiao Tong University     Senior   Male    87.0        N
Qiang Han                   Peking University   Freshman   Male    87.0        N
Chengpeng Zhou               Fudan University     Senior   Male    81.0        N
Feng Han        Shanghai Jiao Tong University  Sophomore   Male    82.0        N
```

对 `Series` 而言同样也可以通过 `iloc` 返回相应位置的值或子序列

```python
#使用定位
df_demo.School.iloc[1]
#切片
df_demo.School.iloc[1:5:2]
```

#### 5.query方法

pandas,支持把字符串形式的查询表达式传入 `query` 方法来查询数据，其表达式的执行结果必须返回的是布尔列表。

这样使用的好处是，体现在复杂的索引时，由于这种检索方式无需像普通方法一样重复使用 `DataFrame` 的名字来引用列名，一般而言会使代码长度在不降低可读性的前提下有所减少。

像是上一节loc的复合条件的列子，在query的方法中，可以写成是。

```python
df.query('((School == "Fudan University")&'
            ' (Grade == "Senior")&'
            ' (Weight > 70))|'
            '((School == "Peking University")&'
            ' (Grade != "Senior")&'
            ' (Weight > 80))')
   
```

在 `query` 表达式中，注册了所有来自 `DataFrame` 的列名，就可以把每一个列可以看作是一个Series,这样所有属于该 `Series` 的方法都可以被调用，非常的方便。

```python
df.query('Weight > Weight.mean()').head()
```

PS：对于含有空格的列名，需要使用 ``col name`` 的方式进行引用。

在可读性方面---在 `query` 中还注册了若干英语的字面用法，帮助提高可读性，例如： `or, and, or, is in, not in` 。

```python
df.query('(Grade not in ["Freshman", "Sophomore"]) and'
           '(Gender == "Male")').head()
```

当字符串中有列表的比较的时候，== 与 != 分别代表的是元素出现在和没有出现在列表中的情况，相当于is in 、not in 

例子:查询表中所有大三大四的信息

```python
 df.query('Grade == ["Junior", "Senior"]').head()
```

特殊的当要引用外部的变量的时候，需要的是在变量的名字前面加上一个@符号，就可以完成引用。

```python
#使用的小例子
low, high =70, 80
df.query('Weight.between(@low, @high)').head()
```

#### 6.随机抽样

 如果把 `DataFrame` 的每一行看作一个样本，或把每一列看作一个特征，再把整个 `DataFrame` 看作总体，想要对样本或特征进行随机抽样就可以用 `sample` 函数。

这样的功能将非常的适合，大型的数据集的特征分布的了解，在无需将所有数据提取而是采用的是总体统计特征的无偏估计(由于许多统计特征在等概率不放回的简单随机抽样条件下，是总体统计特征的无偏估计)。比如样本均值和总体均值，那么就可以先从整张表中抽出一部分来做近似估计。

sample( `n, axis, frac, replace, weights`)函数的主要参数

- n:指抽样数量
- axis:抽样的方向（0为行、1为列）
- frac:抽样比例（0.n则为从总体中抽出n0%的样本）
- replace:是否放回;`replace = True` 则表示有放回抽样
- weight:每个样本的抽样相对概率

例子：构造的 `df_sample` 以 `value` 值的相对大小为抽样概率进行**有放回抽样**，抽样数量为3。

```python
df_sample = pd.DataFrame({'id': list('abcde'),
                         'value': [1, 2, 3, 4, 90]})
#使用sample（）来抽样分析
df_sample.sample(3, replace = True, weights = df_sample.value)
#抽取三个样本，放回的抽样设置，每个样本抽样的相对概率
>>>
#结果肯定是抽样的的相对概率最大的e每次大概率被抽到
 id  value
4  e     90
4  e     90
4  e     90
```

### 二、多级索引

#### 1.多级索引及其表的结构

书中创造了一个具有多级索引结构的DataFrame结构

（由于创造的方法还没学到，等第四个任务结束后，回来补代码）

![multi_index](https://gitee.com/magicye/blogimage/raw/master/img/multi_index.png)

与单层索引的表一样，具备元素值、行索引和列索引三个部分。

但是，索引都是 `MultiIndex` 多层索引类型，每一个索引都是元组，而不是单层索引中的标量。

像是图中的第四行的行索引，元素为（“B”， “Male”）

同样的，列索引中，第二个元素为 `("Height", "Senior")` 

PS:外层连续出现相同的值时，第一次之后出现的会被隐藏显示，使结果的可读性增强(途中的蓝颜色和绿颜色分别表示的就是行索引和列索引的最外层)

从图中可以得知与单层索引类似， `MultiIndex` 也具有名字属性，图中的 `School` 和 `Gender` 分别对应了表的第一层和第二层行索引的名字， `Indicator` 和 `Grade` 分别对应了第一层和第二层列索引的名字。

索引的名字和值属性分别可以通过 `names` 和 `values` 获得：

```python
#由图中可以获得的实例代码
df_multi.index.names
#获得的是每层索引的名字
>>>FrozenList(['School', 'Gender'])
df_multi.columns.names
>>>FrozenList(['Indicator', 'Grade'])
#每层的索引的值
df_multi.index.values
>>>
array([('A', 'Female'), ('A', 'Male'), ('B', 'Female'), ('B', 'Male'),
       ('C', 'Female'), ('C', 'Male'), ('D', 'Female'), ('D', 'Male')],
      dtype=object)
columns.value的使用也是同理
```

某一层的索引的值，则需要通过 `get_level_values（n）` 获得,n是层数

```python
 df_multi.index.get_level_values(0)
>>> Index(['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D'], dtype='object', name='School')
```

修改索引名字的方法，不能直接的直接赋值的方法来实现，

关于如何修改这些属性的话题将在第三节被讨论。

#### 2.多级索引中的loc索引器

回到原来的学习文件，使用set_index()将行索引设置为多级的索引，列索引还是单级的索引

```python
df_multi = df.set_index(['School', 'Grade'])
```

由于多级索引中的单个元素以元组为单位，因此之前在第一节介绍的 `loc` 和 `iloc` 方法完全可以照搬，**只需把标量的位置替换成对应的元组**

**在索引前最好对 `MultiIndex` 进行排序以避免性能警告**

```python
df_multi = df_multi.sort_index()
df_multi.loc[('Fudan University', 'Junior')].head()
#同样的布尔列表和函数都是可以使用的
```

练一练

> 与单层索引类似，若存在重复元素，则不能使用切片，请去除重复索引后给出一个元素切片的例子。

```python
#没理解错题目的意思的话
df_multi = df.set_index(['School', 'Grade'])
df_multi = df_multi.sort_index()
test = set(df_multi.index.values)
print(df_multi.loc[list(test)[0:3]].head())

#输出
>>>
                                      Name  Gender  ...   Test_Date  Time_Record
School            Grade                             ...                         
Peking University Freshman  Changqiang You    Male  ...    2019/9/4      0:04:20
                  Freshman     Gaopeng Shi  Female  ...   2019/9/12      0:04:58
                  Freshman      Gaoli Zhao    Male  ...   2019/10/8      0:03:32
                  Freshman    Xiaojuan Qin    Male  ...  2019/12/10      0:04:10
                  Freshman       Qiang Han    Male  ...    2020/1/7      0:03:58
```

在多级索引中的元组有一种特殊的用法，可以对**多层的元素进行交叉组合后索引**(就是多层索引值之间的交叉组合方式)，但同时需要指定 `loc` 的列，**全选则用 `:`** 表示。其中，每一层需要选中的元素用列表存放，传入 `loc` 的形式为 `[(level_0_list, level_1_list), cols]` （传入行的元组中，一层的索引值用一个list来陈放）。例如，想要得到所有北大和复旦的大二大三学生，可以如下写出：

```python
res = df_multi.loc[(['Peking University', 'Fudan University'],
                     ['Sophomore', 'Junior']), :]

res.head()
>>>
                                     Name  Gender  Weight Transfer
School            Grade                                           
Peking University Sophomore   Changmei Xu  Female    43.0        N
                  Sophomore  Xiaopeng Qin    Male     NaN        N
                  Sophomore        Mei Xu  Female    39.0        N
                  Sophomore   Xiaoli Zhou  Female    55.0        N
                  Sophomore      Peng Han  Female    34.0      NaN

 res.shape
 (33, 4)
```

这和一组组元组传入的选取是不同的，一组组传入的话，不可以交叉的组合，就没有更多的选项。

#### 3.IndexSlice对象

在前面的方法中，即使在索引不重复的时候，也只能对元组整体进行切片，而不能对每层进行切片，也不允许将切片和布尔列表混合使用，引入 `IndexSlice` 对象就能解决这个问题。

 `Slice` 对象一共有两种形式

- 第一种为 `loc[idx[*,*]]` 型
- 第二种为 `loc[idx[*,*],idx[*,*]]` 型

方便实例的代码，先构造一个无重复索引的DataFrame

```python
np.random.seed(0)
L1,L2 = ['A','B','C'],['a','b','c']
mul_index1 = pd.MultiIndex.from_product([L1,L2],names=('Upper', 'Lower'))
L3,L4 = ['D','E','F'],['d','e','f']
mul_index2 = pd.MultiIndex.from_product([L3,L4],names=('Big', 'Small'))
df_ex = pd.DataFrame(np.random.randint(-9,10,(9,9)),
                      index=mul_index1,
                      columns=mul_index2)
#构造的输出
>>>
Big          D        E        F      
Small        d  e  f  d  e  f  d  e  f
Upper Lower                           
A     a      3  6 -9 -6 -6 -2  0  9 -5
      b     -3  3 -8 -3 -2  5  8 -4  4
      c     -1  0  7 -4  6  6 -9  9 -6
B     a      8  5 -2 -9 -8  0 -9  1 -6
      b      2  9 -7 -9 -9 -5 -4 -3 -1
      c      8  6 -5  0  1 -8 -8 -2  0
C     a     -6 -3  2  5  9 -9  5 -6  3
      b      1  2 -5 -3 -5  6 -6  3 -5
      c     -1  5  6 -6  6  4  7  8 -4
```

在使用silce对象之前，要先进行对象的定义

```python
idx = pd.IndexSlice
```

##### (1) `loc[idx[*,*]]` 型

这种情况并**不能进行多层分别切片**，前一个 `*` 表示行的选择，后一个 `*` 表示列的选择，与单纯的 `loc` 是类似的

```python
df_ex.loc[idx['C':, ('D', 'f'):]]
#行的选择和列的选择都是使用了切片
#这样将会输出为
>>>
Big          D  E        F      
Small        f  d  e  f  d  e  f
Upper Lower                     
C     a      2  5  9 -9  5 -6  3
      b     -5 -3 -5  6 -6  3 -5
      c      6 -6  6  4  7  8 -4
#同时，这个方法也是接受布尔序列的函数
 df_ex.loc[idx[:'A', lambda x:x.sum()>0]]
 #选择的是A行，且列的和大于零的列
```

##### （2） `loc[idx[*,*],idx[*,*]]` 型

**这种情况能够分层进行切片**前一个 `idx` 指代的是行索引，后一个是列索引。

还是看代码的实列来学习，每个idx中，多种合理的输入方法可以组合使用

```python
 df_ex.loc[idx[:'A', 'b':], idx['E':, 'e':]]
  >>>
Big          E     F   
Small        e  f  e  f
Upper Lower            
A     b     -2  5 -4  4
      c      6  6  9 -6

```

#### 4.多级索引的构造

那么除了使用 `set_index` 之外，自己构造索引的话

可以使用的是 `from_tuples, from_arrays, from_product` 

它们都是 `pd.MultiIndex` 对象下的函数。

`from_tuples` 指根据传入由元组组成的列表进行构造：

```python
my_tuple = [('a','cat'),('a','dog'),('b','cat'),('b','dog')]#要把所有层的组合都列出来才可以
pd.MultiIndex.from_tuples(my_tuple, names=['First','Second'])
```

`from_product` 指根据给定**多个列表的笛卡尔积**进行构造：

```python
 my_list1 = ['a','b']
 my_list2 = ['cat','dog']
 pd.MultiIndex.from_product([my_list1,
                             my_list2],
                              names=['First','Second'])
#这样将会生成
>>>
MultiIndex([('a', 'cat'),
            ('a', 'dog'),
            ('b', 'cat'),
            ('b', 'dog')],
           names=['First', 'Second'])

```

### 三、索引的常用方法

#### 1. 索引层的交换和删除

先构造一个三级的索引的例子，来方便下面的学习这里使用的是from_product的方法

```python
import numpy as np
np.random.seed(0)#随机数的固定
L1,L2,L3 = ['A','B'],['a','b'],['alpha','beta']
mul_indexs = pd.MultiIndex.from_product([L1,L2,L3],names=('Upper', 'Lower','Extra'))
L4,L5,L6 = ['C','D'],['c','d'],['cat','dog']
mul_colums = pd.MultiIndex.from_product([L4,L5,L6],names=('Big', 'Small', 'Other'))
df_ex = pd.DataFrame(np.random.randint(-9,10,(8,8)),index=mul_indexs, columns=mul_colums)
```

行的索引是一个三级的索引

索引的交换可以由函数---swaplevel和reorder_levels来实现

- swaplevel():只能交换两个层
- reorder_levels();可以交换任意层(即可以多层同时的交换)

两者都可以指定交换的是轴是哪一个，即行索引或列索引

```python
df_ex.swaplevel(0,2,axis=1).head() # 列索引的第一层和第三层交换
#0,2表示的是要交换的层数
#多个层的的一起交换
df_ex.reorder_levels([2,0,1],axis=0).head() # 列表数字指代原来索引中的层
#[]层数的交换方式和tf.transpose()的方式一样
#都可以指定交换的轴
```

行列的索引交换在第五章里会学习到。

若想要删除某一层的索引，可以使用 `droplevel` 方法：

```python
#还是可以指定修改的轴
df_ex.droplevel(1,axis=1)
#将列索引的第二层删除
#输出
>>>
Big                 C               D            
Other             cat dog cat dog cat dog cat dog
Upper Lower Extra                                
A     a     alpha   3   6  -9  -6  -6  -2   0   9
            beta   -5  -3   3  -8  -3  -2   5   8
      b     alpha  -4   4  -1   0   7  -4   6   6
            beta   -9   9  -6   8   5  -2  -9  -8
B     a     alpha   0  -9   1  -6   2   9  -7  -9
            beta   -9  -5  -4  -3  -1   8   6  -5
      b     alpha   0   1  -8  -8  -2   0  -6  -3
            beta    2   5   9  -9   5  -6   3   1
#当要删除的是多层的时候，传入的是一个要删除的list
df_ex.droplevel([0,1], axis=0)
>>>
Big     C               D            
Small   c       d       c       d    
Other cat dog cat dog cat dog cat dog
Extra                                
alpha   3   6  -9  -6  -6  -2   0   9
beta   -5  -3   3  -8  -3  -2   5   8
alpha  -4   4  -1   0   7  -4   6   6
beta   -9   9  -6   8   5  -2  -9  -8
alpha   0  -9   1  -6   2   9  -7  -9
beta   -9  -5  -4  -3  -1   8   6  -5
alpha   0   1  -8  -8  -2   0  -6  -3
beta    2   5   9  -9   5  -6   3   1
```

#### 2.索引属性的修改

索引的属性的修改可以通过-----rename_axis()对索引层的名字进行修改，常用的**修改方式是传入字典的映射**：

```python
df_ex.rename_axis(index={'old_value': 'new_value'}, columns={'old_value': 'new_value'}).head()
```

也可以通过rename()来对索引的属性进行修改，如果是多级索引需要指定修改的层号 `level` :

```python
#用法
#是多级索引的话，还要加上层号
df_ex.rename(columns={'old_value': 'new_value'},level=2).head()
```

传入参数也可以是函数，其**输入值就是索引元素**：

```python
df_ex.rename(index=lambda x:str.upper(x), level=2).head()
#输出为
>>>
Big                 C               D            
Small               c       d       c       d    
Other             cat dog cat dog cat dog cat dog
Upper Lower Extra                                
A     a     ALPHA   3   6  -9  -6  -6  -2   0   9
            BETA   -5  -3   3  -8  -3  -2   5   8
      b     ALPHA  -4   4  -1   0   7  -4   6   6
            BETA   -9   9  -6   8   5  -2  -9  -8
B     a     ALPHA   0  -9   1  -6   2   9  -7  -9
```

练一练

> 尝试在 `rename_axis` 中使用函数完成与例子中一样的功能。

```python

```

对于整个索引的元素替换，可以利用迭代器实现：

```python
#结合迭代器来使用
#先建立一个迭代器
new_values = iter(list('abcdefgh'))
df_ex.rename(index=lambda x:next(new_values),level=2)
#输出的结果为
>>>
Big                 C               D            
Small               c       d       c       d    
Other             cat dog cat dog cat dog cat dog
Upper Lower Extra                                
A     a     a       3   6  -9  -6  -6  -2   0   9
            b      -5  -3   3  -8  -3  -2   5   8
      b     c      -4   4  -1   0   7  -4   6   6
            d      -9   9  -6   8   5  -2  -9  -8
B     a     e       0  -9   1  -6   2   9  -7  -9
            f      -9  -5  -4  -3  -1   8   6  -5
      b     g       0   1  -8  -8  -2   0  -6  -3
            h       2   5   9  -9   5  -6   3   1
```

若想要对某个位置的元素进行修改，在单层索引时容易实现，即先取出索引的 `values` 属性，**再给对得到的列表进行修改，最后再对 `index` 对象重新赋值。**但是如果是多级索引的话就有些麻烦，一个解决的方案是先把某一层索引临时转为表的元素，然后再进行修改，最后重新设定为索引，下面一节将介绍这些操作.

map()函数：是定义在Index上的方法，与上面的rename的函数式方法是相似的，**只不过它传入的不是层的标量值，而是直接传入索引的元组**

用户进行**跨层的修改提供了遍历**。例如，可以等价地写出上面的字符串转大写的操作

```python
#还是修改大小写的问题
new_indexs = df_ex.index.map(lambda x: (x[0], x[1], str.upper(x[2])))
#再更新原来的index,重新的赋值
df_ex.index = newe_indexs
```

关于 `map()` 的另一个重要的使用方法是**对多级索引的压缩**，这在第四章和第五章的一些操作中是有用的

还是用的是函数式的方法。

```python
 df_temp = df_ex.copy()

 new_idx = df_temp.index.map(lambda x:(x[0]+'-'+ x[1]+'-'+ x[2]))

df_temp.index = new_idx

df_temp.head() # 单层索引
>>>
Big         C               D            
Small       c       d       c       d    
Other     cat dog cat dog cat dog cat dog
A-a-alpha   3   6  -9  -6  -6  -2   0   9
A-a-beta   -5  -3   3  -8  -3  -2   5   8
A-b-alpha  -4   4  -1   0   7  -4   6   6
A-b-beta   -9   9  -6   8   5  -2  -9  -8
B-a-alpha   0  -9   1  -6   2   9  -7  -9
```

同时也可以将单层的索引拆开

```python
new_idx = df_temp.index.map(lambda x:tuple(x.split('-')))
df_temp.index = new_idx
df_temp.head() # 三层索引
#张开成为三层的索引
>>>
Big         C               D            
Small       c       d       c       d    
Other     cat dog cat dog cat dog cat dog
A a alpha   3   6  -9  -6  -6  -2   0   9
    beta   -5  -3   3  -8  -3  -2   5   8
  b alpha  -4   4  -1   0   7  -4   6   6
    beta   -9   9  -6   8   5  -2  -9  -8
B a alpha   0  -9   1  -6   2   9  -7  -9
```

#### 3.索引的设置与重置

说明这一节函数的使用，下面构造一个新表

```python
#设置一个新的DataFrame
df_new = pd.DataFrame({'A':list('aacd'),'B':list('PORT'),'c':[1,2,3,4]})
#生成的表
>>>
   A  B  C
0  a  P  1
1  a  Q  2
2  c  R  3
3  d  T  4
```

在索引设置的方法上，之前的小节中，就有使用到这几种的方法，像是方法set_index():主要的参数，除了索引名，还有就是append参数：它代表着**是否来保留原来的索引**，保留的话直接把新设定的添加到原索引的内层。

```python
df_new.set_index('A', appcend=true)
#append的默认是Flase
>>>
     B  C
  A      
0 a  P  1
1 a  Q  2
2 c  R  3
3 d  T  4
#同时这个方法发也可以指定多个列作为索引：
#传入的是一个索引名的list
df_new.set_index(['A'， 'B'])
#如果想要添加索引的列没有出现再其中，那么可以直接在参数中传入相应的 Series
#设置一个想要变为索引的列
my_indexs = df.Series(list('WXYZ'), name='D')
df_new = df_new.set_index(['A', my_indexs])
#DataFrame将会变为
     B  C
A D      
a W  P  1
  X  Q  2
c Y  R  3
d Z  T  4
```

有添加就有去除，reset_index就是set_index的逆函数

它主要的参数就是drop:表示是否要把传入的索引层丢弃而不是添加到列中(默认是把它还原为一列)

```python
#接上一块的代码继续示范
df_new.reset_index(['D'])#把索引层D去掉
#将会输出
>>>
   D  B  C
A         
a  W  P  1
a  X  Q  2
c  Y  R  3
d  Z  T  4
#D还原回了一列
df_new.reset_index(['D'], drop=True)#当drop为True的时候
>>>
#D列将直接被删除
   B  C
A      
a  P  1
a  Q  2
c  R  3
d  T  4

#特殊的，当重置了所有的索引，那么 pandas 会直接重新生成一个默认索引
```

#### 4.索引的变形

在某些场合下，需要对索引做一些扩充或者剔除，更具体地要求是给定一个新的索引，把原表中相应的索引对应元素填充到新索引构成的表中。例如，出了员工信息，需要重新制作一张新的表，要求增加一名员工的同时去掉身高列并增加性别列：

要使用的方法是reindex()来重新的设置行列的索引值

```python
#原表格
df_reindex = pd.DataFrame({"Weight":[60,70,80],"Height":[176,180,179]},index=['1001','1003','1002'])
#设置的方法
#原来有的会保留，新的列没有指定值的话先NaN
df_reindex.reindex(index=['1001','1002','1003','1004'],columns=['Weight','Gender'])
>>>
      Weight  Gender
1001    60.0     NaN
1002    80.0     NaN
1003    70.0     NaN
1004     NaN     NaN
```

这种需求**常出现在时间序列索引的时间点填充以及 `ID` 编号的扩充**。另外，需要注意的是原来表中的数据和新表中会根据索引自动对其，例如原先的1002号位置在1003号之后，而新表中相反，那么 **`reindex` 中会根据元素对齐，与位置无关**。

还有一个与 `reindex` 功能类似的函数是 `reindex_like` ，其功能是仿照传入的表的索引来进行被调用表索引的变形。

相当于传入一个模板，来进行变形。

```python
#使用的方法
#设定一个样式模板
df_existed = pd.DataFrame(index=['1001','1002','1003','1004'],  columns=['Weight','Gender'])
#使用方法来变形
df_reindex.reindex_like(df_existed)
```

### 四、索引运算

#### 1. 集合的运算法则

经常会有一种利用集合运算来取出符合条件行的需求。

先来回顾一下常用的集合运算

![公式](https://gitee.com/magicye/blogimage/raw/master/img/image-20201220204737890.png)

#### 2. 一般的索引运算

由于集合的元素是互异的，但是索引中可能有相同的元素，先用 `unique` 去重后再进行运算。下面构造两张最为简单的示例表进行演示

```python
 df_set_1 = pd.DataFrame([[0,1],[1,2],[3,4]], index = pd.Index(['a','b','a'],name='id1'))
 df_set_2 = pd.DataFrame([[4,5],[2,6],[7,1]],index = pd.Index(['b','b','c'],name='id2'))
#取出去掉了重复索引的索引值
id1, id2 = df_set_1.index.unique(),df_set_2.index.unique()
#id1=[a, b],id2=[b, c]
id1.intersection(id2)
Index(['b'], dtype='object')

id1.union(id2)
Index(['a', 'b', 'c'], dtype='object')

id1.difference(id2)
Index(['a'], dtype='object')

id1.symmetric_difference(id2)
Index(['a', 'c'], dtype='object')
```

同时上述的四类运算还可以用等价的符号表示代替如下：

```python
id1 & id2
id1 | id2
(id1 ^ id2) & id1
id1 ^ id2 # ^符号即对称差
```

若两张表需要做集合运算的列并没有被设置索引，一种办法是先转成索引，运算后再恢复，另一种方法是利用 `isin` 函数，例如在重置索引的第一张表中选出id列交集的所在行：

```
In [162]: df_set_in_col_1 = df_set_1.reset_index()

In [163]: df_set_in_col_2 = df_set_2.reset_index()

In [164]: df_set_in_col_1
Out[164]: 
  id1  0  1
0   a  0  1
1   b  1  2
2   a  3  4

In [165]: df_set_in_col_2
Out[165]: 
  id2  0  1
0   b  4  5
1   b  2  6
2   c  7  1

In [166]: df_set_in_col_1[df_set_in_col_1.id1.isin(df_set_in_col_2.id2)]
Out[166]: 
  id1  0  1
1   b  1  2
```

### 五、练习

练习的代码在代码的文件夹里。