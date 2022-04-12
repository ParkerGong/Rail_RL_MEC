import time
import numpy as np

ticks = time.time()
print("Now Time:", ticks)

class Train:
    '所有列车属性'
    totalCarNum = 0

    def __init__(self,trainNum,trainPlace,trainMEC,trainLevel,trainLoad,TrainMaxload):
        self.num = trainNum
        self.place = trainPlace
        self.MEC = trainMEC
        self.level = trainLevel
        self.load = trainLoad
        self.Maxload = TrainMaxload
        Train.totalCarNum += 1

# hasattr(emp1, 'age')    # 如果存在 'age' 属性返回 True。
# getattr(emp1, 'age')    # 返回 'age' 属性的值
# setattr(emp1, 'age', 8) # 添加属性 'age' 值为 8
# delattr(emp1, 'age')    # 删除属性 'age'

class MEC:
    'MEC属性'
    totalMECNum = 0

    def __init__(self,MECNum,MECPlace,MECConver,MECload,MECmaxload,MECorder):
        self.num = MECNum
        self.place = MECPlace
        self.coverage = MECConver
        self.load = MECload
        self.Maxload = MECmaxload
        self.order = MECorder #任务队列顺序
        MEC.totalMECNum += 1

class Track:
    '轨道属性'

    def __init__(self,TrackDis):
        self.trackDis = TrackDis


