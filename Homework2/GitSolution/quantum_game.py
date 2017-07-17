# -*- coding: utf-8 -*-
"""
This package defines a Quantumboard class to manipulate Quantumboards.


Each player has an allocated colour (White or Black).
White starts the game. Players alternate turns during the game
until one of them cannot make a valid move, thereby losing the
game.
On your turn, you must make one capture. A particle makes a
capture by leaping in a straight line in any of the 6 directions
radiating from it exactly as many spaces as friendly particles
surround its original position, and landing on an enemy
particle, which is removed from the game (the attacking
particle occupies its place). Particles can leap over other
particles.

             .  .  .  .  . 
            .  .  .  .  .  . 
           .  .  .  .  .  .  . 
          .  .  .  .  .  .  .  . 
         .  .  .  .  .  .  .  .  . 
           .  .  .  .  .  .  .  .    
             .  .  .  .  .  .  .       
               .  .  .  .  .  .          
                 .  .  .  .  .  
                 
                 
Code examples
    qb = Quantumboard()  # create a  Quantumboard
    
    # Set up the board row by row. 
    # Empty cells are coded with 0, white stones with +1, black stones with -1


The class Quantumgame is an extension of Quantumboard and allow the manipulation of the
move history with 'do_move' and 'undo_move' instance functions.


Created on Wed Aug 10 19:56:28 2016

@author: f.maire@qut.edu.au

Modification history 

Last modified Fri 20 Aug 2016
added class Quantumgame

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

import random

import array


import game # game.py should be in the same directory


class Quantumboard(object):
    '''
    Class for representing a Quantumboard.
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
    out_symbol = ' ' # 2
    symbol_dict = {0:empty_symbol, -1:black_symbol, 1:white_symbol, 2:out_symbol}
    
    
    def __init__(self):
        '''
        PARAMS:
           n : the length of the side of the board
        '''
        self.n = 9
        self.board  = array.array('b', [0]*self.n*self.n) # empty board
        for r in range(4):
            for c in range(4-r):
                self.board[r*self.n+c] = 2 # outside the Quantum board
                self.board[len(self.board)-1-(r*self.n+c) ] = 2 # outside the Quantum board

    def display(self):
        '''
         Display the board on the console
        '''
        print('')        
        for r in range(self.n):
            print('  '*r,end='')
            for c in range(self.n):
                print(Quantumboard.symbol_dict[self.board[r*self.n+c]].center(3), end='')
            print('')
        print('')
       
       
    def clone(self):
        '''
            Make a clone of this board
        '''
        qb = Quantumboard(self.n)
        qb.board = self.board[:] # make a copy of the board        
        
        return qb

    
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
        # make sure the outside cells are marked correctly
        for r in range(4):
            for c in range(4-r):
                self.board[r*self.n+c] = 2 # outside the Quantum board
                self.board[len(self.board)-1-(r*self.n+c) ] = 2 # outside the Quantum board

    def randomize_board(self):
        '''
        30 white stones and 31 black stones        
        '''
        L = [1]*30+[-1]*31 
        j = 0 # pointer for L
        random.shuffle(L)
        for i in range(self.n*self.n):
            r,c = self.i2rc(i)
            if not (3<r+c<5+8): # inside quantum board?
                self.board[i] = 2  # outside the Quantum board
            else:
                self.board[i] = L[j]
                j += 1
        
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
        To get the list of black neighbors of cell i on the Quantumboard hb, use
          hb.get_neighbors(i,(-1,))
        To get the list of white neighbors of cell i on the Quantumboard hb, use
          hb.get_neighbors(i,(1,))
        To get the list of empty neighbors of cell i on the Quantumboard hb, use
          hb.get_neighbors(i,(0,))
        To get the list of neighbors of cell i on the Quantumboard hb that are
          empty or white, use
          hb.get_neighbors(i,(0,1))                  
        '''
        r,c = self.i2rc(i) # convert to row, column coords	 
        #
        #	INSERT YOUR CODE HERE
        #
        return [ self.rc2i(r+dr,c+dc)
                 for dr,dc in ((-1,0),(1,0),(0,-1),(0,1),(-1,1),(1,-1))
                 if (0<=r+dr<self.n) and (0<=c+dc<self.n) and (3<r+dr+c+dc<5+8)
                 and self.board[self.rc2i(r+dr,c+dc)] in colors]





class Quantumgame(Quantumboard,game.Game):
    '''
        An Quantumboard with a 
            - move history (self.history)
            - a player turn (self.turn)
        The key functions of an Quantumgame qg are
            - qg.do_move(i)
            - qg.undo_move()
        
        White player tries to connect East and West sides
        Black player tries to connect North and South sides
        
        Instance Atributes:
            those of the parents
            self.history = [] # list of moves that have been played
            self.turn  # -1 or +1   (black  or white)
            - 
    '''
    
    def __init__(self):
        '''
        PARAMS:
           n : the length of the side of the board
        '''
        super(Quantumgame, self).__init__()
        self.history = [] # list of moves that have been played
        self.turn = 1 # white start
        # self.legal_moves() caches the result        
        # marked as not computed with None
        # The empty list indicates not legal moves
        self.cache_legal_moves = None 

                
    def clone(self):
        '''
            Return  a clone of this game
        '''
        qg = Quantumgame()
        qg.board = self.board[:] # make a copy of the board    
        qg.turn = self.turn
        qg.history = self.history[:]        
        return qg
 
       
    def do_move(self,m):
        '''
           Perform the move m = (from_i, to_i)
           Self.turn is updated to the opponent color
        '''
        from_i , to_i = m # 
        assert (self.board[from_i] == self.turn) and (self.board[to_i] == -self.turn)
        self.board[from_i] = 0
        self.board[to_i] = self.turn
        self.turn = -self.turn
        self.history.append(m)
        self.cache_legal_moves = None

        
    def undo_move(self):
        ''' 
            Undo the last move in history move list. 
            That is, remove the last stone played, update
            self.history and update self.turn
            Return the cell indices of the move last played
        '''
        assert len(self.history)>0  # check that history is not empty
        from_i, to_i = self.history.pop()
        self.board[to_i] = self.turn # INSERT YOUR CODE HERE  : just the rest of the line
        self.board[from_i] = -self.turn # INSERT YOUR CODE HERE  : just the rest of the line
        self.turn = -self.turn
        self.cache_legal_moves = None
        return from_i , to_i

    def print_move(self, m):
        '''
          Print on the console the move m
        '''
        print('from_i to_i = ',m ,' | from_r_c to_r_c = ', self.i2rc(m[0]), self.i2rc(m[1]) )

    def is_terminal(self):
        '''
            Return True iff the game is over
        '''
        return self.cache_legal_moves is not None and len(self.cache_legal_moves) > 0  # INSERT YOUR CODE HERE  : just the rest of the line


    def legal_moves(self, rc_format=False):
        '''
            Return a copy of the list of legal moves for the current player
            A legal move is a pair (from_i,to_i)
            if rc_format==True, return (from_r from_c to_r to_c)
        '''
            
        if self.cache_legal_moves is None:
            # compute the list of legal moves             
            L = []
            for i in range(self.n*self.n):
                # consider only the cell with the color of the mover
                if self.board[i]!=self.turn:
                    continue
                d = self.num_friendly_neighbors(i)
                if d==0:
                    continue
                r,c = self.i2rc(i)
                for dr,dc in ((-d,0),(d,0),(0,-d),(0,d),(-d,d),(d,-d)):
                    if ( (0<=r+dr<self.n) and 
                         (0<=c+dc<self.n) and 
                         (3<r+dr+c+dc<5+8) and 
                         self.board[self.rc2i(r+dr,c+dc)]==-self.turn 
                         ):
                             L.append( (i,self.rc2i(r+dr,c+dc)) )
            self.cache_legal_moves = L
        #    
        if rc_format:
            return [(self.i2rc(m[0]),self.i2rc(m[1])) for m in self.cache_legal_moves]
#            return [self.i2rc(m[0]),self.i2rc(m[1]) for m in self.cache_legal_moves]
        else:
            return self.cache_legal_moves[:] # return a copy for safety
         
         
    def num_friendly_neighbors(self,i):
        color_i = self.board[i]
        if color_i == 2: 
            return 0
        return len( self.get_neighbors(i,(color_i,)) )

                
    def print_player_turn(self):
        print('Turn is ', 'black' if self.turn==-1 else 'white')
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        
if __name__ == "__main__":
    print('Testing Quantumboard class')
    hb = Quantumboard()
#    hb.set_board([0,0,-1,-1,0, 0,1,-1,0,0, 0,0,-1,-1,0, 0,0,-1,+1,+1 ,0,-1,+1,0,+1 ])
    hb.display()

#    print('Testing Quantumgame class')
#    qg = Quantumgame(5)
#    qg.set_board([0,0,-1,-1,0, 0,1,-1,0,0, 0,0,-1,-1,0, 0,0,-1,+1,+1 ,0,-1,+1,0,+1 ])
#    qg.display()
#    qg.print_player_turn()

#    print(hb.is_connected((1,0)))
#    print(hb.is_connected((-1,0)))
#    print(hb.is_connected((0,-1)))
#    print(hb.is_connected((0,1)))
#    Le, Lc = hb.shortest_path((0,-1))
#    Le, Lc = qg.shortest_path((0,1), verbose=0) # try with verbose=1 for intermediate results
#    print('Le, lc : ', Le, Lc)
#    
    