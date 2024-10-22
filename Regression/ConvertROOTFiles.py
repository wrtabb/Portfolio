import IPython
import pandas as pd
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

    plt.hist(branches['Electron_pT'])
    plot.show()

load_root_file('../Data/background_selection/ZZ.root')
