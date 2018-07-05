from node import Node
from operator import itemgetter
import pickle
import gmplot
from math import radians, cos, sin, asin, sqrt
import stringdist

nodes = []

def haversine(lon1, lat1, lon2, lat2):
    '''Calculates haversine distance which is used as a heuristic
    function for A* algorithm'''
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    km = 6371* c
    return km


with open('database.txt', 'r') as file:
    data = file.read()
        
    data = data.split('\n')
    for line in data:
        line = line.split(';')
        try:
            new_node = Node(float(line[1]), float(line[2]), line[0])
            nodes.append(new_node)
        except:
            pass

for node in nodes:
    temp=[]
    for destnode in nodes:
        if node == destnode:
            continue
        else:
            temp.append([haversine(node.longitude, node.latitude, destnode.longitude, destnode.latitude),destnode])
    sorted_dist = sorted(temp, key = itemgetter(0))
    for i in range(5-node.n_children+1):
        node.addChild(sorted_dist[i][1])
        sorted_dist[i][1].addChild(node)

graphInfo = []


with open('graphInfo.pkl', 'rb') as file:
    data = pickle.load(file)    
    for nodeInfo in data:
        id = nodeInfo[0]
        node = nodes[id]
        node.children_distance = nodeInfo[1]
        node.children_time = nodeInfo[2]
        




def getLocations(src, dest):
    '''matches the user input string with the best possible locations
    in the database using edit distance'''
    mindist = 1000
    mindist1 = 1000
    srcname = ""
    destname = ""
    for node in nodes:
        if stringdist.levenshtein(src, node.name) < mindist:
            mindist = stringdist.levenshtein(src, node.name)
            srcname = node.name
        if stringdist.levenshtein(dest, node.name) < mindist1:
            mindist1 = stringdist.levenshtein(dest, node.name)
            destname = node.name
    return srcname, destname
    


def getValue(node):
    '''returs the f-value of a node'''
    return node.g + node.h

def getTime(path):
    '''returns the total time taken from source to destination using the path'''
    time = 0
    child = path[0]
    for node in path[1:]:
        try:
            time += node.children_time[child.id]
        except:
            pass
        child = node
    
    return time
################################# A* Implementation #############################
def findPath(source, destination):
    i = 0
    j = 0
    source, destination = getLocations(source, destination)
    for node in nodes:
        if node.name == destination:
            destnode = node
            i = 1
        if node.name == source:
            sourcenode = node
            j = 1

        if i and j:
            break
    
    sourcenode.path.append(sourcenode)
    openlist = []
    closedlist = []
    openlist.append(sourcenode)
    
    sourcenode.h = haversine(sourcenode.longitude, sourcenode.latitude, destnode.longitude, destnode.latitude)
    
    while len(openlist) != 0:
        current = openlist[0]
        

        if current == destnode:
            for loc in destnode.path:
                print(loc.name)
            return destnode.path
        
        for child in current.children:
            
            hvalue = haversine(child.longitude, child.latitude, destnode.longitude, destnode.latitude)
            gvalue = current.children_distance[child.id] + current.g
            if child not in openlist and child not in closedlist:
                child.h = hvalue
                child.g = gvalue
                openlist.append(child)
                child.updatePath(current.path)
            elif child in openlist:
                if child.g > gvalue:
                    child.g = gvalue
                    child.updatePath(current.path)
            elif child in closedlist:
                if child.g > gvalue:
                    child.g = gvalue
                    openlist.append(child)
                    closedlist.remove(child)
                    child.updatePath(current.path)
                    
                    
            closedlist.append(current)
            try:
                openlist.remove(current)
            except:
                pass

        openlist = sorted(openlist, key=getValue)
        
    
path = findPath(input("Enter Source: "), input("Enter Destination: "))
print("")
time = getTime(path)
print("Estimated Time: ", str(time), 'mins')
print("Total Distance to be travelled: ", path[-1].g, 'km')
lat = []
long = []
for location in path:
    lat.append(location.latitude)
    long.append(location.longitude)

google_map = gmplot.GoogleMapPlotter((lat[0]+lat[-1])/2, (long[0]+long[-1])/2, 12)
google_map.plot(lat, long, 'cornflowerblue', marker=False, edge_width=7)
google_map.scatter(lat,long,'#FF0000', size=60, marker=True, c=None, s=None)
google_map.draw('map.html')

data = ''
with open('map.html','r') as file:
    data = file.read()

data = data.replace('\\','/')
with open('map.html', 'w') as file:
    file.write(data)








