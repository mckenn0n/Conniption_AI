
This is a list of Len 4 tuples that rep every posable combination of 4 elements in a row posable on a coniption board.

[[(0, 0), (1, 0), (2, 0), (3, 0)], [(1, 0), (2, 0), (3, 0), (4, 0)], [(2, 0), (3, 0), (4, 0), (5, 0)], 
[(3, 0), (4, 0), (5, 0), (6, 0)], [(0, 1), (1, 1), (2, 1), (3, 1)], [(1, 1), (2, 1), (3, 1), (4, 1)], 
[(2, 1), (3, 1), (4, 1), (5, 1)], [(3, 1), (4, 1), (5, 1), (6, 1)], [(0, 2), (1, 2), (2, 2), (3, 2)], 
[(1, 2), (2, 2), (3, 2), (4, 2)], [(2, 2), (3, 2), (4, 2), (5, 2)], [(3, 2), (4, 2), (5, 2), (6, 2)], 
[(0, 3), (1, 3), (2, 3), (3, 3)], [(1, 3), (2, 3), (3, 3), (4, 3)], [(2, 3), (3, 3), (4, 3), (5, 3)], 
[(3, 3), (4, 3), (5, 3), (6, 3)], [(0, 4), (1, 4), (2, 4), (3, 4)], [(1, 4), (2, 4), (3, 4), (4, 4)], 
[(2, 4), (3, 4), (4, 4), (5, 4)], [(3, 4), (4, 4), (5, 4), (6, 4)], [(0, 5), (1, 5), (2, 5), (3, 5)], 
[(1, 5), (2, 5), (3, 5), (4, 5)], [(2, 5), (3, 5), (4, 5), (5, 5)], [(3, 5), (4, 5), (5, 5), (6, 5)], 
[(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 1), (0, 2), (0, 3), (0, 4)], [(0, 2), (0, 3), (0, 4), (0, 5)], 
[(1, 0), (1, 1), (1, 2), (1, 3)], [(1, 1), (1, 2), (1, 3), (1, 4)], [(1, 2), (1, 3), (1, 4), (1, 5)], 
[(2, 0), (2, 1), (2, 2), (2, 3)], [(2, 1), (2, 2), (2, 3), (2, 4)], [(2, 2), (2, 3), (2, 4), (2, 5)], 
[(3, 0), (3, 1), (3, 2), (3, 3)], [(3, 1), (3, 2), (3, 3), (3, 4)], [(3, 2), (3, 3), (3, 4), (3, 5)], 
[(4, 0), (4, 1), (4, 2), (4, 3)], [(4, 1), (4, 2), (4, 3), (4, 4)], [(4, 2), (4, 3), (4, 4), (4, 5)], 
[(5, 0), (5, 1), (5, 2), (5, 3)], [(5, 1), (5, 2), (5, 3), (5, 4)], [(5, 2), (5, 3), (5, 4), (5, 5)], 
[(6, 0), (6, 1), (6, 2), (6, 3)], [(6, 1), (6, 2), (6, 3), (6, 4)], [(6, 2), (6, 3), (6, 4), (6, 5)], 
[(3, 0), (2, 1), (1, 2), (0, 3)], [(4, 0), (3, 1), (2, 2), (1, 3)], [(3, 1), (2, 2), (1, 3), (0, 4)], 
[(5, 0), (4, 1), (3, 2), (2, 3)], [(4, 1), (3, 2), (2, 3), (1, 4)], [(3, 2), (2, 3), (1, 4), (0, 5)], 
[(6, 0), (5, 1), (4, 2), (3, 3)], [(5, 1), (4, 2), (3, 3), (2, 4)], [(4, 2), (3, 3), (2, 4), (1, 5)], 
[(6, 1), (5, 2), (4, 3), (3, 4)], [(5, 2), (4, 3), (3, 4), (2, 5)], [(6, 2), (5, 3), (4, 4), (3, 5)], 
[(3, 0), (4, 1), (5, 2), (6, 3)], [(2, 0), (3, 1), (4, 2), (5, 3)], [(3, 1), (4, 2), (5, 3), (6, 4)], 
[(1, 0), (2, 1), (3, 2), (4, 3)], [(2, 1), (3, 2), (4, 3), (5, 4)], [(3, 2), (4, 3), (5, 4), (6, 5)], 
[(0, 0), (1, 1), (2, 2), (3, 3)], [(1, 1), (2, 2), (3, 3), (4, 4)], [(2, 2), (3, 3), (4, 4), (5, 5)], 
[(0, 1), (1, 2), (2, 3), (3, 4)], [(1, 2), (2, 3), (3, 4), (4, 5)], [(0, 2), (1, 3), (2, 4), (3, 5)]]

Classes:

  Conniption.py
  
  ## Alpha_Beta_Search.py ##

  This class is resposible for the game search.  The search used is iterative deepening with Alpha Beta Pruning.  The class has three methods:

   1. alpha_beta_search()
  To start a search use the method alpha_beta_search() with the parameters for the current object of the board, the integer of max depth to search, and if the search should save the visited board states and their evaluation.  **Warning**: saving visited board for a large number of run against random will consume a large amount of ram.  
  This method sets the alpha to -infinity and beta to infinity at the root of the tree. For all children states in the current board, finds the max of the value or the min_value of the children. If the value is greater than alpha, alpha is set to the value and best_state is added to a list.  The class will return the best state based on the best evaluation returned. 

  2. min_value()
  Recursion helper method of finding the max value for a given depth. The base case of the search is when it has reached the max depth. If it is at the max depth, first check if the board is in a dictionary of board and their evaluation. If so returns the eval score, else calculate the board state and save it in the dictionary. Set value to infinity and for all children states in the board passed finds the min of the value or the max_value of the children.  If the value is less than or equal to alpha, then return the value because the branch can be pruned.  If not, the method should set the beta to the min value of beta or the value.


  3. max_value()
  Recursion helper method of finding the max value for a given depth.  Base case is the same as min_value(). Next, the children states are generated of the board. Set value to -infinity and for all children states in the board passed find the max of value or min_value of the children.  If value is greater than or equal to beta, then return the value because the branch can be pruned.  If not, the method should set the alpha to the max of alpha or value.

