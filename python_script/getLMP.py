import requests
import numpy as np
import pandas as pd
import time
import sys
import time
import os
import getLMP_functions
import zipfile
import glob
    
def main():
    # Counter
    # start = time.time()

    # # # Determine Start and End time
    # template = 'http://oasis.caiso.com/oasisapi/SingleZip?resultformat=6&queryname=PRC_RTPD_LMP&version=3&startdatetime={}&enddatetime={}&market_run_id=RTPD&node={}' 
    # start_time = '20220901T07:00-0000'
    # end_time = '20220902T07:00-0000'

    # # # Get Node ID
    # sd_nodes = pd.read_csv('./data/NodeMetaData.csv')
    # NodeInfo = sd_nodes.drop_duplicates(subset=['PNODE_ID'])
    # pnodes_id = NodeInfo['PNODE_ID'].to_numpy()
    # num_entries = pnodes_id.shape[0]

    # # # Prepare Array
    # getLMP_functions.terminal_print('Preparing API Links, Time Elapsed: {}'.format(getLMP_functions.getTimeElapse(start)))
    # download_links = np.zeros((2,num_entries),dtype=object)
    # for i in range(num_entries):
    #     download_links[1][i] = template.format(start_time,end_time,pnodes_id[i])
    #     download_links[0][i] = pnodes_id[i]

    # # # # Consolidate
    # NodeAndLink = pd.DataFrame(download_links.T,columns=['PNODE_ID','LINK'])
    # NodeInfo = NodeInfo.set_index('PNODE_ID').join(NodeAndLink.set_index('PNODE_ID'))

    # ####### Actual Downloading Starts Here########
    # nodes = NodeInfo.index.to_numpy()
    # links_list = NodeInfo['LINK'].to_numpy()
    # N = nodes.shape[0]

    # # # ##### Create Folder
    # getLMP_functions.creare_folder('NODE_LMP')

    # # ##### Iterate Through All Links and Download
    # wait_time = input('Enter Connection Wait Time (Recommed more than 3 seconds if query huge time interval): ')
    # for i in range(N):
    #     print('Downloading {}/{} {} started ---> '.format(i,N,nodes[i]),end=' ')

    #     req = requests.get(links_list[i])

    #     time.sleep(int(wait_time))
        
    #     with open('NODE_LMP/{}.zip'.format(nodes[i]),'wb') as output_file:
    #         output_file.write(req.content)
        
    #     getLMP_functions.terminal_print('Download Completed, Time Elapsed: {}'.format(getLMP_functions.getTimeElapse(start)))

    # Extra Zip
    # os.system("Unzipping Files")

    files = glob.glob('./NODE_LMP/*.zip')
    for f in files:
        zf = zipfile.ZipFile(f, mode='r')
        zf.extractall("./NODE_LMP")
        zf.close()
    # for filename in os.listdir("./NODE_LMP"):
    #     if filename.endswith(".zip"):
    #         zipfile.ZipFile.extractall(path="./NODE_LMP")
            # print(filename)
            # name = os.path.splitext(os.path.basename(filename))[0]
            # if not os.path.isdir(name):
            #     try:
            #         zip = zipfile.ZipFile(filename)
            #         os.mkdir(name)
            #         zip.extractall(path=name)
            #     except zipfile.BadZipfile as e:
            #         print("Corrupted zip file: "+filename)
            #         try:
            #             os.remove(filename)
            #         except OSError as e: # this would be "except OSError, e:" before Python 2.6
            #             # if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            #             raise # re-raise exception if a different error occured    


