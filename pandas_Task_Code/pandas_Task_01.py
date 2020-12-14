import numpy as np

#Ex1:利用列表推导式写矩阵乘法
def self_matmul():
    M1 = np.random.rand(2,3)
    M2 = np.random.rand(3,4)
    #结果矩阵
    res = np.empty((M1.shape[0],M2.shape[1]))
    #列表推导式
    res = res + np.array([sum(M1[i, :] * M2[:, j]) for i in range(M1.shape[0]) for j in range(M2.shape[1])]).reshape(M1.shape[0],M2.shape[1])
    result = M1@M2
    #误差的判断
    bool = ((M1 @ M2 - res) < 1e-15).all()
    print(res)
    print(result)
    print(bool)

#Ex2:更新矩阵
def new_matrix():
    #由于被调用数组的大小是确定的， reshape允许有一个维度存在空缺，此时只需填充 - 1
    #用指定的公式来更新矩阵
    #用于更新的矩阵
    A = np.arange(1,10).reshape(3,-1)
    print(A)
    #注意np.sum()与单个的sum()的不同只能给list用
    B = np.array([sum(A[i][j] * (1/A[i, :])) for i in range(A.shape[0]) for j in range(A.shape[1])]).reshape(A.shape[0], A.shape[1])
    print(B)

#Ex3卡方统计量
#跟着公式一步步的计算就可以
def x2():
    #固定的随机数
    np.random.seed(0)
    A = np.random.randint(10, 20, (8, 5))
    #先算期望值B(根据公式求解即可)(sum(0):列，sun(1):行)
    B = A.sum(0) * A.sum(1).reshape(-1, 1) / A.sum()
    result = ((A - B) ** 2 / B).sum()
    print(result)

#Ex4改进矩阵的计算性能
def computePerformance():
    np.random.seed(0)
    m, n, p = 100, 80, 50
    #定义三个矩阵
    B = np.random.randint(0, 2, (m, p))
    U = np.random.randint(0, 2, (p, n))
    Z = np.random.randint(0, 2, (m, n))
    #第一眼看到题目的时候，就想用的使列表的推导式(太菜了。。。。)(都说要发挥numpy的特性了)
    #这样写的时间复杂度也应该会很高
    res = [(((B[i]-U[:, j])**2).sum()) * Z[i][j] for i in range(m) for j in range(n)]
    #在答案的改进方法中，将矩阵的运算变为构造一个新的矩阵后的乘法
    #矩阵的对应元素相乘的求和，在 Numpy 中可以用逐元素的乘法后求和实现
    #变为如何构造一个新的矩阵来实现新的运算
    real_res = (((B**2).sum(1).reshape(-1,1) + (U**2).sum(0) - 2*B@U)*Z).sum()
    final = sum(res)
    print(final)

#Ex5：连续整数的最大长度
def maxint_len():
    #输入一个整数的 Numpy 数组，返回其中递增连续整数子数组的最大长度
    #使用提示的函数---diff()和nonzeros()的组合使用来快速的获取答案
    list = np.array([1,2,5,6,7])
    #先得出一个非负个数的list
    list2 = np.diff(list)
    #合并list，diff()中前后差不唯一的保留（nonzero后返回不为零的位数的索引）
    nonzero_list = np.nonzero(np.r_[1, list2 != 1, 1])
    #判断最大的长度
    #最后索引相减得出连续递增的最大长度
    max_len = np.diff(nonzero_list).max()
    print(max_len)



#测试方法用
if __name__ == '__main__':
    #self_matmul()
    #A = np.arange(1,10).reshape(3, -1)
    #new_matrix()
    #x2()
    #computePerformance()
    # x = np.array([1,2,5,6,7])
    # print(x)
    # print(np.diff(x))
    # y = np.r_[1, np.diff(x) != 1, 1]
    # print(y)
    # print(np.nonzero(y))
    maxint_len()

