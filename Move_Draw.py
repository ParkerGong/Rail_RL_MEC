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

"随机生成入侵事件，将任务等级提升为2级"
def intrusion(seed,trainlist):
    n = random.randint(0,1)
    if n :
        i = random.randint(0,len(trainlist))
        trainlist[i].level = 2

"将任务等级恢复为1级"
def relief(seed,trainlist):
    for train_i in trainlist:
        train_i.level =1


