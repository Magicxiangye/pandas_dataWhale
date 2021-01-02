---
title: "Pandas打卡学习笔记（七）"
tag: "Pandas"
---

# Pandas打卡学习笔记（七）

## Task07 ---第七章：缺失数据

### 一、缺失值的统计和删除

#### 1.缺失信息的统计

缺失数据**可以使用 `isna` 或 `isnull` （两个函数没有区别）来查看每个单元格是否缺失**，结合 `mean` 可以计算出每列缺失值的比例

```python
df = pd.read_csv('data/learn_pandas.csv', usecols=  ['Grade', 'Name', 'Gender', 'Height','Weight', 'Transfer'])

#使用isna或者isnull来判断是否是缺失值
df.isna().head()
>>>
   Grade   Name  Gender  Height  Weight  Transfer
0  False  False   False   False   False     False
1  False  False   False   False   False     False
2  False  False   False   False   False     False
3  False  False   False    True   False     False
4  False  False   False   False   False     False

#加上mean()查看缺失的每列缺失值的比例
df.isna().mean()
>>>
Grade       0.000
Name        0.000
Gender      0.000
Height      0.085
Weight      0.055
Transfer    0.060
dtype: float64
```

如果想要**查看某一列缺失或者非缺失的行**，可以利用 `Series` 上的 **`isna` 或者 `notna` 进行布尔索引**。例如，查看身高缺失的行：

```python
df[df.Height.isna()].head()
>>>
        Grade          Name  Gender  Height  Weight Transfer
3   Sophomore  Xiaojuan Sun  Female     NaN    41.0        N
12     Senior      Peng You  Female     NaN    48.0      NaN
26     Junior     Yanli You  Female     NaN    48.0        N
36   Freshman  Xiaojuan Qin    Male     NaN    79.0        Y
60   Freshman    Yanpeng Lv    Male     NaN    65.0        N
```

如果想要**同时对几个列，检索出全部为缺失或者至少有一个缺失或者没有缺失的行，**可以使用 `isna, notna` 和 `any, all` 的组合。

例如，对身高、体重和转系情况这3列分别进行这三种情况的检索：

```python
#对三列的检索情况
sub_set = df[['Height', 'Weight', 'Transfer']]
#检索三列全部缺失的情况
df[sub_set.isna().all(1)]
#以布尔值的索引来提取数据
#至少缺失一个的情况
df[sub_set.isna().any(1)]
#没有缺失的情况
df[sub_set.isna().all(1)]
```

#### 2.缺失信息的删除

数据处理中经常需要根据缺失值的大小、比例或其他特征来**进行行样本或列特征的删除**， `pandas` 中**提供了 `dropna` 函数来进行操作。**

dropna的主要参数：

1.  axis: 轴方向，（默认为0，即删除行）
2. how:删除的方式（ `how` 主要有 `any` 和 `all` 两种参数可以选择。）
3. 删除的非缺失值个数阈值 `thresh`(就是某一行或者某一列，非缺失的值没有达到相应的最小的数量的会被删除)
4. subset:备选的删除子集(就是要做缺失值删除的一列或者多列（list）)

例如，**删除**身高体重至少有一个**缺失的行**：

```python
res = df.dropna(how = 'any', subset = ['Height', 'Weight'])
```

比如：删除超过15个缺失值的列：

```python
res = df.dropna(axis=1, thresh=df.shape[0]-15)
```

当然，不用 `dropna` 同样是可行的，例如上述的两个操作，也可以使用布尔索引来完成。

### 二、缺失值的填充和插值

#### 1.利用fillna进行填充

fillna函数的三个常用的参数

- value: 为填充值，可以是标量，也可以是索引到元素的字典的映射。
- method:为填充的方法，有用前面的元素填充 `ffill` 和用后面的元素填充 `bfill` 两种类型
- limit:表示连续缺失值的最大填充次数。(连续出现的缺失，最多填充几次。)

构造一个简单的 `Series` 来说明用法：

```python
s = pd.Series([np.nan, 1, np.nan, np.nan, 2, np.nan],index=list('aaabcd'))
print(s)
>>>
a    NaN
a    1.0
a    NaN
b    NaN
c    2.0
d    NaN
dtype: float64

s.fillna(method='ffill')#前面的填充后面
>>>
a    NaN
a    1.0
a    1.0
b    1.0
c    2.0
d    2.0
dtype: float64
    
s.fillna(method='ffill', limit=1) # 连续出现的缺失，最多填充一次
a    NaN
a    1.0
a    1.0
b    NaN
c    2.0
d    2.0
dtype: float64

s.fillna(s.mean()) # value为标量
#传入的值是标量
>>>
a    1.5
a    1.0
a    1.5
b    1.5
c    2.0
d    1.5
dtype: float64

s.fillna({'a': 100, 'd': 200}) # 通过索引映射填充的值
#对应的索引变为对应的值
>>>
a    100.0
a      1.0
a    100.0
b      NaN
c      2.0
d    200.0
dtype: float64
```

有时为了更加合理地填充，**需要先进行分组后再操作**。例如，根据年级进行身高的均值填充：

```python
df.groupby('Grade')['Height'].transform(lambda x:x.fillna(x.mean())).head()
```

练一练

> 对一个序列以如下规则填充缺失值：如果单独出现的缺失值，就用前后均值填充，如果连续出现的缺失值就不填充，即序列[1, NaN, 3, NaN, NaN]填充后为[1, 2, 3, NaN, NaN]，请利用 `fillna` 函数实现。（提示：利用 `limit` 参数）

```python
s = pd.Series([1, np.nan, 3,np.nan, np.nan])
#应该结合自定义函数的使用
```

#### 2.插值函数

 `interpolate` 函数

只讨论比较常用且简单的三类情况，即**线性插值、最近邻插值和索引插值。**

对于 `interpolate` 而言，除了插值方法（默认为 `linear` 线性插值）之外，

线性插值：

 线性插值是针对一维数据的插值方法。它根据一维数据序列中需要插值的点的左右临近两个数据来进行数值估计。当然了它不是求这两个点数据大小的

平均值（在中心点的时候就等于平均值）。**而是根据到这两个点的距离来分配比重的。**

有与 **`fillna` 类似的两个常用参数**，一个是**控制方向的 `limit_direction`** ，另一个是**控制最大连续缺失值插值个数的 `limit`** 。其中，**限制插值的方向默认为 `forward`** ，这与 `fillna` 的 `method` 中的 `ffill` 是类似的，若**想要后向限制插值或者双向限制插值可以指定为 `backward` 或 `both`** 。

```python
s = pd.Series([np.nan, np.nan, 1,np.nan, np.nan, np.nan,2, np.nan, np.nan])

s.values
>>>
 array([nan, nan,  1., nan, nan, nan,  2., nan, nan])
#在默认线性插值法下分别进行 backward 和双向限制插值，同时限制最大连续条数为1：
res = s.interpolate(limit_direction='backward', limit=1)
res.values
>>>array([ nan, 1.  , 1.  ,  nan,  nan, 1.75, 2.  ,  nan,  nan])
#当为双向的填充的时候
res = s.interpolate(limit_direction='both', limit=1)
>>>
array([ nan, 1.  , 1.  , 1.25,  nan, 1.75, 2.  , 2.  ,  nan])
```

第二种常见的插值是**最近邻插补**，即**缺失值的元素和离它最近的非缺失值元素一样：**

```python
s.interpolate('nearest').values
array([nan, nan,  1.,  1.,  1.,  2.,  2., nan, nan])
```

最后来介绍索引插值，即根据索引大小进行线性插值。例如，构造不等间距的索引进行演示：

```python
s = pd.Series([0,np.nan,10],index=[0,1,10])
0      0.0
1      NaN
10    10.0
dtype: float64

s.interpolate() # 默认的线性插值，等价于计算中点的值
>>>
0      0.0
1      5.0
10    10.0
dtype: float64

s.interpolate(method='index') # 和索引有关的线性插值，计算相应索引大小对应的值
>>>
#对应的索引大小的值
0      0.0
1      1.0
10    10.0
dtype: float64
#同时，这种方法对于时间戳索引也是可以使用的，有关时间序列的其他话题会在第十章进行讨论
s = pd.Series([0,np.nan,10],index=pd.to_datetime(['20200101','20200102','20200111']))

s
>>>
2020-01-01     0.0
2020-01-02     NaN
2020-01-11    10.0
dtype: float64

s.interpolate()
>>>
2020-01-01     0.0
2020-01-02     5.0
2020-01-11    10.0
dtype: float64

s.interpolate(method='index')
>>>
2020-01-01     0.0
2020-01-02     1.0
2020-01-11    10.0
dtype: float64
```

关于polynomial和spline插值的注意事项

> 在 `interpolate` 中如果选用 `polynomial` 的插值方法，它内部调用的是 `scipy.interpolate.interp1d(*,*,kind=order)` ，这个函数内部调用的是 `make_interp_spline` 方法，因此其实是样条插值而不是类似于 `numpy` 中的 `polyfit` 多项式拟合插值；而当选用 `spline` 方法时， `pandas` 调用的是 `scipy.interpolate.UnivariateSpline` 而不是普通的样条插值。这一部分的文档描述比较混乱，而且这种参数的设计也是不合理的，当使用这两类插值方法时，用户一定要小心谨慎地根据自己的实际需求选取恰当的插值方法。

### 三、Nullable类型

#### 1.缺失记号及其缺陷

在 `python` 中的缺失值用 `None` 表示，**该元素除了等于自己本身之外，与其他任何元素不相等：**

```python
None == None
True
None == False
False
None == []
False
None == ''
False
```

**在 `numpy` 中利用 `np.nan` 来表示缺失值**，该元素除了不和其他任何元素相等之外，**和自身的比较结果也返回 `False`** ：

```python
np.nan == np.nan
>>>False
np.nan == None
>>>False
np.nan == False
>>>False
```

虽然在对缺失序列或表格的元素进行比较操作的时候， `np.nan` 的对应位置会返回 `False` ，但是**在使用 `equals` 函数进行两张表或两个序列的相同性检验时，会自动跳过两侧表都是缺失值的位置，直接返回 `True` ：**

```python
s1 = pd.Series([1, np.nan])
s2 = pd.Series([1, 2])
s3 = pd.Series([1, np.nan])

s1 == 1
>>>
0     True
1    False
dtype: bool

s1.equals(s2)
>>>False

s1.equals(s3)
>>>True
```

在**时间序列的对象中**， **`pandas` 利用 `pd.NaT` 来指代缺失值，它的作用和 `np.nan` 是一致的**（时间序列的对象和构造将在第十章讨论）

知识点：

那么为什么要引入 `pd.NaT` 来表示时间对象中的缺失呢？仍然以 `np.nan` 的形式存放会有什么问题？在 `pandas` 中可以看到 `object` 类型的对象，而 **`object` 是一种混杂对象类型**，**如果出现了多个类型的元素同时存储在 `Series` 中，它的类型就会变成 `object`** 。例如，同时存放整数和字符串的列表：

```python
pd.Series([1, 'two'])
>>>
0      1
1    two
dtype: object

type(np.nan)
float
```

`NaT` 问题的根源来自于 `np.nan` 的本身是一种浮点类型，**而如果浮点和时间类型混合存储，如果不设计新的内置缺失类型来处理，就会变成含糊不清的 `object` 类型**，这显然是不希望看到的。

同时，由于 `np.nan` 的浮点性质，如果在一个整数的 `Series` 中出现缺失，那么其类型会转变为 `float64` ；而如果在一个布尔类型的序列中出现缺失，那么其类型就会转为 `object` 而不是 `bool` ：

```python
pd.Series([1, np.nan]).dtype
dtype('float64')
pd.Series([True, False, np.nan]).dtype
dtype('O')
```

**大佬知识点：**因此，在进入 `1.0.0` 版本后， `pandas` 尝试设计了一种新的缺失类型 `pd.NA` 以及三种 `Nullable` 序列类型来应对这些缺陷，它们分别是 `Int, boolean` 和 `string` 。

#### 2.Nullable类型的性质

从字面意义上看 `Nullable` 就是可空的，言下之意就是序列类型不受缺失值的影响。例如，在上述**三个 `Nullable` 类型中存储缺失值，都会转为 `pandas` 内置的 `pd.NA`** ：

```python
pd.Series([np.nan, 1], dtype = 'Int64') # "i"是大写的

0    <NA>
1       1
dtype: Int64

pd.Series([np.nan, True], dtype = 'boolean')

0    <NA>
1    True
dtype: boolean

pd.Series([np.nan, 'my_str'], dtype = 'string')

0      <NA>
1    my_str
dtype: string
```

在 `Int` 的序列中，返回的结果会尽可能地成为 `Nullable` 的类型：

```python
pd.Series([np.nan, 0], dtype = 'Int64') + 1

0    <NA>
1       1
dtype: Int64

pd.Series([np.nan, 0], dtype = 'Int64') == 0

0    <NA>
1    True
dtype: boolean

pd.Series([np.nan, 0], dtype = 'Int64') * 0.5 # 只能是浮点

0    <NA>
1     0.0
dtype: Float64
```

对于 `boolean` 类型的序列而言，其和 `bool` 序列的行为主要有两点区别：

第一点是**带有缺失的布尔列表无法进行索引器中的选择**，而 **`boolean` 会把缺失值看作 `False` ：**

```python
s = pd.Series(['a', 'b'])

#boolean类型的序列
s_bool = pd.Series([True, np.nan])
#boolean序列
s_boolean = pd.Series([True, np.nan]).astype('boolean')

# s[s_bool] # 报错
In [69]: s[s_boolean]
Out[69]: 
0    a
dtype: object
```

第二点是在进行逻辑运算时， `bool` 类型在缺失处返回的永远是 `False` ，而 `boolean` 会根据逻辑运算是否能确定唯一结果来返回相应的值。那什么叫能否确定唯一结果呢？举个简单例子： `True | pd.NA` 中无论缺失值为什么值，必然返回 `True` ； `False | pd.NA` 中的结果会根据缺失值取值的不同而变化，此时返回 `pd.NA` ； `False & pd.NA` 中无论缺失值为什么值，必然返回 `False` 。

**即在进行逻辑的运算的时候，有的运算会因为缺失值的不确定，而产生不了明确的bool值**

关于 `string` 类型的具体性质将在下一章文本数据中进行讨论。

一般在实际数据处理时，**可以在数据集读入后，先通过 `convert_dtypes` 转为 `Nullable` 类型**：

```python
df = pd.read_csv('data/learn_pandas.csv')

df = df.convert_dtypes()

df.dtypes
>>>
School          string
Grade           string
Name            string
Gender          string
Height         Float64
Weight           Int64
Transfer        string
Test_Number      Int64
Test_Date       string
Time_Record     string
dtype: object
```

#### 3.缺失数据的计算和分组

当调用函数 `sum, prob` 使用**加法和乘法**的时候，缺失数据等价于被**分别视作0和1**，即不改变原来的计算结果：

当使用累计函数时，会自动跳过缺失值所处的位置：

```python
s.cumsum()
>>>
0     2.0
1     5.0
2     NaN
3     9.0
4    14.0
dtype: float64
```

当进行单个标量运算的时候，除了 `np.nan ** 0` =1和 `1 ** np.nan` =1这两种情况为确定的值之外，所有运算结果全为缺失（ **`pd.NA` 的行为与此一致 ），并且 `np.nan` 在比较操作时一定返回 `False` ，而 `pd.NA` 返回 `pd.NA`** ：

```python
In [80]: np.nan == 0
Out[80]: False

In [81]: pd.NA == 0
Out[81]: <NA>

In [82]: np.nan > 0
Out[82]: False

In [83]: pd.NA > 0
Out[83]: <NA>

In [84]: np.nan + 1
Out[84]: nan

In [85]: np.log(np.nan)
Out[85]: nan

In [86]: np.add(np.nan, 1)
Out[86]: nan

In [87]: np.nan ** 0
Out[87]: 1.0

In [88]: pd.NA ** 0
Out[88]: 1

In [89]: 1 ** np.nan
Out[89]: 1.0

In [90]: 1 ** pd.NA
Out[90]: 1
```

另外需要注意的是， `diff, pct_change` 这两个函数虽然功能相似，但是**对于缺失的处理不同**，**前者凡是参与缺失计算的部分全部设为了缺失值，而后者缺失值位置会被设为 0% 的变化率**：

```python
s.diff()
>>>
0    NaN
1    1.0
2    NaN
3    NaN
4    1.0
dtype: float64

s.pct_change()
>>>
0         NaN
1    0.500000
2    0.000000
3    0.333333
4    0.250000
dtype: float64
```

对于一些函数而言，缺失可以作为一个类别处理，例如在 `groupby, get_dummies(独热编码)` 中可以设置相应的参数来进行增加缺失类别。

### 四、练习

在练习代码的文件夹