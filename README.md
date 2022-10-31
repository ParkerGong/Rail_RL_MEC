# Rail_RL_MEC
An open-source experimental environment of railway intrusion detection based on CV, with RL methods for MEC resource allocation.

maddpg_env: the maddpg enviroment from open-AI. Would be modified (todo) to fit the railway intrusion detection experiment. 
NOTICE!! Mark maddpg_env/maddpg-master/maddpg/common as the source root.

basic.py: the basic class of train, MEC, and track. 

Move_Draw.py: some functions of Main_env.py for reuse.

Main_env.py: the main environment of RL, init() for initialize the environment. env() for executing action, calculating reward, and move to the next state.

rl.py: the reinforcement learning network.

main.py: major body code of training process.

test.py: for function testing only.

