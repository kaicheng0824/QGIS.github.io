import requests
import numpy as np
import pandas as pd
import time
import time
import getLMP_function
import zipfile
import glob
import csv
import user_interface
import directory_setup
from datetime import date, timedelta
    
def getCAISOLMP(start,end):
    # Counter
    currentTime = time.time()

    # # Determine Start and End time
    template = 'http://oasis.caiso.com/oasisapi/SingleZip?resultformat=6&queryname=PRC_RTPD_LMP&version=3&startdatetime={}&enddatetime={}&market_run_id=RTPD&node={}' 
    start_time = str(start)+"T07:00-0000"
    print('Start Time: {}'.format(start_time))
    end_time = str(end)+'T07:00-0000'

    # # Get Node ID
    sd_nodes = pd.read_csv('./data/NodeMetaData.csv')
    NodeInfo = sd_nodes.drop_duplicates(subset=['PNODE_ID'])
    pnodes_id = NodeInfo['PNODE_ID'].to_numpy()
    num_entries = pnodes_id.shape[0]

    # # Prepare Array
    user_interface.terminal_print('Preparing API Links, Time Elapsed: {}'.format(getLMP_function.getTimeElapse(currentTime)))
    download_links = np.zeros((2,num_entries),dtype=object)
    for i in range(num_entries):
        download_links[1][i] = template.format(start_time,end_time,pnodes_id[i])
        download_links[0][i] = pnodes_id[i]

    # # # Consolidate
    NodeAndLink = pd.DataFrame(download_links.T,columns=['PNODE_ID','LINK'])
    NodeInfo = NodeInfo.set_index('PNODE_ID').join(NodeAndLink.set_index('PNODE_ID'))

    ####### Actual Downloading Starts Here########
    nodes = NodeInfo.index.to_numpy()
    links_list = NodeInfo['LINK'].to_numpy()
    N = nodes.shape[0]

    # # ##### Create Folder
    directory_setup.create_folder('./data/NODE_LMP')

    PNODE_chunked_list = list()
    chunk_size = 10

    for i in range(0, len(pnodes_id), chunk_size):
        PNODE_chunked_list.append(pnodes_id[i:i+chunk_size])

    # print(chunked_list)

    # BLA = ",".join(list(pnodes_id))
    # print(BLA)
    # req = requests.get(template.format(start_time,end_time,BLA))

    # ##### Iterate Through All Links and Download
    # exit()
    
    N = len(PNODE_chunked_list)
    for i in range(len(PNODE_chunked_list)):
        name_to_save = PNODE_chunked_list[i][0]+'_to_'+PNODE_chunked_list[i][-1]
        print('Downloading {}/{} {} started ---> '.format(i,N,name_to_save),end=' ')

        chunk = ",".join(list(PNODE_chunked_list[i]))
        # print(chunk)
        # print(template.format(start_time,end_time,chunk))
        # exit()
        # req = requests.get(links_list[i])
        req = requests.get(template.format(start_time,end_time,chunk))

        time.sleep(5)
        
        
        # print(name_to_save)

        with open('./data/NODE_LMP/{}.zip'.format(name_to_save),'wb') as output_file:
            output_file.write(req.content)
        
        user_interface.terminal_print('Download Completed, Time Elapsed: {}'.format(getLMP_function.getTimeElapse(currentTime)))

    files = glob.glob('./data/NODE_LMP/*.zip')
    for f in files:
        zf = zipfile.ZipFile(f, mode='r')
        zf.extractall("./data/NODE_LMP")
        zf.close()

def getNEISO(start,end,wait_time):
    sdate = date(int(start[0:4]),int(start[4:6]),int(start[6:]))
    edate = date(int(end[0:4]),int(end[4:6]),int(end[6:]))
    range = pd.date_range(sdate,edate-timedelta(days=0),freq='d')
    range = range.strftime("%Y%m%d")
    range = range.to_list()
    for thedate in range:
        url = 'http://www.iso-ne.com/static-transform/csv/histRpts/rt-lmp/lmp_rt_final_{}.csv'.format(thedate)
        print('Downloading {} for NEISO'.format(thedate),end=' ')

        response = requests.get(url)        

        with open('./data/NODE_LMP/NEISO{}.csv'.format(thedate), 'w') as f:
            writer = csv.writer(f)
            for line in response.iter_lines():
                writer.writerow(line.decode('utf-8').split(','))

def main(start,end):
    getCAISOLMP(start,end)

    # getNEISO('20220901','20220903',3)

