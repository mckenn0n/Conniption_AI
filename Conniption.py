import random
from tqdm import tqdm

class Conniption:
	defaultBoard = (tuple(),tuple(), tuple(), tuple(), tuple(), tuple(), tuple())
	##Parameters:
	#   board - a length 7 list of boolean lists where each list is no longer
	#		   than length 6. This is the current configuration of the board.
	#   flips - a 2-tuple of ints. This is the number of flips remaining for each
	#		   player. The first element represents player1's remaining flips,
	#		   the second represents player2's. By the standard rules, the
	#		   number of remaining flips can be no greater than 4 per player
	#   flippable - a boolean. Represents whether the board is currently allowed
	#			   to flip. Should only be False when the board has just been
	#			   flipped, but a piece was not placed immediately afterwards
	#
	##Board configuration details:
	#   The board configuration should be interpreted such that each list is
	#   a column and they are ordered left to right. Each column should be read
	#   bottom to top, with True indicating a player1 chip and False indicating
	#   a player2 chip. For example, [[],[],[],[True,False],[],[],[]] represents
	#   a board where all columns except for the center column are empty and the
	#   center column consists only of one player2 chip above one player1 chip.
	#
	#NOTE: If board is not passed as a parameter, then defaults for every field
	#      will be used, regardless of whether they are included.
	def __init__(self, board=defaultBoard, player1Turn=True,flips=(4,4), flippable=True, parent=None, resultingMove=None):
		self.board = board
		self.flipsRem = flips
		self.canFlip = flippable
		self.player1Turn = player1Turn
		self.parent = parent
		self.resMove = resultingMove
		self.us_weights = [0, 1, 8, 128, 99999, 99999, 99999, 99999]
		self.them_weights = [0, 1, 8, 128, 99999, 99999, 99999, 99999]
		self.children = None

	##Places a piece in the associated column.
	#   column - an int between 0 and 6. Column in which to place a piece.
	#   player - boolean. If True, then player1 is the person that is placing
	#			the current chip. If False, then the placer is player2.
	#
	#   This method causes flips to be allowed if they are currently disallowed
	#   due to the most recent flip being too recent.
	#
	#   DEPRECATED (Likely Not Necessary due to no need to alter current board state)
	#		Remove if not used in final product
	def placePiece(self, column):
		if isinstance(column, int) and column >= 0 and column <= 6:
			if len(self.board[column]) < 6:
				self.board[column] += (self.player1Turn,)
				self.canFlip = True
				self.player1Turn = not self.player1Turn
			else:
				raise RuntimeError("Column " + str(column) + " is full.")
		else:
			raise ValueError("Columns can only be an int between 0 and 6")

	##Flips the entire board once.
	#   player - boolean. If True, then player1 is the person   that is flipping
	#   the board. If False, then the flipper is player2.
	#
	#   This method disallows further flipping until the method placePiece is
	#   called.
	#
	#   DEPRECATED (Likely Not Necessary due to no need to alter current board state)
	#		Remove if not used in final product
	def flip(self):
		if self.player1Turn:
			if self.flipsRem[0] == 0:
				raise RuntimeError("Player 1 is out of flips")
			self.flipsRem = (self.flipsRem[0] - 1, self.flipsRem[1])
		else:
			if self.flipsRem[1] == 0:
				raise RuntimeError("Player 2 is out of flips")
			self.flipsRem = (self.flipsRem[0], self.flipsRem[1] - 1)

		self.board = [tuple(reversed(x)) for x in self.board]
		self.canFlip = False

	#TODO: IMPLEMENT: This should be the objective function for comparing boards
	#				 Should return an int/float. For Consistency, player1
	#				 advantage should be positive and player2 advantage
	#				 should be negative.
	#IDEA: extend every chip line to length 4 or until blocked and count number of lines that are = length 4
	#			then subtract the same for opponent. Adding the result from the flipped version
	#			of the board will allow considering of flip results. Probably would need to add
	#			the current length of that line to allow weighting of partial lines.
	#				PROBLEM: doesn't consider broken lines that can be improved using flip moves.
	#					ex.	on board below, neither broken line of 3 will be considered despite being very valuable
	#						o o o o o o o
	#						o o o o o o o
	#						o o o W o o o
	#						o o o B W o o
	#						o o o B B B o
	#						o o o W B W W
	#					Another problem: not affected by the number of remaining flips or (maybe) possibility of flips
	def evalBoard(self):
		# Two sets of weights, one for the us (our AI) and one for them (their AI)
		one_score = 0
		b = [list(c) for c in self.board]
		p1Lines, p2Lines = genPosLines(b)
		for c in range(7):
			for r in range(6):
				for li in range(4):
					one_score += self.us_weights[p1Lines[c][r][li]] - self.them_weights[p2Lines[c][r][li]]

		flipped = [list(reversed(c)) for c in self.board]
		p1Lines, p2Lines = genPosLines(flipped)
		for c in range(7):
			for r in range(6):
				for li in range(4):
					one_score += self.us_weights[p1Lines[c][r][li]] - self.them_weights[p2Lines[c][r][li]]
		diffWeight = ((self.flipsRem[0] - self.flipsRem[1]) ** 2) * 50
		if self.flipsRem[0] < self.flipsRem[1]: diffWeight = -diffWeight
		one_score += diffWeight
		one_score += 150 if self.canFlip else -150

		return one_score

	##This returns all of the states that are legally reachable by the end of the
	# current (half) turn. This method will generate all children states that
	# include no flips(noFlip), a flip before placing a chip(preFlip), a flip
	# after placing a chip(postFlip), and a flip both before and after placing
	# a chip(dualFlip).
	#
	# Parameter:
	#   player - boolean. Indicates which player will be placing a piece for this
	#			turn. True indicates that it is player1's turn and False
	#			indicates that it is player2's turn.
	#NOTE: This needs to be made as efficient as possible, as this will be one of
	#	  the major bottlenecks. Can currently generate all 28 possible children
	#	  of a given board state almost 3500 times per second on my machine
	def genChildStates(self):
		if self.children is not None: return
		nextTurn = not self.player1Turn
		#Generate no flip children here
		self.children = {Conniption(self.board[:c]+((self.board[c]+(self.player1Turn,)),)+self.board[c+1:],nextTurn,self.flipsRem,True,self,str(c+1)) for c in range(7) if len(self.board[c]) < 6}	#NoFlip
		fr = self.flipsRem[0 if self.player1Turn else 1]
		if fr > 0:  #Required for all flips
			flipped = tuple(tuple(reversed(c)) for c in self.board)
			remFlips = (self.flipsRem[0]-1, self.flipsRem[1]) if self.player1Turn else (self.flipsRem[0],self.flipsRem[1]-1)
			self.children |= {Conniption(flipped[:c]+(((self.player1Turn,)+flipped[c]),)+flipped[c+1:],nextTurn,remFlips,False,self,str(c+1)+"f") for c in range(7) if len(flipped[c]) < 6}	#PostFlip
			if self.canFlip: #Required for preFlip and dualFlip
				self.children |= {Conniption(flipped[:c]+((flipped[c]+(self.player1Turn,)),)+flipped[c+1:],nextTurn,remFlips,True,self,"f"+str(c+1)) for c in range(7) if len(flipped[c]) < 6}	#PreFlip
				if fr > 1: #Required for dualFlip
					remFlips = (self.flipsRem[0]-2, self.flipsRem[1]) if self.player1Turn else (self.flipsRem[0],self.flipsRem[1]-2)
					self.children |= {Conniption(self.board[:c]+(((self.player1Turn,)+self.board[c]),)+self.board[c+1:],nextTurn,remFlips,False,self,"f"+str(c+1)+"f") for c in range(7) if len(self.board[c]) < 6}	#DualFlip

	##May be useful later for comparing boards to prevent revisiting equivalent
	# states.
	def __eq__(self, connip):
		if self.board == connip.board											\
		and self.player1Turn == connip.player1Turn								\
		and self.flipsRem == connip.flipsRem									\
		and self.canFlip == connip.canFlip:
			return True
		else:
			return False

	def __ne__(self,connip):
		if self.board != connip.board											\
		or self.player1Turn != connip.player1Turn								\
		or self.flipsRem != connip.flipsRem										\
		or self.canFlip != connip.canFlip:
			return True
		else:
			return False

	##This is needed in order to make sets of states.
	def __hash__(self):
		return hash(self.board) + hash(self.player1Turn) + hash(self.flipsRem) + hash(self.canFlip)

	##For the purposes of the printing of the board, player1 chips will be
	# represented by the char "W" and player2 chips by the char "B". The char
	# "o" represents an empty space
	def __str__(self):
		retStr = ""
		for y in range(5,-1,-1):
			for x in range(0,7):
				try:
					retStr += "\033[1;37;40mW\33[0m " if self.board[x][y] else "\033[1;36;40mB\033[0m "
				except:
					retStr += "o "
			retStr = retStr[:-1] + "\n"
		retStr += "White flips:  " + str(self.flipsRem[0]) + "\n"
		retStr += "Blue flips:   " + str(self.flipsRem[1]) + "\n"
		retStr += "Able to flip: " + str(self.canFlip) + "\n"
		retStr += "Player " + ("1" if self.player1Turn else "2") + " places next"
		return retStr

	##May want to change this. FYI: this method defines how an object is printed when
	# you print an object that contains a conniption board. For example, this prevents
	# print([Conniption()]) from yielding the string "[<Conniption object at x...>]"
	#
	# Not a necessary change, but may be helpful for debugging purposes
	def __repr__(self):
		return self.__str__()


##Generates a random board state for testing purposes. Can be removed from final version
def genRandomState():
	board = [[random.random() < 0.5 for _ in range(random.randint(0,5))] for _ in range(7)]
	flips = (random.randint(0,4), random.randint(0,4))
	canFlip = random.random() < 0.5
	player1Turn = random.random() < 0.5

	return Conniption(board, player1Turn, flips, canFlip)

#SHOULD ONLY BE CALLED FROM THE evalBoard METHOD 
def genPosLines(board):
	pos = []
	neg = []
	for c in range(7):
		pos.append([])
		neg.append([])
		for r in range(6):
			try:
				if board[c][r]:
					pos[c].append(True)
					neg[c].append(False)
				else:
					pos[c].append(False)
					neg[c].append(True)
			except:
				pos[c].append(True)
				neg[c].append(True)
	pos[0][0] = [1,1,1,1] if pos[0][0] else [0,0,0,0]
	neg[0][0] = [1,1,1,1] if neg[0][0] else [0,0,0,0]

	for c in range(1,7):
		if pos[c][0]:
			pos[c][0] = [1,pos[c-1][0][1] + 1,1,1]
			pos[c-1][0][1] = 0
		else:
			pos[c][0] = [0,0,0,0]
			if pos[c-1][0][1] < 4: pos[c-1][0][1] = 0
		if neg[c][0]:
			neg[c][0] = [1,neg[c-1][0][1] + 1,1,1]
			neg[c-1][0][1] = 0
		else:
			neg[c][0] = [0,0,0,0]
			if neg[c-1][0][1] < 4: neg[c-1][0][1] = 0

	for r in range(1,6):
		if not pos[0][r]:
			pos[0][r] = [1,1,1,pos[0][r-1][3]+1]
			pos[0][r-1][3] = 0
		else:
			pos[0][r] = [0,0,0,0]
			if pos[0][r-1][3] < 4: pos[0][r-1][3] = 0
		if not neg[0][r]:
			neg[0][r] = [1,1,1,neg[0][r-1][3]+1]
			neg[0][r-1][3] = 0
		else:
			neg[0][r] = [0,0,0,0]
			if neg[0][r-1][3] < 4: neg[0][r-1][3] = 0

	for c in range(1,7):
		for r in range(1,6):
			if pos[c][r]:
				if r == 5:
					pos[c][r] = [1, pos[c-1][r][1] + 1, pos[c-1][r-1][2] + 1, pos[c][r-1][3] + 1]
					pos[c-1][r][1], pos[c-1][r-1][2], pos[c][r-1][3] = 0,0,0
				else:
					pos[c][r] = [pos[c-1][r+1][0] + 1, pos[c-1][r][1] + 1, pos[c-1][r-1][2] + 1, pos[c][r-1][3] + 1]
					pos[c-1][r+1][0], pos[c-1][r][1], pos[c-1][r-1][2], pos[c][r-1][3] = 0,0,0,0
			else:
				pos[c][r] = [0,0,0,0]
				if r != 5 and pos[c-1][r+1][0] < 4: pos[c-1][r+1][0] = 0
				if pos[c-1][r][1] < 4: pos[c-1][r][1] = 0
				if pos[c-1][r-1][2] < 4: pos[c-1][r-1][2] = 0
				if pos[c][r-1][3] < 4: pos[c][r-1][3] = 0
			if neg[c][r]:
				if r == 5:
					neg[c][r] = [1, neg[c-1][r][1] + 1, neg[c-1][r-1][2] + 1, neg[c][r-1][3] + 1]
					neg[c-1][r][1], neg[c-1][r-1][2], neg[c][r-1][3] = 0,0,0
				else:
					neg[c][r] = [neg[c-1][r+1][0] + 1, neg[c-1][r][1] + 1, neg[c-1][r-1][2] + 1, neg[c][r-1][3] + 1]
					neg[c-1][r+1][0], neg[c-1][r][1], neg[c-1][r-1][2], neg[c][r-1][3] = 0,0,0,0
			else:
				neg[c][r] = [0,0,0,0]
				if r != 5 and neg[c-1][r+1][0] < 4: neg[c-1][r+1][0] = 0
				if neg[c-1][r][1] < 4: neg[c-1][r][1] = 0
				if neg[c-1][r-1][2] < 4: neg[c-1][r-1][2] = 0
				if neg[c][r-1][3] < 4: neg[c][r-1][3] = 0

	return pos,neg

if __name__ == "__main__":
	t, f  = True, False
	b = ((t,f),(f,t),(t,f),(f,t),(t,f),(f,t),(t,f))
	testBoard = Conniption(b,player1Turn=True)
	for _ in tqdm(range(30000)):
		testBoard.evalBoard()
	print(testBoard.evalBoard())