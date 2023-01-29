import csv
import json
from collections import OrderedDict

li = []
with open('./data/NodeMetaData.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        d = OrderedDict()
        d['type'] = 'Feature'
        d['geometry'] = {
            'type': 'Point',
            'coordinates': [float(row['Lat']), float(row['Lng'])]
        }
        li.append(d)

d = OrderedDict()
d['type'] = 'FeatureCollection'
d['name'] = "CAISONodesByAverageMCC_3"
d['crs'] = "CAISONodesByAverageMCC_3"
d['features'] = li

print(d)

with open('./data/output.js','w') as f:
    f.write('var json_CAISONodesByAverageMCC_3 = ')
    json.dump(d,f,indent=2)