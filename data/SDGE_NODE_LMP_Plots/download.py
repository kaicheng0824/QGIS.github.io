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

# # Determine Start and End time
template = 'http://oasis.caiso.com/oasisapi/SingleZip?resultformat=6&queryname=PRC_RTPD_LMP&version=3&startdatetime={}&enddatetime={}&market_run_id=RTPD&node={}' 
start_time = '20220901T07:00-0000'
end_time = '20220907T07:00-0000'

# # Get Node ID
sd_nodes = pd.read_csv('CAISO_SDGE_Node.csv')
NodeInfo = sd_nodes.drop_duplicates(subset=['PNODE_ID'])
pnodes_id = NodeInfo['PNODE_ID'].to_numpy()
num_entries = pnodes_id.shape[0]

# # Prepare Array
function.terminal_print('Preparing API Links, Time Elapsed: {}'.format(function.getTimeElapse(start)))
download_links = np.zeros((2,num_entries),dtype=object)
for i in range(num_entries):
    download_links[1][i] = template.format(start_time,end_time,pnodes_id[i])
    download_links[0][i] = pnodes_id[i]

# # Consolidate
NodeAndLink = pd.DataFrame(download_links.T,columns=['PNODE_ID','LINK'])
NodeInfo = NodeInfo.set_index('PNODE_ID').join(NodeAndLink.set_index('PNODE_ID'))

# ###### Actual Downloading Starts Here########
nodes = NodeInfo.index.to_numpy()
links_list = NodeInfo['LINK'].to_numpy()
N = nodes.shape[0]

# ##### Create Folder
function.creare_folder('SDGE_NODE_LMP_{}_to{}'.format(start_time,end_time))

# ##### Iterate Through All Links and Download
for i in range(N):
    print('Downloading {}/{} {} started ---> '.format(i,N,nodes[i]),end=' ')

    req = requests.get(links_list[i])
    time.sleep(5)
    
    with open('SDGE_NODE_LMP/{}.zip'.format(nodes[i]),'wb') as output_file:
        output_file.write(req.content)
    
    function.terminal_print('Download Completed, Time Elapsed: {}'.format(function.getTimeElapse(start)))

# Extra Zip
os.system("Unzipping Files")
os.system('cd/SDGE_NODE_LMP')