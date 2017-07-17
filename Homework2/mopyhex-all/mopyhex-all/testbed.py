import Queue

def Hello():    
    q = Queue.Queue()
    return q
q =Hello()
q.put(1)
q.put("abc")
print q.get()
print q.get()


	#def tree_size(self):
		
		#Count nodes in tree by BFS.
		#Hello
		#Q = Queue.Queue()
		#count = 0
		#Q.put(self.root)
		#while not Q.empty():
			#node = Q.get()
			#count +=1
			#for child in node.children.values():
				#Q.put(child)
		#return count
                #"""

		#stderr.write("Ran "+str(num_rollouts)+ " rollouts in " +\
			#str(time.clock() - startTime)+" sec\n")
		#stderr.write("Node count: "+str(self.tree_size())+"\n")