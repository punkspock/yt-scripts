"""
Sydney Whilden
08/14/2020

Plot all ions of oxygen, same way Eric did.
"""
import OH_fields as oh
import matplotlib.pyplot as plt

if __name__ == "__main__":
    ds, ad = oh.loadData(oh.file)
    oh.addFields()
    cut = oh.velocityCut(ad)

    # plot over log of temperature
    x = oh.np.log10(cut['temperature'])

    o1 = cut['o   ']/cut['t_o']
    o2 = cut['o1  ']/cut['t_o']
    o3 = cut['o2  ']/cut['t_o']
    o4 = cut['o3  ']/cut['t_o']
    o5 = cut['o4  ']/cut['t_o']
    o6 = cut['o5  ']/cut['t_o']
    o7 = cut['o6  ']/cut['t_o']
    o8 = cut['o7  ']/cut['t_o']
    o9 = cut['o8  ']/cut['t_o']

    fig, axs = plt.subplots(1, 3, sharex=True, sharey=True)
    axs[0].scatter(x, o1, c='b', label='O I', s=4)
    axs[0].scatter(x, o2, c='g', label='O II', s=4)
    axs[0].scatter(x, o3, c='r', label='O III', s=4)
    axs[1].scatter(x, o4, c='c', label='O IV', s=4)
    axs[1].scatter(x, o5, c='m', label='O V', s=4)
    axs[1].scatter(x, o6, c='y', label='O VI', s=4)
    axs[2].scatter(x, o7, c='k', label='O VII', s=4)
    axs[2].scatter(x, o8, c='fuchsia', label='O VIII', s=4)
    axs[2].scatter(x, o9, c='chartreuse', label='O IX', s=4)
    fig.text(0.5, 0.04, 'Log(T)', ha='center')
    fig.text(
        0.04, 0.5, 'Ionization Fraction of Oxygen Ions', va='center',
        rotation='vertical'
        )
    axs[0].legend()
    axs[1].legend()
    axs[2].legend()
    plt.savefig('../Plots/scatter_all_O.png')
    plt.close()
