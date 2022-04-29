import json

#creare il JSON

o = {
  "people": 5,
  "latitude": 1.001,
  "longitude": 1.001,
  "speed": 50 
}

data = json.dumps(o)

print(data)

#Smazzare il JSON
#
#dati = json.loads(data)
#
#print(dati["speed"])