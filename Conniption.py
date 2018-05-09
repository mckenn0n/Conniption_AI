import random
from tqdm import tqdm

win_lines = [[(0, 0), (1, 0), (2, 0), (3, 0)], [(1, 0), (2, 0), (3, 0), (4, 0)], [(2, 0), (3, 0), (4, 0), (5, 0)], 
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

us_weights   = [0, 1, 8, 128, 99999]
them_weights = [0, -1, -16, -200, -99999]

class Conniption:
	defaultBoard = (tuple(),tuple(), tuple(), tuple(), tuple(), tuple(), tuple())
	##Parameters:
	#   board - a length 7 list of boolean lists where each list is no longer
	#		   than length 6. This is the current configuration of the board.
	#   player1Turn - True if the AI is the next player to place a piece, False
	#				  otherwise
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
	#   a player2 chip. For example, ((),(),(),(True,False),(),(),()) represents
	#   a board where all columns except for the center column are empty and the
	#   center column consists only of one player2 chip above one player1 chip.
	#
	def __init__(self, board=defaultBoard, player1Turn=True,flips=(4,4), flippable=True, parent=None, resultingMove=None):
		self.board = board
		self.flipsRem = flips
		self.canFlip = flippable
		self.player1Turn = player1Turn
		self.parent = parent
		self.resMove = resultingMove
		self.children = None

	def betterEval(self):
		win = isWin(self.board)
		if win[0]:
			if win[1]:
				if self.player1Turn:
					return 1000000 - ((self.flipsRem[1] - self.flipsRem[0]) * 10000)
				else:
					return -1000000 
			else:
				return 1000000 - ((self.flipsRem[1] - self.flipsRem[0]) * 10000)
		elif win[1]:
			return -1000000 
		one_score = 0
		b = [[self.board[col][row] for row in range(len(self.board[col]))] + [None] * (6 - len(self.board[col])) for col in range(7)]
		isVert = lambda x: x[0][0] == x[1][0] == x[2][0] == x[3][0]
		for line in win_lines:
			lineWeight = 0
			if not isVert(line):
				p1Sum = sum(1 for i in range(4) if b[line[i][0]][line[i][1]] is True)
				p1Sum -= sum(1 for i in range(4) if b[line[i][0]][line[i][1]] is False)
				if p1Sum > 0:
					if p1Sum == 3:
						lineWeight = 2000
					elif p1Sum == 4:
						return 1000000 - ((self.flipsRem[1] - self.flipsRem[0]) * 10000)
					else:
						lineWeight = us_weights[sum(1 for i in range(4) if b[line[i][0]][line[i][1]] is True)]
				elif p1Sum < 0:
					lineWeight = p1Sum * them_weights[sum(1 for i in range(4) if b[line[i][0]][line[i][1]] is False)]
			else:
				p1Sum = sum(1 for i in range(4) if b[line[i][0]][line[i][1]] is True)
				p2Sum = sum(1 for i in range(4) if b[line[i][0]][line[i][1]] is False)
				if p1Sum > 0:
					if p2Sum == 0:
						lineWeight = us_weights[p1Sum]
				elif p2Sum > 0:
					lineWeight = p2Sum * them_weights[p2Sum]
			one_score += lineWeight
		diffWeight = ((self.flipsRem[0] - self.flipsRem[1]) ** 2) * 1000
		if self.flipsRem[0] < self.flipsRem[1]: diffWeight = -diffWeight
		one_score += diffWeight
		one_score += 150 if self.canFlip else -150
		return one_score


	##This returns all of the states that are legally reachable by the end of the
	# current (half) turn. This method will generate all children states that
	# include no flips(noFlip), a flip before placing a chip(preFlip), a flip
	# after placing a chip(postFlip), and a flip both before and after placing
	# a chip(dualFlip).
	def genChildStates(self):
		
		if self.children is not None: return
		order = [3,2,4,1,5,0,6]
		nextTurn = not self.player1Turn
		#Generate no flip children here
		self.children = {Conniption(self.board[:c]+((self.board[c]+(self.player1Turn,)),)+self.board[c+1:],nextTurn,self.flipsRem,True,self,str(c+1)) for c in order if len(self.board[c]) < 6}	#NoFlip
		fr = self.flipsRem[0 if self.player1Turn else 1]
		if fr > 0:  #Required for all flips
			flipped = tuple(tuple(reversed(c)) for c in self.board)
			remFlips = (self.flipsRem[0]-1, self.flipsRem[1]) if self.player1Turn else (self.flipsRem[0],self.flipsRem[1]-1)
			self.children |= {Conniption(flipped[:c]+(((self.player1Turn,)+flipped[c]),)+flipped[c+1:],nextTurn,remFlips,False,self,str(c+1)+"f") for c in order if len(flipped[c]) < 6}	#PostFlip
			if self.canFlip: #Required for preFlip and dualFlip
				self.children |= {Conniption(flipped[:c]+((flipped[c]+(self.player1Turn,)),)+flipped[c+1:],nextTurn,remFlips,True,self,"f"+str(c+1)) for c in order if len(flipped[c]) < 6}	#PreFlip
				if fr > 1: #Required for dualFlip
					remFlips = (self.flipsRem[0]-2, self.flipsRem[1]) if self.player1Turn else (self.flipsRem[0],self.flipsRem[1]-2)
					self.children |= {Conniption(self.board[:c]+(((self.player1Turn,)+self.board[c]),)+self.board[c+1:],nextTurn,remFlips,False,self,"f"+str(c+1)+"f") for c in order if len(self.board[c]) < 6}	#DualFlip
		""" MORE READABLE VERSION OF THE ABOVE. WILL LIKELY BE NOTABLY SLOWER
		if self.children is not None: return
		order = [3,2,4,1,5,0,6]
		nextTurn = not self.player1Turn
		self.children = set()
		flipped = tuple(tuple(reversed(c)) for c in self.board)
		fr = self.flipsRem[0 if self.player1Turn else 1]	#number of flips the current player has available still
		singRemFlips = (self.flipsRem[0]-1, self.flipsRem[1]) if self.player1Turn else (self.flipsRem[0],self.flipsRem[1]-1) #subtracts 1 from current player's remaiing flips
		dualRemFlips = (self.flipsRem[0]-2, self.flipsRem[1]) if self.player1Turn else (self.flipsRem[0],self.flipsRem[1]-2) #subtracts 2 from current player's remaiing flips
		for col in order:
			if len(self.board[col]) < 6: #required for adding to the current column
				#Weird parenthesis structure is necessary to ensure that tuples of tuples are concatenated and not inserted into previous
				#I.E.
				#	current result: ((),(),(),(),(),(),())
				#	result with fewer paren: ((),(),((),(),(),())) or some variation of this
				noFlip = self.board[:col]+((self.board[col]+(self.player1Turn,)),)+self.board[col+1:] #places piece at end of current column's tuple
				self.children.add(Conniption(noFlip, nextTurn, self.flipsRem, True, self, str(col+1)))
				if fr > 0:	#required for flips to be possible
					postFlip = flipped[:col]+(((self.player1Turn,)+flipped[col]),)+flipped[col+1:] #places piece at beginning of flipped version of current column's tuple
					self.children.add(Conniption(postFlip, nextTurn, singRemFlips, False, self, str(col+1)+"f"))
					if self.canFlip:  #required for flips at beginning of ply (pre and dual flips)
						preFlip = flipped[:col]+((flipped[col]+(self.player1Turn,)),)+flipped[col+1:] #places piece at end of flipped version of current column's tuple
						self.children.add(Conniption(preFlip, nextTurn, singRemFlips, True, self, "f"+str(col+1)))
						if fr > 1:  #required for dualflips
							dualFlip = self.board[:col]+(((self.player1Turn,)+self.board[col]),)+self.board[col+1:] #places piece at beginning of current column's tuple
							self.children.add(Conniption(dualFlip, nextTurn, dualRemFlips, False, self, "f"+str(col+1)+"f"))
		"""

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

	def __hash__(self):
		return hash(self.board) + hash(self.player1Turn) + hash(self.flipsRem) + hash(self.canFlip)

	##For the purposes of the printing of the board, player1 chips will be
	# represented by the char "W" and player2 chips by the char "B". The char
	# "o" represents an empty space
	def __str__(self):
		retStr = "|\033[2;30;47m1\033[0m|\033[2;30;47m2\033[0m|\033[2;30;47m3\033[0m|\033[2;30;47m4\033[0m|\033[2;30;47m5\033[0m|\033[2;30;47m6\033[0m|\033[2;30;47m7\033[0m|\n"
		for y in range(5,-1,-1):
			for x in range(0,7):
				try:
					retStr += "|\033[1;37;40mW\33[0m" if self.board[x][y] else "|\033[1;36;40mB\033[0m"
				except:
					retStr += "|\033[1;30;40mo\033[0m"
			retStr = retStr + "|\n"
		retStr += "White flips:  " + str(self.flipsRem[0]) + "\n"
		retStr += "Blue flips:   " + str(self.flipsRem[1]) + "\n"
		retStr += "Able to flip: " + str(self.canFlip) + "\n"
		retStr += "Player " + ("1" if self.player1Turn else "2") + " places next"
		return retStr

	def __repr__(self):
		return self.__str__()

#Checks for a win state
def isWin(board):
	p1Win = False
	p2Win = False
	for l in win_lines:
		try:
			if board[l[0][0]][l[0][1]] == board[l[1][0]][l[1][1]] == board[l[2][0]][l[2][1]] == board[l[3][0]][l[3][1]]:
				if board[l[0][0]][l[0][1]]:
					p1Win = True
				else:
					p2Win = True
		except:
			pass
	return p1Win, p2Win

if __name__ == "__main__":
	t, f  = True, False
	b = ((t,f),(f,t),(t,f),(f,t),(t,f),(f,t),(t,f))
	testBoard = Conniption(b,player1Turn=True)
	testBoard.genChildStates()
	print(testBoard.children)
