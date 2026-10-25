import cProfile


class GreedyBFSAgent:
    def __init__(self, problem):
        self.problem = problem
        self.action_plan = []
        self.planning_index = 0

    def plan(self, current_state):
        start_key = current_state.to_state()
        frontier = [(current_state, [], frozenset({start_key}))]

        while frontier:
            state, actions, path_states = frontier.pop()
            if self.problem.is_goal_state(state):
                return actions

            successors = []
            for action in self.problem.get_applicable_actions(state):
                new_state = self.problem.perform_action(state, action)
                state_key = new_state.to_state()
                if state_key not in path_states:
                    successors.append((self.problem.eval(new_state), action, new_state, state_key))

            successors.sort(key=lambda successor: successor[0])
            for _, action, new_state, state_key in reversed(successors):
                frontier.append(
                    (new_state, actions + [action], path_states | {state_key})
                )

        return []
    
    def act(self):
        if len(self.action_plan) == 0:
            # percept
            current_state = self.problem.get_current_state()
            # serach

            pr = cProfile.Profile()
            pr.enable()

            self.action_plan = self.plan(current_state)

            pr.disable()
            # after your program ends
            pr.print_stats(sort="calls")

        if len(self.action_plan) > 0:
            action = self.action_plan[0]
            current_state_hash = self.problem.to_state()
            if type(action) == dict:
                for k in action.keys():
                    if current_state_hash in k:
                        self.action_plan = action[k]
                        action = self.action_plan[0]
                        break
                    else:
                        print(f"current state {current_state_hash} not in plan")
            self.action_plan = self.action_plan[1:]
            return action


    def to_state(self, state):
        if type(state) == list:
            states = []
            for s in state:
                states.append(s.to_state())
            return frozenset(states)
        else:
            return state.to_state()
