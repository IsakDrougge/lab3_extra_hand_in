# visualization of shortest path in Lab 3, modified to work with Django

try: #added this since it helps when running locally in VS-code
    from .trams import readTramNetwork
    from .graphs import dijkstra
    from .trams import specialize_stops_to_lines
    from .color_tram_svg import color_svg_network
except:
    from trams import readTramNetwork
    from graphs import dijkstra
    from trams import specialize_stops_to_lines
    # from color_tram_svg import color_svg_network

import os
# from django.conf import settings

def remove_endpoints(paths_dict):
    for path in paths_dict:
        values = paths_dict[path]
        nodes_to_remove = []

        continuing = True
        i = 0
        while continuing:
            try:
                if values[i][0] == values[i+1][0]:
                    nodes_to_remove.append(values[i])
                    i += 1
                else:
                    continuing = False
            except:
                break

        continuing = True
        i = len(values)-1
        while continuing:
            try:
                if values[i][0] == values[i-1][0]:
                    nodes_to_remove.append(values[i])
                    i = i-1
                    print("test")
                else:
                    continuing = False
            except:
                break

        
        for node in nodes_to_remove:
            try:
                paths_dict[path].remove(node)
            except:
                pass
    
    return paths_dict

def print_format(path_dict):
    new_path_list = []
    for vertex_tuple in path_dict:
        if new_path_list == []:
            new_path_list.append(path_dict[0][1] + ':')
            new_path_list.append(path_dict[0][0])
        elif vertex_tuple[0] not in new_path_list:
            new_path_list.append(vertex_tuple[0])
        else:
            new_path_list.append(vertex_tuple[1] + ':')
    return new_path_list

def show_shortest(dep, dest):

    network = readTramNetwork()
    network_change = specialize_stops_to_lines(network)

    dep_vertex_list = [vertex for vertex in network_change.vertices() if vertex[0] == dep]
    dep = dep_vertex_list[0] # BORDE ITERERA ÖVER ALLA VERTEX FÖR SAMMA STATION FÖR ATT HITTA DEN SNABBASTE VÄGEN (INTE RÄKNA MED BYTEN PÅ DESTINATIONEN)

    quickest = dijkstra(network_change, dep, cost=lambda u, v: network_change.get_weight(u, v)[0])
    shortest = dijkstra(network_change, dep, cost=lambda u, v: network_change.get_weight(u, v)[1])

    dest_vertex_list = [vertex for vertex in network_change.vertices() if vertex[0] == dest]
    dest = dest_vertex_list[0] # If this guess of index is right, it's right. If not, the function below corrects it. Works either eay.

    quickest = remove_endpoints(quickest)[dest]
    shortest = remove_endpoints(shortest)[dest]

    quickest_traveltime = sum([network_change.get_weight(quickest[i],quickest[i+1])[0] for i in range(len(quickest)-1)])
    shortest_distance = round(sum([network_change.get_weight(quickest[i],quickest[i+1])[1] for i in range(len(quickest)-1)]), ndigits=3)
    
    quickest = print_format(quickest)
    shortest = print_format(shortest)

    timepath = 'Quickest: ' + ', '.join(quickest) + ', ' + str(quickest_traveltime) + ' min'
    geopath = 'Shortest: ' + ', '.join(shortest) + ', ' + str(shortest_distance) + ' km'

    def colors(stop):
        if stop in shortest and stop in quickest:
            return 'cyan'
        elif stop in shortest:
            return 'green'
        elif stop in quickest:
            return 'orange'
        else:
            return 'white'
        
    # this part should be left as it is:
    # change the SVG image with your shortest path colors
    color_svg_network(colormap=colors)
    # return the path texts to be shown in the web page
    return timepath, geopath