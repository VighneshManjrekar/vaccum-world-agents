import cProfile


class DFSAgent:
    def __init__(self, problem):
        self.problem = problem
        self.action_plan = []
        self.planning_index = 0

    def plan(self, current_state):
        frontier = [(current_state, [])]
        visited_states = {current_state.to_state()}

        while frontier:
            current_node = frontier.pop()
            current_state = current_node[0]

            if self.problem.is_goal_state(current_state):
                return current_node[1]

            for action in reversed(self.problem.get_applicable_actions(current_state)):
                new_state = self.problem.perform_action(current_state, action)

                state_key = new_state.to_state()
                if state_key not in visited_states:
                    visited_states.add(state_key)
                    actions = current_node[1][:]
                    actions.append(action)
                    frontier.append((new_state, actions))

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
