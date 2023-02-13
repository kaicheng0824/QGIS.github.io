import requests
import numpy as np
import pandas as pd
import time
import sys
import time
import os
import getLMP_function
import zipfile
import user_interface
import directory_setup
    
def main():
    # Counter
    start = time.time()

    ## Get Node ID
    nodes = pd.read_csv('./data/NodeMetaData.csv')
    NodeInfo = nodes.drop_duplicates(subset=['PNODE_ID'])
    pnodes_id = NodeInfo['PNODE_ID'].to_numpy()
    num_entries = pnodes_id.shape[0]
    print(num_entries)

    ###### Merge Data ######
    user_interface.terminal_print('Merging Started, Time Elapsed: {}'.format(getLMP_function.getTimeElapse(start)))
    index = 0
    df1 = pd.DataFrame()

    for root, dirs, files in os.walk('./data/NODE_LMP'):
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

    # Get LMP Online
    LMP = Node[Node['LMP_TYPE']=='LMP'] 
    MCC = Node[Node['LMP_TYPE']=='MCC'] # Congestion
    MCE = Node[Node['LMP_TYPE']=='MCE'] # Energy
    MCL = Node[Node['LMP_TYPE']=='MCL'] # Loss

    # Get Time Series
    user_interface.terminal_print('Start Generating Time Series, Time Elapsed: {}'.format(getLMP_function.getTimeElapse(start)))
    pd_MCC,pd_MCC_Trans = getLMP_function.generateTS(MCC)
    pd_LMP,pd_LMP_Trans = getLMP_function.generateTS(LMP)
    pd_MCE,pd_MCE_trans = getLMP_function.generateTS(MCE)
    pd_MCL,pd_MCL_trans = getLMP_function.generateTS(MCL)

    pd_MCC_Trans = pd_MCC_Trans.iloc[1:]
    pd_LMP_Trans = pd_LMP_Trans.iloc[1:]
    pd_MCE_trans = pd_MCE_trans.iloc[1:]
    pd_MCL_trans = pd_MCL_trans.iloc[1:]

    # sort by time
    pd_MCC_Trans = pd_MCC_Trans.sort_index(ascending=True)
    pd_LMP_Trans = pd_LMP_Trans.sort_index(ascending=True)
    pd_MCE_trans = pd_MCE_trans.sort_index(ascending=True)
    pd_MCL_trans = pd_MCL_trans.sort_index(ascending=True)

    directory_setup.create_folder('NODE_LMP_Plots')

    user_interface.terminal_print('Start Plotting and Saving Time Series, Time Elapsed: {}'.format(getLMP_function.getTimeElapse(start)))

    pd_MCC_Trans.to_csv('./data/All_node_MCC.csv')
    pd_LMP_Trans.to_csv('./data/All_node_LMP.csv')
    pd_MCE_trans.to_csv('./data/All_node_MCE.csv')
    pd_MCL_trans.to_csv('./data/All_node_MCL.csv')

    # Add Average MCC to NodeMetaData
    AllNodeMCC = pd.read_csv('./data/All_node_MCC.csv')
    avg_mcc = AllNodeMCC.describe().loc['mean'].to_frame()
    avg_mcc_value = avg_mcc['mean'].to_numpy()
    avg = pd.DataFrame({"PNODE_ID": avg_mcc.index, "Average MCC": list(avg_mcc_value)})

    # print(avg)

    nodes = pd.merge(nodes,avg, on='PNODE_ID', how='inner')
    nodes.to_csv('./data/NodeMetaData.csv')

    # Save Figure
    getLMP_function.plot_all_node(pd_MCC_Trans,'MCC',num_entries-1)
    getLMP_function.plot_all_node(pd_LMP_Trans,'LMP',num_entries-1)
    getLMP_function.plot_all_node(pd_MCE_trans,'MCE',num_entries-1)

    # # # Save Figure for each node
    for id in pnodes_id:
        # print(id)
        getLMP_function.plot_node_prices(pd_MCC_Trans,'NodeMCC',id,num_entries-1)
        getLMP_function.plot_node_prices(pd_MCE_trans,'NodeMCE',id,num_entries-1)
        getLMP_function.plot_node_prices(pd_LMP_Trans,'NodeLMP',id,num_entries-1)
        getLMP_function.plot_node_prices(pd_MCL_trans,'NodeMCC',id,num_entries-1)