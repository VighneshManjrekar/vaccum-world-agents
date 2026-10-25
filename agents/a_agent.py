import cProfile
from heapq import heappop, heappush
from itertools import count


class AStarAgent:
    def __init__(self, problem):
        self.problem = problem
        self.action_plan = []
        self.planning_index = 0

    def plan(self, current_state):
        tie_breaker = count()
        start_key = current_state.to_state()
        start_cost = 0
        frontier = [
            (
                start_cost + self.problem.eval(current_state),
                next(tie_breaker),
                start_cost,
                current_state,
                [],
            )
        ]
        best_costs = {start_key: start_cost}

        while frontier:
            _, _, path_cost, state, actions = heappop(frontier)
            state_key = state.to_state()
            if path_cost != best_costs.get(state_key):
                continue

            if self.problem.is_goal_state(state):
                return actions

            for action in self.problem.get_applicable_actions(state):
                new_state = self.problem.perform_action(state, action)
                state_key = new_state.to_state()
                new_cost = path_cost + self.problem.action_cost(state, action, new_state)
                if new_cost < best_costs.get(state_key, float("inf")):
                    best_costs[state_key] = new_cost
                    heappush(
                        frontier,
                        (
                            new_cost + self.problem.eval(new_state),
                            next(tie_breaker),
                            new_cost,
                            new_state,
                            actions + [action],
                        ),
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
