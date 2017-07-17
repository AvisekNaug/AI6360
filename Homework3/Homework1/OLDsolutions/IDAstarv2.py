import heapq
import pprint
pp = pprint.PrettyPrinter(indent=4)

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
    
class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0
        
class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.

      Note that this PriorityQueue does not allow you to change the priority
      of an item.  However, you may insert the same item multiple times with
      different priorities.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        # FIXME: restored old behaviour to check against old results better
        # FIXED: restored to stable behaviour
        entry = (priority, self.count, item)
        # entry = (priority, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        #  (_, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0
        
def search(node,depthBound,frontier,end,expandedNodes):
    explored = []
    #print depthBound
    resultlist = ["notFound","NoPathFound",999999,expandedNodes]
    while not frontier.isEmpty():
        current_path = frontier.pop()
        g = current_path[0]
        h = current_path[1]
        if sum(current_path[:2]) > depthBound:
            if g+h<resultlist[2]:
                resultlist = ["notFound",current_path,g+h,expandedNodes]
        else:
            end_node = current_path[-1]
            if end_node == end:
                resultlist = ["found",current_path,0,expandedNodes]
                return resultlist
            if end_node not in explored:
                explored.append(end_node)
                tempFrontier = PriorityQueue()
                expandedNodes += 1
                for k in moves(end_node):
                    gk = g+1
                    hk = heuristic_2(k)
                    tempNode = [gk,hk]+current_path[2:]+[k]
                    tempFrontier.push(tempNode,-(gk+hk))
                while not tempFrontier.isEmpty():
                    temp = tempFrontier.pop()
                    frontier.push(temp)
    return resultlist      
    
def Puzzle_IDAstar(start,end):
    depthBound = heuristic_2(start)
    expandedNodes = 0
    while True:
        frontier = Stack()
        node = [0,heuristic_2(start),start]
        frontier.push(node)
        result,path,least_bound,expandedNodes = search(node,depthBound,frontier,end,expandedNodes)
        if result == "found" :
            print "expandedNodes:",expandedNodes
            return path
            break # Is it necessary?
        else:
            depthBound = least_bound
            
if __name__ == '__main__':
    #puzzle = str([[9, 5, 7, 4],[1, 0, 3, 8], [13, 10, 2, 12],[14, 6, 11, 15]])
    puzzle = str([[3, 6, 9, 4],[5, 2,8, 11], [10, 0, 15, 7],[13, 1, 14, 12]])
    end = str([[1, 2, 3, 4],[5, 6, 7, 8], [9, 10, 11, 12],[13, 14, 15, 0]])
    path = Puzzle_IDAstar(puzzle,end)
    pp.pprint(path)