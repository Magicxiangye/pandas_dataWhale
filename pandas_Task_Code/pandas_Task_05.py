import pandas as pd
import numpy as np


#Ex1:美国非法药物数据集
def drugs():
    #1.将数据转为如下的形式：
    #ignore_index(忽略之前的索引的值，用新排的顺序作为新的索引)
    df = pd.read_csv('data/Drugs.csv').sort_values(['State','COUNTY','SubstanceName'],ignore_index=True)
    #print(df.head())
    df_2 = df.pivot(index=['State', 'COUNTY', 'SubstanceName'], columns='YYYY', values='DrugReports').reset_index().rename_axis(columns= {'YYYY': ''})
    #要和图片的一样
    #print(df_2.head())
    #2.将变换的还原回去
    #先看看，变为宽表的列的索引都有些什么（宽表再变为长表melt()函数）
    print(df_2.columns)
    res = df_2.melt(id_vars=['State', 'COUNTY', 'SubstanceName'], value_vars=df_2.columns[3:],
                    value_name='DrugReports', var_name='YYYY').dropna(subset=['DrugReports'])
    #还原还需要把数据的存储的格式以及去掉空值
    #print(res.head())
    #print(res.sort_values(['State','COUNTY','SubstanceName'],ignore_index=True).astype({'YYYY':'int64', 'DrugReports':'int64'}).head())
    #按 State 分别统计每年的报告数量总和，其中 State, YYYY 分别为列索引和行索引，
    # 要求分别使用 pivot_table 函数与 groupby+unstack 两种不同的策略实现，并体会它们之间的联系。
    #先用的式pivot_table来实现
    res_2 = df.pivot_table(index='YYYY', columns='State', values='DrugReports', aggfunc='sum')
    print(res_2.head())
    #groupby+unstack
    res_3 = df.groupby(['YYYY', 'State'])['DrugReports'].sum().to_frame().unstack().droplevel(0, axis=1)
    print(res_3)

#Ex2：特殊的wide_to_long方法
#没啥思路，借鉴了答案写的
def sp_wide_to_long():
    df = pd.DataFrame({'Class': [1, 2],'Name':['San Zhang', 'Si Li'],'Chinese':[80, 90],'Math':[80, 75]})
    print(df)
    #使用的wide_to_long方法来实现宽表还原为长表的要求
    df = df.rename(columns={'Chinese': 'pre_Chinese', 'Math': 'pre_Math'})
    res = pd.wide_to_long(df,stubnames = ['pre'],i = ['Class', 'Name'],j = 'Subject',sep = '_',suffix = '.+').reset_index().rename(columns={'pre': 'Grade'})
    print(res)

#测试用
if __name__ == '__main__':
    sp_wide_to_long()
    #drugs()
