import basic
import Move_Draw
import pyglet


class TrainEnv(object):
    Taskload = 1  # 这里要放到超参数里,一级任务和二级任务负载不同
    MECpower = 300  # MEC算力
    Trainpower = 50  # 列车算力
    state_dim = 1  # 状态空间
    action_dim = 4  # 动作空间

    "初始化环境"

    def init(self):
        "创建轨道对象"
        track = basic.Track(2000)  # 长度2000米

        "创建列车对象"
        train0 = basic.Train(1, 2000, [], 1, 0, 100)
        train1 = basic.Train(1, 1800, [], 1, 0, 100)
        train2 = basic.Train(2, 1500, [], 1, 0, 100)
        train3 = basic.Train(3, 1200, [], 1, 0, 100)
        train4 = basic.Train(4, 800, [], 1, 0, 100)
        train5 = basic.Train(5, 700, [], 1, 0, 100)
        train6 = basic.Train(6, 600, [], 1, 0, 100)
        train7 = basic.Train(7, 500, [], 1, 0, 100)
        train8 = basic.Train(8, 300, [], 1, 0, 100)
        train9 = basic.Train(9, 100, [], 1, 0, 100)

        trainList = [train0, train1, train2, train3, train4, train5, train6, train7, train8, train9]

        "创建MEC对象,编号、位置、覆盖范围、负载,最大负载"
        MEC0 = basic.MEC(0, 0, 800, 200, 1000)
        MEC1 = basic.MEC(1, 600, 800, 200, 1000)
        MEC2 = basic.MEC(2, 1200, 800, 200, 1000)
        MEC3 = basic.MEC(3, 1800, 800, 200, 1000)

        MECList = [MEC0, MEC1, MEC2, MEC3]

        "计算列车MEC属性"
        for train_i in trainList:
            train_i.MEC = Move_Draw.mecCover(train_i, MECList)
            # print(train_i.MEC)
        "给MEC随机负载"
        MECList = Move_Draw.MEC_randomload(0,MECList)


        return track, trainList, MECList

    "交互环境"
    def env(self, track, trainList, MECList, action):
        "执行action"

        # aciton[列车算/MEC算，原MEC编号，任务比例、helper编号、任务比例]
        "列车资源更新"
        if action[0] == 0:
            for train_i in trainList:
                train_i.load += TrainEnv.Taskload


        elif action[0] == 1:
            "MEC资源更新"
            for MEC_i in MECList:
                if MEC_i.num == action[2]:
                    MEC_i.load += action[3] * TrainEnv.Taskload  # Taskload作为每个任务的超参数，乘上负载比例
                if MEC_i.num == action[4]:
                    MEC_i.load += action[5] * TrainEnv.Taskload  # Taskload作为每个任务的超参数，乘上负载比例


        "计算当前收获，reward"
        "当前思路：超过计算容量的就变成惩罚项"

        "判断列车计算资源是否超载、计算奖励"
        OverflowData_t = []

        for train_i in trainList:
            if train_i.load > train_i.Maxload:
                i = train_i.num
                OverflowData_t[i] = train_i.Maxload - train_i.load  # 溢出量
                train_i.load = train_i.Maxload
                train_i.load -= TrainEnv.Trainpower
                # 惩罚项在这儿
                Reward_t = 0 #TODO 奖励、惩罚还没做，考虑溢出数据为惩罚，计算时间也为惩罚
            else:
                train_i.load -= TrainEnv.Trainpower  # 每个周期计算掉的容量
                # 奖励项在这儿
                Reward_t = 0

        "判断MEC资源情况、计算奖励"
        OverflowData_m = []
        for MEC_i in MECList:
            if MEC_i.load > MEC_i.Maxload:
                j = MEC_i.num
                OverflowData_m[j] = MEC_i.Maxload - MEC_i.load  # 溢出量
                MEC_i.load = MEC_i.Maxload
                MEC_i.load -= TrainEnv.MECpower
                # 惩罚项在此
                Reward_M = 0
            else:
                MEC_i.load -= TrainEnv.MECpower  # 每个周期计算掉的容量
                # 奖励项在这儿
                Reward_M = 0
        Reward = Reward_M + Reward_t  # 总奖励值


        "状态转移到下一状态"
        "恢复所有入侵事件"
        trainList = Move_Draw.relief(trainList)
        "生成MEC随机负载"
        MECList = Move_Draw.MEC_randomload(0,MECList)


        '列车移动并更新属性'
        for train_i in trainList:
            # 列车移动
            Move_Draw.TrainMovement(train_i)
            # 更新每辆车的MEC coverage
            MEC_train_i = Move_Draw.mecCover(train_i, MECList)
            train_i.MEC = MEC_train_i

        "生成随机入侵事件"
        trainList = Move_Draw.intrusion(trainList)

        return track, trainList, MECList, Reward
