import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data/general/combined_results.csv')

vote_types = ['TOT', 'VBM', 'IPEV']
tally_types = ['Daily Tally %', 'Cumulative %']
graph_names = {
    'TOT': 'Early Voting',
    'VBM': 'Early Voting (VBM)',
    'IPEV': 'Early Voting (IPEV)'
}

fig, ax = plt.subplots(ncols=2, nrows=3, figsize=(15, 10))

for i, vote_type in enumerate(vote_types):
    for j, tally_type in enumerate(tally_types):
        rep = data[['Days until Eday', f'REP-{vote_type}: {tally_type}']].dropna()
        dem = data[['Days until Eday', f'DEM-{vote_type}: {tally_type}']].dropna()
        oth = data[['Days until Eday', f'OTH-{vote_type}: {tally_type}']].dropna()

        
        ax[i,j].plot(rep['Days until Eday'], rep[f'REP-{vote_type}: {tally_type}'], label='Republican', color='red', linewidth=2, marker='o')
        ax[i,j].plot(dem['Days until Eday'], dem[f'DEM-{vote_type}: {tally_type}'], label='Democratic', color='blue', linewidth=2, marker='o')
        ax[i,j].plot(oth['Days until Eday'], oth[f'OTH-{vote_type}: {tally_type}'], label='Other', color='green', linewidth=2, marker='o')
        
        if tally_type == 'Cumulative %':
            ax[i,j].set_title(f'FL-06 Cumulative {graph_names[vote_type]} Voter Share')
        else:
            ax[i,j].set_title(f'FL-06 Daily {graph_names[vote_type]} Voter Share')
        ax[i,j].set_xlabel('Days until Election Day')
        ax[i,j].set_ylabel('Percentage (%)')

        # Add vertical line for IPEV start if necessary
        if vote_type == 'TOT':
            ax[i,j].axvline(x=10, color='black', linestyle='--')
            ax[i,j].text(10.5, 51, 'IPEV begins', rotation=90, fontsize=8)

        # Set axis limits and ticks
        if vote_type == 'IPEV':
            ax[i,j].set_xlim(3, 10)
        else:
            ax[i,j].set_xlim(3, 29)
            ax[i,j].set_xticks(np.arange(3, 30, 3))
        ax[i,j].invert_xaxis()
        ax[i,j].set_ylim(0, 70)
        ax[i,j].grid(True)

        ax[i,j].legend(loc='lower left')

plt.tight_layout()
plt.show()