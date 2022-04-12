import numpy as np
import basic
import Move_Draw
import Main_env
import rl



def sortdata():
    "创建MEC对象,编号、位置、覆盖范围、负载,最大负载、"
    MEC0 = basic.MEC(0, 0, 800, 200, 1000, np.array([[1,50,3],[1,43,4],[2,60,5],[2,11,6]]))
    a = MEC0.order
    idex=np.lexsort([a[:,1], a[:,0]])
    sorted_data = a[idex, :]
    print(sorted_data)

def main(enviroment=None):
    enviroment = Main_env.TrainEnv
    track, trainList, MECList = enviroment.init(enviroment)

    for j in MECList:
        print(j.load)

    # aciton[列车算/MEC算，原MEC编号，任务比例、helper编号、任务比例]
    action = [1,0,0.2,1,0.5]
    track_, trainList_, MECList_, Reward_ = enviroment.env(enviroment, track, trainList, MECList, action)


    # for i in trainList:
    #     print(i.level)


if __name__ == "__main__":
    main()


