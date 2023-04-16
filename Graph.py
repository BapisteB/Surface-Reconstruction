import Utils

class Graph:
    
    def __init__(self, size):
        self.adjlist = [[] for i in range(size)]

    def addEdge(self, edge):
        hash = Utils.hash(edge[0])
        pos = Utils.dichotomia(self.adjlist[hash], edge[1])
        if self.adjlist[hash] != edge[1]:
            self.adjlist[hash].insert(pos, edge[1])
        else:
            return 

        hash = Utils.hash(edge[1])
        pos = Utils.dichotomia(self.adjlist[hash], edge[1])
        if self.adjlist[hash] != edge[0]:
            self.adjlist[hash].insert(pos, edge[0])
        else:
            return 

    #def addVertex(self, vertex):
