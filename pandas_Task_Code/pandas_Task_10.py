import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Ex1：太阳辐射数据集
def solar():
    df = pd.read_csv('data/solar.csv', usecols=['Data', 'Time','Radiation', 'Temperature'])
    print(df.head())
    # 1.将 Datetime, Time 合并为一个时间列 Datetime ，同时把它作为索引后排序。
    # Data先为的是str类型的数据，先用str的提取函数
    # 使用正则来提取
    solar_date = df.Data.str.extract('([/|\w]+\s).+')[0]
    # 合成为时间的数据序列
    df['Data'] = pd.to_datetime(solar_date + df.Time)
    # 去掉time这一列
    df = df.drop(columns='Time')
    # 重命名以及以时间来排序
    df = df.rename(columns={'Data':'Datetime'}).set_index('Datetime').sort_index()
    print(df.head(3))
    # 2.每条记录时间的间隔显然并不一致，请解决如下问题
    # a.找出间隔时间的前三个最大值所对应的三组时间戳。
    # 思路-像是第十章的那样使用diff()函数
    s = df.index.to_series().reset_index(drop=True)
    group_seconds = s.diff().dt.total_seconds()
    # nlargest()的优点就是能一次看到最大的几行，而且不需要排序。缺点就是只能看到最大的，看不到最小的。
    max_3 = group_seconds.nlargest(3).index
    # union()功能回头再研究一下
    out = df.index[max_3.union(max_3 - 1)]
    print(out)
    # b.是否存在一个大致的范围，使得绝大多数的间隔时间都落在这个区间中？
    # 如果存在，请对此范围内的样本间隔秒数画出柱状图，设置 bins=50 。
    s = s.diff().dt.total_seconds()
    res = s.mask((s > s.quantile(0.99)) | (s < s.quantile(0.01)))
    _ = plt.hist(res, bins=50)
    plt.show()
    # 3.求如下指标对应的 Series ：
    # 温度与辐射量的6小时滑动相关系数
    res = df.Radiation.rolling('6H').corr(df.Temperature)
    print(res.tail(3))
    # 以三点、九点、十五点、二十一点为分割，该观测所在时间区间的温度均值序列
    res = df.Temperature.resample('6H', origin='03:00:00').mean()
    print(res.head(3))
    # 每个观测6小时前的辐射量（一般而言不会恰好取到，此时取最近时间戳对应的辐射量）
    my_dt = df.index.shift(freq='-6H')
    int_loc = [df.index.get_loc(i, method='nearest') for i in my_dt]
    res = df.Radiation.iloc[int_loc]
    print(res.tail(3))

# EX2:水果销量数据集
def fruit():
    # 每月上半月（15号及之前）与下半月葡萄销量的比值
    df = pd.read_csv('data/fruit.csv')
    df.Date = pd.to_datetime(df.Date)
    df_grape = df.query("Fruit == 'Grape'")
    res = df_grape.groupby([np.where(df_grape.Date.dt.day <= 15,'First', 'Second'), df_grape.Date.dt.month])['Sale'].mean().to_frame().unstack(0).droplevel(0,axis=1)
    res = (res.First / res.Second).rename_axis('Month')
    print(res.head())
    # 每月最后一天的生梨销量总和
    res = df[df.Date.dt.is_month_end].query("Fruit == 'Pear'").groupby('Date').Sale.sum().head()
    print(res.head())
    # 每月最后一天工作日的生梨销量总和
    res = df[df.Date.isin(pd.date_range('20190101', '20191231',freq = 'BM'))].query("Fruit == 'Pear'").groupby('Date').Sale.mean().head()
    print(res.head())
    # 每月最后五天的苹果销量均值
    target_dt = df.drop_duplicates().groupby(df.Date.drop_duplicates().dt.month)['Date'].nlargest(5).reset_index(drop=True)
    res = df.set_index('Date').loc[target_dt].reset_index().query("Fruit == 'Apple'")
    res = res.groupby(res.Date.dt.month)['Sale'].mean().rename_axis('Month')
    print(res.head())
    # 2.按月计算周一至周日各品种水果的平均记录条数，行索引外层为水果名称，内层为月份，列索引为星期。

    # 3.按天计算向前10个工作日窗口的苹果销量均值序列，非工作日的值用上一个工作日的结果填充
    df_apple = df[(df.Fruit == 'Apple') & (~df.Date.dt.dayofweek.isin([5, 6]))]
    s = pd.Series(df_apple.Sale.values,index = df_apple.Date).groupby('Date').sum()
    res = s.rolling('10D').mean().reindex(pd.date_range('20190101', '20191231')).fillna(method='ffill')
    print(res.head())

# 测试用
if __name__ == '__main__':
    fruit()