#第六章，综合练习代码

import pandas as pd
import math
import xlrd
import openpyxl
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
    #4.pd的连接函数

    #读取表格文件
    df1 = pd.read_csv('data/Company.csv')
    df2 = pd.read_csv('data/Company_data.csv')
    #先对第二章表格进行分组
    #分组的标准是【证卷代码和时间】
    print(df1.dtypes)
    df2.set_index(['证券代码', '日期'])
    #把两张表的证券代码的格式统一一下（＃号加六位数）zfill()向右对齐
    df2['证券代码'] = df2['证券代码'].apply(lambda x: '#' + str(x).zfill(6))
    #再把两张表的日期统一一下，方便表连接
    df2['日期'] = df2['日期'].apply(lambda x: int(x[0:4]))
    # 收入熵的计算函数
    def percent(x):
        count = []
        entry_income = 0
        for per in x:
            per = per/x.sum()
            print(per)
            if per > 0:
                entry_income += -(per * math.log2(per))
            # count.append(per)
        # DataF = pd.DataFrame(count)
        return entry_income
    df2.mask(df2['收入额'] < 0, 'NaN')
    print(df2.head())
    # df2['收入额'].apply(lambda x: x/x.sum())
    df2_group = df2.groupby(['证券代码', '日期'])['收入额'].agg(percent)
    final_df2 = pd.DataFrame(df2_group, columns=['收入额']).reset_index(level=['证券代码', '日期'])
    print(final_df2.head())
    income_data = final_df2['收入额']
    print(income_data.head())
    # concat()实现值的连接
    new_data = pd.merge(df1, final_df2)
    new_data.rename(index={'收入额': 'I'})
    print(new_data.head())

#Ex2:组队学习信息表的变换
def team_data():
    # xlrd的版本不对，踩坑了，用的openpyxl
    df = pd.read_excel('data/Pandas_team.xlsx',  engine='openpyxl')
    print(df.head())
    # 队长的信息成为一个表
    captain_data = pd.DataFrame(data=df[['队伍名称', '队长_群昵称', '队长编号']])
    captain_data.columns = ['队伍名称', '昵称', '编号']
    captain_data.insert(0,'是否队长', 1)
    print(captain_data.head())

    dic = {}
    # 队员的小表格for循环批量产生
    for i in range(10):
        i = i+1
        team_data = pd.DataFrame(data=df[['队伍名称', '队员{}'.format(i)+'_群昵称', '队员{}'.format(i) + ' ' + '编号']])
        team_data.columns = ['队伍名称', '昵称', '编号']
        team_data.insert(0, '是否队长', 0)
        print(team_data.head())
        dic[i] = team_data

     # 纵向的表格拼接(全拼接上就行)(只先连上三个测试一下)
    data = pd.concat([captain_data, dic[1], dic[2],dic[3]]).sort_values(by='队伍名称').reset_index(drop=True)
    print(data)


# Ex3 美国大选投票情况
def ASvote():
    # 两张数据表中分别给出了美国各县（county）的人口数以及大选的投票情况，请解决以下问题：
    # 1.有多少县满足总投票数超过县人口数的一半
    df1 = pd.read_csv('data/president_county_candidate.csv')
    df2 = pd.read_csv('data/county_population.csv')
    # 先分组累计投票的总数
    country_vote_gb = pd.DataFrame(df1.groupby('county')['total_votes'].sum()).reset_index()
    # 把城市的人口表格做处理（先分为state和county）
    # 使用函数来分割一下
    df2['county'] = df2['US County'].str.split(',', 1).str[0]
    df2['county'] = df2['county'].str.split('.', 1).str[1]
    df2['state'] = df2['US County'].str.split(',', 1).str[1]
    # 把原来的列丢弃
    df2.drop('US County', axis=1, inplace=True)
    print(df2.head())
    #整合一下两张表
    df_vote = country_vote_gb.merge(df2, on='county', how='left')
    print(df_vote.head())
    test = list(df_vote['total_votes'] >= df_vote['Population']/2)
    county_name = pd.DataFrame(df_vote['county'].where(test, np.nan))
    print(county_name['county'].dropna().unique())
    #print(country_vote_gb.head(10))
    # 2.把州（state）作为行索引，把投票候选人作为列名，列名的顺序按照候选人在全美的总票数由高到低排序，
    # 行列对应的元素为该候选人在该州获得的总票数
    # (写不完了)


#测试用
if __name__ == '__main__':
    ASvote()