import argparse

import numpy as np
from Myenv.my_env import Scenario




# def sortdata():
#     "创建MEC对象,编号、位置、覆盖范围、负载,最大负载、"
#     MEC0 = basic.MEC(0, 0, 800, 200, 1000, np.array([[1,50,3],[1,43,4],[2,60,5],[2,11,6]]))
#     a = MEC0.order
#     idex=np.lexsort([a[:,1], a[:,0]])
#     sorted_data = a[idex, :]
#     print(sorted_data)

def main(enviroment=None):
    # parser = argparse.ArgumentParser()
    # # Environment
    # parser.add_argument(
    #     '--env',
    #     type=str,
    #     default='simple_spread',
    #     help='scenario of MultiAgentEnv')
    # parser.add_argument(
    #     '--max_step_per_episode',
    #     type=int,
    #     default=50,
    #     help='maximum step per episode')
    # parser.add_argument(
    #     '--max_episodes',
    #     type=int,
    #     default=25000,
    #     help='stop condition:number of episodes')
    # parser.add_argument(
    #     '--stat_rate',
    #     type=int,
    #     default=500,  # 第1000episodes保存一下，并显示reward值。
    #     help='statistical interval of save model or count reward')
    # # Core training parameters
    # parser.add_argument(
    #     '--critic_lr',
    #     type=float,
    #     default=1e-3,
    #     help='learning rate for the critic model')
    # parser.add_argument(
    #     '--actor_lr',
    #     type=float,
    #     default=1e-3,  ##修改 default值可修改学习率
    #     help='learning rate of the actor model')
    # parser.add_argument(
    #     '--gamma', type=float, default=0.95, help='discount factor')
    # parser.add_argument(
    #     '--batch_size',
    #     type=int,
    #     default=1024,
    #     help='number of episodes to optimize at the same time')
    # parser.add_argument('--tau', type=int, default=0.01, help='soft update')
    # # auto save model, optional restore model
    # parser.add_argument(
    #     '--show', action='store_true', default=False, help='display or not')  # TRUE表示显示渲染
    # parser.add_argument(
    #     '--restore',
    #     action='store_true',
    #     default=False,
    #     help='restore or not, must have model_dir')
    # parser.add_argument(
    #     '--model_dir',
    #     type=str,
    #
    #     default='./model',
    #     help='directory for saving model')
    #
    # args = parser.parse_args()
    env = Scenario()

    world = env.make_world()

    for agent in world.agents:
        obv = env.observation(agent, world)





if __name__ == "__main__":
    main()


