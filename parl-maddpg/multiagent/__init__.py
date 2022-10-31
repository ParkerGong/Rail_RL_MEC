from gym.envs.multiagent.environment import MultiAgentEnv

from gym.envs.multiagent.environment import BatchMultiAgentEnv

from gym.envs.registration import register

""" register(
    id='MultiagentSimple-v0',
    entry_point='gym.envs.multiagent:SimpleEnv',
    # FIXME(cathywu) currently has to be exactly max_path_length parameters in
    # rllab run script
    max_episode_steps=100,
)
register(
    id='MultiagenSimpleSpeakerListener-v0',
    entry_point='gym.envs.multiagent:SimpleSpeakerListenerEnv',
    max_episode_steps=100,
)
register(
    id='MultiagenSimpleWorldComm-v0',
    entry_point='gym.envs.multiagent:SimpleWorldCommEnv',
    max_episode_steps=100,
)
register(
    id='MultiagenSimplePush-v0',
    entry_point='gym.envs.multiagent:SimplePushEnv',
    max_episode_steps=100,
) """