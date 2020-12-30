#第六章，综合练习代码

import pandas as pd
import numpy as np


#任务一（企业收入的多样性）
def CompanyIncome():
    # 其中p(xi)是企业该年某产业收入额占该年所有产业总收入的比重。
    # 在company.csv中存有需要计算的企业和年份，在company_data.csv中存有企业、
    # 各类收入额和收入年份的信息。现请利用后一张表中的数据，在前一张表中增加一列表示该公司该年份的收入熵指标I。
    #思路
    #1.读取证券的代码和日期
    #2.在第二张表中，将证券的代码和时间的不同作为index来分组
    #3.计算出组中每一个收入类型的比重，再进行聚合函数的使用
    #4.取出公司代码的index为pd.Series,与第一个的公式的证卷代码进行比较--mask()

    #读取表格文件
    df1 = pd.read_csv('data/Company.csv')
    df2 = pd.read_csv('data/Company_data.csv')
    #先对第二章表格进行分组
    #分组的标准是【证卷代码和时间】
    df2.set_index(['证券代码', '日期'])
    def percent(x):
        count = []
        for per in x:
            per = per/x.sum()
            print(per)
            count.append(per)
        series = pd.Series(count)
        return series


    df2_group = df2.groupby(['证券代码', '日期'])['收入额'].apply(percent)
    print(df2_group.size())



if __name__ == '__main__':
    CompanyIncome()