# Plot the Gnat & Sternberg (2007) data from ADS

import read_gnat as rg
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # read in data
    df = rg.readGnat()
    x, y = rg.logData(df)

    # plot
    fig, ax = plt.subplots(1, 1)
    ax.plot(x, y, color='c', linewidth=4, label="Gnat & Sternberg (2007)")
    ax.set_ylim(-4, 0)
    ax.set_title(r'O VI/O vs. Temperature')
    ax.set_xlabel(r"$\log{T}$")
    ax.set_ylabel(r"$\log{\text{(O VI/O)}}$")
    ax.legend()
    plt.savefig('../../Plots/gnat2007.png')
    plt.close()
