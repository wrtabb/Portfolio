import pandas as pd
import uproot
import json

# A function to convert elements with arrays into separate columns
def expand_arrays(dataframe,var_name):
    print(f'Expanding array:{var_name} into separate columns')
    old_var= var_name
    new_var = pd.DataFrame(dataframe[var_name].tolist(), columns=[var_name+'_1', var_name+'_2'])
    dataframe = dataframe.drop(columns=[var_name])  # Drop original columns
    dataframe = pd.concat([dataframe, new_var], axis=1)

    return dataframe

# The function that does all the work of loading a tree from a root file, converting tree into a dataframe, applying cuts, then saving to a pickel file
def load_root_file():
    # tree and json file names
    tree_name = 'recoTree/DYTree'
    json_name = 'variable_list.json'

    # Load data from json file
    with open(json_name) as j:
        data = json.load(j)

    # define tree variables to save to a dataframe
    #vars_to_keep = data['variables_to_keep']
    ele_vars = data['electron_variables']
    vtx_vars = data['vertex_variables']
    pho_vars = data['photon_variables']
    met_vars = data['met_variables']
    num_vars = data['num_variables']
    vars_to_keep = ele_vars+met_vars+num_vars

    num_vars_to_keep = len(vars_to_keep)
    print(f"Number of variables: {num_vars_to_keep}")
    # Define list of root files to load from
    file_list = data['root_files_to_load']

    # loop over root files to be loaded
    for x in range(len(file_list)):
        file_name = '../Data/background_selection/'
        file_name += file_list[x]
        cat_name = file_list[x]
        cat_name = cat_name[:-5]

        print(f"Loading file: {file_name}")
        
        # load tree from root file using uproot
        with uproot.open(file_name) as file:
            tree = file[tree_name]

        # define dataframe using variables listed in json file
        df_tmp1 = tree.arrays(filter_name=vars_to_keep, library="pd")
        df_tmp2 = df_tmp1[df_tmp1['Nelectrons']==2]

        # Place all array elements into separate columns for each electron
        for x in ele_vars:
            df = expand_arrays(df_tmp2,x)

        # add a column with the category name for later classification
        df['category'] = cat_name 

        nrows_expanded = len(df)
        print(f"After running expand_arrays(), dataframe now has {nrows_expanded} rows after applying dielectron condition")

        # Define name for save file
        save_name = file_name
        save_name = save_name[:-5]
        save_name += '.pkl'

        # Save dataframe in pickle file
        print(f"Saving root file as a pickle file here: {save_name}")
        df.to_pickle(save_name)

        print(df)
    # end loop over file_list

# Run function
load_root_file()
