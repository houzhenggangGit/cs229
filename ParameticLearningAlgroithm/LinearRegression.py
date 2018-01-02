# -*- coding: UTF-8 -*-
'''
@author: Arron
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: hou.zg@foxmail.com
@software: import
@file: LinearRegression.py
@time: 2017/12/30 0030 18:28

'''
import numpy as np
import ParameticLearningAlgroithm.dataSource as pd
from sklearn.metrics import mean_squared_error, explained_variance_score
import threading
import matplotlib.pyplot as plt

# pd.features=pd.features[:2]
data = pd.Data(pd.features, pd.target)
numData = len(data.target)
numTraining = int(0.8 * numData)
# 设置x0=1
data.features = np.concatenate([np.ones((1, numData)), data.features.transpose()]).transpose()
numFeatures = len(data.features[0])
trainData = pd.Data(data.features[:numTraining], data.target[:numTraining])
testData = pd.Data(data.features[numTraining:], data.target[numTraining:])


def h(para, x):
    return np.dot(para, x.transpose())


def err(y, para, x):
    return y - h(para, x)


def J(para, features, target):
    return np.sum(0.5 * (h(para, features) - target) ** 2)


# 线性拟合参数
para = np.array(
    [
        1.3214220306038311, -0.20304558588265248, 0.05693956317367194, 0.02509018017571224, 1.3194373897155887,
        1.1377092339032775, 4.743510947291082, 0.015085507885354885, -0.8501607212053596, 0.3084392761925037,
        -0.012203003090160345, -0.34927154335424127, 0.023990219726218, -0.5880728451024222])
# para=np.ones(numFeatures)
# 步长
step = 0.00000001
errorJ = 10000
accept = 1


def run(step, errorJ, accept):
    k = 0
    while errorJ >= accept:
        k += 1
        if k == 100:
            print('errorJ', errorJ)
            print(para.tolist())
            k = 0
        for i in range(numTraining):
            # print('errorJ', errorJ)
            for j in range(numFeatures):
                # print('(i,j)', i, j)
                errorJ = J(para, trainData.features, trainData.target)
                para[j] = para[j] + step * np.dot(err(trainData.target, para, trainData.features),
                                                  trainData.features[:, j])


for i in range(64):
    t = threading.Thread(target=run, args=(0.00000001, 10000, 0.0000000001))
    t.start()
print(para.tolist())
mse = mean_squared_error(testData.target, h(para, testData.features))
evs = explained_variance_score(testData.target, h(para, testData.features))
print("Mean squared error =", round(mse, 2))
print("Explained variance score =", round(evs, 2))
