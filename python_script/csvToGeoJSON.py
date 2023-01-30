import csv
import json
from collections import OrderedDict

def main(filename):
    li = []
    with open('./data/{}'.format(filename), newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            d = OrderedDict()
            d['type'] = 'Feature'
            d['properties'] = {
                'PNODE_ID': row['PNODE_ID'],
                'RES_TYPE': row['Type'],
                'Lat': row['Lat'],
                'Long': row['Lng'],
                'SDGENodeLMP': row['NodeLMP'],
                'SDGENodeMCC': row['NodeMCC'],
                'SDGENodeMCE': row['NodeMCE'],
                'Average MCC': row['Average MCC']
            }
            d['geometry'] = {
                'type': 'Point',
                'coordinates': [float(row['Lng']), float(row['Lat'])]
            }
            li.append(d)

    d = OrderedDict()
    d['type'] = 'FeatureCollection'
    d['name'] = "CAISONodesByAverageMCC_3"
    d['crs'] = {}
    d['crs']['type'] = 'name'
    d['crs']['properties'] = {}
    d['crs']['properties']['name'] = 'urn:ogc:def:crs:OGC:1.3:CRS84'

    # d['crs'] = "crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84"}}
    d['features'] = li

    # print(d)

    with open('./data/CAISONodesByAverageMCC_3.js','w') as f:
        f.write('var json_CAISONodesByAverageMCC_3 = ')
        json.dump(d,f,indent=2)