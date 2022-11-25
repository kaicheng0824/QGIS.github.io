import requests
import numpy as np
import pandas as pd
import time
import sys
import time
import os
import function
import zipfile
    
# Counter
start = time.time()

# # Get Node ID
sd_nodes = pd.read_csv('SDGE_Node_Info - Node.csv')
NodeInfo = sd_nodes.drop_duplicates(subset=['PNODE_ID'])
pnodes_id = NodeInfo['PNODE_ID'].to_numpy()
num_entries = pnodes_id.shape[0]

###### Merge Data ######
function.terminal_print('Merging Started, Time Elapsed: {}'.format(function.getTimeElapse(start)))
index = 0
df1 = pd.DataFrame()

for root, dirs, files in os.walk('SDGE_NODE_LMP'):
    for filename in files:
        if(filename[-4:]!='.csv'):
            continue
        
        # sys.stdout.write('Concatinating {}/{}'.format(index,257))
        # function.restart_line()

        index += 1
        path = os.path.join(root, filename)
        df2 = pd.read_csv('{}'.format(path))
        df1 = pd.concat([df1,df2],ignore_index=True)

Node = df1
# print(df1)

# Get LMP Online
LMP = Node[Node['LMP_TYPE']=='LMP'] 
MCC = Node[Node['LMP_TYPE']=='MCC'] # Congestion
MCE = Node[Node['LMP_TYPE']=='MCE'] # Energy
MCL = Node[Node['LMP_TYPE']=='MCL'] # Loss

# Get Time Series
function.terminal_print('Start Generating Time Series, Time Elapsed: {}'.format(function.getTimeElapse(start)))
pd_MCC,pd_MCC_Trans = function.generateTS(MCC)
pd_LMP,pd_LMP_Trans = function.generateTS(LMP)
pd_MCE,pd_MCE_trans = function.generateTS(MCE)
pd_MCL,pd_MCL_trans = function.generateTS(MCL)

pd_MCC_Trans = pd_MCC_Trans.iloc[1:]
pd_LMP_Trans = pd_LMP_Trans.iloc[1:]
pd_MCE_trans = pd_MCE_trans.iloc[1:]
pd_MCL_trans = pd_MCL_trans.iloc[1:]

# sort by time
pd_MCC_Trans = pd_MCC_Trans.sort_index(ascending=True)
pd_LMP_Trans = pd_LMP_Trans.sort_index(ascending=True)
pd_MCE_trans = pd_MCE_trans.sort_index(ascending=True)
pd_MCL_trans = pd_MCL_trans.sort_index(ascending=True)

function.creare_folder('SDGE_NODE_LMP_Plots')

function.terminal_print('Start Plotting and Saving Time Series, Time Elapsed: {}'.format(function.getTimeElapse(start)))

pd_MCC_Trans.to_csv('All_node_MCC.csv')
pd_LMP_Trans.to_csv('All_node_LMP.csv')
pd_MCE_trans.to_csv('All_node_MCE.csv')
pd_MCL_trans.to_csv('All_node_MCL.csv')

# Save Figure
function.plot_all_node(pd_MCC_Trans,'MCC')
function.plot_all_node(pd_LMP_Trans,'LMP')
function.plot_all_node(pd_MCE_trans,'MCE')

# # # Save Figure for each node
# for id in pnodes_id:
#     print(id)
#     function.plot_node_prices(pd_MCC_Trans,'SDGE Node MCC',id)
#     function.plot_node_prices(pd_MCE_trans,'SDGE Node MCE',id)
#     function.plot_node_prices(pd_LMP_Trans,'SDGE Node LMP',id)
#     # function.plot_node_prices(pd_MCL_trans,'SDGE Node MCC',id)