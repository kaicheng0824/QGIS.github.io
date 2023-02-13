import os

def create_folder(path_name):
    if not os.path.exists(path_name):
        # if the demo_folder directory is not present 
        # then create it.
        os.makedirs(path_name)