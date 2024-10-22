import IPython
import pandas as pd
import numpy as np
import fastparquet
import uproot
import matplotlib.pyplot as plt

def load_root_file(file_name):
    file = uproot.open(file_name)    
    #print(file.keys())
    #print(file['recoTree/DYTree'])

    tree = file['recoTree/DYTree']
    #print(tree.keys())

    branches = tree.arrays()
    #print(branches['Electron_pT'])

    nEvents = 1000
    elePt = np.zeros(shape=nEvents)
    for i in range(nEvents):
        event_len = len(branches['Electron_pT'][i])
        if event_len > 0:
            for j in range(event_len):
                elePt[i] += branches['Electron_pT'][i][j]
            # end loop over elements in each event
        else:
            elePt[i]=-100
        # end if length
    # end loop over events

    plt.hist(elePt,bins=25)
    plt.xlabel('electron p_T [GeV]')
    plt.ylabel('num entries')
    plt.show()
load_root_file('../Data/background_selection/ZZ.root')
