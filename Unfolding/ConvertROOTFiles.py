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
    gen_vars = data['generator_variables'] # contains arrays
    ele_vars = data['electron_variables'] # contains arrays
    num_vars = data['num_variables'] # no arrays

    # File to load
    file_name = '../Data/background_selection/DYLL_M50toInf.root'
    print(f"Loading file: {file_name}")
    
    # load tree from root file using uproot
    with uproot.open(file_name) as file:
        tree = file[tree_name]
        df_ele1 = tree.arrays(filter_name=ele_vars, library="pd")
        df_gen1 = tree.arrays(filter_name=gen_vars, library="pd")

    # filter rows with 2 electrons 
    df_ele2 = df_ele1[df_ele1['Nelectrons']==2]
    df_gen2 = df_gen1[df_gen1['GENnPair']==2]
    df_gen3 = df_gen2[abs(df_gen1['GENLepton_ID'])==11]

    # Place all array elements into separate columns for each electron
    df_ele3 = df_ele2
    df_gen4 = df_gen2
    for x in ele_vars:
        df_ele3 = expand_arrays(df_ele3,x)
    for x in gen_vars:
        df_gen4 = expand_arrays(df_gen4,x)

    # rename columns for gen leptons to those used by reco electrons
    for x in range(len(ele_vars)):
    df_gen5 = df_gen4.rename(columns={
        gen_vars[x]: ele_vars[x]
    })

    df_ele4 = reorder_electrons(df_ele3,ele_vars)
    df_gen6 = reorder_electrons(df_ele5,gen_vars)
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

parser = argparse.ArgumentParser(description='variable file to use')
parser.add_argument('--var_num')
args = parser.parse_args()

# Run function
convert_root_file(args.var_num)
