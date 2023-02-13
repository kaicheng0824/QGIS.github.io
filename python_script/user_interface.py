import sys
import time

def getISO():
    # Initialization
    iso_input_message = "Enter ISO Regions to Query (APS, AVA, BANC, BCHA, CA, IPCO, LADWP, NV, NWMT, PACE, PACW, PGE, PNM, PSE, SCL, SRP, TEPC, TIDC, TPWR, NewEngland): "
    supported_iso = ['APS', 'AVA', 'BANC', 'BCHA', 'CA', 'IPCO', 'LADWP', 'NV', 'NWMT', 'PACE', 'PACW', 'PGE', 'PNM', 'PSE', 'SCL', 'SRP', 'TEPC', 'TIDC', 'TPWR','NewEngland']

    # Get User input
    iso = input(iso_input_message).split(',')

    # Checking Valid Input
    while list(set(iso) - set(supported_iso)):
        iso = input("Invalid: Please input from this list (APS, AVA, BANC, BCHA, CA, IPCO, LADWP, NV, NWMT, PACE, PACW, PGE, PNM, PSE, SCL, SRP, TEPC. TIDC, TPWR,NewEngland): (Quit by typing quit) ")
        iso =  iso.split(',')
        if(iso==['quit']):
            exit()
    
    return iso

def getStartTime():
    message = 'Please enter the start date of your query in YYYYMMDD Format (E.g. 20220901): '
    starttime = input(message)

    return starttime

def getEndTime():
    message = 'Please enter the end date of your query in YYYYMMDD Format (E.g. 20220901): '
    endttime = input(message)
    
    return endttime

def terminal_print(string):
    sys.stdout.write(string)
    restart_line()

def restart_line():
    sys.stdout.flush()
    time.sleep(0.02)
    sys.stdout.write('\r')
    sys.stdout.flush()