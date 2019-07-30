import pprint
pp = pprint.PrettyPrinter(indent=4)

def puzz_astar(start,end):
    """
    A* algorithm
    """
    weight = 1.1
    Open = [[weight*heuristic_2(start),heuristic_2(start),start]] #optional: heuristic_1
    Closed = []
    Closed_nodes=0
    incumbent = []
    while Open:
        try:
            i = 0
            for j in range(1, len(Open)):
                if Open[i][0] > Open[j][0]:
                    i = j
            path = Open[i]
            Open = Open[:i] + Open[i+1:]
            endnode = path[-1]
            #if endnode == end:
            #   break
            #if endnode in Closed: continue
            for k in moves(endnode):
                if incumbent != [] and k[1] < incumbent[0]: 
                    #Prerequisites for inner cases
                    open_last_nodes = [i[-1] for i in Open]
                    closed_last_nodes = [j[-1] for j in Closed]
                    if k == end:        # if ni is a goal node
                        incumbent = [ path[0]+1 - (1+weight)*heuristic_2(endnode)] + path[2:] + [k]
                    elif (k in open_last_nodes or k in closed_last_nodes):
                        try:
                            i = open_last_nodes.index(k)
                            g = open_last_nodes[i][1] - 
                        except ValueError:
                            i = closed_last_nodes.index(k)
                    else:
                        pass
                    
                    newpath = [path[0] + weight*heuristic_2(k) - weight*heuristic_2(endnode) + 1] + path[1:] + [k] 
                    Open.append(newpath)
                    Closed.append(endnode)
            Closed_nodes += 1 
        except KeyboardInterrupt:
            #print "Closed nodes:", Closed_nodes
            #print "Solution:"
            #pp.pprint(path)
            break
    print "Closed nodes:", Closed_nodes
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
    #puzzle = str([[1, 2, 3, 4],[5, 6, 7, 8], [9, 10, 11, 12],[0, 13, 14, 15]])
    #puzzle = str([[1, 2, 3, 7],[0, 5, 10, 6], [4, 9, 14, 11],[8, 12, 13, 15]])
    #end = str([[0, 1, 2, 3],[4, 5, 6, 7], [8, 9, 10, 11],[12, 13, 14, 15]])
    end = str([[1, 2, 3, 4],[5, 6, 7, 8], [9, 10, 11, 12],[13, 14, 15, 0]])
    puzz_astar(puzzle,end)