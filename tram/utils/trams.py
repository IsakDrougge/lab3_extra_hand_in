import sys
import json
sys.path.insert(0, './Lab1')
sys.path.insert(0, './data')

try:
    from .graphs import *
    from .tramdata import *
except:
    from graphs import *
    from tramdata import *

TRAM_FILE = '/Users/isakdrougge/Desktop/Skola/Advanced-Python/labs-advPyth/data/tramnetwork.json'

class TramStop:

    def __init__(self, stopname, stopPosition=None, connectedLines=None):
        self._stopname = stopname

        if stopPosition is None:
            stopPosition = {}
        self._stopPosition = stopPosition

        if connectedLines is None:
            connectedLines = []
        self._connectedLines = connectedLines

    def get_name(self):
        return self._stopname

    def get_position(self):
        return self._stopPosition
    
    def set_position(self, lat, lon):
        self._stopPosition = {"lat": str(lat), "lon": str(lon)}
    
    def get_lines(self):
        return self._connectedLines
    
    def set_lines(self, lineList):
        self._connectedLines = lineList


class TramLine:

    def __init__(self, lineName, stopsInLine):
        self._lineName = str(lineName) # the name of the line (in Gothenburg usually a number, but do not assume this)
        self._stopsInLine = stopsInLine # the list of stops in order, in one direction

    def get_number(self):
        return self._lineName
    
    def get_stops(self):
        return self._stopsInLine


class TramNetwork(WeightedGraph):

    def __init__(self, stops, lines, times):

        self._stopdict = {stop: TramStop(stop, stopPosition=stops[stop]) for stop in stops}  # stops and their positions (objects of class TramStop)
        self._linedict = {line: TramLine(line, lines[line]) for line in lines}   # lines and their stops (objects of class TramLine)
        self._timedict = times

        # Sets lines via a given stop
        for stop in self._stopdict:
            line_list = []
            for line in self._linedict:
                if stop in lines[line]:
                    line_list.append(line)
            self._stopdict[stop].set_lines(line_list)


        traveltimeDict = {} #list of weights/traveltimes for WeightedGraph class
        edgelist = [] # list of edges for class Graph
        linesDict = {line: self._linedict[line].get_stops() for line in self._linedict}
        for line in self._linedict:
            for i in range(len(self._linedict[line].get_stops()) -1):
                stop1 = self._linedict[line].get_stops()[i]
                stop2 = self._linedict[line].get_stops()[i+1]

                vertex_tuple = sort_verticies(stop1, stop2)
                if vertex_tuple not in traveltimeDict:
                    firstVertex = vertex_tuple[0]
                    secondVertex = vertex_tuple[1]
                    edgelist.append((firstVertex, secondVertex))
                    traveltimeDict[(firstVertex, secondVertex)] = time_between_stops(linesDict, self._timedict, line, firstVertex, secondVertex)


        WeightedGraph.__init__(self, traveltimeDict, edgelist)


    def all_lines(self): #     list all lines (just the line numbers, or whole objects)
        return [self._linedict[line] for line in self._linedict]

    def all_stops(self): #     list all stops (just the stop names, or whole objects)
        return [self._stopdict[stop] for stop in self._stopdict]

    def extreme_positions(self): # method should return the minimum and maximum latitude and longitude found among all stop position
        longitudes = [self._stopdict[stop].get_position()["lon"] for stop in self._stopdict]
        latitudes = [self._stopdict[stop].get_position()["lat"] for stop in self._stopdict] 
        longitudes.sort()
        latitudes.sort()
        return {"min_lon": longitudes[0], "min_lat": latitudes[0], "max_lon": longitudes[len(longitudes)-1], "max_lat": latitudes[len(latitudes)-1]}

    def geo_distance(self, a, b): #     the geographical distance between any two stops (from Lab 1!)
        stopDict = {stop: self._stopdict[stop].get_position() for stop in self._stopdict}
        return distance_between_stops(stopDict, a, b)

    def line_stops(self, line): #     list the stops along a line (just the stop names, or whole objects)
        return [self._stopdict[stop].get_name() for stop in self._linedict[line].get_stops()]

    def stop_lines(self, a):  #     list the lines through a stop (just the line numbers, or whole objects)
        linesDict = {line: self._linedict[line].get_stops() for line in self._linedict}
        linesVia = lines_via_stop(linesDict , a)
        return [self._linedict[line] for line in linesVia]

    def stop_position(self, a): #     the position of a stop
        return self._stopdict[a].get_position()

    def transition_time(self, a,b):   #     the transition time between two subsequent stops
        linesDict = {line: self._linedict[line].get_stops() for line in self._linedict}
        linesViaA = lines_via_stop(linesDict , a)
        linesViaB = lines_via_stop(linesDict , b)
        lines_between_both_stops = [line for line in linesViaA if line in linesViaB]

        traveltimes = [time_between_stops(linesDict, self._timedict, line, a, b) for line in lines_between_both_stops]
        
        traveltimes.sort()

        return traveltimes[0] #returns the shortest travel time, if several routes are possible

def readTramNetwork(tramfile=TRAM_FILE):
    with open(TRAM_FILE, 'r') as openfile:
        loadedFile = json.load(openfile)
    
    return TramNetwork(loadedFile['stops'], loadedFile['lines'], loadedFile['times'])






###     BONUS 1     ###


# takes the output from readTramNetwork as input to modify

def specialize_stops_to_lines(network):

    # creates (stop, line) vertices
    vertices_list = []
    for stop in network.all_stops():
        for line in stop.get_lines():
            vertices_list.append((stop.get_name(), line))

    # creates ((a, line), (b, line)) edges
    edges_list = []
    for edge in network.edges():
        for line in network.stop_lines(edge[0]):
            if line in network.stop_lines(edge[1]):
                vertex_tuple = sort_verticies((edge[0], line.get_number()), (edge[1], line.get_number()))
                vertex1 = vertex_tuple[0]
                vertex2 = vertex_tuple[1]
                new_edge = (vertex1, vertex2)
                if new_edge not in edges_list:
                    edges_list.append(new_edge)
    
    change_edges = []
    for vertex in network.all_stops():
        for line in vertex.get_lines():
            for other_line in vertex.get_lines():
                if line != other_line:
                    vertex_tuple = sort_verticies((vertex.get_name(), line), (vertex.get_name(), other_line))
                    vertex1 = vertex_tuple[0]
                    vertex2 = vertex_tuple[1]
                    new_edge = (vertex1, vertex2)
                    change_edges.append(new_edge)

    # creates weights list in format { ((a, line), (b, line)) : 3 }
    weights_list = {}
    for edge in edges_list:
        weight = network.get_weight(edge[0][0], edge[1][0])
        distance = network.geo_distance(edge[0][0], edge[1][0])
        weights_list[edge] = (weight, distance)

    change_time = 10      # minutes - set this to something reasonable
    change_distance = 0.02  # meters - set this to something reasonable

    for edge in change_edges:
        weights_list[edge] = (change_time, change_distance)
        
    edges_list = edges_list + change_edges

    

    # new graph object created from lists above
    new_network = WeightedGraph(weightlist=weights_list, edgelist=edges_list)

    #returns a new network on bonus 1 specifications
    return new_network

def specialized_transition_time(spec_network, a, b, changetime=10):
    # TODO: write this function as specified
    return changetime


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    # TODO: write this function as specified
    return changedistance


# def demo():
#         G = readTramNetwork()
#         a, b = input('from,to ').split(',')
#         view_shortest(G, a, b)

# if __name__ == '__main__':
#     demo()



def demo2():

        G = readTramNetwork()
        a, b = input('from,to ').split(',')
        a = (a, G.stop_lines(a)[0].get_number())
        b = (b, G.stop_lines(b)[0].get_number())
        G = specialize_stops_to_lines(G)
        view_shortest(G, a, b)

if __name__ == '__main__':
    demo2()

