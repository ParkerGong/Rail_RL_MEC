import pickle
import matplotlib.pyplot as plt

path = ""
agent_num = 3

print("....................")
print("state_reward_all")
print("....................")

f = open('/Users/parkersix/MARL/MADDPG/maddpg-master/experiments/s_r_ddpg/plots/s_r1_agrewards.pkl', 'rb')
info = pickle.load(f, encoding='iso-8859-1') # Soso


# plt.style.use('ggplot')					# 设置图形的显示风格
# fig=plt.figure(1)						# 新建一个 figure1
plt.plot(info)
plt.xlim(0,750)

plt.savefig("overall-ddpg-0-750.pdf")
plt.show()
# for i in info:
#     print(i)