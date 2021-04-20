import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def readGnat():
    headers=['Temp', 'OVI/O']
    df = pd.read_csv('../../Data/gnatsternbergOVI.dat', sep=' ', header=None,
        usecols=[0, 26], names=headers)

    return df


def logData(df):
    logTemp = []
    logIon = []
    for temp, ion_frac in zip(df['Temp'], df['OVI/O']):
        logTemp.append(np.log10(temp))
        logIon.append(np.log10(ion_frac))

    return logTemp, logIon


def plotGnat(x, y):
    fig, ax = plt.subplots(1, 1)
    ax.plot(x, y)
    # ax.plot(df['Temp'], df['OVI/O'])
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    ax.set_ylim(-2.5, 0)
    ax.set_xlim(5.0, 6.0)
    ax.set_title('Gnat & Sternberg curve O VI/O')
    plt.savefig('../../Plots/g&s2007.png')

    return


if __name__ == "__main__":
    df = readGnat()
    logTemp, logIon = logData(df)
    plotGnat(logTemp, logIon)
