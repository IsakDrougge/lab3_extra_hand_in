import graphviz
from queue import PriorityQueue
import sys

def sort_verticies(vertex1, vertex2):
        sortedVerticies = [vertex1, vertex2]
        sortedVerticies.sort()
        firstVertex = sortedVerticies[0]
        secondVertex = sortedVerticies[1]
        return(firstVertex, secondVertex)

class Graph:

    def __init__(self, start=None, values = None, directed=False):
        self._adjacencylist = {} # format: {1: {2}, 2: {1}}
        self._isdirected = directed

        if values is None:
            values = {}
        self._valuelist = values

        if start is None:
            self.edgelist = []
        else:
            self._valuedict = {}
            self.edgelist = []
            for edge in start:
                firstVertex, secondVertex = self.sort_verticies(edge[0], edge[1])

                if (firstVertex, secondVertex) not in self.edgelist:
                    self.edgelist.append((firstVertex, secondVertex))
                else:
                    print("Error, edge already in graph")

                if firstVertex not in self._adjacencylist:
                    self._adjacencylist[firstVertex] = {secondVertex}
                    self._valuedict[firstVertex] = None
                else:
                    self._adjacencylist[firstVertex].add(secondVertex)

                if secondVertex not in self._adjacencylist:
                    self._adjacencylist[secondVertex] = {firstVertex}
                    self._valuedict[secondVertex] = None
                else:
                    self._adjacencylist[secondVertex].add(firstVertex)

    def sort_verticies(self, vertex1, vertex2):
        sortedVerticies = [vertex1, vertex2]
        sortedVerticies.sort()
        firstVertex = sortedVerticies[0]
        secondVertex = sortedVerticies[1]
        return(firstVertex, secondVertex)

    def neighbors(self, vertex):
        if vertex in self._adjacencylist:
            return self._adjacencylist[vertex]
        else:
            print("Error, vertex does not exist in graph (neighbors)")

    def vertices(self):
        return [vertex for vertex in self._adjacencylist]

    def edges(self): #(only given in one direction for undirected graphs)
        return self.edgelist

    def __len__(self): #the number of vertices
        return len(self._adjacencylist)

    def add_vertex(self, vertex):
        if vertex not in self._adjacencylist:
            self._adjacencylist[vertex] = {}
            self._valuedict[vertex] = None
        else:
            print("Error, vertex already added")

    def add_edge(self, vertex1, vertex2):

        firstVertex, secondVertex = self.sort_verticies(vertex1, vertex2)

        if (firstVertex, secondVertex) not in self.edgelist:
            self.edgelist.append((firstVertex, secondVertex))
        else:
            print("Error, edge already in graph")

        if firstVertex not in self._adjacencylist:
            self._adjacencylist[firstVertex] = {secondVertex}
            self._valuelist[firstVertex] = None
        else:
            self._adjacencylist[firstVertex].add(secondVertex)

        if secondVertex not in self._adjacencylist:
            self._adjacencylist[secondVertex] = {firstVertex}
            self._valuelist[secondVertex] = None
        else:
            self._adjacencylist[secondVertex].add(firstVertex)


    def remove_vertex(self, vertex): # (also removing the edges with this vertex)
        
        if vertex in self._adjacencylist:
            del self._adjacencylist[vertex]
            del self._valuedict[vertex]
        else:
            print("Error, vertex not in graph")

        for verticies in self._adjacencylist:
            if vertex in self._adjacencylist[verticies]:
                self._adjacencylist[verticies].remove(vertex)

        edges_to_remove = []
        for edge in self.edgelist:
            if vertex in edge:
                edges_to_remove.append(edge)
        for edge in edges_to_remove:
            self.edgelist.remove(edge)
        

    def remove_edge(self, vertex1, vertex2): # (vertices not removed even if left unconnected)
        firstVertex, secondVertex = self.sort_verticies(vertex1, vertex2)

        if (firstVertex, secondVertex) in self.edgelist:
            self.edgelist.remove((firstVertex, secondVertex))
        else:
            print("Error, edge does not exist")

    def get_vertex_value(self, vertex):
        if vertex in self._valuedict:
            return self._valuedict[vertex]
        else: 
            print("Error, vertex not in graph")

    def set_vertex_value(self, vertex, value):
        if vertex in self._valuedict:
            self._valuedict[vertex] = value
        else: 
            print("Error, vertex not in graph")



class WeightedGraph(Graph):

    def __init__(self, weightlist=None, edgelist=None, values = None, directed=False):
        Graph.__init__(self, edgelist, values, directed)
        if weightlist is None:
            self._weightsDict = {} # format: dict[ (firstVertex, secondVertex) ] = whatever the weight is
        else:
            self._weightsDict = weightlist
    
    def set_weight(self, vertex1, vertex2, weight):
        firstVertex, secondVertex = self.sort_verticies(vertex1, vertex2)
        self._weightsDict[(firstVertex, secondVertex)] = weight

    def get_weight(self, vertex1, vertex2):
        firstVertex, secondVertex = self.sort_verticies(vertex1, vertex2)
        if (firstVertex, secondVertex) in self._weightsDict:
            return self._weightsDict[(firstVertex, secondVertex)]
        else:
            return None



### NEW LAB1, BONUS 1 MODIFIED DIJKSTRA ###

def dijkstra(graph, source, cost=lambda u,v: 1):

    #algo from use of wiki pseudo code
    visted_vertex = []
    queue = PriorityQueue()
    values = {vertex: float(sys.maxsize) for vertex in graph.vertices()}
    visited = {vertex: "" for vertex in graph.vertices() if not vertex == source}
    values[source] = 0
    queue.put((values[source], source))

    while not queue.empty():
        current = queue.get()[1]
        visted_vertex.append(current)
        for neighbor in graph.neighbors(current):
            weight = cost(current, neighbor)
            if neighbor not in visted_vertex:
                old_cost = values[neighbor]
                new_cost = values[current] + weight
                if new_cost < old_cost:
                    queue.put((new_cost, neighbor))
                    values[neighbor] = new_cost
                    visited[neighbor] = current

# create the dict with all shortest paths
    shortest = {}
    for vertex in graph.vertices():
        if vertex != source:
            possible = True
            temp = vertex
            path = []
            while temp != source:
                if temp in visited:
                    path.append(temp)
                    temp = visited[temp]
                else:
                    possible = False
                    break
            if possible:
                path.append(source)
                path.reverse()
                shortest[vertex] = path
    return shortest


### ORIGINAL UNTOUCHED LAB2 DIJKSTRA ###

# def dijkstra(graph, source, cost=lambda u,v: 1):

#     #algo from use of wiki pseudo code
#     visted_vertex = []
#     queue = PriorityQueue()
#     values = {vertex: float(sys.maxsize) for vertex in graph.vertices()}
#     visited = {vertex: "" for vertex in graph.vertices() if not vertex == source}
#     values[source] = 0
#     queue.put((values[source], source))

#     while not queue.empty():
#         current = queue.get()[1]
#         visted_vertex.append(current)
        
#         for neighbor in graph.neighbors(current):
#             weight = cost(current, neighbor)
#             if neighbor not in visted_vertex:
#                 old_cost = values[neighbor]
#                 new_cost = values[current] + weight
#                 if new_cost < old_cost:
#                     queue.put((new_cost, neighbor))
#                     values[neighbor] = new_cost
#                     visited[neighbor] = current

# # create the dict with all shortest paths
#     shortest = {}
#     for vertex in graph.vertices():
#         if vertex != source:
#             possible = True
#             temp = vertex
#             path = []
#             while temp != source:
#                 if temp in visited:
#                     path.append(temp)
#                     temp = visited[temp]
#                 else:
#                     possible = False
#                     break
#             if possible:
#                 path.append(source)
#                 path.reverse()
#                 shortest[vertex] = path
#     return shortest



def visualize(graph, view=True, name='mygraph', nodecolors=[]):

    dot = graphviz.Graph()

    for vertex in graph.vertices():
        if str(vertex) in nodecolors: 
            dot.node(str(vertex), str(vertex), color=nodecolors[str(vertex)], style='filled', shape='rectangle')
        else:
            dot.node(str(vertex), str(vertex), shape='rectangle')

    for edge in graph.edges():
        dot.edge(str(edge[0]), str(edge[1]))
    
    dot.render('./data/GraphRender', format = 'svg', view=True, engine='neato')


def view_shortest(G, source, target, cost=lambda u,v: 1):

    path = dijkstra(G, source, cost)[target]
    colormap = {str(v): 'orange' for v in path}
    visualize(G, view='view', nodecolors=colormap)


def demo():
    G = Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    view_shortest(G, 2, 6)




if __name__ == '__main__':
    demo()

    # G = WeightedGraph()
    # G.add_edge(1, 2)
    # G.add_edge(2, 3)
    # G.add_edge(3, 4)
    # G.add_edge(4, 1)
    # G.add_edge(3,5)
    # G.add_edge(2,5)

    # print(G.edges())
    # print(G.vertices())
    # print(len(G))

    # G.set_weight(1,2,1)
    # G.set_weight(2,3,2)
    # G.set_weight(3,4,3)
    # G.set_weight(4,1,4)
    # G.set_weight(3,5,1)
    # G.set_weight(2,5,2)

    # view_shortest(G, 1, 4)
