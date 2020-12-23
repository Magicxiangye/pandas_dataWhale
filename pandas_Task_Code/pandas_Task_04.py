import pandas as pd
import numpy as np

def car():
    df = pd.read_csv('data/car.csv')
    #先过滤出所属 Country 数超过2个的汽车，
    # 即若该汽车的 Country 在总体数据集中出现次数不超过2则剔除，(一个城市少于两台车的剔除？？)
    # 再按 Country 分组计算价格均值、价格变异系数、该 Country 的汽车数量，
    # 其中变异系数的计算方法是标准差除以均值，并在结果中把变异系数重命名为 CoV 。
    #print(df.head())
    gb = df.groupby('Country')
    res = gb.filter(lambda x: x.shape[0] > 2)
    #print(res)
    #聚合函数的使用
    final = res.groupby('Country')['Price'].agg([ 'mean', 'count', ('Cov',lambda x: x.std() / x.mean() )])#使用多个的内置聚合函数
    print(final)
    #按照表中位置的前三分之一、中间三分之一和后三分之一分组，统计 Price 的均值。

#测试代码用
if __name__ == '__main__':
    car()