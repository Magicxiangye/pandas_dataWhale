import pandas as pd
import numpy as np


#第六章的任务
#EX1：美国疫情的数据集
def us_Covid19():
    #4月12日至11月16日的疫情报表，请将 New York 的 Confirmed, Deaths, Recovered, Active 合并为一张表，
    # 索引为按如下方法生成的日期字符串序列：
    #按照样例的索引列的生成
    date = pd.date_range('20200412', '20201116').to_series()
    #pandas.Series.dt.month和pandas.Series.dt.day来提取月份和日期
    date = date.dt.month.astype('string').str.zfill(2)+'-'+date.dt.day.astype('string').str.zfill(2)+'-'+'2020'

    date = date.tolist()
    #用来保存的是定位到的数据，进行保存
    data = []
    #要提取4月12日至11月16日的疫情报表
    #使用定位的话，要把默认的行的索引更改
    #index_col:变为行索引的列的名称，以城市的列为行索引进行定位
    for use_data in date:
        new_date = pd.read_csv('data/us_report/'+ use_data +'.csv', index_col='Province_State')
        data_add = new_date.loc['New York',['Confirmed', 'Deaths', 'Recovered', 'Active']]
        #先一个个的DataFrame存在数组中，最后在来拼接
        #loc当定位到唯一的输出的时候，是Series格式的
        #所以要转换一下类型加转置一下
        print(data_add)
        data.append(data_add.to_frame().T)

    #拼接数据
    res = pd.concat(data)
    #每一行一一对应的是年份，把索引给替换掉
    res.index = date
    print(res.head())

#EX2:实现join()函数（重难）
def my_join(df1, df2, how='left'):
    #理解答案的代码
    #拼接完成后的表的索引，先保存
    res_col = df1.columns.tolist() + df2.columns.tolist()
    #how有是四种的连接方式

    pass

if __name__ == '__main__':
    us_Covid19()