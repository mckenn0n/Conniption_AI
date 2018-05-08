URL of the project repository:
    https://github.com/mckenn0n/Conniption_AI

Classes:

  ## Conniption.py ##
  
  This class is used for defining, creating, and evaluating game states. The class is primarily composed of a Conniption object alongside its object methods, as well as a single static method.

  1.  Conniption Object:
      Conniption(board, player1Turn=True, flipsRem=(4,4), flippable=True, parent=None, resMove=None)
        This object encapsulates all relevent information about a given state of the game. The fields are as follows
          a. board - a tuple of length 7 that represents the layout of the game board. Each item in
             the tuple is a boolean tuple whose length can be in the range [0,6]. Each element in
             these sub-tuples is a boolean that indicate whose piece is in that position (True if
             that piece belongs to the AI, False otherwise).
          b. player1Turn - a boolean that is True if the AI is the next player to place a piece,
             False otherwise.
          c. flipsRem - an integer tuple of length 2. Each element is the number of flips that the
             corresponding player is still allowed to make, with the first element representing the
             AI and the second element representing the AI's opponent.
          d. flippable - a boolean that is True if the board is allowed to flip. This will only ever
             be False if the turn that led to this state included a flip after placing a piece.
          e. parent - the Conniption object that the current object was generated from. This should
             only be None for the root of the current search tree.
          f. resMove - A string of length 1, 2, or 3 that describes the move that must be used in
             order to transition from the parent state to this board state. The string will always
             include a number in the range [1,7] and may optionally include a lowercase 'f' before and/or after the number. These indicate that there is a flip before/after the piece is
             placed.
          g. children - A set of Conniption objects. This is the only field that cannot be set
             during initiation of the object and it can only be set by the genChildStates method.
             This set contains all Conniption objects that can be legally reached at the end of the
             current turn.

  2.  genChildStates()
        This method generates all game states that can be reached from the state described by the
        current object after a single move. In effect, this method is the expansion function for the
        game search. Importantly, this method will only execute if the children of the current state
        have not previously been computed to prevent unnecessary re-computation. Children are generated in 1-4 stages. Each stage cannot be executed unless the previous stage was also executed. They are listed below.
          a. noFlip - executed for all boards. Generates children that require no flips to reach.
          b. postFlip - only executed if the current player has flips remaining. Generates children
             that require a flip after placing a piece to reach. This stage utilizes the equivalence between a postFlip and placing a piece at the bottom of a column in an already-flipped board.
          c. preFlip - only executed if flippable is True. Generate children that require a flip
             before placing a piece to reach.
          d. dualFlip - only executed if the current player has at least two flips remaining.
             Generates children that require a flip both before and after placing a piece. This
             stage utilizes the equivalence between a dualFlip and placing a piece at the bottom of a column in a non-flipped board.

  3. betterEval()

  4. isWin()
        This function is the only static function in this class. It determines whether the current
        game state is a winning position for either player. It does this by iterating through each of the 69 possible lines of four cells and determining if the value of all four cells in a given line are the same (either all True or all False). If they are, then the appropriate player (AI if the cells are True, Opponent if they are False) is flagged as being in a win state. In order for the main function to be able to determine who won in the case of a flip causing both players to have a line of four, this function returns a tuple of two booleans where the first element is True only if the AI has a line of 4 and the second is True only if the opponent has a line of four.

  ## Alpha_Beta_Search.py ##

  This class is resposible for the game search.  The search used is iterative deepening with Alpha Beta Pruning.  The class has three methods:

  1.  alpha_beta_search()
        To start a search use the method alpha_beta_search() with the parameters for the current
        object of the board, the integer of max depth to search, and if the search should save the
        visited board states and their evaluation.  **Warning**: saving visited board for a large
        number of run against random will consume a large amount of ram.  
        This method sets the alpha to -infinity and beta to infinity at the root of the tree. For
        all children states in the current board, finds the max of the value or the min_value of
        the children. If the value is greater than alpha, alpha is set to the value and best_state
        is added to a list. The class will return the best state based on the best evaluation
        returned. 

  2.  min_value()
        Recursion helper method of finding the max value for a given depth. The base case of the
        search is when it has reached the max depth. If it is at the max depth, first check if the
        board is in a dictionary of board and their evaluation. If so returns the eval score, else
        calculate the board state and save it in the dictionary. Set value to infinity and for all
        children states in the board passed finds the min of the value or the max_value of the
        children.  If the value is less than or equal to alpha, then return the value because the
        branch can be pruned.  If not, the method should set the beta to the min value of beta or
        the value.

  3.  max_value()
        Recursion helper method of finding the max value for a given depth.  Base case is the same
        as min_value(). Next, the children states are generated of the board. Set value to -infinity
        and for all children states in the board passed find the max of value or min_value of the
        children.  If value is greater than or equal to beta, then return the value because the
        branch can be pruned. If not, the method should set the alpha to the max of alpha or value.
