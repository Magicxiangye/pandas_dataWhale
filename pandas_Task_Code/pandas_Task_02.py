import pandas as pd
import numpy as np
#Task_02代码

#Ex1宝可梦
def pokemon():
    #读入文件
    df = pd.read_csv('data/pokemon.csv')
    #print(df.head(3))
    #对 HP, Attack, Defense, Sp. Atk, Sp. Def, Speed 进行加总，验证是否为 Total 值
    #要提取列的list
    df_test_total = df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].head(5).sum(axis=1)
    print(df_test_total)
    #单个的列
    df_total = df['Total'].head(5)
    print(df_total)
    #答案的写法(我没有直接的比较，只是输出来看了看)
    # (df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'
    #     ....:]].sum(1) != df['Total']).mean()
    # ....:
    #2.对于 # 重复的妖怪只保留第一条记录
    df_2 = df.drop_duplicates(['#'], keep='first')

    #a.求第一属性的种类数量和前三多数量对应的种类
    num = df_2['Type 1'].nunique()
    num_2 = df_2['Type 1'].value_counts().index[:3]#前三的索引

    #b.求第一属性和第二属性的组合种类
    num_team = df_2.drop_duplicates(['Type 1', 'Type 2'], keep='first')[['Type 1', 'Type 2']]

    #c.求尚未出现过的属性组合
    #解题的思路--是求出总的属性的组合与现在的做对比
    #但是想不起来用什么函数来实现比较高效
    all_type_list = [i+' '+j for i in df['Type 1'].unique() for j in df['Type 1'].unique()]
    #now_type_list = [i + j for i in df['Type 1'].unique() for j in df['Type 2'].unique()]
    # 看到答案才想起来，之前看dataWhale的python的书里的difference()函数来实现（太菜了）
    # res = set(all_type_list).difference(now_type_list)
    # print(res)
    #上面两个list的代码报错是----TypeError: can only concatenate str (not "float") to str
    #now_type_list前后的有的类型不一致
    #看答案的改进把空值替换掉
    #now_type_list = [i + j for i in df['Type 1'] for j in df['Type 2'].replace(np.nan, '')]
    #结果竟然是为空。。。。。
    #看了答案后加入了zip()函数打包为元组试试
    now_type_list = [i+' '+j for i, j in zip(df['Type 1'], df['Type 2'].replace(np.nan, ''))]
    res = set(all_type_list).difference(now_type_list)
    print(len(res))
    #成了

    #3.按照下述要求，构造 Series ：
    #a.取出物攻，超过120的替换为 high ，不足50的替换为 low ，否则设为 mid
    #思路，就是多个mask()的使用问题
    attack = df['Attack'].mask(df['Attack'] > 120, 'high').mask(df['Attack'] < 50, 'low').mask((df['Attack'] <= 120)&(df['Attack'] >= 50), 'mid').head()

    #b.取出第一属性，分别用 replace 和 apply 替换所有字母为大写
    #使用python自带的大小写变换函数Python upper()方法
    #先用replace
    look = df['Type 1'].replace({i: str.upper(i) for i in df['Type 1'].unique()}).head(10)
    #apply()用的是自定义的函数
    look2 = df['Type 1'].apply(lambda x: str.upper(x)).head()
    #c.求每个妖怪六项能力的离差，即所有能力中偏离中位数最大的值，添加到 df 并从大到小排序--quantile(0.5)中位数方法
    df['licha'] = df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].apply(lambda x: np.max((x-x.quantile(0.5)).abs()), axis=1)
    #再降序排列
    look3 = df.sort_values('licha', ascending=False).head(10)
    print(look3)


#Ex2：指数加权窗口
def exponentialweightingwindow():
    #指数加权平均算法
    #1.请用 expanding 窗口实现
    np.random.seed(0)
    s = pd.Series(np.random.randint(-1, 2, 30).cumsum())
    print( s.ewm(alpha=0.2).mean().head())
    #要自定义指数加权平均的函数方程
    def useFunction(x,alpha=0.2):
        # 需要求加权平均值的数据列表
        elements = list(x)
        #根据加权公式的思想，倒序一下需要计算的list
        elements = elements[::-1]
        # 对应的权值列表
        weights = [(1 - alpha) ** i for i in range(len(elements))]
        #
        res = np.average(elements, weights=weights)
        return res

    #使用
    look4 = s.expanding().apply(useFunction).head()
    print(look4)
    #2.作为滑动窗口的 ewm 窗口
    s.rolling(window=2).apply(useFunction).head()
#测试用
if __name__ == '__main__':
    #pokemon()
    exponentialweightingwindow()