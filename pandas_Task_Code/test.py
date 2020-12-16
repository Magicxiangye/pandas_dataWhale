import pandas as pd


if __name__ == '__main__':
    data = pd.Series([1,2,3])
    #反向的为2的滑动窗口
    #先得出反向的shift(-1)的数据
    back_data= data.shift(-1)
    print(back_data)
    print(data + back_data)