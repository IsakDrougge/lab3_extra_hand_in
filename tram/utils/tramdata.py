import sys
import json

# files given
STOP_FILE = './data/tramstops.json'
LINE_FILE = './data/tramlines.txt'

# file to give
TRAM_FILE = '.data/tramnetwork.json'

def build_tram_stops(jsonobject):
    
    with open(jsonobject, 'r') as openfile:
        loadedFile = json.load(openfile)
    returnDict = {}
    for dict in loadedFile:
        lat = loadedFile[dict]['position'][0]
        lon = loadedFile[dict]['position'][1]
        returnDict[dict] = {'lat': lat, 'lon': lon}
    return returnDict

def build_tram_lines(lines):
    with open(lines, "r") as temp:
        fileLines = temp.read().splitlines()
        
    returnDict1 = {line.split()[0][:len(line.split()[0])-1]: [] for line in fileLines if len(line.split()) == 1}
    stops_and_times = []        #list of lists with stop and arriva time after ten
    for line in fileLines:
        split = line.split()
        if len(split) == 1:
            tramLine = split[0]
        elif len(split) >= 2:
            jointList = " ".join(split[:len(split)-1])
            returnDict1[tramLine[:len(tramLine)-1]].append(jointList)
            timeAfterTen = int(split[len(split)-1][3:5])        #last "letters" of i.e. '10:34' made into int
            stops_and_times.append([jointList, timeAfterTen])

    returnDict2 = {}
    pairs = []
    for stop_key in stops_and_times:

        current_key = stop_key[0]

        try:
            time_diff = stop_key[1] - prev_stop_key[1]
            if time_diff < 0:           # Can't have negative times, only happens with end stations on different lines
                pairs.append({previous_key,current_key})
            if {current_key, previous_key} in pairs:
                prev_stop_key = stop_key
            elif {current_key, previous_key} not in pairs and previous_key not in returnDict2:
                returnDict2[previous_key] = {}
                returnDict2[previous_key][current_key] = time_diff
                prev_stop_key = stop_key
                pairs.append({previous_key,current_key})
            elif {current_key, previous_key} not in pairs and previous_key in returnDict2:
                returnDict2[previous_key][current_key] = time_diff
                prev_stop_key = stop_key
                pairs.append({previous_key,current_key})
        except UnboundLocalError:
            prev_stop_key = stop_key

        previous_key = prev_stop_key[0]

    return returnDict1, returnDict2

def build_tram_network(stopfile, linefile):
    a = build_tram_stops(stopfile)
    b = build_tram_lines(linefile)
    triple_dictionary = {"stops": a, "lines": b[0], "times": b[1]}

    file_dest = TRAM_FILE

    try:
        with open(file_dest, "x") as f:
            f.write(json.dumps(triple_dictionary, indent=2))
    except FileExistsError:
        x = input("File already exists, do you want to delete and create a new one? (y or n)")
        if x == "y":
            import os
            os.remove(file_dest)
        with open(file_dest, "x") as f:
            f.write(json.dumps(triple_dictionary, indent=2))

def lines_via_stop(linedict, stop):
    return [tramline for tramline in linedict if stop in linedict[tramline]]

def lines_between_stops(linedict, stop1, stop2):
    
    return [tramline[:len(tramline)] for tramline in linedict if stop1 in linedict[tramline] and stop2 in linedict[tramline]]

def time_between_stops(linedict, timedict, line, stop1, stop2):

    if line in lines_via_stop(linedict, stop1) and line in lines_via_stop(linedict, stop2):  #checks if the line goes via both stops
        pass
    else:
        print("Error: stops are not along the same/chosen line")
        return(None)
    
    stop_indicies = [linedict[line].index(stop1),linedict[line].index(stop2)]
    stop_indicies.sort()

    stops_between_1and2 = linedict[line][stop_indicies[0]:stop_indicies[1]+1]
    
    stoptimes = []
    for i in range(len(stops_between_1and2)-1):
        current_stop = stops_between_1and2[i]
        next_stop = stops_between_1and2[i+1]

        if current_stop in timedict and next_stop in timedict[current_stop]:
            stoptimes.append(timedict[current_stop][next_stop])
        elif next_stop in timedict:
            stoptimes.append(timedict[next_stop][current_stop])
    
    return sum(stoptimes)

def distance_between_stops(stopdict, stop1, stop2):
    from math import radians,cos,sin,acos

    lon1 = radians(float(stopdict[stop1]["lon"]))
    lat1 = radians(float(stopdict[stop1]["lat"]))
    lon2 = radians(float(stopdict[stop2]["lon"]))
    lat2 = radians(float(stopdict[stop2]["lat"]))

    R = 6371.009 #earth radius from wiki-article referenced in lab desc.
    distance = R * acos( sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon1-lon2))
    return distance

def answer_query(tramdict, query):
    stops_in_query = [stop for stop in tramdict['stops'] if stop in query]
    query = query.split()

    if query[0] == "via":
        query_answer = (lines_via_stop(tramdict["lines"], stops_in_query[0]))
        return(query_answer)

    elif query[0] == "between":
        query_answer = (lines_between_stops(tramdict["lines"], stops_in_query[0], stops_in_query[1]))
        return(query_answer)
                
    elif query[0] == "time":
        query_answer = time_between_stops(tramdict["lines"], tramdict["times"], query[2], stops_in_query[0], stops_in_query[1])
        return(query_answer)
            
    elif query[0] == "distance":
       query_answer = distance_between_stops(tramdict["stops"], stops_in_query[0], stops_in_query[1])
       return(query_answer)

def dialogue(tramfile=TRAM_FILE):
    with open(tramfile) as f:
        tramfileObject = json.load(f)

    while True:
        user_query = input("Write query: ")
        splitQuery = user_query.split()
        try:
            if splitQuery[0] == "quit":
                    print("Quitting...")
                    break
            elif splitQuery[0] not in ["via", "between", "time", "distance"]:
                    print("Error: Invalid input query, try again")
            else:
                answer = answer_query(tramfileObject, user_query)
                if answer in [None, []]:
                    print("Error: Incorrectly formatted input, try again")
                else:
                    print(answer)
        except IndexError:
            print("Error: No input or wrong input given, type something!")
        except:
            print("Error: Incorrectly formatted input, try again")

if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network(STOP_FILE,LINE_FILE)
    else:
        pass