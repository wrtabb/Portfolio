import pandas as pd
import uproot
import json

# The function that does all the work of loading a tree from a root file, converting tree into a dataframe, applying cuts, then saving to a pickel file
def load_root_file():
    # tree and json file names
    tree_name = 'recoTree/DYTree'
    json_name = 'variable_list.json'

    # Load data from json file
    with open(json_name) as j:
        data = json.load(j)

    # define tree variables to save to a dataframe
    vars_to_keep = data['variables_to_keep']
    # Define list of root files to load from
    file_list = data['root_files_to_load']

    # loop over root files to be loaded
    for x in range(len(file_list)):
        file_name = '../Data/background_selection/'
        file_name += file_list[x]

        print(f"Loading file: {file_name}")
        
        # load tree from root file using uproot
        with uproot.open(file_name) as file:
            tree = file[tree_name]

        # define dataframe using variables listed in json file
        df = tree.arrays(filter_name=vars_to_keep, library="pd")

        # determine number of events (rows in dataframe)
        nrows_before = len(df)
        print(f"Created dataframe with {nrows_before} rows before applying dielectron condition")

        # apply selection criterion: only keep events with two electrons
        nelectron_condition = (df['Nelectrons']!=2)
        df = df[~nelectron_condition]

        # determine number of events left after selection applied
        nrows_after = len(df)
        print(f"Dataframe now has {nrows_after} rows after applying dielectron condition")
        print(df['Nelectrons'])

        # Define name for save file
        save_name = file_name
        save_name = save_name[:-5]
        save_name += '.pkl'

        # Save dataframe in pickle file
        print(f"Saving root file as a pickle file here: {save_name}")
        df.to_pickle(save_name)
        print()
    # end loop over file_list

# Run function
load_root_file()
