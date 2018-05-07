from Conniption import Conniption
import time

## Global dictionary to save states and their evaluations
visited = {}


class AlphaBeta:

	##Parameters:
	#   board - Conniption object which holds the state of the board
	#   max_depth - a integer representing the depth the min-max search
	#	saveVistied - a Boolean value to save visited states or not
	#	
	#	Outputs - a Conniption object with the best next move based on the max search depth
	#	Note: saveVisited is defaulted to false to reduce overhead
	def alpha_beta_search(self, board, max_depth, saveVisited=True):
		self.max_depth = max_depth
		self.saveVisited = saveVisited
		infinity = float('inf')
		alpha = -infinity
		beta = infinity

		depth = 0
		best_state = None
		board.genChildStates()

		best_states = []

		for i in range(1,max_depth+1):
			value = 0
			for state in board.children:
				value = self.min_value(state, depth+1, i, alpha, beta)
				if value > alpha:
					alpha = value
					best_state = state
			if value > 1000000 and i == 1:
				return best_state,value
			best_states.append([best_state, value])
		print(*best_states, sep="\n")			#For testing purposes
		return max(best_states, key=lambda x: x[1])

	##Parameters:
	#	state - Conniption object that contains future state of the board
	#	depth - Integer that holds the current depth of the search
	#	max_depth -  Integer of max depth to search
	#	alpha - holds the max value
	#	beta - holds the min value
	# 	
	#	Note: recursion helper method of finding the max value for a given depth
	def max_value(self, state, depth, max_depth, alpha, beta):
		if depth >= max_depth:
			if self.saveVisited:
				global visited
				if state in visited:
					return visited.get(state)
				else:
					eval = state.testSecondEval()
					visited[state]= eval
					return eval
			else:
				return state.testSecondEval()

		infinity = float('inf')
		value = -infinity
		state.genChildStates()

		for s in state.children:
			value = max(value, self.min_value(s, depth+1, max_depth,alpha, beta))
			if value >= beta:
				return value
			alpha = max(alpha, value)
			#print("alpha: "+str(alpha)) 	#For Testing purposes
		return value

	##Parameters:
	#	state - Conniption object that contains future state of the board
	#	depth - Integer that holds the current depth of the search
	#	max_depth -  Integer of max depth to search
	#	alpha - holds the max value
	#	beta - holds the min value
	# 	
	#	Note: recursion helper method of finding the max value for a given depth
	def min_value(self, state, depth, max_depth, alpha, beta):
		if depth >= max_depth:
			if self.saveVisited:
				global visited
				if state in visited:
					return visited.get(state)
				else:
					eval = state.testSecondEval()
					visited[state]= eval
					return eval
			else:
				return state.testSecondEval()

		infinity = float('inf')
		value = infinity
		state.genChildStates()

		for s in state.children:
			value = min(value, self.max_value(s, depth+1, max_depth, alpha, beta))
			if value <= alpha:
				return value
			beta = min(beta, value)
			#print("beta: "+str(beta)) 	#For testing purposes
		return value

##Generate a random board for testing purposes
if __name__ == "__main__":
	t, f  = True, False
	b = ((f,f,f),tuple(),tuple(),(t,),(t,),(t,),tuple())
	testBoard = Conniption(b, True, (4,4), True)
	start = time.time()
	search = AlphaBeta()
	start = time.time()
	result = search.alpha_beta_search(testBoard,6)
	print(time.time() - start)
	print(result[0],'\nScore for player is',result[1])
	
