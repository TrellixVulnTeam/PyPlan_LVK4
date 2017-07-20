from bandits import *
from agents.frameworks import fsss_framework
from heuristics import rollout_heuristic


class FSSSAgentClass(fsss_framework.FSSSAgentClass):
    my_name = "Forward Search Sparse Sampling Agent"

    def __init__(self, depth, pulls_per_node, c=1, heuristic=None, base_policy=None):
        h1 = rollout_heuristic.RolloutHeuristicClass(width=1, depth=depth, rollout_policy=base_policy)
        base_policy = h1.rollout_policy
        fsss_framework.FSSSAgentClass.__init__(self, depth=depth, pulls_per_node=pulls_per_node, heuristic=heuristic,
                                               bandit_alg_class=ucb_bandit_alg.UCBBanditAlgClass, bandit_parameters=c)
        # QUESTION what kind of bandit should we provide?
        self.agent_name = self.my_name + \
                          " (d={}, pulls per node={}, c={}, base policy={})".format(depth,
                                                                                    pulls_per_node,
                                                                                    c,
                                                                                    base_policy.agent_name)
