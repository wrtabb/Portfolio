import IPython
import pandas as pd
import numpy as np
import fastparquet
import uproot
import matplotlib.pyplot as plt
import json

def load_root_file():
    tree_name = 'recoTree/DYTree'
    json_name = 'variable_list.json'

    with open(json_name) as j:
        data = json.load(j)

    vars_to_keep = data['variables_to_keep']
    file_list = data['files_to_load']

    for x in range(len(file_list)):
        file_name = '../Data/background_selection/'
        file_name += file_list[x]

        print(f"Loading file: {file_name}")
        with uproot.open(file_name) as file:
            tree = file[tree_name]

        df = tree.arrays(filter_name=vars_to_keep, library="pd")
        nrows_before = len(df)
        print(f"Created dataframe with {nrows_before} rows before applying dielectron condition")

        nelectron_condition = (df['Nelectrons']<1)
        df = df[~nelectron_condition]

        nrows_after = len(df)
        print(f"Dataframe now has {nrows_after} rows after applying dielectron condition")
        print(df['Nelectrons'])
        save_name = file_name
        save_name = save_name[:-5]
        save_name += '.pkl'

        print(f"Saving root file as a pickle file here: {save_name}")
        df.to_pickle(save_name)
        print()
    # end loop over file_list

load_root_file()
