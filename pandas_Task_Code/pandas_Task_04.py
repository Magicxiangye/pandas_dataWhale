import pandas as pd
import numpy as np

def car():
    df = pd.read_csv('data/car.csv')
    #1.先过滤出所属 Country 数超过2个的汽车，
    # 即若该汽车的 Country 在总体数据集中出现次数不超过2则剔除，(一个城市少于两台车的剔除？？)
    # 再按 Country 分组计算价格均值、价格变异系数、该 Country 的汽车数量，
    # 其中变异系数的计算方法是标准差除以均值，并在结果中把变异系数重命名为 CoV 。
    #print(df.head())
    gb = df.groupby('Country')
    res = gb.filter(lambda x: x.shape[0] > 2)
    #print(res)
    #聚合函数的使用
    final = res.groupby('Country')['Price'].agg([ 'mean', 'count', ('Cov',lambda x: x.std() / x.mean() )])#使用多个的内置聚合函数
    #print(final)
    #2.按照表中位置的前三分之一、中间三分之一和后三分之一分组，统计 Price 的均值。
    #没太想到的很好的方法
    #看了答案之后，才想到可以在分组的条件依据上使用一个列表
    #car.csv的shape[0]为60
    #所以分组依据的条件是
    condition = ['head'] * 20 + ['Mid'] * 20 + ['Tail'] * 20
    print(df.groupby(condition)['Price'].mean())
    #3.对类型 Type 分组，对 Price 和 HP 分别计算最大值和最小值，
    # 结果会产生多级索引，请用下划线把多级列索引合并为单层索引。
    res_2 = df.groupby('Type')[['Price', 'HP']].agg({'Price': ['max', 'min'], 'HP': ['max', 'min']})
    #列索引的组合（columns.map来使用）
    new_columns = res_2.columns.map(lambda x: (x[0] + '-' + x[1]))
    # 设置为新的index
    res_2.columns = new_columns
    #print(res_2)
    #4.对类型 Type 分组，对 HP 进行组内的 min-max 归一化。
    #min-max归一化的处理函数
    def normalize(s):
        s_min, s_max = s.min(), s.max()
        res = (s - s_min) / (s_max - s_min)
        return res
    #组内的变形（肯定用的是transform()）
    res_3 = df.groupby('Type')['HP'].transform(normalize).head()
    #print(res_3)
    #5.对类型 Type 分组，计算 Disp. 与 HP 的相关系数。(相关系数的函数用到是npcorrcoef)
    #np.corrcoef() 接受的参数是一个矩阵,返回的结果也是一个矩阵
    #,返回的矩阵结果 r[i][j] 分别为第 i 组数据和第 j 组数据的皮尔逊积矩相关系数:
    #这里只有两组，第0组和第1组——————所以[0, 1]提取的就是
    #第 [0] 组数组和第 [1] 组数据的相关系数,也就是 Disp.和 HP,的结果
    res_4 = df.groupby('Type')[['Disp.', 'HP']].apply(lambda x: np.corrcoef(x['Disp.'].values, x['HP'].values)[0, 1])
    print(res_4)


#Ex2：实现transform函数
#理解答案的代码
def my_group():
    class my_groupby:
        def __init__(self, my_df, group_cols):
            #copy一份传入的文档
            self.my_df = my_df.copy()
            #返回用于分组的列索引的值的无重复的组合
            self.groups = my_df[group_cols].drop_duplicates()
            #查看是否是一维的Series（isinstance()类型判断的函数）
            if isinstance(self.groups, pd.Series):
                #当分组的依据是一列的情况
                self.groups = self.groups.to_frame()#将得到的Series转化为DataFrame
            self.group_cols = self.groups.columns.tolist()#输出分组用的列的索引
            #变为列索引名，与列索引的值相对应的key：value组合
            self.groups = {i: self.groups[i].values.tolist() for i in self.groups.columns}
            #初始化时要转换的列时为空的先设定为空
            self.transform_col = None

        #实例对象（假设为P）就可以这样P[key]取值
        def __getitem__(self, col):
            #这个时获取数据来源的list,要判断一下是否是进行类型的转换
            self.pr_col = [col] if isinstance(col, str) else list(col)
            return self

        def transform(self, my_func):
            #参数my_func是传入的函数方法
            #用于分组的列的值的长度（每列是等长的）
            self.num = len(self.groups[self.group_cols[0]])
            #保存索引和值的list（两个）
            L_order, L_value = np.array([]), np.array([])
            for i in range(self.num):
                group_df = self.my_df.reset_index().copy()
                for col in self.group_cols:
                    #这里有点没看懂，为啥要这样判断
                    group_df = group_df[group_df[col] == self.groups[col][i]]

                group_df = group_df[self.pr_col]

                if group_df.shape[1] == 1:
                    #一列的情况
                    group_df = group_df.iloc[:, 0]
                group_res = my_func(group_df)

                if not isinstance(group_res, pd.Series):
                    group_res = pd.Series(group_res,index = group_df.index, name = group_df.name)
                L_order = np.r_[L_order, group_res.index]
                L_value = np.r_[L_value, group_res.values]
            self.res = pd.Series(pd.Series(L_value, index=L_order).sort_index().values, index = self.my_df.reset_index().index, name = my_func.__name__)
            return self.res

#测试代码用
if __name__ == '__main__':
    car()