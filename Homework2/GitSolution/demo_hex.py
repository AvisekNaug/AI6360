    
'''
Test functions to illustrate the classes of the
packages 'game' and 'hexgame'


Created on Sat 20 Aug 2016
@author: f.maire@qut.edu.au
    
Last revised Sat 28 Aug
    
    
'''
from __future__ import print_function
from __future__ import division

import game, hexgame,mcts



def test_H_H():
    '''
       Game between two human players
    '''
    hg = hexgame.Hexgame(11)
    p1 = game.Human_hex_player(hg.clone())
    p1.set_color(-1)
    p2 = game.Human_hex_player(hg.clone())    
    p2.set_color(+1)
    hg.print_player_turn()    
    game.play(hg, p1, p2, verbose = 1)


def test_H_M():
    '''
       Game between human player and minmax player
    '''
    hg = hexgame.Hexgame(5)
    #p1 = game.Minmax_player(hg.clone(),hexgame.hexgame_eval)
    #p1 = game.Human_hex_player(hg.clone())
    p1 = mcts.MCTS_player(hg.clone(),iters=1000)
    p1.set_color(+1)
    p2 = game.Minmax_player(hg.clone(),hexgame.hexgame_eval)   
    p2.set_color(-1)

    game.play(hg, p1, p2, verbose = 1)

def test_H_A():
    '''
       Game between human player and alphabeta player
    '''
    hg = hexgame.Hexgame(5)
    p1 = game.Human_hex_player(hg.clone()) 
    p1.set_color(-1)
    p2 = game.Alphabeta_player(hg.clone(),hexgame.hexgame_eval)    
    p2.set_color(+1)

    game.play(hg, p1, p2, verbose = 1)

def test_debug():
    '''
       debug Game between human player and minmax player
    '''
    hg = hexgame.Hexgame(3)
    hg.set_board([1,0,0,-1,1,-1,0,0,-1])
 
    p1 = game.Human_hex_player(hg.clone())
    p1.set_color(-1)
    p2 = game.Minmax_player(hg.clone(),hexgame.hexgame_eval)    
    p2.set_color(+1)
    
  
    game.play(hg, p1, p2, verbose = 1)
    
if __name__ == "__main__":
#    test_H_H()
    print(''' 
    Black tries to connect North and South
    White tries to connect East and West
    
    Top left cell has coordinates r=0 and c=0
    ''')
    test_H_M()



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
