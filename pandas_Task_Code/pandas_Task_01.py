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
    #当个的sum()只能给list用
    B = np.array([sum(A[i][j] * (1/A[i, :])) for i in range(A.shape[0]) for j in range(A.shape[1])]).reshape(A.shape[0], A.shape[1])
    print(B)
#Ex3卡方统计量
def x2():
    pass
#测试方法用
if __name__ == '__main__':
    #self_matmul()
    #A = np.arange(1,10).reshape(3, -1)
    new_matrix()
