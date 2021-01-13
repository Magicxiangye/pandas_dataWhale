import pandas as pd
import numpy as np

# 最后的大作业

# EX1 显卡的信息问题
def RTX3080():
    # 先读取数据
    data_file = pd.read_csv('data/benchmark.txt', delimiter='\t')
    # print(data_file)
    # 先转换一下类型，方便操作
    df = pd.DataFrame(data_file)
    df.columns = ['record']
    # 过滤出有用的数据
    df = df[df['record'].apply(lambda x: 'Benchmarking' in x or 'model average' in x)]
    df = df.reset_index(drop='True')
    # 使用正则表达式提取
    pat = '(?P<模型名称>\w+model)(?P<状态>[_average_]\w+[_time_])(?P<时间>[:__]\w+\.\w{1,3})'
    df_data = df['record'].apply(lambda x: '_'.join(x.split(' ')))
    df_data = pd.DataFrame(df_data)
    # 提取一下数据类型
    type_pat = '(?P<type>\w+\_precision)(?P<other>\w+)'
    type_data = df_data['record'].str.extract(type_pat).dropna()
    type_data['type'] = type_data['type'].apply(lambda x: str(x).split('_')[2])
    type_data = type_data.reset_index(drop='True')
    final_data = df_data['record'].str.extract(pat).dropna()
    # 笨方法，提纯
    final_data['模型名称'] = final_data['模型名称'].apply(lambda x: str(x).split('__')[0])
    final_data['状态'] = final_data['状态'].apply(lambda x: str(x).split('_')[2])
    final_data['时间'] = final_data['时间'].apply(lambda x: str(x).split('_')[2])
    final_data = final_data.reset_index(drop='True')
    final_data['type'] = type_data['type']
    # 合并一下数据
    final_data['type_2'] = final_data['状态'] + '_' + final_data['type']
    # 删除不必要的
    final_data = final_data.drop(labels='状态', axis=1)
    final_data = final_data.drop(labels='type', axis=1)
    # 使用长宽表的变换来达到效果
    final_lable = final_data.pivot(index='模型名称', columns='type_2', values='时间')
    final_lable.columns.names = [' ']
    final_lable.index.names = [' ']
    # 最后输出结果
    print(final_lable)

# Ex2:水压站点的特征工程
def waterFac():
    # df1和df2中分别给出了18年和19年各个站点的数据，
    # 其中列中的H0至H23分别代表当天0点至23点；
    # df3中记录了18-19年的每日该地区的天气情况，请完成如下的任务：
    df1 = pd.read_csv('data/yali18.csv')
    df2 = pd.read_csv('data/yali19.csv')
    df3 = pd.read_csv('data/qx1819.csv')

    # 通过df1和df2构造df，把时间设为索引，第一列为站点编号，
    # 第二列为对应时刻的压力大小，排列方式如下（压力数值请用正确的值替换）：
    df1_melt = df1.melt(id_vars=['MeasName', 'Time'],
                        value_vars=['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12',
                                    'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20', 'H21', 'H22', 'H23'],
                        value_name='压力', var_name='Hours')
    # 设置合并为时间戳
    df1_melt['Hours'] = df1_melt['Hours'].apply(lambda x: x.split('H')[1])
    df1_melt['Hours'] = df1_melt['Hours'].apply(lambda x: '{}:00:00'.format(x))
    df1_melt['time'] = df1_melt['Time']+ '-' + df1_melt['Hours']
    df1_melt = df1_melt.drop(labels='Time', axis=1)
    df1_melt = df1_melt.drop(labels='Hours', axis=1)
    df1_melt.set_index('time', inplace=True)
    df1_melt.index.names = ['']
    # 第二张表同理
    df2_melt = df2.melt(id_vars=['MeasName', 'Time'],
                        value_vars=['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12',
                                    'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20', 'H21', 'H22', 'H23'],
                        value_name='压力', var_name='Hours')
    df2_melt['Hours'] = df2_melt['Hours'].apply(lambda x: x.split('H')[1])
    df2_melt['Hours'] = df2_melt['Hours'].apply(lambda x: '{}:00:00'.format(x))
    df2_melt['time'] = df2_melt['Time'] + '-' + df2_melt['Hours']
    df2_melt = df2_melt.drop(labels='Time', axis=1)
    df2_melt = df2_melt.drop(labels='Hours', axis=1)
    df2_melt.set_index('time', inplace=True)
    df2_melt.index.names = ['']
    # 两表合并(行合并)
    df = pd.concat([df1_melt,df2_melt], axis=0)
    print(df)
    # 下面写不完了，太菜了，先打卡
if __name__ == '__main__':
    waterFac()