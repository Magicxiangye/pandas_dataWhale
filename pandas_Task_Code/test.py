import pandas as pd
import numpy as np
from numpy import number

if __name__ == '__main__':
    # s = pd.Series(['上海市黄浦区方浜中路249号','上海市宝山区密山路5号','北京市昌平区北农路2号'])
    # # 设置分组的条件的正则表达式
    # pat = '(\w+市)(\w+区)(\w+路)(\d+号)'
    # # 给替换的自定义函数添加字典来进行替换
    # city = {'上海市': 'Shanghai', '北京市': 'Beijing'}
    # district = {'昌平区': 'CP District', '黄浦区': 'HP District', '宝山区': 'BS District'}
    # road = {'方浜中路': 'Mid Fangbin Road', '密山路': 'Mishan Road', '北农路': 'Beinong Road'}
    # # 自定义的替换函数
    # def my_func(m):
    #     # 在相应的正则表达式的基础上来进行替换
    #     str_city = city[m.group(1)]
    #     str_district = district[m.group(2)]
    #     str_road = road[m.group(3)]
    #     str_no = 'No. ' + m.group(4)[:-1]
    #     return ' '.join([str_city, str_district, str_road, str_no])
    #
    str = 'Benchmarking_Training_float_precision'
    test = str.split('_')
    print(test)