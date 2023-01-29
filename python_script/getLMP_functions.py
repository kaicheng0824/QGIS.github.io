import requests
import numpy as np
import pandas as pd
import time
import sys
import time
import os
import matplotlib.pyplot as plt

def terminal_print(string):
    sys.stdout.write(string)
    restart_line()

def restart_line():
    sys.stdout.flush()
    time.sleep(0.02)
    sys.stdout.write('\r')
    sys.stdout.flush()

def generateTS(LMP):
    Node_ID = LMP['NODE_ID'].drop_duplicates().to_numpy()
    time = LMP['INTERVALSTARTTIME_GMT'].drop_duplicates().to_numpy()
    Node_ID.dtype = object
    time.dtype = object

    N_node = Node_ID.shape[0]
    N_timeStep = time.shape[0]
    total_N = LMP.shape[0]
    
    LMP_matrix = np.zeros((N_node,N_timeStep+1),dtype=object)

    # total_N = N_node*N_timeStep
    PRC_col = -3
    node_col = -10

    for i in range(total_N):
        LMP_matrix[int(i/N_timeStep)][int(i%N_timeStep)+1] = LMP.iloc[i][PRC_col] # Plus one to make space for PNODE index

    for i in range(N_node):
        LMP_matrix[i][0] = Node_ID[i]
        
    time = np.insert(time,0,'PNODE_ID')
    pd_LMP = pd.DataFrame(LMP_matrix,columns=time,index=Node_ID)
    pd_LMP_Trans = pd_LMP.T
    
    return pd_LMP,pd_LMP_Trans

def creare_folder(name):
    if not os.path.exists(name):
        # if the demo_folder directory is not present 
        # then create it.
        os.makedirs(name)

def plot_all_node(df,title,node_count):
    time_step = df.index.to_numpy()
    for i in range(time_step.shape[0]):
        time_step[i] = pd.to_datetime(time_step[i])

    for i in range(node_count):
        a =  df.to_numpy()[:,i]
        plt.plot(time_step,a.T,alpha=0.03,color='black')
        plt.xticks(rotation=45,fontsize=16)
        plt.yticks(fontsize=16)
        plt.title('SDGE Node {} (All Nodes)'.format(title),fontsize=24)
        plt.xlabel('Day 1 to Day 7',fontsize=20)
        plt.ylabel('Congestion Price ($)',fontsize=20)
    
    plt.savefig("./data/NODE_LMP_Plots/{}_All_Node.png".format(title),bbox_inches="tight")
    plt.close()

def plot_node_prices(df,title,node,node_count):
    time_step = df.index.to_numpy()[1:]

    for i in range(time_step.shape[0]):
        time_step[i] = pd.to_datetime(time_step[i])
    
    for i in range(node_count):
        PNODE = df.columns.to_numpy()[i]

        if(str(PNODE)==str(node)):
            a =  df.to_numpy()[:,i][1:]
            plt.plot(time_step,a,alpha=1,color='black')
            plt.xticks(rotation=45)
            plt.title(title+': '+node)
            # plt.xlabel('Time Series 09/01 to 09/05')
            plt.ylabel('Congestion Price ($)',fontsize=20)
            break
    
    while ' ' in title:
        title = title.replace(' ', '')

    creare_folder('./data/NODE_LMP_Plots/{}'.format(node))
    plt.savefig("./data/NODE_LMP_Plots/{}/{}.png".format(node,title))
    plt.close()

def getTimeElapse(theTime):
    return time.time() - theTime