from Conniption import Conniption, isWin
from Alpha_Beta_Search import AlphaBeta
import re
import time
from random import randint


def displayCommands():
	print("Available commands:")
	print("  q(uit)\tQuit the program")
	print("  h(elp)\tDisplay this menu")
	print("  d(isplay)\tDisplay the current board state")
	print("  u(ndo)\tRevert to the most recent previous state")
	print("\t\t\tNOTE: this command only allows reverting by two ply")
	print("  (f)[1-7](f)\tChange the state to the one that results from the entered move")
	
	print("\n**Players**")
	print("  1) White will always be the opponent\n  W = White\n  2) Blue will always be you (The player)\n  B = Blue")

def checkWins(board, move, player1Turn):
	curBoard = [list(c) for c in board]
	for c in move:
		if c == 'f':
			curBoard = [list(reversed(col)) for col in curBoard]
		else:
			curBoard[int(c) - 1].append(player1Turn)
		wins = isWin(curBoard)
		if wins[0] == wins[1]:
			if wins[0]: #both have line of 4
				return (1 if player1Turn else -1)
		else:
			if wins[0]: #player1 has line of 4
				return 1
			else: #player2 has line of 4
				return -1
	return 0

ai_wins = 0
ai_lose = 0 #This is not needed. Just used for testing to make sure there is no duble counting.
player_two_rand = False
firstMove = 0
print("**Players**")
print("  1) White will always be the AI\n  2) Blue will always be the player\n") #TAGGED as made more understandable
while firstMove != 1 and firstMove != 2:
	firstMove = input("Which color plays first (1 = White or 2 = Blue)?  ") #TAGGED as made more understandable
	if firstMove != "1" and firstMove != "2": #TAGGED as solve crashing problem
		print("\n  Please enter '1' for White, or '2' for Blue\n")
		firstMove = 0
	else:
		firstMove = int(firstMove)
firstMove = firstMove == 1
choice = ''
while choice != "y" and choice != "n":
	choice = input("Would you like Blue to be placed randomly? (Yes or No)  ")
if choice[0].lower() == "y":
	player_two_rand = True

rep = int(input("How many times would you like to play the game with these settings?  ")) #number for for loop

for i in range(rep):
	curBoard = Conniption(player1Turn=firstMove)
	search = AlphaBeta()
	if choice[0].lower() == "y":
		searchDepth = 4
	else:
		if(firstMove):
			searchDepth = 6 #Search depth of 5 is good for when AI goes second
		else:
			searchDepth = 5
	commands = re.compile("q(uit)?|h(elp)?|d(isp)?|u(ndo)?|s(earch)?|f?[1-7]{1}f?")

	displayCommands()
	prompt = "\nConAI> "
	while True:
		com = None
		while com is None:
			if curBoard.player1Turn: 
				com = re.fullmatch(commands, 's') #Auto search on AI turn
			else:
				if player_two_rand:
					one = ''
					two = ''
					if curBoard.flipsRem[1] != 0:
						if randint(0,11) == 3: one = 'f'
						if randint(0,11) == 8: two = 'f'
					com = re.fullmatch(commands, one+str(randint(1,7))+two) #Random play
				else:
					com = re.fullmatch(commands, input(prompt).lower()) 
			if com is None: print("Invalid command. Type 'h' or 'help' to see a list of allowed commands.")

		if   com.string[0] == "q": #quit
			break
		elif com.string[0] == "h": #dislpay command list
			displayCommands()
		elif com.string[0] == "d": #display current board state
			print(curBoard)
		elif com.string[0] == "u": #undo most recent move
			if curBoard.parent is not None:
				curBoard = curBoard.parent.parent
				print("Board state rolled back by one move.")
			else:
				print("Cannot undo past the current state.")
			print('\n',curBoard, sep = '') #TAGGED as make game easier to play.
		elif com.string[0] == "s": #search with current board as root
			if not curBoard.player1Turn:
				print("There is no reason to search when player 2 is the next person to place a piece.")
			else:
				try: curBoard.parent.parent = None #remove reference to allow garbage collection
				except: pass
				start = time.time()
				if choice[0].lower() == 'y':
					curBoard, value = search.alpha_beta_search(curBoard, searchDepth, False)
				else:
					curBoard, value = search.alpha_beta_search(curBoard, searchDepth)
				print(time.time() - start)
				win = checkWins(curBoard.parent.board, curBoard.resMove, not curBoard.player1Turn)
				print("Suggested Move: " + curBoard.resMove)
				print("Predicted path value: " + str(value))
				print('\nRep '+str(i+1)+'\n',curBoard, sep = '') #TAGGED as make game easier to play.
				if win == 1: 
					print("Player1 has won")
					ai_wins += 1
					break
				elif win == -1: 
					print("Player2 has won")
					ai_lose += 1
					break
		else:       #Move made where com.string describes that move
			if curBoard.player1Turn:
				print("You should only input specific moves when player 2 is the next person to place a piece.")
			else:
				found = False
				win = checkWins(curBoard.board, com.string, curBoard.player1Turn)
				curBoard.genChildStates()
				for ch in curBoard.children:
					if ch.resMove == com.string:
						try: curBoard.parent.parent = None #remove reference to allow garbage collection
						except: pass
						curBoard = ch
						found = True
				if not found:
					print(com.string + " is not a legal move.")
				else:
					print("Player 2 played move " + com.string + ".")
					print('\nRep '+str(i+1)+'\n',curBoard, sep = '') #TAGGED as make game easier to play.
				if win == 1: 
					print("Player1 has won")
					ai_wins += 1
					break
				elif win == -1: 
					print("Player2 has won")
					ai_lose += 1
					break
print("Thanks for playing.\n", ai_wins, '\n'+str(ai_lose), sep = '')