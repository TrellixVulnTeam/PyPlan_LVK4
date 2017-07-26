from agents import *
from heuristics import rollout_heuristic
from dealers import pacman_dealer

"""
Policy switching carries with it the theoretical guarantee that at each time step, it will perform at least as well as 
the best policy in its set. However, a certain number of pulls is required to accurately estimate the value of a given 
policy. If an insufficient pull budget is provided, policy switching may do somewhat worse than its best constituent
policy.
"""
if __name__ == '__main__':
    h1 = rollout_heuristic.RolloutHeuristicClass(width=1, depth=10)

    u_ro = uniform_rollout_agent.UniformRolloutAgentClass(depth=1, num_pulls=100)
    ss = sparse_sampling_agent.SparseSamplingAgentClass(depth=2, pulls_per_node=20, heuristic=h1)
    switching_agent = policy_switching_agent.PolicySwitchingAgentClass(depth=3, num_pulls=15, policies=[u_ro, ss])

    pacman = pacman_dealer.Dealer(layout_representation='testClassic')
    pacman.run(agents=[u_ro, ss, switching_agent], num_trials=15)
