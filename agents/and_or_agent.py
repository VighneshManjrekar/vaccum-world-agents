
from agents.agent import Agent


class ANDORAgent(Agent):

    def plan(self, current_state):
        return self.or_search(current_state, set())

    def belief_key(self, states):
        return frozenset(
            state.to_state()
            for state in states
        )

    def or_search(self, state, path):
        # If goal, return empty plan
        if self.problem.is_goal_state(state):
            return []

        # Check for cycles
        state_hash = self.belief_key(state)

        if state_hash in path:
            return None

        # Add current state to path
        new_path = path | {state_hash}

        # For each possible action
        for action in self.problem.get_applicable_actions(state):

            # AND-SEARCH(problem, RESULTS(state, action), path)
            results = self.problem.perform_action(state, action)

            plan = self.and_search(results, new_path)

            # If a valid plan is found
            if plan is not None:
                return [action, plan]

        # No valid plan found
        return None

    def and_search(self, states, path):
        # Group states according to possible percepts
        belief_states = self.problem.update_belief_state(states)

        conditional_plan = {}

        # For each possible belief state
        for belief_state in belief_states:

            # OR-SEARCH(problem, state, path)
            plan = self.or_search(belief_state, path)

            # If any branch fails, the whole plan fails
            if plan is None:
                return None

            # Store the conditional plan for this percept
            belief_hash = self.belief_key(belief_state)

            conditional_plan[belief_hash] = plan

        return conditional_plan
