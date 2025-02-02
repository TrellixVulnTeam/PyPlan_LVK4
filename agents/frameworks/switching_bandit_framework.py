import numpy as np
import multiprocessing
from abstract import abstract_agent
from agents.bandits.uniform_bandit import UniformBandit


class SwitchingBanditFramework(abstract_agent.AbstractAgent):
    """An agent that takes a list of policies and returns the value of the best one at a given state."""
    name = "Policy-Switching Bandit Agent"

    def __init__(self, depth, pulls_per_node, policies, bandit_class=None, bandit_parameters=None):
        """Initialize a policy-switching bandit that follows each selected policy for depth steps per trajectory."""
        self.depth = depth
        self.pulls_per_node = pulls_per_node

        self.policies = policies

        self.bandit_class = bandit_class if bandit_class else UniformBandit
        self.bandit_parameters = bandit_parameters

        self.set_multiprocess(False)

    def set_multiprocess(self, multiprocess):
        """Preclude nested multiprocessing."""
        self.multiprocess = multiprocess
        if self.multiprocess:
            for policy in self.policies:
                if hasattr(policy, 'multiprocess'):
                        policy.multiprocess = False

    def select_action(self, state):
        """Selects the highest-valued action for the given state."""
        return self.estimateV(state)[1]  # return the best action

    def estimateV(self, state):
        """Returns the best expected reward and action selected by the best policy at the given state."""
        num_policies = len(self.policies)
        bandit = self.bandit_class(num_policies, self.bandit_parameters) if self.bandit_parameters \
            else self.bandit_class(num_policies)

        # For each policy, for each player, initialize a q-value
        q_values = np.array([[0.0] * state.num_players for _ in range(num_policies)])

        if self.multiprocess and __name__ == '__main__':
            with multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1) as pool:
                remaining = self.pulls_per_node
                while remaining > 0:
                    pulls_to_use = min(pool._processes, remaining)
                    outputs = pool.starmap(self.run_pull, [[state, bandit]] * pulls_to_use)
                    remaining -= pulls_to_use

                    for policy_idx, total_reward in outputs:
                        q_values[policy_idx] += total_reward
                        bandit.update(policy_idx, total_reward[state.current_player])
        else:
            for _ in range(self.pulls_per_node):  # use pull budget
                # Integrate total reward with current q_values
                policy_idx, total_reward = self.run_pull(state, bandit)
                q_values[policy_idx] += total_reward
                bandit.update(policy_idx, total_reward[state.current_player])  # update the reward for the given arm

        # Get most-selected action of highest-valued policy (useful for stochastic environments)
        best_policy_idx = bandit.get_best_arm()
        best_action_select = self.policies[best_policy_idx].select_action(state)

        return q_values[best_policy_idx] / bandit.num_pulls[best_policy_idx], best_action_select

    def run_pull(self, state, bandit):
        """Choose an arm to pull, execute the action, and return the chosen arm and total reward received."""
        policy_idx = bandit.select_pull_arm()

        sim_state = state.clone()
        total_reward = np.array([0.0] * state.num_players)  # calculate discounted total rewards
        for _ in range(self.depth):
            if sim_state.is_terminal():
                break
            action = self.policies[policy_idx].select_action(sim_state)
            total_reward += sim_state.take_action(action)

        return policy_idx, total_reward

