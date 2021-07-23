"""

06082021
Sydney Whilden

Plot data of ionization fraction over all 200 epochs.

"""

import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":
    file = '../../Plots/if_over_time.csv'
    headers = ['Times', 'O VI', 'O', 'O VI/O']
    df = pd.read_csv(file, sep=',', header=0, names=headers)

    times = df['Times']
    ovi = df['O VI']
    o = df['O']
    ion_frac_vals = df['O VI/O']

    ion_fracs = []
    ion_fracs.append(0.0)  # deal w/ first line
    for val in ion_frac_vals[1:]:
        val = val[0:len(val) - 13]  # remove 'dimensionless'
        val = val.strip()  #  remove leading/trailing white space
        val = float(val)  # turn to float
        ion_fracs.append(val)  # add to list

    sembach = []
    for time in times:
        sembach.append(0.2)

    # Plot
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(times, ion_fracs)
    ax.plot(times, sembach, color='r')
	ax.set_title('O VI/O over time')
	ax.set_xlabel('Epoch (Myr)')
	ax.set_ylabel('O VI/O')
	plt.savefig('../../Plots/if_over_time.png')
