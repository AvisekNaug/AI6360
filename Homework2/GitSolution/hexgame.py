# -*- coding: utf-8 -*-
"""
This package defines a Hexboard class to manipulate hexboards.

Code examples
    hb = Hexboard(5)  # create a 5x5 hexboard
    
    # Set up the board row by row. 
    # Empty cells are coded with 0, white stones with +1, black stones with -1
    hb.set_board([0,0,-1,-1,0, 0,1,-1,0,0, 0,0,-1,-1,0, 0,0,-1,+1,+1 ,0,-1,+1,0,+1 ])

    hb.display()  # will display the board as 

         .  .  b  b  . 
           .  w  b  .  . 
             .  .  b  b  . 
               .  .  b  w  w 
                 .  b  w  .  w 

    You can test whether there exists a chain of a given color connecting two
    opposite sides of the board with the method 'is_connected'
    
    You can compute the best partial path of a given color with the
    method 'shortest_path'


The class Hexgame is an extension of Hexboard and allow the manipulation of the
move history with 'do_move' and 'undo_move' instance functions.

The evaluation function hexgame is quite basic, but can be used with a 
generic minmax or alphabeta player.



Created on Wed Aug 10 19:56:28 2016

@author: f.maire@qut.edu.au

Modification history 

Last modified Fri 20 Aug 2016
added class Hexgame

added __future__ imports and 
      some assert statements for debugging

"""


# For compatibility with Python 2.7
# A future statement is a directive to the compiler that a particular module 
# should be compiled using syntax or semantics that will be available in a 
# specified future release of Python.
# The future statement is intended to ease migration to future versions of 
# Python that introduce incompatible changes to the language. It allows use 
# of the new features on a per-module basis before the release in which the 
# feature becomes standard.
from __future__ import print_function
from __future__ import division


import array

# for compatibility with Python 2.7, instead of math.inf
# we use float('inf')


#import heapq # for heap

import game # game.py should be in the same directory


class Hexboard(object):
    '''
    Class for representing a hexboard.
    self.board[r*n+c] is the cell at row r and column c, where n is the 
    length of a side of the board.
    An empty cell is represented with 0
    A cell with a black stone with -1
    A cell with a white stone with +1
    
    Instance Atributes:
        self.n
        self.board
    '''
    black_symbol = 'b'  # -1
    white_symbol = 'w'  #  +1
    empty_symbol = '.'  #  0
    symbol_dict = {0:empty_symbol, -1:black_symbol, 1:white_symbol}
    
    
    def __init__(self, n):
        '''
        PARAMS:
           n : the length of the side of the board
        '''
        self.n = n
        self.board  = array.array('b', [0]*n*n) # empty board

        # data structure for the  'is_connected' method
        # indices of the border cells given a direction
        # see function 'is_connected'         
        self.border_slices_a = {
            (1,0) : range(0,n) , # vertical connection  (r changes)
            (0,1) : range(0,n*n,n) # horizontal connection (c changes)
            }                        
        # The side opposite to 'side a'
        self.border_slices_b = {
            (1,0) : range(n*(n-1),n*n) , # vertical connection  (r changes)
            (0,1) : range(n-1,n*n,n) # horizontal connection (c changes)
            }


    def display(self):
        '''
         Display the board on the console
        '''
        print('')        
        for r in range(self.n):
            print('  '*r,end='')
            for c in range(self.n):
                print(Hexboard.symbol_dict[self.board[r*self.n+c]].center(3), end='')
            print('')
        print('')
       
       
    def clone(self):
        '''
            Make a clone of this board
        '''
        hb = Hexboard(self.n)
        hb.board = self.board[:] # make a copy of the board        
        return hb

    
    def set_board(self,L):
        ''' 
        Set the board with the list L.
        PRE
           len(L) == self.n
        PARAMS
           L : list of 0, -1 and 1  of length n*n
               the board is coded row by row
        '''
        assert len(L) == self.n*self.n
        self.board  = array.array('b', L ) # array of bytes
        
        
    def i2rc(self,i):
        '''
        Convert from i index to row, column
        '''
        return i//self.n , i%self.n


    def rc2i(self,r,c):
        '''
        Convert from row, column to i index 
        '''
        return r*self.n+c
        
        
    def get_neighbors(self, i, colors):
        '''
        Return the list of 1D indices of the neighbours of cell 'i' which
        have a label in 'colors'      
        To get the list of black neighbors of cell i on the hexboard hb, use
          hb.get_neighbors(i,(-1,))
        To get the list of white neighbors of cell i on the hexboard hb, use
          hb.get_neighbors(i,(1,))
        To get the list of empty neighbors of cell i on the hexboard hb, use
          hb.get_neighbors(i,(0,))
        To get the list of neighbors of cell i on the hexboard hb that are
          empty or white, use
          hb.get_neighbors(i,(0,1))                  
        '''
        r,c = self.i2rc(i) # convert to row, column coords
        return [ self.rc2i(r+dr,c+dc)  
                 for dr,dc in ((-1,0),(1,0),(0,-1),(0,1),(-1,1),(1,-1))
                      if (0<=r+dr<self.n) and (0<=c+dc<self.n)
                          and self.board[self.rc2i(r+dr,c+dc)] in colors]            

        
    def is_connected(self, colored_direction):
        '''
          Determinete whether there exists a path connecting two opposite sides 
          of the board.  The sides of the board and the color of the path are 
          specified with the pair 'colored_direction'.
          Practically, 
              to determine wether the north and south sides are 
              connected with a black chain of stones, call
                  is_connected((-1,0))
              to determine wether the north and south sides are 
              connected with a white chain of stones, call
                  is_connected((1,0))
              to determine wether the east and west sides are 
              connected with a black chain of stones, call
                  is_connected((0,-1))
              to determine wether the east and west sides are direction
              connected with a whitechain of stones, call
                  is_connected((0,1))                  
          PARAMS
              colored_direction: one of the pairs (1,0), (-1,0), (0,1) and (0,-1)
                 (+1 or -1, 0) vertical direction
                 (0, +1 or -1) horizontal direction
              The sign of '1' tells the player  (-1 b, +1 w)
          RETURN
            True if there exists a connecting path
            False otherwise
        '''
        # check that  'colored_direction' is valid
        assert( colored_direction == (-1,0) or 
                colored_direction == (+1,0) or 
                colored_direction == (0,-1) or 
                colored_direction == (0,+1) ) 
        #
        cd = colored_direction
        color = cd[0] if cd[0] != 0 else cd[1] # color of the direction
        cd = (cd[0]*cd[0] , cd[1]*cd[1]) # remove the sign of the direction
        #  La: list of 'border a' cell indices containing stones of the color 
        La = [i for i in self.border_slices_a[cd] if self.board[i]==color] 
        if not La:  # if the list La is empty
            return False # no connecting path
        # Do the same for the opposite border        
        Lb = [i for i in self.border_slices_b[cd] if self.board[i]==color] 
        if not Lb:
            return False # no connecting path
        # Perform a graph search
        frontier = La[:]
        explored = set()
        while frontier:
            i = frontier.pop()
            if i in Lb:
                return True
            explored.add(i)
            # Python note: next line uses of a generator
            frontier.extend( j for j in self.get_neighbors(i,(color,))  
                                  if j not in explored and j not in frontier )
        return False # specified sides are not connected by the specified color

        
    def shortest_path(self, colored_direction, verbose=0):
        '''
          Determine whether there exists a path made of empty cells and 
          stones of a specific color connecting two opposite sides 
          of the board.  The sides of the board and the color of the path are 
          specified as for the 'is_connected' method.
          PARAMS
              colored_direction: same definition as for 'is_connected"
              verbose: print debug info if non zero
          RETURN
             Either a pair (Le,Lc) of list of cells of cheapest path               
                or 
             (None,None) if no path exists
             
             Le is the list of empty cells 
             Lc is the list of cells with stones of the specified color
        '''
        # check the direction is valid
        assert( colored_direction == (-1,0) or 
                colored_direction == (+1,0) or 
                colored_direction == (0,-1) or 
                colored_direction == (0,+1) ) 
        if verbose: # debugging information
            print("direction : ", colored_direction)
        #
        cd = colored_direction
        color = cd[0] if cd[0] != 0 else cd[1] # color of the direction
        cd = (cd[0]*cd[0] , cd[1]*cd[1]) # remove the sign of the direction
        # . . . . . . . . . . . . . . . . . . . . . 
        def cell_cost(i):
            '''
            Cost of traversing cell i
            0 for if cell i is of 'color'
            1 if empty
            math.inf is the opponent color
            '''
            if self.board[i] == 0:
                return 1
            else:
                return 0 if self.board[i] == color else float('inf') 
        # . . . . . . . . . . . . . . . . . . . . .                 
        # C[i] cost of cheapest path known so far from 'side a' to cell i
        C = [cell_cost(i) if i in self.border_slices_a[cd] else float('inf') for i in range(self.n*self.n)] 
        P = [-1]*self.n*self.n # parent index
        goals = self.border_slices_b[cd] # cells of the 'side b'
        explored = set(self.border_slices_a[cd]) # we know the cost for these cells
        frontier = set()
        # initialize the frontier with neighbors of border_a
        for i in self.border_slices_a[cd]:
            if self.board[i] not in (0,color):
                continue
            for j in  self.get_neighbors(i,(0,color)): # j is empty or stone color
                if j in self.border_slices_a[cd]:
                    continue # j should  already be in 'explored'
                frontier.add(j)
                # check if we can better the path to j via i
                altCj = C[i]+cell_cost(j)
                if  altCj < C[j]:
                    C[j] = altCj
                    P[j] = i
        # perform the search in the rest of the board
        if verbose:
            print('initial frontier : ', frontier)
        if not frontier: # test whether frontier is empty
            return None,None # no path possible for this color     
        while frontier:
            # get the the i for which C[i] is smallest
            c,i = min( (C[i],i) for i in frontier )
            frontier.remove(i)
            if verbose: # debugging information
                print('current i : ',i)
                print('current frontier : ', frontier)
                print('current C : ', C)
                print('current P : ', P)
            if c == float('inf'):
                return None, None  # no path of finite cost possible
            if i in goals:
                # return path from i to 'side_a'
                path_i = []
                k=i
                while k != -1:
                    path_i.append(k)
                    k = P[k]      
                if verbose:
                        print('path_i : ', path_i)                          
                return [k  for k in path_i if self.board[k]==0], [k  for k in path_i if self.board[k]==color]
            explored.add(i)
            # Process the neighbors
            for j in self.get_neighbors(i,(0,color)): # j is empty or stone color
                if j in explored:
                    continue
                frontier.add(j) # frontier is a set
                altCj = C[i]+cell_cost(j)
                if  altCj < C[j]:
                    C[j] = altCj
                    P[j] = i
        return None, None



class Hexgame(Hexboard,game.Game):
    '''
        An hexboard with a 
            - move history (self.history)
            - a player turn (self.turn)
        The key functions of an Hexgame hg are
            - hg.do_move(i)
            - hg.undo_move()
        
        White player tries to connect East and West sides
        Black player tries to connect North and South sides
        
        Instance Atributes:
            those of the parents
            self.history = [] # list of moves that have been played
            self.turn  # -1 or +1   (black  or white)
            - 
    '''
    
    def __init__(self,n):
        '''
        PARAMS:
           n : the length of the side of the board
        '''
        super(Hexgame, self).__init__(n)
        self.history = [] # list of moves that have been played
        self.turn = -1 # black 

    def clone(self):
        '''
            Return  a clone of this game
        '''
        hg = Hexgame(self.n)
        hg.board = self.board[:] # make a copy of the board    
        hg.turn = self.turn
        hg.history = self.history        
        return hg
        
    def do_move(self,m,color=None):
        '''
           Put a stone on cell m. The color of the stone
           is determined by self.turn
           Self.turn is updated to the opponent color
        '''
        assert self.board[m] == 0 # can only play on an empty cell
        if not color is None:
            self.board[m] = color
        else:
            self.board[m] = self.turn
            self.turn = -self.turn
            self.history.append(m)

        
    def undo_move(self):
        ''' 
            Undo the last move in history move list. 
            That is, remove the last stone played, update
            self.history and update self.turn
            Return the cell index of the move last played
        '''
        assert self.history # check that history is not empty
        i = self.history.pop()
        self.board[i] = 0 # empty the cell
        self.turn = -self.turn
        return i

    def print_move(self, m):
        '''
          Print on the console the move m
        '''
        print('i = ',m ,' | r c = ', self.i2rc(m) )


    def is_terminal(self):
        '''
            Return True iff the game is over
        '''
        return self.is_connected((-1,0)) or self.is_connected((0,+1))


    def legal_moves(self):
        '''
            Return the list of legal moves for the current player
        '''
        # return list of empty cells
        return [i for i in range(self.n*self.n) if self.board[i]==0]

        
    def print_player_turn(self):
        print('Turn is ', 'black' if self.turn==-1 else 'white')
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def hexgame_eval(hg):
    '''
       Evaluate the board position wrt to current player
       Large positive value is good!
       If math.inf then current player has won       
       
       This evaluation function compute what is the minimum number of stones
       needed by the opponenet to finish a connecting chain of stones.  A
       similar expression is computed for the the current player, and the 
       difference is returned.
    '''
    # White player
    Le, Lc = hg.shortest_path((0,1), verbose=0) # try with verbose=1 for intermediate results
    w_dist_completion = float('inf') if Le is None else len(Le)
    # Black player
    Le, Lc = hg.shortest_path((-1,0), verbose=0) # try with verbose=1 for intermediate results
    b_dist_completion = float('inf') if Le is None else len(Le)
    diff_dist_completion = w_dist_completion - b_dist_completion
    return diff_dist_completion if hg.turn == -1 else -diff_dist_completion


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        
if __name__ == "__main__":
#    print('Testing Hexboard class')
#    hb = Hexboard(5)
#    hb.set_board([0,0,-1,-1,0, 0,1,-1,0,0, 0,0,-1,-1,0, 0,0,-1,+1,+1 ,0,-1,+1,0,+1 ])
#    hb.display()

    print('Testing Hexgame class')
    hg = Hexgame(5)
    hg.set_board([0,0,-1,-1,0, 0,1,-1,0,0, 0,0,-1,-1,0, 0,0,-1,+1,+1 ,0,-1,+1,0,+1 ])
    hg.display()
    hg.print_player_turn()

#    print(hb.is_connected((1,0)))
#    print(hb.is_connected((-1,0)))
#    print(hb.is_connected((0,-1)))
#    print(hb.is_connected((0,1)))
#    Le, Lc = hb.shortest_path((0,-1))
    Le, Lc = hg.shortest_path((0,1), verbose=0) # try with verbose=1 for intermediate results
    print('Le, lc : ', Le, Lc)
    
    