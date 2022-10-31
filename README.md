# Rail_RL_MEC
An open-source experimental environment of railway intrusion detection based on CV, with RL methods for MEC resource allocation.

Myenv: the Rail_RL_MEC environment based on PARL-MADDPG. Modified for rail MEC environment (unfinished).

maddpg_env: the maddpg environment from open-AI. As the baseline of MADDPG model.

parl-maddpg: the original parl-maddpg code.


------code below is the old version, is no longer in use------

basic.py: the basic class of train, MEC, and track. 

Move_Draw.py: some functions of Main_env.py for reuse.

Main_env.py: the main environment of RL, init() for initialize the environment. env() for executing action, calculating reward, and move to the next state.

rl.py: the reinforcement learning network.

main.py: major body code of training process.

test.py: for function testing only.

