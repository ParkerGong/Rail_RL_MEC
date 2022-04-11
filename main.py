# main.py

# 导入环境和学习方法
from Main_env import TrainEnv
from rl import DDPG

# 设置全局变量
MAX_EPISODES = 500
MAX_EP_STEPS = 200

# 设置环境
env = TrainEnv()
s_dim = env.state_dim
a_dim = env.action_dim
a_bound = env.action_bound

# 设置学习方法 (这里使用 DDPG)
rl = DDPG(a_dim, s_dim, a_bound)

# 开始训练
for i in range(MAX_EPISODES):
    s = env.reset()                 # 初始化回合设置
    for j in range(MAX_EP_STEPS):
        env.render()                # 环境的渲染
        a = rl.choose_action(s)     # RL 选择动作
        s_, r, done = env.step(a)   # 在环境中施加动作

        # DDPG 这种强化学习需要存放记忆库
        rl.store_transition(s, a, r, s_)

        if rl.memory_full:
            rl.learn()              # 记忆库满了, 开始学习

        s = s_                      # 变为下一回合


# "主函数，应放到RL主线程中，其余部分封装为新的类"
# def main(action):
#     # Main track, train, MEC
#     Mtrack, MtrainList, MMECList = init()  # 初始化所有状态
#     env(Mtrack, MtrainList, MMECList)
#     # 执行动作
#
#     # 返回下一状态，状态更新


