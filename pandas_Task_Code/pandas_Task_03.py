import pandas as pd
#Task_03_Code

#Ex1：公司员工数据集
def company():
    df = pd.read_csv('data/Company.csv')
    #1.分别只使用 query 和 loc 选出年龄不超过四十岁且工作部门为 Dairy 或 Bakery 的男性。
    #先使用的是query方法
    df.query("(age <= 40)&(department == ['Dairy', 'Bakery'])&(gender=='M')").head()
    #使用loc方法
    df.loc[(df.age <=40)&(df.department.isin(['Dairy', 'Bakery'])&(df.gender == 'M'))].head()
    #2.选出员工 ID 号 为奇数所在行的第1、第3和倒数第2列。
    #解题思路，要同时定位行和列（.iloc[]方法）
    df.iloc[(df.EmployeeID %2 == 1).value, [0,2,-2]].head()
    #3.按照以下步骤进行索引操作
    #把后三列设为索引后交换内外两层
    df_2 = df.copy()
    df_new = df_2.set_index(['department', 'job_title', 'gender'])
    df_new.swaplevel(0,2,axis=1).head()
    #恢复中间那一层
    df_new.reset_index('job_title')
    #修改外层索引名为 Gender
    df_new.rename(index={'gender': 'Gender'},level=0).head()
    #用下划线合并两层行索引
    #`map()` 的另一个重要的使用方法是**对多级索引的压缩**，
    new_index = df_new.index.map(lambda x:(x[0]+'-'+ x[1]))
    #设置为新的index
    df_new.index = new_index
    #把行索引拆分为原状态
    #还是使用map()
    reset_index = df_new.index.map(lambda x: tuple(x.split('-')))
    df_new.index = reset_index
    #修改索引名为原表名称
    #恢复默认索引并将列保持为原表的相对位置
    df_new.reindex_like(df)

#EX2:巧克力数据集
def chocolate():
    df = pd.read_csv('data/chocolate.csv')
    #把列索引名中的 \n 替换为空格
    reset_index = df.index.map(lambda x: ' '.join(x.split('\n')))
    df.index = reset_index
    #巧克力 Rating 评分为1至5，每0.25分一档，请选出2.75分及以下且可可含量 Cocoa Percent 高于中位数的样本。
    #x[:-1]切片去掉百分号
    df['Cocoa Percent'] = df['Cocoa Percent'].apply(lambda x: float(x[:-1]) / 100).head()
    #选符合条件的使用的是query方法
    df.query("(Rating <= 2.75)&('Cocoa Percent' > 'Cocoa Percent'.median())").head()
    #将 Review Date 和 Company Location 设为索引后，选出 Review Date
    # 在2012年之后且 Company Location 不属于 France, Canada, Amsterdam, Belgium 的样本。
    df.set_index(['Review Date', 'Company Location'])
    #选出 Review Date在2012年之后
    #多层索引的选择IndexSlice
    idx = pd.IndexSlice
    df.loc[idx[2012:,~df.index.get_level_values(1).isin(['France', 'Canada', 'Amsterdam', 'Belgium'])],:].head(3)

#测试用
if __name__ == '__main__':
    #company()
    #chocolate()
    df = pd.read_csv('data/chocolate.csv')
    df['Cocoa Percent'] = df['Cocoa Percent'].apply(lambda x: print(x[:-1]))
    print(df.head())