import pprint
pp = pprint.PrettyPrinter(indent=4)

def puzz_astar(start,end):
    """
    A* algorithm
    """
    #weight = 1.0
    Open = [[0,heuristic_2(start),start]] #optional: heuristic_1
    Closed = []
    Nodes_Expanded=0
    #incumbent = [99999999]
    while Open:
            i = 0
            for j in range(1, len(Open)):
                if Open[i][0] +Open[i][1] > Open[j][0] + Open[j][1]:
                    i = j
            path = Open[i]
            Open = Open[:i] + Open[i+1:]
            endnode = path[-1]
            Closed.append(endnode)
            Nodes_Expanded += 1               
            if endnode == end:
                break
            for k in moves(endnode):
                if k in Closed:
                    continue
                gk = path[0]+1
                hk = heuristic_2(k)                         
                newpath = [gk]+[hk]+path[2:]+[k]
                Open.append(newpath)                             
    print "#Expanded nodes:", Nodes_Expanded-1
    print "Solution:"
    pp.pprint(path)

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
    puzzle = str([[3, 6, 9, 4],[5, 2,8, 11], [10, 0, 15, 7],[13, 1, 14, 12]])
    end = str([[1, 2, 3, 4],[5, 6, 7, 8], [9, 10, 11, 12],[13, 14, 15, 0]])
    puzz_astar(puzzle,end)