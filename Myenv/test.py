import time

import gym

env = gym.make("CarRacing-v0")
env.reset()
env.render()
time.sleep(10)
env.close()