from agents import rollout_agent
from agents.bandits.uniform_bandit import UniformBandit


class UniformRolloutAgent(rollout_agent.RolloutAgent):
    base_name = "Uniform Rollout Agent"

    def __init__(self, depth, num_pulls, policy=None):
        rollout_agent.RolloutAgent.__init__(self, depth=depth, num_pulls=num_pulls,
                                            policy=policy,
                                            bandit_class=UniformBandit)
        
        if policy is not None:  # if policy isn't random, it's a nested agent
            self.base_name = "Nested " + self.base_name
        self.name = self.base_name + " (d={}, n={})".format(depth, num_pulls)
