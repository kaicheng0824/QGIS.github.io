import json
import requests
import pandas as pd
import numpy as np
import os

def loadJSON():
    url = 'http://wwwmobile.caiso.com/Web.Service.Chart/api/v1/ChartService/GetPriceContourMap'
    resp = requests.get(url)
    with open('./data/NodeLocationOASIS.json', 'wb') as f:
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

def loadOASIS_JSON():
    if(not os.path.isfile('./data/NodeLocationOASIS.json')):
        print('Connecting to Get OASIS Node Data')
        loadJSON()

def processOASIS():
    with open('./data/NodeLocationOASIS.json') as NodeLocation:
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
    return dfData

def loadNewEngland():
    NE_nodes = pd.read_csv('./data/new_england_node.csv')
    NE_nodes.columns = NE_nodes.iloc[0]
    NE_nodes = NE_nodes.iloc[1:,:]
    NE_nodes = NE_nodes[['Latitude', 'Longitude','Node Name']]

    Node = ['Network']*NE_nodes.index.size
    NE_nodes['Type'] = Node

    ISO = ['NewEngland']*NE_nodes.index.size
    NE_nodes['ISO'] = ISO

    NE_nodes = addHTMLPath(NE_nodes['Node Name'],NE_nodes)
    NE_nodes.columns = ['Lat', 'Lng', 'PNODE_ID', 'Type','ISO','NodeLMP','NodeMCC','NodeMCE']
    NE_nodes = NE_nodes.dropna()
    print(NE_nodes)
    return NE_nodes


def main(iso):
    # Initialization
    oasis = ['APS', 'AVA', 'BANC', 'BCHA', 'CA', 'IPCO', 'LADWP', 'NV', 'NWMT', 'PACE', 'PACW', 'PGE', 'PNM', 'PSE', 'SCL', 'SRP', 'TEPC', 'TIDC', 'TPWR']
    contain_oasis = False

    df_list = []
    
    # Get OASIS
    queried_oasis = list(set.intersection(set(iso), set(oasis)))
    print(queried_oasis)
    if(len(queried_oasis) > 0):
        contain_oasis = True
        loadOASIS_JSON()
        df_OASIS = processOASIS()
        query_oasis = df_OASIS[df_OASIS['ISO'].isin(queried_oasis)]
        df_list.append(query_oasis)

    # Get other ISO
    if('NewEngland' in iso):
        print('pricessing newenglans')
        df_NE = loadNewEngland()
        df_list.append(df_NE)
    
    # Concat All ISO
    querydf = pd.concat(df_list,axis=0)

    querydf.to_csv('./data/NodeMetaData.csv')
    count = int(querydf.describe().loc['count']['Lat'])
    print('Queried: {} Data Count: {}'.format(iso,count))
    


