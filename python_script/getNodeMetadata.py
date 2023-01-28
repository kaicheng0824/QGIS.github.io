import json
import requests
import pandas as pd
import numpy as np
import os

def loadJSON():
    url = 'http://wwwmobile.caiso.com/Web.Service.Chart/api/v1/ChartService/GetPriceContourMap'
    resp = requests.get(url)
    with open('./data/NodeLocation.json', 'wb') as f:
        f.write(resp.content)

def generate_path(pnode,str_type):
    path = '<img src="./data/NODE_LMP_Plots/{}/{}.png" width="200" height="120"/>'
    LMP_path_df = pd.DataFrame()
    array = np.zeros(len(pnode),dtype=object)
    i = 0

    for node in pnode:
        array[i] = path.format(node,str_type)
        i = i + 1
    LMP_path_df = pd.DataFrame({str_type:list(array)})
    return LMP_path_df

def addHTMLPath(pnode,Node):
    LMP_path_df = generate_path(pnode,'NodeLMP')
    MCC_path_df = generate_path(pnode,'NodeMCC')
    MCE_path_df = generate_path(pnode,'NodeMCE')
    Node = pd.concat([Node,LMP_path_df],axis=1)
    Node = pd.concat([Node,MCC_path_df],axis=1)
    Node = pd.concat([Node,MCE_path_df],axis=1)
    
    return Node


def main():
    if(not os.path.isfile('./data/NodeLocation.json')):
        print('Connecting to Get Node Data')
        loadJSON()
    
    with open('./data/NodeLocation.json') as NodeLocation:
        NodeLocationRaw = NodeLocation.read()
    
    NodeLocationJSON = json.loads(NodeLocationRaw)
    allData = NodeLocationJSON['l'][2]['m']

    dfData = pd.DataFrame(allData)
    dfData.drop('t', axis=1, inplace=True)
    Lat = [x for x,y in dfData['c'][:]]
    Lng = [y for x,y in dfData['c'][:]]

    dfData.insert(1, 'Lat', Lat)
    dfData.insert(2, 'Lng', Lng)
    dfData.drop('c', axis=1, inplace=True)
    dfData = dfData.iloc[:,:5]
    pnode = dfData['n']

    dfData = addHTMLPath(pnode,dfData)
    dfData.columns = ['Lat', 'Lng', 'PNODE_ID', 'Type','ISO','NodeLMP','NodeMCC','NodeMCE']

    iso = input("Enter ISO Region to Query (APS, AVA, BANC, BCHA, CA, IPCO, LADWP, NV, NWMT, PACE, PACW, PGE, PNM, PSE, SCL, SRP, TEPC. TIDC, TPWR):")
    dfData = dfData[dfData['ISO']==iso]

    dfData.to_csv('./data/NodeMetaData.csv')
        
# if __name__ == "__main__":
#     main()


