from geopy.geocoders import Nominatim

nom = Nominatim()
n = nom.geocode("gachibowli")

database = []
i = 0
with open('local.txt','r') as file:
    data = file.read()
    data = data.split('\n')
    
    for line in data:
        i = i+1
        print(i)
        try:
            n = nom.geocode(line + ' ,Hyderabad, India')
            database.append([line, n.latitude, n.longitude])
            print([line, n.latitude, n.longitude])        

        except:
            print('Error occured while fetching data for: ' + line)
        
        
with open('database.txt', 'w') as file:
    
    for iter in database:
        file.write(iter[0] + ';' + str(iter[1]) + ';' + str(iter[2]) + '\n')

print(n)