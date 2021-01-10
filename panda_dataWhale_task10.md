---
title: "Pandas打卡学习笔记（十）"
tag: "Pandas"
date: 2021-01-8
---

# Pandas打卡学习笔记（十）

## Task10---第十章 ：时序数据

### 一、时序中的基本对象

时间序列的概念在日常生活中十分常见，但对于一个具体的时序事件而言，可以从多个时间对象的角度来描述。例如2020年9月7日周一早上8点整需要到教室上课，这个课会在当天早上10点结束，其中包含了哪些时间概念？

- 第一，**会出现时间戳（Date times）的概念**，即’2020-9-7 08:00:00’和’2020-9-7 10:00:00’这两个时间点分别代表了上课和下课的时刻，**在 `pandas` 中称为 `Timestamp`** 。同时，**一系列的时间戳可以组成 `DatetimeIndex` ，而将它放到 `Series` 中后， `Series` 的类型就变为了 `datetime64[ns]`** ，如果有涉及时区则为 `datetime64[ns, tz]` ，其中tz是time zone的简写。
- 第二，会出现**时间差（Time deltas）的概念**，即上课需要的时间，两个 `Timestamp` 做差就得到了时间差，pandas中利用 `Timedelta` 来表示。类似的，**一系列的时间差就组成了 `TimedeltaIndex` ， 而将它放到 `Series` 中后， `Series` 的类型就变为了 `timedelta64[ns]` 。**
- 第三，会**出现时间段（Time spans）的概念**，即在8点到10点这个区间都会持续地在上课，在 `pandas` 利用 `Period` 来表示。类似的，**一系列的时间段就组成了 `PeriodIndex` ， 而将它放到 `Series` 中后， `Series` 的类型就变为了 `Period` 。**
- 第四，**会出现日期偏置（Date offsets）的概念**，假设你只知道9月的第一个周一早上8点要去上课，但不知道具体的日期，那么就需要一个类型来处理此类需求。再例如，想要知道2020年9月7日后的第30个工作日是哪一天，那么时间差就解决不了你的问题，从而 `pandas` 中的 `DateOffset` 就出现了。**同时， `pandas` 中没有为一列时间偏置专门设计存储类型**，理由也很简单，因为需求比较奇怪，一般来说我们只需要对一批时间特征做一个统一的特殊日期偏置。

通过这个例子，就能够容易地总结出官方文档中的表格：

|     概念     |  单元素类型  |     数组类型     |  pandas数据类型   |
| :----------: | :----------: | :--------------: | :---------------: |
|  Date times  | `Timestamp`  | `DatetimeIndex`  | `datetime64[ns]`  |
| Time deltas  | `Timedelta`  | `TimedeltaIndex` | `timedelta64[ns]` |
|  Time spans  |   `Period`   |  `PeriodIndex`   |  `period[freq]`   |
| Date offsets | `DateOffset` |      `None`      |      `None`       |

由于时间段对象 `Period/PeriodIndex` 的使用频率并不高，因此书本上没有进行讲解，而**只涉及时间戳序列、时间差序列和日期偏置的相关内容。**

### 二、时间戳

#### 1.Timestamp的构造与属性

单个时间戳的生成利用 `pd.Timestamp` 实现，一般而言的常见日期格式都能被成功地转换：

```python
ts = pd.Timestamp('2020/1/1')
>>>
Timestamp('2020-01-01 00:00:00')
ts = pd.Timestamp('2020-1-1 08:10:30')
>>>
Timestamp('2020-01-01 08:10:30')
```

**通过 `year, month, day, hour, min, second`** 可以获取具体的数值：

```python
ts = pd.Timestamp('2020-1-1 08:10:30')
ts.year
2020

ts.month
1

ts.day
1

ts.hour
8

ts.minute
10

ts.second
30
```

在 `pandas` 中，时间戳的最小精度为纳秒 `ns` ，由于使用了64位存储，可以表示的时间范围大约可以如下计算：

![时间范围的计算](https://gitee.com/magicye/blogimage/raw/master/img/image-20210108233418973.png)

通过 `pd.Timestamp.max` 和 `pd.Timestamp.min` 可以获取时间戳表示的范围，可以看到确实表示的区间年数大小正如上述计算结果：

```python
pd.Timestamp.max
>>>
Timestamp('2262-04-11 23:47:16.854775807')
pd.Timestamp.min
>>>
Timestamp('1677-09-21 00:12:43.145225')
pd.Timestamp.max.year - pd.Timestamp.min.year
>>>
585
```

#### 2.Datetime序列的生成

一组时间戳可以组成时间序列，可以用 `to_datetime` 和 `date_range` 来生成。其中， **`to_datetime` 能够把一列时间戳格式的对象转换成为 `datetime64[ns]` 类型的时间序列：**

```python
pd.to_datetime(['2020-1-1', '2020-1-3', '2020-1-6'])
>>>
DatetimeIndex(['2020-01-01', '2020-01-03', '2020-01-06'], dtype='datetime64[ns]', freq=None)

df = pd.read_csv('data/learn_pandas.csv')
s = pd.to_datetime(df.Test_Date)
s.head()
>>>
0   2019-10-05
1   2019-09-04
2   2019-09-12
3   2020-01-03
4   2019-11-06
Name: Test_Date, dtype: datetime64[ns]
```

在极少数情况，时间戳的**格式不满足转换时**，**可以强制使用 `format` 进行匹配：**

```python
temp = pd.to_datetime(['2020\\1\\1','2020\\1\\3'],format='%Y\\%m\\%d')
temp
>>>
DatetimeIndex(['2020-01-01', '2020-01-03'], dtype='datetime64[ns]', freq=None)
#注意上面由于传入的是列表，而非 pandas 内部的 Series ，因此返回的是 DatetimeIndex ，如果想要转为 datetime64[ns] 的序列，需要显式用 Series 转化：
pd.Series(temp).head()
>>>
0   2020-01-01
1   2020-01-03
dtype: datetime64[ns]
```

另外，还存在一种把表的**多列时间属性拼接转为时间序列的 `to_datetime` 操作**，此时的**列名必须和以下给定的时间关键词列名一致：**

```python
df_date_cols = pd.DataFrame({'year': [2020, 2020],'month': [1, 1],'day': [1, 2],'hour': [10, 20],
'minute': [30, 50],'second': [20, 40]})
pd.to_datetime(df_date_cols)
>>>
0   2020-01-01 10:30:20
1   2020-01-02 20:50:40
dtype: datetime64[ns]
```

`date_range` 是一种生成连续间隔时间的一种方法

主要的参数为：

- start: 开始的时间
- end：结束的时间
- freq:  时间间隔
- periods: 时间戳的个数

其中，四个中的三个参数决定了，那么剩下的一个就随之确定了。这里要注意，开始或结束日期如果作为端点则它会被包含：

```python
pd.date_range('2020-1-1','2020-1-21', freq='10D') # 包含
>>>
DatetimeIndex(['2020-01-01', '2020-01-11', '2020-01-21'], dtype='datetime64[ns]', freq='10D')

pd.date_range('2020-1-1','2020-2-28', freq='10D')
>>>
DatetimeIndex(['2020-01-01', '2020-01-11', '2020-01-21', '2020-01-31',
               '2020-02-10', '2020-02-20'],
              dtype='datetime64[ns]', freq='10D')
pd.date_range('2020-1-1','2020-2-28', periods=6) # 由于结束日期无法取到，freq不为10天
>>>
DatetimeIndex(['2020-01-01 00:00:00', '2020-01-12 14:24:00',
               '2020-01-24 04:48:00', '2020-02-04 19:12:00',
               '2020-02-16 09:36:00', '2020-02-28 00:00:00'],
              dtype='datetime64[ns]', freq=None)
```

**这里的 `freq` 参数与 `DateOffset` 对象紧密相关，将在第四节介绍其具体的用法。**

练一练

> `Timestamp` 上定义了一个 `value` 属性，其返回的整数值代表了从1970年1月1日零点到给定时间戳相差的纳秒数，请利用这个属性构造一个随机生成给定日期区间内日期序列的函数。

```python
def my_func(start, end):
    ts_start = pd.Timestamp(start)
    ts_end = pd.Timestamp(end)
    #使用时间戳上的value属性，来构造随机的时间区间
    data_period = pd.data_range(ts_start, ts_end, freq=ts_start.value-ts_end.value)
    return data_period
```

最后，要**介绍一种改变序列采样频率的方法 `asfreq` ，它能够根据给定的 `freq` 对序列进行类似于 `reindex` 的操作**：

```python
s = pd.Series(np.random.rand(5),index=pd.to_datetime(['2020-1-%d'%i for i in range(1,10,2)]))
s.head()
>>>
2020-01-01    0.836578
2020-01-03    0.678419
2020-01-05    0.711897
2020-01-07    0.487429
2020-01-09    0.604705
dtype: float64
s.asfreq('D').head()
>>>
2020-01-01    0.836578
2020-01-02         NaN
2020-01-03    0.678419
2020-01-04         NaN
2020-01-05    0.711897
Freq: D, dtype: float64
s.asfreq('12H').head()
>>>
2020-01-01 00:00:00    0.836578
2020-01-01 12:00:00         NaN
2020-01-02 00:00:00         NaN
2020-01-02 12:00:00         NaN
2020-01-03 00:00:00    0.678419
Freq: 12H, dtype: float64
```

datetime64[ns]序列的最值与均值

> 前面提到了 `datetime64[ns]` 本质上可以理解为一个大整数，对于一个该类型的序列，可以使用 `max, min, mean` ，来取得最大时间戳、最小时间戳和“平均”时间戳。

#### 3.dt对象

如同 `category, string` 的序列上定义了 `cat, str` 来完成分类数据和文本数据的操作，在**时序类型的序列上定义了 `dt` 对象来完成许多时间序列的相关操作**。这里对于 `datetime64[ns]` 类型而言，可以大致**分为三类操作：取出时间相关的属性、判断时间戳是否满足条件、取整操作**。

第一类操作的常用属性包括： `date, time, year, month, day, hour, minute, second, microsecond, nanosecond, dayofweek, dayofyear, weekofyear, daysinmonth, quarter` ，

其中 `daysinmonth, quarter` 分别表示这个月有几天和季度。

```python
s = pd.Series(pd.date_range('2020-1-1','2020-1-3', freq='D'))
s.dt.date
>>>
0    2020-01-01
1    2020-01-02
2    2020-01-03
dtype: object
s.dt.time
>>>
0    00:00:00
1    00:00:00
2    00:00:00
dtype: object
s.dt.day
>>>
0    1
1    2
2    3
dtype: int64
s.dt.daysinmonth
>>>
0    31
1    31
2    31
dtype: int64
```

经常使用的是 `dayofweek` ，它返**回了周中的星期情况，周一为0、周二为1，以此类推：**

```python
s = pd.Series(pd.date_range('2020-1-1','2020-1-3', freq='D'))
s.dt.dayofweek
>>>
0    2
1    3
2    4
dtype: int64
```

此外，**可以通过 `month_name, day_name` 返回英文的月名和星期名，注意它们是方法而不是属性：**

```python
s.dt.month_name()
>>>
0    January
1    January
2    January
dtype: object
s.dt.day_name()
>>>
0    Wednesday
1     Thursday
2       Friday
dtype: object
```

第二类判断操作主要**用于测试是否为月/季/年的第一天或者最后一天：**

```python
s.dt.is_year_start # 还可选 is_quarter/month_start
>>>
0     True
1    False
2    False
dtype: bool
s.dt.is_year_end # 还可选 is_quarter/month_end
>>>
0    False
1    False
2    False
dtype: bool
```

第三类的**取整操作包含 `round, ceil, floor`** ，(向下取整、向上取整、取整)**它们的公共参数为 `freq` ，常用的包括 `H, min, S` （小时、分钟、秒），所有可选的 `freq` 可参考 [此处](https://pandas.pydata.org/docs/user_guide/timeseries.html#offset-aliases)** 。

```python
s = pd.Series(pd.date_range('2020-1-1 20:35:00','2020-1-1 22:35:00',freq='45min'))
s
>>>
0   2020-01-01 20:35:00
1   2020-01-01 21:20:00
2   2020-01-01 22:05:00
dtype: datetime64[ns]
    
s.dt.round('1H')
>>>
0   2020-01-01 21:00:00
1   2020-01-01 21:00:00
2   2020-01-01 22:00:00
dtype: datetime64[ns]

s.dt.ceil('1H')
>>>
0   2020-01-01 21:00:00
1   2020-01-01 22:00:00
2   2020-01-01 23:00:00
dtype: datetime64[ns]

s.dt.floor('1H')
>>>
0   2020-01-01 20:00:00
1   2020-01-01 21:00:00
2   2020-01-01 22:00:00
dtype: datetime64[ns]
```

#### 4.时间戳的切片与索引

一般而言，时间戳序列作为索引使用。如果想要**选出某个子时间戳序列。**

第一类方法是利用 `dt` 对象和布尔条件联合使用，**另一种方式是利用切片，后者常用于连续时间戳**。下面，举一些例子说明

```python
s = pd.Series(np.random.randint(2,size=366),index=pd.date_range('2020-01-01','2020-12-31'))
#查看这个序列
s.head()
>>>
2020-01-01    1
2020-01-02    1
2020-01-03    0
2020-01-04    1
2020-01-05    0
Freq: D, dtype: int32
#提取出index变为时间戳的序列
idx = pd.Series(s.index).dt
#每月的第一天或者最后一天
#第一类的方法对象的dt对象和布尔条件，来找出对应的值
s[(idx.is_month_start|idx.is_month_end).values].head()
>>>
2020-01-01    1
2020-01-31    0
2020-02-01    1
2020-02-29    1
2020-03-01    0
dtype: int32
#双休日
s[idx.dayofweek.isin([5,6]).values].head()
>>>
2020-01-04    1
2020-01-05    0
2020-01-11    0
2020-01-12    1
2020-01-18    1
dtype: int32
#取出单日值
s['2020-01-01']
>>>
1
s['20200101'] # 自动转换为标准格式
>>>
1
#取出七月
s['2020-07'].head()
>>>
2020-07-01    0
2020-07-02    1
2020-07-03    0
2020-07-04    0
2020-07-05    0
Freq: D, dtype: int32
#取出5月初至7月15日
s['2020-05':'2020-7-15'].head()
>>>
2020-05-01    0
2020-05-02    1
2020-05-03    0
2020-05-04    1
2020-05-05    1
Freq: D, dtype: int32
s['2020-05':'2020-7-15'].tail()
>>>
2020-07-11    0
2020-07-12    0
2020-07-13    1
2020-07-14    0
2020-07-15    1
Freq: D, dtype: int32
```

### 三、时间差

#### 1.Timedelta的生成

正如在第一节中所说，**时间差可以理解为两个时间戳的差，这里也可以通过 `pd.Timedelta` 来构造**：

```python
pd.Timestamp('20200102 08:00:00')-pd.Timestamp('20200101 07:35:00')
>>>
Timedelta('1 days 00:25:00')
pd.Timedelta(days=1, minutes=25) # 需要注意加s
>>>
Timedelta('1 days 00:25:00')
pd.Timedelta('1 days 25 minutes') # 字符串生成
>>>
Timedelta('1 days 00:25:00')
```

生成时间差序列的主要方式是 `pd.to_timedelta` ，**其类型为 `timedelta64[ns]` ：**

```python
s = pd.to_timedelta(df.Time_Record)
s.head()
>>>
0   0 days 00:04:34
1   0 days 00:04:20
2   0 days 00:05:22
3   0 days 00:04:08
4   0 days 00:05:22
Name: Time_Record, dtype: timedelta64[ns]
```

**与 `date_range` 一样，时间差序列也可以用 `timedelta_range`** 来生成，它们两者具有一致的参数(start, end, freq, period)：

```python
pd.timedelta_range('0s', '1000s', freq='6min')
>>>
TimedeltaIndex(['0 days 00:00:00', '0 days 00:06:00', '0 days 00:12:00'], dtype='timedelta64[ns]', freq='6T')
pd.timedelta_range('0s', '1000s', periods=3)
>>>
TimedeltaIndex(['0 days 00:00:00', '0 days 00:08:20', '0 days 00:16:40'], dtype='timedelta64[ns]', freq=None)
```

对于 `Timedelta` 序列，同样也定义了 `dt` 对象，上面主要定义了的属性包括 `days, seconds, mircroseconds, nanoseconds` ，它们分别返回了对应的时间差特征。需要注意的是，**这里的 `seconds` 不是指单纯的秒，而是对天数取余后剩余的秒数：**

```python
s = pd.to_timedelta(df.Time_Record)
s.dt.seconds.head()
>>>
0    274
1    260
2    322
3    248
4    322
Name: Time_Record, dtype: int64
```

如果**不想对天数取余而直接对应秒数，可以使用 `total_seconds`**

```
s.dt.total_seconds().head()
>>>
0    274.0
1    260.0
2    322.0
3    248.0
4    322.0
Name: Time_Record, dtype: float64
```

与时间戳序列类似，取整函数**取整操作包含 `round, ceil, floor`** 也是可以在 `dt` 对象上使用的：

```python
pd.to_timedelta(df.Time_Record).dt.round('min').head()
>>>
0   0 days 00:05:00
1   0 days 00:04:00
2   0 days 00:05:00
3   0 days 00:04:00
4   0 days 00:05:00
Name: Time_Record, dtype: timedelta64[ns]
```

#### 2.Timedelta的运算

时间差支持的常用运算有三类：与**标量的乘法运算、与时间戳的加减法运算、与时间差的加减法与除法运算：**

```python
#两个时间差
td1 = pd.Timedelta(days=1)
td2 = pd.Timedelta(days=3)
#时间戳进行实践
ts = pd.Timestamp('20200101')

#与标量的乘法运算
td1 * 2
>>> Timedelta('2 days 00:00:00')
#与时间戳的加减法运算
ts + td1
>>> Timestamp('2020-01-02 00:00:00')
ts - td1
>>> Timestamp('2019-12-31 00:00:00')
#与时间差的加减法与除法运算
td2 - td1
>>> Timedelta('2 days 00:00:00')
```

这些运算都可以移植到时间差的序列(两序列间的计算也可以像单个的时间差和时间戳一样的使用)上：

```python
#两个时间差的序列
td1 = pd.timedelta_range(start='1 days', periods=5)
td2 = pd.timedelta_range(start='12 hours',freq='2H',periods=5)
#时间戳
ts = pd.date_range('20200101', '20200105')

td1 * 5
>>>
TimedeltaIndex(['5 days', '10 days', '15 days', '20 days', '25 days'], dtype='timedelta64[ns]', freq='5D')

td1 * pd.Series(list(range(5))) # 逐个相乘
>>>
0    0 days
1    2 days
2    6 days
3   12 days
4   20 days
dtype: timedelta64[ns]

td1 - td2
>>>
TimedeltaIndex(['0 days 12:00:00', '1 days 10:00:00', '2 days 08:00:00',
                '3 days 06:00:00', '4 days 04:00:00'],
               dtype='timedelta64[ns]', freq=None)

td1 + pd.Timestamp('20200101')
>>>
DatetimeIndex(['2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05',
               '2020-01-06'],
              dtype='datetime64[ns]', freq='D')

td1 + ts # 逐个相加
>>>
DatetimeIndex(['2020-01-02', '2020-01-04', '2020-01-06', '2020-01-08',
               '2020-01-10'],
              dtype='datetime64[ns]', freq=None)
```

### 四、日期偏置

#### 1.Offset对象

**日期偏置是一种和日历相关的特殊时间差**，例如回到第一节中的两个问题：如何求2020年9月第一个周一的日期，以及如何求2020年9月7日后的第30个工作日是哪一天。

```python
pd.Timestamp('20200831') + pd.offsets.WeekOfMonth(week=0,weekday=0)
>>> 
Timestamp('2020-09-07 00:00:00')
pd.Timestamp('20200907') + pd.offsets.BDay(30)
>>> 
Timestamp('2020-10-19 00:00:00')
pd.Timestamp('20200831') - pd.offsets.WeekOfMonth(week=0,weekday=0)
>>>
Timestamp('2020-08-03 00:00:00')
pd.Timestamp('20200907') - pd.offsets.BDay(30)
>>>
Timestamp('2020-07-27 00:00:00')
pd.Timestamp('20200907') + pd.offsets.MonthEnd()
>>>
Timestamp('2020-09-30 00:00:00')
```

从上面的例子中可以看到， `Offset` 对象在 `pd.offsets` 中被定义。**当使用 `+` 时获取离其最近的下一个日期，当使用 `-` 时获取离其最近的上一个日期.**

常用的日期偏置如下可以查阅这里的 [文档](https://pandas.pydata.org/docs/user_guide/timeseries.html#dateoffset-objects) 描述。在文档罗列的 `Offset` 中，需要介绍一个特殊的 `Offset` 对象 `CDay` ，

其中的 `holidays, weekmask` 参数能够**分别对自定义的日期和星期进行过滤**，**前者传入了需要过滤的日期列表，后者传入的是三个字母的星期缩写构成的星期字符串，其作用是只保留字符串中出现的星期**,**参数n表示：增加n天的CDay，来进行匹配**。

```python
my_filter = pd.offsets.CDay(n=1,weekmask='Wed Fri',holidays=['20200109'])

dr = pd.date_range('20200108', '20200111')

dr.to_series().dt.dayofweek
>>>
2020-01-08    2
2020-01-09    3
2020-01-10    4
2020-01-11    5
Freq: D, dtype: int64

#列表生成式
[i + my_filter for i in dr]
>>>
[Timestamp('2020-01-10 00:00:00'),
 Timestamp('2020-01-10 00:00:00'),
 Timestamp('2020-01-15 00:00:00'),
 Timestamp('2020-01-15 00:00:00')]
```

在上面的例子中， `n` 表示增加一天 `CDay` ， `dr` 中的第一天为 `20200108` ，但由于下一天 `20200109` 被排除了，并且 `20200110` 是合法的周五，因此转为 `20200110` ，其他后面的日期处理类似。

**PS：不要使用部分 `Offset`**

> 在当前版本下由于一些 `bug` ，不要使用 `Day` 级别以下的 `Offset` 对象，比如 `Hour, Second` 等，请使用对应的 `Timedelta` 对象来代替。

#### 2.偏置字符串

前面提到了关于 `date_range` 的 `freq` 取值可用 `Offset` 对象，同时在 `pandas` 中**几乎每一个 `Offset` 对象绑定了日期偏置字符串**（ `frequencies strings/offset aliases` ），**可以指定 `Offset` 对应的字符串来替代使用**。下面举一些常见的例子。

```python
pd.date_range('20200101','20200331', freq='MS') # 月初
>>>
DatetimeIndex(['2020-01-01', '2020-02-01', '2020-03-01'], dtype='datetime64[ns]', freq='MS')

pd.date_range('20200101','20200331', freq='M') # 月末
>>>
DatetimeIndex(['2020-01-31', '2020-02-29', '2020-03-31'], dtype='datetime64[ns]', freq='M')

pd.date_range('20200101','20200110', freq='B') # 工作日
>>>
DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-06',
               '2020-01-07', '2020-01-08', '2020-01-09', '2020-01-10'],
              dtype='datetime64[ns]', freq='B')

pd.date_range('20200101','20200201', freq='W-MON') # 周一
>>>
DatetimeIndex(['2020-01-06', '2020-01-13', '2020-01-20', '2020-01-27'], dtype='datetime64[ns]', freq='W-MON')

pd.date_range('20200101','20200201',
freq='WOM-1MON') # 每月第一个周一
>>>
DatetimeIndex(['2020-01-06'], dtype='datetime64[ns]', freq='WOM-1MON')
```

上面的这些字符串，等价于使用如下的 `Offset` 对象：

```python
pd.date_range('20200101','20200331',freq=pd.offsets.MonthBegin())
>>>
DatetimeIndex(['2020-01-01', '2020-02-01', '2020-03-01'], dtype='datetime64[ns]', freq='MS')

pd.date_range('20200101','20200331',freq=pd.offsets.MonthEnd())
>>>
DatetimeIndex(['2020-01-31', '2020-02-29', '2020-03-31'], dtype='datetime64[ns]', freq='M')

pd.date_range('20200101','20200110', freq=pd.offsets.BDay())
>>>
DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-06',
               '2020-01-07', '2020-01-08', '2020-01-09', '2020-01-10'],
              dtype='datetime64[ns]', freq='B')

pd.date_range('20200101','20200201',
freq=pd.offsets.CDay(weekmask='Mon'))
>>>
DatetimeIndex(['2020-01-06', '2020-01-13', '2020-01-20', '2020-01-27'], dtype='datetime64[ns]', freq='C')

pd.date_range('20200101','20200201',            freq=pd.offsets.WeekOfMonth(week=0,weekday=0))
>>>
DatetimeIndex(['2020-01-06'], dtype='datetime64[ns]', freq='WOM-1MON')
```

**关于时区问题的说明**

> 各类时间对象的开发，除了使用 `python` 内置的 `datetime` 模块， `pandas` 还利用了 `dateutil` 模块，很大一部分是为了处理时区问题。总所周知，**我国是没有夏令时调整时间一说的，但有些国家会有这种做法**，导致了相对而言一天里可能会有23/24/25个小时，也就是 `relativedelta` ，**这使得 `Offset` 对象和 `Timedelta` 对象有了对同一问题处理产生不同结果的现象**，其中的规则也较为复杂，官方文档的写法存在部分描述错误，并且难以对描述做出统一修正，因为牵涉到了 `Offset` 相关的很多组件。

### 五、时序中的滑动与分组

#### 1.滑动窗口

所谓时序的滑窗函数，即把滑动窗口用 `freq` 关键词代替。

下面给出一个具体的应用案例：在股票市场中有一个指标为 `BOLL` 指标，它由中轨线、上轨线、下轨线这三根线构成，具体的计算方法分别是 `N` 日均值线、 `N` 日均值加两倍 `N` 日标准差线、 `N` 日均值减两倍 `N` 日标准差线。**利用 `rolling` 对象计算 `N=30` 的 `BOLL` 指标可以如下写出**

书本上的实例代码：

```python
In [101]: import matplotlib.pyplot as plt

In [102]: idx = pd.date_range('20200101', '20201231', freq='B')

In [103]: np.random.seed(2020)

In [104]: data = np.random.randint(-1,2,len(idx)).cumsum() # 随机游动构造模拟序列

In [105]: s = pd.Series(data,index=idx)

In [106]: s.head()
Out[106]: 
2020-01-01   -1
2020-01-02   -2
2020-01-03   -1
2020-01-06   -1
2020-01-07   -2
Freq: B, dtype: int32

In [107]: r = s.rolling('30D')

In [108]: plt.plot(s)
Out[108]: [<matplotlib.lines.Line2D at 0x2ed114978c8>]

In [109]: plt.title('BOLL LINES')
Out[109]: Text(0.5, 1.0, 'BOLL LINES')

In [110]: plt.plot(r.mean())
Out[110]: [<matplotlib.lines.Line2D at 0x2ed11497f88>]

In [111]: plt.plot(r.mean()+r.std()*2)
Out[111]: [<matplotlib.lines.Line2D at 0x2ed114a3608>]

In [112]: plt.plot(r.mean()-r.std()*2)
Out[112]: [<matplotlib.lines.Line2D at 0x2ed114ab388>]
```

![boll图像](https://gitee.com/magicye/blogimage/raw/master/img/image-20210110161321127.png)

对于 `shift` 函数而言，作用在 `datetime64` 为索引的序列上时，**可以指定 `freq` 单位进行滑动：**

```python
s.shift(freq='50D').head()
>>>
2020-02-20   -1
2020-02-21   -2
2020-02-22   -1
2020-02-25   -1
2020-02-26   -2
dtype: int32
```

另外， `datetime64[ns]` 的序列进行 `diff` (dt.diff(n) = df.shift(n) - dt)后就能够得到 `timedelta64[ns]` 的序列，**这能够使用户方便地观察有序时间序列的间隔：**

```python
my_series = pd.Series(s.index)
my_series.head()
>>>
0   2020-01-01
1   2020-01-02
2   2020-01-03
3   2020-01-06
4   2020-01-07
dtype: datetime64[ns]
    
my_series.diff(1).head()
>>>
0      NaT
1   1 days
2   1 days
3   3 days
4   1 days
dtype: timedelta64[ns]
```

#### 2.重采样

**重采样对象 `resample`** 和第四章中分组对象 `groupby` 的用法类似，前者**是针对时间序列的分组计算而设计的分组对象。**

例如，对上面的序列计算**每10天的均值：**

```python
s.resample('10D').mean().head()
>>>
2020-01-01   -2.000000
2020-01-11   -3.166667
2020-01-21   -3.625000
2020-01-31   -4.000000
2020-02-10   -0.375000
Freq: 10D, dtype: float64
```

同时，如果没有内置定义的处理函数，可以通过 `apply` 方法自定义：

```python
#十天内的最大值最小值的极差
s.resample('10D').apply(lambda x:x.max()-x.min()).head() # 极差
>>>
2020-01-01    3
2020-01-11    4
2020-01-21    4
2020-01-31    2
2020-02-10    4
Freq: 10D, dtype: int32
```

在 `resample` 中要**特别注意组边界值的处理情况**，默认情况下起始值的计算方法是**从最小值时间戳对应日期的午夜 `00:00:00` 开始增加 `freq` ，直到不超过该最小时间戳的最大时间戳**，**由此对应的时间戳为起始值，然后每次累加 `freq` 参数作为分割结点进行分组，区间情况为左闭右开。**下面构造一个不均匀的例子：

```python
idx = pd.date_range('20200101 8:26:35', '20200101 9:31:58', freq='77s')
data = np.random.randint(-1,2,len(idx)).cumsum()#梯次累加
s = pd.Series(data,index=idx)
s.head()
>>>
2020-01-01 08:26:35   -1
2020-01-01 08:27:52   -1
2020-01-01 08:29:09   -2
2020-01-01 08:30:26   -3
2020-01-01 08:31:43   -4
Freq: 77S, dtype: int32
#在以7min为freq的分组中
#起始值为最小时间戳的午夜开始叠加freq
#直到接近最小时间戳的最大值为起始的分组依据开始计算
s.resample('7min').mean().head()
>>>
2020-01-01 08:24:00   -1.750000
2020-01-01 08:31:00   -2.600000
2020-01-01 08:38:00   -2.166667
2020-01-01 08:45:00    0.200000
2020-01-01 08:52:00    2.833333
Freq: 7T, dtype: float64
```

对应的第一个组起始值为 `08:24:00` ，其是从当天0点增加72个 `freq=7 min` 得到的，(这就是初始的分组值)如果再增加一个 `freq` 则超出了序列的最小时间戳 `08:26:35` 

有时候，用户**希望从序列的最小时间戳开始依次增加 `freq` 进行分组**，此时**可以指定 `origin` 参数为 `start`** ：

```python
s.resample('7min', origin='start').mean().head()
>>>
2020-01-01 08:26:35   -2.333333
2020-01-01 08:33:35   -2.400000
2020-01-01 08:40:35   -1.333333
2020-01-01 08:47:35    1.200000
2020-01-01 08:54:35    3.166667
Freq: 7T, dtype: float64
```

**在返回值中，要注意索引一般是取组的第一个时间戳(就是每个分组的第一元素)**，**但 `M, A, Q, BM, BA, BQ, W` 这七个是取对应区间的最后一个时间戳：**

```python
s = pd.Series(np.random.randint(2,size=366),index=pd.date_range('2020-01-01','2020-12-31'))
#返回值要为取组的最后一个元素
s.resample('M').mean().head()
>>>
2020-01-31    0.451613
2020-02-29    0.448276
2020-03-31    0.516129
2020-04-30    0.566667
2020-05-31    0.451613
Freq: M, dtype: float64
#取组的第一个
s.resample('MS').mean().head() # 结果一样，但索引不同
>>>
2020-01-01    0.451613
2020-02-01    0.448276
2020-03-01    0.516129
2020-04-01    0.566667
2020-05-01    0.451613
Freq: MS, dtype: float64
```

### 六、练习

在代码的文件夹