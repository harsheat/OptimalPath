from node import Node
from operator import itemgetter
import pickle


from math import radians, cos, sin, asin, sqrt
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



nodes = []


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

with open('graphInfo.pkl', 'wb') as file:
    i = 0        
    for node in nodes:
        i += 1
        print(node.n_children, node.name)
        node.updateInfo()
        element = node.getInfo()
        graphInfo.append(element)
        
    pickle.dump(graphInfo, file)

with open('graphInfo.pkl', 'rb') as file:
    data = pickle.load(file)
    
    for node in data:
        print(node)

print(nodes[-1].id)
print(haversine(nodes[0].latitude, nodes[0].longitude, nodes[100].latitude, nodes[100].longitude), nodes[0].name, nodes[100].name)
print(nodes[377].name)
