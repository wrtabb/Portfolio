import pandas as pd
import uproot
import json
import argparse

# A function to convert elements with arrays into separate columns
def expand_arrays(dataframe,var_name):
    print(f'Expanding array:{var_name} into separate columns')
    try:
        new_columns = pd.DataFrame(dataframe[var_name].tolist(), 
                                   columns = [f'{var_name}_1', f'{var_name}_2'],
                                   index = dataframe.index)
        dataframe = dataframe.drop(columns=[var_name])
        dataframe = pd.concat([dataframe, new_columns], axis=1)

    except ValueError as e:
        print(f"Error expanding {var_name}: {e}")
    return dataframe

# Define a function to ensure higher pT electron is always in *_1 columns
def reorder_electrons(df, electron_vars):
    for index, row in df.iterrows():
        if row['Electron_pT_2'] > row['Electron_pT_1']:
            # Swap each variable
            for var in electron_vars:
                # Swap values between {var}_1 and {var}_2
                df.at[index, f'{var}_1'], df.at[index, f'{var}_2'] = row[f'{var}_2'], row[f'{var}_1']
    return df

def convert_root_file(var_num):
    json_name = (f'variables_{var_num}.json')
    # tree and json file names
    tree_name = 'recoTree/DYTree'
    print(f'Loading variables from json file: {json_name}')

    # Load data from json file
    with open(json_name) as j:
        data = json.load(j)

    # define tree variables to save to a dataframe
    #vars_to_keep = data['variables_to_keep']
    num_vars = data['num_variables']
    jet_vars = data['jet_variables']
    ele_vars = data['electron_variables']
    unc_vars = data['uncorrEle_variables']
    pho_vars = data['photon_variables']
    pup_vars = data['pileup_variables']
    met_vars = data['met_variables']
    vars_to_keep = ele_vars+pup_vars+met_vars+num_vars

    # Define list of root files to load
    #file_list = data['files_all_categories']
    file_list = data['files_binary']

    # loop over root files to be loaded
    cat_num = 0
    for x in file_list:
        x += '.root'
        file_name = '../Data/background_selection/'+x
        print(f"Loading file: {file_name}")
        
        # load tree from root file using uproot
        with uproot.open(file_name) as file:
            tree = file[tree_name]
            df_tmp1 = tree.arrays(filter_name=vars_to_keep, library="pd")

        # filter rows with 2 electrons 
        df_tmp2 = df_tmp1[df_tmp1['Nelectrons']==2]

        num_before_cut = len(df_tmp1)
        num_after_cut = len(df_tmp2)
        print(f'There are {num_before_cut} rows before electron cut')
        print(f'There are {num_after_cut} rows after electron cut')

        # Place all array elements into separate columns for each electron
        df_tmp3 = df_tmp2
        for x in ele_vars:
            df_tmp3 = expand_arrays(df_tmp3,x)
        #df_tmp4 = df_tmp3
        #for x in jet_vars:
        #    df_tmp4 = expand_arrays(df_tmp4,x)

        df = df_tmp3
        df = reorder_electrons(df,ele_vars)
        # add a column with the category name for later classification
        df['category'] = cat_num
        cat_num = cat_num + 1

        nrows_expanded = len(df)
        print(f"After running expand_arrays(), dataframe now has {nrows_expanded} rows")

        # Define name for save file
        save_name = file_name
        save_name = save_name[:-5]
        save_name += (f'_{var_num}.pkl')

        df = df[:25000]
        df = df.reset_index(drop=True)
        # Save dataframe in pickle file
        print(f"Saving pickle file: {save_name}")
        df.to_pickle(save_name)
        print(df)
        del df
    # end loop over file_list

parser = argparse.ArgumentParser(description='variable file to use')
parser.add_argument('--var_num')
args = parser.parse_args()

# Run function
convert_root_file(args.var_num)
