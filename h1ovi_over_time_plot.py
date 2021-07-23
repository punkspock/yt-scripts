"""
06072021
Sydney Whilden

Plot the output from h1ovi_over_time.py

"""
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

    file = "../../Plots/hi_ovi.csv"

    headers = ['times', 'H I', 'O VI', 'H I/O VI']
    df = pd.read_csv(file, sep=',', header=0, names=headers)

    times = df['times']
    hi = df['H I']
    ovi = df['O VI']


    hi_ovi_vals = df['H I/O VI']
    hi_ovi = []  # initialize
    hi_ovi.append(0.0)  #  first line isn't a string so deal differently
    for val in hi_ovi_vals[1:]:  # remaining lines
        val = val[0:len(val) - 13]  # remove 'dimensionless' at end
        val = val.strip()  # get rid of leading/trailing white spaces
        val = float(val)  # convert to float
        hi_ovi.append(val)

    sembach = []
    for time in times:
        sembach.append(528982.98)

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(times, hi_ovi, color='b', label='Us')
    ax.plot(times, sembach, color='r', label='Sembach')
    ax.set_xlabel('Epoch (Myr)')
    ax.set_ylabel('H I/O VI')
    ax.set_title('H I/O VI Over Time')
    ax.legend()
    plt.savefig('../../Plots/hi_ovi_over_time.png')
