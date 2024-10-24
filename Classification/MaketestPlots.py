import pandas as pd
import matplotlib.pyplot as plt
import json

def MakePlot(df,var):
    elePt = df[var]
    flattened_data = [item for sublist in elePt for item in sublist]

    plt.hist(flattened_data, bins=50, edgecolor='black')
    plt.xlabel(var)
    plt.ylabel('number of entries')

    plot_save = file_name[:-4]
    plot_save += "_"
    plot_save += var
    plot_save += '.png'

    print(f"Saving plot as {plot_save}")
    plt.savefig(plot_save,dpi=300)
    plt.close()

json_name = 'variable_list.json'
with open(json_name) as j:
    data = json.load(j)

pickle_files = data['pickle_files_to_load']

for x in range(len(pickle_files)):
    file_name = '../Data/background_selection/'
    file_name += pickle_files[x]
    print(f"Loading pickle file {file_name}")
    df = pd.read_pickle(file_name)

    MakePlot(df,'Electron_pT')
    MakePlot(df,'Electron_eta')
    MakePlot(df,'Electron_phi')
    print()
