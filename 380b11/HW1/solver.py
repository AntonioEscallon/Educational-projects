import sys
# from this import s
import puzz
import pdqpq
import pdb

GOAL_STATE = puzz.EightPuzzleBoard("012345678")


def solve_puzzle(start_state, flavor):
    """Perform a search to find a solution to a puzzle.
    
    Args:
        start_state (EightPuzzleBoard): the start state for the search
        flavor (str): tag that indicate which type of search to run.  Can be one of the following:
            'bfs' - breadth-first search
            'ucost' - uniform-cost search
            'greedy-h1' - Greedy best-first search using a misplaced tile count heuristic
            'greedy-h2' - Greedy best-first search using a Manhattan distance heuristic
            'greedy-h3' - Greedy best-first search using a weighted Manhattan distance heuristic
            'astar-h1' - A* search using a misplaced tile count heuristic
            'astar-h2' - A* search using a Manhattan distance heuristic
            'astar-h3' - A* search using a weighted Manhattan distance heuristic
    
    Returns: 
        A dictionary containing describing the search performed, containing the following entries:
        'path' - list of 2-tuples representing the path from the start to the goal state (both 
            included).  Each entry is a (str, EightPuzzleBoard) pair indicating the move and 
            resulting successor state for each action.  Omitted if the search fails.
        'path_cost' - the total cost of the path, taking into account the costs associated with 
            each state transition.  Omitted if the search fails.
        'frontier_count' - the number of unique states added to the search frontier at any point 
            during the search.
        'expanded_count' - the number of unique states removed from the frontier and expanded 
            (successors generated)

    """
    if flavor.find('-') > -1:
        strat, heur = flavor.split('-')
    else:
        strat, heur = flavor, None

    if strat == 'bfs':
        return BreadthFirstSolver().solve(start_state)
    elif strat == 'ucost':
        return UCS().solve(start_state)
    elif strat == 'greedy':
        return Greedy().solve(start_state, heur)
    elif strat == 'astar':
        return Astar().solve(start_state, heur)
    else:
        raise ValueError("Unknown search flavor '{}'".format(flavor))


class BreadthFirstSolver:
    """Implementation of Breadth-First Search based puzzle solver"""

    def __init__(self):
        self.goal = GOAL_STATE
        self.parents = {}  # state -> parent_state
        self.frontier = pdqpq.FifoQueue()
        self.explored = set()
        self.frontier_count = 0  # increment when we add something to frontier
        self.expanded_count = 0  # increment when we pull something off frontier and expand
    
    def solve(self, start_state):
        """Carry out the search for a solution path to the goal state.
        
        Args:
            start_state (EightPuzzleBoard): start state for the search 
        
        Returns:
            A dictionary describing the search from the start state to the goal state.

        """
        self.parents[start_state] = None
        self.add_to_frontier(start_state)

        if start_state == self.goal:  # edge case        
            return self.get_results_dict(start_state)

        while not self.frontier.is_empty():
            node = self.frontier.pop()  # get the next node in the frontier queue
            succs = self.expand_node(node)
            for move, succ in succs.items():
                if (succ not in self.frontier) and (succ not in self.explored):
                    self.parents[succ] = node

                    # BFS checks for goal state _before_ adding to frontier
                    if succ == self.goal:
                        return self.get_results_dict(succ)
                    else:
                        self.add_to_frontier(succ)

        # if we get here, the search failed
        return self.get_results_dict(None) 

    def add_to_frontier(self, node):
        """Add state to frontier and increase the frontier count."""
        self.frontier.add(node)
        self.frontier_count += 1

    def expand_node(self, node):
        """Get the next state from the frontier and increase the expanded count."""
        self.explored.add(node)
        self.expanded_count += 1
        return node.successors()

    def get_results_dict(self, state):
        """Construct the output dictionary for solve_puzzle()
        
        Args:
            state (EightPuzzleBoard): final state in the search tree
        
        Returns:
            A dictionary describing the search performed (see solve_puzzle())

        """
        results = {}
        results['frontier_count'] = self.frontier_count
        results['expanded_count'] = self.expanded_count
        if state:
            results['path_cost'] = self.get_cost(state)
            path = self.get_path(state)
            moves = ['start'] + [ path[i-1].get_move(path[i]) for i in range(1, len(path)) ]
            results['path'] = list(zip(moves, path))
        return results

    def get_path(self, state):
        """Return the solution path from the start state of the search to a target.
        
        Results are obtained by retracing the path backwards through the parent tree to the start
        state for the serach at the root.
        
        Args:
            state (EightPuzzleBoard): target state in the search tree
        
        Returns:
            A list of EightPuzzleBoard objects representing the path from the start state to the
            target state

        """
        path = []
        while state is not None:
            path.append(state)
            state = self.parents[state]
        path.reverse()
        return path

    def get_cost(self, state): 
        """Calculate the path cost from start state to a target state.
        
        Transition costs between states are equal to the square of the number on the tile that 
        was moved. 

        Args:
            state (EightPuzzleBoard): target state in the search tree
        
        Returns:
            Integer indicating the cost of the solution path

        """
        cost = 0
        path = self.get_path(state)
        for i in range(1, len(path)):
            x, y = path[i-1].find(None)  # the most recently moved tile leaves the blank behind
            tile = path[i].get_tile(x, y)        
            cost += int(tile)**2
        return cost

class UCS(BreadthFirstSolver):
    def __init__(self):
        super().__init__()
        self.frontier = pdqpq.PriorityQueue()
    
    def solve(self, start_state):
        self.parents[start_state] = None #add the start state to the frontier
        self.add_to_frontier(start_state, self.get_cost(start_state))

        if start_state == self.goal: #if the start state is the goal, return it
            return self.get_results_dict(start_state)

        while not self.frontier.is_empty(): #while the frontier isn't empty
            node = self.frontier.pop() #get the first node from the frontier

            succs = self.expand_node(node) #get the node's successors
            
            if node == self.goal: #if this is the goal, return the solution
                return self.get_results_dict(node)

            for move, succ in succs.items(): #for each possible succ
                if (succ not in self.frontier) and (succ not in self.explored): #if it isn't in the frontier and hasn't been explored
                    self.parents[succ] = node #set succ's parent to node
                    priority = self.get_cost(succ) #get the cost of reaching succ from node
                    self.add_to_frontier(succ, priority) #add succ to the frontier

                elif (succ in self.frontier) and (succ not in self.explored): #if the node is already in the frontier and hasn't been explored
                    old_parent = self.parents[succ] #temporarily set the parent of the successor to the popped node
                    self.parents[succ] = node
                    if (self.frontier.get(succ) > (self.get_cost(succ))): # if the cost of reaching the successor from the popped node is less than what's in the frontier
                        new_priority = (self.get_cost(succ)) #update the successor in the frontier and set its new parent
                        self.update_frontier(succ, new_priority)
                    else: #otherwise, just resest the parent back to the original
                        self.parents[succ] = old_parent

        return self.get_results_dict(None)
    
    def add_to_frontier(self, node, priority):
        self.frontier.add(node, priority)
        self.frontier_count += 1
    
    def update_frontier(self, node, priority):
        self.frontier.add(node, priority)

class Greedy(UCS):

    def __init__(self):
        super().__init__()
        self.frontier = pdqpq.PriorityQueue()
    
    def solve(self, start_state, heur):
        self.parents[start_state] = None #set the parent of the start node to none
        self.add_to_frontier(start_state, self.get_heuristic(start_state, heur)) #add start node to the frontier

        if start_state == self.goal: #if the start is the goal, return it
            return self.get_results_dict(start_state)
        

        while not self.frontier.is_empty(): # while the frontier isn't empty
            node = self.frontier.pop() #pop the first node off the frontier

            succs = self.expand_node(node) #get all of the node's successors

            if node == self.goal: # if the node is the goal, return the solution
                return self.get_results_dict(node)

            for move, succ in succs.items(): #for each successor
                if(succ not in self.frontier) and (succ not in self.explored): #if it isn't in the frontier and hasn't been explored
                    self.parents[succ] = node #set its parent to the popped node
                    priority = self.get_heuristic(succ, heur) #get succ's priority using the appropriate heuristic         
                    self.add_to_frontier(succ, priority) #add succ to the frontier
        
        return self.get_results_dict(None)
                                 
    def __get_h1(self, node):
        priority = 0
        for i in range(0,9):
            if i != int(node._board[i]) and i != 0:
                priority += 1
        return priority
    
    def __get_h2(self, node):
        priority = 0
        for i in range (0,9): #get manhattan distance
            mh = 0
            goal_tile = self.goal.find(str(i))
            curr_tile = node.find(str(i))
            mh = abs(goal_tile[0] - curr_tile[0]) + abs(goal_tile[1] - curr_tile[1])
            if i != 0:
                priority += mh
        return priority
    
    def __get_h3(self, node):
        priority = 0
        for i in range (0,9): #get manhattan distance
            mh = 0
            goal_tile = self.goal.find(str(i))
            curr_tile = node.find(str(i))
            mh = abs(goal_tile[0] - curr_tile[0]) + abs(goal_tile[1] - curr_tile[1])
            priority += (mh * (i ** 2))
        return priority
    
    def get_heuristic(self, node, heur):
        priority = 0
        if heur == "h1": #if heuristic is h1, get number of misplaced tiles (not including the empty tile)
            priority = self.__get_h1(node)

        elif heur == "h2":
            priority = self.__get_h2(node)

        elif heur == "h3":
            priority = self.__get_h3(node)

        return priority

    def add_to_frontier(self, node, priority):
        return super().add_to_frontier(node, priority)      

    def update_frontier(self, node, priority):
        return super().update_frontier(node, priority)

class Astar(Greedy):

    def __init__(self):
        super().__init__()
        self.frontier = pdqpq.PriorityQueue()

    def solve(self, start_state, heur):
        self.parents[start_state] = None #add the start state to the frontier
        self.add_to_frontier(start_state, self.get_heuristic(start_state, heur) + (self.get_cost(start_state)))

        if start_state == self.goal: #if the start state is the goal, return it
            return self.get_results_dict(start_state)

        while not self.frontier.is_empty(): #while the frontier isn't empty
            node = self.frontier.pop() #get the first node from the frontier

            succs = self.expand_node(node) #get the node's successors
            
            if node == self.goal: #if this is the goal, return the solution
                return self.get_results_dict(node)

            for move, succ in succs.items(): #for each possible succ
                if (succ not in self.frontier) and (succ not in self.explored): #if it isn't in the frontier and hasn't been explored
                    self.parents[succ] = node #set succ's parent to node
                    priority = self.get_heuristic(succ, heur) + (self.get_cost(succ))#get the cost of reaching succ from node
                    self.add_to_frontier(succ, priority) #add succ to the frontier

                elif (succ in self.frontier) and (succ not in self.explored): #if the node is already in the frontier and hasn't been explored
                    old_parent = self.parents[succ] #temporarily set the parent of the successor to the popped node
                    self.parents[succ] = node
                    if (self.frontier.get(succ) > self.get_heuristic(succ, heur) + (self.get_cost(succ))): # if the cost of reaching the successor from the popped node is less than what's in the frontier
                        new_priority = self.get_heuristic(succ, heur) + (self.get_cost(succ)) #update the successor in the frontier and set its new parent
                        self.update_frontier(succ, new_priority)
                    else: #otherwise, just resest the parent back to the original
                        self.parents[succ] = old_parent

        return self.get_results_dict(None)
    
    def get_heuristic(self, node, heur):
        return super().get_heuristic(node, heur) 
    
    def add_to_frontier(self, node, priority):
        return super().add_to_frontier(node, priority)

    def update_frontier(self, node, priority):
        return super().update_frontier(node, priority)

def print_table(flav__results, include_path=False):
    """Print out a comparison of search strategy results.

    Args:
        flav__results (dictionary): a dictionary mapping search flavor tags result statistics. See
            solve_puzzle() for detail.
        include_path (bool): indicates whether to include the actual solution paths in the table

    """
    result_tups = sorted(flav__results.items())
    c = len(result_tups)
    na = "{:>12}".format("n/a")
    rows = [  # abandon all hope ye who try to modify the table formatting code...
        "flavor  " + "".join([ "{:>12}".format(tag) for tag, _ in result_tups]),
        "--------" + ("  " + "-"*10)*c,
        "length  " + "".join([ "{:>12}".format(len(res['path'])) if 'path' in res else na 
                                for _, res in result_tups ]),
        "cost    " + "".join([ "{:>12,}".format(res['path_cost']) if 'path_cost' in res else na 
                                for _, res in result_tups ]),
        "frontier" + ("{:>12,}" * c).format(*[res['frontier_count'] for _, res in result_tups]),
        "expanded" + ("{:>12,}" * c).format(*[res['expanded_count'] for _, res in result_tups])
    ]
    if include_path:
        rows.append("path")
        longest_path = max([ len(res['path']) for _, res in result_tups if 'path' in res ] + [0])
        print("longest", longest_path)
        for i in range(longest_path):
            row = "        "
            for _, res in result_tups:
                if len(res.get('path', [])) > i:
                    move, state = res['path'][i]
                    row += " " + move[0] + " " + str(state)
                else:
                    row += " "*12
            rows.append(row)
    print("\n" + "\n".join(rows), "\n")

def get_test_puzzles():
    """Return sample start states for testing the search strategies.
    
    Returns:
        A tuple containing three EightPuzzleBoard objects representing start states that have an
        optimal solution path length of 3-5, 10-15, and >=25 respectively.
    
    """ 
    # Note: test cases can be hardcoded, and are not required to be programmatically generated.
    #
    # fill in function body here
    #
    #Three test cases labeled by difficulty
    easy = puzz.EightPuzzleBoard('120345678')
    med = puzz.EightPuzzleBoard('123045678')
    hard = puzz.EightPuzzleBoard('871602543')
    return (easy, med, hard)  # fix this line!






############################################

if __name__ == '__main__':

    # parse the command line args
    start = puzz.EightPuzzleBoard(sys.argv[1])
    if sys.argv[2] == 'all':
        flavors = ['bfs', 'ucost', 'greedy-h1', 'greedy-h2', 
                   'greedy-h3', 'astar-h1', 'astar-h2', 'astar-h3']
    else:
        flavors = sys.argv[2:]

    # run the search(es)
    results = {}
    for flav in flavors:
        print("solving puzzle {} with {}".format(start, flav))
        results[flav] = solve_puzzle(start, flav)

    print_table(results, include_path=True)  # change to True to see the paths!