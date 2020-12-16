import pandas as pd
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
    #答案的写法
    # (df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'
    #     ....:]].sum(1) != df['Total']).mean()
    # ....:
    #对于 # 重复的妖怪只保留第一条记录
    df_2 = df.drop_duplicates(['#'], keep='first')
    #求第一属性的种类数量和前三多数量对应的种类
    num = df_2['Type 1'].nunique()
    num_2 = df_2['Type 1'].value_counts().index[:3]#前三的索引
    print(num)
    print(num_2)


#测试用
if __name__ == '__main__':
    pokemon()