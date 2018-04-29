from Conniption import Conniption
from Alpha_Beta_Search import AlphaBeta
import re

def displayCommands():
    print("Available commands:")
    print("  q(uit)\tQuit the program")
    print("  h(elp)\tDisplay this menu")
    print("  d(isplay)\tDisplay the current board state")
    print("  u(ndo)\tRevert to the most recent previous state")
    print("\t\t\tNOTE: this command only allows reverting by up to one ply")
    print("  s(earch)\tPerform a search and output the suggested next move")
    print("\t\t\tNOTE: this automatically changes the current state to the")
    print("\t\t\t      suggested one.")
    print("  (f)[1-7](f)\tChange the state to the one that results from the entered move")

firstMove = 0
while firstMove != 1 and firstMove != 2:
    firstMove = int(input("Which player plays first (1 or 2)?  "))
firstMove = firstMove == 1

curBoard = Conniption(player1Turn=firstMove)
search = AlphaBeta()
searchDepth = 6

commands = re.compile("q(uit)?|h(elp)?|d(isp)?|u(ndo)?|s(earch)?|f?[1-7]{1}f?")

displayCommands()
prompt = "\nConAI> "
while True:
    com = None
    while com is None:
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
            curBoard = curBoard.parent
            print("Board state rolled back by one move.")
        else:
            print("Cannot undo past the current state.")
    #TODO: Maybe implement win/loss state checker for this and the following command.
    elif com.string[0] == "s": #search with current board as root
        if not curBoard.player1Turn:
            print("There is no reason to search when player 2 is the next person to place a piece.")
        else:
            try: curBoard.parent.parent = None #remove reference to allow garbage collection
            except: pass
            curBoard, value = search.alpha_beta_search(curBoard, searchDepth)
            print("Suggested Move: " + curBoard.resMove)
            print("Predicted path value: " + str(value))
    else:       #Move made where com.string describes that move
        if curBoard.player1Turn:
            print("You should only input specific moves when player 2 is the next person to place a piece.")
        else:
            found = False
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
print("Thanks for playing.")