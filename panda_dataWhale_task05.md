---
title: "Pandas打卡学习笔记（五）"
tag: "Pandas"
---

# Pandas打卡学习笔记（五）

## Task05 ---第五章：变形

### 一、长宽表的变形

长表和宽表的区别是：对于某一个特征而言的。

像是在一个表中**把性别存储在一个列中**（当作数据存储在了列中）那么他**就是关于性别的长表。**

但如果**把性别作为列名**，这个列的元素是某一个其他的相关特征数值，那这个表**就是关于性别的宽表**。

 像是下边的代码的例子

```python
import pandas as pd
#把相关的存在列中（这是一个长表）
pd.DataFrame({'Gender': ['F', 'F', 'M', 'M'], 'Height': [163, 160, 175, 180]})
>>>
  Gender  Height
0      F     163
1      F     160
2      M     175
3      M     180

#把性别当作列名（这是成为了一个宽表）
pd.DataFrame({'Height: F': [163,160],'Height:M': [175, 180]})
>>>
   Height: F  Height: M
0        163        175
1        160        180
```

从信息上看，这两张表格时完全等价的，（因为都包含了相同的身高的统计数据），但只是呈现的方式不一样。

其呈现方式主要又与**性别一列选择的布局模式有关**，即到底是以 long 的状态存储还是以 wide 的状态存储。因此， `pandas` 针对此类长宽表的变形操作设计了一些有关的变形函数。

#### 1. pivot

`pivot` 是一种典型的长表变宽表的函数

例子：下表存储了张三和李四的语文和数学分数，现在想要把语文和数学分数作为列来展示。

先来构建基础的DataFrame表

```python
df = pd.DataFrame({'Class':[1,1,2,2],'Name':['San Zhang','San Zhang','Si Li','Si Li'],'Subject':['Chinese','Math','Chinese','Math'],'Grade'[80,75,90,85]})
#构建的DataFrame
>>>
   Class       Name  Subject  Grade
0      1  San Zhang  Chinese     80
1      1  San Zhang     Math     75
2      2      Si Li  Chinese     90
3      2      Si Li     Math     85
```

对于一个基本的长变宽的操作，有三个很重要的基本要素，也时pivot()函数的三个参数。

- index参数：变形后的行索引
- columns参数：需要转到列索引的列
- values参数:  这些列和行索引对应的数值

在新生成的表中，

新表的列的索引，**需要转到列索引的列的unique()的值**

新表的行的索引，**是index对应的列的unique()值**

而 `values` 对应了想要展示的数值列

代码的实例

```python
df.pivot(index='Name', columns='Subject', values='Grade')
>>>
#新表的生成
Subject    Chinese  Math
Name                    
San Zhang       80    75
Si Li           90    85
```

利用 `pivot` 进行变形操作需要**满足唯一性的要求**，即由于在新表中的行列索引对应了唯一的 `value` ，因此原表中的 **`index` 和 `columns` 对应两个列的行组合必须唯一。**

比如：现在把原表中第二行张三的数学改为语文就会报错，这是由于 `Name` 与 `Subject` 的组合中两次出现 `("San Zhang", "Chinese")` ，从而最后不能够确定到底变形后应该是填写80分还是75分。

但是新的特性：`pandas` 从 `1.1.0` 开始， `pivot` 相关的**三个参数允许被设置为列表，这也意味着会返回多级索引。**

这里构造一个相应的例子来说明如何使用：下表中六列分别为班级、姓名、测试类型（期中考试和期末考试）、科目、成绩、排名。

```python
df = pd.DataFrame({'Class':[1, 1, 2, 2, 1, 1, 2, 2],
'Name':['San Zhang', 'San Zhang', 'Si Li', 'Si Li',
'San Zhang', 'San Zhang', 'Si Li', 'Si Li'],'Examination': ['Mid', 'Final', 'Mid', 'Final','Mid', 'Final', 'Mid', 'Final'],'Subject':['Chinese', 'Chinese', 'Chinese', 'Chinese',
'Math', 'Math', 'Math', 'Math'],'Grade':[80, 75, 85, 65, 90, 85, 92, 88],'rank':[10, 15, 21, 15, 20, 7, 6, 2]})
df
>>>
   Class       Name Examination  Subject  Grade  rank
0      1  San Zhang         Mid  Chinese     80    10
1      1  San Zhang       Final  Chinese     75    15
2      2      Si Li         Mid  Chinese     85    21
3      2      Si Li       Final  Chinese     65    15
4      1  San Zhang         Mid     Math     90    20
5      1  San Zhang       Final     Math     85     7
6      2      Si Li         Mid     Math     92     6
7      2      Si Li       Final     Math     88     2
```

现在想要把测试类型和科目联合组成的四个类别（期中语文、期末语文、期中数学、期末数学）转到列索引，并且同时统计成绩和排名：

```python
pivot_multi = df.pivot(index = ['Class', 'Name'],
columns = ['Subject','Examination'],values =['Grade','rank'])
>>>
#生成的表格为
                  Grade                     rank         
Subject         Chinese       Math       Chinese       Math      
Examination         Mid Final  Mid Final     Mid Final  Mid Final
Class Name                                            
1     San Zhang      80    75   90    85      10    15   20     7
2     Si Li          85    65   92    88      21    15    6     2
```

根据唯一性原则

新表的行索引等价于对 `index` 中的多列使用 `drop_duplicates` 

而列索引的长度为 `values` 中的元素个数乘以 `columns` 的唯一组合数量（与 `index` 类似）

```python
pivot_multi = df.pivot(index = ['Class', 'Name'],
 columns = ['Subject','Examination'],values = ['Grade','rank'])

>>>
                  Grade                     rank                 
Subject         Chinese       Math       Chinese       Math      
Examination         Mid Final  Mid Final     Mid Final  Mid Final
Class Name                                                       
1     San Zhang      80    75   90    85      10    15   20     7
2     Si Li          85    65   92    88      21    15    6     2
```

![图像化理解](https://gitee.com/magicye/blogimage/raw/master/img/ch5_mulpivot.png)

#### 2. pivot_table

`pivot` 的使用**依赖于唯一性条件**

那如果不满足唯一性条件，那么必须通过聚合操作使得相同行列组合对应的多个值变为一个值(通过聚合函数来实现)。

当不满足唯一性条件的情况的时候，**像是要的是语文或数学成绩是两次考试成绩的平均值**，这不满足唯一性的条件，不能使用pivot函数

```python
 df = pd.DataFrame({'Name':['San Zhang', 'San Zhang','San Zhang', 'San Zhang','Si Li', 'Si Li', 'Si Li', 'Si Li'],'Subject':['Chinese', 'Chinese', 'Math', 'Math','Chinese', 'Chinese', 'Math', 'Math'],'Grade':[80, 90, 100, 90, 70, 80, 85, 95]})
    
>>>
#设置一个成绩的DataFrame
        Name  Subject  Grade
0  San Zhang  Chinese     80
1  San Zhang  Chinese     90
2  San Zhang     Math    100
3  San Zhang     Math     90
4      Si Li  Chinese     70
5      Si Li  Chinese     80
6      Si Li     Math     85
7      Si Li     Math     95
```

这样就可以使用的是pivot_table()函数来实现，

函数中的参数aggfunc:传入的是使用的聚合函数的名称

```python
#则上面的DataFrame的解决方法就是使用pivot_table方法来实现
df.pivot_table(index= 'Name', columns='Subject', values= 'Grade',aggfunc='mean' )
>>>
Subject    Chinese  Math
Name                    
San Zhang       85    95
Si Li           75    90
```

这里函数的aggfunc参数传入的是**上一章中介绍的所有合法聚合字符串**只要是合法的聚合函数的方法名，都可以传入使用。

此外可以传入**以序列为输入标量为输出**的聚合函数来实现自定义操作（自定义的函数也是可以的）

```python
#aggfunc传入自定义的函数
df.pivot_table(index='Name', columns='Subject', values='Grade',aggfunc=lambda x: x.mean())
#传入的是序列，输出的是标量
>>>
#这样自定义函数的输出会和自带的内置的聚合函数的结果，一模一样
Subject    Chinese  Math
Name                    
San Zhang       85    95
Si Li           75    90
```

新特性：pivot_table具有**边际的汇总功能**

margin=True来实现，(其中，边际的聚合方式与aggfunc传入的聚合方式的方法是一样的)

例子：下面就分别统计了语文均分和数学均分、张三均分和李四均分，以及总体所有分数的均分：

```python
df.pivot_table(indecx='Name', cloumns='Subject', values='Grade',aggfunc='mean',margin=True)
>>>
#边际的聚合函数
#将会使得统计总体的平均值
Subject    Chinese  Math    All
Name                           
San Zhang       85  95.0  90.00
Si Li           75  90.0  82.50
All             80  92.5  86.25
```

练一练

> 在上面的边际汇总例子中，行或列的汇总为新表中行元素或者列元素的平均值，而总体的汇总为新表中四个元素的平均值。这种关系一定成立吗？若不成立，请给出一个例子来说明。

```python
#题目有点看不懂
```

#### 3.melt

**长宽表只是数据呈现方式的差异**，但其包含的信息量是等价的，前面提到了利用 `pivot` 把长表转为宽表

melt()函数就是**把宽表转换为长表**的逆操作。

在下面的例子中， `Subject` 以列索引的形式存储，现在**想要将其压缩到一个列中。**

```python
#先构建一个DataFrame,来创造实例
df = pd.DataFrame({'Class':[2,2],'Name':['San Zhang', 'Si Li'],'Chinese': [80,90],'Math':[80,75]})
#产生的表格为
>>>
   Class       Name  Chinese  Math
0      1  San Zhang       80    80
1      2      Si Li       90    75
#转化的方式
 df_melted = df.melt(id_vars =['Class','Name'],value_vars = ['Chinese', 'Math'],var_name = 'Subject',value_name = 'Grade')
 >>>
#结果
   Class       Name  Subject  Grade
0      1  San Zhang  Chinese     80
1      2      Si Li  Chinese     90
2      1  San Zhang     Math     80
3      2      Si Li     Math     75
```

`melt` 的主要参数和压缩的过程如下图所示：

![melt方法l](https://gitee.com/magicye/blogimage/raw/master/img/melt.png)

id_vars:可以看作是pivot的index参数的变换回原来的状态。

value_vars:可以看作是转到列索引的列的还原

var_name:还原列的原来的列的名称

value_name:传入的数值的列的原来的名字

前面提到了 `melt` 和 `pivot` 是一组互逆过程，那么就一定可以通过 `pivot` 操作把 `df_melted` 转回 `df` 的形式：

```python
#把长表再变换为宽表
df_umelted = df_melted.pivot(index=['Class','Name' ], columns='Subject', values='Grade')
>>>
#这样又转换为了宽表
Subject          Chinese  Math
Class Name                    
1     San Zhang       80    80
2     Si Li           90    75

#把索引还原，就是等价于原来的宽表df
#reset_index还原为默认的index
df_umelted = df.umelted.reset_index().rename_axis(columns={'Subject':''})
#rename_axis把列名的名字换掉
#用equals()来比较
df_umelted.equals(df)#输出True
```

#### 4.wide_to_long

`melt` 方法中，在列索引中被压缩的一组值对应的列元素只能代表同一层次的含义.

当有交叉的类别的时候，会无法的使用。

像是如果列中包含了交叉类别，比如期中期末的类别和语文数学的类别，那么想要把 `values_name` **对应的 `Grade` 扩充为两列分别对应语文分数和数学分数，只把期中期末的信息压缩**，这种需求下就要使用 `wide_to_long` 函数来完成。

以书上的代码为例

```python
df = pd.DataFrame({'Class':[1,2],'Name':['San Zhang', 'Si Li'],'Chinese_Mid':[80, 75], 'Math_Mid':[90, 85],
'Chinese_Final':[80, 75], 'Math_Final':[90, 85]})
>>>
#生成的DataFrame
   Class       Name  Chinese_Mid  Math_Mid  Chinese_Final  Math_Final
0      1  San Zhang           80        90             80          90
1      2      Si Li           75        85             75          85

#只有使用wide_to_long的方法
pd.wide_to_long(df,stubname=['Chinese','Math'],i=['Class', 'Name'],j='Examination',sep='_',suffix='.+')
>>>
                             Chinese  Math
Class Name      Examination               
1     San Zhang Mid               80    90
                Final             80    90
2     Si Li     Mid               75    85
                Final             75    85
```

具体的变换过程由下图进行展示，**属相同概念的元素使用了一致的颜色标出**：

![wide_to_long](https://gitee.com/magicye/blogimage/raw/master/img/ch5_wtl.png)

由图可以得出的理解是

- stubnames:x相当于是melt(宽表变长表的value_name变成列的列名)
- i：参数的输入为要保持不变的id变量，相当于pivot的可以看作是把pivot的index参数的变换回原来的状态。
- j:要压缩到每一行的变量的列名
- sep:分隔符（要切分压缩的原列名的分隔符是什么）
- suffix:正则的后缀

书上给出一个比较复杂的案例，把之前在 `pivot` 一节中多列操作的结果（产生了多级索引），利用 `wide_to_long` 函数，将其转为原来的形态。其中，**使用了第八章的 `str.split` 函数，目前暂时只需将其理解为对序列按照某个分隔符进行拆分即可。**

下面是代码

```python
#先copy()一份
res = pivot_multi.copy()
#把列索引的名字换成相应的格式
res.columns = res.columns.map(lambda x: '_'.join(x))
#恢复默认的行索引
res = res.reset_index()
#使用的是相应的方法
res = pd.wide_to_long(res, stubnames=['Grade', 'rank'],i=['Class','Name'],j='Subject_Examination',sep='_',suffix='.+')
res = res.reset_index()
 res[['Subject', 'Examination']] = res['Subject_Examination'].str.split('_', expand=True)
#最后按照Subject字段排序
res = res[['Class', 'Name', 'Examination','Subject', 'Grade', 'rank']].sort_values('Subject')
#再次变为默认的索引
res = res.reset_index(drop=True)
>>>
#输出为
   Class       Name Examination  Subject  Grade  rank
0      1  San Zhang         Mid  Chinese     80    10
1      1  San Zhang       Final  Chinese     75    15
2      2      Si Li         Mid  Chinese     85    21
3      2      Si Li       Final  Chinese     65    15
4      1  San Zhang         Mid     Math     90    20
5      1  San Zhang       Final     Math     85     7
6      2      Si Li         Mid     Math     92     6
7      2      Si Li       Final     Math     88     2
```

### 二、索引的变形

#### 1.stack与unstack

之前提到的索引层之间的交换

swaplevel():两层之间的交换；reorder_levels:多层之间的交换，这都是列索引的内部的交换。

下面的讨论时行列索引之间的交换，这将将会使DataFrame的维度之间发生变换，索引使属于变形的操作。

和前面提到的长宽表的变形：不同的是长宽表的变形**它们都属于某一列或几列 元素 和 列索引 之间的转换，而不是索引之间的转换。**

unstack:函数的作用是**把行索引转为列索引**，例如下面这个简单的例子：

```python
import numpy as np
df = pf.DataFrame(np.ones((4,2)), index =pd.Index([('A', 'cat', 'big'),('A', 'dog', 'small'),('B', 'cat', 'big'),('B', 'dog', 'small')]), columns=['col_1','col_2'])
>>>
#这样将先生成一个初始的DataFrame
             col_1  col_2
A cat big      1.0    1.0
  dog small    1.0    1.0
B cat big      1.0    1.0
  dog small    1.0    1.0
#使用unstack()行列索引的变换
#先使用默认的转换函数
df.unstack()
>>>
      col_1       col_2      
        big small   big small
A cat   1.0   NaN   1.0   NaN
  dog   NaN   1.0   NaN   1.0
B cat   1.0   NaN   1.0   NaN
  dog   NaN   1.0   NaN   1.0
#行列的维度变换后，无元素的地方使用NaN先进行填充
```

`unstack` 的主要参数是**移动的层号**，**默认转化最内层**，移**动到列索引的最内层，同时支持同时转化多个层**：

具体的实例代码

```python
#传入移动的单个层号
df.unstack(2)
>>>
#和默认转换最内层的情况一样
      col_1       col_2      
        big small   big small
A cat   1.0   NaN   1.0   NaN
  dog   NaN   1.0   NaN   1.0
B cat   1.0   NaN   1.0   NaN
  dog   NaN   1.0   NaN   1.0
#转换多层的情况（传入的是层的list）
df.unstack([0,2])
>>>
    col_1                  col_2                 
        A          B           A          B      
      big small  big small   big small  big small
cat   1.0   NaN  1.0   NaN   1.0   NaN  1.0   NaN
dog   NaN   1.0  NaN   1.0   NaN   1.0  NaN   1.0
#两层的行索引都变为列的索引，且都是转化在最内层
```

类似于 `pivot` 中的**唯一性要求**，在 `unstack` 中必须保证 被转为列索引的行索引层 和 被保留的行索引层 **构成的组合是唯一的**，例如把前两个列索引改成相同的**破坏唯一性，那么就会报错**：

```python
my_index = df.index.to_list()
#把索引的组合前两个换成是一样的
my_index[1] = my_index[0]
df.index = pd,Index(my_index)
#这样行索引的组合中，前两个的组合是完全一样的
df
>>>
             col_1  col_2
A cat big      1.0    1.0
      big      1.0    1.0
B cat big      1.0    1.0
  dog small    1.0    1.0
#这样破坏唯一性的行索引的组合，使用unstack()时会报错的
try:
    df.unstack()
    except Exception as e:
    Err_Msg = e
>>>
ValueError('Index contains duplicate entries, cannot reshape')
```

相反的，stack()函数：作用与unstack()相反，是将列索引相应的层再压入行索引中。

用法相似，主要的参数还是移动的层号。

```python
#先生成一个操作的DataFrame（用之前生成的转置一下，成为想要的数据）
df_2 = pd.DataFrame(np.ones((4, 2)),index = pd.Index([('A', 'cat', 'big'),('A', 'dog','small'),('B', 'cat', 'big'),('B', 'dog', 'small')]),columns = ['index_1', 'index_2']).T
>>>df_2
          A          B      
         cat   dog  cat   dog
         big small  big small
index_1  1.0   1.0  1.0   1.0
index_2  1.0   1.0  1.0   1.0
#先用的时默认的方法（默认转化的是最内层的）
#空缺的地方还是补NaN
df_2.stack()
>>>
                 A         B     
               cat  dog  cat  dog
index_1 big    1.0  NaN  1.0  NaN
        small  NaN  1.0  NaN  1.0
index_2 big    1.0  NaN  1.0  NaN
        small  NaN  1.0  NaN  1.0
#多层的转换
df_2.stack([1,2])
>>>
                     A    B
index_1 cat big    1.0  1.0
        dog small  1.0  1.0
index_2 cat big    1.0  1.0
        dog small  1.0  1.0
```

#### 2.聚合与变形的关系

在上面介绍的所有函数中，**除了带有聚合效果的 `pivot_table`** 以外，**所有的函数在变形前后并不会带来 `values` 个数的改变，**只是这些值**在呈现的形式上发生了变化。**

上一章讨论的**分组聚合操作**，由于生成了新的行列索引，因此必然也**属于某种特殊的变形操作**，但由于聚合之后把原来的多个值变为了一个值，**因此 `values` 的个数产生了变化**，这也是分组聚合与变形函数的最大区别。

### 三、其他变形函数

#### 1.crosstab

因为它能实现的所有功能 `pivot_table` 都能完成，并且速度更快。

**在默认状态下， `crosstab` 可以统计元素组合出现的频数，即 `count` 操作。**

例如统计 `learn_pandas` 数据集中学校和转系情况对应的频数：

```python
df = pd.read_csv('data/learn_pandas.csv')
pd.crosstab(index= df.school, columns= df.Transfer)
>>>
Transfer                        N  Y
School                              
Fudan University               38  1
Peking University              28  2
Shanghai Jiao Tong University  53  0
Tsinghua University            62  4
#还有crosstab的等价的写法
 pd.crosstab(index = df.School, columns = df.Transfer, values = [0]*df.shape[0], aggfunc = 'count')
>>>
Transfer                          N    Y
School                                  
Fudan University               38.0  1.0
Peking University              28.0  2.0
Shanghai Jiao Tong University  53.0  NaN
Tsinghua University            62.0  4.0
```

同样，可以利用 `pivot_table` 进行等价操作，由于这里统计的是**组合的频数**，因此 `values` 参数无论**传入哪一个列都不会影响最后的结果：**

```python
df.pivot_table(index='School',columns='Transfer',values='Name',aggfunc='count')
>>>
#相同的结果
Transfer                          N    Y
School                                  
Fudan University               38.0  1.0
Peking University              28.0  2.0
Shanghai Jiao Tong University  53.0  NaN
Tsinghua University            62.0  4.0
```

所以：主要的区别在于

`crosstab` 的对应位置**传入的是具体的序列**

 `pivot_table` 传入的是**被调用表对应的名字**，若传入序列对应的值则会报错。

除了默认状态下的 `count` 统计，crosstab()函数的**所有的聚合字符串和返回标量的自定义函数**都是可用的，例如统计对应组合的身高均值：

```python
#参数传入的都是具体的序列
pd.crosstab(index= df.School,columns=df.Transfer,values =df.Height,aggfunc='mean')
#输出的是
>>>
Transfer                                N       Y
School                                           
Fudan University               162.043750  177.20
Peking University              163.429630  162.40
Shanghai Jiao Tong University  163.953846     NaN
Tsinghua University            163.253571  164.55
```

练一练

> 前面提到了 `crosstab` 的性能劣于 `pivot_table` ，请选用多个聚合方法进行验证。

```python

```

#### 2.explode

`explode` 参数能够对某一列的元素进行纵向的展开，被展开的单元格式必须存储为 `list, tuple, Series, np.ndarray` 中的一种类型。

来看例子

```python
df_ex = pd.DataFrame({'A': [[1, 2],'my_str',{1, 2},pd.Series([3, 4])],'B': 1})

#将A列展开
df_ex.explode('A')
#输出
>>>
        A  B
0       1  1
0       2  1
1  my_str  1
2  {1, 2}  1
3       3  1
3       4  1
```

#### 3.get_dummies

`get_dummies` 是用于特征构建的重要函数之一，**其作用是把类别特征转为指示变量**。例如，**对年级一列转为指示变量，属于某一个年级的对应列标记为1，否则为0：**

```python
pd.get_dummies(df.Grade).head()
>>>
#输出
   Freshman  Junior  Senior  Sophomore
0         1       0       0          0
1         1       0       0          0
2         0       0       1          0
3         0       0       0          1
4         0       0       0          1

```

### 四、练习

练习在代码的文件夹