import numpy as np
import random


# physical/external base state of all entites
# class EntityState(object):
#     def __init__(self):
#         # physical position
#         self.p_pos = None
#         # # physical velocity
#         # self.p_vel = None

# state of agents (including communication and internal/mental state)
class AgentState(object):
    def __init__(self):
        # super(AgentState, self).__init__()
        # train position
        self.t_pos = 0
        # communication utterance
        self.c = None
        # train property 列车就是agent
        # 当前列车等级
        self.level = 0
        # #当前列车负载
        # self.load = 0
        # 最大负载
        self.tMaxload = 0
        # MEC coverage [编号，编号]
        self.MECcover = []
        # 列车运行速度
        self.trainspeed = 0
        # 任务大小
        self.taskmount = 0


# state of agents (including communication and internal/mental state)
class MECState(object):
    def __init__(self):
        # physical position
        self.MEC_pos = None
        # communication utterance
        self.c = None
        # MEC覆盖范围
        self.cover = 0
        # 当前MEC负载
        self.MECload = 0
        # 最大负载
        self.MECMaxload = 0


# action of the agent
class Action(object):
    def __init__(self):
        # # physical action
        # self.u = None
        # communication action
        self.c = None
        # offloading action
        self.offload = None


# properties and state of physical world entity
class Entity(object):
    def __init__(self):
        # name 
        self.name = ''


# properties of agent entities
class Agent(Entity):
    def __init__(self):
        # agent number
        super(Agent, self).__init__()
        self.number = None
        # state
        self.state = AgentState()
        # action
        self.action = Action()
        # script behavior to execute
        self.action_callback = None
        # movable
        self.movable = True


# properties of MEC entities
class MEC(Entity):
    def __init__(self):
        # number of MEC
        super().__init__()
        self.number = 0
        # state
        self.state = MECState()


# multi-agent world
class World(object):
    def __init__(self):
        # list of agents and entities (can change at execution-time!)
        self.agents = []
        self.mecs = []

        # communication channel dimensionality
        self.dim_c = 0
        # position dimensionality
        self.dim_p = 2
        # action dimensionality
        self.dim_act = 3

        # track length
        self.tracklen = 1800

        # # color dimensionality
        # self.dim_color = 3
        # simulation timestep
        self.dt = 0.1
        # # physical damping
        # self.damping = 0.25

        # contact response parameters
        self.contact_force = 1e+2
        self.contact_margin = 1e-3

        self.taskmount0 = 20
        self.taskmount1 = 30

    # return all entities in the world
    @property
    def entities(self):
        return self.agents + self.mecs

    # return all agents controllable by external policies
    @property
    def policy_agents(self):
        return [agent for agent in self.agents if agent.action_callback is None]

    # return all agents controlled by world scripts
    @property
    def scripted_agents(self):
        return [agent for agent in self.agents if agent.action_callback is not None]

    "每个服务器生成随机负载"

    def MEC_randomload(self, seed, MEClist):
        for MEC_i in MEClist:
            MEC_i.state.MECload = MEC_i.state.MECMaxload * random.uniform(0.1, 0.4)
        return MEClist

    "列车计算MEC范围"

    def mecCover(self, t, MEClist):
        trainMEC = []
        if t.state.t_pos < 600:
            # 在0位置时同时也能被环线上最后一个服务器覆盖
            trainMEC.append(MEClist[-1].number) #MEC2
        for MEC_ in MEClist:
            if MEC_.state.MEC_pos - (MEC_.state.cover / 2) <= t.state.t_pos < MEC_.state.MEC_pos + (MEC_.state.cover / 2) :
                trainMEC.append(MEC_.number)
        # print(trainMEC)
        return trainMEC

    "随机生成入侵事件，将任务等级提升为1级"

    def number_of_certain_probability(self, sequence, probability):
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for item, item_probability in zip(sequence, probability):
            cumulative_probability += item_probability
            if x < cumulative_probability:
                break
        return item

    def intrusion(self, seed, trainlist, world):
        value_list = [0, 1]
        probability = [0.9, 0.1]
        for i in range(len(trainlist)):
            result = self.number_of_certain_probability(value_list, probability)
            trainlist[i].state.level = result
            trainlist[i].state.taskmount = world.taskmount0 + result * world.taskmount1 # result == 0 则只有语义分割， == 1 则有两部分任务
        return trainlist

    # update state of the world
    def step(self):
        # # set actions for scripted agents
        # for agent in self.scripted_agents:
        #     agent.action = agent.action_callback(agent, self)
        # # gather forces applied to entities
        # p_force = [None] * len(self.entities)
        # # apply agent physical controls
        # p_force = self.apply_action_force(p_force)
        # # apply environment forces
        # p_force = self.apply_environment_force(p_force)
        # # integrate physical state
        # self.integrate_state(p_force)

        # update agent state
        for agent in self.agents:
            self.update_agent_state(agent)
        # update mec state
        self.update_mec_state(self)

    # # gather agent action forces
    # def apply_action_force(self, p_force):
    #     # set applied forces
    #     for i, agent in enumerate(self.agents):
    #         if agent.movable:
    #             noise = np.random.randn(*agent.action.u.shape) * agent.u_noise if agent.u_noise else 0.0
    #             p_force[i] = agent.action.u + noise
    #     return p_force
    #
    # # gather physical forces acting on entities
    # def apply_environment_force(self, p_force):
    #     # simple (but inefficient) collision response
    #     for a, entity_a in enumerate(self.entities):
    #         for b, entity_b in enumerate(self.entities):
    #             if (b <= a): continue
    #             [f_a, f_b] = self.get_collision_force(entity_a, entity_b)
    #             if (f_a is not None):
    #                 if (p_force[a] is None): p_force[a] = 0.0
    #                 p_force[a] = f_a + p_force[a]
    #             if (f_b is not None):
    #                 if (p_force[b] is None): p_force[b] = 0.0
    #                 p_force[b] = f_b + p_force[b]
    #     return p_force
    #
    # # integrate physical state
    # def integrate_state(self, p_force):
    #     for i, entity in enumerate(self.entities):
    #         if not entity.movable: continue
    #         entity.state.p_vel = entity.state.p_vel * (1 - self.damping)
    #         if (p_force[i] is not None):
    #             entity.state.p_vel += (p_force[i] / entity.mass) * self.dt
    #         if entity.max_speed is not None:
    #             speed = np.sqrt(np.square(entity.state.p_vel[0]) + np.square(entity.state.p_vel[1]))
    #             if speed > entity.max_speed:
    #                 entity.state.p_vel = entity.state.p_vel / np.sqrt(np.square(entity.state.p_vel[0]) +
    #                                                                   np.square(
    #                                                                       entity.state.p_vel[1])) * entity.max_speed
    #         entity.state.p_pos += entity.state.p_vel * self.dt

    def update_agent_state(self, agent):
        # # set communication state (directly for now)
        # if agent.silent:
        #     agent.state.c = np.zeros(self.dim_c)
        # else:
        #     noise = np.random.randn(*agent.action.c.shape) * agent.c_noise if agent.c_noise else 0.0
        #     agent.state.c = agent.action.c + noise
        agent.state.t_pos += agent.state.trainspeed

    def update_mec_state(self, world):
        # MEC恢复初始load
        world.mecs = World.MEC_randomload(world, seed=0, MEClist=world.mecs)  # 随机负载

        "生成随机入侵事件"
        world.agents = world.intrusion(0, world.agents, world)

            # get collision forces for any contact between two entities

    def get_collision_force(self, entity_a, entity_b):
        if (not entity_a.collide) or (not entity_b.collide):
            return [None, None]  # not a collider
        if (entity_a is entity_b):
            return [None, None]  # don't collide against itself
        # compute actual distance between entities
        delta_pos = entity_a.state.p_pos - entity_b.state.p_pos
        dist = np.sqrt(np.sum(np.square(delta_pos)))
        # minimum allowable distance
        dist_min = entity_a.size + entity_b.size
        # softmax penetration
        k = self.contact_margin
        penetration = np.logaddexp(0, -(dist - dist_min) / k) * k
        force = self.contact_force * delta_pos / dist * penetration
        force_a = +force if entity_a.movable else None
        force_b = -force if entity_b.movable else None
        return [force_a, force_b]
