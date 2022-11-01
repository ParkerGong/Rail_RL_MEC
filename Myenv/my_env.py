import numpy as np
from Myenv.core import World, Agent, MEC
from scenario import BaseScenario
import random


class Scenario(BaseScenario):

    def make_world(self):
        world = World()
        # set any world properties first

        Taskload = 1  # 这里要放到超参数里,一级任务和二级任务负载不同
        MECpower = 300  # MEC算力
        MECrange = 1200  # MEC覆盖范围
        Trainpower = 50  # 列车算力
        Trainspeed = 20  # 列车运行速度
        world.dim_p = 3  # 动作三维 本地算 服务器a算 服务器b算
        world.dim_c = 2  # ！！！！ communication channel dimensionality
        num_agents = 3  # 车的数量
        num_MECs = 3  # MEC数量
        taskmout0 = 20  # 一级任务量
        taskmout1 = 20  # 二级任务量
        world.collaborative = True

        # # add agents
        # world.agents = [Agent() for i in range(num_agents)]
        # for i, agent in enumerate(world.agents):
        #     agent.name = 'agent %d' % i
        #     agent.collide = True
        #     agent.silent = True
        #     agent.size = 0.15

        # add trains
        world.agents = [Agent() for i in range(num_agents)]
        for i, agent in enumerate(world.agents):
            agent.name = 'train %d' % i  # 编号
            agent.number = i
            agent.state.t_pos = 0 + 300 * i  # 位置
            # agents.MEC_cov = [] #MEC覆盖，这个要动态更新
            agent.state.level = 0  # 任务等级，0为正常状态，1为特殊情况需优先处理
            agent.state.trainspeed = Trainspeed  # 列车运行速度
            # agents.workload = 0 #当前负载
            agent.state.tMaxload = Trainpower  # 最大负载
            agent.state.MECcover = [0, 0]  # MEC覆盖，这个要动态更新
            agent.state.taskmount = taskmout0  # 当前任务量

        # add MECs
        world.mecs = [MEC() for i in range(num_MECs)]
        for i, mec in enumerate(world.mecs):
            mec.name = 'mec %d' % i  # 编号
            mec.number = i  # 编号
            mec.state.MEC_pos = 600 + 600 * i
            mec.state.MECMaxload = MECpower
            mec.state.MECload = 0
            mec.state.cover = MECrange

        world.mecs = World.MEC_randomload(world, seed=0, MEClist=world.mecs)

        # make initial conditions
        world = self.reset_world(world)
        return world

    def reset_world(self, world):

        for train_i in world.agents:
            # 列车恢复位置
            train_i.state.t_pos = 0 + 600 * train_i.number
            # 计算列车MEC属性
            train_i.state.MECcover = world.mecCover(train_i, world.mecs)
            # print(train_i.state.MECconver)

        # MEC恢复初始load
        world.mecs = World.MEC_randomload(world, seed=0, MEClist=world.mecs)  # 随机负载

        "生成随机入侵事件"
        world.agents = world.intrusion(0, world.agents)
        return world

        # # random properties for agents
        # for i, agent in enumerate(world.agents):
        #     agent.color = np.array([0.35, 0.35, 0.85])
        # # random properties for landmarks
        # for i, landmark in enumerate(world.landmarks):
        #     landmark.color = np.array([0.25, 0.25, 0.25])
        # set random initial states
        # for agent in world.agents:
        #     agent.state.p_pos = np.random.uniform(-1, +1, world.dim_p)
        #     agent.state.p_vel = np.zeros(world.dim_p)
        #     agent.state.c = np.zeros(world.dim_c)
        # for i, landmark in enumerate(world.landmarks):
        #     landmark.state.p_pos = np.random.uniform(-1, +1, world.dim_p)
        #     landmark.state.p_vel = np.zeros(world.dim_p)

    # def benchmark_data(self, agent, world):
    #     rew = 0
    #     collisions = 0
    #     occupied_landmarks = 0
    #     min_dists = 0
    #     for l in world.landmarks:
    #         dists = [np.sqrt(np.sum(np.square(a.state.p_pos - l.state.p_pos))) for a in world.agents]
    #         min_dists += min(dists)
    #         rew -= min(dists)
    #         if min(dists) < 0.1:
    #             occupied_landmarks += 1
    #     if agent.collide:
    #         for a in world.agents:
    #             if self.is_collision(a, agent):
    #                 rew -= 1
    #                 collisions += 1
    #     return (rew, collisions, min_dists, occupied_landmarks)

    # def is_collision(self, agent1, agent2):
    #     delta_pos = agent1.state.p_pos - agent2.state.p_pos
    #     dist = np.sqrt(np.sum(np.square(delta_pos)))
    #     dist_min = agent1.size + agent2.size
    #     return True if dist < dist_min else False

    def reward(self, agent, world):
        # Agents are rewarded based on computing time of all trains.
        rew = 0

        # # Agents are rewarded based on minimum agent distance to each landmark, penalized for collisions
        # rew = 0
        # for l in world.landmarks:
        #     dists = [np.sqrt(np.sum(np.square(a.state.p_pos - l.state.p_pos))) for a in world.agents]
        #     rew -= min(dists)
        # if agent.collide:
        #     for a in world.agents:
        #         if self.is_collision(a, agent):
        #             rew -= 1
        return rew

    def observation(self, agent, world):
        # mec覆盖范围

        mec_cover = agent.state.MECcover

        # 获取覆盖范围MEC位置、当前负载、最大负载
        mec_states = []
        for num in agent.state.MECcover:
            for mec in world.mecs:
                if mec.number == num:
                    # mec_states.append(world.mecs.state.MEC_pos) # MEC位置
                    mec_states.append(mec.state.MECload)  # 当前负载
                    mec_states.append(mec.state.MECMaxload)  # 最大负载

        # 自身任务等级、自身位置、负载、任务量
        train_states = []
        # train_states.append(agent.state.t_pos) #列车位置
        train_states.append(agent.state.level)  # 等级
        train_states.append(agent.state.tMaxload)  # 最大算力
        train_states.append(agent.state.taskmount)  # 任务量

        return (mec_cover + mec_states + train_states)

    def trainmove(self, world):
        # move train and refresh state of agent and mec
        for train_i in world.agents:
            if (train_i.state.t_pos + train_i.state.trainspeed) <= world.tracklen:
                # 位置移动后不超过轨道范围
                train_i.state.t_pos += train_i.state.trainspeed  # 列车向前移动
            elif (train_i.state.t_pos + train_i.state.trainspeed) >= world.tracklen:
                # 位置移动后超过轨道范围
                train_i.state.t_pos += train_i.state.trainspeed - world.tracklen  # 列车运行到第二圈 环形轨道
            "列车状态刷新"
            # 重新计算MECcover
            train_i.state.MECcover = world.mecCover(train_i, world.mecs)
            # 重新生成新的入侵事件
            world.agents = world.intrusion(0, world.agents)
