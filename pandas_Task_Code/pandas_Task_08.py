import pandas as pd

# EX1:房屋信息数据集
def houseInfo():
    # 后缀是.xls的还是用xlrd读取
    df = pd.read_excel("data/house_info.xls", engine='xlrd', usecols=['floor','year','area','price'])

    # 1.将 year 列改为整数年份存储。
    # 是要把年份的其他多余的字符去掉吗
    df['year'] = df['year'].apply(lambda x: str(x).split('年建')[0])

    # 2.将 floor 列替换为 Level, Highest 两列，
    # 其中的元素分别为 string 类型的层类别（高层、中层、低层）与整数类型的最高层数。
    # 使用的是分组提取的命名子组
    pat_level = '(?P<level>\w+层)'
    df_level = df['floor'].str.extract(pat_level)
    pat_Highest = '(?P<Highest>\d)'
    df_highest = df['floor'].str.extract(pat_Highest)
    # 表的合并
    df = df.drop(columns=['floor'])
    df = pd.concat([df, df_level, df_highest], axis=1)

    # 3.计算房屋每平米的均价 avg_price ，以 ***元/平米 的格式存储到表中，其中 *** 为整数。
    # 还是没太懂，是每个房间单独的均价吗
    print(df.head())
    pat_int = '(\d+|\d+)'
    df_area = df['area'].str.extract(pat_int)
    df_price = df['price'].str.extract(pat_int)
    df_avg_price = pd.concat([df_price, df_area], axis=1)
    df_avg_price.columns = ['0', '1']
    avg_price = df_avg_price.apply(lambda x: (int(x[0])/int(x[1]))*10000, axis=1)
    # 平均的价格的Series
    avg_price = avg_price.astype(dtype=int)
    # 加入到原来的表格
    df['avg_price'] = avg_price.apply(lambda x: str(x) + '元/平米')
    print(avg_price.head())
    print(df.head())

# EX2 《权力的游戏》剧本数据集
def script():
    # 先读取文件
    df = pd.read_csv('data/script.csv')
    df_2 = pd.read_csv('data/script.csv')
    print(df.head())

    # 1.计算每一个Episode的台词条数。
    sentence_count = df['Sentence'].str.count('\.|\?|\!|\-')
    # df['sentence_count'] = sentence_count
    print(df.head())

    # 使用分组来进行统计，同时再排列顺序
    # print(sentence_count)
    # 2.以空格为单词的分割符号，请求出单句台词平均单词量最多的前五个人。
    word = df['Sentence'].str.count('\s')
    # print(word.head())
    # 计入到原表格，好进行分组
    df['word_count'] = word
    final_index = df.groupby('Name')['word_count'].sum()
    # 降序的排列，取前五个（升降序的设置ascending）
    final_index = pd.DataFrame(final_index).sort_values(by='word_count', ascending=False)
    print(final_index.head())

    # 3.若某人的台词中含有问号，那么下一个说台词的人即为回答者。
    # 若上一人台词中含有 n 个问号，则认为回答者回答了 n 个问题，请求出回答最多问题的前五个人。
    # 设置上一个人的台词问句的list
    question = df['Sentence'].str.count('\?').tolist()# 去掉最后，前面第一个人补零
    question.insert(0, 0)
    question.pop()
    # 再变为Series连接到原表格，进行操作
    question_s = pd.Series(question)
    df_2['question'] = question_s
    # 分组进行统计
    word_index = df_2.groupby('Name')['question'].sum()
    print(word_index)
    word_index = pd.DataFrame(word_index).sort_values(by='question', ascending=False)
    print(word_index.head())


#测试用
if __name__ == '__main__':
    script()