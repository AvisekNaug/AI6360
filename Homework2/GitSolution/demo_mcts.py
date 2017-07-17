    
'''

Created on Sat 27 Aug 2016

@author: f.maire@qut.edu.au
    
    Test functions to illlustrate the classes of 
    packages 
    
'''
from __future__ import print_function
from __future__ import division


import game
import quantum_game
import mcts

# for setting the seed of the random number generator for debugging purpose
import random # random.seed()


def test_1():
    '''
       Game between two human players
    '''
    qg = quantum_game.Quantumgame()
    qg.randomize_board()
    print(qg.legal_moves(True))
    ph1 = game.Human_quantum_player(qg.clone())
    ph1.set_color(-1)
    ph2 = game.Human_quantum_player(qg.clone())    
    ph2.set_color(+1)
    qg.print_player_turn()    
    game.play(qg, ph1, ph2, verbose = 1)

#
def test_2():
    '''
       Game between human player and minmax player
    '''
    qg = quantum_game.Quantumgame()
    random.seed(a=22)
    qg.randomize_board()
    p1 = game.Human_quantum_player(qg.clone())
    p1.set_color(+1)
    p2 = mcts.MCTS_player(qg.clone(),iters=1000)    
    p2.set_color(-1)

    game.play(qg, p1, p2, verbose = 1)
#
#def test_2a():
#    '''
#       Game between human player and minmax player
#    '''
#    qg = hexgame.Hexgame(5)
#    ph1 = game.Human_player(qg.clone())
#    ph1.set_color(-1)
#    ph2 = game.Alphabeta_player(qg.clone(),hexgame.hexgame_eval)    
#    ph2.set_color(+1)
#
#    game.play(qg, ph1, ph2, verbose = 1)
#
#def test_3():
#    '''
#       debug Game between human player and minmax player
#    '''
#    qg = hexgame.Hexgame(3)
#    qg.set_board([1,0,0,-1,1,-1,0,0,-1])
# 
#    ph1 = game.Human_player(qg.clone())
#    ph1.set_color(-1)
#    ph2 = game.Minmax_player(qg.clone(),hexgame.hexgame_eval)    
#    ph2.set_color(+1)
#    
#  
#    game.play(qg, ph1, ph2, verbose = 1)
    
if __name__ == "__main__":
#    test_1()
    test_2()
#    test_2a()
#    test_3()



# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 
#                              CODE CEMETARY
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 

#
#    # Experiment 1:
#    # Player 1 and Player 2 are evenly matched with 3-ply deep search
#    # player 2 wins with a final score of 28
#    # player 1 0.2 s per ply player 2 0.4 s per ply
#    play(othello.game(), player(lambda x: minimax.minimax(x, 3)),
#         player(lambda x: minimax.minimax(x, 3)), False)
#    
#    # Experiment 2:
#    # now we show the significance of an evaluation function
#    # we weaken player1 to 2 ply deep but use the edge eval fun
#    # player 1 now beats player 2 with a score of 58!
#    # player 1 0.1 s per ply player 2 0.4 s per ply
#    play(othello.game(), player(lambda x: minimax.minimax(x, 2, othello.edge_eval)),
#         player(lambda x: minimax.minimax(x, 3)), False)
#
#    # Experiment 1 (with alpha-beta):
#    # player 1 0.1 s per ply, player 2 0.1 s per ply
#    play(othello.game(), player(lambda x: minimax.alphabeta(x, 3)),
#         player(lambda x: minimax.alphabeta(x, 3)), False)
#
#    # Experiment 2 (with alpha-beta):
#    # player 1 0.0 s per ply player 2 0.1 s per ply
#    play(othello.game(), player(lambda x: minimax.alphabeta(x, 2, othello.edge_eval)),
#         player(lambda x: minimax.alphabeta(x, 3)), False)
#
