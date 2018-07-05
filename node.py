import math
import requests
import json
import re
class Node:
    node_id = 0
    API_KEY = []
    
    i = 0
    def __init__(self, lat, long, location):
        '''Constructor for a node which stores all the attributes of the nodes, i.e
        coordinates, location name, its children and their distance from the parent node'''
        self.latitude = lat
        self.longitude = long
        self.id = Node.node_id
        self.name = location
        
        self.n_children = 0
        Node.node_id += 1
        
        self.children = []
        self.children_distance = {}
        self.children_time = {}
        
        self.path = []
        
        self.g = 0
        self.h = 0
        self.f = self.g + self.h

    def addChild(self, child):
        '''Adds child to a node'''
        if child not in self.children:
            self.children.append(child)
        self.n_children = len(self.children)
        
    def generateURL(self, child):
        '''generates URL for API calls'''
        self.url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&" + \
					"origins={0},{1}&".format(self.latitude, self.longitude) + \
					"destinations={0},{1}&key={2}".format(child.latitude, child.longitude, Node.API_KEY[Node.i])
        return self.url
                    
    def calcDistance(self, child):
        '''returns actual road distance from google distance matrix API'''
        self.data = requests.get(self.generateURL(child)).text
        #print(json.loads(self.data)['rows'][0]['elements'][0]['distance']['text'])
        s = json.loads(self.data)['rows'][0]['elements'][0]['distance']['text']
        s = re.sub("[^.0-9]", "", s)
        #print (s + " km")
        return float(s)
    
    def calcTime(self, child):
        '''returns travel time from google distance matrix API'''
        self.data = requests.get(self.generateURL(child)).text
        s = json.loads(self.data)['rows'][0]['elements'][0]['duration']['text']
        s = re.sub("[^0-9]", "", s)
        #print (s + " min")
        return float(s)
		    
    def updateInfo(self):
        '''sets distance and time values for children of the node'''
        Node.API_KEY.append('AIzaSyA_S5j_EsZm9RS15qwqco9G7xHIfYzcu3U')
        Node.API_KEY.append('AIzaSyBHCrW7r98b-C5JNXpkBRFVJNEmAtc-VSY')
        Node.API_KEY.append('AIzaSyAvuLkCQfH6cgYmtOl_AhRyWfJjGUWYlKw')
        Node.API_KEY.append('AIzaSyAFtPEMUK6UwOG4t8zhqc4dmr3G_NKyhy0')
        for child in self.children:
            try:
                self.children_distance[child.id] = self.calcDistance(child)
                self.children_time[child.id] = self.calcTime(child)
            except:
                print('error occured')
                Node.i = (Node.i+1)%len(Node.API_KEY)
                self.children_distance[child.id] = self.calcDistance(child)
                self.children_time[child.id] = self.calcTime(child)
    
    def getInfo(self):
        return [self.id, self.children_distance, self.children_time]
    
    def updatePath(self, par_path):
        '''updates the most viable path from source to the given node'''
        self.path = []
        for i in par_path:
            
            self.path.append(i)
            if self == i:
                return
        self.path.append(self)
        
        
            