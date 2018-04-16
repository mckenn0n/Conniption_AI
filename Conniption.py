import random
class Conniption:
    ##Parameters:
    #   board - a length 7 list of boolean lists where each list is no longer
    #           than length 6. This is the current configuration of the board.
    #   flips - a 2-tuple of ints. This is the number of flips remaining for each
    #           player. The first element represents player1's remaining flips,
    #           the second represents player2's. By the standard rules, the
    #           number of remaining flips can be no greater than 4 per player
    #   flippable - a boolean. Represents whether the board is currently allowed
    #               to flip. Should only be False when the board has just been
    #               flipped, but a piece was not placed immediately afterwards
    #
    ##Board configuration details:
    #   The board configuration should be interpreted such that each list is
    #   a column and they are ordered left to right. Each column should be read
    #   bottom to top, with True indicating a player1 chip and False indicating
    #   a player2 chip. For example, [[],[],[],[True,False],[],[],[]] represents
    #   a board where all columns except for the center column are empty and the
    #   center column consists only of one player2 chip above one player1 chip.
    def __init__(self, board=None, flips=(4,4), flippable=True):
        if board is not None:
            if isinstance(board, list)                                         \
            and all([isinstance(x, list) for x in board])                      \
            and all([isinstance(y,bool) for x in board for y in x]):
                if len(board) == 7 and all(len(x) <= 6 for x in board):
                    self.board = board
                else:
                    raise ValueError("Boards must have exactly 7 bool lists, " \
                               + "none of which can have more than 6 elements")
            else:
                raise TypeError("Boards must be a list of boolean lists")
        else:
            self.board = [[],[],[],[],[],[],[]]

        if isinstance(flips, tuple) and len(flips) == 2                        \
        and isinstance(flips[0], int) and isinstance(flips[1], int):
            if flips[0] >=0 and flips[0] <= 4                                  \
            and flips[1] >= 0 and flips[1] <= 4:
                self.flipsRem = flips
            else:
                raise ValueError("Number of remaining flips must between 0 and 4")
        else:
            raise TypeError("flips must be a 2-tuple of ints")

        if isinstance(flippable, bool):
            self.canFlip = flippable
        else:
            raise TypeError("flippable must be a boolean")

    ##Places a piece in the associated column.
    #   column - an int between 0 and 6. Column in which to place a piece.
    #   player - boolean. If True, then player1 is the person that is placing
    #            the current chip. If False, then the placer is player2.
    #
    #   This method causes flips to be allowed if they are currently disallowed
    #   due to the most recent flip being too recent.
    def placePiece(self, column, player):
        if not isinstance(player, bool):
            raise TypeError("Player must be a boolean")

        if isinstance(column, int) and column >= 0 and column <= 6:
            if len(self.board[column]) < 6:
                self.board[column].append(player)
                self.canFlip = True
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
    def flip(self, player):
        if not isinstance(player, bool):
            raise TypeError("Player must be a boolean")
        if not self.canFlip:
            raise RuntimeError("A piece must be placed before board can be flipped")

        if player:
            if self.flipsRem[0] == 0:
                raise RuntimeError("Player 1 is out of flips")
            self.flipsRem = (self.flipsRem[0] - 1, self.flipsRem[1])
        else:
            if self.flipsRem[1] == 0:
                raise RuntimeError("Player 2 is out of flips")
            self.flipsRem = (self.flipsRem[0], self.flipsRem[1] - 1)

        self.board = [list(reversed(x)) for x in self.board]
        self.canFlip = False

    #TODO: IMPLEMENT: This should be the objective function for comparing boards
    #                 Should return an int/float. For Consistency, player1
    #                 advantage should be positive and player2 advantage
    #                 should be negative.
    def evalBoard(self):
        pass

    ##This returns all of the states that are legally reachable by the end of the
    # current (half) turn. This method will generate all children states that
    # include no flips(noFlip), a flip before placing a chip(preFlip), a flip
    # after placing a chip(postFlip), and a flip both before and after placing
    # a chip(dualFlip).
    #
    # Parameter:
    #   player - boolean. Indicates which player will be placing a piece for this
    #            turn. True indicates that it is player1's turn and False
    #            indicates that it is player2's turn.
    #NOTE: This needs to be made as efficient as possible, as this will be one of
    #      the major bottlenecks. Can currently generate all 28 possible children
    #      of a given board state almost 4000 times per second on my machine
    def genChildStates(self, player):
        #Generate no flip children here
        noFlip = [(self.board[:c]+[self.board[c]+[player]]+self.board[c+1:],self.flipsRem,True) for c in range(7) if len(self.board[c]) < 6]
        if self.canFlip or self.flipsRem[0 if player else 1] > 0:
            flipped = [list(reversed(c)) for c in self.board]
        else:
            return [Conniption(b[0],b[1],b[2]) for b in noFlip]
        
        #Generate post-flip children here
        if self.flipsRem[0 if player else 1] > 0:
            remFlips = (self.flipsRem[0]-1, self.flipsRem[1]) if player else (self.flipsRem[0],self.flipsRem[1]-1)
            postFlip = [(flipped[:c]+[[player]+flipped[c]]+flipped[c+1:],remFlips,True) for c in range(7) if len(flipped[c]) < 6]
        else:
            postFlip = []

        #Generate pre-flip and dual-flip children here
        fr = self.flipsRem[0 if player else 1]
        if self.canFlip and fr > 0:
            remFlips = (self.flipsRem[0]-1, self.flipsRem[1]) if player else (self.flipsRem[0],self.flipsRem[1]-1)
            preFlip = [(flipped[:c]+[flipped[c]+[player]]+flipped[c+1:],remFlips,True) for c in range(7) if len(flipped[c]) < 6]

            if fr > 1:
                remFlips = (self.flipsRem[0]-1, self.flipsRem[1]) if player else (self.flipsRem[0],self.flipsRem[1]-1)
                dualFlip = [(self.board[:c]+[[player]+self.board[c]]+self.board[c+1:],remFlips,True) for c in range(7) if len(self.board[c]) < 6]
            else:
                dualFlip = []
        else:
            preFlip = []
            dualFlip = []
        
        return [Conniption(b[0],b[1],b[2]) for b in noFlip + preFlip + postFlip + dualFlip]

    ##May be useful later for comparing boards to prevent revisiting equivalent
    # states. Usefulness might be less than previously expected, however, due to
    # inability to place a Conniption object in a set. This may be able to be
    # worked around by defining an appropriate __hash__() function (possibly just
    # concatenated string version of all three parameters.
    #       E.g. str(self.board) + str(self.flipsRem) + str(self.canFlip))
    def __eq__(self, connip):
        if self.canFlip == connip.canFlip                                      \
        and self.flipsRem == connip.flipsRem                                   \
        and self.board == connip.board:
            return True
        else:
            return False

    ##For the purposes of the printing of the board, player1 chips will be
    # represented by the char "W" and player2 chips by the char "B". The char
    # "o" represents an empty space
    def __str__(self):
        retStr = ""
        for y in range(5,-1,-1):
            for x in range(0,7):
                try:
                    retStr += "W " if self.board[x][y] else "B "
                except:
                    retStr += "o "
            retStr = retStr[:-1] + "\n"
        retStr += "White flips:  " + str(self.flipsRem[0]) + "\n"
        retStr += "Blue flips:   " + str(self.flipsRem[1]) + "\n"
        retStr += "Able to flip: " + str(self.canFlip)
        return retStr

    ##May want to change this. FYI: this method defines how a object is printed when
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

    return Conniption(board, flips, canFlip)

if __name__ == "__main__":
    t, f  = True, False
    b = [[t,f],[f,t],[t,f],[f,t],[t,f],[f,t],[t,f]]
    randBoard = Conniption(b)
    x = randBoard.genChildStates(True)
    print(randBoard)
    print("Possible moves: " + str(len(x)))
