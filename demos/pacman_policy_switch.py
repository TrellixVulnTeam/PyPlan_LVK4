from agents import *
from heuristics import rollout_heuristic
from simulators import pacman_sim

"""
Policy switching carries with it the theoretical guarantee that at each juncture, it will perform at least as well as 
the best policy in its set.
"""

if __name__ == '__main__':
    rand_agent = random_agent.RandomAgentClass()

    u_ro = uniform_rollout_agent.UniformRolloutAgentClass(depth=1, num_pulls=100, policy=rand_agent)

    h = rollout_heuristic.RolloutHeuristicClass(rollout_policy=rand_agent, width=1, depth=10)
    ss_d3 = sparse_sampling_agent.SparseSamplingAgentClass(depth=3, pulls_per_node=5, heuristic=h)

    switch_agent = policy_switch_agent.PolicySwitchAgentClass(num_pulls=10, policies=[u_ro, ss_d3])

    pacman = pacman_sim.PacmanStateClass(layout_repr='testClassic', agents=[u_ro, ss_d3, switch_agent],
                                         use_graphics=True)
    pacman.run(num_trials=5)