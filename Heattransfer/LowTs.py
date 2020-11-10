import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append(...)

sample = pd.read_excel(
    '핀 작업용 데이터셋.xlsx', header=1, usecols='B: D')
print(sample['pin length'][0])
X = np.zeros((len(sample['pin length']), 2))
X[:, 0] = sample['pin diameter']
X[:, 1] = sample['pin length']
Y = np.zeros((len(sample['pin length']), 1))
Y[:, 0] = sample['MaxTemp']
X_mean, Y_mean = np.mean(X, axis=0), np.mean(Y, axis=0)
X_std, Y_std = np.std(X, axis=0), np.std(Y, axis=0)
X, Y = (X-X_mean)/X_std, (Y-Y_mean)/Y_std


m, n = X.shape
X = np.column_stack((np.ones(m), X))


def computeCost(X, Y, theta):
    m = len(Y)
    J = 0
    h = X.dot(theta)
    error = h-Y
    sqerror = error**2
    J = 1.0/(2.0*m)*np.sum(sqerror)

    return J


def gradientdescent(X, Y, theta, lr, iters):
    m = len(Y)
    J_list = []
    for _ in range(iters):
        h = X.dot(theta)
        error = h-Y
        delta = (1.0/m)*np.dot(X.T, error)
        theta -= lr*delta
        J_list.append(computeCost(X, Y, theta))

    return theta, J_list


theta = np.zeros((3, 1))
lr = 0.03  # * 여러개 해보기
iters = 400
theta, J_list = gradientdescent(X, Y, theta, lr, iters)
print(theta)

# * 일단 ansys결과랑 비교하기
