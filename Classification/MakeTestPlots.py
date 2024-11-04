import pandas as pd
import matplotlib.pyplot as plt
import json

def MakePlot(df,var):
    data_to_plot = df[var]

    plt.hist(data_to_plot, bins=50, edgecolor='black')
    plt.xlabel(var)
    plt.ylabel('number of entries')

    tmp_save = file_name[8:-4]
    plot_save = '../Plots/'+tmp_save+'_'
    plot_save += var
    plot_save += '.png'

    print(f"Saving plot as {plot_save}\n")
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
    df.head()

    MakePlot(df,'Electron_pT_1')
    MakePlot(df,'Electron_eta_1')
    MakePlot(df,'Electron_phi_1')
    MakePlot(df,'Electron_pT_2')
    MakePlot(df,'Electron_eta_2')
    MakePlot(df,'Electron_phi_2')


