import cProfile


class IDDFSAgent:
    def __init__(self, problem):
        self.problem = problem
        self.action_plan = []
        self.planning_index = 0

    def plan(self, current_state):
        depth_limit = 0
        start_key = current_state.to_state()

        while True:
            frontier = [(current_state, [], frozenset({start_key}))]
            cutoff_reached = False

            while frontier:
                state, actions, path_states = frontier.pop()

                if self.problem.is_goal_state(state):
                    return actions

                applicable_actions = self.problem.get_applicable_actions(state)
                if len(actions) == depth_limit:
                    for action in applicable_actions:
                        next_state = self.problem.perform_action(state, action)
                        if next_state.to_state() not in path_states:
                            cutoff_reached = True
                            break
                    continue

                for action in reversed(applicable_actions):
                    next_state = self.problem.perform_action(state, action)
                    state_key = next_state.to_state()
                    if state_key not in path_states:
                        frontier.append(
                            (next_state, actions + [action], path_states | {state_key})
                        )

            if not cutoff_reached:
                return []
            depth_limit += 1
    
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
