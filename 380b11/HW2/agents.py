import random
import math
import pdb;

BOT_NAME =  "BOT" # INSERT NAME FOR YOUR BOT HERE OR IT WILL THROW AN EXCEPTION


class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
  
    rseed = None  # change this to a value if you want consistent random choices

    def __init__(self):
        if self.rseed is None:
            self.rstate = None
        else:
            random.seed(self.rseed)
            self.rstate = random.getstate()

    def get_move(self, state):
        if self.rstate is not None:
            random.setstate(self.rstate)
        return random.choice(state.successors())


class HumanAgent:
    """Prompts user to supply a valid move.  Very slow and not always smart."""

    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]


class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Gets called by get_move() to determine the value of each successor state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """
        #
        # Fill this in!
        #
        if state.next_player() == 1:
            return self.maxHelper(state)
        
        elif state.next_player() == -1:
            return self.minHelper(state)
        # Change this line!
    
    def maxHelper (self, state):
        child_list =[]
        max = -100000

        if state.is_full():
            return state.utility()

        for moves, child in state.successors():

            child_list.append(self.maxHelper(child))

            max = max(child_list)  
        
        return max 
    
    def minHelper(self, state):

        child_list =[]
        min = 100000

        if state.is_full():
            return state.utility()

        for moves, child in state.successors():

            child_list.append(self.minHelper(child))

            min = min(child_list)  
        
        return min 


class MinimaxLookaheadAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move.
 
    Hint: Consider what you did for MinimaxAgent. What do you need to change to get what you want? 
    """

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit
        #super().__init__()
    
    def maxHelper (self, state, depth):
        child_list =[]
        maxTemp = -100000

        if state.is_full():
            return state.utility()
        elif depth == 0:
            return self.evaluation(state)

        for moves, child in state.successors():

            child_list.append(self.maxHelper(child, depth -1))

            maxTemp = max(child_list)  
        
        return maxTemp 
    
    def minHelper(self, state, depth):

        child_list =[]
        minTemp = 100000

        if state.is_full():
            return state.utility()
        elif depth == 0:
            return self.evaluation(state)

        for moves, child in state.successors():

            child_list.append(self.minHelper(child, depth - 1))

            minTemp = min(child_list)  
        
        return minTemp


    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state.

        Gets called by get_move() to determine the value of successor states.

        The depth data member (set in the constructor) determines the maximum depth of the game 
        tree that gets explored before estimating the state utilities using the evaluation() 
        function.  If depth is 0, no traversal is performed, and minimax returns the results of 
        a call to evaluation().  If depth is None, the entire game tree is traversed.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the (possibly estimated) minimax utility value of the state
        """
        if state.next_player() == 1:
            return self.maxHelper(state, self.depth_limit)
        
        elif state.next_player() == -1:
            return self.minHelper(state, self.depth_limit)
        # Change this line!

    def minimax_depth(self, state, depth):
        """This is just a helper method for minimax(). Feel free to use it or not. """
        pass

    def __get_row_threats(self, rows, player):
        final_score = 0
        for row in rows:
            cnsc = 0
            score = 0
            i = 0
            
            while i < len(row): #iterate over the row
                if row[i] == player: #if the current position holds our tile
                    cnsc += 1 ##inrement number of consecutive tiles we've seen

                elif row[i] != player: #if the current tile we're looking at isn't our piece
                    if row[i] == -2 or row[i] == player*(-1): #if it's an obstacle or the other player's tile
                        if cnsc >= 3: #if we have 3+ consecutive tiles of our players tiles
                            score += cnsc**2 #add it to this row's score
                        cnsc = 0 #reset the number of consecutive tiles of our player we've seen
                    elif row[i] == 0: #otherwise if it's an empty space, see how many empty spaces are next to it
                        j = i + 1 
                        open_spaces = 1 #we know we already have at least one empty space
                        while (j < len(row) and row[j] == 0): #while we have an empty space adjacent and haven't reached the end of the row
                            open_spaces += 1 #increment the number of consecutive empty spaces we've seen
                            j += 1 #move on to the next tile
                            if j == (len(row)): #if we've reached the end of the row
                                cnsc += open_spaces #add the number of consecutive open spaces we have to the number of consecutive of our player's tiles we have
                                if cnsc >= 3: #if there are more than three
                                    score += cnsc ** 2 #increment the row score
                                final_score += score #add row score to final score
                                score = 0 #reset the score
                                open_spaces = 0 #reset the number of empty spaces we see
                                cnsc = 0 #reset cnsc tiles
                        cnsc += open_spaces #if at the end of row does nothing; otherwise, adds the number of empty spaces as potential consecutive tiles
                        i = j #continue looking at the row from where we just left off looking
                        continue
                i += 1 #once we have looked at a tile, move onto the next

            if score > 0: #if we have reached the end of a row and haven't had a chance to add the score yet, add it (ie in the case of player -1 and row [-1,0,0,1,0])
                final_score += score
            if cnsc >= 3: #if there are more than three consecutive tiles
                score += cnsc ** 2 #increment the row score
                final_score += score #add row score to final score
        return final_score
            

    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.

        Gets called by minimax() once the depth limit has been reached.  
        N.B.: This method must run in "constant" time for all states!

        Args:
            state: a connect383.GameState object representing the current board

        Returns: a heuristic estimate of the utility value of the state
        """
        rows = state.get_rows()
        cols = state.get_cols()
        diags = state.get_diags()
        p1_score = 0
        p2_score = 0

        if(len(rows) < 2) and (len(cols) < 2):
            return 0

        p1_score += self.__get_row_threats(rows, 1)
        p2_score += self.__get_row_threats(rows, -1)

       
        return (p1_score - p2_score)  # Change this line!


class AltMinimaxLookaheadAgent(MinimaxAgent):
    """Alternative heursitic agent used for testing."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state."""
        #
        # Fill this in, if it pleases you.
        #
        return 19  # Change this line, unless you have something better to do.


class MinimaxPruneAgent(MinimaxAgent):
    """Computer agent that uses minimax with alpha-beta pruning to select the best move.
    
    Hint: Consider what you did for MinimaxAgent.  What do you need to change to prune a
    branch of the state space? 
    """
    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the value of the class 
        variable GameState.state_count, which keeps track of how many GameState objects have been 
        created over time.  This agent does not have a depth limit.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to column 1 (we're trading optimality for gradeability here).

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        #
        # Fill this in!
        #
        if state.next_player() == 1:
            return self.maxHelper(state, self.depth_limit, -100000, 10000)
        
        elif state.next_player() == -1:
            return self.minHelper(state, self.depth_limit, -100000, 10000)
        # Change this line!

    def maxAlphabeta(self, state, depth, alpha, beta):
        """This is just a helper method for minimax(). Feel free to use it or not."""
        child_list =[]
        maxTemp = -100000

        if state.is_full():
            return state.utility()
        elif depth == 0:
            return self.evaluation(state)

        for moves, child in state.successors():

            child_list.append(self.maxHelper(child, depth -1, alpha, beta))

            maxTemp  = max(child_list) 
            if maxTemp  >= beta:
                return maxTemp 
            a = max(a, maxTemp ) 
        
        return maxTemp 
    
    def minAlphabeta(self, state, depth, alpha, beta):
        """This is just a helper method for minimax(). Feel free to use it or not."""
        child_list =[]
        minTemp = 100000

        if state.is_full():
            return state.utility()
        elif depth == 0:
            return self.evaluation(state)

        for moves, child in state.successors():

            child_list.append(self.minHelper(child, depth - 1, alpha, beta))

            minTemp = min(child_list)  
            if minTemp <= alpha:
                return minTemp
            beta = min(beta, minTemp)
    
        return minTemp
    
    def alphabeta(self, state,alpha, beta):
        """This is just a helper method for minimax(). Feel free to use it or not."""
        pass


def get_agent(tag):
    if tag == 'random':
        return RandomAgent()
    elif tag == 'human':
        return HumanAgent()
    elif tag == 'mini':
        return MinimaxAgent()
    elif tag == 'prune':
        return MinimaxPruneAgent()
    elif tag.startswith('look'):
        depth = int(tag[4:])
        return MinimaxLookaheadAgent(depth)
    elif tag.startswith('alt'):
        depth = int(tag[3:])
        return AltMinimaxLookaheadAgent(depth)
    else:
        raise ValueError("bad agent tag: '{}'".format(tag))       
