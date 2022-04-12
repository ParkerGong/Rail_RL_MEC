import matplotlib.pyplot

import basic
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation  # 动图的核心函数
import Main_env
import math
import random



"列车移动，距离控制"
def TrainMovement(train):
    train.place += 100

"MEC覆盖列车范围计算"
def mecCover(train,MEClist):
    trainMEC = []
    for MEC_ in MEClist:
        if train.place >= MEC_.place - MEC_.coverage/2 and train.place <= MEC_.place + MEC_.coverage/2:
            trainMEC.append(MEC_.num)

    return trainMEC

"随机生成入侵事件，将任务等级提升为1级"
def intrusion(seed,trainlist):
    n = random.randint(0,1)
    if n :
        i = random.randint(0,len(trainlist))
        trainlist[i].level = 1

"将任务等级恢复为2级"
def relief(trainlist):
    for train_i in trainlist:
        train_i.level =2
    return trainlist


"每个服务器生成随机负载"
def MEC_randomload(seed,MEClist):
    for MEC_i  in MEClist:
        MEC_i.load = MEC_i.Maxload * random.uniform(0.1,0.4)
    return MEClist

#TODO 需要增加MEC workload排序、计算每个任务的时间

def MEC_taskorder(MEClist):
    for MEC_i in MEClist:
        a = MEC_i.order
        idex = np.lexsort([a[:, 1], a[:, 0]])
        sorted_data = a[idex, :]
        MEC_i.order = sorted_data
    return MEClist








