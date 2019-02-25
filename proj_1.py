import sys
import random
import heapq


class Puzzle:

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    parity_0 = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    parity_1 = [1, 2, 3, 8, 0, 4, 7, 6, 5]

    def __init__(self, input_arr=None):
        if input_arr:
            self.state = input_arr
        else:
            self.state = [i for i in range(9)]
            random.shuffle(self.state)
        self.goal_state = self.get_goal_state()

    def print_state(self, state):
        print('{0}\n{1}\n{2}'.format(
            ' '.join([str(state[i]) for i in range(0, 3)]),
            ' '.join([str(state[i]) for i in range(3, 6)]),
            ' '.join([str(state[i]) for i in range(6, 9)])))

    def print_actions(self, action):
        action_str = []
        str_map = {
            Puzzle.UP: 'UP',
            Puzzle.DOWN: 'DOWN',
            Puzzle.LEFT: 'LEFT',
            Puzzle.RIGHT: 'RIGHT'
        }
        for a in action:
            action_str.append(str_map[a])
        print(' '.join(action_str))

    def get_goal_state(self):

        def calc_parity(state):  
            parity = 0
            for i in range(9):
                for j in range(i, 9):
                    if state[j] > state[i]:
                        parity += 1
            return parity % 2
        
        parity = calc_parity(self.state)

        if parity == 0:
            return self.parity_0
        else:
            return self.parity_1

    def get_possible_actions(self, actions):
        new_state = self.get_updated_state(actions)
        i = self.find_empty_space(new_state)
        
        possible_actions = []
        last_action = None
        if len(actions) > 0:
            last_action = actions[-1]

        add_new_action = lambda x: possible_actions.append(actions + [x])

        if i > 2 and last_action != Puzzle.DOWN:
           add_new_action(Puzzle.UP)
        if i % 3 > 0 and last_action != Puzzle.RIGHT:
            add_new_action(Puzzle.LEFT)
        if i % 3 < 2 and last_action != Puzzle.LEFT:
            add_new_action(Puzzle.RIGHT)
        if i < 6 and last_action != Puzzle.UP:
            add_new_action(Puzzle.DOWN)

        return possible_actions

    def find_empty_space(self, state):
        return state.index(0)

    def get_updated_state(self, actions, state=None):
        current_state = list(state) if state else list(self.state)
        empty = self.find_empty_space(state if state else self.state)

        def swap(i):
            current_state[i], current_state[empty] = current_state[empty], current_state[i]
            return i

        for a in actions:
            if a == Puzzle.UP:
                empty = swap(empty - 3)
            if a == Puzzle.DOWN:
                empty = swap(empty + 3)
            if a == Puzzle.LEFT:
                empty = swap(empty - 1)
            if a == Puzzle.RIGHT:
                empty = swap(empty + 1)

        return current_state

    def serialize_actions(self, actions):
        return ''.join([str(a) for a in actions])

    def bfs_search(self):

        queue = []
        queue.append([])

        tried_states = {}

        action_str = lambda x: ''.join([str(a) for a in x])

        node_count = 1

        while len(queue) > 0:
            p = queue.pop(0)

            '''
            self.print_state(self.state)
            self.print_actions(p)
            self.print_state(self.get_updated_state(p))
            '''

            if self.get_updated_state(p) == self.goal_state:
                return self.state, p, node_count

            tried_states[action_str(self.get_updated_state(p))] = 1
            print(len(action_str(p)))

            for a in self.get_possible_actions(p):
                
                if action_str(self.get_updated_state(a)) in tried_states:
                    continue
                
                if a not in queue:
                    queue.append(a)
                    node_count += 1
        
        print(self.state)
        print(self.goal_state)
        print(node_count)      

    def a_star_search(self, h):
        pqueue = []

        tried_states = {}

        action_str = lambda x: ''.join([str(a) for a in x])

        cost = lambda a: len(a) + h(self.get_updated_state(a), self.goal_state)

        heapq.heappush(pqueue, (cost([]), []))

        node_count = 1

        while len(pqueue) > 0:
            c, p = heapq.heappop(pqueue)

            if self.get_updated_state(p) == self.goal_state:
                return self.state, p, node_count

            tried_states[action_str(self.get_updated_state(p))] = 1

            print(len(p), c - len(p))
            # print(self.get_possible_actions(p))
            # self.print_state(self.get_updated_state(p))
            # self.print_actions(p)
            # self.print_state(self.goal_state)

            for a in self.get_possible_actions(p):

                if action_str(self.get_updated_state(a)) in tried_states:
                    continue
                
                in_frontier = len([i for i in pqueue if i[1] == a]) > 0
                if not in_frontier:
                    heapq.heappush(pqueue, (cost(a), a))
                    node_count += 1
        
        print(self.state)
        print(self.goal_state)
        print(node_count)      


def manhattan(curr_state, goal_state):
    assert len(curr_state) == 9 and len(goal_state) == 9
    total_diff = 0
    for i, v in enumerate(curr_state):
        goal_i = goal_state.index(v)
        vert_diff = abs(goal_i - i) // 3
        hori_diff = abs(goal_i - i) % 3
        total_diff += vert_diff + hori_diff
    return total_diff

def out_of_place(curr_state, goal_state):
    assert len(curr_state) == 9 and len(goal_state) == 9
    total_diff = 0
    for i, v in enumerate(curr_state):
        goal_i = goal_state.index(v)
        if i != goal_i:
            total_diff += 1
    return total_diff

if __name__ == '__main__':
    input_arr = None
    if len(sys.argv) == 10:
        input_arr = [int(i) for i in sys.argv[1:]]
        print(input_arr)

    puzzle = Puzzle(input_arr) if input_arr else Puzzle()

    state, actions, count = puzzle.bfs_search()
    # state, actions, count = puzzle.a_star_search(manhattan)
    # state, actions, count = puzzle.a_star_search(out_of_place)
    
    puzzle.print_state(puzzle.get_updated_state(actions, state))
    puzzle.print_actions(actions)
    puzzle.print_state(puzzle.get_goal_state())

    print(state)
    print(actions)
    print(count)
    
    
    

