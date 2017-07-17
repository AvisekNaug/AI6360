import timeit
import pprint
pp = pprint.PrettyPrinter(indent=4)

def puzz_astar(start,end):
    """
    ARA* algorithm
    """
    startTime = timeit.default_timer()
    weight = 2.00
    epsilon = 0.1
    open_nodes = 0
    maxSizeINCONS = 0
    maxSize = 0
    Nodes_Expanded=0
    ClosedToIncons = 0
    s_goal = [99999999]
    Open = [[0,heuristic_2(start),start]]
    Closed = []
    Incons = []
    Open,Incons,Closed,s_goal,open_nodes,maxSizeINCONS,maxSize,Nodes_Expanded,ClosedToIncons = ImprovePath(
    weight,Open,Incons,Closed,s_goal,end,open_nodes,maxSizeINCONS,maxSize,Nodes_Expanded,ClosedToIncons)
    weight_prime = min([weight,(s_goal[0]*1.0)/(1.0*min([i[0]+i[1] for i in Open+Incons]))])
    print "Current e-optimal solution: ", s_goal[0]
    while weight_prime>1:
        weight = weight - epsilon
        Open = Open + Incons
        Incons = []
        Closed = []
        Open,Incons,Closed,s_goal,open_nodes,maxSizeINCONS,maxSize,Nodes_Expanded,ClosedToIncons = ImprovePath(
        weight,Open,Incons,Closed,s_goal,end,open_nodes,maxSizeINCONS,maxSize,Nodes_Expanded,ClosedToIncons)
        weight_prime = min([weight,(s_goal[0]*1.0)/(1.0*min([i[0]+i[1] for i in Open+Incons]))])
        print "Current e-optimal solution: ", s_goal[0]
    stopTime = timeit.default_timer()
    print "time required: ",stopTime-startTime
    print "Open_nodes: ",open_nodes
    print "#Expanded nodes:", Nodes_Expanded
    print "Number of nodes transferred from Closed to Incons list: ",ClosedToIncons
    print "maximum size of INCONS List: ",maxSizeINCONS
    print "maximum size of OPEN+CLOSED+INCONS List: ",maxSize
    pp.pprint(s_goal)
    
    

def ImprovePath(weight,Open,Incons,Closed,s_goal,end,open_nodes,maxSizeINCONS,maxSize,Nodes_Expanded,ClosedToIncons):
    comparison = [i[0]+weight*i[1] for i in Open]
    min_fvalue = min(comparison)
    while s_goal[0]>min_fvalue:
        min_index = comparison.index(min_fvalue)
        min_node = Open[min_index]
        endnode = min_node[-1]
        Open = Open[:min_index] + Open[min_index+1:]
        Closed.append(min_node)
        Nodes_Expanded += 1
        for k in moves(endnode):
            gcost_minnode = min_node[0] + 1
            if k == end:
                s_goal = [gcost_minnode]+min_node[2:]+[k]
                print "FOUND A GOAL NODE!!!"
            else:
                open_endnode = [i[-1] for i in Open]
                closed_endnode = [i[-1] for i in Closed]
                #incons_endnode = [i[-1] for i in Incons]
                if k in open_endnode:
                    k_index = open_endnode.index(k)
                    if Open[k_index][0] > gcost_minnode:
                        Open[k_index][0] = gcost_minnode
                elif k in closed_endnode:
                    k_index = closed_endnode.index(k)
                    if Closed[k_index][0] > gcost_minnode:
                        Closed[k_index][0] = gcost_minnode        
                        Incons.append(Closed[k_index])
                        Closed = Closed[:k_index] + Closed[k_index +1 :]
                        ClosedToIncons += 1
                else:
                    gk = gcost_minnode
                    hk = heuristic_2(k)
                    Open.append([gk,hk]+min_node[2:]+[k])
                    open_nodes += 1
        comparison = [i[0]+weight*i[1] for i in Open]
        min_fvalue = min(comparison) 
        maxSizeINCONS = max(maxSizeINCONS,len(Incons))
        maxSize = max(maxSize,len(Open)+len(Incons)+len(Closed))  
    result = [Open]+[Incons]+[Closed]+[s_goal]+[open_nodes]+[maxSizeINCONS]+[maxSize]+[Nodes_Expanded]+[ClosedToIncons]
    return result
    
def moves(mat): 
    """
    Returns a list of all possible moves
    """
    output = []  

    m = eval(mat)   
    i = 0
    while 0 not in m[i]: i += 1
    j = m[i].index(0); #blank space (zero)

    if i > 0:                                   
      m[i][j], m[i-1][j] = m[i-1][j], m[i][j];  #move up
      output.append(str(m))
      m[i][j], m[i-1][j] = m[i-1][j], m[i][j]; 
      
    if i < 3:                                   
      m[i][j], m[i+1][j] = m[i+1][j], m[i][j]   #move down
      output.append(str(m))
      m[i][j], m[i+1][j] = m[i+1][j], m[i][j]

    if j > 0:                                                      
      m[i][j], m[i][j-1] = m[i][j-1], m[i][j]   #move left
      output.append(str(m))
      m[i][j], m[i][j-1] = m[i][j-1], m[i][j]

    if j < 3:                                   
      m[i][j], m[i][j+1] = m[i][j+1], m[i][j]   #move right
      output.append(str(m))
      m[i][j], m[i][j+1] = m[i][j+1], m[i][j]

    return output

def heuristic_1(puzz):
    """
    Counts the number of misplaced tiles
    """ 
    misplaced = 0
    compare = 1
    m = eval(puzz)
    for i in range(4):
        for j in range(4):
            if m[i][j] != compare and m[i][j] != 0:
                misplaced += 1
            compare += 1
    return misplaced

def heuristic_2(puzz):
    """
    Manhattan distance
    """  
    distance = 0
    m = eval(puzz)          
    for i in range(4):
        for j in range(4):
            if m[i][j] == 0: continue
            distance += abs(i - ((m[i][j]-1)/4)) + abs(j -  ((m[i][j]-1)%4));
    #print distance
    return distance

if __name__ == '__main__':
    #puzzle = str([[9, 5, 7, 4],[1, 0, 3, 8], [13, 10, 2, 12],[14, 6, 11, 15]])
    #puzzle = str([[3, 6, 9, 4],[5, 2,8, 11], [10, 0, 15, 7],[13, 1, 14, 12]])
    #puzzle = str([[5, 3, 0, 4],[7, 2, 6, 8], [1, 9, 10, 11],[13, 14, 15, 12]])
    puzzle = str([[6, 2, 4, 8], [15, 9, 1, 0], [7, 5, 11, 3], [14, 13, 10, 12]])
    end = str([[1, 2, 3, 4],[5, 6, 7, 8], [9, 10, 11, 12],[13, 14, 15, 0]])
    puzz_astar(puzzle,end)
