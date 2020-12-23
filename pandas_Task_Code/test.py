import pandas as pd
import numpy as np
from numpy import number

if __name__ == '__main__':
    # data = pd.Series([1,2,3])
    # #反向的为2的滑动窗口
    # #先得出反向的shift(-1)的数据
    # back_data= data.shift(-1)
    # print(back_data)
    # print(data + back_data)
    # data = pd.Series([1, 2, 3])[::-1]
    # print(data.rolling(2).sum()[::-1])
    # s = pd.Series(['a', 'b', 'c', 'd', 'e', 'f'],
    #               index=[1, 3, 1, 2, 5, 4])
    # print(s[1:-1:1])
    df = pd.read_csv('data/learn_pandas.csv')
    #df_demo = df.set_index('Name')
    #若要选出所有数值型的列
    #布尔的选择列表
    #print(df_demo.dtypes)
    # condition_dtype = df.dtypes.isin(['int64','float64'])
    # final_col = list(df.dtypes.loc[condition_dtype].index)
    # print(df[final_col].head())
    # df_multi = df.set_index(['School', 'Grade'])
    # df_multi = df_multi.sort_index()
    # test = set(df_multi.index.values)
    # print(list(test))
    # print(df_multi.loc[list(test)[0:3]].head())
    gb = df.groupby('Gender')[['Height', 'Weight']]
    #gb.filter(lambda x: print(x.shape[0])).head()
    #print(gb.filter(lambda x: x.shape[0] > 100).head())
    #test = gb.apply(lambda x: pd.DataFrame(np.ones((2, 2)),index = ['a','b']))
    #print(test)
    print(df.groupby('Gender')[['Height', 'Weight']].mean())
    test = gb.apply(lambda x: x.cov())
    print(test)
