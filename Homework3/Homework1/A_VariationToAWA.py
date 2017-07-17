import timeit
import pprint
pp = pprint.PrettyPrinter(indent=4)

def puzz_astar(start,end):
    """
    AWA* algorithm
    """
    startTime = timeit.default_timer()
    weight = 1.3
    Open = [[0,heuristic_2(start),start]] #optional: heuristic_1
    open_nodes = 0
    Closed = []
    Nodes_Expanded=0
    ClosedToOpen = 0
    incumbent = [99999]
    maxSize = 0
    while Open:
        try:
            print len(Open)
            i = 0
            for j in range(1, len(Open)):
                if Open[i][0] + weight*Open[i][1] > Open[j][0] + weight*Open[j][1]:
                    i = j
            path = Open[i]
            Open = Open[:i] + Open[i+1:]
            if (path[0] + path[1])<incumbent[0]:
                Closed.append(path)
                Nodes_Expanded += 1               
                endnode = path[-1]
                for k in moves(endnode):
                    gk = path[0]+1
                    hk = heuristic_2(k)
                    if gk+hk < incumbent[0]:
                        temp = 0
                        if k == end:        # if ni is a goal node
                            incumbent = [gk] + path[2:] + [k]
                            temp = 1
                        else:
                            #Prerequisites for inner cases
                            open_last_nodes = [i[-1] for i in Open]
                            closed_last_nodes = [j[-1] for j in Closed]
                            if (k in open_last_nodes):
                                    i = open_last_nodes.index(k)
                                    if Open[i][0] > gk:
                                        Open[i][0] = gk
                                        temp = 1
                            if (k in closed_last_nodes):
                                    i = closed_last_nodes.index(k)
                                    if Closed[i][0] > gk:
                                        Closed[i][0] = gk
                                        Open.append(Closed[i])
                                        open_nodes += 1
                                        ClosedToOpen += 1
                                        Closed = Closed[:i] + Closed[i+1:] 
                                        temp = 1                          
                        if temp==0:
                            newpath = [gk]+[hk]+path[2:]+[k]
                            Open.append(newpath)
                            open_nodes += 1
            maxSize = max(maxSize,len(Open)+len(Closed))                    
        except KeyboardInterrupt:
            #print " Some error happened!"
            break
    stopTime = timeit.default_timer()
    print "time required: ",stopTime-startTime
    print "MaxSize of Open&Closed List: ",maxSize
    print "#Expanded nodes:", Nodes_Expanded
    print "Open_nodes: ",open_nodes
    print "Number of nodes transferred from Closed to Open list: ",ClosedToOpen
    print "Solution:"
    pp.pprint(incumbent)
    if Open:
        error_bound = incumbent[0]-min([(i[0]+i[1]) for i in Open])
        print "ErrorBound:", error_bound


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
    puzzle = str([[5, 3, 0, 4],[7, 2, 6, 8], [1, 9, 10, 11],[13, 14, 15, 12]])
    #puzzle = str([[6, 2, 4, 8], [15, 9, 1, 0], [7, 5, 11, 3], [14, 13, 10, 12]])
    end = str([[1, 2, 3, 4],[5, 6, 7, 8], [9, 10, 11, 12],[13, 14, 15, 0]])
    puzz_astar(puzzle,end)