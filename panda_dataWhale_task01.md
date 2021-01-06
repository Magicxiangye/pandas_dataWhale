# Pandas打卡学习笔记（一）

## Task01:  预备知识

### 一、Python基础知识

（1）在生成一个数字序列的时候，在python中，有许多的可以可以实用的方法，像是--列表推导式的方法，来简练的生成一个只包含数字的序列

```python
L = []

 def my_func(x):
    return 2*x
 for i in range(5):
    L.append(my_func(i))
 #输出将会是 
 >>>[0, 2, 4, 6, 8]
    
[my_func(i) for i in range(5)]
#这样的列表推导式也可以实现相同的简化的输出
```

（2）在条件赋值中，比较实用的方法是带有语法糖的if选择的赋值方法

```python
#像是
value = 'cat' if 3>1 else 'dog'
#来作出一个条件的选择
```

（3） lambda匿名函数的使用，可以在上面的列表推导式中，做进一步的简化：

```python
#这样的简化亦可以得出相同的结果
[(lambda x: x*2)(i) for i in range(5)]

#在列表推导式的匿名函数的映射，也可以通过使用python自带的
#map函数来实现

list(map(lambda x: 2*x,range(5)))
>>>[0,2,4,6,8]
```

PS：当对于多个输入值的函数映射，可以通过追加迭代的对象就可以实现

（4）zip函数：使得多个可迭代的对象打包成一个元组构成的迭代对象（每个元组里的元素按照index来组合）通过 `tuple, list, dict`，可以得到相应的打包结果。

既然有了压缩函数，那么 `Python` 也提供了 `*` 操作符和 `zip` 联合使用来进行解压操作

```python
zipped = list(zip(l1,l2,l3))

zipped
>>>[('a', 'd', 'h'), ('b', 'e', 'i'), ('c', 'f', 'j')]

list(zip(*zipped)) # 三个元组分别对应原来的列表
>>>[('a', 'b', 'c'), ('d', 'e', 'f'), ('h', 'i', 'j')]
```

​      enumerate方法：返回键值配对的迭代元素的方法

###     二、Numpy基础

（1）np数组常用的是np.array方法

（2）一些特殊数组和矩阵的生成方式

```python
#等差序列的两种方法
np.linspace(1,5,11) # 起始、终止（包含）、样本个数
np.arange(1,5,2) # 起始、终止（不包含）、步长

#几种特殊的矩阵
#零矩阵
np.zeros(shape)
#单位矩阵
np.eyes(dimention)#关键字参数k=N是表示偏移主对角线多少个单位
np.full(shape,N)#N表示的是该shape的矩阵用什么数据来填充

```

（3）随机的矩阵

np.random.XX --这里的XX可以是：rand、 randn、 randint、 choice

分别表示0-1均匀分布的随机数组、标准正态的随机数组、随机整数组和随机列表抽样。

```python
np.random.rand(dim1,dim2)#这里的参数都是一个维度一个维度传入，不是shape了
np.random.randn()
#对于服从方差为 σ**2 均值为 μ 的一元正态分布可以如下生成
sigma, mu = 2.5, 3
mu + np.random.randn(3) * sigma
>>>array([3.92768073, 2.20521001, 3.14752812])

#randint 可以指定生成随机整数的最小值最大值和维度大小：
low, high, shape = 5, 15, (2,2)
np.random.randint(low,high,shape)

#choice 可以从给定的列表中，以一定概率和方式抽取结果，当不指定概率时为均匀采样，默认抽取方式为有放回抽样：
test_list = ['a','b','c']
np.random.choice(test_list,shape)
```

当返回的元素个数与原列表相同时，等价于使用 `permutation` 函数，即打散原列表：

```python
np.random.permutation(list)

#随机种子，它能够固定随机数的输出结果：
np.random.seed(0)
```

(4)np数组的操作

- 转置： `T`
- 合并操作： `r_, c_` （对于二维数组而言， `r_` 和 `c_` 分别表示上下合并和左右合并）
- 一维数组和二维数组进行合并时，应当把其视作列向量，在长度匹配的情况下只能够使用左右合并的 `c_` 操作。

```python
#举例子
np.r_[np.zeros((2,3)),np.zeros((2,3))]
>>>array([[0., 0., 0.],
          [0., 0., 0.],
          [0., 0., 0.],
          [0., 0., 0.]])
```

- .reshape():维度变换的方法，使用是可以设置按照行还是列的顺序来读取填充新的矩阵的shape

  ```python
  target = np.arange(8).reshape(2,4)
  >>>array([[0, 1, 2, 3],
           [4, 5, 6, 7]])
  # 使用不同的模式来读取并生成新的矩阵
  #C模式是按行来读取，F模式是按列来读取
  target.reshape((4,2), order='C') # 按照行读取和填充
  
  #将 n*1 大小的数组转为1维数组的操作是经常使用的方法是
  target.reshape(-1)
  ```

  - 数组的切片模式支持使用 `slice` 类型的 `start:end:step` 切片，还可以直接传入列表指定某个维度的索引进行切片
  - 同时，使用np.ix_在矩阵的对应的维度上使用布尔的索引来确定哪些需要被保留

  ```python
  target = np.arange(9).reshape(3,3)
  >>>array([[0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]])
  #使用np.ix_
  target[np.ix_([True, False, True], [True, False, True])]
  >>>array([[0, 2],
            [6, 8]])
  #限定提取的行号时
   target[np.ix_([1,2], [True, False, True])]
   >>>array([[3, 5],
             [6, 8]])
  #np数组的特性
  #当数组维度为1维时，可以直接进行布尔索引，而无需 np.ix_ （5）np的常用函数
  ```

  (5)np的常用函数

  `where` 是一种条件函数，可以指定满足条件与不满足条件位置对应的填充值

```python
a = np.array([-1,1,-1,0])
np.where(a>0, a, 5) # 对应位置为True时填充a对应元素，否则填充5
>>>array([5, 1, 5, 5])
```

- nonzero():返回的是数组中非零的数的index
- argmax():返回的是数组中最大数的index
- argmin()：返回的是数组中最小数的index
- any():当序列至少 存在一个 `True` 或非零元素时返回 `True` ，否则返回 `False`
- all():当序列元素 全为 `True` 或非零元素时返回 `True` ，否则返回 `False`
- `cumprod(), cumsum()` 分别表示累乘和累加函数，返回同长度的数组， `diff()` 表示和前一个元素做差，由于第一个元素为缺失值，因此在默认参数情况下，返回长度是原数组减1
- 统计函数也是常用的方法：包括 `max, min, mean, median, std, var, sum, quantile`
- 特殊的函数：分位数计算是全局方法，因此不能通过 `array.quantile` 的方法调用。

​     但是对于含有缺失值的数组，它们返回的结果也是缺失值，如果需要略过缺失值，必须使用 `nan*` 类型的函数，上述的几个统计函数都有对应的 `nan*` 函数。

```python
#其他的统计函数也是用的相同的改变的函数名称
target = np.array([1, 2, np.nan])
target.max()
>>>nan
np.nanmax(target)
>>>2.0
```

对于协方差和相关系数分别可以利用 `cov, corrcoef` 

```python
target1 = np.array([1,3,5,9])
target2 = np.array([1,5,3,-9])
#协方差
np.cov(target1, target2)
>>>array([[ 11.66666667, -16.66666667],
          [-16.66666667,  38.66666667]])
#相关系数
np.corrcoef(target1, target2)
>>>array([[ 1.        , -0.78470603],
          [-0.78470603,  1.        ]])
```

PS：二维 `Numpy` 数组中统计函数的 `axis` 参数，它能够进行某一个维度下的统计特征计算，当 `axis=0` 时结果为列的统计指标，当 `axis=1` 时结果为行的统计指标。

（6）np的广播机制

通俗来说就是可以使了两个不同维度的数组，在一定的条件下进行操作。

常用在二维数组之间的操作，像是在深度学习神经网络的前向传播的偏移量的加法一样，可以将符合一定条件的数组扩充维度，以满足算数条件。

（7）向量与矩阵的运算

- 向量内积： `.dot（）`

- 向量范数和矩阵范数： `np.linalg.norm`

  在矩阵范数的计算中，最重要的是 `ord` 参数，可选值如下：

  |  ord  |      norm for matrices       |      norm for vectors      |
  | :---: | :--------------------------: | :------------------------: |
  | None  |        Frobenius norm        |           2-norm           |
  | ‘fro’ |        Frobenius norm        |             –              |
  | ‘nuc’ |         nuclear norm         |             –              |
  |  inf  |   max(sum(abs(x), axis=1))   |        max(abs(x))         |
  | -inf  |   min(sum(abs(x), axis=1))   |        min(abs(x))         |
  |   0   |              –               |        sum(x != 0)         |
  |   1   |   max(sum(abs(x), axis=0))   |          as below          |
  |  -1   |   min(sum(abs(x), axis=0))   |          as below          |
  |   2   | 2-norm (largest sing. value) |          as below          |
  |  -2   |   smallest singular value    |          as below          |
  | other |              –               | sum(abs(x)**ord)**(1./ord) |

- 矩阵乘法： `@`