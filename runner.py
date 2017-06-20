import simulate
from simulators import connect4_sim, pacman_sim, openai_sim
from heuristics import rollout_heuristic, switching_heuristic
from agents import random_agent
from agents import mcts_agent
from agents import policy_switch_agent
from agents import uniform_rollout_agent
from agents import e_rollout_agent
from agents import ucb_rollout_agent
from agents import uct_agent
from agents import eroot_uct_agent
from agents import sparse_sampling_agent

rand_agent = random_agent.RandomAgentClass()

h1 = rollout_heuristic.RolloutHeuristicClass(rollout_policy=rand_agent, width=1, depth=10)

h10 = rollout_heuristic.RolloutHeuristicClass(rollout_policy=rand_agent, width=10, depth=10)

u_ro = uniform_rollout_agent.UniformRolloutAgentClass(depth=1, num_pulls=10, policy=rand_agent)

nested_u_ro = uniform_rollout_agent.UniformRolloutAgentClass(depth=10, num_pulls=10, policy=u_ro)

e_ro_d10_n10 = e_rollout_agent.ERolloutAgentClass(depth=10, num_pulls=10, epsilon=0.5, policy=rand_agent)

ucb_ro_d100_n100_c1 = ucb_rollout_agent.UCBRolloutAgentClass(depth=100, num_pulls=100, c=1.0, policy=rand_agent)

ss_d3 = sparse_sampling_agent.SparseSamplingAgentClass(depth=3, pulls_per_node=100, heuristic=h1)
ss_d5 = sparse_sampling_agent.SparseSamplingAgentClass(depth=5, pulls_per_node=5, heuristic=h1)

uct1000 = uct_agent.UCTAgentClass(depth=10, max_width=1, num_trials=1000, c=1)

eroot_uct1000 = eroot_uct_agent.ERootUCTAgentClass(depth=10, max_width=1, num_trials=1000, c=1)

switch_agent = policy_switch_agent.PolicySwitchAgentClass(depth=1, num_pulls=10, policies=[u_ro, e_ro_d10_n10])

openai = openai_sim.OpenAIStateClass('FrozenLake-v0', nested_u_ro, wrapper_target='FrozenLake', api_key='sk_brIgt2t3TLGjd0IFrWW9rw')
openai.run()

#pacman = pacman_sim.PacmanStateClass('testClassic', u_ro)
#pacman.run()

#initial_state = connect4_sim.Connect4StateClass()
#agents_list = [switch_agent, u_ro]
#simulate.run(initial_state, agents_list)
