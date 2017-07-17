# -*- coding: utf-8 -*-
'''
This package defines 
    - an abstract Game class
    - an abstract Player class
    - a Human_player class
    - a minmax player
    - an alphabeta player
    
Note that the two players are very basic.

Created on Sat 20 Aug 2016

@author: f.maire@qut.edu.au
    
Last modified Sat 27 Aug 2016
- replace the test "if opp_move:" with "if opp_move is not None:"
- import re


'''
from __future__ import print_function
from __future__ import division

import re # re.findall('\d+',some_imput)

# for python 2 compatibility
try: 
    input = raw_input
except NameError: 
    pass
    

class IllegalMove(Exception):
    pass


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

class Game(object):
    '''
        Abstract class to represent a game (match) between two players.
        An instance of this class manages the history of the moves, 
        the current state of the board, and whose turn it is.
        
        Atributes:        
            self.turn :  color of the next player to move (-1 Black or +1 White)
            self.history : list of the moves playedd so far
    
    '''

    def display(self):
        '''
            Display the current state
        '''
        raise NotImplementedError # could raise a NonImplemented Exception
        
    def clone(self):
        '''
            Make a clone of this game.
            Implematation s
        '''
        raise NotImplementedError
    
    def do_move(self, m, color=None):
        '''
           Perform move 'm' 
           if color == None, 
              put a stone of color 'self.turn' 
              update self.turn
           else:
              add a stone of color 'color' but
              do not update self.turn
        '''
        raise NotImplementedError
        
    def undo_move(self):
        raise NotImplementedError
    
    def print_move(self, m):
        '''
          Print on the console the move m
        '''
        raise NotImplementedError


    def is_terminal(self):
        '''
          Return True if the game is over
                 otherwise return False
        '''
        raise NotImplementedError
    
    def legal_moves(self):
        '''
            Return the list of legal moves for the current player
        '''
        raise NotImplementedError
    
    def set_turn(self, c):
        self.turn = c
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        

class Player(object):
    '''
        Abstract player class
        
        Attributes        
            self.color : -1 or +1  
            self.game : own copy of the game
    '''

    def __init__(self, game):
        self.game = game  # player's own private copy of the board

    def play(self, opp_move):
        '''
            Given 'opp_move', the last move of the opponent 
            return a move 
        '''
        raise NotImplementedError
    
    def set_color(self, c):
        self.color = c

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

class Human_hex_player(Player):
    '''
        Allow a user player to play a game at the console
        Player enters move either in format 'i' or format 'r c'
    '''

    def __init__(self, game):
        self.game = game  # player's own private copy of the board

    def play(self, opp_move):
        if opp_move is not None:
            self.game.do_move(opp_move)
        while True:
            # move is an integer specifying the index of the cell played
            m = re.findall('\d+', input("Your Move (format 'i' or 'r c') -> ") )
            if len(m) not in (1,2):
                continue
            if len(m)==2:
                m = self.game.rc2i(int(m[0]), int(m[1]))
            else:
                m = int(m[0])
            if m not in self.game.legal_moves():
                print ("Error: illegal move")
                continue
            break
        self.game.do_move(m)
        return m    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

class Human_quantum_player(Player):
    '''
        Allow a user player to play a game at the console
        in format 'from_i to_i' or 'from_r from_c to_r to_c'
    '''

    def __init__(self, game):
        self.game = game  # player's own private copy of the board

    def play(self, opp_move):
        if opp_move is not None:
            self.game.do_move(opp_move)
        while True:
            # move is list of  integers specifying the coords  of move played
            m = re.findall('\d+', input("Your Move (format 'from_i to_i' or 'from_r from_c to_r to_c') -> ") )
            if len(m)==4:
                from_i = self.game.rc2i(int(m[0]), int(m[1]))
                to_i = self.game.rc2i(int(m[2]), int(m[3]))
                m = [from_i, to_i]
            if len(m)==2:
                m[0] , m[1] = int(m[0]), int(m[1])
            m = tuple(m)
#            print('m = ',m )
#            print (self.game.legal_moves())
            if m not in self.game.legal_moves():
                print ("Error: illegal move ", m)
                continue
            break
        self.game.do_move(m)
        return m    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def play(game, player1, player2, verbose = 1):
    ''' 
        Run a game between two players. 
        Can raise IllegalMove exception
        
        PRE:
          - players player1 and player2 have been created
            and given a clone of the initial board
    '''
    
    # Create dictionary  color -> player

    # players must be of opposite color    
    assert player1.color == -player2.color

    if player1.color == -1:        
        dict_color_player = {-1:player1, +1:player2}
    else:
        dict_color_player = {-1:player2, +1:player1}
    
    # initial conditions
    last_move = None
    
    if verbose:
        print ('** Player {} starts **'.format('Black' if game.turn==-1 else 'White'))
        
    while not game.is_terminal():
        # get the next move from current player

        # debug
        if verbose and last_move is not None:
            print('-'*20)
            print('Last move : ',end='')
            game.print_move(last_move)

        if verbose:
            game.display()
            print ('Player {} to move '.format('Black' if game.turn==-1 else 'White'))

        move = dict_color_player[game.turn].play(last_move)
        if move not in game.legal_moves():
            raise IllegalMove
        # update the master board
        game.do_move(move)
        last_move = move
        
    # display terminal state
    if verbose:
        print('-'*20)
        print('** Game over **')
        game.display()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


class Minmax_player(Player):
    '''
    A player that uses minmax to computes its moves.
    
    Attributes:
        self.maxply : depth of the lookahead (default is 2)
        self.eval_fn : the evaluation function to use at the leaves        
    '''

    def __init__(self, game, eval_fn = lambda x : 0):
        self.game = game  # player's own copy of the board
        self.maxply = 2  # 
        self.eval_fn = eval_fn  # default evaluation function

    def play(self, opp_move):
        '''
            Return a move using the minmax algorithm
            
            PRE:
                Game state not terminal        
        '''                
        if opp_move is not None:
            self.game.do_move(opp_move)
            
        best = None # pair  (value, move)
        # try each move
        for m in self.game.legal_moves():
            self.game.do_move(m)
            val = -1 * self.minimax_value(self.maxply)
            self.game.undo_move()
            # update the best operator so far
            if best is None or val > best[0]:
                best = (val, m)
        m = best[1] # best move found
        
        # need to play this move on our own copy of the board
        self.game.do_move(m)
        return m
    
    def minimax_value(self, maxply):
        """Find the utility value of the game state w.r.t. the current player."""
      
        # if we have reached the maximum depth, the utility is approximated
        # with the evaluation function
        if maxply == 0 or self.game.is_terminal():
            return self.eval_fn(self.game)
    
        best_val = None # just a value, not a move
    
        # try each move
        for m in self.game.legal_moves():
            self.game.do_move(m)
            # evaluate the position and choose the best move
            # NOTE: the minimax function computes the value for the current
            # player which is the opponent so we need to invert the value
            val = -1 * self.minimax_value(maxply-1)
            self.game.undo_move()
            if best_val is None or val > best_val:
                best_val = val
        return best_val

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


class Alphabeta_player(Player):
    '''
    A player that uses alpha-beta algorithm to computes its moves.
    
    Attributes:
        self.maxply : depth of the lookahead (default is 2)
        self.eval_fn : the evaluation function to use at the leaves        
    '''

    def __init__(self, game, eval_fn = lambda x : 0):
        self.game = game  # player's own copy of the board
        self.maxply = 2  # 
        self.eval_fn = eval_fn  # default evaluation function

    def play(self, opp_move):
        '''
            Return a move using the alpha-beta algorithm
            
            PRE:
                Game state not terminal        
        '''                
        if opp_move is not None:
            self.game.do_move(opp_move)
            
        best_val, best_move = None, None # pair  (best value, best move)
        # try each move
        for m in self.game.legal_moves():
            self.game.do_move(m)
            if best_val is not None:
                opp_beta = -1 * best_val
            else:
                opp_beta = None
            val = -1 * self.alphabeta_value(self.maxply, None,opp_beta)
            self.game.undo_move()
            # update the best operator so far
            if best_val is None or val > best_val:
                (best_val, best_move) = (val, m)
        
        # need to play this move on our own copy of the board
        self.game.do_move(best_move)
        return best_move

    def alphabeta_value(self, maxply,alpha,beta):
        """Find the utility value of the game state w.r.t. the current player."""
      
        # if we have reached the maximum depth, the utility is approximated
        # with the evaluation function
        if maxply == 0 or self.game.is_terminal():
            return self.eval_fn(self.game)
    
        best_val = None # just a value, not a move
    
        # try each move
        for m in self.game.legal_moves():
            self.game.do_move(m)
            # NOTE: the minimax function computes the value for the current
            # player which is the opponent so we need to invert the value
            # invert alpha beta values and meaning, think of the following
            #     alpha <=  my score <=  beta
            # => -alpha >= -my score >= -beta
            # => -alpha >= opp score >=  beta
            # => -beta  <= opp score <= -alpha
            if beta is not None:
                opp_alpha = -1 * beta
            else:
                opp_alpha = None
            if alpha is not None:
                opp_beta = -1 * alpha
            else:
                opp_beta = None
            
            val = -1 * self.alphabeta_value(maxply-1,opp_alpha, opp_beta)
            self.game.undo_move()
            if best_val is None or val > best_val:
                best_val = val
        return best_val
