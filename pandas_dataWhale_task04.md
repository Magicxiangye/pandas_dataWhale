---
title: "Pandas打卡学习笔记（四）"
tag: "Pandas"
---

# Pandas打卡学习笔记（四）

## Task04 ---第四章：分组

### 一、分组模式及其对象

#### 1.分组的一般模式

实现分组操作的三个要素：分组依据 、 数据来源 、 操作及其返回结果 。同时从充分性的角度来说，如果明确了这三方面，就能确定一个分组操作，从而分组代码的一般模式即：

```python
df = pd.read_csv('data/learn_pandas.csv')
df.groupby(分组的依据)[数据的来源].使用的操作
```

像是：依据 性别 分组，统计全国人口 寿命 的 平均值

```python
df.groupby('Gender')['Longevity'].mean()
```

#### 2.分组依据的本质

当需要根据多个维度进行分组时，只需在 `groupby` 中传入相应列名构成的列表即可。

```python
#根据学校和性别进行分组，统计身高的均值就可以如下写出：
df.groupby(['School', 'Gender'])['Height'].mean()
>>>
Gender
Female    159.6
Male      173.4
Name: Height, dtype: float64
```

同时，想要通过一定的复杂逻辑来分组，首先**应该先写出分组条件。**

例子：据学生体重是否超过总体均值来分组，同样还是计算身高的均值。

```python
#先写出分组的条件
 condition = df.Weight > df.Weight.mean()
 #再使用groupby()[].的方法
df.groupby(condition)['Height'].mean()
>>>
Weight
False    159.034646
True     172.705357
Name: Height, dtype: float64
```

练一练

> 请根据上下四分位数分割，将体重分为high、normal、low三组，统计身高的均值。

```python
#先学习一下上下四分位数的分割方法
import numpy as np
lower_q=np.quantile(df['Weight'],0.25,interpolation='lower')#下四分位数
higher_q=np.quantile(df['Weight'],0.75,interpolation='higher')#上四分位数
df_new = df.mask(((df['Weight'] >= lower_q)&(df['Weight'] <= higher_q)),'normal').mask(df['Weight'] > higher_q, 'high').mask(df['Weight'] < lower_q, 'low')
#分组
df.groupby('Weight')['Height'].mean()
```

从上几个代码块中可以看出，最后产生的分组的结果按照条件列表中元素的值来分组。

用随机传入字母序列来验证这一想法：

```python
item = np.random.choice(list('abc'), df.shape[0])
df.groupby(item)['Height'].mean()

#输出
>>>
a    163.924242
b    162.928814
c    162.708621
Name: Height, dtype: float64
```

如果传入多个序列进入 `groupby` ，那么最后分组的依据就是这两个序列对应行的去掉重复的所有组合：

```python
df.groupby([condition, item])['Height'].mean()
>>>
Weight   
False   a    160.193617
        b    158.921951
        c    157.756410
True    a    173.152632
        b    172.055556
        c    172.873684
Name: Height, dtype: float64
```

也可以说是，最后分组的依据来自于分组列组合的unique值，通过 `drop_duplicates` 就能知道具体的组类别，多少种无重复的组合：

```python
#像是分组本质中的School和Gender的例子
df[['School', 'Gender']].drop_duplicates()
>>>
#这两个列的无重复的数据项的组合
                          School  Gender
0   Shanghai Jiao Tong University  Female
1               Peking University    Male
2   Shanghai Jiao Tong University    Male
3                Fudan University  Female
4                Fudan University    Male
5             Tsinghua University  Female
9               Peking University  Female
16            Tsinghua University    Male
```

#### 3.Groupby对象

在具体的分组的操作的时候，使用的都是来源于Pandas中的groupby对象，这一节，介绍的是这个对象的常用的方法和方便的属性。

通过 `ngroups` 属性，可以访问分为了多少组。

通过 `groups` 属性，可以返回从 组名 映射到 组索引列表 的字典：

```python
gb = df.groupby(['School', 'Grade'])
gb
>>>
<pandas.core.groupby.generic.DataFrameGroupBy object at 0x00000263B9E494C8>
gb.ngroups
>>>
#输出的是分组的个数
res = gb.groups
res.keys()#展示的是字典的keys
```

练一练

> 上一小节介绍了可以通过 `drop_duplicates` 得到具体的组类别，现请用 `groups` 属性完成类似的功能。

```python
df.groupby(['School', 'Grade']).groups.keys()
```

当 `size` 作为 `DataFrame` 的属性时，返回的是表长乘以表宽的大小，但在 `groupby` 对象上**表示统计每个组的元素个数**

```python
gb.size()
>>>
#显示的是每个组的元素个数
School                         Grade    
Fudan University               Freshman      9
                               Junior       12
                               Senior       11
                               Sophomore     8
Peking University              Freshman     13
                               Junior        8
                               Senior        8
                               Sophomore     5
Shanghai Jiao Tong University  Freshman     13
                               Junior       17
                               Senior       22
                               Sophomore     5
Tsinghua University            Freshman     17
                               Junior       22
                               Senior       14
                               Sophomore    16
dtype: int64
```

通过 `get_group` 方法可以直接获取所在组对应的行，此时必须知道组的具体名字：

```python
gb.get_group(('Fudan University', 'Freshman')).iloc[:3, :3] # 展示一部分
>>>
             School     Grade             Name
15  Fudan University  Freshman  Changqiang Yang
28  Fudan University  Freshman     Gaoqiang Qin
63  Fudan University  Freshman     Gaofeng Zhao
```

#### 4.分组的三大操作

前面举的例子，这三个的类型的分组返回数据的结果形态是不一样的

- 分组的返回值可以是个标量值，可以是平均值、中位数、组容量 `size` 等
- 在做了原序列的标准化处理后，每组返回的是一个 `Series` 类型
- 同样的，也可以返回整个组所在行的本身，即返回了 `DataFrame` 类型

由此，引申出分组的三大操作：**聚合、变换和过滤**，分别对应了三个例子的操作，下面就要分别介绍相应的 `agg` 、 `transform` 和 `filter` 函数及其操作。

### 二、聚合函数

#### 1.内置聚合函数

先学习一些定义在Groupby()对象里的聚合函数，使用功能时应当优先考虑。根据返回标量值的原则。

`max/min/mean/median/count/all/any/idxmax/idxmin/mad/nunique/skew/quantile/sum/std/var/sem/size/prod` 。

```python
 gb = df.groupby('Gender')['Height']
 gb.idxmin()
 >>>
 Gender
Female    143
Male      199
Name: Height, dtype: int64
```

练一练

> 请查阅文档，明确 `all/any/mad/skew/sem/prod` 函数的含义。

```python
all()
#含义是Return True if all values in the group are truthful, else False.
any()同理
#Return True if any value in the group is truthful, else False.
mad()
#返回请求轴的值的均值绝对偏差。主要的参数axis
skew()
#求的是指定的轴上的偏度（skewness），是统计数据分布偏斜方向和程度的度量，是统计数据分布非对称程度的数字特征。偏度(Skewness)亦称偏态、偏态系数。 
sem()
#计算组平均值的标准误差，不包括缺失值。(参数是 ddofint, default 1)
prod()
#计算每个组中的值的组。
```

这些聚合函数当传入的数据来源包含多个列时，将按照列进行迭代计算：

```python
gb = df.groupby('Gender')[['Height', 'Weight']]
gb.max()
>>>
        Height  Weight
Gender                
Female   170.2    63.0
Male     193.9    89.0
```

#### 2.agg方法

聚合使用

在groupby对象上的不便之处

- 无法同时使用多个函数
- 无法对特定的列使用特定的聚合函数
- 无法使用自定义的聚合函数
- 无法直接对结果的列名在聚合前进行自定义命名

##### （1）使用多个函数

当使用多个聚合函数时，需要用**列表的形式**把内置聚合函数的对应的字符串传入，先前**提到的所有字符串都是合法的**。

```python
gb.agg(['sum', 'idxmax', 'skew'])
>>>
         Height                   Weight                 
            sum idxmax      skew     sum idxmax      skew
Gender                                                   
Female  21014.0     28 -0.219253  6469.0     28 -0.268482
Male     8854.9    193  0.437535  3929.0      2 -0.332393
```

从代码的结果来看，此时的列索引为多级索引，第一层为数据源，第二层为使用的聚合方法，分别逐一对列使用聚合

##### （2）对特定的列使用特定的聚合函数

对于方法和列的特殊对应，可以通过**构造字典传入 `agg` 中实现**，其中字典以列名为键，以聚合字符串或字符串列表为值。

像是这样的代码

```python
gb.agg({'Height':['mean','max'], 'Weight':'count'})
```

练一练

> 请使用【2】中的传入字典的方法完成【1】中等价的聚合任务。

```python
gb.agg({'Height':['sum', 'idxmax', 'skew'], 'Weight':['sum', 'idxmax', 'skew']})
```

##### （3）使用自定义函数

在 `agg` 中可以使用具体的自定义函数， 需要注意**传入函数的参数是之前数据的来源中的列**，逐列进行计算

练一练

> 在 `groupby` 对象中可以使用 `describe` 方法进行统计信息汇总，请同时使用多个聚合函数，完成与该方法相同的功能。

```python
#describe函数，能够直接输出最大值、最小值、均值、方差、分位数等等
gb.agg(lambda x: set(x.max(), x.min(), x.mean(),x.quantile(0.5)))
```

由于传入的是序列，因此**序列上的方法和属性都是可以在函数中使用的**，只需保证返回值是标量即可。下面的例子是指，如果组的指标均值，超过该指标的总体均值，返回High，否则返回Low。

```python
def my_func(s):
     res = 'High'
     if s.mean() <= df[s.name].mean():
        res = 'Low'
      return res
gb.agg(my_func)
>>>
       Height Weight
Gender              
Female    Low    Low
Male     High   High
```

##### （4）聚合结果重命名

想要对**结果进行重命名**，只需要**将上述函数的位置改写成元组**，元组的**第一个元素为新的名字**，**第二个位置为原来的函数**，包括聚合字符串和自定义函数，现举若干例子说明：

```python
gb.agg([('range', lambda x: x.max()-x.min()), ('my_sum', 'sum')])
#给特定的列使用
gb.agg({'Height': [('my_func', my_func), 'sum'],'Weight': lambda x:x.max()})
```

另外需要注意，使用对一个或者多个列**使用单个聚合的时候**，**重命名需要加方括号**，否则就不知道是新的名字还是手误输错的内置函数字符串：

```python
 gb.agg([('my_sum', 'sum')])
 gb.agg({'Height': [('my_func', my_func), 'sum'],
  'Weight': [('range', lambda x:x.max())]})
```

### 三、变换和过滤

#### 1. 变换函数与transform方法

变换函数的**返回值为同长度的序列**，最常用的内置变换函数是累计函数： `cumcount/cumsum/cumprod/cummax/cummin` ，它们的使用方式和聚合函数类似，只不过完成的是**组内累计操作**。

`groupby` 对象定义的其他函数将会在其他章节学习到。

```python
gb.cummax().head()
   Height  Weight
0   158.9    46.0
1   166.5    70.0
2   188.9    89.0
3     NaN    46.0
4   188.9    89.0
```

练一练

> 在 `groupby` 对象中， `rank` 方法也是一个实用的变换函数，请查阅它的功能并给出一个使用的例子。

```python
#rank()这是一个排名函数，目的就是按照某种规则（从大到小，从小到大）给原序列的值进行排名。所返回的结果也是一个序列
#rank函数的默认处理是当出现重复值的情况下，默认取他们排名次序值（像是第1名、第2名）的平均值。也就是说索引0和索引1对应的值1统一排名为（1+2）/2 = 1.5。
#使用，给gb对象的列使用默认的排列
#通过设置method参数，可以控制自己想要的排名方式。
#以考试排名为例子
    method='average' （默认设置）:那么这两个人就占据了前两名，分不出谁第 1，谁第 2，就把两人的名次算个平均数，都算 1.5 名，这样下一个人就是第3名。

    method='max':两人并列第 2 名，下一个人是第 3 名。

    method='min':两人并列第 1 名，下一个人是第 3 名。

    method='dense':两人并列第 1 名，但下一个人是第 2 名。

    method='first':那么试卷先被改出来的人是第 1 名，试卷后被改出来的是第 2 名.

gb.rank()
```

当用自定义变换时需要使用 `transform` 方法，被调用的**自定义函数**， 其**传入值为数据源的序列** ，**与 `agg` 的传入类型是一致的**，其最后的返回结果是行列索引与数据源一致的 `DataFrame` 。

例子：对身高和体重进行分组标准化，即减去组均值后除以组的标准差：

```
gb.transform(lambda x: (x-x.mean())/x.std()).head()
#输出
>>>
     Height    Weight
0 -0.058760 -0.354888
1 -1.010925 -0.355000
2  2.167063  2.089498
3       NaN -1.279789
4  0.053133  0.159631
```

练一练

> 对于 `transform` 方法无法像 `agg` 一样，通过传入字典来对指定列使用特定的变换，如果需要在一次 `transform` 的调用中实现这种功能，请给出解决方案。

```python
#暂时没想到，难道要用匿名函数提取index吗
```

前面提到了 `transform` 只能返回同长度的序列，但事实上**还可以返回一个标量，这会使得结果被广播到其所在的整个组**，这种 **标量广播** 的技巧在特征工程中是非常常见的。

例如，构造两列新特征来分别表示样本所在性别组的身高均值和体重均值：

```python
 gb.transform('mean').head() # 传入返回标量的函数也是可以的
```

#### 2. 组索引与过滤

过滤在分组中是对于组的过滤，而索引是对于行的过滤.

在第二章中的返回值，无论是布尔列表还是元素列表或者位置列表，本质上都是对于行的筛选，即如果筛选条件的则选入结果的表，否则不选入。

组过滤作为行过滤的推广，指的是如果对一个组的全体所在行进行统计的结果返回 `True` 则会被保留， `False` 则该组会被过滤，**最后把所有未被过滤的组其对应的所在行拼接起来作为 `DataFrame` 返回**。

`groupby` 对象中，定义了 `filter` 方法进行组的筛选

当使用的是自定义的函数的时候，**输入参数为数据源构成的 `DataFrame` 本身**（无论数据的来源有几列）。**返回的是布尔值**

所有表方法和属性都可以在自定义函数中相应地使用，同时只需保证自定义函数的返回为布尔值即可。

例如，在原表中通过过滤得到所有容量大于100的组(即使分组中大于100行的数据，得出)：

```python
gb = df.groupby('Gender')[['Height', 'Weight']]
gb.filter(lambda x: x.shape[0] > 100).head()
```

练一练

> 从概念上说，索引功能是组过滤功能的子集，请使用 `filter` 函数完成 `loc[.]` 的功能，这里假设 ” `.` “是元素列表。

```python
#.是元素列表。
#应该就是groupby对象的数据来源
#设还是以Gender作为分组依据
gb = df.groupby('Gender')[.]
gb.filter(匿名函数)
```

### 四、跨列分组

#### 1.apply的引入

事实上还有一种常见的分组场景，无法用前面介绍的任何一种方法处理，例如现在如下定义身体质量指数BMI：

![公式2](https://gitee.com/magicye/blogimage/raw/master/img/image-20201223202055344.png)

其中体重和身高的单位分别为千克和米，需要分组计算组BMI的均值。

**首先，这显然不是过滤操作，因此 `filter` 不符合要求；其次，返回的均值是标量而不是序列，因此 `transform` 不符合要求；最后，似乎使用 `agg` 函数能够处理，但是之前强调过聚合函数是逐列处理的，而不能够 多列数据同时处理 。由此，引出了 `apply` 函数来解决这一问题。**

#### 2.apply的使用

在传入的参数上： `apply` 的自定义函数传入参数与 `filter` 完全一致。

但是filter()过滤函数传入的自定义函数**只能返回的是布尔值或布尔值的序列。**

但是apply()方法可以返回值的选择就很多。

除了返回标量之外， `apply` 方法还可以返回一维 `Series` 和二维 `DataFrame` 。

```python
In [38]: def BMI(x):
   ....:     Height = x['Height']/100
   ....:     Weight = x['Weight']
   ....:     BMI_value = Weight/Height**2
   ....:     return BMI_value.mean()
   ....: 

In [39]: gb.apply(BMI)
Out[39]: 
Gender
Female    18.860930
Male      24.318654
dtype: float64
```

它们产生的数据框维数和多级索引的层数应当如何变化？下面举三组例子就非常容易明白结果是如何生成的：

##### （1）标量情况

结果得到的是 `Series` ，索引与 `agg` 的结果一致（列的聚合）

```python
gb = df.groupby(['Gender','Test_Number'])[['Height','Weight']]
#每组的数据都变为一个标量
gb.apply(lambda x: 0)
>>>
Gender  Test_Number
Female  1              0
        2              0
        3              0
Male    1              0
        2              0
        3              0
dtype: int64
#还有特殊的情况
gb.apply(lambda x: [0, 0]) # 虽然是列表，但是作为返回值仍然看作标量
```

##### （2）Series 情况

得到的是 `DataFrame` ，行索引与标量情况一致，列索引为 `Series` 的索引

```python
gb.apply(lambda x: pd.Series([0,0],index=['a','b']))
#这样的Series也能生成结果
>>>
                    a  b
Gender Test_Number      
Female 1            0  0
       2            0  0
       3            0  0
Male   1            0  0
       2            0  0
       3            0  0
```

##### （3）`DataFrame` 情况

得到的是 `DataFrame` ，**行索引最内层在每个组原先 `agg` 的结果索引上，再加一层返回的 `DataFrame` 行索引**（就是在最内层加上新生成的index列），同时分组结果 `DataFrame` 的**列索引和返回的 `DataFrame` 列索引一致。**

```python
gb.apply(lambda x: pd.DataFrame(np.ones((2,2)),index = ['a','b'],                       columns=pd.Index([('w','x'),('y','z')])))

>>>
                        w    y
                        x    z
Gender Test_Number            
Female 1           a  1.0  1.0
                   b  1.0  1.0
       2           a  1.0  1.0
                   b  1.0  1.0
       3           a  1.0  1.0
                   b  1.0  1.0
Male   1           a  1.0  1.0
                   b  1.0  1.0
       2           a  1.0  1.0
                   b  1.0  1.0
       3           a  1.0  1.0
                   b  1.0  1.0
```

练一练

> 请尝试在 `apply` 传入的自定义函数中，根据组的某些特征返回相同大小但列索引不同的 `DataFrame` ，会报错吗？如果只是行索引不同，会报错吗？

练一练：试了一下，应该是列索引不同不会报错，但是没有传入行索引，最内层的行索引会变为默认的索引，只有行索引也是一样。新的列索引也会变为默认的索引。

 `apply` 函数的灵活性是以牺牲一定性能为代价换得的，除非需要使用跨列处理的分组处理，**否则应当使用其他专门设计的 `groupby` 对象方法**.

同时，在使用聚合函数和变换函数时，也应当优先使用内置函数，它们经过了高度的性能优化，一般而言在速度上都会快于用自定义函数来实现

### 五、练习

练习的代码在代码文件夹